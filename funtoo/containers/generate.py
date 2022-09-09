import os
import shutil
import sys

import dyne.org.funtoo.boxer.containers as containers

from boxer.config.base import SingularityConfig, DockerConfig


async def start():
	errcode = 0
	try:
		if isinstance(containers.model, SingularityConfig):
			success = containers.singularity.create_container()
		elif isinstance(containers.model, DockerConfig):
			success = containers.docker.create_container()
	except ChildProcessError as e:
		errcode = 1
	finally:
		if os.path.exists(containers.model.tmp):
			shutil.rmtree(containers.model.tmp)
	if not success:
		errcode = 1
	sys.exit(errcode)

