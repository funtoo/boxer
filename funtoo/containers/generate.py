import sys

import dyne.org.funtoo.boxer.containers as containers


async def start():
	try:
		if containers.model.target == "docker":
			containers.docker.create_docker_container()
		else:
			containers.model.log.error("target not supported.")
	except ChildProcessError as e:
		sys.exit(1)

