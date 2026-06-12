from unittest.mock import MagicMock, patch

from src.loan_sales_agent_shared.tools.db_tool import (
    get_customer_by_email_tool
)


@patch(
    "src.loan_sales_agent_shared.tools.db_tool.get_customer_by_email"
)
@patch(
    "src.loan_sales_agent_shared.tools.db_tool.SessionLocal"
)
def test_get_customer_by_email_found(
        mock_session_local,
        mock_get_customer_by_email_repo
):
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_customer = MagicMock()
    mock_customer.customer_id = 1
    mock_customer.name = "Pritam Das"
    mock_customer.age = 24

    mock_get_customer_by_email_repo.return_value = mock_customer

    # Act
    response = get_customer_by_email_tool(
        "pritam@gmail.com"
    )

    # Assert
    assert response == {
        "customer_id": 1,
        "name": "Pritam Das",
        "age": 24
    }

    mock_db.close.assert_called_once()

@patch(
    "src.loan_sales_agent_shared.tools.db_tool.get_customer_by_email"
)
@patch(
    "src.loan_sales_agent_shared.tools.db_tool.SessionLocal"
)
def test_get_customer_by_email_not_found(
        mock_session_local,
        mock_get_customer_by_email_repo
):
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_get_customer_by_email_repo.return_value = None

    # Act
    response = get_customer_by_email_tool(
        "unknown@gmail.com"
    )

    # Assert
    assert response == {
        "customer_id": None
    }

    mock_db.close.assert_called_once()