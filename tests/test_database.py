import pytest
from umbral import SecretKey, Signer
from src.database import store_data, consume_data, DataStorageError


def test_store_data():
    """
    Test the storage of encrypted data and metadata in the database.
    """
    # Create an empty database
    database = {'collection': {}}

    # Define test data and metadata
    asset_id = "test_asset"
    data = b"Test data"
    access_url = "https://example.com/data"

    # Generate keys for data owner and consumer
    owner_key = SecretKey.random()
    owner_signer = Signer(owner_key)
    consumer_key = SecretKey.random().public_key()

    # Store the encrypted data and metadata in the database
    store_data(database, asset_id, data, access_url, owner_key, owner_signer, consumer_key)

    # Assert that the data is stored in the correct collection and asset ID
    assert 'collection' in database
    assert asset_id in database['collection']


def test_consume_data():
    """
    Test the consumption of encrypted data from the database.
    """
    # Create an empty database
    database = {'collection': {}}

    # Define test data and metadata
    asset_id = "test_asset"
    data = b"Test data"
    access_url = "https://example.com/data"

    # Generate keys for data owner and consumer
    owner_key = SecretKey.random()
    owner_signer = Signer(owner_key)
    consumer_key = SecretKey.random()

    # Store the encrypted data and metadata in the database
    store_data(database, asset_id, data, access_url, owner_key, owner_signer, consumer_key.public_key())

    # Consume the encrypted data from the database
    decrypted_data, access_link = consume_data(
        database,
        asset_id,
        "consumer_address",
        consumer_key,
        owner_key.public_key(),
        consumer_key.public_key()
    )

    # Assert that the decrypted data matches the original data
    assert decrypted_data == data

    # Assert that the access link matches the expected URL
    assert access_link == access_url
