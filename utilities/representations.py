import json


class AsDictionaryMixin:
    default_indent = 2

    def to_dict(self):
        return {
            prop: self._represent(value)
            for prop, value in self.__dict__.items()
            if not self._is_internal(prop)
        }

    @staticmethod
    def print_dict(obj, indent=default_indent):
        print(json.dumps(obj, indent=indent))

    def _represent(self, value):
        if isinstance(value, object):
            if hasattr(value, 'to_dict'):
                return value.to_dict()
            else:
                return str(value)
        else:
            return value

    def _is_internal(self, prop):
        return prop.startswith('_')
