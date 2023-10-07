import unittest
from unittest.mock import Mock,patch
from actions import create_account, login,get_files_list,pickling_Binary,pickling_JSON,pickling_XML,encrypt_data

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

    def test_pickling_Binary(self):
        # Mock the encrypt_data function
        encrypt_data_mock = Mock(return_value=b'encrypted_data')
        
        # Create a mock public key
        public_key = Mock()

        # Patch the encrypt_data function to return the mock encrypted data
        with patch('actions.encrypt_data', encrypt_data_mock):
            # Call the pickling_Binary function with mock data and options
            data_dict = {'key': 'value'}
            filename = 'test'
            
            encryptdata = True
            result = pickling_Binary(data_dict, filename, encryptdata, public_key)

        # Assert that the encrypt_data function was called with the expected arguments
        assert_encrypt_data_called_with(encrypt_data_mock, b'{"key": "value"}', public_key)

        # Assert that the result is the expected file path
        expected_filepath = './client/assets/test.pkl'
        self.assertEqual(result, expected_filepath)

    def test_pickling_JSON(self):
        # Mock the encrypt_data function
        encrypt_data_mock = Mock(return_value=b'encrypted_data')
        
        # Create a mock public key
        public_key = Mock()

        # Patch the encrypt_data function to return the mock encrypted data
        with patch('actions.encrypt_data', encrypt_data_mock):
            # Call the pickling_JSON function with mock data and options
            data_dict = {'key': 'value'}
            filename = 'test'
            encryptdata = True
            result = pickling_JSON(data_dict, filename, encryptdata, public_key)

        # Assert that the encrypt_data function was called with the expected arguments
        assert_encrypt_data_called_with(encrypt_data_mock, b'{"key": "value"}', public_key)

        # Assert that the result is the expected file path
        expected_filepath = './client/assets/test.json'
        self.assertEqual(result, expected_filepath)

    def test_pickling_XML(self):
        # Mock the encrypt_data function
        encrypt_data_mock = Mock(return_value=b'encrypted_data')
        
        # Create a mock public key
        public_key = Mock()

        # Patch the encrypt_data function to return the mock encrypted data
        with patch('actions.encrypt_data', encrypt_data_mock):
            # Call the pickling_XML function with mock data and options
            data_dict = {'key': 'value'}
            filename = 'test'
            encryptdata = True
            result = pickling_XML(data_dict, filename, encryptdata, public_key)

        # Assert that the encrypt_data function was called with the expected arguments
        assert_encrypt_data_called_with(encrypt_data_mock, b'{"key": "value"}', public_key)

        # Assert that the result is the expected file path
        expected_filepath = './client/assets/test.xml'
        self.assertEqual(result, expected_filepath)


if __name__ == '__main__':
    unittest.main()






