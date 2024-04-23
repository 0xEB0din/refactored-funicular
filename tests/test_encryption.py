import unittest
from src.encryption import encrypt_data, decrypt_data, create_kfrags, reencrypt_data, decrypt_reencrypted_data
from umbral import SecretKey, Signer, pre, keys, decrypt_reencrypted


class TestEncryption(unittest.TestCase):
    def setUp(self):
        """
        Set up the necessary keys and data for the tests.
        """
        self.data = b"Test Data"
        self.owner_secret_key = SecretKey.random()
        self.owner_public_key = self.owner_secret_key.public_key()
        self.consumer_secret_key = SecretKey.random()
        self.consumer_public_key = self.consumer_secret_key.public_key()
        self.signer = Signer(self.owner_secret_key)

    def test_encrypt_data(self):
        """
        Test the encryption of data using the owner's public key.
        """
        ciphertext, capsule = encrypt_data(self.data, self.owner_public_key)
        self.assertIsNotNone(ciphertext)
        self.assertIsNotNone(capsule)

    def test_decrypt_data_without_proxy(self):
        """
        Test the decryption of data without proxy re-encryption.
        """
        ciphertext, capsule = encrypt_data(self.data, self.owner_public_key)
        decrypted_data = decrypt_data(self.owner_secret_key, capsule, ciphertext)
        self.assertEqual(self.data, decrypted_data)

    def test_proxy_re_encryption_flow(self):
        """
        Test the full proxy re-encryption flow.
        """
        # Encrypt the data using the owner's public key
        ciphertext, capsule = encrypt_data(self.data, self.owner_public_key)

        # Create key fragments (kfrags) for proxy re-encryption
        kfrags = create_kfrags(self.owner_secret_key, self.consumer_public_key, self.signer, 2, 3)

        # Use the verified kfrags directly for re-encryption
        verified_kfrags = kfrags[:2]

        # Re-encrypt the capsule using the verified kfrags
        cfrags = [reencrypt_data(capsule, kfrag) for kfrag in verified_kfrags]

        # Decrypt the re-encrypted data using the consumer's secret key
        decrypted_data = decrypt_reencrypted_data(
            self.consumer_secret_key,
            self.owner_public_key,
            capsule,
            cfrags,
            ciphertext
        )

        # Assert that the decrypted data matches the original data
        assert decrypted_data == self.data


if __name__ == '__main__':
    unittest.main()
