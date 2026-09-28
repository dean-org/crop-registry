# ruff: noqa: E402
import asyncio
import logging

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_registry_core.app import Initializer as CoreInitializer

from .register_domain.models import (
    G2PRegisterCrop,
    G2PRegisterHistoryCrop,
    G2PIntakeFormCrop,
)
from .register_domain.factory import G2PRegisterDomainFactory
from .register_domain.services import G2PRegisterDomainServiceCrop

_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize()
        CoreInitializer().initialize()

        G2PRegisterDomainFactory()
        G2PRegisterDomainServiceCrop()

    def migrate_database(self, args):

        async def migrate():
            _logger.info("Migrating crop extension database")

            await G2PRegisterCrop.create_migrate()
            await G2PRegisterHistoryCrop.create_migrate()
            await G2PIntakeFormCrop.create_migrate()

        asyncio.run(migrate())
