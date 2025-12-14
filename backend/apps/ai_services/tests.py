"""
Unit tests for AI services
"""
from django.test import TestCase
from .classification import DocumentClassifier
from .redaction import PIIDetector
from .agentic_rag import AgenticRAG, RouterAgent, GraderAgent, ValidatorAgent
import tempfile
import os


class DocumentClassifierTests(TestCase):
    """Test document classification"""
    
    def setUp(self):
        self.classifier = DocumentClassifier()
    
    def test_classify_revenue_document(self):
        """Test classification of revenue-related document"""
        text = "This is a tax certificate application for property tax payment"
        category = self.classifier.classify(text)
        self.assertEqual(category, "REVENUE")
    
    def test_classify_health_document(self):
        """Test classification of health-related document"""
        text = "Medical certificate application for hospital treatment"
        category = self.classifier.classify(text)
        self.assertEqual(category, "HEALTH")
    
    def test_classify_education_document(self):
        """Test classification of education-related document"""
        text = "School admission certificate for student enrollment"
        category = self.classifier.classify(text)
        self.assertEqual(category, "EDUCATION")
    
    def test_classify_empty_text(self):
        """Test classification with empty text"""
        category = self.classifier.classify("")
        self.assertEqual(category, "GENERAL")
    
    def test_classify_ambiguous_text(self):
        """Test classification with ambiguous text"""
        text = "General application for certificate"
        category = self.classifier.classify(text)
        self.assertIn(category, ["REVENUE", "HEALTH", "EDUCATION", "GENERAL"])


class PIIDetectorTests(TestCase):
    """Test PII detection and redaction"""
    
    def setUp(self):
        self.detector = PIIDetector()
    
    def test_detect_phone_number(self):
        """Test detection of phone numbers"""
        text = "Contact me at 9876543210"
        has_pii = self.detector.detect_pii(text)
        self.assertTrue(has_pii)
    
    def test_detect_aadhaar(self):
        """Test detection of Aadhaar numbers"""
        text = "My Aadhaar is 1234 5678 9012"
        has_pii = self.detector.detect_pii(text)
        self.assertTrue(has_pii)
    
    def test_detect_email(self):
        """Test detection of email addresses"""
        text = "Email me at john.doe@example.com"
        has_pii = self.detector.detect_pii(text)
        self.assertTrue(has_pii)
    
    def test_no_pii_detected(self):
        """Test text without PII"""
        text = "This is a general application for certificate"
        has_pii = self.detector.detect_pii(text)
        self.assertFalse(has_pii)
    
    def test_redact_phone_number(self):
        """Test redaction of phone numbers"""
        text = "Contact me at 9876543210"
        redacted = self.detector.redact_pii(text)
        self.assertNotIn("9876543210", redacted)
        self.assertIn("[REDACTED]", redacted)


class AgenticRAGTests(TestCase):
    """Test Agentic RAG system"""
    
    def setUp(self):
        self.rag = AgenticRAG()
        self.router = RouterAgent()
        self.grader = GraderAgent()
        self.validator = ValidatorAgent()
    
    def test_router_agent_simple_query(self):
        """Test router agent with simple query"""
        query = "What is the capital of France?"
        needs_retrieval = self.router.route(query)
        # Simple query might not need retrieval
        self.assertIsInstance(needs_retrieval, bool)
    
    def test_router_agent_complex_query(self):
        """Test router agent with complex query"""
        query = "Explain the detailed process for tax certificate application"
        needs_retrieval = self.router.route(query)
        # Complex query should need retrieval
        self.assertTrue(needs_retrieval)
    
    def test_grader_agent_relevant_chunks(self):
        """Test grader agent with relevant chunks"""
        query = "tax certificate"
        chunks = ["Tax certificate application process", "Revenue department procedures"]
        relevant = self.grader.grade(query, chunks)
        self.assertTrue(len(relevant) > 0)
    
    def test_grader_agent_irrelevant_chunks(self):
        """Test grader agent with irrelevant chunks"""
        query = "tax certificate"
        chunks = ["Weather forecast", "Sports news"]
        relevant = self.grader.grade(query, chunks)
        self.assertEqual(len(relevant), 0)
    
    def test_validator_agent_valid_answer(self):
        """Test validator agent with valid answer"""
        query = "What is tax?"
        answer = "Tax is a mandatory financial charge imposed by government"
        sources = ["Tax is a government levy", "Financial obligations to state"]
        is_valid = self.validator.validate(query, answer, sources)
        self.assertTrue(is_valid)
    
    def test_validator_agent_invalid_answer(self):
        """Test validator agent with invalid answer"""
        query = "What is tax?"
        answer = "Tax is a type of fruit"
        sources = ["Tax is a government levy", "Financial obligations to state"]
        is_valid = self.validator.validate(query, answer, sources)
        self.assertFalse(is_valid)
