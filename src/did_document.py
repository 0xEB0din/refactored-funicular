from datetime import datetime
from typing import Dict, List
from umbral import PublicKey, Capsule, KeyFrag


def create_did_document(
    data_asset_id: str,
    access_url: str,
    owner_public_key: PublicKey,
    ciphertext: bytes,
    capsule: Capsule,
    kfrags: List[KeyFrag]
) -> Dict:
    """
    Create a DID document for a data asset.

    Args:
        data_asset_id (str): Unique identifier for the data asset.
        access_url (str): URL or link to access the data asset.
        owner_public_key (PublicKey): Public key of the data owner.
        ciphertext (bytes): Ciphertext of the encrypted data.
        capsule (Capsule): Capsule used for encryption.
        kfrags (List[KeyFrag]): List of key fragments (kfrags) for re-encryption.

    Returns:
        Dict: DID document representing the data asset.
    """
    did_document = {
        "@context": "https://w3id.org/did/v1",
        "id": f"did:op:{data_asset_id}",
        "created": datetime.utcnow().isoformat() + "Z",
        "access": [
            {
                "type": "rest",
                "accessUrl": access_url,
                "data": ciphertext.hex(),
                "capsule": bytes(capsule).hex(),
                "kfrags": [bytes(kfrag).hex() for kfrag in kfrags],
            }
        ],
        "encryption": {
            "type": "PyUmbral",
            "publicKey": bytes(owner_public_key).hex(),
        },
    }
    return did_document
