import logging
from sure import expect
from unittest.mock import patch

from src.correlation_logger.cloudwatch_handler import CloudWatchHandler


@patch("src.correlation_logger.cloudwatch_handler.boto3.client")
def test_emit(mock_boto3_client):
    # Mock the boto3 client and set up the handler
    mock_client = mock_boto3_client.return_value
    handler = CloudWatchHandler(
        level=logging.INFO,  # Set the logging level
        region_name="us-east-1",
        aws_access_key_id="your_access_key",
        aws_secret_access_key="your_secret_key",
        log_group_name="your_log_group",
        log_stream_name="your_log_stream",
    )

    # Create a sample log record
    record = logging.LogRecord(
        "test_logger",  # Logger name
        logging.INFO,  # Log level
        "test_module",  # Module name
        42,  # Line number
        "Log message",  # Log message
        None,  # Log arguments
        None,  # Log exception
    )

    # Mock the time.time method to return a fixed timestamp
    with patch("time.time", return_value=1594838400000):
        handler.emit(record)

    # Verify that put_log_events was called with the expected arguments
    expect(mock_client.put_log_events).called_with(
        logGroupName="your_log_group",
        logStreamName="your_log_stream",
        logEvents=[{"timestamp": 1594838400000, "message": "Log message"}]
    )
