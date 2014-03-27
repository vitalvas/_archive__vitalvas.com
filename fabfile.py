# coding: utf-8
import os
from fabric.api import run, env, cd, roles, sudo

env.roledefs['test'] = ['vitalvas@cs1.jotcdn.net']
env.roledefs['production'] = ['vitalvas@cs2.jotcdn.net']

def production_env():
	env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]
	env.project_root = '/srv/apps/vitalvascom'
	env.python = '/srv/venv/vitalvascom/bin/python'
	env.pip = '/srv/venv/vitalvascom/bin/pip'

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

@roles('test')
def deploy_test():
	deploy_proc()

@roles('production')
def deploy():
	deploy_proc()