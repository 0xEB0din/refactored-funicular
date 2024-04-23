import pytest
from umbral import SecretKey, Signer
from src.encryption import encrypt_data, create_kfrags
from src.did_document import create_did_document


def test_create_did_document():
    """
    Test the creation of a DID document for a data asset.
    """
    # Define test data and metadata
    data_asset_id = "test_asset"
    access_url = "https://example.com/data"
    data = b"Test data"

    # Generate keys for data owner and consumer
    owner_key = SecretKey.random()
    owner_signer = Signer(owner_key)
    consumer_key = SecretKey.random().public_key()

    # Encrypt the data using the owner's public key
    ciphertext, capsule = encrypt_data(data, owner_key.public_key())

    # Create key fragments (kfrags) for proxy re-encryption
    kfrags = create_kfrags(owner_key, consumer_key, owner_signer, threshold=1, shares=1)

    # Create the DID document
    did_doc = create_did_document(data_asset_id, access_url, owner_key.public_key(), ciphertext, capsule, kfrags)

    # Assert that the DID document contains the expected asset ID
    assert did_doc["id"] == f"did:op:{data_asset_id}"

    # Assert that the access URL in the DID document matches the expected URL
    assert did_doc["access"][0]["accessUrl"] == access_url

    # Assert that the DID document contains the expected number of key fragments (kfrags)
    assert len(did_doc["access"][0]["kfrags"]) == 1
