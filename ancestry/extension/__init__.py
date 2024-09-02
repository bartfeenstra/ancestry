import logging
from typing import override

from betty.ancestry import (
    PersonName,
    Person,
    Event,
    File,
    Place,
    Presence,
)
from betty.ancestry.event_type import Birth, Conference
from betty.ancestry.presence_role import Subject
from betty.event_dispatcher import EventHandlerRegistry
from betty.extension.privatizer import Privatizer
from betty.load import PostLoadAncestryEvent
from betty.locale.localizable import Localizable, static
from betty.locale.localizer import DEFAULT_LOCALIZER
from betty.machine_name import MachineName
from betty.plugin import PluginIdentifier
from betty.project.extension import Extension

_PEOPLE = {
    "I0000": ("Bart", "Feenstra"),
    "I0863": ("Ger", "Huijbregts"),
    "I0073": ("Jan", "Feenstra"),
    "I0006": ("Thom", "Feenstra"),
}


_FILES = {
    "O0530",
    "O0531",
}


class Ancestry(Extension):
    @override
    @classmethod
    def comes_after(cls) -> set[PluginIdentifier[Extension]]:
        return {Privatizer}

    @override
    @classmethod
    def plugin_id(cls) -> MachineName:
        return "ancestry"

    @override
    @classmethod
    def plugin_label(cls) -> Localizable:
        return static("Publish people")

    @override
    @classmethod
    def plugin_description(cls) -> Localizable:
        return static("Publishes curated information about selected people.")

    @override
    def register_event_handlers(self, registry: EventHandlerRegistry) -> None:
        registry.add_handler(
            PostLoadAncestryEvent,
            self._publish_people,
            self._publish_bart,
            self._publish_files,
        )

    async def _publish_people(self, event: PostLoadAncestryEvent):
        logger = logging.getLogger("betty")
        logger.info("Publishing selected people...")
        for person_id, (individual_name, affiliation_name) in _PEOPLE.items():
            person = self.project.ancestry[Person][person_id]
            person.public = True
            person_name = PersonName(
                person=person,
                individual=individual_name,
                affiliation=affiliation_name,
                public=True,
            )
            self.project.ancestry.add(person_name)
            logger.info(f"Published {person_name.label.localize(DEFAULT_LOCALIZER)}")

    async def _publish_bart(self, event: PostLoadAncestryEvent):
        logger = logging.getLogger("betty")
        logger.info("Publishing Bart...")
        bart = self.project.ancestry[Person]["I0000"]
        netherlands = self.project.ancestry[Place]["P0052"]
        birth = Event(
            event_type=Birth(),
            place=netherlands,
            public=True,
        )
        Presence(bart, Subject(), birth)
        self.project.ancestry.add(birth)
        for presence in bart.presences:
            if presence.event and isinstance(presence.event.event_type, Conference):
                presence.public = True
                presence.event.public = True

    async def _publish_files(self, event: PostLoadAncestryEvent):
        logger = logging.getLogger("betty")
        logger.info("Publishing selected files...")
        for file_id in _FILES:
            file = self.project.ancestry[File][file_id]
            file.public = True
            logger.info(f"Published {file.label.localize(DEFAULT_LOCALIZER)}")
