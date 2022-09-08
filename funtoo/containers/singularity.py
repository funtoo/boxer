
import os

import dyne.org.funtoo.boxer.containers.common as common
import dyne.org.funtoo.boxer.containers as containers


def remove(rootfs, path):
	path = path.lstrip("/")
	common.cmd(rootfs, ["rm", "-rf", path], desc=f"Cleaning rootfs: {path}")


def create_singularity_container():
	rootfs = os.path.join(containers.model.tmp, "rootfs")
	os.makedirs(rootfs, exist_ok=False)
	common.cmd(rootfs,
	    ["tar", "--numeric-owner", "--xattrs", "--xattrs-include='*'", "-xpf", str(containers.model.stage), "."],
	    desc="Extracting stage tarball")
	remove(rootfs, "/usr/src/linux*")
	remove(rootfs, "/lib/modules/*")
	remove(rootfs, "/var/git/*")
	remove(rootfs, "/var/db/pkg/sys-kernel/debian-sources*")
	d_dir = os.path.join(rootfs, ".singularity.d")
	os.makedirs(os.path.join(d_dir), exist_ok=True)
	if os.path.exists(os.path.join(rootfs, "etc/mtab")):
		os.unlink(os.path.join(rootfs, "etc/mtab"))
	with open(os.path.join(rootfs, "etc/fstab"), "w") as f:
		f.write("proc /proc proc defaults 0 0\n")
	with open(os.path.join(rootfs, "etc/rc.conf"), "a") as f:
		f.write("rc_sys=lxd\n")
	with open(os.path.join(d_dir, "runscript"), "w") as f:
		f.write("""#!/bin/bash
exec /bin/bash --login
""")
	out = os.path.join(os.getcwd(), "funtoo-stage3.sif")
	common.cmd(containers.model.tmp, ["singularity", "build", out, rootfs], desc="Creating singularity container")