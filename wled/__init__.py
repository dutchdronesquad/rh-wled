"""Control WLED Matrix display"""
import asyncio
import time
import logging

from eventmanager import Evt
from led_event_manager import ColorVal
from RHUI import UIField, UIFieldType
from wled import WLED, WLEDConnectionError

logger = logging.getLogger(__name__)

wled_manager = None


def convert_rgb(color: int) -> tuple:
    """Convert RGB hexadecimal to RGB int values.

    Args:
    -----
        color: RGB hexadecimal value.

    Returns:
    --------
        r: Red value.
        g: Green value.
        b: Blue value.
    """
    r = 0xFF & (color >> 16)
    g = 0xFF & (color >> 8)
    b = 0xFF & color
    return r, g, b


class WLEDManager:
    """WLED Manager class."""

    def __init__(self, rhapi):
        """Initialize WLED Manager.

        Args:
        -----
            rhapi (RotorHazardAPI): RotorHazard API instance.
        """
        self._rhapi = rhapi
        self._rhapi.events.on(Evt.LED_INITIALIZE, register_handlers)
        self._rhapi.events.on(Evt.RACE_START, start_wled_matrix)
        self._rhapi.events.on(Evt.RACE_STOP, stop_wled_matrix)
        self._rhapi.events.on(Evt.RACE_STAGE, staging_wled_matrix)
        self._rhapi.events.on(Evt.RACE_LAP_RECORDED, lap_wled_matrix)

        self._rhapi.ui.register_panel("wled", "WLED", "settings")
        self._rhapi.fields.register_option(
            UIField(
                "device_ip",
                "Enter IP Address of WLED device",
                UIFieldType.TEXT,
                placeholder="i.e. 192.168.1.10",
            ),
            "wled",
        )
        self._rhapi.ui.register_quickbutton(
            "wled", "save_ip", "Save IP Address", self.save_ip, {"rhapi": rhapi}
        )
        logger.debug("WLED RotorHazard Plugin Initialized")

    def save_ip(self, args) -> None:
        """Save IP Address of WLED device.

        Args:
        -----
            args: Arguments passed to function.
        """
        device_ip = str(self._rhapi.db.option("device_ip", "wled"))
        device = None

        # Try to connect to WLED device
        try:
            device = asyncio.run(self.wled_info(device_ip))
        except WLEDConnectionError:
            args["rhapi"].ui.message_notify(
                f"Unable to connect to WLED device at {device_ip}"
            )

        # Show notification if device is connected
        if device:
            args["rhapi"].ui.message_notify(
                f"Connected to WLED device at {device_ip} with version: {device.info.version}"
            )

    async def set_matrix(
        self, color, trans: int = 7, effect: str = "solid", speed: int = 128
    ):
        """Send request to WLED device.

        Args:
        -----
            color: RGB color values.
            trans (int): Transition time.
            effect (str): WLED effect.
            speed (int): Effect speed.
        """
        async with WLED(self._rhapi.db.option("device_ip", "wled")) as client:
            await client.segment(
                on=True,
                segment_id=0,
                brightness=128,
                color_primary=color,
                transition=trans,
                effect=effect,
                speed=speed,
            )

    async def wled_connect(self, device_ip) -> WLED:
        """Connect to WLED device.

        Args:
        -----
            device_ip: IP Address of WLED device.
        """
        async with WLED(device_ip) as client:
            return await client.connect()

    async def wled_info(self, device_ip) -> WLED:
        """Get WLED device information.

        Args:
        -----
            device_ip: IP Address of WLED device.
        """
        async with WLED(device_ip) as client:
            return await client.update()


def initialize(rhapi):
    """Initialize plugin.

    Args:
    -----
        rhapi: RotorHazard API instance.
    """
    global wled_manager
    wled_manager = WLEDManager(rhapi)


def register_handlers(args):
    if "registerFn" in args:
        for led_effect in discover():
            args["registerFn"](led_effect)


def discover(*args, **kwargs):
    """Discover WLED effects."""
    return []


def start_wled_matrix(*args):
    """LED effect on start race."""
    asyncio.run(wled_manager.set_matrix(color=convert_rgb(ColorVal.GREEN), trans=1))
    time.sleep(3)
    asyncio.run(wled_manager.set_matrix(color=convert_rgb(ColorVal.NONE), trans=1))


def stop_wled_matrix(*args):
    """LED effect on stop race."""
    asyncio.run(wled_manager.set_matrix(color=convert_rgb(ColorVal.RED)))
    time.sleep(3)
    asyncio.run(wled_manager.set_matrix(color=convert_rgb(ColorVal.NONE), trans=1))


def staging_wled_matrix(*args):
    """Run staging LED effect."""
    asyncio.run(
        wled_manager.set_matrix(
            color=convert_rgb(ColorVal.BLUE), effect="fade", speed=255
        )
    )


def lap_wled_matrix(*args):
    """Run lap LED effect."""
    pilot_color = convert_rgb(args[0]["color"])
    asyncio.run(wled_manager.set_matrix(color=pilot_color, trans=1))
    time.sleep(1)
    asyncio.run(wled_manager.set_matrix(color=convert_rgb(ColorVal.NONE), trans=1))
