from os import system as s


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
	path_to_venv = input('Enter path to venv: ')
	path_to_project = input('Enter path to project: ')
	domen = input('Enter site domen name: ')
	project_name = input('Enter project folder name: ')
	unix_username = input('Enter unix user for setup: ')

	gunicorn_setup(unix_username, path_to_project, project_name)
	nginx_setup(path_to_project, project_name, domen)


if __name__ == '__main__':
	setup()
