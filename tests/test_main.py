import pytest
from main import main


def test_main(capsys):
    """
    Test the main function of the application.
    """
    # Call the main function
    main()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the decrypted data is printed
    assert "Decrypted Data (bytes):" in captured.out

    # Assert that the access link is printed
    assert "Access Link:" in captured.out

