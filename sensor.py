"""Platform for sensor integration."""
from __future__ import annotations

from wotpy.wot.servient import Servient
from wotpy.wot.wot import WoT

import logging
import json
from . import wot_util
from .const import DOMAIN

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, CONF_URL

_LOGGER = logging.getLogger(__name__)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    
    url = config[CONF_URL]

    # Setup connection with devices/cloud
    hub = [{ "url": url, "id": 'wot_sensor_{}'.format(wot_util.makeHash(url)) }]
    _LOGGER.info( json.dumps(hub, indent=2))

    # Add devices
    add_entities(ExampleSensor(light) for light in hub)



class ExampleSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, sensor) -> None:
        self._name = "WOT Sensor"
        self._url = sensor["url"]
        self._native_value = None
        self._unique_id = 'wot_sensor'
  
    @property
    def name(self) -> str:
        """Return the display name of this sensor."""
        return self._name
    
    @property
    def unique_id(self) -> str:
        """Return the display name of this sensor."""
        return self._unique_id
    
    @property
    def id(self) -> str:
        """Return the display name of this light."""
        return self._unique_id
    
    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        
        wot = WoT(servient=Servient())
        consumed_thing = await wot.consume_from_url(self._url)
        propertyState = await consumed_thing.read_property('temperature')
        _LOGGER.debug('state is: {}'.format(json.dumps(propertyState, indent=2)))
        if propertyState:
            state = propertyState["temperature"]
            self._attr_native_value = state
