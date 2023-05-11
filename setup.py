from os import system as s
from os import path
from os import mkdir, chdir
import sys


def apps_install():
	commands = [
		'add-apt-repository ppa:deadsnakes/ppa',
		'apt update',
		'apt upgrade',
		'apt install python3.11',
		'apt install gunicorn',
		'apt install nginx',
		'apt install mysql-server',
		'apt install mysql-client',
		'apt install python3-dev',
		'apt install libmysqlclient-dev',
		'apt install python3-venv',
		'apt install python3-pip',
		'apt install python-is-python3',
		'service nginx status'
	]
	for command in commands:
		s(f'{command} -y')


def mysql_init(project_name):
	sys.path.append(f'/{project_name}/{project_name}/{project_name}')
	from settings import DATABASES

	db_name = DATABASES['default']['NAME']
	db_user = DATABASES['default']['USER']
	db_user_password = DATABASES['default']['PASSWORD']
	db_user_host = DATABASES['default']['HOST']

	sql_command = f'''create database {db_name};
create user {db_user}@{db_user_host} identified by "{db_user_password}";
grant all privileges on {db_name}.* to {db_user}@{db_user_host} with grant option;
flush privileges;
'''
	with open('mysql_conf.sql', 'w', encoding='utf-8') as file:
		file.write(sql_command)

	s('mysql < mysql_conf.sql')
	s('rm mysql_conf.sql')


def download_repo():
	repo_link = input('Введите ссылку на публичный репозиторий проекта: ')
	project_name = repo_link.split('/')[-1].replace('.git', '')

	mkdir(f'/{project_name}')
	chdir(f'/{project_name}')

	s(f'git clone {repo_link}')
	s('python -m venv venv')
	s(f'chown www-data -R /{project_name}')
	s(f'chmod 755 -R /{project_name}')

	is_ok = True
	if not path.exists(f'/{project_name}/{project_name}/{project_name}/settings.py'):
		is_ok = False
	if not path.exists(f'/{project_name}/venv'):
		is_ok = False

	if not is_ok:
		print('Ошибка конфигурации проекта')
		return 'error'

	mysql_init(project_name)


if __name__ == '__main__':
	#apps_install()
	download_repo()
