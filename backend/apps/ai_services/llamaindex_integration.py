"""
LlamaIndex Integration for Agentic RAG System
Provides vector indexing, retrieval, and agent orchestration
"""

from typing import Dict, List, Optional
from llama_index.core import (
    VectorStoreIndex,
    Document,
    Settings,
    StorageContext,
    load_index_from_storage
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.memory import ChatMemoryBuffer
import os


class LlamaIndexRAGSystem:
    """
    Complete RAG system using LlamaIndex
    Integrates with existing Agentic RAG agents
    """
    
    def __init__(
        self,
        llm_model: str = "gpt-4",
        embedding_model: str = "text-embedding-3-small",
        persist_dir: str = "./storage"
    ):
        # Configure LlamaIndex settings
        Settings.llm = OpenAI(
            model=llm_model,
            temperature=0.1,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        Settings.embed_model = OpenAIEmbedding(
            model=embedding_model,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50
        
        self.persist_dir = persist_dir
        self.indexes = {}
        self.query_engines = {}
        self.agents = {}
    
    def create_index(
        self,
        documents: List[Dict],
        index_name: str = "default"
    ) -> VectorStoreIndex:
        """
        Create vector index from documents
        
        Args:
            documents: List of documents with 'text' and 'metadata'
            index_name: Name for the index
            
        Returns:
            VectorStoreIndex
        """
        # Convert to LlamaIndex Document format
        llama_docs = [
            Document(
                text=doc.get('text', ''),
                metadata=doc.get('metadata', {}),
                id_=doc.get('id', f"doc_{i}")
            )
            for i, doc in enumerate(documents)
        ]
        
        # Create index
        index = VectorStoreIndex.from_documents(
            llama_docs,
            show_progress=True
        )
        
        # Persist index
        index.storage_context.persist(
            persist_dir=f"{self.persist_dir}/{index_name}"
        )
        
        self.indexes[index_name] = index
        return index
    
    def load_index(self, index_name: str = "default") -> VectorStoreIndex:
        """Load existing index from storage"""
        storage_context = StorageContext.from_defaults(
            persist_dir=f"{self.persist_dir}/{index_name}"
        )
        index = load_index_from_storage(storage_context)
        self.indexes[index_name] = index
        return index
    
    def create_query_engine(
        self,
        index_name: str = "default",
        similarity_top_k: int = 5,
        similarity_cutoff: float = 0.7
    ):
        """
        Create query engine with retrieval and post-processing
        
        Args:
            index_name: Name of index to query
            similarity_top_k: Number of chunks to retrieve
            similarity_cutoff: Minimum similarity score
        """
        index = self.indexes.get(index_name)
        if not index:
            raise ValueError(f"Index '{index_name}' not found")
        
        # Configure retriever
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=similarity_top_k
        )
        
        # Add post-processor for filtering
        postprocessor = SimilarityPostprocessor(
            similarity_cutoff=similarity_cutoff
        )
        
        # Create query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[postprocessor]
        )
        
        self.query_engines[index_name] = query_engine
        return query_engine
    
    def query(
        self,
        query: str,
        index_name: str = "default"
    ) -> Dict:
        """
        Query the RAG system
        
        Args:
            query: User query
            index_name: Index to query
            
        Returns:
            Dict with answer and sources
        """
        query_engine = self.query_engines.get(index_name)
        if not query_engine:
            query_engine = self.create_query_engine(index_name)
        
        # Execute query
        response = query_engine.query(query)
        
        # Extract sources
        sources = []
        for node in response.source_nodes:
            sources.append({
                'text': node.node.text,
                'score': node.score,
                'metadata': node.node.metadata
            })
        
        return {
            'answer': str(response),
            'sources': sources,
            'confidence': sources[0]['score'] if sources else 0.0
        }


class LlamaIndexAgenticRAG:
    """
    Agentic RAG using LlamaIndex ReActAgent
    Router → Grader → Validator implemented as LlamaIndex agents
    """
    
    def __init__(self, llm_model: str = "gpt-4"):
        self.llm = OpenAI(
            model=llm_model,
            temperature=0.1,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.rag_system = LlamaIndexRAGSystem(llm_model=llm_model)
        self.memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
    
    def create_router_agent(self, index_name: str = "default"):
        """
        Create Router Agent using LlamaIndex ReActAgent
        Decides if retrieval is needed
        """
        # Create query tool
        query_engine = self.rag_system.query_engines.get(index_name)
        if not query_engine:
            query_engine = self.rag_system.create_query_engine(index_name)
        
        query_tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="knowledge_base",
                description="Search government policies and procedures knowledge base. Use this when query requires specific policy information."
            )
        )
        
        # Create ReAct agent
        agent = ReActAgent.from_tools(
            tools=[query_tool],
            llm=self.llm,
            memory=self.memory,
            verbose=True,
            system_prompt="""You are a Router Agent for a government services RAG system.

Your job:
1. Analyze if the query is simple (definitions, general info) or complex (specific policies, procedures)
2. For simple queries: Answer directly without using tools
3. For complex queries: Use the knowledge_base tool to retrieve information

Always explain your reasoning before deciding."""
        )
        
        self.agents['router'] = agent
        return agent
    
    def create_grader_agent(self):
        """
        Create Grader Agent to validate retrieved chunks
        """
        grader_prompt = """You are a Grader Agent for a RAG system.

Your job:
1. Evaluate if retrieved information is relevant to the query
2. Grade each source as RELEVANT, PARTIALLY_RELEVANT, or NOT_RELEVANT
3. Decide if we should retry with a rewritten query
4. Filter out low-quality sources

Return your assessment in this format:
- Overall Quality: GOOD/POOR
- Should Retry: YES/NO
- Reasoning: [your explanation]
"""
        
        agent = ReActAgent.from_tools(
            tools=[],  # Grader doesn't need tools, just evaluates
            llm=self.llm,
            memory=self.memory,
            verbose=True,
            system_prompt=grader_prompt
        )
        
        self.agents['grader'] = agent
        return agent
    
    def create_validator_agent(self):
        """
        Create Validator Agent to check for hallucinations
        """
        validator_prompt = """You are a Validator Agent for a RAG system.

Your job:
1. Check if the generated answer is grounded in the provided sources
2. Identify any hallucinations or unsupported claims
3. Verify no contradictions with sources
4. Decide if answer should be regenerated

Return your assessment:
- Is Valid: YES/NO
- Confidence: 0.0-1.0
- Hallucinations Found: [list]
- Should Retry: YES/NO
"""
        
        agent = ReActAgent.from_tools(
            tools=[],
            llm=self.llm,
            memory=self.memory,
            verbose=True,
            system_prompt=validator_prompt
        )
        
        self.agents['validator'] = agent
        return agent
    
    def process_query(
        self,
        query: str,
        index_name: str = "default",
        max_retries: int = 3
    ) -> Dict:
        """
        Process query through full agentic pipeline
        
        Args:
            query: User query
            index_name: Index to use
            max_retries: Maximum retry attempts
            
        Returns:
            Dict with answer and metadata
        """
        retry_count = 0
        
        # Step 1: Router Agent
        router = self.agents.get('router')
        if not router:
            router = self.create_router_agent(index_name)
        
        router_response = router.chat(f"""
Query: {query}

Should I retrieve from knowledge base or answer directly?
""")
        
        # Check if router decided to skip retrieval
        if "answer directly" in str(router_response).lower():
            return {
                'answer': str(router_response),
                'pipeline': 'router_direct',
                'confidence': 0.9,
                'sources': []
            }
        
        # Step 2: Retrieve and Grade
        while retry_count < max_retries:
            # Retrieve
            rag_result = self.rag_system.query(query, index_name)
            
            # Grade
            grader = self.agents.get('grader')
            if not grader:
                grader = self.create_grader_agent()
            
            grader_response = grader.chat(f"""
Query: {query}

Retrieved Sources:
{self._format_sources(rag_result['sources'])}

Grade these sources for relevance.
""")
            
            # Check if grading passed
            if "GOOD" in str(grader_response).upper():
                break
            
            # Rewrite query and retry
            query = self._rewrite_query(query, retry_count)
            retry_count += 1
        
        # Step 3: Validate Answer
        validator = self.agents.get('validator')
        if not validator:
            validator = self.create_validator_agent()
        
        validator_response = validator.chat(f"""
Query: {query}

Generated Answer: {rag_result['answer']}

Sources:
{self._format_sources(rag_result['sources'])}

Validate if answer is grounded in sources.
""")
        
        # Check validation
        is_valid = "YES" in str(validator_response).upper()
        
        return {
            'answer': rag_result['answer'],
            'sources': rag_result['sources'],
            'confidence': rag_result['confidence'],
            'pipeline': 'full_agentic_llamaindex',
            'validation': 'passed' if is_valid else 'failed',
            'retries': retry_count,
            'metadata': {
                'router_decision': str(router_response)[:200],
                'grader_assessment': str(grader_response)[:200],
                'validator_result': str(validator_response)[:200]
            }
        }
    
    def _format_sources(self, sources: List[Dict]) -> str:
        """Format sources for agent prompts"""
        formatted = []
        for i, source in enumerate(sources[:3]):  # Top 3 sources
            formatted.append(f"Source {i+1} (score: {source['score']:.2f}):\n{source['text'][:200]}...")
        return "\n\n".join(formatted)
    
    def _rewrite_query(self, query: str, attempt: int) -> str:
        """Rewrite query for better retrieval"""
        rewrites = [
            f"Detailed information about: {query}",
            f"Explain the process and requirements for: {query}",
            f"What are the official guidelines for: {query}"
        ]
        return rewrites[min(attempt, len(rewrites) - 1)]


