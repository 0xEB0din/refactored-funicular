from encryption import encrypt, decrypt
from did_document import create_did_document
from token_validation import validate_token_burn
from typing import Dict, Any
from eth_account.account import LocalAccount


class DataStorageError(Exception):
    """
    Custom exception class for errors related to data storage operations.
    """
    pass


def store_data(
        database: Dict[str, Any],
        data_asset_id: str,
        data: str,
        access_link: str,
        encryption_key: str,
        owner_public_key: str,
) -> None:
    """
    Store encrypted data and metadata in the database with a specified data asset ID.

    Args:
        database (Dict[str, Any]): In-memory database to store encrypted data and metadata.
        data_asset_id (str): Unique identifier for the data asset.
        data (str): Data to be encrypted and stored.
        access_link (str): URL or link to access the data asset.
        encryption_key (str): Ethereum public key used for encryption.
        owner_public_key (str): Public key of the data owner.

    Raises:
        ValueError: If any of the required parameters are missing or invalid.
        DataStorageError: If there was an error during the encryption or DID document creation process.
    """
    if not data_asset_id or not data or not access_link or not encryption_key or not owner_public_key:
        raise ValueError("All parameters are required")

    try:
        encrypted_data = encrypt(data, public_key=encryption_key)
        did_doc = create_did_document(data_asset_id, access_link, encryption_key, encrypted_data, owner_public_key)
    except Exception as e:
        raise DataStorageError(f"Failed to store data: {str(e)}")

    document = {
        'did_document': did_doc
    }

    if 'collection' not in database or not isinstance(database['collection'], dict):
        database['collection'] = {}

    database['collection'][data_asset_id] = document


def consume_data(
        database: Dict[str, Any],
        data_asset_id: str,
        consumer_address: str,
        decryption_key: LocalAccount,
) -> tuple:
    """
    Consume encrypted data from the database if the token burn is valid.

    Args:
        database (Dict[str, Any]): In-memory database containing encrypted data and metadata.
        data_asset_id (str): Unique identifier for the data asset.
        consumer_address (str): Address of the consumer attempting to access the data.
        decryption_key (LocalAccount): Ethereum account used for decryption.

    Returns:
        tuple: A tuple containing the decrypted data and access link if token burn is valid.

    Raises:
        ValueError: If no encrypted data is found in the database for the specified data asset ID,
            or if the token burn is insufficient for access.
    """
    if validate_token_burn(consumer_address, 1):
        if 'collection' in database and data_asset_id in database['collection']:
            document = database['collection'][data_asset_id]
            did_doc = document['did_document']
            encrypted_data = did_doc['access'][0]['data']
            decrypted_data = decrypt(encrypted_data, provider_wallet=decryption_key)
            access_link = did_doc['access'][0]['accessUrl']
            return decrypted_data.decode(), access_link
        else:
            raise ValueError("No encrypted data found in the database for the specified data asset ID")
    else:
        raise ValueError("Insufficient token burn for access")
