# Local LlamaIndex Setup - NO API Keys Required

## 100% FREE Setup - No OpenAI, No Cloud APIs

This guide shows you how to run the entire RAG system locally on your machine for FREE.

## Why Local?

✅ **FREE** - No API costs  
✅ **Private** - Data never leaves your machine  
✅ **No Rate Limits** - Use as much as you want  
✅ **Offline** - Works without internet (after initial download)  
✅ **Government Compliant** - Data sovereignty

## Installation

### Step 1: Install Ollama (Recommended - Easiest)

**Windows:**
```bash
# Download from https://ollama.ai/download
# Or use winget
winget install Ollama.Ollama
```

**Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Download Local LLM

```bash
# Download Llama 2 (7B model - ~4GB)
ollama pull llama2

# Or use smaller model (faster)
ollama pull phi

# Or use larger model (better quality)
ollama pull llama2:13b
```

### Step 3: Install Python Dependencies

```bash
pip install llama-index-core
pip install llama-index-llms-ollama
pip install llama-index-embeddings-huggingface
pip install sentence-transformers
```

### Step 4: Test Ollama

```bash
# Start Ollama (if not running)
ollama serve

# Test in another terminal
ollama run llama2 "Hello, how are you?"
```

## Usage - Local RAG (No API Keys)

### Basic Local RAG

```python
from backend.apps.ai_services.llamaindex_local import LocalLlamaIndexRAG

# Initialize with local models (NO API KEY)
rag = LocalLlamaIndexRAG(
    embedding_model="BAAI/bge-small-en-v1.5",  # Free HuggingFace model
    llm_model="llama2",  # Free Ollama model
    use_ollama=True
)

# Index documents
documents = [
    {
        "text": "Land registration requires property deed and survey documents.",
        "metadata": {"category": "land_records"}
    },
    {
        "text": "Police verification needs identity proof and address proof.",
        "metadata": {"category": "police"}
    }
]

# Create index (uses local embeddings)
index = rag.create_index(documents, index_name="policies")

# Create query engine
rag.create_query_engine("policies")

# Query (uses local LLM)
result = rag.query("What documents are needed for land registration?")

print(result['answer'])
print(f"Confidence: {result['confidence']}")
print(f"Model: {result['model']}")  # Shows 'local'
```

### Local Agentic RAG

```python
from backend.apps.ai_services.llamaindex_local import LocalAgenticRAG

# Initialize (NO API KEY)
agentic = LocalAgenticRAG(
    embedding_model="BAAI/bge-small-en-v1.5",
    llm_model="llama2"
)

# Index documents
agentic.rag.create_index(documents, "policies")
agentic.rag.create_query_engine("policies")

# Process with Router → Grader → Validator
result = agentic.process_query(
    "What are the requirements for building permit?",
    index_name="policies",
    max_retries=2
)

print(result['answer'])
print(f"Pipeline: {result['pipeline']}")
print(f"Model: {result['model']}")  # Shows 'local'
```

### Local GraphRAG

```python
from backend.apps.ai_services.llamaindex_local import LocalGraphRAG

# Initialize (NO API KEY)
graph_rag = LocalGraphRAG()

# Create knowledge graph
documents = [
    {
        "text": "Revenue Department manages Land Records. Land Records require Property Deed.",
        "metadata": {"type": "policy"}
    }
]

graph_rag.create_knowledge_graph(documents, max_triplets_per_chunk=5)

# Query with multi-hop reasoning
result = graph_rag.query_graph("What department manages property registration?")

print(result['answer'])
print(f"Model: {result['model']}")  # Shows 'local'
```

## Integration with Classification

```python
# In backend/apps/ai_services/classification.py

from .llamaindex_local import LocalLlamaIndexRAG

class AgenticServiceClassifier:
    def __init__(self):
        # Use LOCAL RAG instead of OpenAI
        self.local_rag = LocalLlamaIndexRAG(
            llm_model="llama2",
            use_ollama=True
        )
        self._initialize_local_rag()
    
    def _initialize_local_rag(self):
        """Initialize with local models"""
        policy_docs = [
            {"text": "Land records policy...", "metadata": {"category": "LAND_RECORD"}},
            {"text": "Police verification policy...", "metadata": {"category": "POLICE_VERIFICATION"}}
        ]
        
        self.local_rag.create_index(policy_docs, "classification")
        self.local_rag.create_query_engine("classification")
    
    def classify_with_local_rag(self, text: str) -> Dict:
        """Classify using local LLM"""
        result = self.local_rag.query(
            f"Classify this document: {text[:500]}",
            index_name="classification"
        )
        
        return {
            'category': self._extract_category(result['answer']),
            'confidence': result['confidence'],
            'model': 'local'
        }
```

## Model Options

### Embedding Models (All FREE)

