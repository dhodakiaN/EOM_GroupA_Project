import unittest
from client.actions import create_account, login, get_files_list, encrypt_data
from unittest.mock import Mock

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

    def test_encrypt_data_success(self):
        # Mock the rsa.encrypt function
        rsa_encrypt_mock = Mock(return_value=b'encrypted_data')

        # Create a mock public key
        public_key = Mock()

        # Patch the rsa.encrypt function to return the mock encrypted data
        with unittest.mock.patch('client.helpers.rsa.encrypt', rsa_encrypt_mock):
            # Test data
            data = b'This is a test data'

            # Call the encrypt_data function with the mock data and public key
            result = encrypt_data(data, public_key)

            # Assert that rsa.encrypt was called with the expected arguments
            rsa_encrypt_mock.assert_called_once_with(data, public_key)

            # Assert that the result is the expected encrypted data
            self.assertEqual(result, b'encrypted_data')

    def test_encrypt_data_exception(self):
        # Mock the rsa.encrypt function to raise an exception
        rsa_encrypt_mock = Mock(side_effect=Exception('Encryption failed'))

        # Create a mock public key
        public_key = Mock()

        # Patch the rsa.encrypt function to raise an exception
        with unittest.mock.patch('client.helpers.rsa.encrypt', rsa_encrypt_mock):
            # Test data
            data = b'This is a test data'

            # Call the encrypt_data function with the mock data and public key
            result = encrypt_data(data, public_key)

            # Assert that rsa.encrypt was called with the expected arguments
            rsa_encrypt_mock.assert_called_once_with(data, public_key)

            # Assert that the result is None when an exception is raised
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
