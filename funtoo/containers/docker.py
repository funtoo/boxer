import os
import subprocess
import jinja2

import dyne.org.funtoo.boxer.containers as containers
from subpop.util import AttrDict


def get_docker_args():
	return AttrDict({
		"push": containers.model.push,
		"tag": containers.model.tag,
		"stage": containers.model.stage.name,
	})


def cmd(cwd, cmd: list, desc: str = None):
	if desc:
		containers.model.log.info(desc)
	containers.model.log.debug(f"cwd: {cwd}")
	containers.model.log.info(f"Running command: {cmd}")
	result = subprocess.run(cmd, cwd=cwd)
	if result.returncode != 0:
		containers.model.log.error(f"Error: exit code {result.returncode}.")
		raise ChildProcessError()


def create_container():
	dfpath = os.path.join(containers.model.root, 'templates', 'Dockerfile.tmpl')
	args = get_docker_args()
	try:
		with open(dfpath, "r") as tempf:
			template = jinja2.Template(tempf.read())
			outfile = os.path.join(containers.model.tmp, 'Dockerfile')
			with open(outfile, "wb") as myf:
				myf.write(template.render(**args).encode("utf-8"))
				containers.model.log.debug(f"Output written to {outfile}.")
			dest_stage = os.path.join(containers.model.tmp, containers.model.stage.name)
			if os.path.exists(dest_stage):
				os.unlink(dest_stage)
			cmd(containers.model.tmp, ["cp", containers.model.stage, "."], desc="Copy stage to temp directory")
			base_cmd = ["docker", "build", "--rm", "."]
			if args.tag:
				base_cmd += ["-t", args.tag]
			cmd(containers.model.tmp, base_cmd, desc="Creating docker container")
			if args.tag and args.push:
				cmd(containers.model.tmp, ["docker", "push", args.tag], desc="Pushing container")
			return True
	except FileNotFoundError as e:
		containers.model.log.error(f"Could not find template: {dfpath}")
		raise e

