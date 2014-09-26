from sqlalchemy.ext.declarative import declarative_base as real_declarative_base

declarative_base = lambda cls: real_declarative_base(cls=cls)

@declarative_base
class Base(object):
    def __init__(self):
        self.__mapping__ = {}

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.columnitems)

    @property
    def columns(self):
        return [column.name for column in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(column, getattr(self, column)) for column in self.columns])

    @classmethod
    def from_dict(cls, values, mapping=None, instance=None):
        key_preset = ''
        list_mode = None
        if mapping is None:
            mapping = cls.__mapping__
        if '__preset__' in mapping:
            key_preset = mapping['__preset__'] + '_'
        if '__list_mode__' in mapping:
            list_mode = mapping['__list_mode__']
        if list_mode == 'first':
            values = values[0]
        if instance is None:
            instance = cls()
        for key, value in values.iteritems():
            if key in mapping:
                mapped_key = mapping[key]
                if mapped_key is None:
                    continue
                elif isinstance(mapped_key, dict):
                    cls.from_dict(value, mapped_key, instance)
                elif isinstance(mapped_key, tuple):
                    setattr(instance, key_preset + mapped_key[0], mapped_key[1](value))
                elif hasattr(mapped_key, '__call__'):
                    setattr(instance, key_preset + key, mapped_key(value))
                else:
                    setattr(instance, key_preset + mapped_key, value)
            else:
                if hasattr(instance, key_preset + key):
                    setattr(instance, key_preset + key, value)
        return instance

    def to_dict(value):
        result = dict()
        for key in value.__mapper__.c.keys():
            result[key] = getattr(value, key)
        return result

