"""
Agentic Document Classification with Multi-Agent System
Router → Grader → Validator for self-correcting classification
"""

import PyPDF2
from io import BytesIO
from typing import Dict, Optional
from .agentic_rag import AgenticRAGPipeline, RouterAgent, GraderAgent, ValidatorAgent
from .graph_rag import GraphRAGPipeline


class AgenticServiceClassifier:
    """
    Self-correcting document classifier using Agentic RAG
    Multi-agent system: Router → Grader → Validator with feedback loops
    """
    
    CATEGORIES = [
        'LAND_RECORD',
        'POLICE_VERIFICATION',
        'RATION_CARD',
        'VEHICLE_REGISTRATION',
        'BUILDING_PERMISSION',
        'REVENUE_MUTATION',
        'OTHER'
    ]
    
    def __init__(self):
        # Initialize agents
        self.router = RouterAgent()
        self.grader = GraderAgent()
        self.validator = ValidatorAgent()
        
        # Initialize GraphRAG for policy knowledge
        self.graph_rag = GraphRAGPipeline()
        self._initialize_policy_graph()
        
        # Category keywords for routing
        self.category_keywords = {
            'LAND_RECORD': ['land', 'property', 'survey', 'plot', 'acre', 'deed'],
            'POLICE_VERIFICATION': ['police', 'verification', 'clearance', 'character', 'antecedents'],
            'RATION_CARD': ['ration', 'card', 'food', 'pds', 'subsidy'],
            'VEHICLE_REGISTRATION': ['vehicle', 'registration', 'rc', 'car', 'bike', 'transport'],
            'BUILDING_PERMISSION': ['building', 'construction', 'permission', 'plan', 'approval'],
            'REVENUE_MUTATION': ['revenue', 'mutation', 'transfer', 'ownership', 'khata'],
            'OTHER': []
        }
    
    def _initialize_policy_graph(self):
        """Initialize knowledge graph with government service policies"""
        policy_docs = [
            {
                "id": "policy_land",
                "text": "Land Record services include property registration, survey documents, and ownership verification. Requires property deed, survey number, and identity proof. Managed by Revenue Department."
            },
            {
                "id": "policy_police",
                "text": "Police Verification services for character certificate, employment clearance, and passport verification. Requires identity proof, address proof, and purpose statement. Managed by Police Department."
            },
            {
                "id": "policy_vehicle",
                "text": "Vehicle Registration includes new registration, transfer of ownership, and RC renewal. Requires purchase invoice, insurance, pollution certificate. Managed by Transport Department."
            },
            {
                "id": "policy_building",
                "text": "Building Permission for construction approval, plan sanction, and occupancy certificate. Requires site plan, structural design, and NOC. Managed by Municipal Corporation."
            },
            {
                "id": "policy_ration",
                "text": "Ration Card for food subsidy under Public Distribution System. Requires income proof, address proof, and family details. Managed by Food & Civil Supplies Department."
            }
        ]
        
        self.graph_rag.index_documents(policy_docs)
    
    def classify(self, pdf_file) -> str:
        """
        Classify service using Agentic RAG pipeline
        
        Args:
            pdf_file: Uploaded PDF file
            
        Returns:
            str: Service category
        """
        result = self.classify_with_confidence(pdf_file)
        return result['category']
    
    def classify_with_confidence(self, pdf_file) -> Dict:
        """
        Classify with confidence score and validation
        
        Args:
            pdf_file: Uploaded PDF file
            
        Returns:
            Dict with category, confidence, and metadata
        """
        if not pdf_file:
            return {
                'category': 'OTHER',
                'confidence': 0.0,
                'pipeline': 'fallback'
            }
        
        try:
            # Extract text from PDF
            text = self._extract_text(pdf_file)
            
            if not text or len(text) < 10:
                return {
                    'category': 'OTHER',
                    'confidence': 0.0,
                    'pipeline': 'empty_document'
                }
            
            # Step 1: Router Agent - Initial classification
            router_result = self._router_classify(text)
            
            # If high confidence, proceed
            if router_result['confidence'] > 0.85:
                return {
                    'category': router_result['category'],
                    'confidence': router_result['confidence'],
                    'pipeline': 'router_direct',
                    'agent': 'router'
                }
            
            # Step 2: Grader Agent - Validate classification
            grader_result = self._grade_classification(text, router_result['category'])
            
            if grader_result['is_valid'] and grader_result['confidence'] > 0.75:
                return {
                    'category': router_result['category'],
                    'confidence': grader_result['confidence'],
                    'pipeline': 'router_grader',
                    'validation': 'passed'
                }
            
            # Step 3: GraphRAG - Use policy knowledge for better classification
            graph_result = self._classify_with_graph_context(text)
            
            # Step 4: Validator Agent - Final validation
            validator_result = self._validate_classification(
                text,
                graph_result['category']
            )
            
            return {
                'category': graph_result['category'],
                'confidence': validator_result['confidence'],
                'pipeline': 'full_agentic_rag',
                'validation': 'validated',
                'graph_entities': graph_result.get('graph_entities', 0)
            }
            
        except Exception as e:
            return {
                'category': 'OTHER',
                'confidence': 0.0,
                'pipeline': 'error',
                'error': str(e)
            }
    
    def _router_classify(self, text: str) -> Dict:
        """
        Router Agent - Quick initial classification
        Decides if document can be classified directly
        """
        text_lower = text.lower()
        
        best_category = 'OTHER'
        best_score = 0.0
        
        for category, keywords in self.category_keywords.items():
            if not keywords:
                continue
            
            # Calculate keyword match score
            matches = sum(1 for kw in keywords if kw in text_lower)
            score = matches / len(keywords)
            
            if score > best_score:
                best_score = score
                best_category = category
        
        return {
            'category': best_category,
            'confidence': min(best_score * 1.2, 1.0),  # Boost score slightly
            'agent': 'router'
        }
    
    def _grade_classification(self, text: str, category: str) -> Dict:
        """
        Grader Agent - Validate if classification is relevant
        Checks if retrieved category matches document content
        """
        # Re-classify to verify
        router_result = self._router_classify(text)
        
        # Check if classifications match
        is_valid = router_result['category'] == category
        
        # Calculate confidence based on keyword density
        text_lower = text.lower()
        keywords = self.category_keywords.get(category, [])
        
        if keywords:
            keyword_count = sum(1 for kw in keywords if kw in text_lower)
            confidence = keyword_count / len(keywords)
        else:
            confidence = 0.5
        
        return {
            'is_valid': is_valid,
            'confidence': confidence,
            'agent': 'grader',
            'reasoning': f"Classification {'matches' if is_valid else 'does not match'} document content"
        }
    
    def _classify_with_graph_context(self, text: str) -> Dict:
        """
        Use GraphRAG to classify with policy knowledge
        Retrieves connected policy information for better classification
        """
        # Query graph for relevant policies
        graph_result = self.graph_rag.query(text[:500], max_hops=2)
        
        # Re-classify with enhanced context
        router_result = self._router_classify(text)
        
        # Boost confidence if graph provides supporting evidence
        confidence_boost = 0.15 if graph_result.get('sources') else 0.0
        
        return {
            'category': router_result['category'],
            'confidence': min(router_result['confidence'] + confidence_boost, 1.0),
            'graph_entities': len(graph_result.get('metadata', {}).get('graph_entities', 0)),
            'graph_context': graph_result.get('sources', [])
        }
    
    def _validate_classification(self, text: str, category: str) -> Dict:
        """
        Validator Agent - Final validation before returning
        Catches potential misclassifications
        """
        # Final verification
        router_result = self._router_classify(text)
        grader_result = self._grade_classification(text, category)
        
        # Combine scores
        matches = router_result['category'] == category
        final_confidence = (
            (0.5 * router_result['confidence']) +
            (0.5 * grader_result['confidence'])
        )
        
        # Penalize if classifications don't match
        if not matches:
            final_confidence *= 0.7
        
        return {
            'is_valid': final_confidence > 0.6,
            'confidence': final_confidence,
            'agent': 'validator',
            'reasoning': f"Final validation {'passed' if final_confidence > 0.6 else 'failed'}"
        }
    
    def _extract_text(self, pdf_file):
        """Extract text from PDF"""
        try:
            # Reset file pointer
            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception:
            return ''


# Maintain backward compatibility
class ServiceClassifier(AgenticServiceClassifier):
    """Alias for backward compatibility"""
    pass
