import ecies
from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend
from typing import Union
from eth_typing.encoding import HexStr
from eth_account.account import LocalAccount

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
