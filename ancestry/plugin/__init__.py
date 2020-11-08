from typing import Any, Set, Type

from betty.ancestry import Ancestry, PersonName
from betty.parse import PostParser
from betty.plugin import NO_CONFIGURATION, Plugin
from betty.plugin.anonymizer import Anonymizer, anonymize_person
from betty.plugin.cleaner import Cleaner
from betty.plugin.privatizer import Privatizer
from betty.site import Site


_PEOPLE = {
    'I0000': PersonName('Bart', 'Feenstra'),
    'I0863': PersonName('Ger', 'Huijbregts'),
}


class PublishPeople(Plugin, PostParser):
    def __init__(self, ancestry: Ancestry):
        self._ancestry = ancestry

    @classmethod
    def for_site(cls, site: Site, configuration: Any = NO_CONFIGURATION):
        return cls(site.ancestry)

    @classmethod
    def comes_before(cls) -> Set[Type]:
        return {Privatizer}

    async def post_parse(self) -> None:
        self._publish_people()

    def _publish_people(self):
        for person_id in _PEOPLE:
            self._ancestry.people[person_id].private = False


class PopulatePeople(Plugin, PostParser):
    def __init__(self, ancestry: Ancestry):
        self._ancestry = ancestry

    @classmethod
    def for_site(cls, site: Site, configuration: Any = NO_CONFIGURATION):
        return cls(site.ancestry)

    @classmethod
    def depends_on(cls) -> Set[Type]:
        return {Anonymizer}

    @classmethod
    def comes_before(cls) -> Set[Type]:
        return {Cleaner}

    async def post_parse(self) -> None:
        self._populate_people()

    def _populate_people(self):
        for person_id, person_name in _PEOPLE.items():
            person = self._ancestry.people[person_id]
            anonymize_person(person)
            person.names.prepend(person_name)
