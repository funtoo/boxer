Funtoo Boxer Container Tools
============================

Author: Daniel Robbins <drobbins@funtoo.org>;
Copyright 2022, Daniel Robbins, Funtoo Solutions, Inc.

License
~~~~~~~

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.

Official Location
~~~~~~~~~~~~~~~~~

The official location for boxer is at:

https://github.com/funtoo/boxer

Issues for boxer can be filed as GitHub issues or at https://bugs.funtoo.org,
using an account created at https://auth.funtoo.org/new.

Introduction
~~~~~~~~~~~~

This repository contains Funtoo Linux tools for creation of containers
and/or virtual machine images from Funtoo stage3 tarballs. This tool
exists so that Funtoo users don't need to search for a magic script
scattered somewhere on the Internet to create a container -- instead,
we now have an official tool to create any kind of image desired, all
with a single tool, and is officially supported, maintained and
documented by the Funtoo Linux project. It is my hope that users of
this tool will find it to be convenient and trouble-free to use.

Compatibility
~~~~~~~~~~~~~

The 1.0.0 release initially supports the following container formats,
with more to be added in future releases:

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
Funtoo Linux functionality, we will always strive to offer fully-
functional, long-running Funtoo Linux containers will full OpenRC
support as our primary target.

Prerequisites
~~~~~~~~~~~~~

For the container system you wish to make images for, you will need
to have that container system installed locally and your user account
will need permission to use it.

In addition, you will also need Python 3.7 or higher, and the
SubPop, Jinja2 and PyYAML python modules installed and available.
This can be accomplished by installing funtoo-boxer from PyPi via::

  $ pip install funtoo-boxer

or by installing the ``boxer`` Funtoo package under Funtoo Linux
as follows::

  $ emerge boxer

Direct-From-Git Option
~~~~~~~~~~~~~~~~~~~~~~

If you install all necessary dependencies, it's easily possible to
run boxer from a live git repository. This can be done as follows::

  $ git clone https://github.com/funtoo/boxer
  $ cd boxer
  $ export PYTHONPATH=$(pwd)
  $ bin/boxer

When run from a git repository, the ``tmp`` directory within the
git repository will be used as temporary storage for building
containers. When installed as a package, a directory within
``/var/tmp`` will be used for this purpose.

Starting from Stage3
~~~~~~~~~~~~~~~~~~~~

The ``boxer`` utility is designed to always start from a "stage3
tarball" downloaded from https://build.funtoo.org, or built using
Funtoo's metro build tool. This stage3 will be finalized by boxer
to make a functioning container for one of the supported targets.

Now, let's look at the different targets supported by boxer and
how to use them.

Generating Docker Containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set up Docker
-------------

On a Funtoo Linux system, you will need to set up Docker and start
the ``docker`` service, and add your current user to the ``docker``
group if you would like to be able to run ``boxer`` without being
root::

  $ sudo emerge docker
  $ sudo rc-update add docker default
  $ sudo rc
  $ sudo usermod -a -G docker $USER
  <log out, log back in>

Create a Docker Container
-------------------------

When generating a Docker container, the container you generate will
be added to the local Docker image repository, and the tag specified
by the ``--tag`` option will be applied to the image, if provided.
Additionally, the ``--push`` option can be used to also instruct
boxer to push the image to Docker Hub.

Here is an example of using boxer to create a Docker container from
a Funtoo stage3, launching it, and entering it and running commands
inside it::

  $ boxer docker --tag funtoo/boxer-generic_64:2022-06-16 --stage /var/tmp/stage3-generic_64-next-2022-06-16.tar.xz
  $ docker run -d --name=foobs funtoo/boxer-generic_64:2022-06-16
  $ docker exec -it foobs /bin/bash
  03ec0962bada / # ego sync
  ...

Generating Singularity Containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set up Singularity
------------------

On a Funtoo Linux system, you will simply need to
``emerge sys-cluster/singularity``. Singularity is a standalone tool
so it doesn't require a standalone system daemon running like Docker or LXD.

Create a Singularity Container
------------------------------

When using boxer to generate a Singularity ("sif format") container,
the container will by default be written to a file named ``stage3-funtoo.sif``
in the current working directory. Alternatively, the ``--out <filename>``
option can be used to specify an alternate location and/or name. Additionally,
the ``--force`` option can be used to overwrite the target file if it exists.

When creating a Singularity container for non-personal or production
use, it is recommended to run boxer as root, which will allow for
permissions, extended attributes and ACLs to be properly preserved within
the resultant container rather than being mapped to the user id of the
currently-running user. We will use this method in the following example,
below::

  $ sudo boxer sif --stage /var/tmp/stage3-generic_64-next-2022-06-16.tar.xz --force
  $ sudo singularity instance start --boot --writable-tmpfs funtoo-stage3.sif f1
  $ sudo singularity shell instance://f1

As noted, this documentation demonstrates the use of long-running containers
that properly start ``/sbin/init`` as the first process in the container, and
start OpenRC so that a fully-functional Funtoo Linux system is available. It
is also possible to simply execute a binary within the Funtoo environment
without using instances.

Starting Writable Singularity Funtoo Containers
...............................................

Also note the use of the ``--writable-tmpfs`` option, above. This allows
singularity (which uses a read-only squashfs filesystem by default) to
write inside the container, which allows things like ``sshd``
to generate its initial host keys, and other important things for official
Funtoo Linux booting that expect a writable root filesystem. However, this
tmpfs option is only really suitable for minimal I/O within the container
and will be exhausted if you perform any significant I/O such as running
``ego sync``. If you are planning to use the container for more
significant work, such as the running of ``ego sync`` and ``emerge``,
you will likely want to create an overlay filesystem of a suitable size
to allow these actions to complete successfully without filling up the
tmpfs overlay we used above. Below, we create an overlay of 4096 MiB
to support writes within our singularity instance::

  $ singularity overlay create --size 4096 ./overlay.img
  $ sudo singularity instance start --boot --overlay ./overlay.img funtoo-stage3.sif f2
  $ sudo singularity shell instance://f2
  Singularity> ego sync

Launching a Singularity container using this technique will allow the
instance to be used as a fully functional Funtoo Linux system -- for
development, or other tasks.
