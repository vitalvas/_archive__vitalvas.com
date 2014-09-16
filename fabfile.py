# coding: utf-8
import os
from fabric.api import run, env, cd, roles, sudo

env.roledefs['production'] = ['vitalvas@cs3.jotcdn.net']

def production_env():
	env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]
	env.project_root = '/srv/apps/vitalvascom'
	env.python = '/opt/venv/vitalvascom/bin/python'
	env.pip = '/opt/venv/vitalvascom/bin/pip'

def deploy_proc():
	production_env()
	with cd(env.project_root):
		sudo('git pull origin')
		sudo('{pip} install --upgrade -r {filepath}'.format(pip=env.pip,
			filepath=os.path.join(env.project_root, 'requirements.txt')))
		sudo('{} manage.py collectstatic --noinput'.format(env.python))
		sudo('{} manage.py syncdb --noinput'.format(env.python))
		sudo('supervisorctl restart vitalvascom')
		sudo('service nginx reload')


@roles('production')
def deploy():
	deploy_proc()