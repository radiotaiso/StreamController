"""
Author: Core447
Year: 2024

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This programm comes with ABSOLUTELY NO WARRANTY!

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
from src.backend.Migration.Migrator import Migrator

from loguru import logger as log

class MigrationManager:
    def __init__(self):
        self.migrators: list[Migrator] = []
        pass

    def add_migrator(self, migrator: Migrator):
        self.migrators.append(migrator)

    def run_migrators(self):
        for migrator in self.get_ordered_migrators():
            if migrator.get_need_migration():
                log.info(f"Running migrator to app version {migrator.app_version}")
                migrator.create_backup()
                migrator.migrate()
                log.success(f"Successfully ran migrator to app version {migrator.app_version}")

    def get_ordered_migrators(self) -> list[Migrator]:
        return sorted(self.migrators, key=lambda migrator: migrator.parsed_app_version)