from collections import defaultdict

import yaml
from yaml.loader import SafeLoader


class Config(object):
    data = defaultdict(dict)

    def __init__(self, environment="development") -> None:
        self._environment = environment
        self.load()
        self.set_account_details()
        self.set_environment()
        self.set_variables()
        self.set_roles()
        self.set_secrets()

    def load(self) -> dict:
        with open(f"configs/{self._environment}.yaml") as f:
            self.data = yaml.load(f, Loader=SafeLoader)

    def set_account_details(self):
        for _key, _value in self.data.get("ACCOUNT").items():
            setattr(self, _key, _value)

    def set_variables(self):
        for _key, _value in self.data.get("VARIABLES").items():
            setattr(self, _key, _value)

    def set_environment(self):
        for _key, _value in self.data.get("ENV").items():
            setattr(self, _key, _value)

    def set_roles(self):
        self.ROLES = self.data.get("ROLES")

    def set_secrets(self):
        self.SECRETS = self.data.get("SECRETS")
