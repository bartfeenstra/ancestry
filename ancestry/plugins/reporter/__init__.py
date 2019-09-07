from os.path import dirname
from typing import Optional

from betty.plugin import Plugin


class Report:
    def __init__(self):
        self.places_without_wikipedia_links = []


class ReportProvider:
    def reports(self):
        return []


class Reporter(Plugin):
    @property
    def resource_directory_path(self) -> Optional[str]:
        return '%s/resources' % dirname(__file__)