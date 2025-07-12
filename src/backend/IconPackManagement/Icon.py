"""
Author: Core447
Year: 2023

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This programm comes with ABSOLUTELY NO WARRANTY!

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import os

# Import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.backend.IconPackManagement.IconPack import IconPack

class Icon:
    def __init__(self, icon_pack: "IconPackpath", path: str):
        self.icon_pack = icon_pack
        self.path = path

        self.name = os.path.splitext(os.path.basename(path))[0]

    def get_attribution(self):
        attribution = self.icon_pack.get_attribution_json()

        if os.path.basename(self.path) in attribution:
            return attribution[os.path.basename(self.path)]
        else:
            return attribution.get("default", attribution.get("general", attribution.get("generic")))