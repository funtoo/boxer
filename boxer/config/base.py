#!/usr/bin/python3

import logging
import os
import pathlib
import shutil

from boxer.common import parse_args
from boxer.model import set_model
from boxer.pretty_logging import TornadoPrettyLogFormatter
from subpop.config import SubPopModel, ConfigurationError
from boxer.context import GitRepositoryLocator


class BoxerConfig(SubPopModel):
	"""
	This class contains configuration settings common to all the metatools plugins and tools.
	"""

	logger_name = "boxer"
	stage = None
	root = None
	tmp = None
	sub = None

	def __init__(self):
		super().__init__()

	async def initialize(self, stage=None, debug=False):

		if not stage:
			raise ValueError("stage not defined.")
		stage = pathlib.Path(stage).expanduser().resolve()
		if not stage.exists():
			raise FileNotFoundError(f"Cannot find stage: {stage}")
		self.stage = stage
		try:
			self.root = GitRepositoryLocator().root
		except ConfigurationError:
			self.root = f"/var/tmp/boxer_{os.getlogin()}_{os.getpid()}"
		self.tmp = self.root + "/tmp"
		if os.path.exists(self.tmp):
			shutil.rmtree(self.tmp)
		os.makedirs(self.tmp, exist_ok=False, mode=0o700)
		self.log = logging.getLogger(self.logger_name)
		self.log.propagate = False
		if debug:
			self.debug = debug
			self.log.setLevel(logging.DEBUG)
		else:
			self.log.setLevel(logging.INFO)
		channel = logging.StreamHandler()
		channel.setFormatter(TornadoPrettyLogFormatter())
		self.log.addHandler(channel)
		if debug:
			self.log.warning("DEBUG enabled")
		set_model("containers", self)


class DockerConfig(BoxerConfig):

	tag = None
	push = None
	sub = "docker"

	CLI_CONFIG = {
		"push": {"default": False, "action": "store_true"},
		"tag": {"default": None, "action": "store", "help": "Set a tag/name for the resultant container"},
	}

	async def initialize(self, stage=None, debug=False, extra_args=None):
		local_args = parse_args(self.CLI_CONFIG, extra_args)
		await super().initialize(stage=stage, debug=debug)
		self.push = local_args.push
		self.tag = local_args.tag


class SingularityConfig(BoxerConfig):

	out = None
	force = False
	sub = "singularity"

	CLI_CONFIG = {
		"out": {"default": None, "action": "store", "help": "Set an output filename/path for .sif file for singularity container."},
		"force": {"default": False, "action": "store_true", "help": "Force overwrite of existing singularity container."},
	}

	async def initialize(self, stage=None, debug=False, extra_args=None):
		local_args = parse_args(self.CLI_CONFIG, extra_args)
		await super().initialize(stage=stage, debug=debug)
		self.out = local_args.out
		self.force = local_args.force
