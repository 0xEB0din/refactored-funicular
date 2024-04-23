from umbral import SecretKey, Signer
from src.database import store_data, consume_data
from src.encryption import encrypt_data, create_kfrags


def main() -> None:
    """
    Main function to demonstrate the usage of the mini data proxy
    provider server.

    This function performs the following steps:
    1. Initializes an empty database.
    2. Generates keys for the data owner and consumer.
    3. Defines sample data and access link.
    4. Encrypts the data, generates capsule and kfrags.
    5. Stores the encrypted data in the database.
    6. Attempts to consume the encrypted data.
    7. Prints the decrypted data and access link if successful.
    """
    # Initialize an empty database
    database = {'collection': {}}

    # Generate keys for data owner and consumer
    owner_secret_key = SecretKey.random()
    owner_public_key = owner_secret_key.public_key()
    owner_signer = Signer(owner_secret_key)
    consumer_secret_key = SecretKey.random()
    consumer_public_key = consumer_secret_key.public_key()

    # Define sample data and access link
    data_asset_id = "123456789"
    data = b"Sample data"
    access_link = "https://example.com/data"

    # Encrypt data and generate capsule, kfrags
    ciphertext, capsule = encrypt_data(data, owner_public_key)
    create_kfrags(owner_secret_key, consumer_public_key, owner_signer,
                  threshold=2, shares=3)

    # Store encrypted data
    store_data(
        database,
        data_asset_id,
        ciphertext,
        access_link,
        owner_secret_key,
        owner_signer,
        consumer_public_key,
    )

    # Attempt to consume encrypted data
    try:
        decrypted_data, access_link = consume_data(
            database,
            data_asset_id,
            "consumer_address",
            consumer_secret_key,
            owner_public_key,
            consumer_public_key
        )
        print("Decrypted Data (bytes):", decrypted_data)
        print("Access Link:", access_link)
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