```python
# Small & Fast (recommended)
"BAAI/bge-small-en-v1.5"  # 33MB, fast

# Medium Quality
"sentence-transformers/all-MiniLM-L6-v2"  # 80MB

# High Quality
"BAAI/bge-base-en-v1.5"  # 109MB

# Best Quality
"BAAI/bge-large-en-v1.5"  # 335MB
```

### LLM Models (All FREE via Ollama)

```python
# Small & Fast
"phi"  # 1.6GB, very fast

# Balanced (recommended)
"llama2"  # 3.8GB, good quality

# Better Quality
"llama2:13b"  # 7.3GB, better responses

# Best Quality
"llama2:70b"  # 39GB, requires powerful GPU

# Code-focused
"codellama"  # 3.8GB, good for technical docs
```

## Performance Comparison

### Local vs OpenAI

| Metric | Local (Llama2) | OpenAI (GPT-4) |
|--------|----------------|----------------|
| Cost | $0 | ~$0.03/1K tokens |
| Speed | 2-5 sec | 1-3 sec |
| Quality | Good | Excellent |
| Privacy | 100% | Cloud-based |
| Offline | ✅ Yes | ❌ No |

### Hardware Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 10GB
- Model: phi or llama2

**Recommended:**
- CPU: 8 cores
- RAM: 16GB
- GPU: 8GB VRAM (optional, speeds up)
- Storage: 20GB
- Model: llama2 or llama2:13b

**Optimal:**
- CPU: 16 cores
- RAM: 32GB
- GPU: 24GB VRAM
- Storage: 50GB
- Model: llama2:70b

## Optimization Tips

### 1. Use GPU Acceleration

```python
# Automatically uses GPU if available
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    device="cuda"  # or "mps" for Mac
)
```

### 2. Reduce Chunk Size

```python
Settings.chunk_size = 256  # Smaller = faster
Settings.chunk_overlap = 25
```

### 3. Limit Retrieved Chunks

```python
rag.create_query_engine(
    similarity_top_k=3,  # Retrieve fewer chunks
    similarity_cutoff=0.7  # Higher threshold
)
```

### 4. Use Smaller Model

```python
# Use phi instead of llama2 for faster responses
rag = LocalLlamaIndexRAG(llm_model="phi")
```

## Troubleshooting

### Issue: "Ollama not found"
**Solution:**
```bash
# Check if Ollama is running
ollama list

# Start Ollama
ollama serve
```

### Issue: "Model not found"
**Solution:**
```bash
# Download the model
ollama pull llama2
```

### Issue: Slow responses
**Solution:**
```python
# Use smaller model
rag = LocalLlamaIndexRAG(llm_model="phi")

# Or reduce chunk size
Settings.chunk_size = 256
```

### Issue: Out of memory
**Solution:**
```python
# Use smaller embedding model
embedding_model="sentence-transformers/all-MiniLM-L6-v2"

# Or use smaller LLM
llm_model="phi"
```

## Testing

```python
# Test script: test_local_rag.py

from llamaindex_local import LocalLlamaIndexRAG

def test_local_rag():
    print("Testing Local RAG (no API keys)...")
    
    rag = LocalLlamaIndexRAG(llm_model="llama2")
    
    docs = [
        {"text": "Land registration requires property deed", "metadata": {}}
    ]
    
    rag.create_index(docs, "test")
    rag.create_query_engine("test")
    
    result = rag.query("What is needed for land registration?", "test")
    
    assert result['answer']
    assert result['model'] == 'local'
    
    print("✓ Local RAG working!")
    print(f"Answer: {result['answer']}")

if __name__ == "__main__":
    test_local_rag()
```

Run test:
```bash
python backend/apps/ai_services/test_local_rag.py
```

## Production Deployment

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.10

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Download models
RUN ollama pull llama2
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"

# Copy application
COPY . /app
WORKDIR /app

CMD ["python", "manage.py", "runserver"]
```

### Environment Variables

```bash
# .env
USE_LOCAL_MODELS=true
OLLAMA_HOST=http://localhost:11434
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
LLM_MODEL=llama2
```

## Comparison: Local vs Cloud

### When to Use Local

✅ Government/sensitive data  
✅ Budget constraints  
✅ High volume usage  
✅ Offline requirements  
✅ Data sovereignty compliance

### When to Use Cloud (OpenAI)

✅ Need best quality  
✅ Low volume usage  
✅ Don't want to manage infrastructure  
✅ Need latest models  
✅ Speed is critical

## Next Steps

1. ✅ Install Ollama
2. ✅ Download llama2 model
3. ✅ Test local RAG
4. ✅ Integrate with your app
5. ✅ Deploy to production

## Resources

- Ollama: https://ollama.ai/
- HuggingFace Models: https://huggingface.co/models
- LlamaIndex Docs: https://docs.llamaindex.ai/

---

**No API keys. No costs. 100% local. 100% free.**
