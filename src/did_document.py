from datetime import datetime


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
