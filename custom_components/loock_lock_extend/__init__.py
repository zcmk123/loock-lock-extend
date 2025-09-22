"""Top-level package for Loock Lock Extend."""

__author__ = """DoubleBird"""
__email__ = 'zcmk1234@gmail.com'

"""Loock Lock Extend - Home Assistant 集成主模块

这个模块提供了 Home Assistant 集成的核心功能，
包括平台设置和配置管理。
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# 支持的平台
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """设置集成入口点"""
    _LOGGER.info("设置Loock Lock Extend集成")
    
    # 存储集成数据
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}
    
    # 设置平台
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载集成入口点"""
    _LOGGER.info("卸载Loock Lock Extend集成")
    
    # 卸载平台
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """重新加载集成入口点"""
    _LOGGER.info("重新加载Loock Lock Extend集成")
    
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)