"""
LlamaIndex Integration with LOCAL Models - NO API Keys Required
100% Free, runs on your machine
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

# LOCAL MODELS - NO API KEYS
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.llms.huggingface import HuggingFaceLLM


class LocalLlamaIndexRAG:
    """
    Complete RAG system using LOCAL models
    NO OpenAI API key needed - 100% FREE
    """
    
    def __init__(
        self,
        embedding_model: str = "BAAI/bge-small-en-v1.5",
        llm_model: str = "llama2",  # Ollama model
        use_ollama: bool = True,
        persist_dir: str = "./storage"
    ):
        """
        Initialize with local models
        
        Args:
            embedding_model: HuggingFace embedding model (free)
            llm_model: Ollama model name (free) or HuggingFace model
            use_ollama: Use Ollama (recommended) or HuggingFace
            persist_dir: Storage directory
        """
        
        # Configure LOCAL embedding model (FREE)
        print("Loading local embedding model...")
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=embedding_model,
            cache_folder="./models"
        )
        
        # Configure LOCAL LLM (FREE)
        if use_ollama:
            # Ollama - Best option for local LLMs
            print("Using Ollama for LLM (make sure Ollama is running)")
            Settings.llm = Ollama(
                model=llm_model,
                request_timeout=120.0
            )
        else:
            # HuggingFace - Alternative local option
            print("Loading local LLM from HuggingFace...")
            Settings.llm = HuggingFaceLLM(
                model_name="HuggingFaceH4/zephyr-7b-beta",
                tokenizer_name="HuggingFaceH4/zephyr-7b-beta",
                context_window=3900,
                max_new_tokens=256,
                generate_kwargs={"temperature": 0.1, "do_sample": False},
                device_map="auto"
            )
        
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50
        
        self.persist_dir = persist_dir
        self.indexes = {}
        self.query_engines = {}
        
        print("✓ Local RAG system initialized (no API keys needed)")
    
    def create_index(
        self,
        documents: List[Dict],
        index_name: str = "default"
    ) -> VectorStoreIndex:
        """Create vector index using local embeddings"""
        
        # Convert to LlamaIndex documents
        llama_docs = [
            Document(
                text=doc.get('text', ''),
                metadata=doc.get('metadata', {}),
                id_=doc.get('id', f"doc_{i}")
            )
            for i, doc in enumerate(documents)
        ]
        
        print(f"Creating index with {len(llama_docs)} documents...")
        
        # Create index with local embeddings
        index = VectorStoreIndex.from_documents(
            llama_docs,
            show_progress=True
        )
        
        # Persist
        index.storage_context.persist(
            persist_dir=f"{self.persist_dir}/{index_name}"
        )
        
        self.indexes[index_name] = index
        print(f"✓ Index '{index_name}' created and saved")
        return index
    
    def load_index(self, index_name: str = "default") -> VectorStoreIndex:
        """Load existing index"""
        storage_context = StorageContext.from_defaults(
            persist_dir=f"{self.persist_dir}/{index_name}"
        )
        index = load_index_from_storage(storage_context)
        self.indexes[index_name] = index
        return index
    
    def create_query_engine(
        self,
        index_name: str = "default",
        similarity_top_k: int = 3,
        similarity_cutoff: float = 0.6
    ):
        """Create query engine"""
        index = self.indexes.get(index_name)
        if not index:
            raise ValueError(f"Index '{index_name}' not found")
        
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=similarity_top_k
        )
        
        postprocessor = SimilarityPostprocessor(
            similarity_cutoff=similarity_cutoff
        )
        
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
        """Query using local models"""
        query_engine = self.query_engines.get(index_name)
        if not query_engine:
            query_engine = self.create_query_engine(index_name)
        
        print(f"Querying: {query}")
        response = query_engine.query(query)
        
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
            'confidence': sources[0]['score'] if sources else 0.0,
            'model': 'local'
        }


class LocalAgenticRAG:
    """
    Agentic RAG with local models
    Router → Grader → Validator using local LLMs
    """
    
    def __init__(
        self,
        embedding_model: str = "BAAI/bge-small-en-v1.5",
        llm_model: str = "llama2"
    ):
        self.rag = LocalLlamaIndexRAG(
            embedding_model=embedding_model,
            llm_model=llm_model
        )
        print("✓ Local Agentic RAG initialized")
    
    def process_query(
        self,
        query: str,
        index_name: str = "default",
        max_retries: int = 2
    ) -> Dict:
        """
        Process query through agentic pipeline using local models
        """
        retry_count = 0
        
        # Step 1: Router - Check if simple query
        if self._is_simple_query(query):
            return {
                'answer': self._answer_simple_query(query),
                'pipeline': 'router_direct',
                'confidence': 0.9,
                'sources': [],
                'model': 'local'
            }
        
        # Step 2: Retrieve and grade
        while retry_count < max_retries:
            result = self.rag.query(query, index_name)
            
            # Grade results
            if result['confidence'] > 0.7:
                # Good results, validate
                is_valid = self._validate_answer(
                    query,
                    result['answer'],
                    result['sources']
                )
                
                if is_valid:
                    return {
                        **result,
                        'pipeline': 'full_agentic_local',
                        'validation': 'passed',
                        'retries': retry_count
                    }
            
            # Retry with rewritten query
            query = self._rewrite_query(query, retry_count)
            retry_count += 1
        
        return {
            **result,
            'pipeline': 'agentic_local_max_retries',
            'retries': retry_count
        }
    
    def _is_simple_query(self, query: str) -> bool:
        """Router logic - local, no LLM needed"""
        simple_patterns = ['what is', 'define', 'meaning of']
        return any(p in query.lower() for p in simple_patterns) and len(query.split()) < 8
    
    def _answer_simple_query(self, query: str) -> str:
        """Answer simple queries without retrieval"""
        return f"This is a simple query that can be answered directly: {query}"
    
    def _validate_answer(self, query: str, answer: str, sources: List[Dict]) -> bool:
        """Validator logic - check grounding"""
        if not sources:
            return False
        
        # Simple validation: check if answer words appear in sources
        answer_words = set(answer.lower().split())
        source_text = " ".join([s['text'].lower() for s in sources])
        source_words = set(source_text.split())
        
        overlap = len(answer_words.intersection(source_words))
        grounding_score = overlap / len(answer_words) if answer_words else 0
        
        return grounding_score > 0.6
    
    def _rewrite_query(self, query: str, attempt: int) -> str:
        """Rewrite query for better results"""
        rewrites = [
            f"detailed information about {query}",
            f"explain {query} in detail",
            f"what are the requirements for {query}"
        ]
        return rewrites[min(attempt, len(rewrites) - 1)]


class LocalGraphRAG:
    """
    GraphRAG with local models
    Knowledge graph without API keys
    """
    
    def __init__(self):
        from llama_index.core import KnowledgeGraphIndex
        from llama_index.core.graph_stores import SimpleGraphStore
        
        # Use local embedding
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        
        # Use Ollama for LLM
        Settings.llm = Ollama(model="llama2")
        
        self.graph_store = SimpleGraphStore()
        self.kg_index = None
        
        print("✓ Local GraphRAG initialized")
    
    def create_knowledge_graph(
        self,
        documents: List[Dict],
        max_triplets_per_chunk: int = 5
    ):
        """Create knowledge graph using local LLM"""
        from llama_index.core import KnowledgeGraphIndex
        
        llama_docs = [
            Document(text=doc.get('text', ''), metadata=doc.get('metadata', {}))
            for doc in documents
        ]
        
        print("Building knowledge graph with local LLM...")
        
        self.kg_index = KnowledgeGraphIndex.from_documents(
            llama_docs,
            max_triplets_per_chunk=max_triplets_per_chunk,
            storage_context=StorageContext.from_defaults(graph_store=self.graph_store),
            show_progress=True
        )
        
        print("✓ Knowledge graph created")
        return self.kg_index
    
    def query_graph(self, query: str) -> Dict:
        """Query graph with local models"""
        if not self.kg_index:
            raise ValueError("Create knowledge graph first")
        
        query_engine = self.kg_index.as_query_engine(
            include_text=True,
            response_mode="tree_summarize"
        )
        
        response = query_engine.query(query)
        
        return {
            'answer': str(response),
            'pipeline': 'graph_rag_local',
            'model': 'local'
        }


# Export classes
__all__ = [
    'LocalLlamaIndexRAG',
    'LocalAgenticRAG',
    'LocalGraphRAG'
]
