import os

from fabric.colors import red, green, yellow
from fabric.context_managers import settings, hide
from fabric.operations import local, put, run

_dir_path = os.path.dirname(os.path.realpath(__file__))
_line = red('#' * 74)
_default_admin_name = 'admin'
_default_admin_email = 'admin@example.org'
_default_pwd = 'changeme'
_data_dir = '/var/data'
_log_dir = '/var/log'
_default_domain = 'localhost:8000'
_docker_compose_filename = 'docker-compose.tmplt.yml'
_docker_compose_https_filename = 'docker-compose.https.tmplt.yml'


def _build_web_container():
    local("docker-compose build")


def build_docker_compose_file(media_dir, data_dir, log_dir, admin_email, site_domain=_default_domain,
                              docker_compose_file_name=_docker_compose_filename):
    _build_docker_compose_file(media_dir, data_dir, log_dir, admin_email, site_domain, docker_compose_file_name)


def _build_docker_compose_file(media_dir, data_dir, log_dir, admin_email, site_domain=_default_domain,
                               docker_compose_filename=_docker_compose_filename):
    os.environ['MEDIA_DIR'] = media_dir
    os.environ['LOG_DIR'] = log_dir
    os.environ['DATA_DIR'] = data_dir
    os.environ['SITE_DOMAIN'] = site_domain
    os.environ['ADMIN_EMAIL'] = admin_email
    with open(docker_compose_filename, 'r') as templated_file, open('docker-compose.yml', 'w') as output_file:
        for templated_line in templated_file:
            output_file.writelines(os.path.expandvars(templated_line))


def launch_local():
    local("./docker/mychichair/docker-entrypoint.sh")


def build_main_container_assets(node_modules_dir='{}/build/cache/node_modules'.format(_dir_path),
                                static_dir='{0}/build/static'.format(_dir_path)):
    build_image_name = 'ekougs/mychichair_build'
    local('docker build -t {} -f Dockerfile_build .'.format(build_image_name))
    local('docker run -v {}:/usr/src/mychichair/static/ -v {}:/usr/src/mychichair/node_modules -i --rm {}'
          .format(static_dir, node_modules_dir, build_image_name))
    local('cp build/static/webpack-bundle.json webpack-bundle.json')


def launch_prod_local(contact_email, contact_email_pwd, admin_name=_default_admin_name,
                      admin_email=_default_admin_email, postgres_user='admin', postgres_pwd=_default_pwd,
                      secret_key=_default_pwd, media_dir='./media', data_dir='./data', log_dir='./log',
                      populatedb=False, node_modules_dir='{}/build/cache/node_modules'.format(_dir_path),
                      static_dir='{0}/build/static'.format(_dir_path), docker_machine_name=None):
    build_main_container_assets(node_modules_dir, static_dir)
    docker_compose_filename = _docker_compose_filename
    # TODO enable https
    # if docker_machine_name:
    #     docker_compose_filename = _docker_compose_https_filename
    site_domain = _default_domain
    if docker_machine_name:
        site_domain = docker_machine_name
    _build_docker_compose_file(media_dir, data_dir, log_dir, admin_email, site_domain, docker_compose_filename)
    _build_web_container()
    db_url = 'postgres://{0}:{1}@db/{0}'.format(postgres_user, postgres_pwd)
    docker_compose_cmd = ('ADMIN_NAME="' + admin_name + '"')
    docker_compose_cmd += (' ADMIN_EMAIL="' + admin_email + '"')
    docker_compose_cmd += (' CONTACT_EMAIL="' + contact_email + '"')
    docker_compose_cmd += (' CONTACT_EMAIL_PASSWORD="' + contact_email_pwd + '"')
    docker_compose_cmd += (' POSTGRES_USER="' + postgres_user + '"')
    docker_compose_cmd += (' POSTGRES_PASSWORD="' + postgres_pwd + '"')
    docker_compose_cmd += (' DATABASE_URL="' + db_url + '"')
    docker_compose_cmd += (' DEFAULT_FROM_EMAIL="' + contact_email + '"')
    docker_compose_cmd += (' SECRET_KEY="' + secret_key + '"')
    docker_compose_cmd += ' DEBUG="False"'
    if docker_machine_name:
        docker_machine_ip = local('docker-machine ip {} 2> /dev/null'.format(docker_machine_name), capture=True)
        docker_compose_cmd += " ALLOWED_HOSTS=mychichair.com,{}]".format(docker_machine_ip)
        # docker machine name is the domain
        docker_compose_cmd += ' SITE_DOMAIN={}'.format(docker_machine_name)
    else:
        docker_compose_cmd += ' ALLOWED_HOSTS=mychichair.com'
    if populatedb:
        docker_compose_cmd += (' POPULATE_DB="' + str(populatedb) + '"')
    docker_compose_cmd += " docker-compose up -d"
    local(docker_compose_cmd)


