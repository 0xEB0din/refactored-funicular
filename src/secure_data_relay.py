import json
import ecies
from web3 import Web3
from typing import Union
from datetime import datetime
from eth_account.account import LocalAccount
from eth_typing.encoding import HexStr
from eth_utils.hexadecimal import is_0x_prefixed
from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend
from eth_account import Account

keys = KeyAPI(NativeECCBackend)


def get_private_key(wallet):
    """Returns the private key of the given wallet."""
    pk = wallet.key
    if not isinstance(pk, bytes):
        pk = Web3.toBytes(hexstr=pk)
    return keys.PrivateKey(pk)


def encrypt(
        document: Union[HexStr, str, bytes],
        wallet: LocalAccount = None,
        public_key: str = None,
) -> HexStr:
    key = get_private_key(wallet).public_key.to_hex() if wallet else public_key

    if isinstance(document, str):
        document = document.encode()  # Convert string to bytes

    encrypted_document = ecies.encrypt(key, document)

    return encrypted_document.hex()


def decrypt(
        encrypted_document: Union[HexStr, bytes], provider_wallet: LocalAccount
) -> bytes:
    """
    :param encrypted_document: Encrypted document as HexStr or bytes
    :param provider_wallet: LocalAccount instance
    :return: Decrypted string
    """
    key = get_private_key(provider_wallet).to_hex()
    encrypted_bytes = bytes.fromhex(encrypted_document)
    return ecies.decrypt(key, encrypted_bytes)


def create_did_document(data_asset_id, access_link, encryption_key, encrypted_data, owner_public_key):
    """
    Create a DID document for a data asset.

    Parameters:
    - data_asset_id (str): Unique identifier for the data asset.
    - access_link (str): URL or link to access the data asset.
    - encryption_key (str): Public key used for encryption.

    Returns:
    - dict: DID document representing the data asset.
    """
    did_document = {
        "@context": "https://w3id.org/did/v1",
        "id": f"did:op:{data_asset_id}",
        "owner": owner_public_key,
        "created": datetime.utcnow().isoformat() + "Z",
        "access": [
            {
                "type": "rest",
                "accessUrl": access_link,
                "data": encrypted_data
            }
        ],
        "encryption": {
            "type": "EthereumEncrypt",
            "publicKey": f"did:op:{data_asset_id}#keys-1",
            "publicKeyHex": encryption_key  # Ethereum public key (hex format)
        }
    }

    return did_document


def store_data(database, data_asset_id, data, access_link, encryption_key, owner_public_key):
    """
    Store encrypted data and metadata in the database with a specified data asset ID.

    Parameters:
    - database (dict): In-memory database to store encrypted data and metadata.
    - data_asset_id (str): Unique identifier for the data asset.
    - data (str): Data to be encrypted and stored.
    - access_link (str): URL or link to access the data asset.
    - encryption_key (str): Ethereum public key used for encryption.
    """
    # Encrypt data using recipient's Ethereum public key
    encrypted_data = encrypt(data, public_key=encryption_key)

    # Create a DID document for the data asset
    did_doc = create_did_document(data_asset_id, access_link, encryption_key, encrypted_data, owner_public_key)

    # Store encrypted data and metadata in database with data_asset_id as key
    document = {
        'did_document': did_doc
    }
    if 'collection' not in database or not isinstance(database['collection'], dict):
        database['collection'] = {}

    database['collection'][data_asset_id] = document  # Use data_asset_id as the key


def consume_data(database, data_asset_id, consumer_address, decryption_key):
    """
    Consume encrypted data from the database if the token burn is valid.

    Parameters:
    - database (dict): In-memory database containing encrypted data and metadata.
    - data_asset_id (str): Unique identifier for the data asset.
    - consumer_address (str): Address of the consumer attempting to access the data.
    - decryption_key (str): Ethereum private key used for decryption.

    Returns:
    - tuple: Decrypted data and access link if token burn is valid.
    """
    # Validate token burn (1 BAAI token is required)
    if validate_token_burn(consumer_address, 1):
        # Retrieve encrypted data and DID document from database
        if 'collection' in database and data_asset_id in database['collection']:
            document = database['collection'][data_asset_id]
            did_doc = document['did_document']
            encrypted_data = did_doc['access'][0]['data']

            # Decrypt the encrypted data using the consumer's Ethereum private key
            decrypted_data = decrypt(encrypted_data, provider_wallet=decryption_key)

            # Retrieve access link from the DID document
            access_link = did_doc['access'][0]['accessUrl']

            return decrypted_data.decode(), access_link
        else:
            raise ValueError("No encrypted data found in the database for the specified data asset ID")
    else:
        raise ValueError("Insufficient token burn for access")


def validate_token_burn(consumer_address, token_amount):
    """
    Validate token burn for access.

    Parameters:
    - consumer_address (str): Address of the consumer performing token burn.
    - token_amount (int): Amount of tokens burned.

    Returns:
    - bool: True if token burn is valid, False otherwise (placeholder for actual token validation).
    """
    # Don't implement this function.
    # It is only used for simulation purposes.
    return True  # Simulate valid token burn


# Simulated in-memory database (dictionary)
database = {
    'collection': {}
}

# Example usage:
if __name__ == "__main__":
    # Store encrypted data
    data_to_store = "Sample DID document"
    access_link = "https://example.com/asset"
    data_asset_id = "123456789"

    # Generate Ethereum keypair for owner
    owner_account = Account.create()
    owner_private_key = owner_account.key.hex()
    owner_address = owner_account.address
    owner_public_key = (get_private_key(owner_account).public_key.to_hex())

    # Generate Ethereum keypair for relayer
    relay_account = Account.create()
    relay_address = relay_account.address
    relay_private_key = relay_account.key.hex()
    relay_public_key = (get_private_key(relay_account).public_key.to_hex())

    # Generate Ethereum keypair for consumer
    consumer_account = Account.create()
    consumer_address = relay_account.address
    consumer_private_key = relay_account.key.hex()
    consumer_public_key = (get_private_key(relay_account).public_key.to_hex())

    # store and encrypt DID document data using relayer public key
    store_data(database, data_asset_id, data_to_store, access_link, consumer_public_key, owner_public_key)

    decrypted_data, access_link = consume_data(database, data_asset_id, relay_public_key, relay_account)

    print("Decrypted Data:", decrypted_data)
    print("Access Link:", access_link)