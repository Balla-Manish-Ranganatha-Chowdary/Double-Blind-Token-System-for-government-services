"""
LLM-Powered RAG Agents - No training required, uses prompting
Works with OpenAI, Anthropic, or any LLM API
"""

from typing import Dict, List
import os


class LLMRouterAgent:
    """
    Router Agent powered by LLM
    Uses few-shot prompting - no training needed
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
        
        # Few-shot examples teach the agent
        self.system_prompt = """You are a routing agent for a RAG system.
Decide if a query needs retrieval or can be answered directly.

Examples:
Query: "What is land registration?"
Decision: SKIP (simple definition)

Query: "What documents are needed for land registration in Hyderabad district?"
Decision: RETRIEVE (specific, needs policy documents)

Query: "List all requirements for building permit in my area"
Decision: RETRIEVE (complex, location-specific)

Return JSON: {"decision": "SKIP" or "RETRIEVE", "confidence": 0.0-1.0, "reasoning": "..."}
"""
    
    def route(self, query: str) -> Dict:
        """Route using LLM - no training, just prompting"""
        
        # Call LLM (OpenAI example)
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Query: {query}"}
            ],
            temperature=0.1  # Low temp for consistent routing
        )
        
        # Parse response
        result = eval(response.choices[0].message.content)
        return result


class LLMGraderAgent:
    """
    Grader Agent powered by LLM
    Validates if retrieved chunks are relevant
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
        
        self.system_prompt = """You are a grading agent for a RAG system.
Evaluate if retrieved document chunks are relevant to the query.

Grade each chunk:
- RELEVANT: Directly answers the query
- PARTIALLY_RELEVANT: Contains related information
- NOT_RELEVANT: Unrelated to query

Return JSON: {
    "chunks": [
        {"id": 1, "grade": "RELEVANT", "score": 0.9},
        {"id": 2, "grade": "NOT_RELEVANT", "score": 0.2}
    ],
    "overall_quality": "GOOD" or "POOR",
    "should_retry": true/false
}
"""
    
    def grade(self, query: str, chunks: List[Dict]) -> Dict:
        """Grade chunks using LLM"""
        
        chunks_text = "\n\n".join([
            f"Chunk {i+1}: {chunk['text'][:200]}..."
            for i, chunk in enumerate(chunks)
        ])
        
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Query: {query}\n\nChunks:\n{chunks_text}"}
            ],
            temperature=0.1
        )
        
        return eval(response.choices[0].message.content)


class LLMValidatorAgent:
    """
    Validator Agent powered by LLM
    Checks if answer is grounded in sources (catches hallucinations)
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
        
        self.system_prompt = """You are a validation agent for a RAG system.
Check if the generated answer is grounded in the provided sources.

Validation criteria:
1. Every claim in the answer must be supported by sources
2. No information should be added that's not in sources
3. Answer should not contradict sources

Return JSON: {
    "is_valid": true/false,
    "confidence": 0.0-1.0,
    "hallucinations": ["list of unsupported claims"],
    "should_retry": true/false,
    "reasoning": "..."
}
"""
    
    def validate(self, query: str, answer: str, sources: List[Dict]) -> Dict:
        """Validate answer using LLM"""
        
        sources_text = "\n\n".join([
            f"Source {i+1}: {src['text'][:200]}..."
            for i, src in enumerate(sources)
        ])
        
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"""
Query: {query}

Answer: {answer}

Sources:
{sources_text}

Validate if the answer is grounded in sources.
"""}
            ],
            temperature=0.1
        )
        
        return eval(response.choices[0].message.content)


# Usage Example
"""
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

router = LLMRouterAgent(client)
grader = LLMGraderAgent(client)
validator = LLMValidatorAgent(client)

# Use in pipeline
router_result = router.route("What documents needed for land registration?")
if router_result['decision'] == 'RETRIEVE':
    chunks = retrieve_from_db(query)
    grader_result = grader.grade(query, chunks)
    
    if grader_result['overall_quality'] == 'GOOD':
        answer = generate_answer(query, chunks)
        validator_result = validator.validate(query, answer, chunks)
        
        if validator_result['is_valid']:
            return answer
"""
