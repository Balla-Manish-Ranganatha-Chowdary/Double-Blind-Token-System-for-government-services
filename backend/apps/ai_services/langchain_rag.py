"""
LangChain-based Agentic RAG Implementation
Uses LangChain and LangGraph for advanced multi-agent workflows
"""

from typing import Dict, List, Optional, TypedDict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama


class AgentState(TypedDict):
    """State shared between agents in the graph"""
    query: str
    documents: List[Document]
    relevant_docs: List[Document]
    answer: str
    confidence: float
    needs_retrieval: bool
    is_valid: bool
    retry_count: int


class LangChainAgenticRAG:
    """
    Agentic RAG using LangChain and LangGraph
    Multi-agent workflow: Router → Retriever → Grader → Generator → Validator
    """
    
    def __init__(self, use_local_llm: bool = True):
        """
        Initialize LangChain Agentic RAG
        
        Args:
            use_local_llm: If True, uses Ollama (free local). If False, uses OpenAI
        """
        self.use_local_llm = use_local_llm
        
        # Initialize embeddings (free, runs locally)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize LLM
        if use_local_llm:
            # Free local LLM using Ollama
            self.llm = Ollama(model="llama2")
        else:
            # OpenAI (requires API key)
            from langchain.llms import OpenAI
            self.llm = OpenAI(temperature=0)
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        
        # Initialize vector store (will be populated with documents)
        self.vectorstore = None
        
        # Build the agent graph
        self.graph = self._build_agent_graph()
    
    def index_documents(self, documents: List[Dict[str, str]]):
        """
        Index documents into vector store
        
        Args:
            documents: List of dicts with 'id' and 'text' keys
        """
        # Convert to LangChain Document objects
        docs = [
            Document(
                page_content=doc['text'],
                metadata={'id': doc['id']}
            )
            for doc in documents
        ]
        
        # Split documents into chunks
        split_docs = self.text_splitter.split_documents(docs)
        
        # Create vector store
        self.vectorstore = FAISS.from_documents(split_docs, self.embeddings)
    
    def _build_agent_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes (agents)
        workflow.add_node("router", self._router_agent)
        workflow.add_node("retriever", self._retriever_agent)
        workflow.add_node("grader", self._grader_agent)
        workflow.add_node("generator", self._generator_agent)
        workflow.add_node("validator", self._validator_agent)
        
        # Define edges (workflow)
        workflow.set_entry_point("router")
        
        # Router decides: retrieve or answer directly
        workflow.add_conditional_edges(
            "router",
            self._route_decision,
            {
                "retrieve": "retriever",
                "direct": "generator"
            }
        )
        
        # After retrieval, grade documents
        workflow.add_edge("retriever", "grader")
        
        # After grading, generate answer
        workflow.add_edge("grader", "generator")
        
        # After generation, validate
        workflow.add_edge("generator", "validator")
        
        # Validator decides: accept or retry
        workflow.add_conditional_edges(
            "validator",
            self._validation_decision,
            {
                "accept": END,
                "retry": "retriever"
            }
        )
        
        return workflow.compile()
    
    def _router_agent(self, state: AgentState) -> AgentState:
        """
        Router Agent: Decides if retrieval is needed
        """
        query = state['query']
        
        # Simple heuristic: if query is complex, retrieve
        # In production, use LLM to make this decision
        needs_retrieval = len(query.split()) > 5 or '?' in query
        
        state['needs_retrieval'] = needs_retrieval
        state['retry_count'] = 0
        
        return state
    
    def _retriever_agent(self, state: AgentState) -> AgentState:
        """
        Retriever Agent: Retrieves relevant documents
        """
        if not self.vectorstore:
            state['documents'] = []
            return state
        
        query = state['query']
        
        # Retrieve top-k documents
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        docs = retriever.get_relevant_documents(query)
        
        state['documents'] = docs
        
        return state
    
    def _grader_agent(self, state: AgentState) -> AgentState:
        """
        Grader Agent: Grades relevance of retrieved documents
        """
        query = state['query']
        documents = state['documents']
        
        # Grade each document for relevance
        relevant_docs = []
        
        for doc in documents:
            # Simple relevance check (in production, use LLM)
            query_terms = set(query.lower().split())
            doc_terms = set(doc.page_content.lower().split())
            
            # Calculate overlap
            overlap = len(query_terms & doc_terms)
            relevance_score = overlap / len(query_terms) if query_terms else 0
            
            if relevance_score > 0.3:  # Threshold
                relevant_docs.append(doc)
        
        state['relevant_docs'] = relevant_docs
        
        return state
    
    def _generator_agent(self, state: AgentState) -> AgentState:
        """
        Generator Agent: Generates answer from documents
        """
        query = state['query']
        relevant_docs = state.get('relevant_docs', [])
        
        if not relevant_docs:
            # No relevant docs, generate generic answer
            state['answer'] = "I don't have enough information to answer this question."
            state['confidence'] = 0.3
            return state
        
        # Create context from relevant documents
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Create prompt
        prompt_template = """
        Based on the following context, answer the question.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Generate answer using LLM
        formatted_prompt = prompt.format(context=context, question=query)
        answer = self.llm(formatted_prompt)
        
        state['answer'] = answer.strip()
        state['confidence'] = 0.8  # High confidence with relevant docs
        
        return state
    
    def _validator_agent(self, state: AgentState) -> AgentState:
        """
        Validator Agent: Validates the generated answer
        """
        answer = state['answer']
        relevant_docs = state.get('relevant_docs', [])
        retry_count = state.get('retry_count', 0)
        
        # Validation logic
        if not answer or len(answer) < 10:
            # Answer too short
            state['is_valid'] = False
        elif not relevant_docs:
            # No supporting documents
            state['is_valid'] = False
        else:
            # Check if answer is grounded in documents
            answer_terms = set(answer.lower().split())
            doc_terms = set()
            for doc in relevant_docs:
                doc_terms.update(doc.page_content.lower().split())
            
            # Calculate grounding score
            grounding = len(answer_terms & doc_terms) / len(answer_terms) if answer_terms else 0
            
            state['is_valid'] = grounding > 0.5 or retry_count >= 2
        
        return state
    
    def _route_decision(self, state: AgentState) -> str:
        """Decide routing after router agent"""
        return "retrieve" if state['needs_retrieval'] else "direct"
    
    def _validation_decision(self, state: AgentState) -> str:
        """Decide routing after validator agent"""
        if state['is_valid']:
            return "accept"
        elif state['retry_count'] < 2:
            state['retry_count'] += 1
            return "retry"
        else:
            return "accept"  # Accept after max retries
    
    def query(self, query: str) -> Dict:
        """
        Query the Agentic RAG system
        
        Args:
            query: User query
            
        Returns:
            Dict with answer, confidence, and metadata
        """
        # Initialize state
        initial_state: AgentState = {
            'query': query,
            'documents': [],
            'relevant_docs': [],
            'answer': '',
            'confidence': 0.0,
            'needs_retrieval': False,
            'is_valid': False,
            'retry_count': 0
        }
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        return {
            'answer': final_state['answer'],
            'confidence': final_state['confidence'],
            'sources': [doc.metadata for doc in final_state.get('relevant_docs', [])],
            'retry_count': final_state['retry_count']
        }


class LangChainGraphRAG:
    """
    GraphRAG implementation using LangChain
    Knowledge graph-based retrieval with multi-hop reasoning
    """
    
    def __init__(self):
        """Initialize GraphRAG with LangChain"""
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.llm = Ollama(model="llama2")
        
        # Knowledge graph structure
        self.entities = {}  # entity_id -> entity_data
        self.relationships = []  # (entity1, relation, entity2)
        self.vectorstore = None
    
    def build_knowledge_graph(self, documents: List[Dict[str, str]]):
        """
        Build knowledge graph from documents
        
        Args:
            documents: List of documents with 'id' and 'text'
        """
        # Extract entities and relationships
        for doc in documents:
            # Simple entity extraction (in production, use NER)
            entities = self._extract_entities(doc['text'])
            
            for entity in entities:
                entity_id = f"{doc['id']}_{entity}"
                self.entities[entity_id] = {
                    'name': entity,
                    'document_id': doc['id'],
                    'text': doc['text']
                }
        
        # Create vector store for entities
        entity_docs = [
            Document(
                page_content=data['text'],
                metadata={'entity_id': eid, 'name': data['name']}
            )
            for eid, data in self.entities.items()
        ]
        
        self.vectorstore = FAISS.from_documents(entity_docs, self.embeddings)
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract entities from text (simplified)"""
        # In production, use spaCy or other NER
        words = text.split()
        # Extract capitalized words as entities
        entities = [w for w in words if w[0].isupper() and len(w) > 3]
        return list(set(entities))[:5]  # Top 5 unique entities
    
    def query_with_graph(self, query: str, max_hops: int = 2) -> Dict:
        """
        Query using knowledge graph with multi-hop reasoning
        
        Args:
            query: User query
            max_hops: Maximum number of hops in graph traversal
            
        Returns:
            Dict with answer and graph metadata
        """
        if not self.vectorstore:
            return {
                'answer': 'Knowledge graph not initialized',
                'entities': [],
                'hops': 0
            }
        
        # Find relevant entities
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(query)
        
        # Extract entities from retrieved docs
        entities = [doc.metadata['name'] for doc in docs]
        
        # Multi-hop reasoning (simplified)
        context = "\n".join([doc.page_content for doc in docs])
        
        # Generate answer
        prompt = f"""
        Based on the following information from the knowledge graph:
        
        {context}
        
        Answer the question: {query}
        
        Answer:
        """
        
        answer = self.llm(prompt)
        
        return {
            'answer': answer.strip(),
            'entities': entities,
            'hops': min(len(entities), max_hops),
            'sources': [doc.metadata for doc in docs]
        }


# Example usage
if __name__ == "__main__":
    # Initialize Agentic RAG
    rag = LangChainAgenticRAG(use_local_llm=True)
    
    # Index documents
    documents = [
        {
            "id": "doc1",
            "text": "Land record certificates require property deed, survey number, and identity proof. Processing time is 7-10 days."
        },
        {
            "id": "doc2",
            "text": "Police verification for passport requires address proof, identity proof, and passport application. Processing time is 15 days."
        }
    ]
    
    rag.index_documents(documents)
    
    # Query
    result = rag.query("How long does land record certificate take?")
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Sources: {result['sources']}")
