import unittest
from unittest.mock import Mock
from actions import create_account, login,get_files_list

class TestClientActions(unittest.TestCase):

    def test_create_account_success(self):
        # Create a mock socket connection
        connection = Mock()
        
        # Define the 'data' dictionary with test data
        data = {'email': 'test@example.com', 'username': 'testuser'}

        # Call the create_account function with the mock connection and data
        result = create_account(connection, data)

        # Assert that the function returned True for a successful account creation
        self.assertTrue(result)

    def test_login_success(self):
        # Create a mock socket connection
        connection = Mock()

        # Configure the mock connection to return a response that simulates a successful login
        connection.recv.return_value.decode.return_value = '{"email": "Unittest@example.com", "username": "Unittestuser"}'

        # Call the login function with the mock connection
        result, email, username = login(connection)

        # Assert that the login was successful (assuming a successful login scenario)
        self.assertTrue(result)  # Make sure that this assertion passes
        self.assertEqual(email, 'Unittest@example.com')  # Replace with the expected email
        self.assertEqual(username, 'Unittestuser')

    def test_get_files_list_success(self):
        # Create a mock socket connection
        connection = Mock()

        # Configure the mock connection to return a response that simulates a list of files
        connection.recv.return_value.decode.return_value = '[{"name": "file1.txt", "size": 100}, {"name": "file2.txt", "size": 200}]'

        # Call the get_files_list function with the mock connection
        files_list = get_files_list(connection)

        # Assert that the returned files list contains the expected file information
        expected_files = [{"name": "file1.txt", "size": 100}, {"name": "file2.txt", "size": 200}]
        self.assertEqual(files_list, expected_files)

    

if __name__ == '__main__':
    unittest.main()






