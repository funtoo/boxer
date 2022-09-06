import dyne.org.funtoo.boxer.containers as containers


async def start(stage=None):
	containers.model.log.debug("hello there.")
	containers.model.log.info(f"I am at root: {containers.model.root}")