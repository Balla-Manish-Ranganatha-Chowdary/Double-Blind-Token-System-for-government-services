# LlamaIndex Integration Setup Guide

## Installation

### Step 1: Install LlamaIndex Dependencies

```bash
cd backend
pip install -r requirements_llamaindex.txt
```

### Step 2: Set Environment Variables

Add to your `.env` file:

```bash
# OpenAI API Key (required)
OPENAI_API_KEY=sk-your-key-here

# Optional: Anthropic for Claude
ANTHROPIC_API_KEY=your-key-here

# Optional: Pinecone for vector storage
PINECONE_API_KEY=your-key-here
PINECONE_ENVIRONMENT=your-env

# Optional: Neo4j for graph storage
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
```

### Step 3: Initialize Storage

```bash
# Create storage directory
mkdir -p backend/storage/indexes
mkdir -p backend/storage/graphs
```

## Usage Examples

### 1. Basic RAG with LlamaIndex

```python
from backend.apps.ai_services.llamaindex_integration import LlamaIndexRAGSystem

# Initialize system
rag = LlamaIndexRAGSystem(
    llm_model="gpt-4",
    embedding_model="text-embedding-3-small"
)

# Index documents
documents = [
    {
        "text": "Land registration requires property deed and survey documents.",
        "metadata": {"category": "land_records", "department": "revenue"}
    },
    {
        "text": "Police verification needs identity proof and address proof.",
        "metadata": {"category": "police", "department": "police"}
    }
]

index = rag.create_index(documents, index_name="government_policies")

# Create query engine
rag.create_query_engine("government_policies", similarity_top_k=5)

# Query
result = rag.query("What documents are needed for land registration?")
print(result['answer'])
print(f"Confidence: {result['confidence']}")
```

### 2. Agentic RAG with Router → Grader → Validator

```python
from backend.apps.ai_services.llamaindex_integration import LlamaIndexAgenticRAG

# Initialize agentic system
agentic_rag = LlamaIndexAgenticRAG(llm_model="gpt-4")

# Create index first
agentic_rag.rag_system.create_index(documents, "policies")

# Create agents
agentic_rag.create_router_agent("policies")
agentic_rag.create_grader_agent()
agentic_rag.create_validator_agent()

# Process query through full pipeline
result = agentic_rag.process_query(
    "What are the requirements for building permit?",
    index_name="policies",
    max_retries=3
)

print(result['answer'])
print(f"Pipeline: {result['pipeline']}")
print(f"Validation: {result['validation']}")
print(f"Retries: {result['retries']}")
```

### 3. GraphRAG with Knowledge Graph

```python
from backend.apps.ai_services.llamaindex_integration import LlamaIndexGraphRAG

# Initialize GraphRAG
graph_rag = LlamaIndexGraphRAG(llm_model="gpt-4")

# Create knowledge graph
documents = [
    {
        "text": "Revenue Department manages Land Records. Land Records require Property Deed. Property Deed is part of Registration Process.",
        "metadata": {"type": "policy"}
    }
]

graph_rag.create_knowledge_graph(documents, max_triplets_per_chunk=10)

# Query with multi-hop reasoning
result = graph_rag.query_graph(
    "What department manages property registration?",
    include_text=True,
    retriever_mode="keyword"
)

print(result['answer'])
```

### 4. Document Classification with LlamaIndex

```python
from backend.apps.ai_services.classification import AgenticServiceClassifier
from backend.apps.ai_services.llamaindex_integration import LlamaIndexRAGSystem

# Initialize classifier with LlamaIndex backend
classifier = AgenticServiceClassifier()

# Index policy documents for classification
policy_docs = [
    {"text": "Land records policy: requires survey documents...", "metadata": {"category": "LAND_RECORD"}},
    {"text": "Police verification policy: requires identity proof...", "metadata": {"category": "POLICE_VERIFICATION"}}
]

rag = LlamaIndexRAGSystem()
rag.create_index(policy_docs, "classification_policies")

# Classify document
with open('application.pdf', 'rb') as f:
    result = classifier.classify_with_confidence(f)
    print(f"Category: {result['category']}")
    print(f"Confidence: {result['confidence']}")
```

### 5. PII Detection with LlamaIndex

```python
from backend.apps.ai_services.redaction import AgenticPIIDetector

detector = AgenticPIIDetector()

with open('document.pdf', 'rb') as f:
    result = detector.detect_pii(f)
    
    if result['has_pii']:
        print("PII Detected!")
        for pii in result['pii_types']:
            print(f"- {pii['type']}: {pii['count']} occurrences")
    else:
        print("No PII detected")
```

## Integration with Existing Code

### Update Classification Service

