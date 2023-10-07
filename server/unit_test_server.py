import unittest
from unittest.mock import patch, MagicMock
from controllers import check_account

class TestControllers(unittest.TestCase):
    @patch('controllers.load_account')
    def test_check_account_success(self, mock_load_account):
        # Define mock data and expected output
        mock_data = {'mac_address': 'mock_mac'}
        mock_load_account.return_value = {'mock_mac': {'email': 'test@example.com', 'username': 'testuser'}}
        expected_output = "{'email': 'test@example.com', 'username': 'testuser'}"  # Match the format of the actual data
        
        # Mock socket connection
        mock_connection = MagicMock()
        
        # Call the function
        check_account(mock_connection, mock_data)
        
        # Assert that the connection.send method was called with the expected output
        mock_connection.send.assert_called_once_with(expected_output.encode('utf-8'))
    
    @patch('controllers.load_account')
    def test_check_account_failure(self, mock_load_account):
        # Define mock data and expected output
        mock_data = {'mac_address': 'non_existent_mac'}
        mock_load_account.return_value = {'existing_mac': {'email': 'test@example.com', 'username': 'testuser'}}
        expected_output = 'not-authorized'
        
        # Mock socket connection
        mock_connection = MagicMock()
        
        # Call the function
        check_account(mock_connection, mock_data)
        
        # Assert that the connection.send method was called with the expected output
        mock_connection.send.assert_called_once_with(expected_output.encode('utf-8'))

if __name__ == '__main__':
    unittest.main()
