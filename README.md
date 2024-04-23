# Mini Data Proxy Provider - Refactored

This project aims to refactor a mini data proxy provider server that enables secure data sharing among three actors: Alice (owner), Bob (consumer), and a relayer (proxy server). The primary objective is to utilize proxy re-encryption to securely transfer encrypted messages from Alice to Bob via the relayer.

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Current Analysis](#current-analysis)
  - [Gaps](#gaps)
  - [Trade-offs](#trade-offs)
  - [Limitations](#limitations)
- [Implementation Plan](#implementation-plan)
  - [Phase 1: Refactoring and Code Quality](#phase-1-refactoring-and-code-quality)
  - [Phase 2: Proxy Re-encryption Integration](#phase-2-proxy-re-encryption-integration)
  - [Phase 3: Testing and Validation](#phase-3-testing-and-validation)
  - [Phase 4: Documentation](#documentation)
- [Setup and Usage](#setup-and-usage)
- [How It Works](#how-it-works)
- [Best Practices Followed](#best-practices-followed)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Project Overview

The Mini Data Proxy Provider project focuses on providing a secure and efficient solution for data sharing using proxy re-encryption. The provided script serves as a starting point, and the goal is to refactor and enhance it to meet the project requirements while adhering to best practices regarding code quality, security, and performance.

## Project Structure
- `src/`: Contains the source code files.
  - `encryption.py`: Handles encryption and decryption functionality.
  - `did_document.py`: Manages DID document creation and handling.
  - `database.py`: Provides database storage and retrieval functionality.
  - `token_validation.py`: Validates token burn for data access.
- `tests/`: Contains the test files for each module.
  - `test_main.py`: Tests for the main module.
  - `test_encryption.py`: Tests for the encryption module.
  - `test_did_document.py`: Tests for the DID document module.
  - `test_database.py`: Tests for the database module.
- `main.py`: The main script to run the mini data proxy provider server.
- `requirements.txt`: Lists the required dependencies.



## Current Analysis (Before Refactoring)

### Gaps
- The current script needs proper modularization and separation of concerns, making it difficult to maintain and extend.
- The code does not follow consistent naming conventions and lacks meaningful comments, hindering readability and comprehension.
- The script does not include comprehensive error handling and input validation, which could lead to potential vulnerabilities and unexpected behaviour.
- The dependency versions are not pinned in the `requirements.txt` file, which may result in inconsistent behaviour across different environments.
- No linting configuration is set up to enforce code quality and adherence to coding standards.

### Trade-offs
- The choice of the `ecies` library for encryption and decryption provides simplicity but may have limitations in terms of performance and security compared to other well-established libraries, such as [PyNaCl](https://pynacl.readthedocs.io/en/stable/) or [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/).
- The current implementation does not utilize proxy re-encryption, which could introduce additional complexity but offers enhanced security and privacy features for data sharing.

### Limitations
- Secure key management and storage mechanisms are not implemented, which could pose security risks when handling encryption keys.
- Performance metrics are not defined, which could impact the scalability and efficiency of the data-sharing process.
- The need for a logging mechanism makes tracking and debugging issues during the data-sharing process challenging.
- The test coverage is limited, which may result in undetected bugs and issues in the codebase.

## Implementation Plan

### Phase 1: Refactoring and Code Quality
- [x] Modularize codebase for better organization and maintainability
- [x] Enhance code readability with meaningful comments, consistent naming, and type hints
- [x] Implement robust error handling and input validation for stability and security
  - Custom exception classes (e.g., `DataStorageError`) for specific error handling
  - Input validation checks (e.g., for missing parameters, invalid data formats)
- [x] Update `requirements.txt` file with exact versions to ensure consistent and secure dependencies
- [x] Setup Pylint configuration to enforce code quality and adherence to coding standards
- [x] Create a CI workflow file to facilitate the deployment when needed

### Phase 2: Proxy Re-encryption Integration
- [x] Research and select a suitable proxy re-encryption library based on security, performance, and compatibility
  - PyUmbral was selected for its strong security, high performance, and seamless integration capabilities
- [x] Integrate PyUmbral into the existing codebase for proxy re-encryption functionalities and cryptographic operations

### Phase 3: Testing and Validation
- [x] Develop comprehensive test cases for proxy re-encryption functionality
- [x] Conduct thorough testing to ensure data integrity and confidentiality
- [x] Validate the integration of dependencies and their proper utilization

### Phase 4: Documentation
- [x] Update README with detailed setup instructions, usage guidelines, and testing procedures
- [x] Include project overview, implementation details, and future enhancements
- [x] Document the proxy re-encryption process and its benefits for secure data sharing

## Setup, Usage and Testing

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions
1. Clone the repository:
`git clone https://github.com/0xEB0din/refactored-mini-data-proxy.git`
2. Navigate to the project directory:
`cd refactored-mini-data-proxy`
3. (Optional) Create a virtual environment to isolate project dependencies:
`python -m venv venv`
4. (Optional) Activate the virtual environment:
  - For macOS and Linux: `source venv/bin/activate`
  - For Windows: `venv\Scripts\activate`
5. Install the required dependencies:
`pip install -r requirements.txt`

### Usage Instructions
1. Ensure you are in the project directory and the virtual environment is activated (if using one).
2. Run the mini data proxy provider server: `python main.py`
3. The server will start running, and you will see an output similar to the following:
```
  Decrypted Data (bytes): b'Sample data'
  Access Link: https://example.com/data
```

### Testing Instructions
1. Ensure you are in the project directory and the virtual environment is activated (if using one).
2. Run the test suite:`pytest tests` or `python -m unittest discover tests`
3. The test suite will execute, and you will see the test results in the console. Any failures or errors will be reported, along with their details.

## How It Works
The project utilizes **Proxy Re-Encryption (PRE)** with the [pyUmbral](https://github.com/nucypher/pyUmbral/ "pyUmbral") to facilitate secure, scalable data sharing:
- **Encryption**: Utilizes Alice's public key for data encryption and generates re-encryption keys that allow proxy data transformation for Bob, without revealing its contents.
- **Proxy Re-Encryption**: Manages data transformation at the proxy server and ensures the secure storage and retrieval of encrypted and transformed data.
- **Decryption**: Enables Bob to securely access the re-encrypted data using his private key, ensuring data is only accessible to authorized parties.
> Scenario: Alice encrypts data using her public key and generates re-encryption keys for Bob. The proxy server transforms the encrypted data for Bob using the re-encryption keys, ensuring secure data sharing without revealing the original content. Bob can then decrypt the transformed data using his private key, maintaining data confidentiality and integrity.
This streamlined approach enhances data security and efficiency, demonstrating advanced cryptographic implementation in a multi-user environment.

## Best Practices Followed
- **Modularization**: The codebase is structured into separate modules for better organization and maintainability.
- **Error Handling**: Custom exception classes and input validation checks are implemented to ensure stability and security.
- **Security**: Utilized PyUmbral for strong security and high performance in proxy re-encryption operations.
- **Documentation**: Meaningful comments and docstrings are included to enhance code readability and comprehension.
- **Dependency Management**: The `requirements.txt` file lists exact versions to ensure consistent and secure dependencies.
- **Code Quality**: Pylint configuration is set up to enforce code quality and adherence to coding standards.
- **Testing**: Comprehensive test cases are developed to validate the functionality and ensure data integrity and confidentiality.
- **Convention**: Followed PEP8 coding standards and type hints for better code readability and maintainability.
- **Commit Messages**: Followed the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for better commit message clarity and consistency.
- **CI/CD**: A CI workflow file is created to facilitate deployment and integration with continuous integration tools.


## Future Enhancements
- [ ] SonarQube integration
- [ ] Security Scanning
- [ ] Increase test coverage
- [ ] Defining performance metrics
- [ ] Introducing a logging mechanism 
- [ ] Implement secure key management and storage mechanisms

Feel free to hit me up on [github](https://github.com/0xEB0din) or [email](mailto:edge@roguebit.me) if you have any questions. Cheers!


## License

This project is licensed under the [MIT License](LICENSE).