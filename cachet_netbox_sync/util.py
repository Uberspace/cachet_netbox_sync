
import operator


def deepgetattr(obj, attr):
    try:
        return operator.attrgetter(attr)(obj)
    except (AttributeError, TypeError):
        return None
