"""Удобные декораторы для конфигов

@env_config
class AgentConf:
    DH_RABBIT_URI: str
    DH_HUB_HOST: str
    DH_HUB_PORT: int
    DH_DATAHUB_QUEUE_NAME = "DataHub"

Декларируем класс с нужными параметрами, в них автоматически подставляются
соответствующие переменные окружения. Можно задать тип и значение по умолчанию.
Если значение по умолчанию не задано и переменная окружения не установлена
при доступе к параметру вывалится исключение.

Нужно для того, чтобы собрать в одном месте информацию о том, какими переменными
пользуется приложение.
"""

import os
import re


# ====================================================
# Не очень удобные декораторы - все переменные подсасываются при старте
from typing import Mapping


def dict_config2(d):
    def decor(cls):
        annotations = getattr(cls, '__annotations__', {})
        attributes = {
            a: getattr(cls, a)
            for a in dir(cls)
            if not re.match(r'__(.+)__', a)
        }
        for a in set(annotations.keys()) | set(attributes.keys()):
            desired_type = annotations[a] if a in annotations else type(attributes[a])
            try:
                value = d[a] if a in d else attributes[a]
            except KeyError:
                raise ValueError(f"BAD CONFIG: Nor default nor actual value provided for {a}")

            try:
                setattr(cls, a, desired_type(value))
            except ValueError as e:
                raise ValueError("BAD CONFIG: Can not convert type for {}: {}".format(a, e))

        return cls

    return decor


def env_config2(cls):
    return dict_config2(os.environ)(cls)


# ====================================================
# Немного питоножести - lazy декораторы,
# к переменной окружения обращаемся только при необходимости

def getter_factory(config: Mapping, attributes: dict, annotations: dict, attr: str):
    class Getter:
        def __get__(self, instance, owner):

            desired_type = annotations[attr] if attr in annotations else type(attributes[attr])

            try:
                value = config[attr] if attr in config else attributes[attr]
            except KeyError:
                raise ValueError(f"BAD CONFIG: Nor default nor actual value provided for {attr}")

            try:
                value = desired_type(value)
            except ValueError as e:
                raise ValueError("BAD CONFIG: Can not convert type for {}: {}".format(attr, e))

            return value

    return Getter


def dict_config(config: Mapping):
    def decor(cls):
        attributes = {
            a: getattr(cls, a)
            for a in dir(cls)
            if not re.match(r'__(.+)__', a)
        }
        annotations = getattr(cls, '__annotations__', {})

        for a in set(annotations.keys()) | set(attributes.keys()):
            setattr(cls, a, getter_factory(config, attributes, annotations, a)())

        return cls

    return decor


def env_config(cls):
    return dict_config(os.environ)(cls)
