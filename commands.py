import fabric.operations
import fabric.api
import fabric.utils

DEBUG = False


def set_environment(environment):
    fabric.api.env.host_string = environment.get_host_string()


def _get_level(debug):
    if DEBUG:
        level = fabric.api.show('everything')
    else:
        level = fabric.api.hide('everything')

    return level


def _get_settings():
    settings_dict = {"warn_only": True}
    return fabric.api.settings(_get_level(DEBUG), **settings_dict)


def local(command):
    with _get_settings():
        return fabric.operations.local(command, capture=True)


def run(command):
    with _get_settings():
        return fabric.operations.run(command)


def put(local_path, remote_path):
    with _get_settings():
        return fabric.operations.put(local_path=local_path,
                                     remote_path=remote_path)


def puts(text):
    fabric.utils.puts(text)


def abort(msg):
    fabric.utils.abort(msg)


def sudo(command):
    with _get_settings():
        return fabric.operations.sudo(command)
