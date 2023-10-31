import logging
from unittest.mock import MagicMock, patch

from src.correlation_logger.cloudwatch_handler import CloudWatchHandler
from src.correlation_logger.logger import Logger, LogSink


def test_console_log():
    alogger = Logger("correlation-logger", LogSink.CONSOLE)
    alogger.name.should.equal("correlation-logger")
    alogger.name = "new_name"
    alogger.name.should.equal("new_name")
    alogger.debug("Test error message", "123456")
    alogger.info("Test error message", "123456")
    alogger.error("Test error message", "123456")
    alogger.warning("Test error message", "123456")
    alogger.critical("Test error message", "123456")


@patch("src.correlation_logger.cloudwatch_handler.boto3")
def test_cloudwatch_log(mock_boto3):
    mock_handler = CloudWatchHandler(level=logging.ERROR,
                                     region_name="aws_region",
                                     aws_access_key_id="aws_access_key_id",
                                     aws_secret_access_key="aws_secret_access_key",
                                     log_group_name="aws_log_group",
                                     log_stream_name="log_stream_name")
    mock_handler.emit = MagicMock(return_value=None)
    Logger("breadcrumbs-logger", LogSink.CLOUDWATCH, logging.ERROR, mock_handler)
