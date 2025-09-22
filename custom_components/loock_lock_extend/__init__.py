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
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# 支持的平台
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """通过YAML配置设置集成"""
    _LOGGER.info("设置Loock Lock Extend集成")
    
    # 存储集成数据
    hass.data.setdefault(DOMAIN, {})
    
    # 检查配置中是否有我们的域
    domain_config = config.get(DOMAIN)
    if domain_config is not None:
        # 有配置时使用传统方式
        _LOGGER.info("通过YAML配置加载传感器")
        hass.async_create_task(
            hass.helpers.discovery.async_load_platform(Platform.SENSOR, DOMAIN, {}, config)
        )
    else:
        # 没有配置时自动加载
        _LOGGER.info("自动加载Loock Lock Extend传感器")
        
        # 直接加载传感器平台
        from .sensor import async_setup_platform
        
        async def auto_setup():
            """自动设置传感器"""
            try:
                # 创建一个虚拟的async_add_entities函数
                entities = []
                
                async def collect_entities(new_entities):
                    entities.extend(new_entities)
                
                # 调用传感器设置函数
                await async_setup_platform(hass, {}, collect_entities, None)
                
                # 手动注册实体
                for entity in entities:
                    hass.async_create_task(entity.async_added_to_hass())
                    hass.states.async_set(
                        entity.entity_id,
                        entity.state,
                        attributes=entity.extra_state_attributes
                    )
                
                _LOGGER.info(f"已自动添加 {len(entities)} 个传感器实体")
            except Exception as e:
                _LOGGER.error(f"自动添加传感器失败: {e}")
        
        hass.async_create_task(auto_setup())
    
    return True


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