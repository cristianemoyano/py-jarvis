from os import environ

ENV = environ.get("JARVIS_ENV", "DEV")


def get_settings():
    if ENV == "DEV":
        from settings import dev

        return dev


SETTINGS = get_settings()
