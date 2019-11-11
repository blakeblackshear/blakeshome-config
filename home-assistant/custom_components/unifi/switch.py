"""Support for devices connected to UniFi POE."""
import logging

from homeassistant.components.unifi.config_flow import get_controller_from_config_entry
from homeassistant.components.switch import SwitchDevice
from homeassistant.core import callback
from homeassistant.helpers import entity_registry
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.restore_state import RestoreEntity

LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Component doesn't support configuration through configuration.yaml."""


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up switches for UniFi component.

    Switches are controlling network switch ports with Poe.
    """
    controller = get_controller_from_config_entry(hass, config_entry)

    if controller.site_role != "admin":
        return

    switches = {}
    switches_off = []

    registry = await entity_registry.async_get_registry(hass)

    # Restore clients that is not a part of active clients list.
    for entity in registry.entities.values():

        if (
            entity.config_entry_id == config_entry.entry_id
            and entity.unique_id.startswith("poe-")
        ):

            _, mac = entity.unique_id.split("-", 1)

            if mac in controller.api.clients or mac not in controller.api.clients_all:
                continue

            client = controller.api.clients_all[mac]
            controller.api.clients.process_raw([client.raw])
            switches_off.append(entity.unique_id)

    @callback
    def update_controller():
        """Update the values of the controller."""
        update_items(controller, async_add_entities, switches, switches_off)

    controller.listeners.append(
        async_dispatcher_connect(hass, controller.signal_update, update_controller)
    )

    update_controller()
    switches_off.clear()


@callback
def update_items(controller, async_add_entities, switches, switches_off):
    """Update POE port state from the controller."""
    new_switches = []
    devices = controller.api.devices

    # block client
    for client_id in controller.option_block_clients:

        block_client_id = f"block-{client_id}"

        if block_client_id in switches:
            LOGGER.debug(
                "Updating UniFi block switch %s (%s)",
                switches[block_client_id].entity_id,
                switches[block_client_id].client.mac,
            )
            switches[block_client_id].async_schedule_update_ha_state()
            continue

        if client_id not in controller.api.clients_all:
            continue

        client = controller.api.clients_all[client_id]
        switches[block_client_id] = UniFiBlockClientSwitch(client, controller)
        new_switches.append(switches[block_client_id])
        LOGGER.debug("New UniFi Block switch %s (%s)", client.hostname, client.mac)

    # control POE
    for client_id in controller.api.clients:

        poe_client_id = f"poe-{client_id}"

        if poe_client_id in switches:
            LOGGER.debug(
                "Updating UniFi POE switch %s (%s)",
                switches[poe_client_id].entity_id,
                switches[poe_client_id].client.mac,
            )
            switches[poe_client_id].async_schedule_update_ha_state()
            continue

        client = controller.api.clients[client_id]

        if poe_client_id in switches_off:
            pass
        # Network device with active POE
        elif (
            client_id in controller.wireless_clients
            or client.sw_mac not in devices
            or not devices[client.sw_mac].ports[client.sw_port].port_poe
            or not devices[client.sw_mac].ports[client.sw_port].poe_enable
            or controller.mac == client.mac
        ):
            continue

        # Multiple POE-devices on same port means non UniFi POE driven switch
        multi_clients_on_port = False
        for client2 in controller.api.clients.values():

            if poe_client_id in switches_off:
                break

            if (
                client2.is_wired
                and client.mac != client2.mac
                and client.sw_mac == client2.sw_mac
                and client.sw_port == client2.sw_port
            ):
                multi_clients_on_port = True
                break

        if multi_clients_on_port:
            continue

        switches[poe_client_id] = UniFiPOEClientSwitch(client, controller)
        new_switches.append(switches[poe_client_id])
        LOGGER.debug("New UniFi POE switch %s (%s)", client.hostname, client.mac)

    if new_switches:
        async_add_entities(new_switches)


class UniFiClient:
    """Base class for UniFi switches."""

    def __init__(self, client, controller):
        """Set up switch."""
        self.client = client
        self.controller = controller

    async def async_update(self):
        """Synchronize state with controller."""
        await self.controller.request_update()

    @property
    def name(self):
        """Return the name of the client."""
        return self.client.name or self.client.hostname

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return {"connections": {(CONNECTION_NETWORK_MAC, self.client.mac)}}


class UniFiPOEClientSwitch(UniFiClient, SwitchDevice, RestoreEntity):
    """Representation of a client that uses POE."""

    def __init__(self, client, controller):
        """Set up POE switch."""
        super().__init__(client, controller)
        self.poe_mode = None
        if self.client.sw_port and self.port.poe_mode != "off":
            self.poe_mode = self.port.poe_mode

    async def async_added_to_hass(self):
        """Call when entity about to be added to Home Assistant."""
        state = await self.async_get_last_state()

        if state is None:
            return

        if self.poe_mode is None:
            self.poe_mode = state.attributes["poe_mode"]

        if not self.client.sw_mac:
            self.client.raw["sw_mac"] = state.attributes["switch"]

        if not self.client.sw_port:
            self.client.raw["sw_port"] = state.attributes["port"]

    @property
    def unique_id(self):
        """Return a unique identifier for this switch."""
        return f"poe-{self.client.mac}"

    @property
    def is_on(self):
        """Return true if POE is active."""
        return self.port.poe_mode != "off"

    @property
    def available(self):
        """Return if switch is available.

        Poe_mode None means its poe state is unknown.
        Sw_mac unavailable means restored client.
        """
        return (
            self.poe_mode is None
            or self.client.sw_mac
            and (
                self.controller.available
                and self.client.sw_mac in self.controller.api.devices
            )
        )

    async def async_turn_on(self, **kwargs):
        """Enable POE for client."""
        await self.device.async_set_port_poe_mode(self.client.sw_port, self.poe_mode)

    async def async_turn_off(self, **kwargs):
        """Disable POE for client."""
        await self.device.async_set_port_poe_mode(self.client.sw_port, "off")

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        attributes = {
            "power": self.port.poe_power,
            "switch": self.client.sw_mac,
            "port": self.client.sw_port,
            "poe_mode": self.poe_mode,
        }
        return attributes

    @property
    def device(self):
        """Shortcut to the switch that client is connected to."""
        return self.controller.api.devices[self.client.sw_mac]

    @property
    def port(self):
        """Shortcut to the switch port that client is connected to."""
        return self.device.ports[self.client.sw_port]


class UniFiBlockClientSwitch(UniFiClient, SwitchDevice):
    """Representation of a blockable client."""

    @property
    def unique_id(self):
        """Return a unique identifier for this switch."""
        return f"block-{self.client.mac}"

    @property
    def is_on(self):
        """Return true if client is allowed to connect."""
        return not self.client.blocked

    @property
    def available(self):
        """Return if controller is available."""
        return self.controller.available

    async def async_turn_on(self, **kwargs):
        """Turn on connectivity for client."""
        await self.controller.api.clients.async_unblock(self.client.mac)

    async def async_turn_off(self, **kwargs):
        """Turn off connectivity for client."""
        await self.controller.api.clients.async_block(self.client.mac)
