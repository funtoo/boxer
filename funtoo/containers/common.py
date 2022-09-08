import subprocess

import dyne.org.funtoo.boxer.containers as containers


def cmd(cwd, cmd: list, desc: str = None):
	if desc:
		containers.model.log.info(desc)
	containers.model.log.debug(f"cwd: {cwd}")
	containers.model.log.info(f"Running command: {cmd}")
	result = subprocess.run(cmd, cwd=cwd)
	if result.returncode != 0:
		containers.model.log.error(f"Error: exit code {result.returncode}.")
		raise ChildProcessError()
