import os

from fabric.colors import red, green, yellow
from fabric.context_managers import settings, hide
from fabric.operations import local

_line = red('#' * 74)
_default_admin_name = 'admin'
_default_admin_email = 'admin@example.org'
_default_pwd = 'changeme'
_data_dir = '/var/data'
_log_dir = '/var/log'


def _stop_and_remove_containers():
    with settings(warn_only=True):
        local("docker-compose stop")
        local("docker-compose rm -f")


def _build_web_container():
    local("docker-compose build")


def _build_docker_compose_file(media_dir, data_dir, log_dir):
    os.environ['MEDIA_DIR'] = media_dir
    os.environ['LOG_DIR'] = log_dir
    os.environ['DATA_DIR'] = data_dir
    with open('docker-compose.tmplt.yml', 'r') as templated_file, \
            open('docker-compose.yml', 'w') as output_file:
        for templated_line in templated_file:
            output_file.writelines(os.path.expandvars(templated_line))


def launch_local():
    local("./docker/mychichair/docker-entrypoint.sh")


def launch_prod_local(contact_email, contact_email_pwd, admin_name=_default_admin_name,
                      admin_email=_default_admin_email, postgres_user='admin', postgre_pwd=_default_pwd,
                      secret_key=_default_pwd, media_dir='./media', data_dir='./data', log_dir='./log',
                      populatedb=False):
    _build_docker_compose_file(media_dir, data_dir, log_dir)
    _build_web_container()
    _stop_and_remove_containers()
    db_url = 'postgres://{0}:{1}@db/{0}'.format(postgres_user, postgre_pwd)
    os.environ['ADMIN_NAME'] = admin_name
    os.environ['ADMIN_EMAIL'] = admin_email
    os.environ['CONTACT_EMAIL'] = contact_email
    os.environ['CONTACT_EMAIL_PASSWORD'] = contact_email_pwd
    os.environ['DATABASE_URL'] = db_url
    os.environ['DEFAULT_FROM_EMAIL'] = contact_email
    os.environ['SECRET_KEY'] = secret_key
    os.environ['DEBUG'] = 'False'
    os.environ['ALLOWED_HOSTS'] = 'mychichair.com'
    os.environ['POPULATE_DB'] = populatedb
    local("docker-compose up -d")


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
            print(_line)
            print(' > eval $(docker-machine env mychichair.com)')
            print(_line)
    else:
        print(yellow('Create Digital Ocean docker machine for deployment'))
    return False


def launch_prod_digital_ocean(contact_email, contact_email_pwd, admin_name, admin_email, postgres_user,
                              postgre_pwd, secret_key, populatedb=False):
    if _is_my_chic_hair_com_active():
        launch_prod_local(contact_email, contact_email_pwd, admin_name, admin_email, postgres_user, postgre_pwd,
                          secret_key, '{}/mychichair/media'.format(_data_dir), _data_dir, _log_dir, populatedb)
