import subprocess

from briefcase.config import BaseConfig
from briefcase.commands import (
    BuildCommand,
    CreateCommand,
    PublishCommand,
    RunCommand,
    UpdateCommand
)
from briefcase.exceptions import BriefcaseCommandError
from briefcase.platforms.iOS import iOSMixin


class iOSXcodeMixin(iOSMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, output_format='Xcode', **kwargs)

    def binary_path(self, app):
        return self.platform_path / '{app.formal_name} / {app.formal_name}.xcodeproj'.format(app=app)

    def bundle_path(self, app):
        return self.platform_path / '{app.formal_name}'.format(app=app)


class iOSXcodeCreateCommand(iOSXcodeMixin, CreateCommand):
    description = "Create and populate a iOS Xcode project."


class iOSXcodeUpdateCommand(iOSXcodeMixin, UpdateCommand):
    description = "Update an existing iOS Xcode project."


class iOSXcodeBuildCommand(iOSXcodeMixin, BuildCommand):
    description = "Build an iOS Xcode project."


class iOSXcodeRunCommand(iOSXcodeMixin, RunCommand):
    description = "Run an iOS Xcode project."

    def run_app(self, app: BaseConfig):
        """
        Start the application.

        :param app: The config object for the app
        :param base_path: The path to the project directory.
        """
        print()
        print('[{app.name}] Starting app...'.format(
            app=app
        ))
        try:
            print()
            self.subprocess.run(
                [
                    'open',
                    self.binary_path(app),
                ],
                check=True,
            )
        except subprocess.CalledProcessError:
            print()
            raise BriefcaseCommandError(
                "Unable to start app {app.name}.".format(app=app)
            )


class iOSXcodePublishCommand(iOSXcodeMixin, PublishCommand):
    description = "Publish an iOS app."
    publication_channels = ['ios_appstore']
    default_publication_channel = 'ios_appstore'


# Declare the briefcase command bindings
create = iOSXcodeCreateCommand  # noqa
update = iOSXcodeUpdateCommand  # noqa
build = iOSXcodeBuildCommand  # noqa
run = iOSXcodeRunCommand  # noqa
publish = iOSXcodePublishCommand  # noqa
