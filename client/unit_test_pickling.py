import unittest
import os
from actions import pickling_XML, pickling_Binary, pickling_JSON
import pickle
import json
import xml.etree.ElementTree as ET

class TestPickling(unittest.TestCase):
    def setUp(self):
        self.test_directory = './client/assets/test/'
        self.test_filename = 'testfile'
        self.test_data = {'key': 'value'}


    def test_pickling_XML_unencrypted(self):
        # Test when data should not be encrypted
        result = pickling_XML(self.test_data, self.test_filename, encryptdata=False)

        # Assert that the result is the expected file path
        expected_filepath = './client/assets/testfile.xml'
        self.assertEqual(result, expected_filepath)

        # Assert that the file exists and contains the XML data (not encrypted)
        self.assertTrue(os.path.exists(expected_filepath))
        with open(expected_filepath, 'r') as file:
            # Parse the XML data from the file
            tree = ET.parse(file)
            root = tree.getroot()

            # Define the expected data (your test_data) as an XML string
            expected_data = {'key': 'value'}

            # Extract data from the parsed XML and compare it to expected_data
            file_data = {}
            for child in root:
                file_data[child.tag] = child.text

            # Assert that the loaded XML data is equal to the expected data
            self.assertEqual(file_data, expected_data)

    def test_pickling_Binary_unencrypted(self):
        # Test when data should not be encrypted
        result = pickling_Binary(self.test_data, self.test_filename, encryptdata=False)

        # Assert that the result is the expected file path
        expected_filepath = './client/assets/testfile.pkl'
        self.assertEqual(result, expected_filepath)
        expected_data = {'key': 'value'}

        # Assert that the file exists and contains the data (not encrypted)
        self.assertTrue(os.path.exists(expected_filepath))
        with open(expected_filepath, 'rb') as file:
            file_data = pickle.load(file)
            self.assertEqual(file_data, expected_data)

    def test_pickling_JSON_unencrypted(self):
        # Test when data should not be encrypted
        result = pickling_JSON(self.test_data, self.test_filename, encryptdata=False)

        # Assert that the result is the expected file path
        expected_filepath = './client/assets/testfile.json'
        self.assertEqual(result, expected_filepath)
        expected_data = {'key': 'value'}

        # Assert that the file exists and contains the JSON data (not encrypted)
        self.assertTrue(os.path.exists(expected_filepath))
        with open(expected_filepath, 'r') as file:
            file_data = json.load(file) 
            self.assertEqual(file_data, expected_data)

if __name__ == '__main__':
    unittest.main()