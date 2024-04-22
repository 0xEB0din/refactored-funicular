import ecies
from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend
from typing import Union
from eth_typing.encoding import HexStr
from eth_account.account import LocalAccount
from eth_utils import is_0x_prefixed
from web3.exceptions import InvalidAddress

keys = KeyAPI(NativeECCBackend)


def get_private_key(wallet: LocalAccount) -> keys.PrivateKey:
    """
    Retrieves the private key from the given wallet.

    Args:
        wallet (LocalAccount): Wallet instance.

    Returns:
        keys.PrivateKey: Private key.
    """
    pk = wallet.key
    if not isinstance(pk, bytes):
        pk = Web3.toBytes(hexstr=pk)
    return keys.PrivateKey(pk)


def encrypt(
        document: Union[HexStr, str, bytes],
        wallet: LocalAccount = None,
        public_key: str = None,
) -> HexStr:
    """
    Encrypts the given document using the provided wallet or public key.

    Args:
        document (Union[HexStr, str, bytes]): Document to be encrypted.
        wallet (LocalAccount, optional): Wallet instance. Defaults to None.
        public_key (str, optional): Public key. Defaults to None.

    Returns:
        HexStr: Encrypted document.

    Raises:
        InvalidAddress: If the provided public_key is an invalid Ethereum address.
    """
    key = get_private_key(wallet).public_key.to_hex() if wallet else public_key

    # Validate public_key if provided
    if public_key and not is_0x_prefixed(public_key):
        raise InvalidAddress("Invalid public key format. Must be a 0x-prefixed hex string.")

    if isinstance(document, str):
        document = document.encode()  # Convert string to bytes

    # Encrypt the document using the provided key
    encrypted_document = ecies.encrypt(key, document)

    return encrypted_document.hex()


def decrypt(
        encrypted_document: Union[HexStr, bytes],
        provider_wallet: LocalAccount
) -> bytes:
    """
    Decrypts the encrypted document using the provided wallet.

    Args:
        encrypted_document (Union[HexStr, bytes]): Encrypted document.
        provider_wallet (LocalAccount): Wallet instance.

    Returns:
        bytes: Decrypted document.
    """
    key = get_private_key(provider_wallet).to_hex()
    encrypted_bytes = bytes.fromhex(encrypted_document)
    return ecies.decrypt(key, encrypted_bytes)
