from encryption import encrypt, decrypt
from did_document import create_did_document
from token_validation import validate_token_burn


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
