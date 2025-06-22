from __future__ import annotations

from argparse import Namespace
from pathlib import Path
from typing import get_origin
from typing import Literal
from typing import Type
from typing import TypeVar

import toml
from pydantic_core import PydanticUndefined

from config_parser._config_base import ConfigBase
from config_parser._custom_argument_parser import CustomArgumentParser

_ConfigType = TypeVar("_ConfigType", bound=ConfigBase)


class ConfigCreator:
    def __init__(
        self, description: str = "Configure the application settings."
    ):
        self.description = description

    def create_config(self, config_class: Type[_ConfigType]) -> _ConfigType:
        return self._create_config_with_args(
            config_class, self._parse_arguments(config_class)
        )

    def _parse_arguments(self, config_class: Type[_ConfigType]) -> Namespace:
        parser = CustomArgumentParser(description=self.description)

        for name, value in config_class.model_fields.items():
            if name.startswith("_"):
                continue
            annotation = value.annotation
            if len(getattr(value.annotation, "__args__", [])) > 1:
                annotation = next(filter(None, value.annotation.__args__))
            if get_origin(value.annotation) == Literal:
                annotation = str
            parser.add_argument(
                f"--{name}" if name != "pos_args" else name,
                type=annotation,
                default=value.default,
                help=f"Default: {value}",
            )

        return parser.parse_args()

    @staticmethod
    def _create_config_with_args(
        config_class: Type[_ConfigType], args: Namespace
    ) -> _ConfigType:
        arg_dict = {
            name: getattr(args, name)
            for name in config_class.model_fields.keys()
            if hasattr(args, name) and getattr(args, name) != PydanticUndefined
        }
        if (
            arg_dict.get("config_file")
            and Path(arg_dict["config_file"]).exists()
        ):
            config = config_class.model_validate(
                {
                    **arg_dict,
                    **toml.load(arg_dict.get("config_file")),
                }
            )
        else:
            config = config_class.model_validate(arg_dict)
        for variable in config_class.model_fields.keys():
            value = getattr(config, variable)
            if (
                isinstance(value, Path)
                and value.suffix == ""
                and not value.exists()
            ):
                value.mkdir(parents=True)
        return config
