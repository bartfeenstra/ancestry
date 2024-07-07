import logging
from typing import override

from betty.extension import Privatizer
from betty.load import PostLoader
from betty.locale import DEFAULT_LOCALIZER
from betty.locale.localizable import Localizable, plain
from betty.model.ancestry import (
    PersonName,
    Person,
    Event,
    File,
    Place,
    Presence,
    Subject,
)
from betty.model.event_type import Birth, Conference
from betty.project.extension import Extension, UserFacingExtension

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


class Ancestry(UserFacingExtension, PostLoader):
    @override
    @classmethod
    def comes_after(cls) -> set[type[Extension]]:
        return {Privatizer}

    @override
    @classmethod
    def label(cls) -> Localizable:
        return plain("Publish people")

    @override
    @classmethod
    def description(cls) -> Localizable:
        return plain("Publishes curated information about selected people.")

    @override
    async def post_load(self) -> None:
        self._publish_people()
        self._publish_bart()
        self._publish_files()

    def _publish_people(self):
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

    def _publish_bart(self):
        logger = logging.getLogger("betty")
        logger.info("Publishing Bart...")
        bart = self.project.ancestry[Person]["I0000"]
        netherlands = self.project.ancestry[Place]["P0052"]
        birth = Event(
            event_type=Birth,
            place=netherlands,
            public=True,
        )
        Presence(bart, Subject(), birth)
        self.project.ancestry.add(birth)
        for presence in bart.presences:
            if presence.event and presence.event.event_type is Conference:
                presence.public = True
                presence.event.public = True

    def _publish_files(self):
        logger = logging.getLogger("betty")
        logger.info("Publishing selected files...")
        for file_id in _FILES:
            file = self.project.ancestry[File][file_id]
            file.public = True
            logger.info(f"Published {file.label.localize(DEFAULT_LOCALIZER)}")
