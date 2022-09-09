import argparse
import subprocess

from boxer.model import get_model

model = get_model('containers')


def cmd(cwd, cmd: list, desc: str = None):
	if desc:
		model.log.info(desc)
	model.log.debug(f"cwd: {cwd}")
	model.log.info(f"Running command: {cmd}")
	result = subprocess.run(cmd, cwd=cwd)
	if result.returncode != 0:
		model.log.error(f"Error: exit code {result.returncode}.")
		raise ChildProcessError()


def parse_args(cli_config, args=None, parse_known=False):
	ap = argparse.ArgumentParser()
	for arg, kwargs in cli_config.items():
		if "positional" in kwargs and kwargs["positional"]:
			new_kwargs = kwargs.copy()
			del new_kwargs["positional"]
			ap.add_argument(arg, **new_kwargs)
		else:
			if "os" in kwargs:
				del kwargs["os"]
			ap.add_argument("--" + arg, **kwargs)
	if parse_known:
		return ap.parse_known_args(args)
	else:
		return ap.parse_args(args)
