from django.test import TestCase
from ..services.blockchain_service import BlockchainService

class BlockchainServiceTest(TestCase):
    def setUp(self):
        self.blockchain_service = BlockchainService()
        self.test_patient_id = "TEST123"
        self.test_report_data = "Test medical report"
    
    def test_store_and_retrieve_record(self):
        # Store a record
        result = self.blockchain_service.store_medical_record(
            self.test_patient_id,
            "test_hash",
            self.test_report_data
        )
        
        self.assertTrue(result['success'])
        self.assertIn('transaction_hash', result)
        self.assertIn('block_number', result)
        
        # Retrieve the record
        record = self.blockchain_service.get_medical_record(
            self.test_patient_id,
            "test_hash"
        )
        
        self.assertTrue(record['success'])
        self.assertEqual(record['data']['patient_id'], self.test_patient_id)
        self.assertEqual(record['data']['report_data'], self.test_report_data)
        self.assertTrue(record['data']['is_valid'])
    
    def test_update_record(self):
        # Store initial record
        self.blockchain_service.store_medical_record(
            self.test_patient_id,
            "test_hash",
            self.test_report_data
        )
        
        # Update record
        new_data = "Updated medical report"
        result = self.blockchain_service.update_medical_record(
            self.test_patient_id,
            "test_hash",
            new_data
        )
        
        self.assertTrue(result['success'])
        
        # Verify update
        record = self.blockchain_service.get_medical_record(
            self.test_patient_id,
            "test_hash"
        )
        
        self.assertEqual(record['data']['report_data'], new_data)
    
    def test_invalidate_record(self):
        # Store record
        self.blockchain_service.store_medical_record(
            self.test_patient_id,
            "test_hash",
            self.test_report_data
        )
        
        # Invalidate record
        result = self.blockchain_service.invalidate_medical_record(
            self.test_patient_id,
            "test_hash"
        )
        
        self.assertTrue(result['success'])
        
        # Verify invalidation
        record = self.blockchain_service.get_medical_record(
            self.test_patient_id,
            "test_hash"
        )
        
        self.assertFalse(record['data']['is_valid']) 