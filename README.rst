Funtoo Boxer Container Tools
============================

This repository contains Funtoo Linux tools for creation of containers
from Funtoo stage3 tarballs. Target container image formats currently
supported are:

  1. Docker (20.10.17) images
  2. Singularity (3.8.7) images

The resultant containers are designed to be long-running and have an
official Funtoo startup process -- in other words, /sbin/init will
start, OpenRC will initialize the system, and thus standard Funtoo
services such as mail servers can be set up and started using OpenRC,
OpenRC supervised processes will work correctly, env-update will
work correctly, etc.

In some cases, it will also be possible to use these containers to
have a different entrypoint and bypass the official startup process
of Funtoo Linux and run a specific executable, but to support full
Funtoo Linux functionality we will be focusing on long-running
containers for the purpose of this document.

Prerequisites
=============

For the container system you wish to make images for, you will need
to have that container system installed locally and your user account
will need permission to use it. In addition, you will also need Python
3, SubPop, Jinja2 and PyYAML installed and available. This can be
accomplished by installing funtoo-boxer from PyPi via ``pip install``
or by installing the ``boxer`` Funtoo package.

Direct-From-Git Option
======================

If you install all necessary dependencies, it's easily possible to
run boxer from a live git repository. This can be done as follows::

  $ git clone
  $ cd funtoo-boxer
  $ export PYTHONPATH=$(pwd)
  $ bin/boxer

Generating Docker Containers
============================

Here is an example of using boxer to create a Docker container from
a Funtoo stage3, launching it, and entering it and running commands
inside it::

  $ boxer --target docker --tag funtoo/boxer-generic_64:2022-06-16 /var/tmp/stage3-generic_64-next-2022-06-16.tar.xz
  ...
  Successfully built cb852d7b7b6e
  Successfully tagged funtoo/boxer-generic_64:2022-06-16

  $ docker run -d --name=foobs funtoo/boxer-generic_64:2022-06-16

  $ docker exec -it foobs /bin/bash
  03ec0962bada / # ego sync
  ...
