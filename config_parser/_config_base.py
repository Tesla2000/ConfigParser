from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import Field

load_dotenv()


class ConfigBase(BaseModel):
    _root: Path = Field(default_factory=lambda: Path(os.getcwd()))
    pos_args: list[str] = Field(default_factory=list)
    config_file: Optional[Path] = None
