from typing import Dict, Any
from umbral import SecretKey, PublicKey, Signer, Capsule, VerifiedKeyFrag
from encryption import encrypt_data, create_kfrags, reencrypt_data, decrypt_reencrypted_data, deserialize_kfrag
from did_document import create_did_document
from token_validation import validate_token_burn


class DataStorageError(Exception):
    """Exception raised for errors that occur during data storage."""
    pass


def store_data(
    database: Dict[str, Any],
    asset_id: str,
    data: bytes,
    access_url: str,
    owner_key: SecretKey,
    owner_signer: Signer,
    consumer_key: PublicKey,
) -> None:
    """
    Stores encrypted data along with its metadata in a simulated in-memory database.

    Args:
        database (Dict[str, Any]): The database to store the data.
        asset_id (str): The unique identifier for the data asset.
        data (bytes): The data to be encrypted and stored.
        access_url (str): A URL or link where the data can be accessed.
        owner_key (SecretKey): The secret key of the data owner for encryption.
        owner_signer (Signer): The signer object used for signing the data.
        consumer_key (PublicKey): The public key of the intended data consumer.

    Raises:
        DataStorageError: If there is an error during the storage of data.
    """
    if not (asset_id and data and access_url and owner_key and owner_signer and consumer_key):
        raise ValueError("All parameters are required")

    try:
        ciphertext, capsule = encrypt_data(data, owner_key.public_key())
        kfrags = create_kfrags(owner_key, consumer_key, owner_signer, threshold=1, shares=1)
        did_doc = create_did_document(asset_id, access_url, owner_key.public_key(), ciphertext, capsule, kfrags)
    except ValueError as e:
        raise DataStorageError(f"Failed to store data: {str(e)}")

    document = {'did_document': did_doc}
    database.setdefault('collection', {})[asset_id] = document


def consume_data(
    database: Dict[str, Any],
    data_asset_id: str,
    consumer_address: str,
    consumer_secret_key: SecretKey,
    delegating_public_key: PublicKey,
    receiving_public_key: PublicKey
) -> tuple:
    """
    Consume encrypted data, attempting to decrypt it using the consumer's secret key and verified capsule fragments.

    Args:
        database (Dict[str, Any]): Database containing stored data.
        data_asset_id (str): Identifier for the data asset.
        consumer_address (str): Address of the consumer.
        consumer_secret_key (SecretKey): Secret key of the consumer.
        delegating_public_key (PublicKey): Public key of the original data owner.
        receiving_public_key (PublicKey): Public key of the data receiver.

    Returns:
        tuple: Decrypted data and access link, if successful.

    Raises:
        ValueError: If no encrypted data is found for the specified data asset ID.
    """
    if 'collection' in database and data_asset_id in database['collection']:
        document = database['collection'][data_asset_id]
        did_doc = document['did_document']
        ciphertext = bytes.fromhex(did_doc['access'][0]['data'])
        capsule = Capsule.from_bytes(bytes.fromhex(did_doc['access'][0]['capsule']))
        kfrags_bytes = [bytes.fromhex(hex_kfrag) for hex_kfrag in did_doc['access'][0]['kfrags']]

        verified_kfrags = [VerifiedKeyFrag.from_verified_bytes(kfrag_bytes) for kfrag_bytes in kfrags_bytes]

        cfrags = [reencrypt_data(capsule, vkfrag) for vkfrag in verified_kfrags if vkfrag]

        if not cfrags:
            raise ValueError("No valid capsule fragments generated for decryption.")

        decrypted_data = decrypt_reencrypted_data(
            receiving_sk=consumer_secret_key,
            delegating_pk=delegating_public_key,
            capsule=capsule,
            verified_cfrags=cfrags,
            ciphertext=ciphertext
        )
        return decrypted_data, did_doc['access'][0]['accessUrl']
    else:
        raise ValueError("No encrypted data found for the specified data asset ID.")