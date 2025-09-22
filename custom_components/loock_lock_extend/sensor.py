"""Loock Lock Extend 传感器平台"""
from __future__ import annotations

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LockState, state_mapper

_LOGGER = logging.getLogger(__name__)


class LoockDoorStateSensor(SensorEntity):
    """门锁状态传感器"""
    
    def __init__(self, hass):
        """初始化传感器"""
        self.hass = hass
        self._attr_name = "门锁状态"
        self._attr_unique_id = f"{DOMAIN}_door_state"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:door"
        
        # 设置可能的状态选项
        self._attr_options = [state.value for state in LockState]

    @property
    def native_value(self):
        """返回传感器的当前值"""
        state_code = self._get_door_state_code()
        if state_code is None:
            return "unknown"
        
        # 使用state_mapper获取状态
        state_str = state_mapper.get_state_str(state_code)
        return state_str if state_str else "unknown"

    @property
    def extra_state_attributes(self):
        """返回额外的状态属性"""
        state_code = self._get_door_state_code()
        if state_code is None:
            return {
                "raw_state": None,
                "friendly_state": "未知",
                "error": "无法获取门锁状态"
            }
        
        state = state_mapper.get_state(state_code)
        friendly_names = {
            LockState.LOCKED: "已锁定",
            LockState.UNLOCKED: "已解锁", 
            LockState.DOOR_OPEN: "门已开启",
            LockState.DOOR_AJAR: "门虚掩"
        }
        
        attributes = {
            "raw_state": state_code,
            "friendly_state": friendly_names.get(state, "未知状态"),
            "is_locked": state_mapper.is_locked(state_code),
            "is_unlocked": state_mapper.is_unlocked(state_code),
            "is_door_open": state_mapper.is_door_open(state_code),
            "is_door_ajar": state_mapper.is_door_ajar(state_code),
        }
        
        return attributes

    @property
    def available(self):
        """检查传感器是否可用"""
        return self._get_door_state_code() is not None

    def _get_door_state_code(self):
        """获取门锁状态码"""
        try:
            val = self.hass.states.get("button.loock_t2pv1_559c_info")
            if not val or not val.attributes:
                return None
            return val.attributes.get("door.door_state")
        except Exception:
            return None
