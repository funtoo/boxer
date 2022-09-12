import os
import subprocess
import jinja2

import dyne.org.funtoo.boxer.containers as containers
from subpop.util import AttrDict


dockerfile = """
# we are going to use alpine as our bootstrap container
ARG BOOTSTRAP
FROM ${BOOTSTRAP:-alpine:3.13} as builder

WORKDIR /funtoo

ARG STAGE3="{{stage}}"

COPY "${STAGE3}" /
RUN echo "Building Funtoo Container image." \
 && sleep 3 \
 && apk --no-cache add gnupg tar wget xz \
 && tar xpf /${STAGE3} --xattrs --xattrs-include='*' --numeric-owner \
 && sed -i -e 's/#rc_sys=""/rc_sys="docker"/g' etc/rc.conf \
 && rm -f etc/localtime \
 && ln -s ../usr/share/zoneinfo/UTC etc/localtime \
 && rm /*.xz

FROM scratch

WORKDIR /
COPY --from=builder /funtoo/ /
RUN echo "Customizing funtoo for the needs of the people." \
 && rm /etc/fstab \
 && touch /etc/fstab \
 && sed -i -e 's/^c/#c/g' /etc/inittab \
 && rm -rf /usr/src/linux* \
 && rm -rf /var/db/pkg/sys-kernel/debian-sources* \
 && rc-update del sysctl boot \
 && rc-update del hostname boot \
 && rc-update del loopback boot \
 && rc-update del udev sysinit \
 && rc-update del bootmisc boot \
 && rm -rf /var/git/* \
 && rm -rf /lib/modules/*
ENTRYPOINT ["/sbin/init"]
"""

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
	args = get_docker_args()
	template = jinja2.Template(dockerfile)
	outfile = os.path.join(containers.model.tmp, 'Dockerfile')
	with open(outfile, "wb") as myf:
		myf.write(template.render(**args).encode("utf-8"))
		containers.model.log.debug(f"Output written to {outfile}.")
	dest_stage = os.path.join(containers.model.tmp, containers.model.stage.name)
	if os.path.exists(dest_stage):
		os.unlink(dest_stage)
	cmd(containers.model.tmp, ["cp", containers.model.stage, "."], desc="Copy stage to temp directory")
	base_cmd = ["docker", "build", "."]
	if args.tag:
		base_cmd += ["-t", args.tag]
	cmd(containers.model.tmp, base_cmd, desc="Creating docker container")
	if args.tag and args.push:
		cmd(containers.model.tmp, ["docker", "push", args.tag], desc="Pushing container")
	return True

