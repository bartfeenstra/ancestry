"""
Bart's ancestry enricher.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self, final, override

from betty.date import Date, DateRange
from betty.factory import Manufacturable
from betty.job import Job
from betty.load import Enricher, EnricherDefinition
from betty.locale.localize import DEFAULT_LOCALIZER
from betty.plugins.enricher.privatizer import Privatizer
from betty.plugins.enricher.privatizer.jobs import PrivatizeAncestry
from betty.plugins.entity.event import Event
from betty.plugins.entity.file import File
from betty.plugins.entity.person import Person
from betty.plugins.entity.person_name import PersonName
from betty.plugins.entity.place import Place
from betty.plugins.entity.presence import Presence
from betty.plugins.event_type.birth import Birth
from betty.plugins.event_type.conference import Conference
from betty.plugins.role.subject import Subject
from betty.privacy import Privacy
from betty.project import Project

if TYPE_CHECKING:
    from betty.job.scheduler import Scheduler

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


class _Republish(Job):
    def __init__(self, project: Project, /):
        super().__init__(
            "ancestry:republish", dependencies={PrivatizeAncestry.id_for()}
        )
        self._project = project

    @override
    async def do(self, scheduler: Scheduler, /) -> None:
        await self._republish_people(scheduler)
        await self._republish_bart(scheduler)
        await self._republish_files(scheduler)

    async def _republish_people(self, scheduler: Scheduler, /) -> None:
        user = self._project.upstream.user
        await user.message_debug("Publishing selected people...")
        for person_id, (individual_name, affiliation_name) in _PEOPLE.items():
            person = self._project.ancestry[Person][person_id]
            person.public = True
            person_name = PersonName(
                person=person,
                individual=individual_name,
                affiliation=affiliation_name,
                privacy=Privacy.PUBLIC,
            )
            self._project.ancestry.add(person_name)
            await user.message_debug(
                f"Published {person_name.label.localize(DEFAULT_LOCALIZER)}"
            )

    async def _republish_bart(self, scheduler: Scheduler, /) -> None:
        user = self._project.upstream.user
        await user.message_debug("Publishing Bart...")
        bart = self._project.ancestry[Person]["I0000"]
        netherlands = self._project.ancestry[Place]["P0052"]
        birth = Event(
            event_type=Birth(),
            date=DateRange(Date(1970, 1, 1), start_is_boundary=True),
            place=netherlands,
            privacy=Privacy.PUBLIC,
        )
        Presence(bart, Subject(), birth)
        self._project.ancestry.add(birth)
        for presence in bart.presences:
            if isinstance(presence.event.event_type, Conference):
                presence.public = True
                presence.event.public = True

    async def _republish_files(self, scheduler: Scheduler, /) -> None:
        user = self._project.upstream.user
        await user.message_debug("Publishing selected files...")
        for file_id in _FILES:
            file = self._project.ancestry[File][file_id]
            file.public = True
            await user.message_debug(
                f"Published {file.label.localize(DEFAULT_LOCALIZER)}"
            )


@final
@EnricherDefinition(
    "ancestry",
    label="Publish people",
    requires={Project.enrichers.require(Privatizer)},
)
class Ancestry(Enricher, Manufacturable):
    """
    Bart's ancestry enricher.
    """

    def __init__(self, project: Project, /):
        self._project = project

    @override
    @Project.require
    @classmethod
    async def new(cls, project: Project, /) -> Self:
        return cls(project)

    @override
    async def enrich(self, scheduler: Scheduler) -> None:
        await scheduler.add(_Republish(self._project))
