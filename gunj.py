from os import system as s
import os
import platform
import sys


def apps_setup():
	#  Установка необходимых пакетов
	commands = [
		'add-apt-repository ppa:deadsnakes/ppa',
		'apt update',
		'apt upgrade',
		'apt install python3.11',
		'apt install git',
		'apt install nginx',
		'apt install mysql-server',
		'apt install mysql-client',
		'apt install python3-dev',
		'apt install libmysqlclient-dev',
		'apt install python3-venv',
		'apt install python3-pip',
		'apt install python-is-python3',
		'test -f /home/$USER/.ssh/id_rsa.pub || ssh-keygen -t rsa -b 4096 -C dshutrin@mail.ru -f /home/$USER/.ssh/id_rsa -N ""',
		'clear',
		'service nginx status',
		'cat /home/$USER/.ssh/id_rsa.pub'
	]
	for command in commands:
		s(f'{command} -y')

	input('Добавьте ssh ключ в свой github аккаунт и клонируйте репозиторий с проектом перед тем как продолжить\nПродолжить...')


def gunicorn_setup(user: str, path_to_project: str, project_name: str):
	#  Настройка файлов для работы gunicorn
	with open('/etc/systemd/system/gunicorn.socket', 'w', encoding='utf-8') as file:
		file.write('[Unit]\nDescription=gunicorn socket\n[Socket]\nListenStream=/run/gunicorn.sock\n[Install]\nWantedBy=sockets.target')
	with open('/etc/systemd/system/gunicorn.service', 'w', encoding='utf-8') as file:
		file.write(f'[Unit]\nDescription=gunicorn daemon\nRequires=gunicorn.socket\nAfter=network.target\n[Service]\nUser={user}\nGroup=www-data\nWorkingDirectory={path_to_project}/{project_name}\nExecStart={path_to_project}/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock {project_name}.wsgi:application\n[Install]\nWantedBy=multi-user.target')

	commands = ['systemctl daemon-reload', 'systemctl start gunicorn', 'systemctl enable gunicorn']
	for command in commands:
		s(command)


def nginx_setup(path_to_project, project_name, domen):
	#  Настройка файлов для работы Njinx
	file_data = 'server {\nlisten 80;\nserver_name ' + domen
	file_data = file_data + ';\nlocation = /favicon.ico { access_log off; log_not_found off; }\nlocation /static/ {\nroot '
	file_data = file_data + path_to_project + '/' + project_name
	file_data += ';\nindex index.html;\n}\nlocation / {\ninclude proxy_params;\nproxy_pass http://unix:/run/gunicorn.sock;\n}\n}\n'
	with open(f'/etc/nginx/sites-available/{project_name}', 'w', encoding='utf-8') as file:
		file.write(file_data)
	commands = [f'ln -s /etc/nginx/sites-available/{project_name} /etc/nginx/sites-enabled', 'systemctl restart nginx']
	for command in commands:
		s(command)


def mysql_setup(path_to_project, project_name):
	# Создание базы данных, пользователя, выдача прав
	sys.path.append(f'{path_to_project}/{project_name}/{project_name}')
	from settings import DATABASES

	if DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
		db_name = DATABASES['default']['NAME']
		db_username = DATABASES['default']['USER']
		db_host = DATABASES['default']['HOST']
		db_password = DATABASES['default']['PASSWORD']

		with open('mysql_conf.sql', 'w') as file:
			file.write(f'create database if not exists {db_name};')
			file.write(f'create user if not exists {db_username}@{db_host} identified by "{db_password}";')
			file.write(f'grant all privileges on {db_name}.* to {db_username}@{db_password} with grant option;')
			file.write('flush privileges;')

		s('mysql < mysql_conf.sql')
		s('rm mysql_conf.sql')
	else:
		exit('ОШИБКА!!!\nНастройте проект на работу с MYSQL')


def auto_migrate_database():
	pass


def get_path(message):
	#  Корректный ввод расположения папки
	path = input(message)
	while '\\' in path:
		print('Все пути к файлам и директориям должны использовать знак <</>> вместо <<\>>.')
		path = input(message)
	if path.endswith('/'):
		path = path[::-1][1:][::-1]
	return path


def chmod(path):
	#  Выдача прав доступа
	s(f'chmod 755 -R /home')
	s(f'chown -R www-data /home')


def setup():

	if os.getlogin() != 'root':
		print('Запустите скрипт от пользователя root!')
		exit()

	print('Внимание!!!\nВ папке проекта должно быть виртуальное окружение!\nПеред запуском этого скрипта - активируйте виртуальое окружение и выполните установку необходимых модулей!')
	input('!!!Предупреждение!!!\nВсе вводимые вами пути к файлам и директориям должны использовать знак <</>> вместо <<\>>.')

	apps_setup()

	input('Скачайте репозиторий проекта, если это необходимо и нажмите ENTER...')

	path_to_project = get_path('Введите путь к проекту: ')
	domen = input('Введите домен, на котором будет работать сайт: ')
	project_name = input('Введите название проекта (имя папки): ')
	unix_username = input('Введите имя пользователя: ')

	if os.path.exists(f'{path_to_project}/venv') and os.path.exists(f'{path_to_project}/{project_name}') and os.path.exists(f'{path_to_project}/{project_name}/{project_name}/settings.py'):
		mysql_setup(path_to_project, project_name)
		gunicorn_setup(unix_username, path_to_project, project_name)
		nginx_setup(path_to_project, project_name, domen)
	else:
		print('Ошибка введённых данных!')


if (__name__ == '__main__') and (platform.system() == 'Linux'):
	setup()
