"""Config flow for UniFi."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_USERNAME,
    CONF_VERIFY_SSL,
)

from .const import (
    CONF_ALLOW_BANDWIDTH_SENSORS,
    CONF_CONTROLLER,
    CONF_DETECTION_TIME,
    CONF_SITE_ID,
    CONF_TRACK_CLIENTS,
    CONF_TRACK_DEVICES,
    CONF_TRACK_WIRED_CLIENTS,
    CONTROLLER_ID,
    DEFAULT_ALLOW_BANDWIDTH_SENSORS,
    DEFAULT_TRACK_CLIENTS,
    DEFAULT_TRACK_DEVICES,
    DEFAULT_TRACK_WIRED_CLIENTS,
    DEFAULT_DETECTION_TIME,
    DOMAIN,
    LOGGER,
)
from .controller import get_controller
from .errors import AlreadyConfigured, AuthenticationRequired, CannotConnect

DEFAULT_PORT = 8443
DEFAULT_SITE_ID = "default"
DEFAULT_VERIFY_SSL = False


@callback
def get_controller_id_from_config_entry(config_entry):
    """Return controller with a matching bridge id."""
    return CONTROLLER_ID.format(
        host=config_entry.data[CONF_CONTROLLER][CONF_HOST],
        site=config_entry.data[CONF_CONTROLLER][CONF_SITE_ID],
    )


@callback
def get_controller_from_config_entry(hass, config_entry):
    """Return controller with a matching bridge id."""
    return hass.data[DOMAIN][get_controller_id_from_config_entry(config_entry)]


class UnifiFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a UniFi config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return UnifiOptionsFlowHandler(config_entry)

    def __init__(self):
        """Initialize the UniFi flow."""
        self.config = None
        self.desc = None
        self.sites = None

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:

            try:
                self.config = {
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_USERNAME: user_input[CONF_USERNAME],
                    CONF_PASSWORD: user_input[CONF_PASSWORD],
                    CONF_PORT: user_input.get(CONF_PORT),
                    CONF_VERIFY_SSL: user_input.get(CONF_VERIFY_SSL),
                    CONF_SITE_ID: DEFAULT_SITE_ID,
                }

                controller = await get_controller(self.hass, **self.config)

                self.sites = await controller.sites()

                return await self.async_step_site()

            except AuthenticationRequired:
                errors["base"] = "faulty_credentials"

            except CannotConnect:
                errors["base"] = "service_unavailable"

            except Exception:  # pylint: disable=broad-except
                LOGGER.error(
                    "Unknown error connecting with UniFi Controller at %s",
                    user_input[CONF_HOST],
                )
                return self.async_abort(reason="unknown")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                    vol.Optional(CONF_VERIFY_SSL, default=DEFAULT_VERIFY_SSL): bool,
                }
            ),
            errors=errors,
        )

    async def async_step_site(self, user_input=None):
        """Select site to control."""
        errors = {}

        if user_input is not None:
            try:
                desc = user_input.get(CONF_SITE_ID, self.desc)

                for site in self.sites.values():
                    if desc == site["desc"]:
                        self.config[CONF_SITE_ID] = site["name"]
                        break

                for entry in self._async_current_entries():
                    controller = entry.data[CONF_CONTROLLER]
                    if (
                        controller[CONF_HOST] == self.config[CONF_HOST]
                        and controller[CONF_SITE_ID] == self.config[CONF_SITE_ID]
                    ):
                        raise AlreadyConfigured

                data = {CONF_CONTROLLER: self.config}

                return self.async_create_entry(title=desc, data=data)

            except AlreadyConfigured:
                return self.async_abort(reason="already_configured")

        if len(self.sites) == 1:
            self.desc = next(iter(self.sites.values()))["desc"]
            return await self.async_step_site(user_input={})

        sites = []
        for site in self.sites.values():
            sites.append(site["desc"])

        return self.async_show_form(
            step_id="site",
            data_schema=vol.Schema({vol.Required(CONF_SITE_ID): vol.In(sites)}),
            errors=errors,
        )


class UnifiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Unifi options."""

    def __init__(self, config_entry):
        """Initialize UniFi options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Manage the UniFi options."""
        return await self.async_step_device_tracker()

    async def async_step_device_tracker(self, user_input=None):
        """Manage the device tracker options."""
        if user_input is not None:
            self.options.update(user_input)
            return await self.async_step_statistics_sensors()

        return self.async_show_form(
            step_id="device_tracker",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_TRACK_CLIENTS,
                        default=self.config_entry.options.get(
                            CONF_TRACK_CLIENTS, DEFAULT_TRACK_CLIENTS
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_TRACK_WIRED_CLIENTS,
                        default=self.config_entry.options.get(
                            CONF_TRACK_WIRED_CLIENTS, DEFAULT_TRACK_WIRED_CLIENTS
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_TRACK_DEVICES,
                        default=self.config_entry.options.get(
                            CONF_TRACK_DEVICES, DEFAULT_TRACK_DEVICES
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_DETECTION_TIME,
                        default=self.config_entry.options.get(
                            CONF_DETECTION_TIME, DEFAULT_DETECTION_TIME
                        ),
                    ): int,
                }
            ),
        )

    async def async_step_statistics_sensors(self, user_input=None):
        """Manage the statistics sensors options."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="statistics_sensors",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_ALLOW_BANDWIDTH_SENSORS,
                        default=self.config_entry.options.get(
                            CONF_ALLOW_BANDWIDTH_SENSORS,
                            DEFAULT_ALLOW_BANDWIDTH_SENSORS,
                        ),
                    ): bool
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(title="", data=self.options)
