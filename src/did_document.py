from datetime import datetime, timezone
from typing import Dict, List
from umbral import PublicKey, Capsule, VerifiedKeyFrag


class InvalidKeyFrag(Exception):
    """Exception raised when an invalid key fragment is encountered."""
    pass


def create_did_document(
    data_asset_id: str,
    access_url: str,
    owner_public_key: PublicKey,
    ciphertext: bytes,
    capsule: Capsule,
    kfrags: List[VerifiedKeyFrag]
) -> Dict:
    """
    Create a DID document for a data asset.

    Args:
        data_asset_id (str): Unique identifier for the data asset.
        access_url (str): URL or link to access the data asset.
        owner_public_key (PublicKey): Public key of the data owner.
        ciphertext (bytes): Ciphertext of the encrypted data.
        capsule (Capsule): Capsule used for encryption.
        kfrags (List[VerifiedKeyFrag]): List of verified key fragments (kfrags) for re-encryption.

    Returns:
        Dict: DID document representing the data asset.

    Raises:
        ValueError: If any of the required parameters are missing or invalid.
        InvalidKeyFrag: If an invalid key fragment is encountered.
    """
    try:
        if not data_asset_id:
            raise ValueError("Data asset ID is missing or empty.")
        if not access_url:
            raise ValueError("Access URL is missing or empty.")
        if not owner_public_key or not isinstance(owner_public_key, PublicKey):
            raise ValueError("Invalid owner public key.")
        if not ciphertext or not isinstance(ciphertext, bytes):
            raise ValueError("Invalid ciphertext.")
        if not capsule or not isinstance(capsule, Capsule):
            raise ValueError("Invalid capsule.")
        if not kfrags or not all(isinstance(kfrag, VerifiedKeyFrag) for kfrag in kfrags):
            raise InvalidKeyFrag("Invalid key fragments.")

        did_document = {
            "@context": "https://w3id.org/did/v1",
            "id": f"did:op:{data_asset_id}",
            "created": datetime.now(timezone.utc).isoformat(),
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
    except (ValueError, InvalidKeyFrag) as e:
        raise e
    except Exception as e:
        raise ValueError(f"Error occurred while creating DID document: {str(e)}") from e
