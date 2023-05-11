from os import system as s
from os import path
from os import mkdir, chdir
import sys
from pprint import pprint


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
		exit()


def mysql_init(project_name):
	sys.path.append(f'/{project_name}/{project_name}/{project_name}')
	from settings import DATABASES

	pprint(DATABASES)


if __name__ == '__main__':
	#apps_install()
	download_repo()
