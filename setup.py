import setuptools
from subpop.pkg import Packager, SubPopSetupInstall

pkgr = Packager()

with open("README.rst", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="funtoo-boxer",
	version="1.0.3",
	author="Daniel Robbins",
	author_email="drobbins@funtoo.org",
	description="Funtoo framework for container generation.",
	long_description=long_description,
	long_description_content_type="text/x-rst",
	url="https://code.funtoo.org/bitbucket/users/drobbins/repos/funtoo-boxer/browse",
	scripts=["bin/boxer"],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: POSIX :: Linux",
	],
	python_requires=">=3.7",
	install_requires=[
		"colorama",
		"subpop >= 2.0.0",
		"Jinja2 >= 3",
		"PyYAML"
	],
	packages=setuptools.find_packages(),
	data_files=pkgr.generate_data_files(),
	cmdclass={"install": SubPopSetupInstall},
)

# vim: ts=4 sw=4 noet
