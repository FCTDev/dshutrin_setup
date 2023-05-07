from os import system as s


def apps_setup():
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
	with open('/etc/systemd/system/gunicorn.socket', 'w', encoding='utf-8') as file:
		file.write('[Unit]\nDescription=gunicorn socket\n[Socket]\nListenStream=/run/gunicorn.sock\n[Install]\nWantedBy=sockets.target')
	with open('/etc/systemd/system/gunicorn.service', 'w', encoding='utf-8') as file:
		file.write(f'[Unit]\nDescription=gunicorn daemon\nRequires=gunicorn.socket\nAfter=network.target\n[Service]\nUser={user}\nGroup=www-data\nWorkingDirectory={path_to_project}/{project_name}\nExecStart={path_to_project}/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock {project_name}.wsgi:application\n[Install]\nWantedBy=multi-user.target')

	commands = ['systemctl daemon-reload', 'systemctl start gunicorn', 'systemctl enable gunicorn']
	for command in commands:
		s(command)


def nginx_setup(path_to_project, project_name, domen):
	file_data = 'server {\nlisten 80;\nserver_name ' + domen
	file_data = file_data + ';\nlocation = /favicon.ico { access_log off; log_not_found off; }\nlocation /static/ {\nroot '
	file_data = file_data + path_to_project + '/' + project_name
	file_data += ';\nindex index.html;\n}\nlocation / {\ninclude proxy_params;\nproxy_pass http://unix:/run/gunicorn.sock;\n}\n}\n'
	with open(f'/etc/nginx/sites-available/{project_name}', 'w', encoding='utf-8') as file:
		file.write(file_data)
	commands = [f'ln -s /etc/nginx/sites-available/{project_name} /etc/nginx/sites-enabled', 'systemctl restart nginx']
	for command in commands:
		s(command)


def setup():
	input('!!!Предупреждение!!!\nФайл должен быть запущен с правами суперпользователя!')

	path_to_project = input('Введите путь к проекту: ')
	domen = input('Введите домен, на котором будет работать сайт: ')
	project_name = input('Введите название проекта (имя папки): ')
	unix_username = input('Введите имя пользователя: ')

	apps_setup()
	gunicorn_setup(unix_username, path_to_project, project_name)
	nginx_setup(path_to_project, project_name, domen)


if __name__ == '__main__':
	setup()
