import unittest
from unittest.mock import Mock, patch

from helpers import decrypt_data  

class TestDecryptData(unittest.TestCase):

    @patch('helpers.rsa.decrypt')
    def test_decrypt_data(self, mock_decrypt):
        # Define the encrypted data and a mock private key
        encrypted_data = b'encrypted_data'
        mock_private_key = Mock()

        # Set the return value for the mock rsa.decrypt function
        mock_decrypt.return_value = b'decrypted_data'

        # Call the decrypt_data function
        decrypted_result = decrypt_data(encrypted_data, mock_private_key)

        # Assert that the rsa.decrypt function was called with the expected arguments
        mock_decrypt.assert_called_once_with(encrypted_data, mock_private_key)

        # Assert that the decrypted result matches the expected result
        expected_decrypted_data = b'decrypted_data'
        self.assertEqual(decrypted_result, expected_decrypted_data)

if __name__ == '__main__':
    unittest.main()
