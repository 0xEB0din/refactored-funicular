from datetime import datetime
from typing import Dict


def create_did_document(
        data_asset_id: str,
        access_link: str,
        encryption_key: str,
        encrypted_data: str,
        owner_public_key: str,
) -> Dict:
    """
    Create a DID document for a data asset.

    Args:
        data_asset_id (str): Unique identifier for the data asset.
        access_link (str): URL or link to access the data asset.
        encryption_key (str): Public key used for encryption.
        encrypted_data (str): Encrypted data of the data asset.
        owner_public_key (str): Public key of the data owner.

    Returns:
        Dict: DID document representing the data asset.

    Raises:
        ValueError: If any of the required parameters are missing or invalid.
    """
    if not data_asset_id or not access_link or not encryption_key or not encrypted_data or not owner_public_key:
        raise ValueError("All parameters are required")

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
