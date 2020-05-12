from typing import Callable, Tuple, List, Set, Type

from betty.ancestry import PersonName
from betty.event import Event
from betty.parse import PostParseEvent
from betty.plugin import Plugin
from betty.plugin.anonymizer import Anonymizer, anonymize_person
from betty.plugin.cleaner import Cleaner
from betty.plugin.privatizer import Privatizer


_PEOPLE = {
    'I0000': PersonName('Bart', 'Feenstra'),
    'I0863': PersonName('Ger', 'Huijbregts'),
}


class PublishPeople(Plugin):
    @classmethod
    def comes_before(cls) -> Set[Type]:
        return {Privatizer}

    def subscribes_to(self) -> List[Tuple[Type[Event], Callable]]:
        return [
            (PostParseEvent, self._publish_people),
        ]

    async def _publish_people(self, event: PostParseEvent):
        for person_id in _PEOPLE:
            event.ancestry.people[person_id].private = False


class PopulatePeople(Plugin):
    @classmethod
    def depends_on(cls) -> Set[Type]:
        return {Anonymizer}

    @classmethod
    def comes_before(cls) -> Set[Type]:
        return {Cleaner}

    def subscribes_to(self) -> List[Tuple[Type[Event], Callable]]:
        return [
            (PostParseEvent, self._populate_people),
        ]

    async def _populate_people(self, event: PostParseEvent):
        for person_id, person_name in _PEOPLE.items():
            person = event.ancestry.people[person_id]
            anonymize_person(person)
            person.names.prepend(person_name)
