# Copyright (C) 2021, Hadron Industries, Inc.
# Carthage is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation. It is distributed
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the file
# LICENSE for details.

from .implementation import ModelingBase, InjectableModelType
from .utils import setattr_default


class ModelingDecoratorWrapper:

    subclass: type = ModelingBase
    name: str

    def __init__(value):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.name}({repr(self.value)})'

    def handle(self, cls, ns, k, state):
        if not issubclass(cls, self.subclass):
            raise TypeError(f'{self.__class__.name} decorator only for subclasses of {self.cls.__name__}')
        state.value =  self.value

class ProvidesDecorator(ModelingDecoratorWrapper):
    subclass = InjectableModelType
    name = "provides"

    def __init__(self, value, *keys):
        super().__init__(value)
        self.keys = keys

    def handle(self, cls, ns, k, state):
        super().handle(cls, ns, k, state)
        state.extra_keys.extend(self.keys)

def provides(*keys):
    '''Indicate that the decorated value provides these InjectionKeys'''
    def wrapper(val):
        try:
            setattr_default(val, '__provides_dependencies_for__', [])
            val.__provides_dependencies_for__ = keys+val.__provides_dependencies_for__
        except:
            return ProvidesDecorator(val, *keys)
    return wrapper

__all__ = ["ModelingDecoratorWrapper", "provides"]
