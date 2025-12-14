"""
Agentic RAG System - Self-correcting multi-agent pipeline
Router → Grader → Validator with feedback loops
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json


class AgentDecision(Enum):
    """Agent decision outcomes"""
    PROCEED = "proceed"
    RETRY = "retry"
    SKIP = "skip"
    FAIL = "fail"


@dataclass
class AgentResult:
    """Result from an agent"""
    decision: AgentDecision
    confidence: float
    reasoning: str
    data: Optional[Dict] = None
    retry_count: int = 0


class RouterAgent:
    """
    Router Agent - Decides if retrieval is needed
    "Can I answer this directly or do I need to retrieve?"
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.max_confidence_threshold = 0.9
    
    def route(self, query: str, context: Dict) -> AgentResult:
        """
        Determine if query can be answered directly or needs retrieval
        
        Args:
            query: Input query/document
            context: Additional context
            
        Returns:
            AgentResult with routing decision
        """
        # Check if query is simple and can be answered directly
        simple_patterns = [
            "what is", "define", "explain", "how to"
        ]
        
        is_simple = any(pattern in query.lower() for pattern in simple_patterns)
        
        if is_simple and len(query.split()) < 10:
            return AgentResult(
                decision=AgentDecision.SKIP,
                confidence=0.95,
                reasoning="Query is simple and can be answered directly without retrieval",
                data={"route": "direct_answer"}
            )
        
        # For complex queries, route to retrieval
        return AgentResult(
            decision=AgentDecision.PROCEED,
            confidence=0.85,
            reasoning="Query requires retrieval from knowledge base",
            data={"route": "retrieval_needed"}
        )
    
    def can_answer_directly(self, query: str) -> Tuple[bool, str]:
        """Check if router can answer without retrieval"""
        # Implement direct answering logic
        # For now, return False to always use retrieval
        return False, ""


class GraderAgent:
    """
    Grader Agent - Validates retrieved chunks
    "Are these chunks relevant to the query?"
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.relevance_threshold = 0.7
    
    def grade_chunks(self, query: str, chunks: List[Dict]) -> AgentResult:
        """
        Grade retrieved chunks for relevance
        
        Args:
            query: Original query
            chunks: Retrieved document chunks
            
        Returns:
            AgentResult with grading decision
        """
        if not chunks:
            return AgentResult(
                decision=AgentDecision.RETRY,
                confidence=0.0,
                reasoning="No chunks retrieved, need to rewrite query",
                data={"relevant_chunks": []}
            )
        
        # Grade each chunk for relevance
        relevant_chunks = []
        total_relevance = 0.0
        
        for chunk in chunks:
            relevance_score = self._calculate_relevance(query, chunk)
            total_relevance += relevance_score
            
            if relevance_score >= self.relevance_threshold:
                relevant_chunks.append({
                    **chunk,
                    "relevance_score": relevance_score
                })
        
        avg_relevance = total_relevance / len(chunks) if chunks else 0.0
        
        if not relevant_chunks:
            return AgentResult(
                decision=AgentDecision.RETRY,
                confidence=avg_relevance,
                reasoning="Retrieved chunks not relevant, rewriting query",
                data={"relevant_chunks": [], "avg_relevance": avg_relevance}
            )
        
        return AgentResult(
            decision=AgentDecision.PROCEED,
            confidence=avg_relevance,
            reasoning=f"Found {len(relevant_chunks)} relevant chunks",
            data={"relevant_chunks": relevant_chunks, "avg_relevance": avg_relevance}
        )
    
    def _calculate_relevance(self, query: str, chunk: Dict) -> float:
        """Calculate relevance score between query and chunk"""
        # Simple keyword matching for now
        # In production, use semantic similarity with embeddings
        query_words = set(query.lower().split())
        chunk_text = chunk.get('text', '').lower()
        chunk_words = set(chunk_text.split())
        
        if not query_words or not chunk_words:
            return 0.0
        
        overlap = len(query_words.intersection(chunk_words))
        relevance = overlap / len(query_words)
        
        return min(relevance, 1.0)
    
    def rewrite_query(self, original_query: str, failed_attempt: Dict) -> str:
        """Rewrite query for better retrieval"""
        # Add context or rephrase for better results
        # In production, use LLM to rewrite
        return f"Detailed information about: {original_query}"


class ValidatorAgent:
    """
    Validator Agent - Validates generated answers
    "Does the answer match the sources? Is it hallucinating?"
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.validation_threshold = 0.8
    
    def validate_answer(self, query: str, answer: str, sources: List[Dict]) -> AgentResult:
        """
        Validate that answer is grounded in sources
        
        Args:
            query: Original query
            answer: Generated answer
            sources: Source chunks used
            
        Returns:
            AgentResult with validation decision
        """
        if not answer or not sources:
            return AgentResult(
                decision=AgentDecision.RETRY,
                confidence=0.0,
                reasoning="Empty answer or no sources provided",
                data={"is_valid": False}
            )
        
        # Check if answer is grounded in sources
        validation_score = self._validate_grounding(answer, sources)
        
        # Check for hallucination indicators
        hallucination_score = self._detect_hallucination(answer, sources)
        
        final_score = (validation_score * 0.7) + ((1 - hallucination_score) * 0.3)
        
        if final_score >= self.validation_threshold:
            return AgentResult(
                decision=AgentDecision.PROCEED,
                confidence=final_score,
                reasoning="Answer is well-grounded in sources",
                data={
                    "is_valid": True,
                    "validation_score": validation_score,
                    "hallucination_score": hallucination_score
                }
            )
        
        return AgentResult(
            decision=AgentDecision.RETRY,
            confidence=final_score,
            reasoning="Answer may contain hallucinations or unsupported claims",
            data={
                "is_valid": False,
                "validation_score": validation_score,
                "hallucination_score": hallucination_score
            }
        )
    
    def _validate_grounding(self, answer: str, sources: List[Dict]) -> float:
        """Check if answer statements are grounded in sources"""
        # Simple implementation: check if answer words appear in sources
        answer_words = set(answer.lower().split())
        
        source_text = " ".join([s.get('text', '') for s in sources]).lower()
        source_words = set(source_text.split())
        
        if not answer_words:
            return 0.0
        
        grounded_words = answer_words.intersection(source_words)
        grounding_score = len(grounded_words) / len(answer_words)
        
        return grounding_score
    
    def _detect_hallucination(self, answer: str, sources: List[Dict]) -> float:
        """Detect potential hallucinations in answer"""
        # Check for absolute statements not in sources
        hallucination_indicators = [
            "definitely", "certainly", "absolutely", "always", "never",
            "all", "none", "every", "no one"
        ]
        
        answer_lower = answer.lower()
        hallucination_count = sum(
            1 for indicator in hallucination_indicators 
            if indicator in answer_lower
        )
        
        # Normalize score
        hallucination_score = min(hallucination_count / 5, 1.0)
        
        return hallucination_score