```python
# In backend/apps/ai_services/classification.py

from .llamaindex_integration import LlamaIndexRAGSystem

class AgenticServiceClassifier:
    def __init__(self):
        # ... existing code ...
        
        # Add LlamaIndex RAG
        self.llamaindex_rag = LlamaIndexRAGSystem()
        self._initialize_llamaindex()
    
    def _initialize_llamaindex(self):
        """Initialize LlamaIndex with policy documents"""
        try:
            # Try to load existing index
            self.llamaindex_rag.load_index("classification_policies")
        except:
            # Create new index
            policy_docs = self._get_policy_documents()
            self.llamaindex_rag.create_index(policy_docs, "classification_policies")
            self.llamaindex_rag.create_query_engine("classification_policies")
    
    def _classify_with_llamaindex(self, text: str) -> Dict:
        """Use LlamaIndex for classification"""
        result = self.llamaindex_rag.query(
            f"Classify this document into a service category: {text[:500]}",
            index_name="classification_policies"
        )
        
        # Extract category from response
        category = self._extract_category_from_response(result['answer'])
        
        return {
            'category': category,
            'confidence': result['confidence'],
            'reasoning': result['answer']
        }
```

## Performance Optimization

### 1. Use Local Embeddings (Free)

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
```

### 2. Use ChromaDB for Vector Storage (Free)

```python
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.create_collection("government_docs")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)
```

### 3. Batch Processing

```python
# Process multiple documents efficiently
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512, chunk_overlap=50),
        Settings.embed_model
    ]
)

nodes = pipeline.run(documents=documents, show_progress=True)
index = VectorStoreIndex(nodes)
```

## Monitoring and Debugging

### Enable Logging

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

### Track Token Usage

```python
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
import tiktoken

token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model("gpt-4").encode
)

callback_manager = CallbackManager([token_counter])
Settings.callback_manager = callback_manager

# After queries
print(f"Embedding Tokens: {token_counter.total_embedding_token_count}")
print(f"LLM Prompt Tokens: {token_counter.prompt_llm_token_count}")
print(f"LLM Completion Tokens: {token_counter.completion_llm_token_count}")
```

## Testing

```python
# Test script: backend/apps/ai_services/test_llamaindex.py

from llamaindex_integration import LlamaIndexRAGSystem, LlamaIndexAgenticRAG

def test_basic_rag():
    rag = LlamaIndexRAGSystem()
    
    docs = [
        {"text": "Test document about land records", "metadata": {}}
    ]
    
    rag.create_index(docs, "test_index")
    rag.create_query_engine("test_index")
    
    result = rag.query("What is this about?", "test_index")
    assert result['answer']
    assert result['confidence'] > 0
    print("✓ Basic RAG test passed")

def test_agentic_rag():
    agentic = LlamaIndexAgenticRAG()
    
    docs = [
        {"text": "Land registration requires property deed", "metadata": {}}
    ]
    
    agentic.rag_system.create_index(docs, "test_agentic")
    agentic.create_router_agent("test_agentic")
    
    result = agentic.process_query("What documents are needed?", "test_agentic")
    assert result['answer']
    print("✓ Agentic RAG test passed")

if __name__ == "__main__":
    test_basic_rag()
    test_agentic_rag()
    print("\n✓ All tests passed!")
```

Run tests:
```bash
cd backend/apps/ai_services
python test_llamaindex.py
```

## Troubleshooting

### Issue: "No module named 'llama_index'"
**Solution:** Install dependencies
```bash
pip install -r requirements_llamaindex.txt
```

### Issue: "OpenAI API key not found"
**Solution:** Set environment variable
```bash
export OPENAI_API_KEY=your-key-here
```

### Issue: "Storage directory not found"
**Solution:** Create directories
```bash
mkdir -p backend/storage/indexes
```

### Issue: High API costs
**Solution:** Use local embeddings
```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
```

## Production Deployment

### 1. Use Managed Vector DB

```python
# Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
import pinecone

pinecone.init(api_key=os.getenv('PINECONE_API_KEY'))
vector_store = PineconeVectorStore(pinecone_index=pinecone.Index("gov-docs"))
```

### 2. Cache Embeddings

```python
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore

docstore = SimpleDocumentStore()
index_store = SimpleIndexStore()

storage_context = StorageContext.from_defaults(
    docstore=docstore,
    index_store=index_store
)
```

### 3. Async Processing

```python
# Use async for better performance
import asyncio

async def process_documents_async(documents):
    tasks = [process_doc(doc) for doc in documents]
    results = await asyncio.gather(*tasks)
    return results
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Set environment variables
3. ✅ Run test script
4. ✅ Index your policy documents
5. ✅ Integrate with classification/redaction
6. ✅ Deploy to production

## Support

- LlamaIndex Docs: https://docs.llamaindex.ai/
- GitHub: https://github.com/run-llama/llama_index
- Discord: https://discord.gg/dGcwcsnxhU
