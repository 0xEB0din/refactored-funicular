from encryption import encrypt, decrypt
from did_document import create_did_document
from token_validation import validate_token_burn
from typing import Dict, Any
from eth_account.account import LocalAccount


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

    Parameters:
    - database (Dict[str, Any]): In-memory database to store encrypted data and metadata.
    - data_asset_id (str): Unique identifier for the data asset.
    - data (str): Data to be encrypted and stored.
    - access_link (str): URL or link to access the data asset.
    - encryption_key (str): Ethereum public key used for encryption.
    - owner_public_key (str): Public key of the data owner.
    """
    encrypted_data = encrypt(data, public_key=encryption_key)
    did_doc = create_did_document(data_asset_id, access_link, encryption_key, encrypted_data, owner_public_key)

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

    Parameters:
    - database (Dict[str, Any]): In-memory database containing encrypted data and metadata.
    - data_asset_id (str): Unique identifier for the data asset.
    - consumer_address (str): Address of the consumer attempting to access the data.
    - decryption_key (LocalAccount): Ethereum account used for decryption.

    Returns:
    - tuple: Decrypted data and access link if token burn is valid, otherwise raises an exception.
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
