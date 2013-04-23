#!/usr/bin/env python

import os
from fabric.api import run, env, cd, roles


env.roledefs['production'] = [
	'root@cs2.jotcdn.net',
#	'root@cs3.jotcdn.net'
]


def production_env():
	env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]
	env.user = 'root'
	env.project_root = '/srv/apps/mypage'
	env.python = '/srv/env/bin/python'


@roles('production')
def deploy():
	production_env()
	with cd(env.project_root):
		run('git pull')
#		run('srvenv update config')
		run('supervisorctl restart mypage')
