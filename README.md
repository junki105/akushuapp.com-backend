# MusicianBackend Backend Deploy Guide

## Development setup

### Install required system packages:
    sudo apt update
    sudo apt-get install python3-pip
    sudo apt-get install python3-dev python3-setuptools
    sudo apt-get install libpq-dev
    sudo apt-get install postgresql postgresql-contrib
    sudo apt-get install mysql-server
    sudo apt-get install libmysqlclient-dev

### Create www directory where project sites and environment dir

    mkdir /var/www && mkdir /var/envs && mkdir /var/envs/bin

### Install virtualenvwrapper

    sudo pip3 install virtualenvwrapper
    sudo pip3 install --upgrade virtualenv

### Add these to your bashrc virutualenvwrapper work

    export WORKON_HOME=/var/envs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    export PROJECT_HOME=/var/www
    export VIRTUALENVWRAPPER_HOOK_DIR=/var/envs/bin
    source /usr/local/bin/virtualenvwrapper.sh

### Create virtualenv

    cd /var/envs && mkvirtualenv --python=/usr/bin/python3 musician

### Install requirements for a project.

    cd /var/www/musician && pip install -r requirements.txt

    sudo chown :www-data /var/www/musician

### Database creation

    sudo mysql -u root -p
    mysql > DROP DATABASE IF EXISTS database_name;
    mysql > CREATE DATABASE database_name CHARACTER SET utf8;
    mysql > CREATE USER 'db_user_name'@'localhost' IDENTIFIED BY 'password';
    mysql > GRANT ALL PRIVILEGES ON database_name.* TO 'db_user_name'@'localhost';
