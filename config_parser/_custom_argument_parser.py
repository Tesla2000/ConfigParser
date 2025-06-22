from __future__ import annotations

import argparse
from types import GenericAlias


class CustomArgumentParser(argparse.ArgumentParser):
    def add_argument(
        self,
        *args,
        **kwargs,
    ):
        if isinstance(kwargs.get("type"), GenericAlias):
            kwargs["type"] = kwargs.get("type").__origin__
        if isinstance(kwargs.get("type"), type):
            if issubclass(kwargs.get("type"), bool):
                kwargs["type"] = str
            elif issubclass(kwargs.get("type"), list):
                kwargs["nargs"] = "*"
                kwargs["type"] = str
            elif issubclass(kwargs.get("type"), tuple):
                kwargs["nargs"] = "+"
                kwargs["type"] = str
        super().add_argument(
            *args,
            **kwargs,
        )
