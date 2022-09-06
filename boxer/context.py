#!/usr/bin/env python3

import os

from subpop.config import ConfigurationError


class Locator:
	start_path = None
	root: str = None
	expected_files = []
	"""
	This method will look, from the current directory, and find the 'context' of where
	we are in a kit-fixups repository, so we know where the main kit-fixups repository
	is and what is our current working set for autogeneration.
	"""

	def found_root(self, cur_path) -> bool:
		for file in self.expected_files:
			if not os.path.exists(os.path.join(cur_path, file)):
				return False
		return True

	def find_root(self):
		"""
		This method starts from ``start_path`` and looks backwards in the path structure until it
		gets to the point where it finds a 'profiles/repo_name' and/or 'metadata/layout.conf' file,
		which indicates that it is at the root of an overlay, and then it returns this value.

		If it gets to / without finding these files, it returns None as a failure indicator that
		it couldn't find the overlay that we are currently inside of via the current working
		directory.
		"""
		cur_path = self.start_path
		while (
				cur_path != "/"
				and not self.found_root(cur_path)
		):
			cur_path = os.path.dirname(cur_path)
		if cur_path == "/":
			cur_path = None
		return cur_path

	def __init__(self, start_path=None):
		self.start_path = start_path if start_path else os.getcwd()
		self.root = self.find_root()
		if self.root is None:
			raise ConfigurationError(f"Could not determine context in {self.start_path}. Trying to find these marker files: {self.expected_files}")

class GitRepositoryLocator(Locator):
	expected_files = [".git"]
