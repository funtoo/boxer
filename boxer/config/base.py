#!/usr/bin/python3

import logging
import os

from boxer.model import set_model
from boxer.pretty_logging import TornadoPrettyLogFormatter
from subpop.config import SubPopModel
from boxer.context import GitRepositoryLocator

class BoxerConfig(SubPopModel):
	"""
	This class contains configuration settings common to all the metatools plugins and tools.
	"""

	logger_name = "boxer"
	stage = None
	root = None
	target = None

	def __init__(self):
		super().__init__()

	async def initialize(self, stage=None, debug=False, target=None):
		if not stage:
			raise ValueError("stage not defined.")
		elif not os.path.exists(stage):
			raise FileNotFoundError(f"Cannot find stage: {stage}")
		self.stage = stage
		self.target = target
		self.root = GitRepositoryLocator().root
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
		set_model(self.logger_name, self)




