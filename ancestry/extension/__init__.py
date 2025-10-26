from collections.abc import Sequence
from typing import override, final

from betty.ancestry.event import Event
from betty.ancestry.event_type.event_types import Birth, Conference
from betty.ancestry.file import File
from betty.ancestry.person import Person
from betty.ancestry.person_name import PersonName
from betty.ancestry.place import Place
from betty.ancestry.presence import Presence
from betty.ancestry.presence_role.presence_roles import Subject
from betty.date import Date, DateRange
from betty.html import NavigationLink, NavigationLinkProvider
from betty.job import Job
from betty.job.scheduler import Scheduler
from betty.locale.localizable import _, Plain
from betty.locale.localizer import DEFAULT_LOCALIZER
from betty.project import ProjectContext
from betty.project.extension import Extension, ExtensionDefinition
from betty.project.extension.privatizer import Privatizer
from betty.project.extension.privatizer.jobs import PrivatizeAncestry
from betty.project.load import PostLoader

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


class _PublishPeople(Job[ProjectContext]):
    def __init__(self):
        super().__init__(
            "ancestry:publish-people", dependencies={PrivatizeAncestry.id_for()}
        )

    @override
    async def do(self, scheduler: Scheduler[ProjectContext], /) -> None:
        project = scheduler.context.project
        user = project.app.user
        await user.message_information(Plain("Publishing selected people..."))
        for person_id, (individual_name, affiliation_name) in _PEOPLE.items():
            person = project.ancestry[Person][person_id]
            person.public = True
            person_name = PersonName(
                person=person,
                individual=individual_name,
                affiliation=affiliation_name,
                public=True,
            )
            project.ancestry.add(person_name)
            await user.message_information(
                Plain(f"Published {person_name.label.localize(DEFAULT_LOCALIZER)}")
            )


class _PublishBart(Job[ProjectContext]):
    def __init__(self):
        super().__init__(
            "ancestry:publish-bart", dependencies={PrivatizeAncestry.id_for()}
        )

    @override
    async def do(self, scheduler: Scheduler[ProjectContext], /) -> None:
        project = scheduler.context.project
        user = project.app.user
        await user.message_information(Plain("Publishing Bart..."))
        bart = project.ancestry[Person]["I0000"]
        netherlands = project.ancestry[Place]["P0052"]
        birth = Event(
            event_type=Birth(),
            date=DateRange(Date(1970, 1, 1), start_is_boundary=True),
            place=netherlands,
            public=True,
        )
        Presence(bart, Subject(), birth)
        project.ancestry.add(birth)
        for presence in bart.presences:
            if isinstance(presence.event.event_type, Conference):
                presence.public = True
                presence.event.public = True


class _PublishFiles(Job[ProjectContext]):
    def __init__(self):
        super().__init__(
            "ancestry:publish-files", dependencies={PrivatizeAncestry.id_for()}
        )

    @override
    async def do(self, scheduler: Scheduler[ProjectContext], /) -> None:
        project = scheduler.context.project
        user = project.app.user
        await user.message_information(Plain("Publishing selected files..."))
        for file_id in _FILES:
            file = project.ancestry[File][file_id]
            file.public = True
            await user.message_information(
                Plain(f"Published {file.label.localize(DEFAULT_LOCALIZER)}")
            )


@final
@ExtensionDefinition(
    id="ancestry",
    label=Plain("Publish people"),
    description=Plain("Publishes curated information about selected people."),
    depends_on={Privatizer},
)
class Ancestry(NavigationLinkProvider, PostLoader, Extension):
    @override
    async def post_load(self, scheduler: Scheduler[ProjectContext]) -> None:
        await scheduler.add(
            _PublishPeople(),
            _PublishBart(),
            _PublishFiles(),
        )

    @override
    def secondary_navigation_links(self) -> Sequence[NavigationLink]:
        return [
            NavigationLink("betty-entity://person/I0000", _("About the author")),
        ]
