import unittest
import json
import os
from main import check_node_in_object_info

class TestNodeChecker(unittest.TestCase):
    def setUp(self):
        # Load sample object_info response from JSON file
        test_dir = os.path.dirname(os.path.abspath(__file__))
        sample_file_path = os.path.join(test_dir, 'object_info.json')
        
        with open(sample_file_path, 'r') as f:
            self.sample_object_info = json.load(f)

    def test_find_existing_node(self):
        """Test finding a node that exists in object_info"""
        found, details = check_node_in_object_info("comfyui_ipadapter_plus", self.sample_object_info)
        print(found, details)
        self.assertTrue(found)
        self.assertIn("IPAdapterAdvanced", details)

    def test_node_not_found(self):
        """Test searching for a node that doesn't exist"""
        found, details = check_node_in_object_info("non-existent-node", self.sample_object_info)
        self.assertFalse(found)
        self.assertEqual(details, "No matching entries found in object_info")

    def test_empty_object_info(self):
        """Test with empty object_info"""
        found, details = check_node_in_object_info("any-node", {})
        self.assertFalse(found)
        self.assertEqual(details, "No matching entries found in object_info")

if __name__ == '__main__':
    unittest.main() 
