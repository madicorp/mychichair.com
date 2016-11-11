from fabric.context_managers import settings, shell_env
from fabric.operations import local


def _stop_and_remove_containers():
    with settings(warn_only=True):
        local("docker-compose stop")
        local("docker-compose rm -f")


def _build_web_container():
    local("docker-compose build")


def _run_web_container():
    local("docker-compose up -d")


def launch_local():
    _stop_and_remove_containers()
    _build_web_container()
    with shell_env(DJANGO_SETTINGS_MODULE="mychichair.settings.local"):
        _run_web_container()


def launch_prod_local(contact_email, contact_email_pwd):
    _stop_and_remove_containers()
    _build_web_container()
    with shell_env(DJANGO_SETTINGS_MODULE="mychichair.settings.prod", CONTACT_EMAIL=contact_email,
                   CONTACT_EMAIL_PASSWORD=contact_email_pwd):
        _run_web_container()
