from typing import Set, Type

from betty.ancestry import Ancestry, PersonName
from betty.load import PostLoader
from betty.extension import Extension
from betty.extension.anonymizer import Anonymizer, anonymize_person
from betty.extension.cleaner import Cleaner
from betty.extension.privatizer import Privatizer
from betty.app import App, AppAwareFactory


_PEOPLE = {
    'I0000': PersonName('Bart', 'Feenstra'),
    'I0863': PersonName('Ger', 'Huijbregts'),
}


class PublishPeople(Extension, PostLoader, AppAwareFactory):
    def __init__(self, ancestry: Ancestry):
        self._ancestry = ancestry

    @classmethod
    def new_for_app(cls, app: App):
        return cls(app.ancestry)

    @classmethod
    def comes_before(cls) -> Set[Type]:
        return {Privatizer}

    async def post_load(self) -> None:
        self._publish_people()

    def _publish_people(self):
        for person_id in _PEOPLE:
            self._ancestry.people[person_id].private = False


class PopulatePeople(Extension, PostLoader, AppAwareFactory):
    def __init__(self, ancestry: Ancestry):
        self._ancestry = ancestry

    @classmethod
    def new_for_app(cls, app: App):
        return cls(app.ancestry)

    @classmethod
    def depends_on(cls) -> Set[Type]:
        return {Anonymizer}

    @classmethod
    def comes_before(cls) -> Set[Type]:
        return {Cleaner}

    async def post_load(self) -> None:
        self._populate_people()

    def _populate_people(self):
        for person_id, person_name in _PEOPLE.items():
            person = self._ancestry.people[person_id]
            anonymize_person(person)
            person.names.prepend(person_name)
