add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt upgrade

apt install python3.11 -y

apt install git -y
apt install nginx -y
apt install mysql-server -y
apt install mysql-client -y

apt install python3-dev -y
apt install libmysqlclient-dev -y
apt install python3-venv -y
apt install python3-pip -y
apt install python-is-python3 -y


test -f /home/$USER/.ssh/id_rsa.pub || ssh-keygen -t rsa -b 4096 -C dshutrin@mail.ru -f /home/$USER/.ssh/id_rsa -N ""
clear

service nginx status
cat /home/$USER/.ssh/id_rsa.pub
