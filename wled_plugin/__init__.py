"""Control WLED Matrix display"""
import asyncio
import time
import logging

from eventmanager import Evt
from led_event_manager import ColorVal
from RHUI import UIField, UIFieldType
from wled import WLED

logger = logging.getLogger(__name__)

wled_manager = None


# Convert RGB hexadecimal to RGB int values
def convert_rgb(color):
    r = 0xFF & (color >> 16)
    g = 0xFF & (color >> 8)
    b = 0xFF & color
    return r, g, b


class WLEDManager:
    """WLED Manager class."""

    def __init__(self, rhapi):
        """Initialize WLED Manager.

        Args:
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

    def save_ip(self, args):
        """Save IP Address of WLED device."""
        device_ip = str(self._rhapi.db.option("device_ip", "wled"))
        args["rhapi"].ui.message_notify(f"WLED IP Address Saved: {device_ip}")

    async def setMatrix(self, color, trans=7, effect="solid"):
        """Send request to WLED device.

        Args:
        -----
            color: RGB color values.
            trans: Transition time.
            effect: WLED effect.
        """
        async with WLED(self._rhapi.db.option("device_ip", "wled")) as client:
            await client.segment(
                on=True,
                segment_id=0,
                brightness=128,
                color_primary=color,
                transition=trans,
                effect=effect,
            )


def initialize(rhapi):
    """Initialize plugin."""
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
    asyncio.run(wled_manager.setMatrix(color=convert_rgb(ColorVal.GREEN), trans=1))


def stop_wled_matrix(*args):
    """LED effect on stop race."""
    asyncio.run(wled_manager.setMatrix(color=convert_rgb(ColorVal.RED)))


def staging_wled_matrix(*args):
    """Run staging LED effect."""
    asyncio.run(wled_manager.setMatrix(color=convert_rgb(ColorVal.BLUE), effect="fade"))


def lap_wled_matrix(*args):
    asyncio.run(wled_manager.setMatrix(color=[255, 255, 0], trans=1))
    time.sleep(1)
    asyncio.run(wled_manager.setMatrix(color=convert_rgb(ColorVal.NONE), trans=1))
