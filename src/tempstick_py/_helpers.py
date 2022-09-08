from datetime import datetime
import re


def format_mac(mac: str) -> str:
    """Return canonical MAC address

    Taken exactly from https://stackoverflow.com/a/29446103/19251950

    :param mac: Common MAC address; may include common delimiters and mixed-case
    :type mac: str
    :return: Canonical MAC address of form '00:80:41:ae:fd:7e'
    :rtype: str
    """
    mac = re.sub(
        "[.:-]", "", mac
    ).lower()  # remove delimiters and convert to lower case
    mac = "".join(mac.split())  # remove whitespaces
    assert len(mac) == 12  # length should be now exactly 12 (eg. 008041aefd7e)
    assert mac.isalnum()  # should only contain letters and numbers
    mac = ":".join(["%s" % (mac[i : i + 2]) for i in range(0, 12, 2)])
    return mac


# 2022-09-04 07:00:00Z
def format_datetime(dt: str) -> datetime:
    obj = datetime.strptime(dt, "%Y-%m-%d %H:%M:%SZ")
    return obj


def set_attr_from_dict(cls, values: dict):
    for key, val in values.items():
        setattr(cls, key, val)


def debug_print(var_name, var_value, cls):
    name = cls.__class__.__name__
    value = "{parent} | {name}: {value}".format(
        parent=name, name=var_name, value=var_value
    )
    print(value)
