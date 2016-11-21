from fabric.colors import red, green, yellow
from fabric.context_managers import settings, shell_env, hide
from fabric.operations import local

line = red('#' * 74)


def _stop_and_remove_containers():
    with settings(warn_only=True):
        local("docker-compose stop")
        local("docker-compose rm -f")


def _build_web_container():
    local("docker-compose build")


def _run_web_container():
    local("docker-compose up -d")


def launch_local():
    local("./docker/mychichair/docker-entrypoint.sh")


def launch_prod_local(contact_email, contact_email_pwd):
    _build_web_container()
    _stop_and_remove_containers()
    with shell_env(DJANGO_SETTINGS_MODULE="mychichair.settings.prod", CONTACT_EMAIL=contact_email,
                   CONTACT_EMAIL_PASSWORD=contact_email_pwd):
        _run_web_container()


def _get_result(cmd: str = 'echo "Hello, World!'):
    with hide('output', 'running', 'warnings'), settings(warn_only=True):
        result = local(cmd, capture=True)
        return result if result else ''


def _is_my_chic_hair_com_active():
    mychichair_com_machines = _get_result('docker-machine ls --filter name=mychichair.com')
    mychichair_com_machines = mychichair_com_machines.split('\n')
    if len(mychichair_com_machines) > 1:
        mychichair_com_machine = mychichair_com_machines[1]
        if mychichair_com_machine.find('Running') != -1 and mychichair_com_machine.find('*') != -1:
            print(green('mychichair.com machine running and active'))
            return True
        elif mychichair_com_machine.find('Running') != -1 and mychichair_com_machine.find('-') != -1:
            print(yellow('Warning: Default machine running but not active'))
            print(line)
            print(' > eval $(docker-machine env mychichair.com)')
            print(line)
    else:
        print(yellow('Create Digital Ocean docker machine for deployment'))
    return False


def launch_prod_digital_ocean(contact_email, contact_email_pwd):
    if _is_my_chic_hair_com_active():
        launch_prod_local(contact_email, contact_email_pwd)
