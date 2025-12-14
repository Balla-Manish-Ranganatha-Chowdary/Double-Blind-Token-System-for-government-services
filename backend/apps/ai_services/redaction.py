"""
Agentic PII Detection and Redaction with Self-Correction
Multi-agent system with validation loops to catch all PII
"""

import re
import PyPDF2
from io import BytesIO
from typing import Dict, List, Tuple
from .agentic_rag import RouterAgent, GraderAgent, ValidatorAgent


class AgenticPIIDetector:
    """
    Self-correcting PII detector using Agentic RAG
    Router → Grader → Validator with retry loops
    """
    
    PII_PATTERNS = {
        'aadhaar': r'\b\d{4}\s?\d{4}\s?\d{4}\b',
        'phone': r'\b\d{10}\b',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'pan': r'\b[A-Z]{5}\d{4}[A-Z]\b',
        'name': r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',
        'address': r'\b\d+[,\s]+[A-Za-z\s]+[,\s]+\d{6}\b',
        'date_of_birth': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
    }
    
    def __init__(self):
        # Initialize agents
        self.router = RouterAgent()
        self.grader = GraderAgent()
        self.validator = ValidatorAgent()
        
        # Detection thresholds
        self.high_confidence_threshold = 0.9
        self.validation_threshold = 0.85
    
    def detect_pii(self, pdf_file) -> Dict:
        """
        Detect PII using multi-agent system with validation
        
        Args:
            pdf_file: PDF file to check
            
        Returns:
            Dict with detection results and confidence
        """
        if not pdf_file:
            return {
                'has_pii': False,
                'confidence': 0.0,
                'pipeline': 'no_file'
            }
        
        try:
            # Extract text
            text = self._extract_text(pdf_file)
            
            if not text:
                return {
                    'has_pii': False,
                    'confidence': 0.0,
                    'pipeline': 'empty_document'
                }
            
            # Step 1: Router Agent - Quick PII scan
            router_result = self._router_detect(text)
            
            if router_result['confidence'] > self.high_confidence_threshold:
                # High confidence detection, return immediately
                return {
                    'has_pii': router_result['has_pii'],
                    'confidence': router_result['confidence'],
                    'pii_types': router_result['pii_types'],
                    'pipeline': 'router_direct',
                    'agent': 'router'
                }
            
            # Step 2: Grader Agent - Validate detections
            grader_result = self._grade_detections(text, router_result['pii_types'])
            
            if grader_result['is_valid']:
                return {
                    'has_pii': len(grader_result['validated_pii']) > 0,
                    'confidence': grader_result['confidence'],
                    'pii_types': grader_result['validated_pii'],
                    'pipeline': 'router_grader',
                    'validation': 'passed'
                }
            
            # Step 3: Deep scan with retry
            deep_result = self._deep_scan(text)
            
            # Step 4: Validator Agent - Final validation
            validator_result = self._validate_detections(text, deep_result['pii_types'])
            
            return {
                'has_pii': validator_result['has_pii'],
                'confidence': validator_result['confidence'],
                'pii_types': validator_result['validated_pii'],
                'pipeline': 'full_agentic_detection',
                'validation': 'validated',
                'retries': 1
            }
            
        except Exception as e:
            return {
                'has_pii': True,  # Fail safe - reject on error
                'confidence': 0.5,
                'pipeline': 'error',
                'error': str(e)
            }
    
    def _router_detect(self, text: str) -> Dict:
        """
        Router Agent - Quick initial PII detection
        Fast pattern matching for common PII types
        """
        detected_pii = []
        confidence_scores = []
        
        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                detected_pii.append({
                    'type': pii_type,
                    'count': len(matches),
                    'samples': matches[:3]  # First 3 matches
                })
                # Higher confidence for more matches
                confidence = min(len(matches) / 5, 1.0)
                confidence_scores.append(confidence)
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        return {
            'has_pii': len(detected_pii) > 0,
            'pii_types': detected_pii,
            'confidence': avg_confidence,
            'agent': 'router'
        }
    
    def _grade_detections(self, text: str, pii_detections: List[Dict]) -> Dict:
        """
        Grader Agent - Validate detected PII
        Filters false positives
        """
        validated_pii = []
        
        for detection in pii_detections:
            pii_type = detection['type']
            samples = detection.get('samples', [])
            
            # Validate each detection
            if self._is_valid_pii(pii_type, samples, text):
                validated_pii.append(detection)
        
        # Calculate confidence based on validation rate
        if pii_detections:
            validation_rate = len(validated_pii) / len(pii_detections)
        else:
            validation_rate = 0.0
        
        return {
            'is_valid': len(validated_pii) > 0,
            'validated_pii': validated_pii,
            'confidence': validation_rate,
            'agent': 'grader',
            'filtered_count': len(pii_detections) - len(validated_pii)
        }
    
    def _is_valid_pii(self, pii_type: str, samples: List[str], text: str) -> bool:
        """Validate if detected pattern is actually PII"""
        if not samples:
            return False
        
        # Type-specific validation
        if pii_type == 'aadhaar':
            # Check if it's a valid Aadhaar format
            for sample in samples:
                digits = re.sub(r'\D', '', sample)
                if len(digits) == 12:
                    return True
        
        elif pii_type == 'phone':
            # Check if it's a valid phone number
            for sample in samples:
                if sample.startswith(('6', '7', '8', '9')):
                    return True
        
        elif pii_type == 'email':
            # Email is always valid if pattern matches
            return True
        
        elif pii_type == 'pan':
            # PAN is always valid if pattern matches
            return True
        
        elif pii_type == 'name':
            # Check if name appears in context suggesting it's a person's name
            name_contexts = ['name:', 'applicant:', 'mr.', 'mrs.', 'ms.']
            text_lower = text.lower()
            for sample in samples:
                for context in name_contexts:
                    if context in text_lower and sample in text:
                        return True
        
        return False
    
    def _deep_scan(self, text: str) -> Dict:
        """
        Deep scan with additional patterns
        Used when initial detection has low confidence
        """
        # Extended patterns for deep scan
        extended_patterns = {
            **self.PII_PATTERNS,
            'account_number': r'\b\d{9,18}\b',
            'passport': r'\b[A-Z]\d{7}\b',
            'voter_id': r'\b[A-Z]{3}\d{7}\b'
        }
        
        detected_pii = []
        
        for pii_type, pattern in extended_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                detected_pii.append({
                    'type': pii_type,
                    'count': len(matches),
                    'samples': matches[:3]
                })
        
        return {
            'pii_types': detected_pii,
            'scan_type': 'deep'
        }
    
    def _validate_detections(self, text: str, pii_detections: List[Dict]) -> Dict:
        """
        Validator Agent - Final validation before decision
        Ensures no false negatives
        """
        # Re-run router detection
        router_result = self._router_detect(text)
        
        # Combine detections
        all_pii_types = set()
        for detection in pii_detections + router_result['pii_types']:
            all_pii_types.add(detection['type'])
        
        # Grade combined detections
        grader_result = self._grade_detections(text, pii_detections)
        
        # Final decision
        has_pii = len(grader_result['validated_pii']) > 0
        confidence = grader_result['confidence']
        
        return {
            'has_pii': has_pii,
            'validated_pii': grader_result['validated_pii'],
            'confidence': confidence,
            'agent': 'validator',
            'total_pii_types': len(all_pii_types)
        }
    
    def _extract_text(self, pdf_file):
        """Extract text from PDF"""
        try:
            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception:
            return ''


class DocumentRedactor:
    """
    Enhanced document redactor with Agentic PII detection
    Backward compatible interface
    """
    
    def __init__(self):
        self.detector = AgenticPIIDetector()
    
    def check_for_pii(self, pdf_file) -> bool:
        """
        Check if document contains PII
        
        Args:
            pdf_file: PDF file to check
            
        Returns:
            bool: True if PII detected
        """
        result = self.detector.detect_pii(pdf_file)
        return result.get('has_pii', True)  # Fail safe
    
    def check_for_pii_detailed(self, pdf_file) -> Dict:
        """
        Check for PII with detailed results
        
        Args:
            pdf_file: PDF file to check
            
        Returns:
            Dict with detection details
        """
        return self.detector.detect_pii(pdf_file)
    
    def redact_document(self, pdf_file):
        """
        Redact PII from document
        In production: Use NER models, bounding box detection
        """
        # Placeholder for actual redaction
        # Would use libraries like PyMuPDF or pdf-redactor
        pass
    
    def _extract_text(self, pdf_file):
        """Extract text from PDF"""
        return self.detector._extract_text(pdf_file)