def _get_result(cmd: str = 'echo "Hello, World!'):
    with hide('output', 'running', 'warnings'), settings(warn_only=True):
        result = local(cmd, capture=True)
        return result if result else ''


def _is_docker_machine_active(docker_machine_name):
    mychichair_com_machines = _get_result('docker-machine ls --filter name={}'.format(docker_machine_name))
    mychichair_com_machines = mychichair_com_machines.split('\n')
    if len(mychichair_com_machines) > 1:
        mychichair_com_machine = mychichair_com_machines[1]
        if mychichair_com_machine.find('Running') != -1 and mychichair_com_machine.find('*') != -1:
            print(green('{} machine running and active'.format(docker_machine_name)))
            return True
        elif mychichair_com_machine.find('Running') != -1 and mychichair_com_machine.find('-') != -1:
            print(yellow('Warning: Default machine running but not active'))
            print(_line)
            print(' > eval $(docker-machine env {})'.format(docker_machine_name))
            print(_line)
    else:
        print(yellow('Create Digital Ocean docker machine for deployment'))
    return False


def launch_prod_digital_ocean(contact_email, contact_email_pwd, admin_name, admin_email, postgres_user,
                              postgres_pwd, secret_key, populatedb=False):
    _launch_on_digital_ocean('mychichair.com', contact_email, contact_email_pwd, admin_name, admin_email,
                             postgres_user, postgres_pwd, secret_key, populatedb)


def launch_test_digital_ocean(contact_email, contact_email_pwd, admin_name, admin_email, postgres_user,
                              postgres_pwd, secret_key, populatedb=False):
    _launch_on_digital_ocean('test.mychichair.com', contact_email, contact_email_pwd, admin_name, admin_email,
                             postgres_user, postgres_pwd, secret_key, populatedb)


def install_node_and_modules_on_digital_ocean():
    # TODO do not forget the swap https://www.digitalocean.com/community/tutorials/how-to-add-swap-on-ubuntu-14-04
    run('mkdir -p /tmp/mychichair/node_cache')
    put('package.json', '/tmp/mychichair/node_cache')

    with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
        npm_version = run('npm --version')
    if npm_version.failed:
        # Install node and npm if not present
        run('curl -sL https://deb.nodesource.com/setup_6.x | bash -')
        run('sudo apt-get install nodejs')

    run('cd /tmp/mychichair/node_cache && npm install')


def _launch_on_digital_ocean(docker_machine_name, contact_email, contact_email_pwd, admin_name, admin_email,
                             postgres_user, postgres_pwd, secret_key, populatedb=False):
    install_node_and_modules_on_digital_ocean()
    if _is_docker_machine_active(docker_machine_name):
        launch_prod_local(contact_email, contact_email_pwd, admin_name, admin_email, postgres_user, postgres_pwd,
                          secret_key, '{}/mychichair/media'.format(_data_dir), _data_dir, _log_dir, populatedb,
                          # static are copied on remote home directory
                          '/tmp/mychichair/node_cache/node_modules', '/root/build/static', docker_machine_name)


def create_super_user(user_email):
    create_super_user_cmd = \
        'docker exec -i -t mychichaircom_mychichair_1 python manage.py createsuperuser --email {}'.format(user_email)
    local(create_super_user_cmd)
