from eth_account import Account
from encryption import encrypt, decrypt, get_private_key
from did_document import create_did_document
from database import store_data, consume_data


def main() -> None:
    """
    Main function to demonstrate the usage of the app.
    """
    # Simulated in-memory database
    database = {
        'collection': {}
    }

    # Example usage
    data_to_store = "Sample DID document is here"
    access_link = "https://example.com/asset"
    data_asset_id = "123456789"

    # Generate Ethereum keypair for owner
    owner_account = Account.create()
    owner_private_key = owner_account.key.hex()
    owner_address = owner_account.address
    owner_public_key = get_private_key(owner_account).public_key.to_hex()

    # Generate Ethereum keypair for relayer
    relay_account = Account.create()
    relay_address = relay_account.address
    relay_private_key = relay_account.key.hex()
    relay_public_key = get_private_key(relay_account).public_key.to_hex()

    # Generate Ethereum keypair for consumer
    consumer_account = Account.create()
    consumer_address = relay_account.address
    consumer_private_key = relay_account.key.hex()
    consumer_public_key = get_private_key(relay_account).public_key.to_hex()

    # Store and encrypt DID document data using relayer public key
    store_data(database, data_asset_id, data_to_store, access_link, consumer_public_key, owner_public_key)

    # Consume encrypted data using relayer account
    decrypted_data, access_link = consume_data(database, data_asset_id, relay_public_key, relay_account)

    print("Decrypted Data:", decrypted_data)
    print("Access Link:", access_link)


if __name__ == "__main__":
    main()
