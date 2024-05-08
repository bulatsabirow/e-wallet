import argparse
import enum


class CaseInsensitiveTuple(tuple[str]):
    def __contains__(self, item):
        # use .lower() method to make tuple case insensitive
        if isinstance(item, str):
            return super().__contains__(item.lower())

        return super().__contains__(item)


class EnumAction(argparse.Action):
    """
    Argparse action for handling Enums
    """

    def __init__(self, **kwargs):
        # Pop off the type value
        enum_type = kwargs.pop("type", None)

        # Ensure an Enum subclass is provided
        if enum_type is None:
            raise ValueError("type must be assigned an Enum when using EnumAction")
        if not issubclass(enum_type, enum.Enum):
            raise TypeError("type must be an Enum when using EnumAction")

        # Generate choices from the Enum
        kwargs.setdefault("choices", CaseInsensitiveTuple(e.value for e in enum_type))

        super(EnumAction, self).__init__(**kwargs)
        self._enum = enum_type

    def __call__(self, parser, namespace, values, option_string=None):
        # Convert value back into an Enum
        value = self._enum(values).value
        setattr(namespace, self.dest, value)
