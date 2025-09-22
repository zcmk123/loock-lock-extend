"""Config flow for Loock Lock Extend integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class LoockLockExtendConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Loock Lock Extend."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({}),
                description_placeholders={},
            )

        # 检查是否已经配置过
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title="Loock门锁扩展",
            data={},
        )

    async def async_step_import(self, import_info: dict[str, Any]) -> FlowResult:
        """Handle import from YAML."""
        return await self.async_step_user(import_info)