class AgenticRAGPipeline:
    """
    Complete Agentic RAG Pipeline with feedback loops
    Router → Retrieve → Grader → Generate → Validator → Retry if needed
    """
    
    def __init__(self, vector_db=None, llm_client=None, max_retries: int = 3):
        self.router = RouterAgent(llm_client)
        self.grader = GraderAgent(llm_client)
        self.validator = ValidatorAgent(llm_client)
        self.vector_db = vector_db
        self.llm_client = llm_client
        self.max_retries = max_retries
    
    def process(self, query: str, context: Optional[Dict] = None) -> Dict:
        """
        Process query through agentic RAG pipeline
        
        Args:
            query: Input query
            context: Additional context
            
        Returns:
            Dict with answer and metadata
        """
        context = context or {}
        retry_count = 0
        
        # Step 1: Router - Check if retrieval needed
        router_result = self.router.route(query, context)
        
        if router_result.decision == AgentDecision.SKIP:
            # Can answer directly
            direct_answer = self.router.can_answer_directly(query)
            return {
                "answer": direct_answer[1],
                "confidence": router_result.confidence,
                "sources": [],
                "pipeline": "direct_answer",
                "metadata": {"router_decision": "skip_retrieval"}
            }
        
        # Step 2: Retrieval + Grading Loop
        current_query = query
        relevant_chunks = []
        
        while retry_count < self.max_retries:
            # Retrieve chunks
            chunks = self._retrieve_chunks(current_query)
            
            # Grade chunks
            grader_result = self.grader.grade_chunks(current_query, chunks)
            
            if grader_result.decision == AgentDecision.PROCEED:
                relevant_chunks = grader_result.data.get('relevant_chunks', [])
                break
            
            # Retry with rewritten query
            current_query = self.grader.rewrite_query(query, {
                "attempt": retry_count,
                "chunks": chunks
            })
            retry_count += 1
        
        if not relevant_chunks:
            return {
                "answer": "Unable to find relevant information after multiple attempts.",
                "confidence": 0.0,
                "sources": [],
                "pipeline": "failed_retrieval",
                "metadata": {"retries": retry_count}
            }
        
        # Step 3: Generate Answer
        answer = self._generate_answer(query, relevant_chunks)
        
        # Step 4: Validation Loop
        validation_retry = 0
        while validation_retry < self.max_retries:
            validator_result = self.validator.validate_answer(
                query, answer, relevant_chunks
            )
            
            if validator_result.decision == AgentDecision.PROCEED:
                # Answer is valid
                return {
                    "answer": answer,
                    "confidence": validator_result.confidence,
                    "sources": relevant_chunks,
                    "pipeline": "agentic_rag",
                    "metadata": {
                        "retrieval_retries": retry_count,
                        "validation_retries": validation_retry,
                        "validation_score": validator_result.data.get('validation_score'),
                        "grounding_score": validator_result.data.get('validation_score')
                    }
                }
            
            # Regenerate with different reasoning
            answer = self._generate_answer(
                query, 
                relevant_chunks,
                reasoning_path=f"alternative_{validation_retry}"
            )
            validation_retry += 1
        
        # Return best attempt with warning
        return {
            "answer": answer,
            "confidence": 0.5,
            "sources": relevant_chunks,
            "pipeline": "agentic_rag_unvalidated",
            "metadata": {
                "warning": "Answer could not be fully validated",
                "validation_retries": validation_retry
            }
        }
    
    def _retrieve_chunks(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve chunks from vector database"""
        # Placeholder - integrate with actual vector DB
        # In production: use Milvus, Pinecone, or Weaviate
        return [
            {"text": f"Sample chunk about {query}", "score": 0.8, "id": "chunk_1"},
            {"text": f"Related information on {query}", "score": 0.7, "id": "chunk_2"}
        ]
    
    def _generate_answer(
        self, 
        query: str, 
        chunks: List[Dict],
        reasoning_path: str = "default"
    ) -> str:
        """Generate answer from chunks"""
        # Placeholder - integrate with actual LLM
        # In production: use OpenAI, Anthropic, or local LLM
        context = "\n".join([c.get('text', '') for c in chunks])
        return f"Based on the provided information: {context[:200]}..."


# Export main class
__all__ = ['AgenticRAGPipeline', 'RouterAgent', 'GraderAgent', 'ValidatorAgent']
