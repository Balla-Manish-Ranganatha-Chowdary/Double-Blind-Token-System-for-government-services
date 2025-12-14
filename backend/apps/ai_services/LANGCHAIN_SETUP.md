# LangChain & LangGraph Integration

Complete guide for using LangChain and LangGraph with the Government Portal's Agentic RAG system.

## Overview

This implementation uses:
- **LangChain**: Framework for building LLM applications
- **LangGraph**: State machine for multi-agent workflows
- **FAISS**: Vector database for semantic search
- **Sentence Transformers**: Free local embeddings
- **Ollama**: Free local LLM (no API keys needed)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    LangGraph Workflow                    │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌─────▼──────┐    ┌─────▼──────┐
   │ Router  │      │ Retriever  │    │  Grader    │
   │ Agent   │──────│   Agent    │────│   Agent    │
   └─────────┘      └────────────┘    └────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌─────▼──────┐    ┌─────▼──────┐
   │Generator│      │ Validator  │    │   Retry    │
   │  Agent  │──────│   Agent    │────│   Loop     │
   └─────────┘      └────────────┘    └────────────┘
```

## Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Ollama (Free Local LLM)

**Windows**:
```bash
# Download from https://ollama.ai/download
# Or use winget
winget install Ollama.Ollama
```

**Linux**:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Mac**:
```bash
brew install ollama
```

### 3. Download LLM Model

```bash
# Download Llama 2 (free, runs locally)
ollama pull llama2

# Or use smaller model for faster inference
ollama pull llama2:7b

# Or use Mistral (alternative)
ollama pull mistral
```

### 4. Verify Installation

```bash
# Test Ollama
ollama run llama2 "Hello, how are you?"

# Test LangChain
python -c "from langchain_community.llms import Ollama; print('LangChain OK')"

# Test LangGraph
python -c "from langgraph.graph import StateGraph; print('LangGraph OK')"
```

## Usage

### Basic Agentic RAG

```python
from apps.ai_services.langchain_rag import LangChainAgenticRAG

# Initialize (uses free local Ollama)
rag = LangChainAgenticRAG(use_local_llm=True)

# Index documents
documents = [
    {
        "id": "policy_land",
        "text": "Land record certificates require property deed and survey number. Processing time is 7-10 days."
    },
    {
        "id": "policy_police",
        "text": "Police verification requires address proof and identity proof. Processing time is 15 days."
    }
]

rag.index_documents(documents)

# Query with multi-agent validation
result = rag.query("How long does land record certificate take?")

print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']}")
print(f"Sources: {result['sources']}")
print(f"Retries: {result['retry_count']}")
```

### GraphRAG with Knowledge Graph

```python
from apps.ai_services.langchain_rag import LangChainGraphRAG

# Initialize GraphRAG
graph_rag = LangChainGraphRAG()

# Build knowledge graph
documents = [
    {
        "id": "doc1",
        "text": "Revenue Department handles land records. Contact: revenue@gov.in"
    },
    {
        "id": "doc2",
        "text": "Land records include property deeds and survey documents."
    }
]

graph_rag.build_knowledge_graph(documents)

# Query with multi-hop reasoning
result = graph_rag.query_with_graph(
    "What documents does Revenue Department handle?",
    max_hops=2
)

print(f"Answer: {result['answer']}")
print(f"Entities: {result['entities']}")
print(f"Hops: {result['hops']}")
```

## LangGraph Workflow

### Agent Flow

1. **Router Agent**: Decides if retrieval is needed
   - Simple queries → Direct answer
   - Complex queries → Retrieve documents

2. **Retriever Agent**: Fetches relevant documents
   - Uses FAISS vector search
   - Returns top-k documents

3. **Grader Agent**: Validates document relevance
   - Filters irrelevant documents
   - Calculates relevance scores

4. **Generator Agent**: Creates answer
   - Uses LLM with context
   - Generates grounded response

5. **Validator Agent**: Checks answer quality
   - Validates grounding in sources
   - Triggers retry if needed (max 2 retries)

### State Management

```python
class AgentState(TypedDict):
    query: str              # User query
    documents: List         # Retrieved documents
    relevant_docs: List     # Filtered relevant docs
    answer: str            # Generated answer
    confidence: float      # Confidence score
    needs_retrieval: bool  # Router decision
    is_valid: bool        # Validator decision
    retry_count: int      # Number of retries
```

## Integration with Existing System

### Update Classification Service

```python
# In apps/ai_services/classification.py

from .langchain_rag import LangChainAgenticRAG

