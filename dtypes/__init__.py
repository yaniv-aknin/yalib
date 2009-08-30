"Classes that try to behave like a native Python datatype"

class Bag(dict):
    def __getattr__(self, attribute_name):
        if attribute_name in self:
            return self[attribute_name]
        raise AttributeError("%r object has no attribute %r" % (self.__class__.__name__, attribute_name))
    def __setattr__(self, attribute_name, attribute_value):
        self.__setitem__(attribute_name, attribute_value)