class LlamaIndexGraphRAG:
    """
    GraphRAG implementation using LlamaIndex Knowledge Graph
    """
    
    def __init__(self, llm_model: str = "gpt-4"):
        from llama_index.core import KnowledgeGraphIndex
        from llama_index.core.graph_stores import SimpleGraphStore
        
        self.llm = OpenAI(model=llm_model, api_key=os.getenv('OPENAI_API_KEY'))
        self.graph_store = SimpleGraphStore()
        self.kg_index = None
    
    def create_knowledge_graph(
        self,
        documents: List[Dict],
        max_triplets_per_chunk: int = 10
    ):
        """
        Create knowledge graph from documents
        
        Args:
            documents: List of documents
            max_triplets_per_chunk: Max entity-relationship triplets per chunk
        """
        from llama_index.core import KnowledgeGraphIndex
        
        # Convert to LlamaIndex documents
        llama_docs = [
            Document(text=doc.get('text', ''), metadata=doc.get('metadata', {}))
            for doc in documents
        ]
        
        # Create knowledge graph index
        self.kg_index = KnowledgeGraphIndex.from_documents(
            llama_docs,
            max_triplets_per_chunk=max_triplets_per_chunk,
            storage_context=StorageContext.from_defaults(graph_store=self.graph_store),
            show_progress=True
        )
        
        return self.kg_index
    
    def query_graph(
        self,
        query: str,
        include_text: bool = True,
        retriever_mode: str = "keyword"
    ) -> Dict:
        """
        Query knowledge graph with multi-hop reasoning
        
        Args:
            query: Search query
            include_text: Include source text in response
            retriever_mode: 'keyword' or 'embedding'
        """
        if not self.kg_index:
            raise ValueError("Knowledge graph not created. Call create_knowledge_graph first.")
        
        # Create query engine
        query_engine = self.kg_index.as_query_engine(
            include_text=include_text,
            retriever_mode=retriever_mode,
            response_mode="tree_summarize"
        )
        
        # Execute query
        response = query_engine.query(query)
        
        return {
            'answer': str(response),
            'graph_context': response.source_nodes,
            'pipeline': 'graph_rag_llamaindex'
        }


# Export classes
__all__ = [
    'LlamaIndexRAGSystem',
    'LlamaIndexAgenticRAG',
    'LlamaIndexGraphRAG'
]
