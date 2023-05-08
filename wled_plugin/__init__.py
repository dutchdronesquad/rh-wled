"""Control WLED Matrix display"""
import asyncio
import time

from eventmanager import Evt
from wled import WLED

from .const import HOST

def registerHandlers(args):
    if 'registerFn' in args:
        for effect in discover():
            args['registerFn'](effect)

def initialize(**kwargs):
    if 'Events' in kwargs:
        kwargs['Events'].on('actionsInitialize', 'action_led_matrix', registerHandlers, {}, 75, True)
        kwargs['Events'].on(Evt.RACE_START, 'Start_wled_matrix', start_wled_matrix, {}, 75, True)
        kwargs['Events'].on(Evt.RACE_STOP, 'Stop_wled_matrix', stop_wled_matrix, {}, 75, True)
        kwargs['Events'].on(Evt.RACE_STAGE, 'Staging_wled_matrix', staging_wled_matrix, {}, 75, True)
        kwargs['Events'].on(Evt.RACE_LAP_RECORDED, 'Lap_wled_matrix', lap_wled_matrix, {}, 75, True)

def start_wled_matrix(args):
    asyncio.run(setMatrix(color=[0, 255, 0], trans=1))

def stop_wled_matrix(args):
    asyncio.run(setMatrix(color=[255, 0, 0]))

def staging_wled_matrix(args):
    asyncio.run(setMatrix(color=[0, 0, 255], effect="fade"))

def lap_wled_matrix(args):
    asyncio.run(setMatrix(color=[255, 255, 0], trans=1))
    time.sleep(1)
    asyncio.run(setMatrix(color=[0, 0, 0], trans=1))

async def setMatrix(color, trans=7, effect="solid"):
    """Send request to WLED device."""
    async with WLED(HOST) as client:
        await client.segment(on=True, segment_id=0, brightness=128, color_primary=color, transition=trans, effect=effect)

def discover(*args, **kwargs):
    return [
        
    ]