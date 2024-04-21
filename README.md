# Mini Data Proxy Provider - Refactored

This project aims to refactor a mini data proxy provider server that enables secure data sharing among three actors: Alice (owner), Bob (consumer), and a relayer (proxy server). The primary objective is to utilize proxy re-encryption for securely transferring encrypted messages from Alice to Bob via the relayer.

## Table of Contents
- [Project Overview](#project-overview)
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
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Project Overview

The Mini Data Proxy Provider project focuses on providing a secure and efficient solution for data sharing using proxy re-encryption. The provided script serves as a starting point, and the goal is to refactor and enhance it to meet the project requirements while adhering to best practices in terms of code quality, security, and performance.

## Current Analysis

### Gaps
- The current script lacks proper modularization and separation of concerns, making it difficult to maintain and extend.
- The code does not follow consistent naming conventions and lacks meaningful comments, hindering readability and comprehension.
- The script does not include comprehensive error handling and input validation, which could lead to potential vulnerabilities and unexpected behavior.

### Trade-offs
- The choice of the `ecies` library for encryption and decryption provides simplicity but may have limitations in terms of performance and security compared to other well-established libraries.
- The use of an in-memory database (dictionary) simplifies the implementation but may not be suitable for production environments with high scalability and persistence requirements.

### Limitations
- The current script does not include a mechanism for secure key management and storage, which is critical for ensuring the confidentiality and integrity of sensitive data.

## Implementation Plan

### Phase 1: Refactoring and Code Quality
- [ ] Modularize codebase for better organization and maintainability
- [ ] Enhance code readability with meaningful comments, consistent naming, and type hints
- [ ] Implement robust error handling and input validation for stability and security
- [ ] Update `requirements.txt` file with exact versions to ensure consistent and secure dependencies
- [ ] Setup Pylint configuration to enforce code quality and adherence to coding standards
- [ ] Setup CI workflow configuration to facilitate the deployment

### Phase 2: Proxy Re-encryption Integration
- [ ] Research and select a suitable proxy re-encryption library based on security, performance, and compatibility
- [ ] Integrate the proxy re-encryption library into the existing codebase, ensuring secure implementation of cryptographic operations

### Phase 3: Testing and Validation
- [ ] Develop comprehensive test cases for proxy re-encryption functionality
- [ ] Conduct thorough testing to ensure data integrity and confidentiality
- [ ] Validate the integration of dependencies and their proper utilization

### Phase 4: Documentation
- [ ] Document any assumptions, limitations, and known issues

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
2. Run the mini data proxy provider server:
`python src/secure_data_relay.py`
3. The server will start running, and you will see output indicating that it's ready to handle requests.
4. Follow the on-screen instructions to store and consume data using the proxy re-encryption scheme.

### Testing Instructions
1. Ensure you are in the project directory and the virtual environment is activated (if using one).
2. Run the test suite:
`python -m unittest discover tests`
3. The test suite will execute, and you will see the test results in the console. Any failures or errors will be reported, along with their details.

## Future Enhancements
[ ] SonarQube integration
*[TBD]*

## License

This project is licensed under the [MIT License](LICENSE).