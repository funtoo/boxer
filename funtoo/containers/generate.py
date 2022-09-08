import os
import shutil
import sys

import dyne.org.funtoo.boxer.containers as containers


async def start():
	errcode = 0
	try:
		if containers.model.target == "docker":
			containers.docker.create_docker_container()
		elif containers.model.target == "sif":
			containers.singularity.create_singularity_container()
		else:
			containers.model.log.error("target not supported.")
	except ChildProcessError as e:
		errcode = 1
	finally:
		if os.path.exists(containers.model.tmp):
			shutil.rmtree(containers.model.tmp)
	sys.exit(errcode)

