#!/usr/bin/env python3

# This was originally added so that support classes can get access to the model without having to be
# part of the subsystem. The original way to use it was to have the MergeConfig initialize call
# set_model(self) and then a support library could call get_model("metatools.merge"). Now I am trying
# to extend this so that get_model() by itself will return *any* model, and get_model("metatools")
# will return any model that is part of metatools. This can be used with utility libraries that
# need functionality that are in the metatools BaseConfig, so *any* metatools config object will
# do.

MODELS = {}


class ModelWrapper:

	def __init__(self, name=None):
		self.name = name

	def __getattr__(self, item):
		try:
			return getattr(MODELS[self.name], item)
		except KeyError as ke:
			print(f"Available models: {MODELS.keys()}")
			raise ke


def set_model(name, model):
	model_split = name.split('.')
	if len(model_split) == 1:
		MODELS[name] = model
	elif len(model_split) == 2:
		MODELS[name] = model
		MODELS[model_split[0]] = model
	# Set default model to last set:
	MODELS[None] = model


def get_model(name):
	if name is None:
		return ModelWrapper()
	else:
		return ModelWrapper(name)
