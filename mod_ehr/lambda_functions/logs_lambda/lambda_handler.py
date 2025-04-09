from health_connector_base import models
from health_connector_base.handlers import APIHandler


class LogsHandler(APIHandler):
    model = models.FTPLogs


def lambda_handler(event, context):
    return LogsHandler.process_event(event)
