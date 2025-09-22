"""Example Load Platform integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import load_platform
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Your controller/hub specific code."""
    # Data that you want to share with your platforms
    # hass.data[DOMAIN] = {
    #     'temperature': 23
    # }

    load_platform(hass, 'sensor', DOMAIN, {}, config)

    return True