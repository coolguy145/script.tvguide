script.tvguide
==============

import test
import xbmcaddon
from test import MyClass


try:
    mydisplay = MyClass()
    mydisplay.doModal()
    del mydisplay

except Exception:
    pass
