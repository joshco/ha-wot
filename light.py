"""Platform for light integration."""
from __future__ import annotations

import logging
import json
from . import wot_util
from .const import DOMAIN

from wotpy.wot.servient import Servient
from wotpy.wot.wot import WoT
import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (ATTR_BRIGHTNESS, PLATFORM_SCHEMA,
                                            LightEntity)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.string,
})


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config[CONF_HOST]
    username = config[CONF_USERNAME]
    password = config.get(CONF_PASSWORD)
    url = config[CONF_URL]

    # Setup connection with devices/cloud
    hub = [{ "url": url, "id": 'wot_led_{}'.format(wot_util.makeHash(url)) }]
    _LOGGER.info( json.dumps(hub, indent=2))

    # Add devices
    add_entities(AwesomeLight(light) for light in hub)


class AwesomeLight(LightEntity):
    """Representation of an Awesome Light."""

    def __init__(self, light) -> None:
        """Initialize an AwesomeLight."""
        self._name = "wot light"
        self._url = light["url"]
        self._state = None
        self._brightness = None
        self._unique_id = light["id"]

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state
    
    @property
    def unique_id(self) -> str:
        """Return the display name of this light."""
        return self._unique_id
        
    
    @property
    def id(self) -> str:
        """Return the display name of this light."""
        return self._unique_id
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        wot = WoT(servient=Servient())
        consumed_thing = await wot.consume_from_url(self._url)
            
        makeWotLight = await consumed_thing.invoke_action('toggle', {'state': True})
        _LOGGER.info(makeWotLight)
        if makeWotLight:
            state = makeWotLight["toggle"]["input"]["input"]["state"]
            if state:
                _LOGGER.info('Enjoy your drink! \n{}'.format(makeWotLight))
                self._state = True
            else:
                _LOGGER.info('Failed making your drink: {}'.format(makeWotLight))

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        
        wot = WoT(servient=Servient())
        consumed_thing = await wot.consume_from_url(self._url)
            
        makeWotLight = await consumed_thing.invoke_action('toggle', {'state': False})
        _LOGGER.info(makeWotLight)
        if makeWotLight:
            state = makeWotLight["toggle"]["input"]["input"]["state"]
            if state:
                _LOGGER.info('Enjoy your drink! \n{}'.format(makeWotLight))
                self._state=False
            else:
                _LOGGER.info('Failed making your drink: {}'.format(makeWotLight))

    async def async_update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        
        wot = WoT(servient=Servient())
        consumed_thing = await wot.consume_from_url(self._url)
        propertyState = await consumed_thing.read_property('state')
        _LOGGER.debug('state is: {}'.format(json.dumps(propertyState, indent=2)))
        if propertyState:
            state = propertyState["state"]
            self._state = state
        #self._light.update()
        #self._state = True
        #self._brightness = 0