class EnhancedServiceClassifier:
    def __init__(self):
        self.rag = LangChainAgenticRAG(use_local_llm=True)
        
        # Index policy documents
        self.rag.index_documents(self._get_policy_documents())
    
    def classify_with_rag(self, pdf_file):
        """Classify using LangChain RAG"""
        text = self._extract_text(pdf_file)
        
        # Query RAG for classification
        result = self.rag.query(
            f"What service category does this document belong to: {text[:500]}"
        )
        
        return {
            'category': self._extract_category(result['answer']),
            'confidence': result['confidence'],
            'reasoning': result['answer']
        }
```

### Update PII Detection

```python
# In apps/ai_services/redaction.py

from .langchain_rag import LangChainAgenticRAG

class EnhancedPIIDetector:
    def __init__(self):
        self.rag = LangChainAgenticRAG(use_local_llm=True)
        
        # Index PII patterns and examples
        self.rag.index_documents(self._get_pii_examples())
    
    def detect_with_rag(self, text: str):
        """Detect PII using LangChain RAG"""
        result = self.rag.query(
            f"Does this text contain personal information: {text}"
        )
        
        return {
            'has_pii': 'yes' in result['answer'].lower(),
            'confidence': result['confidence'],
            'explanation': result['answer']
        }
```

## Performance Optimization

### 1. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(query: str):
    return rag.query(query)
```

### 2. Batch Processing

```python
# Process multiple queries in batch
queries = ["query1", "query2", "query3"]
results = [rag.query(q) for q in queries]
```

### 3. Async Processing

```python
import asyncio

async def async_query(query: str):
    return await asyncio.to_thread(rag.query, query)

# Run multiple queries concurrently
results = await asyncio.gather(*[async_query(q) for q in queries])
```

## Monitoring

### Track Agent Performance

```python
import time

def query_with_metrics(query: str):
    start = time.time()
    result = rag.query(query)
    duration = time.time() - start
    
    return {
        **result,
        'duration_ms': duration * 1000,
        'timestamp': time.time()
    }
```

### Log Agent Decisions

```python
import logging

logger = logging.getLogger(__name__)

def query_with_logging(query: str):
    logger.info(f"Query: {query}")
    result = rag.query(query)
    logger.info(f"Answer: {result['answer']}")
    logger.info(f"Confidence: {result['confidence']}")
    logger.info(f"Retries: {result['retry_count']}")
    return result
```

## Troubleshooting

### Ollama Not Running

```bash
# Start Ollama service
ollama serve

# Or on Windows
Start-Service Ollama
```

### Model Not Found

```bash
# List available models
ollama list

# Pull required model
ollama pull llama2
```

### Memory Issues

```bash
# Use smaller model
ollama pull llama2:7b

# Or use quantized model
ollama pull llama2:7b-q4_0
```

### Slow Performance

1. **Use GPU**: Ollama automatically uses GPU if available
2. **Reduce context**: Limit document chunks
3. **Cache results**: Use LRU cache for repeated queries
4. **Batch queries**: Process multiple queries together

## Advanced Features

### Custom Prompts

```python
from langchain.prompts import PromptTemplate

custom_prompt = PromptTemplate(
    template="""
    You are a government services assistant.
    
    Context: {context}
    Question: {question}
    
    Provide a clear, concise answer based only on the context.
    
    Answer:
    """,
    input_variables=["context", "question"]
)

# Use custom prompt in generator agent
```

### Custom Agents

```python
def custom_validator_agent(state: AgentState) -> AgentState:
    """Custom validation logic"""
    answer = state['answer']
    
    # Your custom validation
    is_valid = len(answer) > 20 and 'government' in answer.lower()
    
    state['is_valid'] = is_valid
    return state

# Add to workflow
workflow.add_node("validator", custom_validator_agent)
```

## Comparison: LangChain vs Custom Implementation

| Feature | Custom RAG | LangChain RAG |
|---------|-----------|---------------|
| **Setup** | Simple | Requires Ollama |
| **Flexibility** | High | Very High |
| **LLM Support** | Rule-based | LLM-powered |
| **Cost** | Free | Free (with Ollama) |
| **Accuracy** | Good | Excellent |
| **Maintenance** | Manual | Framework-managed |

## Best Practices

1. **Start with Custom RAG** for simple use cases
2. **Upgrade to LangChain** when you need:
   - LLM-powered reasoning
   - Complex multi-agent workflows
   - Advanced prompt engineering
3. **Use Ollama** for free local inference
4. **Cache frequently asked queries**
5. **Monitor agent performance**
6. **Log all decisions** for debugging

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Ollama Documentation](https://ollama.ai/docs)
- [FAISS Documentation](https://faiss.ai/)

---

**LangChain + LangGraph = Production-Ready Agentic RAG! 🚀**
