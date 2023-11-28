"""Control WLED Matrix display"""
import asyncio
import time
import logging

from eventmanager import Evt
from led_event_manager import LEDEvent, LEDEffect
from RHUI import UIField, UIFieldType
from wled import WLED

logger = logging.getLogger(__name__)


class WLEDManager:
    """WLED Manager class."""

    def __init__(self, rhapi):
        """Initialize WLED Manager.

        Args:
            rhapi (RotorHazardAPI): RotorHazard API instance.
        """
        self._rhapi = rhapi
        self._rhapi.events.on(Evt.LED_INITIALIZE, register_handlers)

        self._rhapi.ui.register_panel("wled", "WLED", "settings")
        self._rhapi.fields.register_option(UIField('device_ip', "Enter IP Address of WLED device", UIFieldType.TEXT, placeholder="i.e. 192.168.1.10"), "wled")
        self._rhapi.ui.register_quickbutton("wled", "save_ip", "Save IP Address", self.save_ip, {'rhapi': rhapi})
        logger.debug("WLED RotorHazard Plugin Initialized")

    def save_ip(self, args):
        """Save IP Address of WLED device."""
        device_ip = str(self._rhapi.db.option("device_ip", "wled"))
        args["rhapi"].ui.message_notify(f"WLED IP Address Saved: {device_ip}")

def initialize(rhapi):
    """Initialize plugin."""
    WLEDManager(rhapi)

def register_handlers(args):
    if 'registerFn' in args:
        for led_effect in discover():
            args['registerFn'](led_effect)

def discover(*args, **kwargs):
    """Discover WLED effects."""
    return [
        LEDEffect("Turn Off[WLED]", wled_clear(), {
            "manual": False,
            "include": [Evt.SHUTDOWN, LEDEvent.IDLE_DONE, LEDEvent.IDLE_READY, LEDEvent.IDLE_RACING],
            'recommended': [Evt.ALL]
        })
    ]


# def initialize(**kwargs):
#     if 'Events' in kwargs:
#         kwargs['Events'].on('actionsInitialize', 'action_led_matrix', registerHandlers, {}, 75, True)
#         kwargs['Events'].on(Evt.RACE_START, 'Start_wled_matrix', start_wled_matrix, {}, 75, True)
#         kwargs['Events'].on(Evt.RACE_STOP, 'Stop_wled_matrix', stop_wled_matrix, {}, 75, True)
#         kwargs['Events'].on(Evt.RACE_STAGE, 'Staging_wled_matrix', staging_wled_matrix, {}, 75, True)
#         kwargs['Events'].on(Evt.RACE_LAP_RECORDED, 'Lap_wled_matrix', lap_wled_matrix, {}, 75, True)

# def start_wled_matrix(args):
#     asyncio.run(setMatrix(color=[0, 255, 0], trans=1))

# def stop_wled_matrix(args):
#     asyncio.run(setMatrix(color=[255, 0, 0]))

# def staging_wled_matrix(args):
#     asyncio.run(setMatrix(color=[0, 0, 255], effect="fade"))

# def lap_wled_matrix(args):
#     asyncio.run(setMatrix(color=[255, 255, 0], trans=1))
#     time.sleep(1)
#     asyncio.run(setMatrix(color=[0, 0, 0], trans=1))

# async def setMatrix(color, trans=7, effect="solid"):
#     """Send request to WLED device."""
#     async with WLED(
#         await client.segment(on=True, segment_id=0, brightness=128, color_primary=color, transition=trans, effect=effect)