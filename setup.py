from os import system as s
from os import path
from os import mkdir, chdir


def apps_install():
	commands = [
		'add-apt-repository ppa:deadsnakes/ppa',
		'apt update',
		'apt upgrade',
		'apt install python3.11',
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
	domen = input('Введите домен, на котором будет работать сайт: ')

	mkdir(f'/{project_name}')
	chdir(f'/{project_name}')

	s(f'git clone {repo_link}')
	s('python -m venv venv')
	s(f'chown www-data -R /{project_name}')
	s(f'chmod 755 -R /{project_name}')


if __name__ == '__main__':
	#apps_install()
	download_repo()
