from health_connector_base import models  # noqa
from health_connector_base.handlers import APIHandler  # noqa


class SettingsHandler(APIHandler):
    model = models.Settings


def settings_handler(event, context):
    return SettingsHandler.process_event(event)
