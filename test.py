script.tvguide
==============

import xbmc
import xbmcgui
import xbmcaddon
import os
import threading
import datetime
import time
import urllib2
import StringIO
import sqlite3
import threading
from sqlite3 import dbapi2 as database
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from UserDict import DictMixin

__killthread__ = False


#get actioncodes from keyboard.xml
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_UP = 3
ACTION_MOVE_DOWN = 4
ACTION_ENTER = 7
ACTION_PREVIOUS_MENU = 10
ACTION_BACKSPACE = 110
ACTION_NUMBER1 = 59
ACTION_NUMBER2 = 60
ACTION_NUMBER3 = 61
ACTION_NUMBER4 = 62
ACTION_NUMBER5 = 63
ACTION_NUMBER6 = 64
ACTION_NUMBER7 = 65
ACTION_NUMBER8 = 66
ACTION_NUMBER9 = 67
ACTION_NUMBER0 = 58


def cSetVisible(WiNdOw,iD,V=True): WiNdOw.getControl(iD).setVisible(V)
ADDON = xbmcaddon.Addon(id = 'script.tvguide')


class Channel:
     def __init__(self):
         self.__display_name = None
         self.__icon = None
         self.__programs = []


     def get_display_name(self):
         return self.__display_name


     def get_icon(self):
         return self.__icon


     def get_programs(self):
         return self.__programs



     def set_display_name(self, value):
         self.__display_name = value


     def set_icon(self, value):
         self.__icon = value


     def set_programs(self, value):
         self.__programs = value


     def del_display_name(self):
         del self.__display_name


     def del_icon(self):
         del self.__icon


     def del_programs(self):
         del self.__programs

     display_name = property(get_display_name, set_display_name, del_display_name, "display_name's docstring")
     icon = property(get_icon, set_icon, del_icon, "icon's docstring")
     programs = property(get_programs, set_programs, del_programs, "programs's docstring")




class Programme:
     def __init__(self):
         self.__start = None
         self.__stop = None
         self.__title = None
         self.__sub_title = None
         self.__desc = None
         self.__category = []
         self.__credits = []
         self.__icon = None
         self.__episode_num = None

     def get_episode_num(self):
         return self.__episode_num


     def set_episode_num(self, value):
         self.__episode_num = value


     def del_episode_num(self):
         del self.__episode_num


     def get_start(self):
         return self.__start


     def get_stop(self):
         return self.__stop


     def get_title(self):
         return self.__title


     def get_sub_title(self):
         return self.__sub_title


     def get_desc(self):
         return self.__desc


     def get_category(self):
         return self.__category


     def get_credits(self):
         return self.__credits


     def get_icon(self):
         return self.__icon


     def set_start(self, value):
         self.__start = value


     def set_stop(self, value):
         self.__stop = value


     def set_title(self, value):
         self.__title = value


     def set_sub_title(self, value):
         self.__sub_title = value


     def set_desc(self, value):
         self.__desc = value


     def set_category(self, value):
         self.__category = value


     def set_credits(self, value):
         self.__credits = value


     def set_icon(self, value):
         self.__icon = value


     def del_start(self):
         del self.__start


     def del_stop(self):
         del self.__stop


     def del_title(self):
         del self.__title


     def del_sub_title(self):
         del self.__sub_title


     def del_desc(self):
         del self.__desc


     def del_category(self):
         del self.__category


     def del_credits(self):
         del self.__credits


     def del_icon(self):
         del self.__icon

     start = property(get_start, set_start, del_start, "start's docstring")
     stop = property(get_stop, set_stop, del_stop, "stop's docstring")
     title = property(get_title, set_title, del_title, "title's docstring")
     sub_title = property(get_sub_title, set_sub_title, del_sub_title, "sub_title's docstring")
     desc = property(get_desc, set_desc, del_desc, "desc's docstring")
     category = property(get_category, set_category, del_category, "category's docstring")
     creditss = property(get_credits, set_credits, del_credits, "credits's docstring")
     icon = property(get_icon, set_icon, del_icon, "icon's docstring")
     episode_num = property(get_episode_num, set_episode_num, del_episode_num, "episode_num's docstring")




class Credits:
     def __init__(self):
         self.__type = None
         self.__role = None
         self.__name = None

     def get_type(self):
         return self.__type


     def get_role(self):
         return self.__role


     def get_name(self):
         return self.__name


     def set_type(self, value):
         self.__type = value


     def set_role(self, value):
         self.__role = value


     def set_name(self, value):
         self.__name = value


     def del_type(self):
         del self.__type


     def del_role(self):
         del self.__role


     def del_name(self):
         del self.__name

     type = property(get_type, set_type, del_type, "type's docstring")
     role = property(get_role, set_role, del_role, "role's docstring")
     name = property(get_name, set_name, del_name, "name's docstring")




class OrderedDict(dict, DictMixin):

    def __init__(self, *args, **kwds):
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__end
        except AttributeError:
            self.clear()
        self.update(*args, **kwds)

    def clear(self):
        self.__end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.__map = {}                 # key --> [key, prev, next]
        dict.clear(self)

    def __setitem__(self, key, value):
        if key not in self:
            end = self.__end
            curr = end[1]
            curr[2] = end[1] = self.__map[key] = [key, curr, end]
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        key, prev, next = self.__map.pop(key)
        prev[2] = next
        next[1] = prev

    def __iter__(self):
        end = self.__end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.__end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def popitem(self, last=True):
        if not self:
            raise KeyError('dictionary is empty')
        if last:
            key = reversed(self).next()
        else:
            key = iter(self).next()
        value = self.pop(key)
        return key, value

    def __reduce__(self):
        items = [[k, self[k]] for k in self]
        tmp = self.__map, self.__end
        del self.__map, self.__end
        inst_dict = vars(self).copy()
        self.__map, self.__end = tmp
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)

    def keys(self):
        return list(self)

    setdefault = DictMixin.setdefault
    update = DictMixin.update
    pop = DictMixin.pop
    values = DictMixin.values
    items = DictMixin.items
    iterkeys = DictMixin.iterkeys
    itervalues = DictMixin.itervalues
    iteritems = DictMixin.iteritems

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, self.items())

    def copy(self):
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d

    def __eq__(self, other):
        if isinstance(other, OrderedDict):
            if len(self) != len(other):
                return False
            for p, q in  zip(self.items(), other.items()):
                if p != q:
                    return False
            return True
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self == other




class MyClass(xbmcgui.WindowXML):

     def __new__(cls):
         return super(MyClass, cls).__new__(cls, 'script-tvguide-mainmenu.xml', ADDON.getAddonInfo('path'))



     def onInit(self):
         self.getControl(3).setAnimations([('fade', 'effect=fade start=0 end=100 time=1500')])
         self.getControl(5).setAnimations([('fade', 'effect=fade start=0 end=100 time=1500')])
         self.getControl(7).setAnimations([('fade', 'effect=fade start=0 end=100 time=1500')])
         self.getControl(9).setAnimations([('fade', 'effect=fade start=0 end=100 time=1500')])
         self.getControl(4).setVisible(False)
         self.getControl(6).setVisible(False)
         self.getControl(8).setVisible(False)
         self.getControl(10).setVisible(False)
         cSetVisible(self,110,False)
         changelanguage_yellow_BOX = self.getControl(110)
         changelanguage_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/changelang_yellow.png")
         cSetVisible(self,111,False)
         changelanguage_blue_BOX = self.getControl(111)
         changelanguage_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/changelang_blue.png")
         self.getControl(142).setVisible(False)
         savesettings_yellow_BOX = self.getControl(142)
         savesettings_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/savesettings_yellow.png")
         self.getControl(143).setVisible(False)
         savesettings_blue_BOX = self.getControl(143)
         savesettings_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/savesettings_blue.png")
         cSetVisible(self,146,False)
         self.getControl(116).setVisible(False)
         language_yellow_BOX = self.getControl(116)
         language_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/lang_yellow.png")
         self.getControl(117).setVisible(False)
         language_blue_BOX = self.getControl(117)
         language_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/lang_blue.png")
         self.getControl(114).setVisible(False)
         leftarrowlang_control = self.getControl(114)
         leftarrowlang_control.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/left-arrow.png")
         self.getControl(115).setVisible(False)
         rightarrowlang_control = self.getControl(115)
         rightarrowlang_control.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/right-arrow.png")
         cSetVisible(self,11,True)
         allchannels_yellow_BOX = self.getControl(11)
         allchannels_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_yellow.png")
         cSetVisible(self,10,False)
         allchannels_blue_BOX = self.getControl(10)
         allchannels_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_blue.png")
         cSetVisible(self,12,False)
         entertainment_yellow_BOX = self.getControl(12)
         entertainment_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_yellow.png")
         cSetVisible(self,13,True)
         entertainment_blue_BOX = self.getControl(13)
         entertainment_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_blue.png")
         cSetVisible(self,14,False)
         movies_yellow_BOX = self.getControl(14)
         movies_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_yellow.png")
         cSetVisible(self,15,True)
         movies_blue_BOX = self.getControl(15)
         movies_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_blue.png")
         cSetVisible(self,16,False)
         kids_yellow_BOX = self.getControl(16)
         kids_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_yellow.png")
         cSetVisible(self,17,True)
         kids_blue_BOX = self.getControl(17)
         kids_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_blue.png")
         cSetVisible(self,18,False)
         sports_yellow_BOX = self.getControl(18)
         sports_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_yellow.png")
         cSetVisible(self,19,True)
         sports_blue_BOX = self.getControl(19)
         sports_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_blue.png")
         cSetVisible(self,20,False)
         news_yellow_BOX = self.getControl(20)
         news_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_yellow.png")
         cSetVisible(self,21,True)
         news_blue_BOX = self.getControl(21)
         news_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_blue.png")
         cSetVisible(self,22,False)
         documentaries_yellow_BOX = self.getControl(22)
         documentaries_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_yellow.png")
         cSetVisible(self,23,True)
         documentaries_blue_BOX = self.getControl(23)
         documentaries_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_blue.png")
         cSetVisible(self,24,False)
         musicradio_yellow_BOX = self.getControl(24)
         musicradio_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_yellow.png")
         cSetVisible(self,25,True)
         musicradio_blue_BOX = self.getControl(25)
         musicradio_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_blue.png")
         cSetVisible(self,26,False)
         adult_yellow_BOX = self.getControl(26)
         adult_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_yellow.png")
         cSetVisible(self,27,True)
         adult_blue_BOX = self.getControl(27)
         adult_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_blue.png")
         cSetVisible(self,28,False)
         favourites_yellow_BOX = self.getControl(28)
         favourites_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_yellow.png")
         cSetVisible(self,29,True)
         favourites_blue_BOX = self.getControl(29)
         favourites_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/channels_blue.png")
         cSetVisible(self,30,False)
         picture_yellow_BOX = self.getControl(30)
         picture_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_yellow.png")
         cSetVisible(self,31,False)
         picture_blue_BOX = self.getControl(31)
         picture_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_blue.png")
         cSetVisible(self,32,False)
         sound_yellow_BOX = self.getControl(32)
         sound_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_yellow.png")
         cSetVisible(self,33,False)
         sound_blue_BOX = self.getControl(33)
         sound_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_blue.png")
         cSetVisible(self,34,False)
         changelanguage_yellow_BOX = self.getControl(34)
         changelanguage_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_yellow.png")
         cSetVisible(self,35,False)
         changelanguage_blue_BOX = self.getControl(35)
         changelanguage_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_blue.png")
         cSetVisible(self,36,False)
         changepin_yellow_BOX = self.getControl(36)
         changepin_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_yellow.png")
         cSetVisible(self,37,False)
         changepin_blue_BOX = self.getControl(37)
         changepin_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_blue.png")
         cSetVisible(self,38,False)
         viewrestrictions_yellow_BOX = self.getControl(38)
         viewrestrictions_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_yellow.png")
         cSetVisible(self,39,False)
         viewrestrictions_blue_BOX = self.getControl(39)
         viewrestrictions_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_blue.png")
         cSetVisible(self,40,False)
         removechannels_yellow_BOX = self.getControl(40)
         removechannels_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_yellow.png")
         cSetVisible(self,41,False)
         removechannels_blue_BOX = self.getControl(41)
         removechannels_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_blue.png")
         cSetVisible(self,42,False)
         systemdetails_yellow_BOX = self.getControl(42)
         systemdetails_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_yellow.png")
         cSetVisible(self,43,False)
         systemdetails_blue_BOX = self.getControl(43)
         systemdetails_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_blue.png")
         cSetVisible(self,44,False)
         speedtest_yellow_BOX = self.getControl(44)
         speedtest_yellow_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_yellow.png")
         cSetVisible(self,45,False)
         speedtest_blue_BOX = self.getControl(45)
         speedtest_blue_BOX.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/allsettings_blue.png")
         cSetVisible(self,4000,False)
         enterpin_yellow = self.getControl(4000)
         enterpin_yellow.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/enterpin_yellow.png")
         cSetVisible(self,4001,False)
         enterpin_blue = self.getControl(4001)
         enterpin_blue.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/enterpin_blue1.png")
         cSetVisible(self,4002,False)
         enterpin_bottom_blue = self.getControl(4002)
         enterpin_bottom_blue.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/enterpin_blue1.png")
         cSetVisible(self,4006,False)
         pin_press_back = self.getControl(4006)
         pin_press_back.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/pressback3.png")
         cSetVisible(self,4009,False)
         enterpin_blank_1 = self.getControl(4009)
         enterpin_blank_1.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/pin_numb1.png")
         cSetVisible(self,4010,False)
         enterpin_blank_2 = self.getControl(4010)
         enterpin_blank_2.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/pin_numb2.png")
         cSetVisible(self,4011,False)
         enterpin_blank_3 = self.getControl(4011)
         enterpin_blank_3.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/pin_numb3.png")
         cSetVisible(self,4012,False)
         enterpin_blank_4 = self.getControl(4012)
         enterpin_blank_4.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/pin_numb4.png")
         cSetVisible(self,4013,False)
         enterpin_chars_1 = self.getControl(4013)
         enterpin_chars_1.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/pin_1.png")
         cSetVisible(self,4014,False)
         enterpin_chars_2 = self.getControl(4014)
         enterpin_chars_2.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/pin_2.png")
         cSetVisible(self,4015,False)
         enterpin_chars_3 = self.getControl(4015)
         enterpin_chars_3.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/pin_3.png")
         cSetVisible(self,4016,False)
         enterpin_chars_4 = self.getControl(4016)
         enterpin_chars_4.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/pin_4.png")
         cSetVisible(self,4200,False)
         loading_gif = self.getControl(4200)
         loading_gif.setImage("special://home/addons/script.tvguide/resources/skins/Default/media/tvguide-loading.gif")
         ADDON = xbmcaddon.Addon(id = 'script.tvguide')
         english_enabled = ADDON.getSetting('english.enabled') == 'true'
         french_enabled = ADDON.getSetting('french.enabled') == 'true'
         self.getString = ADDON.getLocalizedString
         self.getControl(46).setVisible(False)
         self.getControl(46).setLabel(self.getString(30001))
         self.getControl(47).setVisible(False)
         self.getControl(47).setLabel(self.getString(30001))
         self.getControl(48).setVisible(False)
         self.getControl(48).setLabel(self.getString(30002))
         self.getControl(49).setVisible(False)
         self.getControl(49).setLabel(self.getString(30002))
         self.getControl(50).setVisible(False)
         self.getControl(50).setLabel(self.getString(30003))
         self.getControl(51).setVisible(False)
         self.getControl(51).setLabel(self.getString(30003))
         self.getControl(52).setVisible(False)
         self.getControl(52).setLabel(self.getString(30004))
         self.getControl(53).setVisible(False)
         self.getControl(53).setLabel(self.getString(30004))
         self.getControl(54).setVisible(False)
         self.getControl(54).setLabel(self.getString(30005))
         self.getControl(55).setVisible(False)
         self.getControl(55).setLabel(self.getString(30005))
         self.getControl(56).setVisible(False)
         self.getControl(56).setLabel(self.getString(30006))
         self.getControl(57).setVisible(False)
         self.getControl(57).setLabel(self.getString(30006))
         self.getControl(58).setVisible(False)
         self.getControl(58).setLabel(self.getString(30007))
         self.getControl(59).setVisible(False)
         self.getControl(59).setLabel(self.getString(30007))
         self.getControl(60).setVisible(False)
         self.getControl(60).setLabel(self.getString(30008))
         self.getControl(61).setVisible(False)
         self.getControl(61).setLabel(self.getString(30008))
         self.getControl(62).setVisible(False)
         self.getControl(62).setLabel(self.getString(30009))
         self.getControl(63).setVisible(False)
         self.getControl(63).setLabel(self.getString(30009))
         self.getControl(64).setVisible(False)
         self.getControl(64).setLabel(self.getString(30010))
         self.getControl(65).setVisible(False)
         self.getControl(65).setLabel(self.getString(30010))
         self.getControl(66).setVisible(False)
         self.getControl(66).setLabel(self.getString(30011))
         self.getControl(67).setVisible(False)
         self.getControl(67).setLabel(self.getString(30011))
         self.getControl(68).setVisible(False)
         self.getControl(68).setLabel(self.getString(30012))
         self.getControl(69).setVisible(False)
         self.getControl(69).setLabel(self.getString(30012))
         self.getControl(70).setVisible(False)
         self.getControl(70).setLabel(self.getString(30013))
         self.getControl(71).setVisible(False)
         self.getControl(71).setLabel(self.getString(30013))
         self.getControl(72).setVisible(False)
         self.getControl(72).setLabel(self.getString(30014))
         self.getControl(73).setVisible(False)
         self.getControl(73).setLabel(self.getString(30014))
         self.getControl(74).setVisible(False)
         self.getControl(74).setLabel(self.getString(30015))
         self.getControl(75).setVisible(False)
         self.getControl(75).setLabel(self.getString(30015))
         self.getControl(76).setVisible(False)
         self.getControl(76).setLabel(self.getString(30016))
         self.getControl(77).setVisible(False)
         self.getControl(77).setLabel(self.getString(30016))
         self.getControl(78).setVisible(False)
         self.getControl(78).setLabel(self.getString(30017))
         self.getControl(79).setVisible(False)
         self.getControl(79).setLabel(self.getString(30017))
         self.getControl(80).setVisible(False)
         self.getControl(80).setLabel(self.getString(30018))
         self.getControl(81).setVisible(False)
         self.getControl(81).setLabel(self.getString(30018))
         self.getControl(82).setVisible(False)
         self.getControl(82).setLabel(self.getString(30019))
         self.getControl(83).setVisible(False)
         self.getControl(83).setLabel(self.getString(30019))
         self.getControl(84).setVisible(False)
         self.getControl(84).setLabel(self.getString(30020))
         self.getControl(85).setVisible(False)
         self.getControl(85).setLabel(self.getString(30020))
         self.getControl(86).setVisible(False)
         self.getControl(86).setLabel(self.getString(30021))
         self.getControl(87).setVisible(False)
         self.getControl(87).setLabel(self.getString(30021))
         self.getControl(88).setVisible(False)
         self.getControl(88).setLabel(self.getString(30022))
         self.getControl(89).setVisible(False)
         self.getControl(89).setLabel(self.getString(30022))
         self.getControl(90).setVisible(False)
         self.getControl(90).setLabel(self.getString(30023))
         self.getControl(91).setVisible(False)
         self.getControl(91).setLabel(self.getString(30024))
         self.getControl(92).setVisible(False)
         self.getControl(92).setLabel(self.getString(30025))
         self.getControl(93).setVisible(False)
         self.getControl(93).setLabel(self.getString(30026))
         self.getControl(94).setVisible(False)
         self.getControl(94).setLabel(self.getString(30027))
         self.getControl(95).setVisible(False)
         self.getControl(95).setLabel(self.getString(30028))
         self.getControl(96).setVisible(False)
         self.getControl(96).setLabel(self.getString(30029))
         self.getControl(97).setVisible(False)
         self.getControl(97).setLabel(self.getString(30030))
         self.getControl(98).setVisible(False)
         self.getControl(98).setLabel(self.getString(30031))
         self.getControl(99).setVisible(False)
         self.getControl(99).setLabel(self.getString(30032))
         self.getControl(100).setVisible(False)
         self.getControl(100).setLabel(self.getString(30035))
         self.getControl(101).setVisible(False)
         self.getControl(101).setLabel(self.getString(30035))
         self.getControl(101).setVisible(False)
         self.getControl(101).setLabel(self.getString(30035))
         self.getControl(109).setVisible(False)
         self.getControl(109).setLabel(self.getString(30045))
         self.getControl(112).setVisible(False)
         self.getControl(112).setLabel(self.getString(30046))
         self.getControl(113).setVisible(False)
         self.getControl(113).setLabel(self.getString(30046))
         self.getControl(118).setVisible(False)
         self.getControl(118).setLabel(self.getString(30047))
         self.getControl(119).setVisible(False)
         self.getControl(119).setLabel(self.getString(30047))
         self.getControl(120).setVisible(False)
         self.getControl(120).setLabel(self.getString(30048))
         self.getControl(121).setVisible(False)
         self.getControl(121).setLabel(self.getString(30048))
         self.getControl(122).setVisible(False)
         self.getControl(122).setLabel(self.getString(30049))
         self.getControl(123).setVisible(False)
         self.getControl(123).setLabel(self.getString(30049))
         self.getControl(124).setVisible(False)
         self.getControl(124).setLabel(self.getString(30050))
         self.getControl(125).setVisible(False)
         self.getControl(125).setLabel(self.getString(30050))
         self.getControl(126).setVisible(False)
         self.getControl(126).setLabel(self.getString(30051))
         self.getControl(127).setVisible(False)
         self.getControl(127).setLabel(self.getString(30051))
         self.getControl(128).setVisible(False)
         self.getControl(128).setLabel(self.getString(30052))
         self.getControl(129).setVisible(False)
         self.getControl(129).setLabel(self.getString(30052))
         self.getControl(130).setVisible(False)
         self.getControl(130).setLabel(self.getString(30053))
         self.getControl(131).setVisible(False)
         self.getControl(131).setLabel(self.getString(30053))
         self.getControl(132).setVisible(False)
         self.getControl(132).setLabel(self.getString(30054))
         self.getControl(133).setVisible(False)
         self.getControl(133).setLabel(self.getString(30054))
         self.getControl(134).setVisible(False)
         self.getControl(134).setLabel(self.getString(30055))
         self.getControl(135).setVisible(False)
         self.getControl(135).setLabel(self.getString(30055))
         self.getControl(136).setVisible(False)
         self.getControl(136).setLabel(self.getString(30056))
         self.getControl(137).setVisible(False)
         self.getControl(137).setLabel(self.getString(30056))
         self.getControl(138).setVisible(False)
         self.getControl(138).setLabel(self.getString(30057))
         self.getControl(139).setVisible(False)
         self.getControl(139).setLabel(self.getString(30057))
         self.getControl(140).setVisible(False)
         self.getControl(140).setLabel(self.getString(30058))
         self.getControl(141).setVisible(False)
         self.getControl(141).setLabel(self.getString(30058))
         self.getControl(144).setVisible(False)
         self.getControl(144).setLabel(self.getString(30041))
         self.getControl(145).setVisible(False)
         self.getControl(145).setLabel(self.getString(30041))
         self.getControl(264).setVisible(False)
         self.getControl(264).setLabel(self.getString(31001))
         self.getControl(265).setVisible(False)
         self.getControl(265).setLabel(self.getString(31001))
         self.getControl(4201).setVisible(True)
         self.getControl(4201).setLabel(self.getString(30060))
         self.getControl(4003).setVisible(False)
         self.getControl(4003).setLabel(self.getString(30100))
         self.getControl(4004).setVisible(False)
         self.getControl(4004).setLabel(self.getString(30101))
         self.getControl(4005).setVisible(False)
         self.getControl(4005).setLabel(self.getString(30102))
         self.getControl(4007).setVisible(False)
         self.getControl(4007).setLabel(self.getString(30103))
         self.getControl(4008).setVisible(False)
         self.getControl(4008).setLabel(self.getString(30104))
         cSetVisible(self,4201,False)
         cSetVisible(self,4202,False)




         if english_enabled:
             cSetVisible(self,46,True)
             cSetVisible(self,49,True)
             cSetVisible(self,51,True)
             cSetVisible(self,53,True)
             cSetVisible(self,54,True)
             cSetVisible(self,57,True)
             cSetVisible(self,59,True)
             cSetVisible(self,61,True)
             cSetVisible(self,63,True)
             cSetVisible(self,65,True)
             cSetVisible(self,67,True)
             cSetVisible(self,69,True)
             cSetVisible(self,71,True)
             cSetVisible(self,73,True)



         if french_enabled:
             cSetVisible(self,264,True)




     def load_channel(self, elem):
         channel = Channel()
         for elem in elem.getchildren():
             if elem.tag == 'display-name':
                 channel.set_display_name(elem.text)
             elif elem.tag == 'icon':
                 channel.set_icon(elem.attrib['src'])
         return channel



     def load_programme(self, elem):
         programme = Programme()
         programme.set_start(elem.attrib['start'])
         programme.set_stop(elem.attrib['stop'])

         for elem in elem.getchildren():
             if elem.tag == 'title':
                 programme.set_title(elem.text)
             elif elem.tag == 'sub-title':
                 programme.set_title(elem.text)
             elif elem.tag == 'desc':
                 programme.set_desc(elem.text)
             elif elem.tag == 'category':
                 categories = programme.get_category()
                 categories.append(elem.text)
             elif elem.tag == 'episode-num':
                 programme.set_episode_num(elem.text)
             elif elem.tag == 'credits':
                 creditss = programme.get_credits()
                 creditss.append(self.load_credits(elem))
             elif elem.tag == 'icon':
                 programme.set_icon(elem.attrib['src'])
         return programme



     def load_credits(self, elem):
         creditss = Credits()
         for elem in elem.getchildren():
             if elem.tag == 'actor':
                 creditss.set_name(elem.text)
                 creditss.set_type('actor')
             elif elem.tag == 'presenter':
                 creditss.set_name(elem.text)
                 creditss.set_type('presenter')
             elif elem.tag == 'director':
                 creditss.set_name(elem.text)
                 creditss.set_type('director')
         return credits


     def timer1_8percent(self):
         for i in range(1):
             time.sleep(1)
             self.getControl(4202).setLabel("8%")


     def timer1_12percent(self):
         for i in range(1):
             time.sleep(2)
             self.getControl(4202).setLabel("12%")


     def timer1_18percent(self):
         for i in range(1):
             time.sleep(3)
             self.getControl(4202).setLabel("18%")


     def timer1_24percent(self):
         for i in range(1):
             time.sleep(4)
             self.getControl(4202).setLabel("24%")


     def timer1_32percent(self):
         for i in range(1):
             time.sleep(5)
             self.getControl(4202).setLabel("32%")


     def timer1_36percent(self):
         for i in range(1):
             time.sleep(6)
             self.getControl(4202).setLabel("36%")


     def timer1_40percent(self):
         for i in range(1):
             time.sleep(7)
             self.getControl(4202).setLabel("40%")


     def timer1_48percent(self):
         for i in range(1):
             time.sleep(8)
             self.getControl(4202).setLabel("48%")


     def timer1_56percent(self):
         for i in range(1):
             time.sleep(9)
             self.getControl(4202).setLabel("56%")


     def timer1_64percent(self):
         for i in range(1):
             time.sleep(10)
             self.getControl(4202).setLabel("64%")


     def timer1_72percent(self):
         for i in range(1):
             time.sleep(11)
             self.getControl(4202).setLabel("72%")


     def timer1_80percent(self):
         for i in range(1):
             time.sleep(12)
             self.getControl(4202).setLabel("80%")


     def timer1_88percent(self):
         for i in range(1):
             time.sleep(13)
             self.getControl(4202).setLabel("88%")


     def timer1_94percent(self):
         for i in range(1):
             time.sleep(14)
             self.getControl(4202).setLabel("94%")


     def timer1_98percent(self):
         for i in range(1):
             time.sleep(15)
             self.getControl(4202).setLabel("98%")


     def timer1_100percent(self):
         for i in range(1):
             time.sleep(16)
             self.getControl(4202).setLabel("100%")




     def allchannels_timer(self):
         while __killthread__ is False:
             time.sleep(2)
             self.getControl(4202).setLabel("1%")
             self.thread = threading.Thread(target=self.timer1_8percent)
             self.thread.setDaemon(True)
             self.thread.start()
             self.thread = threading.Thread(target=self.timer1_12percent)
             self.thread.setDaemon(True)
             self.thread.start()
             #DOWNLOAD THE XML SOURCE HERE
             url = ADDON.getSetting('allchannel.url')
             req = urllib2.Request(url)
             response = urllib2.urlopen(req)
             data = response.read()
             response.close()
             self.thread = threading.Thread(target=self.timer1_18percent)
             self.thread.setDaemon(True)
             self.thread.start()
             self.thread = threading.Thread(target=self.timer1_24percent)
             self.thread.setDaemon(True)
             self.thread.start()
             self.thread = threading.Thread(target=self.timer1_32percent)
             self.thread.setDaemon(True)
             self.thread.start()
             profilePath = xbmc.translatePath(os.path.join('special://userdata/addon_data/script.tvguide', ''))



             if os.path.exists(profilePath):
                 profilePath = profilePath + 'source.db'
                 con = database.connect(profilePath)
                 cur = con.cursor()
                 cur.execute('CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, stop_date TIMESTAMP, description TEXT)')
                 con.commit()
                 tv_elem = ElementTree.parse(StringIO.StringIO(data)).getroot()
                 profilePath = xbmc.translatePath(os.path.join('special://userdata/addon_data/script.tvguide', ''))
                 cur = con.cursor()
                 channels = OrderedDict()
                 self.thread = threading.Thread(target=self.timer1_36percent)
                 self.thread.setDaemon(True)
                 self.thread.start()
                 self.thread = threading.Thread(target=self.timer1_40percent)
                 self.thread.setDaemon(True)
                 self.thread.start()
                 self.thread = threading.Thread(target=self.timer1_48percent)
                 self.thread.setDaemon(True)
                 self.thread.start()
                 self.thread = threading.Thread(target=self.timer1_56percent)
                 self.thread.setDaemon(True)
                 self.thread.start()
                 self.thread = threading.Thread(target=self.timer1_64percent)
                 self.thread.setDaemon(True)
                 self.thread.start()
                 self.thread = threading.Thread(target=self.timer1_72percent)
                 self.thread.setDaemon(True)
                 self.thread.start()
                 self.thread = threading.Thread(target=self.timer1_80percent)
                 self.thread.setDaemon(True)
                 self.thread.start()
                 self.thread = threading.Thread(target=self.timer1_88percent)
                 self.thread.setDaemon(True)
                 self.thread.start()
                 self.thread = threading.Thread(target=self.timer1_94percent)
                 self.thread.setDaemon(True)
                 self.thread.start()
                 self.thread = threading.Thread(target=self.timer1_98percent)
                 self.thread.setDaemon(True)
                 self.thread.start()
                 self.thread = threading.Thread(target=self.timer1_100percent)
                 self.thread.setDaemon(True)
                 self.thread.start()
 
 
                 # Get the loaded data
                 for channel in tv_elem.findall('channel'):
                     channel_name = channel.find('display-name').text
                     for program in channel.findall('programme'):
                         if __killthread__:
                             return
                         title = program.find('title').text
                         start_time = program.get("start")
                         stop_time = program.get("stop")
                         cur.execute("INSERT INTO programs(channel, title, start_date, stop_date)" + " VALUES(?, ?, ?, ?)", [channel_name, title, start_time, stop_time])
                         con.commit()
                         con.close
 
                 print 'Channels store into database are now successfully!'
                 program = None
                 now = datetime.datetime.now()
                 #strCh = '(\'' + '\',\''.join(channelMap.keys()) + '\')'
                 cur.execute('SELECT channel, title, start_date, stop_date FROM programs WHERE channel')
                 getprogram_info = cur.fetchall()
 
                 for row in getprogram_info:
                     programming = row[0], row[1], row[2], row[3]
                     print programming
                     #print row[0], row[1], row[2], row[3]
                     #programming = row[0], row[1], row[2], row[3]
                     #programming = row[0], row[1], row[2], row[3]
                     #cur.close()#




     def entertainment_timer(self):
         pass


     def movies_timer(self):
         pass


     def kids_timer(self):
         pass


     def sports_timer(self):
         pass


     def news_timer(self):
         pass


     def documentaries_timer(self):
         pass


     def musicandradio_timer(self):
         pass


     def adult_timer(self):
         pass


     def myfavourites_timer(self):
         pass


     def picture_timer(self):
         pass


     def sound_timer(self):
         pass


     def changelanguage_timer(self):
         pass


     def parental_control_timer(self):
         for i in range(1):
             time.sleep(0.3)
             self.getControl(2).setVisible(False)
             self.getControl(5).setVisible(False)
             self.getControl(7).setVisible(False)
             self.getControl(8).setVisible(False)
             self.getControl(31).setVisible(False)
             self.getControl(33).setVisible(False)
             self.getControl(35).setVisible(False)
             self.getControl(36).setVisible(False)
             self.getControl(39).setVisible(False)
             self.getControl(41).setVisible(False)
             self.getControl(43).setVisible(False)
             self.getControl(45).setVisible(False)
             self.getControl(4000).setVisible(True)
             self.getControl(4001).setVisible(True)
             self.getControl(4002).setVisible(True)
             self.getControl(4006).setVisible(True)
             self.getControl(4009).setVisible(True)
             self.getControl(4010).setVisible(True)
             self.getControl(4011).setVisible(True)
             self.getControl(4012).setVisible(True)
             ADDON.setSetting('changepin.enabled', 'true')
             english_enabled = ADDON.getSetting('english.enabled') == 'true'


             if english_enabled:
                 self.getControl(47).setVisible(False)
                 self.getControl(49).setVisible(False)
                 self.getControl(51).setVisible(False)
                 self.getControl(52).setVisible(False)
                 self.getControl(75).setVisible(False)
                 self.getControl(77).setVisible(False)
                 self.getControl(79).setVisible(False)
                 self.getControl(80).setVisible(False)
                 self.getControl(83).setVisible(False)
                 self.getControl(85).setVisible(False)
                 self.getControl(87).setVisible(False)
                 self.getControl(89).setVisible(False)
                 self.getControl(4003).setVisible(True)
                 self.getControl(4004).setVisible(True)
                 self.getControl(4005).setVisible(True)
                 self.getControl(4007).setVisible(True)
                 self.getControl(4008).setVisible(True)




     def viewrestrictions_timer(self):
         pass                 


     def removechannels_timer(self):
         pass


     def systemdetails_timer(self):
         pass


     def speedtest_timer(self):
         pass




     def onAction(self, action):
         tvguide_table = xbmc.getCondVisibility('Control.IsVisible(5000)')
         tvguide_1 = xbmc.getCondVisibility('Control.IsVisible(5001)')
         tvguide_2 = xbmc.getCondVisibility('Control.IsVisible(4201)')
         tvguide_3 = xbmc.getCondVisibility('Control.IsVisible(4001)')
         tvguide_4 = xbmc.getCondVisibility('Control.IsVisible(4002)')
         tvguide_5 = xbmc.getCondVisibility('Control.IsVisible(4003)')
         tvguide_6 = xbmc.getCondVisibility('Control.IsVisible(4004)')
         tvguide_7 = xbmc.getCondVisibility('Control.IsVisible(4011)')
         tvguide_8 = xbmc.getCondVisibility('Control.IsVisible(4012)')
         tvguide_9 = xbmc.getCondVisibility('Control.IsVisible(4013)')
         tvguide_10 = xbmc.getCondVisibility('Control.IsVisible(4014)')
         tvguide_11 = xbmc.getCondVisibility('Control.IsVisible(4020)')
         tvguide_yellow = xbmc.getCondVisibility('Control.IsVisible(3)')
         reminders_yellow = xbmc.getCondVisibility('Control.IsVisible(4)')
         recorded_yellow = xbmc.getCondVisibility('Control.IsVisible(6)')
         settings_yellow = xbmc.getCondVisibility('Control.IsVisible(8)')
         allchannels_yellow = xbmc.getCondVisibility('Control.IsVisible(11)')
         entertainment_yellow = xbmc.getCondVisibility('Control.IsVisible(12)')
         movies_yellow = xbmc.getCondVisibility('Control.IsVisible(14)')
         kids_yellow = xbmc.getCondVisibility('Control.IsVisible(16)')
         sports_yellow = xbmc.getCondVisibility('Control.IsVisible(18)')
         news_yellow = xbmc.getCondVisibility('Control.IsVisible(20)')
         documentaries_yellow = xbmc.getCondVisibility('Control.IsVisible(22)')
         musicradio_yellow = xbmc.getCondVisibility('Control.IsVisible(24)')
         adult_yellow = xbmc.getCondVisibility('Control.IsVisible(26)')
         favourites_yellow = xbmc.getCondVisibility('Control.IsVisible(28)')
         picture_yellow = xbmc.getCondVisibility('Control.IsVisible(30)')
         sound_yellow = xbmc.getCondVisibility('Control.IsVisible(32)')
         changelanguage_yellow = xbmc.getCondVisibility('Control.IsVisible(34)')
         changepin_yellow = xbmc.getCondVisibility('Control.IsVisible(36)')
         viewrestrictions_yellow = xbmc.getCondVisibility('Control.IsVisible(38)')
         removechannels_yellow = xbmc.getCondVisibility('Control.IsVisible(40)')
         systemdetails_yellow = xbmc.getCondVisibility('Control.IsVisible(42)')
         speedtest_yellow = xbmc.getCondVisibility('Control.IsVisible(44)')
         lang_yellow = xbmc.getCondVisibility('Control.IsVisible(116)')
         lang_blue = xbmc.getCondVisibility('Control.IsVisible(117)')
         englishblck_enabled = xbmc.getCondVisibility('Control.IsVisible(118)')
         englishwhte_enabled = xbmc.getCondVisibility('Control.IsVisible(119)')
         frenchblck_enabled = xbmc.getCondVisibility('Control.IsVisible(120)')
         frenchwhte_enabled = xbmc.getCondVisibility('Control.IsVisible(121)')
         germanblck_enabled = xbmc.getCondVisibility('Control.IsVisible(122)')
         germanwhte_enabled = xbmc.getCondVisibility('Control.IsVisible(123)')
         italianblck_enabled = xbmc.getCondVisibility('Control.IsVisible(124)')
         italianwhte_enabled = xbmc.getCondVisibility('Control.IsVisible(125)')
         spainishblck_enabled = xbmc.getCondVisibility('Control.IsVisible(126)')
         spainishwhte_enabled = xbmc.getCondVisibility('Control.IsVisible(127)')
         russianblck_enabled = xbmc.getCondVisibility('Control.IsVisible(128)')
         russianwhte_enabled = xbmc.getCondVisibility('Control.IsVisible(129)')
         portugueseblck_enabled = xbmc.getCondVisibility('Control.IsVisible(130)')
         portuguesewhte_enabled = xbmc.getCondVisibility('Control.IsVisible(131)')
         greekblck_enabled = xbmc.getCondVisibility('Control.IsVisible(132)')
         greekwhte_enabled = xbmc.getCondVisibility('Control.IsVisible(133)')
         dutchblck_enabled = xbmc.getCondVisibility('Control.IsVisible(134)')
         dutchwhte_enabled = xbmc.getCondVisibility('Control.IsVisible(135)')
         chineseblck_enabled = xbmc.getCondVisibility('Control.IsVisible(136)')
         chinesewhte_enabled = xbmc.getCondVisibility('Control.IsVisible(137)')
         koreanblck_enabled = xbmc.getCondVisibility('Control.IsVisible(138)')
         koreanwhte_enabled = xbmc.getCondVisibility('Control.IsVisible(139)')
         arabicblck_enabled = xbmc.getCondVisibility('Control.IsVisible(140)')
         arabicwhte_enabled = xbmc.getCondVisibility('Control.IsVisible(141)')
         langsavesettings_yellow = xbmc.getCondVisibility('Control.IsVisible(142)')
         loading_gif = xbmc.getCondVisibility('Control.IsVisible(4200)')
         self.strAction = xbmcgui.ControlLabel(300, 200, 600, 200, '', 'font14', '0xFF00FF00')
         self.addControl(self.strAction)
         ADDON = xbmcaddon.Addon(id = 'script.tvguide')
         english_enabled = ADDON.getSetting('english.enabled') == 'true'
         french_enabled = ADDON.getSetting('french.enabled') == 'true'
         allchannels_enabled = ADDON.getSetting('allchannels.enabled') == 'true'
         entertainment_enabled = ADDON.getSetting('entertainment.enabled') == 'true'
         movies_enabled = ADDON.getSetting('movies.enabled') == 'true'
         kids_enabled = ADDON.getSetting('kids.enabled') == 'true'
         sports_enabled = ADDON.getSetting('sports.enabled') == 'true'
         news_enabled = ADDON.getSetting('news.enabled') == 'true'
         documentaries_enabled = ADDON.getSetting('documentaries.enabled') == 'true'
         musicradio_enabled = ADDON.getSetting('musicradio.enabled') == 'true'
         adult_enabled = ADDON.getSetting('adult.enabled') == 'true'
         favourites_enabled = ADDON.getSetting('favourites.enabled') == 'true'
         picture_enabled = ADDON.getSetting('picture.enabled') == 'true'
         sound_enabled = ADDON.getSetting('sound.enabled') == 'true'
         changelanguage_enabled = ADDON.getSetting('changelanguage.enabled') == 'true'
         changepin_enabled = ADDON.getSetting('changepin.enabled') == 'true'
         viewrestrictions_enabled = ADDON.getSetting('viewrestrictions.enabled') == 'true'
         removechannels_enabled = ADDON.getSetting('removechannels.enabled') == 'true'
         systemdetails_enabled = ADDON.getSetting('systemdetails.enabled') == 'true'
         speedtest_enabled = ADDON.getSetting('speedtest.enabled') == 'true'
         savesettings_yellow_enabled = xbmc.getCondVisibility('Control.IsVisible(142)')
         PIN_1_enabled = xbmc.getCondVisibility('Control.IsVisible(4009)')
         PIN_2_enabled = xbmc.getCondVisibility('Control.IsVisible(4010)')
         PIN_3_enabled = xbmc.getCondVisibility('Control.IsVisible(4011)')
         PIN_4_enabled = xbmc.getCondVisibility('Control.IsVisible(4012)')
         PIN_chars_1_enabled = xbmc.getCondVisibility('Control.IsVisible(4013)')
         PIN_chars_2_enabled = xbmc.getCondVisibility('Control.IsVisible(4014)')
         PIN_chars_3_enabled = xbmc.getCondVisibility('Control.IsVisible(4015)')
         PIN_chars_4_enabled = xbmc.getCondVisibility('Control.IsVisible(4016)')
         allchannels_server = "MY WEB SERVER URL"
         entertainment_server = "MY WEB SERVER URL"
         movies_server = "MY WEB SERVER URL"
         kids_server = 'URL'
         sports_server = "MY WEB SERVER URL"
         news_server = "MY WEB SERVER URL"
         documentaries_server = "MY WEB SERVER URL"
         musicradio_server = "MY WEB SERVER URL"
         adult_server = 'URL'
         favourites_server = "MY WEB SERVER URL"
         main_loading = 4200
         main_loading_progress = 4201
         main_loading_time_left = 4202




         if action == ACTION_PREVIOUS_MENU:
             self.close()


         if action == ACTION_BACKSPACE:
             if allchannels_enabled:
                 cSetVisible(self,3,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,9,True)
                 cSetVisible(self,11,True)
                 cSetVisible(self,13,True)
                 cSetVisible(self,15,True)
                 cSetVisible(self,17,True)
                 cSetVisible(self,19,True)
                 cSetVisible(self,21,True)
                 cSetVisible(self,23,True)
                 cSetVisible(self,25,True)
                 cSetVisible(self,27,True)
                 cSetVisible(self,29,True)
                 cSetVisible(self,146,False)
                 cSetVisible(self,4200,False)
                 cSetVisible(self,4201,False)
                 cSetVisible(self,4202,False)
                 self.getControl(4202).setLabel("")
                 ADDON.setSetting('allchannels.enabled', 'false')
                 __killthread__ = True
                 self.thread.join(0.5)
                 profilePath = xbmc.translatePath(os.path.join('special://userdata/addon_data/script.tvguide', ''))


                 if english_enabled:
                     cSetVisible(self,46,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,53,True)
                     cSetVisible(self,54,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)
                     cSetVisible(self,90,False)




             if entertainment_enabled:
                 cSetVisible(self,3,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,9,True)
                 cSetVisible(self,10,True)
                 cSetVisible(self,12,True)
                 cSetVisible(self,15,True)
                 cSetVisible(self,17,True)
                 cSetVisible(self,19,True)
                 cSetVisible(self,21,True)
                 cSetVisible(self,23,True)
                 cSetVisible(self,25,True)
                 cSetVisible(self,27,True)
                 cSetVisible(self,29,True)
                 ADDON.setSetting('entertainment.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,46,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,53,True)
                     cSetVisible(self,55,True)
                     cSetVisible(self,56,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)
                     cSetVisible(self,91,False)



             if movies_enabled:
                 cSetVisible(self,3,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,9,True)
                 cSetVisible(self,10,True)
                 cSetVisible(self,13,True)
                 cSetVisible(self,14,True)
                 cSetVisible(self,17,True)
                 cSetVisible(self,19,True)
                 cSetVisible(self,21,True)
                 cSetVisible(self,23,True)
                 cSetVisible(self,25,True)
                 cSetVisible(self,27,True)
                 cSetVisible(self,29,True)
                 ADDON.setSetting('movies.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,46,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,53,True)
                     cSetVisible(self,55,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,58,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)
                     cSetVisible(self,92,False)



             if kids_enabled:
                 cSetVisible(self,3,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,9,True)
                 cSetVisible(self,10,True)
                 cSetVisible(self,13,True)
                 cSetVisible(self,15,True)
                 cSetVisible(self,16,True)
                 cSetVisible(self,19,True)
                 cSetVisible(self,21,True)
                 cSetVisible(self,23,True)
                 cSetVisible(self,25,True)
                 cSetVisible(self,27,True)
                 cSetVisible(self,29,True)
                 ADDON.setSetting('kids.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,46,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,53,True)
                     cSetVisible(self,55,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,60,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)
                     cSetVisible(self,93,False)



             if sports_enabled:
                 cSetVisible(self,3,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,9,True)
                 cSetVisible(self,10,True)
                 cSetVisible(self,13,True)
                 cSetVisible(self,15,True)
                 cSetVisible(self,17,True)
                 cSetVisible(self,18,True)
                 cSetVisible(self,21,True)
                 cSetVisible(self,23,True)
                 cSetVisible(self,25,True)
                 cSetVisible(self,27,True)
                 cSetVisible(self,29,True)
                 ADDON.setSetting('sports.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,46,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,53,True)
                     cSetVisible(self,55,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,62,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)
                     cSetVisible(self,94,False)



             if news_enabled:
                 cSetVisible(self,3,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,9,True)
                 cSetVisible(self,10,True)
                 cSetVisible(self,13,True)
                 cSetVisible(self,15,True)
                 cSetVisible(self,17,True)
                 cSetVisible(self,19,True)
                 cSetVisible(self,20,True)
                 cSetVisible(self,23,True)
                 cSetVisible(self,25,True)
                 cSetVisible(self,27,True)
                 cSetVisible(self,29,True)
                 ADDON.setSetting('news.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,46,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,53,True)
                     cSetVisible(self,55,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,64,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)
                     cSetVisible(self,95,False)



             if documentaries_enabled:
                 cSetVisible(self,3,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,9,True)
                 cSetVisible(self,10,True)
                 cSetVisible(self,13,True)
                 cSetVisible(self,15,True)
                 cSetVisible(self,17,True)
                 cSetVisible(self,19,True)
                 cSetVisible(self,21,True)
                 cSetVisible(self,22,True)
                 cSetVisible(self,25,True)
                 cSetVisible(self,27,True)
                 cSetVisible(self,29,True)
                 ADDON.setSetting('documentaries.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,46,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,53,True)
                     cSetVisible(self,55,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,66,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)
                     cSetVisible(self,96,False)



             if musicradio_enabled:
                 cSetVisible(self,3,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,9,True)
                 cSetVisible(self,10,True)
                 cSetVisible(self,13,True)
                 cSetVisible(self,15,True)
                 cSetVisible(self,17,True)
                 cSetVisible(self,19,True)
                 cSetVisible(self,21,True)
                 cSetVisible(self,23,True)
                 cSetVisible(self,24,True)
                 cSetVisible(self,27,True)
                 cSetVisible(self,29,True)
                 ADDON.setSetting('musicradio.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,46,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,53,True)
                     cSetVisible(self,55,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,68,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)
                     cSetVisible(self,97,False)



             if adult_enabled:
                 cSetVisible(self,3,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,9,True)
                 cSetVisible(self,10,True)
                 cSetVisible(self,13,True)
                 cSetVisible(self,15,True)
                 cSetVisible(self,17,True)
                 cSetVisible(self,19,True)
                 cSetVisible(self,21,True)
                 cSetVisible(self,23,True)
                 cSetVisible(self,25,True)
                 cSetVisible(self,26,True)
                 cSetVisible(self,29,True)
                 ADDON.setSetting('adult.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,46,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,53,True)
                     cSetVisible(self,55,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,70,True)
                     cSetVisible(self,73,True)
                     cSetVisible(self,98,False)



             if favourites_enabled:
                 cSetVisible(self,3,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,9,True)
                 cSetVisible(self,10,True)
                 cSetVisible(self,13,True)
                 cSetVisible(self,15,True)
                 cSetVisible(self,17,True)
                 cSetVisible(self,19,True)
                 cSetVisible(self,21,True)
                 cSetVisible(self,23,True)
                 cSetVisible(self,25,True)
                 cSetVisible(self,27,True)
                 cSetVisible(self,28,True)
                 ADDON.setSetting('favourites.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,46,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,53,True)
                     cSetVisible(self,55,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,72,True)
                     cSetVisible(self,99,False)



             if picture_enabled:
                 cSetVisible(self,2,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,8,True)
                 cSetVisible(self,30,True)
                 cSetVisible(self,33,True)
                 cSetVisible(self,35,True)
                 cSetVisible(self,37,True)
                 cSetVisible(self,39,True)
                 cSetVisible(self,41,True)
                 cSetVisible(self,43,True)
                 cSetVisible(self,45,True)
                 ADDON.setSetting('picture.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,47,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,52,True)
                     cSetVisible(self,74,True)
                     cSetVisible(self,77,True)
                     cSetVisible(self,79,True)
                     cSetVisible(self,81,True)
                     cSetVisible(self,83,True)
                     cSetVisible(self,85,True)
                     cSetVisible(self,87,True)
                     cSetVisible(self,89,True)



             if sound_enabled:
                 cSetVisible(self,2,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,8,True)
                 cSetVisible(self,31,True)
                 cSetVisible(self,32,True)
                 cSetVisible(self,35,True)
                 cSetVisible(self,37,True)
                 cSetVisible(self,39,True)
                 cSetVisible(self,41,True)
                 cSetVisible(self,43,True)
                 cSetVisible(self,45,True)
                 ADDON.setSetting('sound.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,47,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,52,True)
                     cSetVisible(self,75,True)
                     cSetVisible(self,76,True)
                     cSetVisible(self,79,True)
                     cSetVisible(self,81,True)
                     cSetVisible(self,83,True)
                     cSetVisible(self,85,True)
                     cSetVisible(self,87,True)
                     cSetVisible(self,89,True)



             if changelanguage_enabled:
                 cSetVisible(self,2,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,8,True)
                 cSetVisible(self,31,True)
                 cSetVisible(self,33,True)
                 cSetVisible(self,34,True)
                 cSetVisible(self,37,True)
                 cSetVisible(self,39,True)
                 cSetVisible(self,41,True)
                 cSetVisible(self,43,True)
                 cSetVisible(self,45,True)
                 cSetVisible(self,114,False)
                 cSetVisible(self,115,False)
                 cSetVisible(self,116,False)
                 cSetVisible(self,143,False)
                 ADDON.setSetting('changelanguage.enabled', 'false')


                 if savesettings_yellow_enabled:
                     cSetVisible(self,111,False)
                     cSetVisible(self,117,False)
                     cSetVisible(self,142,False)
                     
                     
                     if english_enabled:
                         cSetVisible(self,113,False)
                         cSetVisible(self,144,False)


                 if english_enabled:
                     cSetVisible(self,109,False)
                     cSetVisible(self,110,False)
                     cSetVisible(self,112,False)
                     cSetVisible(self,145,False)
                     cSetVisible(self,47,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,52,True)
                     cSetVisible(self,75,True)
                     cSetVisible(self,77,True)
                     cSetVisible(self,78,True)
                     cSetVisible(self,81,True)
                     cSetVisible(self,83,True)
                     cSetVisible(self,85,True)
                     cSetVisible(self,87,True)
                     cSetVisible(self,89,True)


                     if englishblck_enabled:
                         cSetVisible(self,118,False)
                     elif englishwhte_enabled:
                         cSetVisible(self,119,False)

                     if frenchblck_enabled:
                         cSetVisible(self,120,False)
                     elif frenchwhte_enabled:
                         cSetVisible(self,121,False)


                     if germanblck_enabled:
                         cSetVisible(self,122,False)
                     elif germanwhte_enabled:
                         cSetVisible(self,123,False)


                     if italianblck_enabled:
                         cSetVisible(self,124,False)
                     elif italianwhte_enabled:
                         cSetVisible(self,125,False)


                     if spainishblck_enabled:
                         cSetVisible(self,126,False)
                     elif spainishwhte_enabled:
                         cSetVisible(self,127,False)


                     if russianblck_enabled:
                         cSetVisible(self,128,False)
                     elif russianwhte_enabled:
                         cSetVisible(self,129,False)


                     if portugueseblck_enabled:
                         cSetVisible(self,130,False)
                     elif portuguesewhte_enabled:
                         cSetVisible(self,131,False)


                     if greekblck_enabled:
                         cSetVisible(self,132,False)
                     elif greekwhte_enabled:
                         cSetVisible(self,133,False)


                     if dutchblck_enabled:
                         cSetVisible(self,134,False)
                     elif dutchwhte_enabled:
                         cSetVisible(self,135,False)


                     if chineseblck_enabled:
                         cSetVisible(self,136,False)
                     elif chinesewhte_enabled:
                         cSetVisible(self,137,False)


                     if koreanblck_enabled:
                         cSetVisible(self,138,False)
                     elif koreanwhte_enabled:
                         cSetVisible(self,139,False)


                     if arabicblck_enabled:
                         cSetVisible(self,140,False)
                     elif arabicwhte_enabled:
                         cSetVisible(self,141,False)



             if changepin_enabled:
                 if PIN_chars_4_enabled:
                     if PIN_chars_4_enabled == True:
                         cSetVisible(self,4016,False)
                         cSetVisible(self,4012,True)
                 
                 
                 elif PIN_chars_3_enabled:
                     if PIN_chars_3_enabled == True:
                         cSetVisible(self,4015,False)
                         cSetVisible(self,4011,True)
                 
                 
                 elif PIN_chars_2_enabled:
                     if PIN_chars_2_enabled == True:
                         cSetVisible(self,4014,False)
                         cSetVisible(self,4010,True)
                 
                 
                 elif PIN_chars_1_enabled:
                     if PIN_chars_1_enabled == True:
                         cSetVisible(self,4013,False)
                         cSetVisible(self,4009,True)





                 else:
                     cSetVisible(self,2,True)
                     cSetVisible(self,5,True)
                     cSetVisible(self,7,True)
                     cSetVisible(self,8,True)
                     cSetVisible(self,31,True)
                     cSetVisible(self,33,True)
                     cSetVisible(self,35,True)
                     cSetVisible(self,36,True)
                     cSetVisible(self,39,True)
                     cSetVisible(self,41,True)
                     cSetVisible(self,43,True)
                     cSetVisible(self,45,True)
                     cSetVisible(self,4000,False)
                     cSetVisible(self,4001,False)
                     cSetVisible(self,4002,False)
                     cSetVisible(self,4006,False)
                     cSetVisible(self,4009,False)
                     cSetVisible(self,4010,False)
                     cSetVisible(self,4011,False)
                     cSetVisible(self,4012,False)
                     ADDON.setSetting('changepin.enabled', 'false')




                     if english_enabled:
                         cSetVisible(self,47,True)
                         cSetVisible(self,49,True)
                         cSetVisible(self,51,True)
                         cSetVisible(self,52,True)
                         cSetVisible(self,75,True)
                         cSetVisible(self,77,True)
                         cSetVisible(self,79,True)
                         cSetVisible(self,80,True)
                         cSetVisible(self,83,True)
                         cSetVisible(self,85,True)
                         cSetVisible(self,87,True)
                         cSetVisible(self,89,True)
                         cSetVisible(self,4003,False)
                         cSetVisible(self,4004,False)
                         cSetVisible(self,4005,False)
                         cSetVisible(self,4007,False)
                         cSetVisible(self,4008,False)



             if viewrestrictions_enabled:
                 cSetVisible(self,2,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,8,True)
                 cSetVisible(self,31,True)
                 cSetVisible(self,33,True)
                 cSetVisible(self,35,True)
                 cSetVisible(self,37,True)
                 cSetVisible(self,38,True)
                 cSetVisible(self,41,True)
                 cSetVisible(self,43,True)
                 cSetVisible(self,45,True)
                 ADDON.setSetting('viewrestrictions.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,47,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,52,True)
                     cSetVisible(self,75,True)
                     cSetVisible(self,77,True)
                     cSetVisible(self,79,True)
                     cSetVisible(self,81,True)
                     cSetVisible(self,82,True)
                     cSetVisible(self,85,True)
                     cSetVisible(self,87,True)
                     cSetVisible(self,89,True)



             if removechannels_enabled:
                 cSetVisible(self,2,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,8,True)
                 cSetVisible(self,31,True)
                 cSetVisible(self,33,True)
                 cSetVisible(self,35,True)
                 cSetVisible(self,37,True)
                 cSetVisible(self,39,True)
                 cSetVisible(self,40,True)
                 cSetVisible(self,43,True)
                 cSetVisible(self,45,True)
                 ADDON.setSetting('removechannels.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,47,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,52,True)
                     cSetVisible(self,75,True)
                     cSetVisible(self,77,True)
                     cSetVisible(self,79,True)
                     cSetVisible(self,81,True)
                     cSetVisible(self,83,True)
                     cSetVisible(self,84,True)
                     cSetVisible(self,87,True)
                     cSetVisible(self,89,True)



             if systemdetails_enabled:
                 cSetVisible(self,2,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,8,True)
                 cSetVisible(self,31,True)
                 cSetVisible(self,33,True)
                 cSetVisible(self,35,True)
                 cSetVisible(self,37,True)
                 cSetVisible(self,39,True)
                 cSetVisible(self,41,True)
                 cSetVisible(self,42,True)
                 cSetVisible(self,45,True)
                 ADDON.setSetting('systemdetails.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,47,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,52,True)
                     cSetVisible(self,75,True)
                     cSetVisible(self,77,True)
                     cSetVisible(self,79,True)
                     cSetVisible(self,81,True)
                     cSetVisible(self,83,True)
                     cSetVisible(self,85,True)
                     cSetVisible(self,86,True)
                     cSetVisible(self,89,True)



             if speedtest_enabled:
                 cSetVisible(self,2,True)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,True)
                 cSetVisible(self,8,True)
                 cSetVisible(self,31,True)
                 cSetVisible(self,33,True)
                 cSetVisible(self,35,True)
                 cSetVisible(self,37,True)
                 cSetVisible(self,39,True)
                 cSetVisible(self,41,True)
                 cSetVisible(self,43,True)
                 cSetVisible(self,44,True)
                 ADDON.setSetting('speedtest.enabled', 'false')


                 if english_enabled:
                     cSetVisible(self,47,True)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,True)
                     cSetVisible(self,52,True)
                     cSetVisible(self,75,True)
                     cSetVisible(self,77,True)
                     cSetVisible(self,79,True)
                     cSetVisible(self,81,True)
                     cSetVisible(self,83,True)
                     cSetVisible(self,85,True)
                     cSetVisible(self,87,True)
                     cSetVisible(self,88,True)



             elif tvguide_yellow == True:
                 self.close()
             elif reminders_yellow == True:
                 self.close()
             elif recorded_yellow == True:
                 self.close()
             elif settings_yellow == True:
                 self.close()



         if action == ACTION_ENTER:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,3,False)
                     cSetVisible(self,4,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,9,False)
                     cSetVisible(self,11,False)
                     cSetVisible(self,13,False)
                     cSetVisible(self,15,False)
                     cSetVisible(self,17,False)
                     cSetVisible(self,19,False)
                     cSetVisible(self,21,False)
                     cSetVisible(self,23,False)
                     cSetVisible(self,25,False)
                     cSetVisible(self,27,False)
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('allchannels.enabled', 'true')
                     cSetVisible(self,146,True)
                     cSetVisible(self,4200,True)
                     cSetVisible(self,4201,True)
                     cSetVisible(self,4202,True)
                     self.getControl(4202).setLabel("0%")
                     self.thread = threading.Thread(target=self.allchannels_timer)
                     self.thread.setDaemon(True)
                     self.thread.start()



                     if englishblck_enabled == False:
                         cSetVisible(self,46,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,53,False)
                         cSetVisible(self,54,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)
                         cSetVisible(self,90,True)




                 if entertainment_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,3,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,9,False)
                     cSetVisible(self,10,False)
                     cSetVisible(self,12,False)
                     cSetVisible(self,15,False)
                     cSetVisible(self,17,False)
                     cSetVisible(self,19,False)
                     cSetVisible(self,21,False)
                     cSetVisible(self,23,False)
                     cSetVisible(self,25,False)
                     cSetVisible(self,27,False)
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('entertainment.enabled', 'true')


                     #get language
                     if english_enabled:
                         cSetVisible(self,46,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,53,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,56,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)
                         cSetVisible(self,91,True)


                     #DOWNLOAD THE XML SOURCE HERE
                     url = ADDON.getSetting('ontv.url')
                     req = urllib2.Request(url)
                     response = urllib2.urlopen(req)
                     data = response.read()
                     response.close()
                     profilePath = xbmc.translatePath(os.path.join('special://userdata/addon_data/script.tvguide', ''))

                     if os.path.exists(profilePath):
                         profilePath = profilePath + 'source.db'
                         con = database.connect(profilePath)
                         cur = con.cursor()
                         cur.execute('CREATE TABLE programs(id TEXT, channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT)')
                         con.commit()
                         con.close
                         tv_elem = ElementTree.parse(StringIO.StringIO(data)).getroot()

                         profilePath = xbmc.translatePath(os.path.join('special://userdata/addon_data/script.tvguide', ''))
                         profilePath = profilePath + 'source.db'
                         con = database.connect(profilePath)
                         cur = con.cursor()
                         channels = OrderedDict()

                         for elem in tv_elem.getchildren():
                             if elem.tag == 'channel':
                                 channels[elem.attrib['id']] = self.load_channel(elem)
                         for channel_key in channels:
                             channel = channels[channel_key]
                             display_name = channel.get_display_name()
                             print display_name




                 if movies_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,3,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,9,False)
                     cSetVisible(self,10,False)
                     cSetVisible(self,13,False)
                     cSetVisible(self,14,False)
                     cSetVisible(self,17,False)
                     cSetVisible(self,19,False)
                     cSetVisible(self,21,False)
                     cSetVisible(self,23,False)
                     cSetVisible(self,25,False)
                     cSetVisible(self,27,False)
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('movies.enabled', 'true')

                     #get language
                     if english_enabled:
                         SetVisible(self,46,False)
                         SetVisible(self,49,False)
                         SetVisible(self,51,False)
                         SetVisible(self,53,False)
                         SetVisible(self,55,False)
                         SetVisible(self,57,False)
                         SetVisible(self,58,False)
                         SetVisible(self,61,False)
                         SetVisible(self,63,False)
                         SetVisible(self,65,False)
                         SetVisible(self,67,False)
                         SetVisible(self,69,False)
                         SetVisible(self,71,False)
                         SetVisible(self,73,False)
                         SetVisible(self,92,True)



                 if kids_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,3,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,9,False)
                     cSetVisible(self,10,False)
                     cSetVisible(self,13,False)
                     cSetVisible(self,15,False)
                     cSetVisible(self,16,False)
                     cSetVisible(self,19,False)
                     cSetVisible(self,21,False)
                     cSetVisible(self,23,False)
                     cSetVisible(self,25,False)
                     cSetVisible(self,27,False)
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('kids.enabled', 'true')

                     #get language
                     if english_enabled:
                         SetVisible(self,46,False)
                         SetVisible(self,49,False)
                         SetVisible(self,51,False)
                         SetVisible(self,53,False)
                         SetVisible(self,55,False)
                         SetVisible(self,57,False)
                         SetVisible(self,59,False)
                         SetVisible(self,60,False)
                         SetVisible(self,63,False)
                         SetVisible(self,65,False)
                         SetVisible(self,67,False)
                         SetVisible(self,69,False)
                         SetVisible(self,71,False)
                         SetVisible(self,73,False)
                         SetVisible(self,93,True)




                 if sports_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,3,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,9,False)
                     cSetVisible(self,10,False)
                     cSetVisible(self,13,False)
                     cSetVisible(self,15,False)
                     cSetVisible(self,17,False)
                     cSetVisible(self,18,False)
                     cSetVisible(self,21,False)
                     cSetVisible(self,23,False)
                     cSetVisible(self,25,False)
                     cSetVisible(self,27,False)
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('sports.enabled', 'true')

                     #get language
                     if english_enabled:
                         SetVisible(self,46,False)
                         SetVisible(self,49,False)
                         SetVisible(self,51,False)
                         SetVisible(self,53,False)
                         SetVisible(self,55,False)
                         SetVisible(self,57,False)
                         SetVisible(self,59,False)
                         SetVisible(self,61,False)
                         SetVisible(self,62,False)
                         SetVisible(self,65,False)
                         SetVisible(self,67,False)
                         SetVisible(self,69,False)
                         SetVisible(self,71,False)
                         SetVisible(self,73,False)
                         SetVisible(self,94,True)



                 if news_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,3,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,9,False)
                     cSetVisible(self,10,False)
                     cSetVisible(self,13,False)
                     cSetVisible(self,15,False)
                     cSetVisible(self,17,False)
                     cSetVisible(self,19,False)
                     cSetVisible(self,20,False)
                     cSetVisible(self,23,False)
                     cSetVisible(self,25,False)
                     cSetVisible(self,27,False)
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     cSetVisible(self,52,False)
                     ADDON.setSetting('news.enabled', 'true')

                     #get language
                     if english_enabled:
                         SetVisible(self,46,False)
                         SetVisible(self,49,False)
                         SetVisible(self,51,False)
                         SetVisible(self,53,False)
                         SetVisible(self,55,False)
                         SetVisible(self,57,False)
                         SetVisible(self,59,False)
                         SetVisible(self,61,False)
                         SetVisible(self,63,False)
                         SetVisible(self,64,False)
                         SetVisible(self,67,False)
                         SetVisible(self,69,False)
                         SetVisible(self,71,False)
                         SetVisible(self,73,False)
                         SetVisible(self,95,True)



                 if documentaries_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,3,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,9,False)
                     cSetVisible(self,10,False)
                     cSetVisible(self,13,False)
                     cSetVisible(self,15,False)
                     cSetVisible(self,17,False)
                     cSetVisible(self,19,False)
                     cSetVisible(self,21,False)
                     cSetVisible(self,22,False)
                     cSetVisible(self,25,False)
                     cSetVisible(self,27,False)
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     cSetVisible(self,52,False)
                     ADDON.setSetting('documentaries.enabled', 'true')

                     #get language
                     if english_enabled:
                         SetVisible(self,46,False)
                         SetVisible(self,49,False)
                         SetVisible(self,51,False)
                         SetVisible(self,53,False)
                         SetVisible(self,55,False)
                         SetVisible(self,57,False)
                         SetVisible(self,59,False)
                         SetVisible(self,61,False)
                         SetVisible(self,63,False)
                         SetVisible(self,65,False)
                         SetVisible(self,66,False)
                         SetVisible(self,69,False)
                         SetVisible(self,71,False)
                         SetVisible(self,73,False)
                         SetVisible(self,96,True)




                 if musicradio_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,3,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,9,False)
                     cSetVisible(self,10,False)
                     cSetVisible(self,13,False)
                     cSetVisible(self,15,False)
                     cSetVisible(self,17,False)
                     cSetVisible(self,19,False)
                     cSetVisible(self,21,False)
                     cSetVisible(self,23,False)
                     cSetVisible(self,24,False)
                     cSetVisible(self,27,False)
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     cSetVisible(self,52,False)
                     ADDON.setSetting('musicradio.enabled', 'true')

                     #get language
                     if english_enabled:
                         SetVisible(self,46,False)
                         SetVisible(self,49,False)
                         SetVisible(self,51,False)
                         SetVisible(self,53,False)
                         SetVisible(self,55,False)
                         SetVisible(self,57,False)
                         SetVisible(self,59,False)
                         SetVisible(self,61,False)
                         SetVisible(self,63,False)
                         SetVisible(self,65,False)
                         SetVisible(self,67,False)
                         SetVisible(self,68,False)
                         SetVisible(self,71,False)
                         SetVisible(self,73,False)
                         SetVisible(self,97,True)



                 if adult_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,3,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,9,False)
                     cSetVisible(self,10,False)
                     cSetVisible(self,13,False)
                     cSetVisible(self,15,False)
                     cSetVisible(self,17,False)
                     cSetVisible(self,19,False)
                     cSetVisible(self,21,False)
                     cSetVisible(self,23,False)
                     cSetVisible(self,25,False)
                     cSetVisible(self,26,False)
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('adult.enabled', 'true')

                     #get language
                     if english_enabled:
                         cSetVisible(self,46,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,53,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,70,False)
                         cSetVisible(self,73,False)
                         cSetVisible(self,98,True)



                 if favourites_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,3,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,9,False)
                     cSetVisible(self,10,False)
                     cSetVisible(self,13,False)
                     cSetVisible(self,15,False)
                     cSetVisible(self,17,False)
                     cSetVisible(self,19,False)
                     cSetVisible(self,21,False)
                     cSetVisible(self,23,False)
                     cSetVisible(self,25,False)
                     cSetVisible(self,27,False)
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('favourites.enabled', 'true')


                     #get language
                     if english_enabled:
                         cSetVisible(self,46,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,53,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,72,False)
                         cSetVisible(self,99,True)




             elif settings_yellow:
                 if picture_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,8,False)
                     cSetVisible(self,30,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('picture.enabled', 'true')


                     if english_enabled:
                         cSetVisible(self,47,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,52,False)
                         cSetVisible(self,74,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)



                 if sound_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,8,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,32,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('sound.enabled', 'true')


                     if english_enabled:
                         cSetVisible(self,47,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,52,False)
                         cSetVisible(self,75,False)
                         cSetVisible(self,76,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)


                 if changelanguage_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,8,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,34,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     cSetVisible(self,110,True)
                     cSetVisible(self,114,True)
                     cSetVisible(self,115,True)
                     cSetVisible(self,116,True)
                     cSetVisible(self,143,True)
                     ADDON.setSetting('changelanguage.enabled', 'true')


                     if english_enabled:
                         cSetVisible(self,47,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,52,False)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,78,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)
                         cSetVisible(self,109,True)
                         cSetVisible(self,112,True)
                         cSetVisible(self,118,True)
                         cSetVisible(self,145,True)





                 if changepin_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,8,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,36,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     cSetVisible(self,4000,True)
                     cSetVisible(self,4001,True)
                     cSetVisible(self,4002,True)
                     cSetVisible(self,4006,True)
                     cSetVisible(self,4009,True)
                     cSetVisible(self,4010,True)
                     cSetVisible(self,4011,True)
                     cSetVisible(self,4012,True)
                     ADDON.setSetting('changepin.enabled', 'true')


                     if english_enabled:
                         cSetVisible(self,47,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,52,False)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,80,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)
                         cSetVisible(self,4003,True)
                         cSetVisible(self,4004,True)
                         cSetVisible(self,4005,True)
                         cSetVisible(self,4007,True)
                         cSetVisible(self,4008,True)





                 if viewrestrictions_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,8,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,38,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('viewrestrictions.enabled', 'true')


                     if english_enabled:
                         cSetVisible(self,47,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,52,False)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,82,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)



                 if removechannels_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,8,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,40,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('removechannels.enabled', 'true')


                     if english_enabled:
                         cSetVisible(self,47,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,52,False)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,84,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)



                 if systemdetails_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,8,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,42,False)
                     cSetVisible(self,45,False)
                     ADDON.setSetting('systemdetails.enabled', 'true')


                     if english_enabled:
                         cSetVisible(self,47,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,52,False)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,86,False)
                         cSetVisible(self,89,False)



                 if speedtest_yellow:
                     cSetVisible(self,2,False)
                     cSetVisible(self,5,False)
                     cSetVisible(self,7,False)
                     cSetVisible(self,8,False)
                     cSetVisible(self,31,False)
                     cSetVisible(self,33,False)
                     cSetVisible(self,35,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,44,False)
                     ADDON.setSetting('speedtest.enabled', 'true')


                     if english_enabled:
                         cSetVisible(self,47,False)
                         cSetVisible(self,49,False)
                         cSetVisible(self,51,False)
                         cSetVisible(self,52,False)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,88,False)



             if changelanguage_enabled:
                 if savesettings_yellow_enabled:
                     cSetVisible(self,2,True)
                     cSetVisible(self,5,True)
                     cSetVisible(self,7,True)
                     cSetVisible(self,8,True)
                     cSetVisible(self,31,True)
                     cSetVisible(self,33,True)
                     cSetVisible(self,34,True)
                     cSetVisible(self,37,True)
                     cSetVisible(self,39,True)
                     cSetVisible(self,41,True)
                     cSetVisible(self,43,True)
                     cSetVisible(self,45,True)
                     cSetVisible(self,111,False)
                     cSetVisible(self,114,False)
                     cSetVisible(self,115,False)
                     cSetVisible(self,117,False)
                     cSetVisible(self,142,False)
                     ADDON.setSetting('changelanguage.enabled', 'false')


                     if english_enabled:
                         cSetVisible(self,109,False)
                         cSetVisible(self,113,False)
                         cSetVisible(self,144,False)


                     if englishwhte_enabled:
                         cSetVisible(self,119,False)
                         cSetVisible(self,47,True)
                         cSetVisible(self,49,True)
                         cSetVisible(self,51,True)
                         cSetVisible(self,52,True)
                         cSetVisible(self,75,True)
                         cSetVisible(self,77,True)
                         cSetVisible(self,78,True)
                         cSetVisible(self,81,True)
                         cSetVisible(self,83,True)
                         cSetVisible(self,85,True)
                         cSetVisible(self,87,True)
                         cSetVisible(self,89,True)
                         ADDON.setSetting('english.enabled', 'true')


                     if frenchwhte_enabled:
                         cSetVisible(self,265,True)
                         ADDON.setSetting('english.enabled', 'false')
                         ADDON.setSetting('french.enabled', 'true')


                     if germanwhte_enabled:
                         self.close()




         if action == ACTION_MOVE_LEFT:
             if tvguide_yellow:
                 cSetVisible(self,3,False)
                 cSetVisible(self,2,True)
                 cSetVisible(self,9,False)
                 cSetVisible(self,8,True)
                 cSetVisible(self,10,False)
                 cSetVisible(self,11,False)
                 cSetVisible(self,12,False)
                 cSetVisible(self,13,False)
                 cSetVisible(self,14,False)
                 cSetVisible(self,15,False)
                 cSetVisible(self,16,False)
                 cSetVisible(self,17,False)
                 cSetVisible(self,18,False)
                 cSetVisible(self,19,False)
                 cSetVisible(self,20,False)
                 cSetVisible(self,21,False)
                 cSetVisible(self,22,False)
                 cSetVisible(self,23,False)
                 cSetVisible(self,24,False)
                 cSetVisible(self,25,False)
                 cSetVisible(self,26,False)
                 cSetVisible(self,27,False)
                 cSetVisible(self,28,False)
                 cSetVisible(self,29,False)
                 cSetVisible(self,30,True)
                 cSetVisible(self,33,True)
                 cSetVisible(self,35,True)
                 cSetVisible(self,37,True)
                 cSetVisible(self,39,True)
                 cSetVisible(self,41,True)
                 cSetVisible(self,43,True)
                 cSetVisible(self,45,True)



                 if english_enabled:
                     cSetVisible(self,46,False)
                     cSetVisible(self,47,True)
                     cSetVisible(self,53,False)
                     cSetVisible(self,52,True)
                     cSetVisible(self,74,True)
                     cSetVisible(self,77,True)
                     cSetVisible(self,79,True)
                     cSetVisible(self,81,True)
                     cSetVisible(self,83,True)
                     cSetVisible(self,85,True)
                     cSetVisible(self,87,True)
                     cSetVisible(self,89,True)


                 if allchannels_yellow:
                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)




                 if entertainment_yellow:
                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,56,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)


                 if movies_yellow:
                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,58,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)



                 if kids_yellow:
                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,60,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)


                 if sports_yellow:
                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,62,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)



                 if news_yellow:
                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,64,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)


                 if documentaries_yellow:
                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,66,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)


                 if musicradio_yellow:
                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,68,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)


                 if adult_yellow:
                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,70,False)
                         cSetVisible(self,73,False)


                 if favourites_yellow:
                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,72,False)


             if reminders_yellow:
                 cSetVisible(self,4,False)
                 cSetVisible(self,5,True)
                 cSetVisible(self,2,False)
                 cSetVisible(self,3,True)
                 cSetVisible(self,10,False)
                 cSetVisible(self,11,True)
                 cSetVisible(self,12,False)
                 cSetVisible(self,13,True)
                 cSetVisible(self,14,False)
                 cSetVisible(self,15,True)
                 cSetVisible(self,16,False)
                 cSetVisible(self,17,True)
                 cSetVisible(self,18,False)
                 cSetVisible(self,19,True)
                 cSetVisible(self,20,False)
                 cSetVisible(self,21,True)
                 cSetVisible(self,22,False)
                 cSetVisible(self,23,True)
                 cSetVisible(self,24,False)
                 cSetVisible(self,25,True)
                 cSetVisible(self,26,False)
                 cSetVisible(self,27,True)
                 cSetVisible(self,28,False)
                 cSetVisible(self,29,True)



                 if english_enabled:
                     cSetVisible(self,47,False)
                     cSetVisible(self,46,True)
                     cSetVisible(self,48,False)
                     cSetVisible(self,49,True)
                     cSetVisible(self,54,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)




             if recorded_yellow:
                 cSetVisible(self,6,False)
                 cSetVisible(self,7,True)
                 cSetVisible(self,5,False)
                 cSetVisible(self,4,True)

                 if english_enabled:
                     cSetVisible(self,50,False)
                     cSetVisible(self,51,True)
                     cSetVisible(self,49,False)
                     cSetVisible(self,48,True)



             if settings_yellow:
                 cSetVisible(self,8,False)
                 cSetVisible(self,9,True)
                 cSetVisible(self,7,False)
                 cSetVisible(self,6,True)
                 cSetVisible(self,30,False)
                 cSetVisible(self,31,False)
                 cSetVisible(self,32,False)
                 cSetVisible(self,33,False)
                 cSetVisible(self,34,False)
                 cSetVisible(self,35,False)
                 cSetVisible(self,36,False)
                 cSetVisible(self,37,False)
                 cSetVisible(self,38,False)
                 cSetVisible(self,39,False)
                 cSetVisible(self,40,False)
                 cSetVisible(self,41,False)
                 cSetVisible(self,42,False)
                 cSetVisible(self,43,False)
                 cSetVisible(self,44,False)
                 cSetVisible(self,45,False)



                 if picture_yellow:
                     if english_enabled:
                         cSetVisible(self,52,False)
                         cSetVisible(self,53,True)
                         cSetVisible(self,51,False)
                         cSetVisible(self,50,True)
                         cSetVisible(self,74,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)


                 if sound_yellow:
                     if english_enabled:
                         cSetVisible(self,52,False)
                         cSetVisible(self,53,True)
                         cSetVisible(self,51,False)
                         cSetVisible(self,50,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,76,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)


                 if changelanguage_yellow:
                     if english_enabled:
                         cSetVisible(self,52,False)
                         cSetVisible(self,53,True)
                         cSetVisible(self,51,False)
                         cSetVisible(self,50,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,78,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)


                 if changepin_yellow:
                     if english_enabled:
                         cSetVisible(self,52,False)
                         cSetVisible(self,53,True)
                         cSetVisible(self,51,False)
                         cSetVisible(self,50,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,80,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)


                 if viewrestrictions_yellow:
                     if english_enabled:
                         cSetVisible(self,52,False)
                         cSetVisible(self,53,True)
                         cSetVisible(self,51,False)
                         cSetVisible(self,50,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,82,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)


                 if removechannels_yellow:
                     if english_enabled:
                         cSetVisible(self,52,False)
                         cSetVisible(self,53,True)
                         cSetVisible(self,51,False)
                         cSetVisible(self,50,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,84,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)


                 if systemdetails_yellow:
                     if english_enabled:
                         cSetVisible(self,52,False)
                         cSetVisible(self,53,True)
                         cSetVisible(self,51,False)
                         cSetVisible(self,50,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,86,False)
                         cSetVisible(self,89,False)


                 if speedtest_yellow:
                     if english_enabled:
                         cSetVisible(self,52,False)
                         cSetVisible(self,53,True)
                         cSetVisible(self,51,False)
                         cSetVisible(self,50,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,88,False)



             if changelanguage_enabled:
                 if englishblck_enabled == True:
                     cSetVisible(self,118,False)
                     cSetVisible(self,140,True)
                 elif frenchblck_enabled == True:
                     cSetVisible(self,120,False)
                     cSetVisible(self,118,True)
                 elif germanblck_enabled == True:
                     cSetVisible(self,122,False)
                     cSetVisible(self,120,True)
                 elif italianblck_enabled == True:
                     cSetVisible(self,124,False)
                     cSetVisible(self,122,True)
                 elif spainishblck_enabled == True:
                     cSetVisible(self,126,False)
                     cSetVisible(self,124,True)
                 elif russianblck_enabled == True:
                     cSetVisible(self,128,False)
                     cSetVisible(self,126,True)
                 elif portugueseblck_enabled == True:
                     cSetVisible(self,130,False)
                     cSetVisible(self,128,True)
                 elif greekblck_enabled == True:
                     cSetVisible(self,132,False)
                     cSetVisible(self,130,True)
                 elif dutchblck_enabled == True:
                     cSetVisible(self,134,False)
                     cSetVisible(self,132,True)
                 elif chineseblck_enabled == True:
                     cSetVisible(self,136,False)
                     cSetVisible(self,134,True)
                 elif koreanblck_enabled == True:
                     cSetVisible(self,138,False)
                     cSetVisible(self,136,True)
                 elif arabicblck_enabled == True:
                     cSetVisible(self,140,False)
                     cSetVisible(self,138,True)




         if action == ACTION_MOVE_RIGHT:
             if tvguide_yellow:
                 cSetVisible(self,3,False)
                 cSetVisible(self,2,True)
                 cSetVisible(self,5,False)
                 cSetVisible(self,4,True)
                 cSetVisible(self,11,False)
                 cSetVisible(self,12,False)
                 cSetVisible(self,13,False)
                 cSetVisible(self,15,False)
                 cSetVisible(self,17,False)
                 cSetVisible(self,19,False)
                 cSetVisible(self,21,False)
                 cSetVisible(self,23,False)
                 cSetVisible(self,25,False)
                 cSetVisible(self,27,False)
                 cSetVisible(self,29,False)


                 if english_enabled:
                     cSetVisible(self,46,False)
                     cSetVisible(self,47,True)
                     cSetVisible(self,49,False)
                     cSetVisible(self,48,True)


                 if allchannels_yellow:
                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)




                 if entertainment_yellow:
                     if english_enabled:
                         cSetVisible(self,10,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,56,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)


                 if movies_yellow:
                     if english_enabled:
                         cSetVisible(self,10,False)
                         cSetVisible(self,14,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,58,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)



                 if kids_yellow:
                     if english_enabled:
                         cSetVisible(self,10,False)
                         cSetVisible(self,16,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,60,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)


                 if sports_yellow:
                     if english_enabled:
                         cSetVisible(self,10,False)
                         cSetVisible(self,18,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,62,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)



                 if news_yellow:
                     if english_enabled:
                         cSetVisible(self,10,False)
                         cSetVisible(self,20,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,64,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)


                 if documentaries_yellow:
                     if english_enabled:
                         cSetVisible(self,10,False)
                         cSetVisible(self,22,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,66,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)


                 if musicradio_yellow:
                     if english_enabled:
                         cSetVisible(self,10,False)
                         cSetVisible(self,24,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,68,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,73,False)


                 if adult_yellow:
                     if english_enabled:
                         cSetVisible(self,10,False)
                         cSetVisible(self,26,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,70,False)
                         cSetVisible(self,73,False)


                 if favourites_yellow:
                     if english_enabled:
                         cSetVisible(self,10,False)
                         cSetVisible(self,28,False)
                         cSetVisible(self,55,False)
                         cSetVisible(self,57,False)
                         cSetVisible(self,59,False)
                         cSetVisible(self,61,False)
                         cSetVisible(self,63,False)
                         cSetVisible(self,65,False)
                         cSetVisible(self,67,False)
                         cSetVisible(self,69,False)
                         cSetVisible(self,71,False)
                         cSetVisible(self,72,False)



             if reminders_yellow:
                 cSetVisible(self,4,False)
                 cSetVisible(self,5,True)
                 cSetVisible(self,7,False)
                 cSetVisible(self,6,True)


                 if english_enabled:
                     cSetVisible(self,48,False)
                     cSetVisible(self,49,True)
                     cSetVisible(self,51,False)
                     cSetVisible(self,50,True)



             if recorded_yellow:
                 cSetVisible(self,6,False)
                 cSetVisible(self,7,True)
                 cSetVisible(self,9,False)
                 cSetVisible(self,8,True)
                 cSetVisible(self,30,True)
                 cSetVisible(self,33,True)
                 cSetVisible(self,35,True)
                 cSetVisible(self,37,True)
                 cSetVisible(self,39,True)
                 cSetVisible(self,41,True)
                 cSetVisible(self,43,True)
                 cSetVisible(self,45,True)


                 if english_enabled:
                     cSetVisible(self,50,False)
                     cSetVisible(self,51,True)
                     cSetVisible(self,53,False)
                     cSetVisible(self,52,True)
                     cSetVisible(self,74,True)
                     cSetVisible(self,77,True)
                     cSetVisible(self,79,True)
                     cSetVisible(self,81,True)
                     cSetVisible(self,83,True)
                     cSetVisible(self,85,True)
                     cSetVisible(self,87,True)
                     cSetVisible(self,89,True)


             if settings_yellow:
                 cSetVisible(self,8,False)
                 cSetVisible(self,9,True)
                 cSetVisible(self,2,False)
                 cSetVisible(self,3,True)
                 cSetVisible(self,11,True)
                 cSetVisible(self,13,True)
                 cSetVisible(self,15,True)
                 cSetVisible(self,17,True)
                 cSetVisible(self,19,True)
                 cSetVisible(self,21,True)
                 cSetVisible(self,23,True)
                 cSetVisible(self,25,True)
                 cSetVisible(self,27,True)
                 cSetVisible(self,29,True)
                 cSetVisible(self,30,False)
                 cSetVisible(self,33,False)
                 cSetVisible(self,35,False)
                 cSetVisible(self,37,False)
                 cSetVisible(self,39,False)
                 cSetVisible(self,41,False)
                 cSetVisible(self,43,False)
                 cSetVisible(self,45,False)


                 if picture_yellow:
                     if english_enabled:
                         cSetVisible(self,52,False)
                         cSetVisible(self,53,True)
                         cSetVisible(self,47,False)
                         cSetVisible(self,46,True)
                         cSetVisible(self,74,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,57,True)
                         cSetVisible(self,59,True)
                         cSetVisible(self,61,True)
                         cSetVisible(self,63,True)
                         cSetVisible(self,65,True)
                         cSetVisible(self,67,True)
                         cSetVisible(self,69,True)
                         cSetVisible(self,71,True)
                         cSetVisible(self,73,True)



                 if sound_yellow:
                     if english_enabled:
                         cSetVisible(self,52,False)
                         cSetVisible(self,53,True)
                         cSetVisible(self,47,False)
                         cSetVisible(self,46,True)
                         cSetVisible(self,31,False)
                         cSetVisible(self,32,False)
                         cSetVisible(self,35,False)
                         cSetVisible(self,37,False)
                         cSetVisible(self,39,False)
                         cSetVisible(self,41,False)
                         cSetVisible(self,43,False)
                         cSetVisible(self,45,False)
                         cSetVisible(self,75,False)
                         cSetVisible(self,76,False)
                         cSetVisible(self,79,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,57,True)
                         cSetVisible(self,59,True)
                         cSetVisible(self,61,True)
                         cSetVisible(self,63,True)
                         cSetVisible(self,65,True)
                         cSetVisible(self,67,True)
                         cSetVisible(self,69,True)
                         cSetVisible(self,71,True)
                         cSetVisible(self,73,True)


                 if changelanguage_yellow:
                     if english_enabled:
                         cSetVisible(self,52,False)
                         cSetVisible(self,53,True)
                         cSetVisible(self,47,False)
                         cSetVisible(self,46,True)
                         cSetVisible(self,31,False)
                         cSetVisible(self,32,False)
                         cSetVisible(self,34,False)
                         cSetVisible(self,37,False)
                         cSetVisible(self,39,False)
                         cSetVisible(self,41,False)
                         cSetVisible(self,43,False)
                         cSetVisible(self,45,False)
                         cSetVisible(self,75,False)
                         cSetVisible(self,77,False)
                         cSetVisible(self,78,False)
                         cSetVisible(self,81,False)
                         cSetVisible(self,83,False)
                         cSetVisible(self,85,False)
                         cSetVisible(self,87,False)
                         cSetVisible(self,89,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,57,True)
                         cSetVisible(self,59,True)
                         cSetVisible(self,61,True)
                         cSetVisible(self,63,True)
                         cSetVisible(self,65,True)
                         cSetVisible(self,67,True)
                         cSetVisible(self,69,True)
                         cSetVisible(self,71,True)
                         cSetVisible(self,73,True)


                 if changepin_yellow:
                     cSetVisible(self,52,False)
                     cSetVisible(self,53,True)
                     cSetVisible(self,47,False)
                     cSetVisible(self,46,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,32,False)
                     cSetVisible(self,34,False)
                     cSetVisible(self,36,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     cSetVisible(self,75,False)
                     cSetVisible(self,77,False)
                     cSetVisible(self,79,False)
                     cSetVisible(self,80,False)
                     cSetVisible(self,83,False)
                     cSetVisible(self,85,False)
                     cSetVisible(self,87,False)
                     cSetVisible(self,89,False)
                     cSetVisible(self,54,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)


                 if viewrestrictions_yellow:
                     cSetVisible(self,52,False)
                     cSetVisible(self,53,True)
                     cSetVisible(self,47,False)
                     cSetVisible(self,46,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,32,False)
                     cSetVisible(self,34,False)
                     cSetVisible(self,37,False)
                     cSetVisible(self,38,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     cSetVisible(self,75,False)
                     cSetVisible(self,77,False)
                     cSetVisible(self,79,False)
                     cSetVisible(self,81,False)
                     cSetVisible(self,82,False)
                     cSetVisible(self,85,False)
                     cSetVisible(self,87,False)
                     cSetVisible(self,89,False)
                     cSetVisible(self,54,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)


                 if removechannels_yellow:
                     cSetVisible(self,52,False)
                     cSetVisible(self,53,True)
                     cSetVisible(self,47,False)
                     cSetVisible(self,46,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,32,False)
                     cSetVisible(self,34,False)
                     cSetVisible(self,36,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,40,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,45,False)
                     cSetVisible(self,75,False)
                     cSetVisible(self,77,False)
                     cSetVisible(self,79,False)
                     cSetVisible(self,81,False)
                     cSetVisible(self,83,False)
                     cSetVisible(self,84,False)
                     cSetVisible(self,87,False)
                     cSetVisible(self,89,False)
                     cSetVisible(self,54,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)


                 if systemdetails_yellow:
                     cSetVisible(self,52,False)
                     cSetVisible(self,53,True)
                     cSetVisible(self,47,False)
                     cSetVisible(self,46,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,32,False)
                     cSetVisible(self,34,False)
                     cSetVisible(self,36,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,42,False)
                     cSetVisible(self,45,False)
                     cSetVisible(self,75,False)
                     cSetVisible(self,77,False)
                     cSetVisible(self,79,False)
                     cSetVisible(self,81,False)
                     cSetVisible(self,83,False)
                     cSetVisible(self,85,False)
                     cSetVisible(self,86,False)
                     cSetVisible(self,89,False)
                     cSetVisible(self,54,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)


                 if speedtest_yellow:
                     cSetVisible(self,52,False)
                     cSetVisible(self,53,True)
                     cSetVisible(self,47,False)
                     cSetVisible(self,46,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,32,False)
                     cSetVisible(self,34,False)
                     cSetVisible(self,36,False)
                     cSetVisible(self,39,False)
                     cSetVisible(self,41,False)
                     cSetVisible(self,43,False)
                     cSetVisible(self,44,False)
                     cSetVisible(self,75,False)
                     cSetVisible(self,77,False)
                     cSetVisible(self,79,False)
                     cSetVisible(self,81,False)
                     cSetVisible(self,83,False)
                     cSetVisible(self,85,False)
                     cSetVisible(self,87,False)
                     cSetVisible(self,88,False)
                     cSetVisible(self,54,True)
                     cSetVisible(self,57,True)
                     cSetVisible(self,59,True)
                     cSetVisible(self,61,True)
                     cSetVisible(self,63,True)
                     cSetVisible(self,65,True)
                     cSetVisible(self,67,True)
                     cSetVisible(self,69,True)
                     cSetVisible(self,71,True)
                     cSetVisible(self,73,True)



             if changelanguage_enabled:
                 if english_enabled:
                     if englishblck_enabled == True:
                         self.getControl(118).setVisible(False)
                         self.getControl(120).setVisible(True)
                     elif frenchblck_enabled == True:
                         self.getControl(120).setVisible(False)
                         self.getControl(122).setVisible(True)
                     elif germanblck_enabled == True:
                         self.getControl(122).setVisible(False)
                         self.getControl(124).setVisible(True)
                     elif italianblck_enabled == True:
                         self.getControl(124).setVisible(False)
                         self.getControl(126).setVisible(True)
                     elif spainishblck_enabled == True:
                         self.getControl(126).setVisible(False)
                         self.getControl(128).setVisible(True)
                     elif russianblck_enabled == True:
                         self.getControl(128).setVisible(False)
                         self.getControl(130).setVisible(True)
                     elif portugueseblck_enabled == True:
                         self.getControl(130).setVisible(False)
                         self.getControl(132).setVisible(True)
                     elif greekblck_enabled == True:
                         self.getControl(132).setVisible(False)
                         self.getControl(134).setVisible(True)
                     elif dutchblck_enabled == True:
                         self.getControl(134).setVisible(False)
                         self.getControl(136).setVisible(True)
                     elif chineseblck_enabled == True:
                         self.getControl(136).setVisible(False)
                         self.getControl(138).setVisible(True)
                     elif koreanblck_enabled == True:
                         self.getControl(138).setVisible(False)
                         self.getControl(140).setVisible(True)
                     elif arabicblck_enabled == True:
                         self.getControl(140).setVisible(False)
                         self.getControl(118).setVisible(True)



         if action == ACTION_MOVE_UP:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,11,False)
                     cSetVisible(self,10,True)
                     cSetVisible(self,29,False)
                     cSetVisible(self,28,True)


                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,55,True)
                         cSetVisible(self,73,False)
                         cSetVisible(self,72,True)


                 if entertainment_yellow:
                     cSetVisible(self,12,False)
                     cSetVisible(self,13,True)
                     cSetVisible(self,10,False)
                     cSetVisible(self,11,True)


                     if english_enabled:
                         cSetVisible(self,56,False)
                         cSetVisible(self,57,True)
                         cSetVisible(self,55,False)
                         cSetVisible(self,54,True)


                 if movies_yellow:
                     cSetVisible(self,14,False)
                     cSetVisible(self,15,True)
                     cSetVisible(self,13,False)
                     cSetVisible(self,12,True)


                     if english_enabled:
                         cSetVisible(self,58,False)
                         cSetVisible(self,59,True)
                         cSetVisible(self,57,False)
                         cSetVisible(self,56,True)


                 if kids_yellow:
                     cSetVisible(self,16,False)
                     cSetVisible(self,17,True)
                     cSetVisible(self,15,False)
                     cSetVisible(self,14,True)


                     if english_enabled:
                         cSetVisible(self,60,False)
                         cSetVisible(self,61,True)
                         cSetVisible(self,59,False)
                         cSetVisible(self,58,True)


                 if sports_yellow:
                     cSetVisible(self,18,False)
                     cSetVisible(self,19,True)
                     cSetVisible(self,17,False)
                     cSetVisible(self,16,True)


                     if english_enabled:
                         cSetVisible(self,62,False)
                         cSetVisible(self,63,True)
                         cSetVisible(self,61,False)
                         cSetVisible(self,60,True)


                 if news_yellow:
                     cSetVisible(self,20,False)
                     cSetVisible(self,21,True)
                     cSetVisible(self,19,False)
                     cSetVisible(self,18,True)


                     if english_enabled:
                         cSetVisible(self,64,False)
                         cSetVisible(self,65,True)
                         cSetVisible(self,63,False)
                         cSetVisible(self,62,True)


                 if documentaries_yellow:
                     cSetVisible(self,22,False)
                     cSetVisible(self,23,True)
                     cSetVisible(self,21,False)
                     cSetVisible(self,20,True)


                     if english_enabled:
                         cSetVisible(self,66,False)
                         cSetVisible(self,67,True)
                         cSetVisible(self,65,False)
                         cSetVisible(self,64,True)


                 if musicradio_yellow:
                     cSetVisible(self,24,False)
                     cSetVisible(self,25,True)
                     cSetVisible(self,23,False)
                     cSetVisible(self,22,True)


                         
                     if english_enabled:
                         cSetVisible(self,68,False)
                         cSetVisible(self,69,True)
                         cSetVisible(self,67,False)
                         cSetVisible(self,66,True)


                 if adult_yellow:
                     cSetVisible(self,26,False)
                     cSetVisible(self,27,True)
                     cSetVisible(self,25,False)
                     cSetVisible(self,24,True)


                     if english_enabled:
                         cSetVisible(self,70,False)
                         cSetVisible(self,71,True)
                         cSetVisible(self,69,False)
                         cSetVisible(self,68,True)


                 if favourites_yellow:
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,True)
                     cSetVisible(self,27,False)
                     cSetVisible(self,26,True)


                     if english_enabled:
                         cSetVisible(self,72,False)
                         cSetVisible(self,73,True)
                         cSetVisible(self,71,False)
                         cSetVisible(self,70,True)




             if settings_yellow:
                 if picture_yellow:
                     cSetVisible(self,30,False)
                     cSetVisible(self,31,True)
                     cSetVisible(self,45,False)
                     cSetVisible(self,44,True)
                         
                         
                     if english_enabled:
                         cSetVisible(self,74,False)
                         cSetVisible(self,75,True)
                         cSetVisible(self,89,False)
                         cSetVisible(self,88,True)


                 if sound_yellow:
                     cSetVisible(self,32,False)
                     cSetVisible(self,33,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,30,True)


                     if english_enabled:
                         cSetVisible(self,76,False)
                         cSetVisible(self,77,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,74,True)


                 if changelanguage_yellow:
                     cSetVisible(self,34,False)
                     cSetVisible(self,35,True)
                     cSetVisible(self,33,False)
                     cSetVisible(self,32,True)


                     if english_enabled:
                         cSetVisible(self,78,False)
                         cSetVisible(self,79,True)
                         cSetVisible(self,77,False)
                         cSetVisible(self,76,True)


                 if changepin_yellow:
                     cSetVisible(self,36,False)
                     cSetVisible(self,37,True)
                     cSetVisible(self,35,False)
                     cSetVisible(self,34,True)


                     if english_enabled:
                         cSetVisible(self,80,False)
                         cSetVisible(self,81,True)
                         cSetVisible(self,79,False)
                         cSetVisible(self,78,True)


                 if viewrestrictions_yellow:
                     cSetVisible(self,38,False)
                     cSetVisible(self,39,True)
                     cSetVisible(self,37,False)
                     cSetVisible(self,36,True)


                     if english_enabled:
                         cSetVisible(self,82,False)
                         cSetVisible(self,83,True)
                         cSetVisible(self,81,False)
                         cSetVisible(self,80,True)


                 if removechannels_yellow:
                     cSetVisible(self,40,False)
                     cSetVisible(self,41,True)
                     cSetVisible(self,39,False)
                     cSetVisible(self,38,True)


                     if english_enabled:
                         cSetVisible(self,84,False)
                         cSetVisible(self,85,True)
                         cSetVisible(self,83,False)
                         cSetVisible(self,82,True)


                 if systemdetails_yellow:
                     cSetVisible(self,42,False)
                     cSetVisible(self,43,True)
                     cSetVisible(self,41,False)
                     cSetVisible(self,40,True)


                     if english_enabled:
                         cSetVisible(self,86,False)
                         cSetVisible(self,87,True)
                         cSetVisible(self,85,False)
                         cSetVisible(self,84,True)


                 if speedtest_yellow:
                     cSetVisible(self,44,False)
                     cSetVisible(self,45,True)
                     cSetVisible(self,43,False)
                     cSetVisible(self,42,True)


                     if english_enabled:
                         cSetVisible(self,88,False)
                         cSetVisible(self,89,True)
                         cSetVisible(self,87,False)
                         cSetVisible(self,86,True)



             if changelanguage_enabled:
                 if lang_yellow == True:
                     cSetVisible(self,110,False)
                     cSetVisible(self,111,True)
                     cSetVisible(self,114,False)
                     cSetVisible(self,115,False)
                     cSetVisible(self,116,False)
                     cSetVisible(self,117,True)
                     cSetVisible(self,143,False)
                     cSetVisible(self,142,True)



                     if english_enabled:
                         cSetVisible(self,112,False)
                         cSetVisible(self,113,True)
                         cSetVisible(self,145,False)
                         cSetVisible(self,144,True)


                     if englishblck_enabled:
                         cSetVisible(self,118,False)
                         cSetVisible(self,119,True)

                     if frenchblck_enabled:
                         cSetVisible(self,120,False)
                         cSetVisible(self,121,True)

                     if germanblck_enabled:
                         cSetVisible(self,122,False)
                         cSetVisible(self,123,True)

                     if italianblck_enabled:
                         cSetVisible(self,124,False)
                         cSetVisible(self,125,True)

                     if spainishblck_enabled:
                         cSetVisible(self,126,False)
                         cSetVisible(self,127,True)

                     if russianblck_enabled:
                         cSetVisible(self,128,False)
                         cSetVisible(self,129,True)

                     if portugueseblck_enabled:
                         cSetVisible(self,130,False)
                         cSetVisible(self,131,True)

                     if greekblck_enabled:
                         cSetVisible(self,132,False)
                         cSetVisible(self,133,True)

                     if dutchblck_enabled:
                         cSetVisible(self,134,False)
                         cSetVisible(self,135,True)

                     if chineseblck_enabled:
                         cSetVisible(self,136,False)
                         cSetVisible(self,137,True)

                     if koreanblck_enabled:
                         cSetVisible(self,138,False)
                         cSetVisible(self,139,True)

                     if arabicblck_enabled:
                         cSetVisible(self,140,False)
                         cSetVisible(self,141,True)



                 elif lang_blue == True:
                     cSetVisible(self,142,False)
                     cSetVisible(self,143,True)
                     cSetVisible(self,111,False)
                     cSetVisible(self,110,True)
                     cSetVisible(self,114,True)
                     cSetVisible(self,115,True)
                     cSetVisible(self,117,False)
                     cSetVisible(self,116,True)



                     if english_enabled:
                         cSetVisible(self,113,False)
                         cSetVisible(self,112,True)
                         cSetVisible(self,144,False)
                         cSetVisible(self,145,True)


                         if englishwhte_enabled:
                             cSetVisible(self,119,False)
                             cSetVisible(self,118,True)

                         if frenchwhte_enabled:
                             cSetVisible(self,121,False)
                             cSetVisible(self,120,True)

                         if germanwhte_enabled:
                             cSetVisible(self,123,False)
                             cSetVisible(self,122,True)

                         if italianwhte_enabled:
                             cSetVisible(self,125,False)
                             cSetVisible(self,124,True)

                         if spainishwhte_enabled:
                             cSetVisible(self,127,False)
                             cSetVisible(self,126,True)

                         if russianwhte_enabled:
                             cSetVisible(self,129,False)
                             cSetVisible(self,128,True)

                         if portuguesewhte_enabled:
                             cSetVisible(self,131,False)
                             cSetVisible(self,130,True)

                         if greekwhte_enabled:
                             cSetVisible(self,133,False)
                             cSetVisible(self,132,True)

                         if dutchwhte_enabled:
                             cSetVisible(self,135,False)
                             cSetVisible(self,134,True)

                         if chinesewhte_enabled:
                             cSetVisible(self,137,False)
                             cSetVisible(self,136,True)

                         if koreanwhte_enabled:
                             cSetVisible(self,139,False)
                             cSetVisible(self,138,True)

                         if arabicwhte_enabled:
                             cSetVisible(self,141,False)
                             cSetVisible(self,140,True)




         if action == ACTION_MOVE_DOWN:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,11,False)
                     cSetVisible(self,10,True)
                     cSetVisible(self,13,False)
                     cSetVisible(self,12,True)


                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,55,True)
                         cSetVisible(self,57,False)
                         cSetVisible(self,56,True)



                 if entertainment_yellow:
                     cSetVisible(self,12,False)
                     cSetVisible(self,13,True)
                     cSetVisible(self,15,False)
                     cSetVisible(self,14,True)


                     if english_enabled:
                         cSetVisible(self,56,False)
                         cSetVisible(self,57,True)
                         cSetVisible(self,59,False)
                         cSetVisible(self,58,True)



                 if movies_yellow:
                     cSetVisible(self,14,False)
                     cSetVisible(self,15,True)
                     cSetVisible(self,17,False)
                     cSetVisible(self,16,True)


                     if english_enabled:
                         cSetVisible(self,58,False)
                         cSetVisible(self,59,True)
                         cSetVisible(self,61,False)
                         cSetVisible(self,60,True)



                 if kids_yellow:
                     cSetVisible(self,16,False)
                     cSetVisible(self,17,True)
                     cSetVisible(self,19,False)
                     cSetVisible(self,18,True)


                     if english_enabled:
                         cSetVisible(self,60,False)
                         cSetVisible(self,61,True)
                         cSetVisible(self,63,False)
                         cSetVisible(self,62,True)



                 if sports_yellow:
                     cSetVisible(self,18,False)
                     cSetVisible(self,19,True)
                     cSetVisible(self,21,False)
                     cSetVisible(self,20,True)


                     if english_enabled:
                         cSetVisible(self,62,False)
                         cSetVisible(self,63,True)
                         cSetVisible(self,65,False)
                         cSetVisible(self,64,True)




                 if news_yellow:
                     cSetVisible(self,20,False)
                     cSetVisible(self,21,True)
                     cSetVisible(self,23,False)
                     cSetVisible(self,22,True)


                     if english_enabled:
                         cSetVisible(self,64,False)
                         cSetVisible(self,65,True)
                         cSetVisible(self,67,False)
                         cSetVisible(self,66,True)



                 if documentaries_yellow:
                     cSetVisible(self,22,False)
                     cSetVisible(self,23,True)
                     cSetVisible(self,25,False)
                     cSetVisible(self,24,True)


                     if english_enabled:
                         cSetVisible(self,66,False)
                         cSetVisible(self,67,True)
                         cSetVisible(self,69,False)
                         cSetVisible(self,68,True)



                 if musicradio_yellow:
                     cSetVisible(self,24,False)
                     cSetVisible(self,25,True)
                     cSetVisible(self,27,False)
                     cSetVisible(self,26,True)


                     if english_enabled:
                         cSetVisible(self,68,False)
                         cSetVisible(self,69,True)
                         cSetVisible(self,71,False)
                         cSetVisible(self,70,True)



                 if adult_yellow:
                     cSetVisible(self,26,False)
                     cSetVisible(self,27,True)
                     cSetVisible(self,29,False)
                     cSetVisible(self,28,True)


                     if english_enabled:
                         cSetVisible(self,70,False)
                         cSetVisible(self,71,True)
                         cSetVisible(self,73,False)
                         cSetVisible(self,72,True)



                 if favourites_yellow:
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,True)
                     cSetVisible(self,10,False)
                     cSetVisible(self,11,True)


                     if english_enabled:
                         cSetVisible(self,72,False)
                         cSetVisible(self,73,True)
                         cSetVisible(self,55,False)
                         cSetVisible(self,54,True)





             if settings_yellow:
                 if picture_yellow:
                     cSetVisible(self,30,False)
                     cSetVisible(self,31,True)
                     cSetVisible(self,33,False)
                     cSetVisible(self,32,True)


                     if english_enabled:
                         cSetVisible(self,74,False)
                         cSetVisible(self,75,True)
                         cSetVisible(self,77,False)
                         cSetVisible(self,76,True)


                 if sound_yellow:
                     cSetVisible(self,32,False)
                     cSetVisible(self,33,True)
                     cSetVisible(self,35,False)
                     cSetVisible(self,34,True)


                     if english_enabled:
                         cSetVisible(self,76,False)
                         cSetVisible(self,77,True)
                         cSetVisible(self,79,False)
                         cSetVisible(self,78,True)



                 if changelanguage_yellow:
                     cSetVisible(self,34,False)
                     cSetVisible(self,35,True)
                     cSetVisible(self,37,False)
                     cSetVisible(self,36,True)


                     if english_enabled:
                         cSetVisible(self,78,False)
                         cSetVisible(self,79,True)
                         cSetVisible(self,81,False)
                         cSetVisible(self,80,True)



                 if changepin_yellow:
                     cSetVisible(self,36,False)
                     cSetVisible(self,37,True)
                     cSetVisible(self,39,False)
                     cSetVisible(self,38,True)


                     if english_enabled:
                         cSetVisible(self,80,False)
                         cSetVisible(self,81,True)
                         cSetVisible(self,83,False)
                         cSetVisible(self,82,True)



                 if viewrestrictions_yellow:
                     cSetVisible(self,38,False)
                     cSetVisible(self,39,True)
                     cSetVisible(self,41,False)
                     cSetVisible(self,40,True)


                     if english_enabled:
                         cSetVisible(self,82,False)
                         cSetVisible(self,83,True)
                         cSetVisible(self,85,False)
                         cSetVisible(self,84,True)



                 if removechannels_yellow:
                     cSetVisible(self,40,False)
                     cSetVisible(self,41,True)
                     cSetVisible(self,43,False)
                     cSetVisible(self,42,True)


                     if english_enabled:
                         cSetVisible(self,84,False)
                         cSetVisible(self,85,True)
                         cSetVisible(self,87,False)
                         cSetVisible(self,86,True)



                 if systemdetails_yellow:
                     cSetVisible(self,42,False)
                     cSetVisible(self,43,True)
                     cSetVisible(self,45,False)
                     cSetVisible(self,44,True)


                     if english_enabled:
                         cSetVisible(self,86,False)
                         cSetVisible(self,87,True)
                         cSetVisible(self,89,False)
                         cSetVisible(self,88,True)



                 if speedtest_yellow:
                     cSetVisible(self,44,False)
                     cSetVisible(self,45,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,30,True)


                     if english_enabled:
                         cSetVisible(self,88,False)
                         cSetVisible(self,89,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,74,True)



             if changelanguage_enabled:
                 if lang_yellow == True:
                     cSetVisible(self,110,False)
                     cSetVisible(self,111,True)
                     cSetVisible(self,114,False)
                     cSetVisible(self,115,False)
                     cSetVisible(self,116,False)
                     cSetVisible(self,117,True)
                     cSetVisible(self,143,False)
                     cSetVisible(self,142,True)



                     if english_enabled:
                         cSetVisible(self,112,False)
                         cSetVisible(self,113,True)
                         cSetVisible(self,145,False)
                         cSetVisible(self,144,True)
                     
                     
                     if englishblck_enabled:
                         cSetVisible(self,118,False)
                         cSetVisible(self,119,True)

                     if frenchblck_enabled:
                         cSetVisible(self,120,False)
                         cSetVisible(self,121,True)

                     if germanblck_enabled:
                         cSetVisible(self,122,False)
                         cSetVisible(self,123,True)

                     if italianblck_enabled:
                         cSetVisible(self,124,False)
                         cSetVisible(self,125,True)

                     if spainishblck_enabled:
                         cSetVisible(self,126,False)
                         cSetVisible(self,127,True)

                     if russianblck_enabled:
                         cSetVisible(self,128,False)
                         cSetVisible(self,129,True)

                     if portugueseblck_enabled:
                         cSetVisible(self,130,False)
                         cSetVisible(self,131,True)

                     if greekblck_enabled:
                         cSetVisible(self,132,False)
                         cSetVisible(self,133,True)

                     if dutchblck_enabled:
                         cSetVisible(self,134,False)
                         cSetVisible(self,135,True)

                     if chineseblck_enabled:
                         cSetVisible(self,136,False)
                         cSetVisible(self,137,True)

                     if koreanblck_enabled:
                         cSetVisible(self,138,False)
                         cSetVisible(self,139,True)

                     if arabicblck_enabled:
                         cSetVisible(self,140,False)
                         cSetVisible(self,141,True)



                 elif lang_blue == True:
                     cSetVisible(self,142,False)
                     cSetVisible(self,143,True)
                     cSetVisible(self,111,False)
                     cSetVisible(self,110,True)
                     cSetVisible(self,114,True)
                     cSetVisible(self,115,True)
                     cSetVisible(self,117,False)
                     cSetVisible(self,116,True)



                     if english_enabled:
                         cSetVisible(self,113,False)
                         cSetVisible(self,112,True)
                         cSetVisible(self,144,False)
                         cSetVisible(self,145,True)


                         if englishwhte_enabled:
                             cSetVisible(self,119,False)
                             cSetVisible(self,118,True)

                         if frenchwhte_enabled:
                             cSetVisible(self,121,False)
                             cSetVisible(self,120,True)

                         if germanwhte_enabled:
                             cSetVisible(self,123,False)
                             cSetVisible(self,122,True)

                         if italianwhte_enabled:
                             cSetVisible(self,125,False)
                             cSetVisible(self,124,True)

                         if spainishwhte_enabled:
                             cSetVisible(self,127,False)
                             cSetVisible(self,126,True)

                         if russianwhte_enabled:
                             cSetVisible(self,129,False)
                             cSetVisible(self,128,True)

                         if portuguesewhte_enabled:
                             cSetVisible(self,131,False)
                             cSetVisible(self,130,True)

                         if greekwhte_enabled:
                             cSetVisible(self,133,False)
                             cSetVisible(self,132,True)

                         if dutchwhte_enabled:
                             cSetVisible(self,135,False)
                             cSetVisible(self,134,True)

                         if chinesewhte_enabled:
                             cSetVisible(self,137,False)
                             cSetVisible(self,136,True)

                         if koreanwhte_enabled:
                             cSetVisible(self,139,False)
                             cSetVisible(self,138,True)

                         if arabicwhte_enabled:
                             cSetVisible(self,141,False)
                             cSetVisible(self,140,True)




         if action == ACTION_NUMBER1:
             if tvguide_yellow:
                 if allchannels_yellow:
                     pass


                 elif entertainment_yellow:
                     cSetVisible(self,10,False)
                     cSetVisible(self,11,True)
                     cSetVisible(self,12,False)
                     cSetVisible(self,13,True)


                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,56,False)
                         cSetVisible(self,57,True)


                 elif movies_yellow:
                     cSetVisible(self,10,False)
                     cSetVisible(self,11,True)
                     cSetVisible(self,14,False)
                     cSetVisible(self,15,True)


                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,58,False)
                         cSetVisible(self,59,True)


                 elif kids_yellow:
                     cSetVisible(self,10,False)
                     cSetVisible(self,11,True)
                     cSetVisible(self,16,False)
                     cSetVisible(self,17,True)


                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,60,False)
                         cSetVisible(self,61,True)


                 elif sports_yellow:
                     cSetVisible(self,10,False)
                     cSetVisible(self,11,True)
                     cSetVisible(self,18,False)
                     cSetVisible(self,19,True)


                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,62,False)
                         cSetVisible(self,63,True)


                 elif news_yellow:
                     cSetVisible(self,10,False)
                     cSetVisible(self,11,True)
                     cSetVisible(self,20,False)
                     cSetVisible(self,21,True)


                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,64,False)
                         cSetVisible(self,65,True)


                 elif documentaries_yellow:
                     cSetVisible(self,10,False)
                     cSetVisible(self,11,True)
                     cSetVisible(self,22,False)
                     cSetVisible(self,23,True)


                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,66,False)
                         cSetVisible(self,67,True)


                 elif musicradio_yellow:
                     cSetVisible(self,10,False)
                     cSetVisible(self,11,True)
                     cSetVisible(self,24,False)
                     cSetVisible(self,25,True)


                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,68,False)
                         cSetVisible(self,69,True)
                     
                     
                 elif adult_yellow:
                     cSetVisible(self,10,False)
                     cSetVisible(self,11,True)
                     cSetVisible(self,26,False)
                     cSetVisible(self,27,True)


                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,70,False)
                         cSetVisible(self,71,True)


                 elif favourites_yellow:
                     cSetVisible(self,10,False)
                     cSetVisible(self,11,True)
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,True)


                     if english_enabled:
                         cSetVisible(self,55,False)
                         cSetVisible(self,54,True)
                         cSetVisible(self,72,False)
                         cSetVisible(self,73,True)




             elif settings_yellow:
                 if picture_yellow:
                     pass
                 elif sound_yellow:
                     cSetVisible(self,32,False)
                     cSetVisible(self,33,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,30,True)

                     if english_enabled:
                         cSetVisible(self,76,False)
                         cSetVisible(self,77,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,74,True)



                 elif changelanguage_yellow:
                     cSetVisible(self,34,False)
                     cSetVisible(self,35,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,30,True)

                     if english_enabled:
                         cSetVisible(self,78,False)
                         cSetVisible(self,79,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,74,True)


                 elif changepin_yellow:
                     cSetVisible(self,36,False)
                     cSetVisible(self,37,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,30,True)

                     if english_enabled:
                         cSetVisible(self,80,False)
                         cSetVisible(self,81,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,74,True)


                 elif viewrestrictions_yellow:
                     cSetVisible(self,38,False)
                     cSetVisible(self,39,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,30,True)

                     if english_enabled:
                         cSetVisible(self,82,False)
                         cSetVisible(self,83,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,74,True)


                 elif removechannels_yellow:
                     cSetVisible(self,40,False)
                     cSetVisible(self,41,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,30,True)

                     if english_enabled:
                         cSetVisible(self,84,False)
                         cSetVisible(self,85,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,74,True)
                         
                         
                 elif systemdetails_yellow:
                     cSetVisible(self,42,False)
                     cSetVisible(self,43,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,30,True)

                     if english_enabled:
                         cSetVisible(self,86,False)
                         cSetVisible(self,87,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,74,True)


                 elif speedtest_yellow:
                     cSetVisible(self,44,False)
                     cSetVisible(self,45,True)
                     cSetVisible(self,31,False)
                     cSetVisible(self,30,True)

                     if english_enabled:
                         cSetVisible(self,88,False)
                         cSetVisible(self,89,True)
                         cSetVisible(self,75,False)
                         cSetVisible(self,74,True)




             elif changepin_enabled:
                 if PIN_1_enabled:
                     if PIN_1_enabled == True:
                         cSetVisible(self,4009,False)
                         cSetVisible(self,4013,True)
                     elif PIN_1_enabled == False:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)


                 elif PIN_2_enabled:
                     if PIN_2_enabled == True:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                     elif PIN_2_enabled == False:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)


                 elif PIN_3_enabled:
                     if PIN_3_enabled == True:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                     elif PIN_3_enabled == False:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)


                 elif PIN_4_enabled:
                     if PIN_4_enabled == True:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                     elif PIN_4_enabled == False:
                         pass




         if action == ACTION_NUMBER2:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,11,False)
                     cSetVisible(self,10,True)
                     cSetVisible(self,13,False)
                     cSetVisible(self,12,True)


                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,55,True)
                         cSetVisible(self,57,False)
                         cSetVisible(self,56,True)


                 elif entertainment_yellow:
                     pass


                 elif movies_yellow:
                     cSetVisible(self,14,False)
                     cSetVisible(self,15,True)
                     cSetVisible(self,13,False)
                     cSetVisible(self,12,True)


                     if english_enabled:
                         cSetVisible(self,58,False)
                         cSetVisible(self,59,True)
                         cSetVisible(self,57,False)
                         cSetVisible(self,56,True)


                 elif kids_yellow:
                     cSetVisible(self,16,False)
                     cSetVisible(self,17,True)
                     cSetVisible(self,13,False)
                     cSetVisible(self,12,True)


                     if english_enabled:
                         cSetVisible(self,60,False)
                         cSetVisible(self,61,True)
                         cSetVisible(self,57,False)
                         cSetVisible(self,56,True)


                 elif sports_yellow:
                     cSetVisible(self,18,False)
                     cSetVisible(self,19,True)
                     cSetVisible(self,13,False)
                     cSetVisible(self,12,True)


                     if english_enabled:
                         cSetVisible(self,62,False)
                         cSetVisible(self,63,True)
                         cSetVisible(self,57,False)
                         cSetVisible(self,56,True)


                 elif news_yellow:
                     cSetVisible(self,20,False)
                     cSetVisible(self,21,True)
                     cSetVisible(self,13,False)
                     cSetVisible(self,12,True)


                     if english_enabled:
                         cSetVisible(self,64,False)
                         cSetVisible(self,65,True)
                         cSetVisible(self,57,False)
                         cSetVisible(self,56,True)


                 elif documentaries_yellow:
                     cSetVisible(self,22,False)
                     cSetVisible(self,23,True)
                     cSetVisible(self,13,False)
                     cSetVisible(self,12,True)


                     if english_enabled:
                         cSetVisible(self,66,False)
                         cSetVisible(self,67,True)
                         cSetVisible(self,57,False)
                         cSetVisible(self,56,True)


                 elif musicradio_yellow:
                     cSetVisible(self,24,False)
                     cSetVisible(self,25,True)
                     cSetVisible(self,13,False)
                     cSetVisible(self,12,True)


                     if english_enabled:
                         cSetVisible(self,68,False)
                         cSetVisible(self,69,True)
                         cSetVisible(self,57,False)
                         cSetVisible(self,56,True)


                 elif adult_yellow:
                     cSetVisible(self,26,False)
                     cSetVisible(self,27,True)
                     cSetVisible(self,13,False)
                     cSetVisible(self,12,True)


                     if english_enabled:
                         cSetVisible(self,70,False)
                         cSetVisible(self,71,True)
                         cSetVisible(self,57,False)
                         cSetVisible(self,56,True)


                 elif favourites_yellow:
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,True)
                     cSetVisible(self,13,False)
                     cSetVisible(self,12,True)


                     if english_enabled:
                         cSetVisible(self,72,False)
                         cSetVisible(self,73,True)
                         cSetVisible(self,57,False)
                         cSetVisible(self,56,True)




             elif settings_yellow:
                 if picture_yellow:
                     cSetVisible(self,30,False)
                     cSetVisible(self,31,True)
                     cSetVisible(self,33,False)
                     cSetVisible(self,32,True)

                     if english_enabled:
                         cSetVisible(self,74,False)
                         cSetVisible(self,75,True)
                         cSetVisible(self,77,False)
                         cSetVisible(self,76,True)


                 elif sound_yellow:
                     pass


                 elif changelanguage_yellow:
                     cSetVisible(self,34,False)
                     cSetVisible(self,35,True)
                     cSetVisible(self,33,False)
                     cSetVisible(self,32,True)

                     if english_enabled:
                         cSetVisible(self,78,False)
                         cSetVisible(self,79,True)
                         cSetVisible(self,77,False)
                         cSetVisible(self,76,True)


                 elif changepin_yellow:
                     cSetVisible(self,36,False)
                     cSetVisible(self,37,True)
                     cSetVisible(self,33,False)
                     cSetVisible(self,32,True)

                     if english_enabled:
                         cSetVisible(self,80,False)
                         cSetVisible(self,81,True)
                         cSetVisible(self,77,False)
                         cSetVisible(self,76,True)


                 elif viewrestrictions_yellow:
                     cSetVisible(self,38,False)
                     cSetVisible(self,39,True)
                     cSetVisible(self,33,False)
                     cSetVisible(self,32,True)

                     if english_enabled:
                         cSetVisible(self,82,False)
                         cSetVisible(self,83,True)
                         cSetVisible(self,77,False)
                         cSetVisible(self,76,True)


                 elif removechannels_yellow:
                     cSetVisible(self,40,False)
                     cSetVisible(self,41,True)
                     cSetVisible(self,33,False)
                     cSetVisible(self,32,True)

                     if english_enabled:
                         cSetVisible(self,84,False)
                         cSetVisible(self,85,True)
                         cSetVisible(self,77,False)
                         cSetVisible(self,76,True)


                 elif systemdetails_yellow:
                     cSetVisible(self,42,False)
                     cSetVisible(self,43,True)
                     cSetVisible(self,33,False)
                     cSetVisible(self,32,True)

                     if english_enabled:
                         cSetVisible(self,86,False)
                         cSetVisible(self,87,True)
                         cSetVisible(self,77,False)
                         cSetVisible(self,76,True)


                 elif speedtest_yellow:
                     cSetVisible(self,44,False)
                     cSetVisible(self,45,True)
                     cSetVisible(self,33,False)
                     cSetVisible(self,32,True)

                     if english_enabled:
                         cSetVisible(self,88,False)
                         cSetVisible(self,89,True)
                         cSetVisible(self,77,False)
                         cSetVisible(self,76,True)




             elif changepin_enabled:
                 if PIN_1_enabled:
                     if PIN_1_enabled == True:
                         cSetVisible(self,4009,False)
                         cSetVisible(self,4013,True)
                     elif PIN_1_enabled == False:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                 elif PIN_2_enabled:
                     if PIN_2_enabled == True:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                     elif PIN_2_enabled == False:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                 elif PIN_3_enabled:
                     if PIN_3_enabled == True:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                     elif PIN_3_enabled == False:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                 elif PIN_4_enabled:
                     if PIN_4_enabled == True:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                     elif PIN_4_enabled == False:
                         pass




         if action == ACTION_NUMBER3:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,11,False)
                     cSetVisible(self,10,True)
                     cSetVisible(self,15,False)
                     cSetVisible(self,14,True)


                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,55,True)
                         cSetVisible(self,59,False)
                         cSetVisible(self,58,True)


                 elif entertainment_yellow:
                     cSetVisible(self,12,False)
                     cSetVisible(self,13,True)
                     cSetVisible(self,15,False)
                     cSetVisible(self,14,True)
                     ADDON.setSetting('movies.enabled', 'true')


                     if english_enabled:
                         cSetVisible(self,56,False)
                         cSetVisible(self,57,True)
                         cSetVisible(self,59,False)
                         cSetVisible(self,58,True)


                 elif movies_yellow:
                     pass


                 elif kids_yellow:
                     cSetVisible(self,16,False)
                     cSetVisible(self,17,True)
                     cSetVisible(self,15,False)
                     cSetVisible(self,14,True)


                     if english_enabled:
                         cSetVisible(self,60,False)
                         cSetVisible(self,61,True)
                         cSetVisible(self,59,False)
                         cSetVisible(self,58,True)


                 elif sports_yellow:
                     cSetVisible(self,18,False)
                     cSetVisible(self,19,True)
                     cSetVisible(self,15,False)
                     cSetVisible(self,14,True)


                     if english_enabled:
                         cSetVisible(self,62,False)
                         cSetVisible(self,63,True)
                         cSetVisible(self,59,False)
                         cSetVisible(self,58,True)


                 elif news_yellow:
                     cSetVisible(self,20,False)
                     cSetVisible(self,21,True)
                     cSetVisible(self,15,False)
                     cSetVisible(self,14,True)


                     if english_enabled:
                         cSetVisible(self,64,False)
                         cSetVisible(self,65,True)
                         cSetVisible(self,59,False)
                         cSetVisible(self,58,True)


                 elif documentaries_yellow:
                     cSetVisible(self,22,False)
                     cSetVisible(self,23,True)
                     cSetVisible(self,15,False)
                     cSetVisible(self,14,True)


                     if english_enabled:
                         cSetVisible(self,66,False)
                         cSetVisible(self,67,True)
                         cSetVisible(self,59,False)
                         cSetVisible(self,58,True)


                 elif musicradio_yellow:
                     cSetVisible(self,24,False)
                     cSetVisible(self,25,True)
                     cSetVisible(self,15,False)
                     cSetVisible(self,14,True)


                     if english_enabled:
                         cSetVisible(self,68,False)
                         cSetVisible(self,69,True)
                         cSetVisible(self,59,False)
                         cSetVisible(self,58,True)


                 elif adult_yellow:
                     cSetVisible(self,26,False)
                     cSetVisible(self,27,True)
                     cSetVisible(self,15,False)
                     cSetVisible(self,14,True)


                     if english_enabled:
                         cSetVisible(self,70,False)
                         cSetVisible(self,71,True)
                         cSetVisible(self,59,False)
                         cSetVisible(self,58,True)


                 elif favourites_yellow:
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,True)
                     cSetVisible(self,15,False)
                     cSetVisible(self,14,True)


                     if english_enabled:
                         cSetVisible(self,72,False)
                         cSetVisible(self,73,True)
                         cSetVisible(self,59,False)
                         cSetVisible(self,58,True)



             elif settings_yellow:
                 if picture_yellow:
                     cSetVisible(self,30,False)
                     cSetVisible(self,31,True)
                     cSetVisible(self,35,False)
                     cSetVisible(self,34,True)

                     if english_enabled:
                         cSetVisible(self,74,False)
                         cSetVisible(self,75,True)
                         cSetVisible(self,79,False)
                         cSetVisible(self,78,True)


                 elif sound_yellow:
                     cSetVisible(self,32,False)
                     cSetVisible(self,33,True)
                     cSetVisible(self,35,False)
                     cSetVisible(self,34,True)

                     if english_enabled:
                         cSetVisible(self,76,False)
                         cSetVisible(self,77,True)
                         cSetVisible(self,79,False)
                         cSetVisible(self,78,True)


                 elif changelanguage_yellow:
                     pass


                 elif changepin_yellow:
                     cSetVisible(self,36,False)
                     cSetVisible(self,37,True)
                     cSetVisible(self,35,False)
                     cSetVisible(self,34,True)

                     if english_enabled:
                         cSetVisible(self,80,False)
                         cSetVisible(self,81,True)
                         cSetVisible(self,79,False)
                         cSetVisible(self,78,True)


                 elif viewrestrictions_yellow:
                     cSetVisible(self,38,False)
                     cSetVisible(self,39,True)
                     cSetVisible(self,35,False)
                     cSetVisible(self,34,True)

                     if english_enabled:
                         cSetVisible(self,82,False)
                         cSetVisible(self,83,True)
                         cSetVisible(self,79,False)
                         cSetVisible(self,78,True)


                 elif removechannels_yellow:
                     cSetVisible(self,40,False)
                     cSetVisible(self,41,True)
                     cSetVisible(self,35,False)
                     cSetVisible(self,34,True)

                     if english_enabled:
                         cSetVisible(self,84,False)
                         cSetVisible(self,85,True)
                         cSetVisible(self,79,False)
                         cSetVisible(self,78,True)


                 elif systemdetails_yellow:
                     cSetVisible(self,42,False)
                     cSetVisible(self,43,True)
                     cSetVisible(self,35,False)
                     cSetVisible(self,34,True)

                     if english_enabled:
                         cSetVisible(self,86,False)
                         cSetVisible(self,87,True)
                         cSetVisible(self,79,False)
                         cSetVisible(self,78,True)


                 elif speedtest_yellow:
                     cSetVisible(self,44,False)
                     cSetVisible(self,45,True)
                     cSetVisible(self,35,False)
                     cSetVisible(self,34,True)

                     if english_enabled:
                         cSetVisible(self,88,False)
                         cSetVisible(self,89,True)
                         cSetVisible(self,79,False)
                         cSetVisible(self,78,True)




             elif changepin_enabled:
                 if PIN_1_enabled:
                     if PIN_1_enabled == True:
                         cSetVisible(self,4009,False)
                         cSetVisible(self,4013,True)
                     elif PIN_1_enabled == False:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                 elif PIN_2_enabled:
                     if PIN_2_enabled == True:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                     elif PIN_2_enabled == False:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                 elif PIN_3_enabled:
                     if PIN_3_enabled == True:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                     elif PIN_3_enabled == False:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                 elif PIN_4_enabled:
                     if PIN_4_enabled == True:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                     elif PIN_4_enabled == False:
                         pass




         if action == ACTION_NUMBER4:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,11,False)
                     cSetVisible(self,10,True)
                     cSetVisible(self,17,False)
                     cSetVisible(self,16,True)


                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,55,True)
                         cSetVisible(self,61,False)
                         cSetVisible(self,60,True)


                 elif entertainment_yellow:
                     cSetVisible(self,12,False)
                     cSetVisible(self,13,True)
                     cSetVisible(self,17,False)
                     cSetVisible(self,16,True)


                     if english_enabled:
                         cSetVisible(self,56,False)
                         cSetVisible(self,57,True)
                         cSetVisible(self,61,False)
                         cSetVisible(self,60,True)


                 elif movies_yellow:
                     cSetVisible(self,14,False)
                     cSetVisible(self,15,True)
                     cSetVisible(self,17,False)
                     cSetVisible(self,16,True)


                     if english_enabled:
                         cSetVisible(self,58,False)
                         cSetVisible(self,59,True)
                         cSetVisible(self,61,False)
                         cSetVisible(self,60,True)


                 elif kids_yellow:
                     pass


                 elif sports_yellow:
                     cSetVisible(self,18,False)
                     cSetVisible(self,19,True)
                     cSetVisible(self,17,False)
                     cSetVisible(self,16,True)


                     if english_enabled:
                         cSetVisible(self,62,False)
                         cSetVisible(self,63,True)
                         cSetVisible(self,61,False)
                         cSetVisible(self,60,True)


                 elif news_yellow:
                     cSetVisible(self,20,False)
                     cSetVisible(self,21,True)
                     cSetVisible(self,17,False)
                     cSetVisible(self,16,True)


                     if english_enabled:
                         cSetVisible(self,64,False)
                         cSetVisible(self,65,True)
                         cSetVisible(self,61,False)
                         cSetVisible(self,60,True)


                 elif documentaries_yellow:
                     cSetVisible(self,22,False)
                     cSetVisible(self,23,True)
                     cSetVisible(self,17,False)
                     cSetVisible(self,16,True)


                     if english_enabled:
                         cSetVisible(self,66,False)
                         cSetVisible(self,67,True)
                         cSetVisible(self,61,False)
                         cSetVisible(self,60,True)


                 elif musicradio_yellow:
                     cSetVisible(self,24,False)
                     cSetVisible(self,25,True)
                     cSetVisible(self,17,False)
                     cSetVisible(self,16,True)


                     if english_enabled:
                         cSetVisible(self,68,False)
                         cSetVisible(self,69,True)
                         cSetVisible(self,61,False)
                         cSetVisible(self,60,True)


                 elif adult_yellow:
                     cSetVisible(self,26,False)
                     cSetVisible(self,27,True)
                     cSetVisible(self,17,False)
                     cSetVisible(self,16,True)


                     if english_enabled:
                         cSetVisible(self,70,False)
                         cSetVisible(self,71,True)
                         cSetVisible(self,61,False)
                         cSetVisible(self,60,True)


                 elif favourites_yellow:
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,True)
                     cSetVisible(self,17,False)
                     cSetVisible(self,16,True)


                     if english_enabled:
                         cSetVisible(self,72,False)
                         cSetVisible(self,73,True)
                         cSetVisible(self,61,False)
                         cSetVisible(self,60,True)




             elif settings_yellow:
                 if picture_yellow:
                     cSetVisible(self,30,False)
                     cSetVisible(self,31,True)
                     cSetVisible(self,37,False)
                     cSetVisible(self,36,True)

                     if english_enabled:
                         cSetVisible(self,74,False)
                         cSetVisible(self,75,True)
                         cSetVisible(self,81,False)
                         cSetVisible(self,80,True)


                 elif sound_yellow:
                     cSetVisible(self,32,False)
                     cSetVisible(self,33,True)
                     cSetVisible(self,37,False)
                     cSetVisible(self,36,True)

                     if english_enabled:
                         cSetVisible(self,76,False)
                         cSetVisible(self,77,True)
                         cSetVisible(self,81,False)
                         cSetVisible(self,80,True)


                 elif changelanguage_yellow:
                     cSetVisible(self,34,False)
                     cSetVisible(self,35,True)
                     cSetVisible(self,37,False)
                     cSetVisible(self,36,True)

                     if english_enabled:
                         cSetVisible(self,78,False)
                         cSetVisible(self,79,True)
                         cSetVisible(self,81,False)
                         cSetVisible(self,80,True)


                 elif changepin_yellow:
                     pass


                 elif viewrestrictions_yellow:
                     cSetVisible(self,38,False)
                     cSetVisible(self,39,True)
                     cSetVisible(self,37,False)
                     cSetVisible(self,36,True)

                     if english_enabled:
                         cSetVisible(self,82,False)
                         cSetVisible(self,83,True)
                         cSetVisible(self,81,False)
                         cSetVisible(self,80,True)


                 elif removechannels_yellow:
                     cSetVisible(self,40,False)
                     cSetVisible(self,41,True)
                     cSetVisible(self,37,False)
                     cSetVisible(self,36,True)

                     if english_enabled:
                         cSetVisible(self,84,False)
                         cSetVisible(self,85,True)
                         cSetVisible(self,81,False)
                         cSetVisible(self,80,True)


                 elif systemdetails_yellow:
                     cSetVisible(self,42,False)
                     cSetVisible(self,43,True)
                     cSetVisible(self,37,False)
                     cSetVisible(self,36,True)

                     if english_enabled:
                         cSetVisible(self,86,False)
                         cSetVisible(self,87,True)
                         cSetVisible(self,81,False)
                         cSetVisible(self,80,True)


                 elif speedtest_yellow:
                     cSetVisible(self,44,False)
                     cSetVisible(self,45,True)
                     cSetVisible(self,37,False)
                     cSetVisible(self,36,True)

                     if english_enabled:
                         cSetVisible(self,88,False)
                         cSetVisible(self,89,True)
                         cSetVisible(self,81,False)
                         cSetVisible(self,80,True)




             elif changepin_enabled:
                 if PIN_1_enabled:
                     if PIN_1_enabled == True:
                         cSetVisible(self,4009,False)
                         cSetVisible(self,4013,True)
                     elif PIN_1_enabled == False:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                 elif PIN_2_enabled:
                     if PIN_2_enabled == True:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                     elif PIN_2_enabled == False:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                 elif PIN_3_enabled:
                     if PIN_3_enabled == True:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                     elif PIN_3_enabled == False:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                 elif PIN_4_enabled:
                     if PIN_4_enabled == True:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                     elif PIN_4_enabled == False:
                         pass




         if action == ACTION_NUMBER5:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,11,False)
                     cSetVisible(self,10,True)
                     cSetVisible(self,19,False)
                     cSetVisible(self,18,True)


                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,55,True)
                         cSetVisible(self,63,False)
                         cSetVisible(self,62,True)


                 elif entertainment_yellow:
                     cSetVisible(self,12,False)
                     cSetVisible(self,13,True)
                     cSetVisible(self,19,False)
                     cSetVisible(self,18,True)


                     if english_enabled:
                         cSetVisible(self,56,False)
                         cSetVisible(self,57,True)
                         cSetVisible(self,63,False)
                         cSetVisible(self,62,True)


                 elif movies_yellow:
                     cSetVisible(self,14,False)
                     cSetVisible(self,15,True)
                     cSetVisible(self,19,False)
                     cSetVisible(self,18,True)


                     if english_enabled:
                         cSetVisible(self,58,False)
                         cSetVisible(self,59,True)
                         cSetVisible(self,63,False)
                         cSetVisible(self,62,True)


                 elif kids_yellow:
                     cSetVisible(self,16,False)
                     cSetVisible(self,17,True)
                     cSetVisible(self,19,False)
                     cSetVisible(self,18,True)


                     if english_enabled:
                         cSetVisible(self,60,False)
                         cSetVisible(self,61,True)
                         cSetVisible(self,63,False)
                         cSetVisible(self,62,True)


                 elif sports_yellow:
                     pass


                 elif news_yellow:
                     cSetVisible(self,20,False)
                     cSetVisible(self,21,True)
                     cSetVisible(self,19,False)
                     cSetVisible(self,18,True)


                     if english_enabled:
                         cSetVisible(self,64,False)
                         cSetVisible(self,65,True)
                         cSetVisible(self,63,False)
                         cSetVisible(self,62,True)


                 elif documentaries_yellow:
                     cSetVisible(self,22,False)
                     cSetVisible(self,23,True)
                     cSetVisible(self,19,False)
                     cSetVisible(self,18,True)


                     if english_enabled:
                         cSetVisible(self,66,False)
                         cSetVisible(self,67,True)
                         cSetVisible(self,63,False)
                         cSetVisible(self,62,True)


                 elif musicradio_yellow:
                     cSetVisible(self,24,False)
                     cSetVisible(self,25,True)
                     cSetVisible(self,19,False)
                     cSetVisible(self,18,True)


                     if english_enabled:
                         cSetVisible(self,68,False)
                         cSetVisible(self,69,True)
                         cSetVisible(self,63,False)
                         cSetVisible(self,62,True)


                 elif adult_yellow:
                     cSetVisible(self,26,False)
                     cSetVisible(self,27,True)
                     cSetVisible(self,19,False)
                     cSetVisible(self,18,True)


                     if english_enabled:
                         cSetVisible(self,70,False)
                         cSetVisible(self,71,True)
                         cSetVisible(self,63,False)
                         cSetVisible(self,62,True)


                 elif favourites_yellow:
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,True)
                     cSetVisible(self,19,False)
                     cSetVisible(self,18,True)


                     if english_enabled:
                         cSetVisible(self,72,False)
                         cSetVisible(self,73,True)
                         cSetVisible(self,63,False)
                         cSetVisible(self,62,True)




             elif settings_yellow:
                 if picture_yellow:
                     cSetVisible(self,30,False)
                     cSetVisible(self,31,True)
                     cSetVisible(self,39,False)
                     cSetVisible(self,38,True)

                     if english_enabled:
                         cSetVisible(self,74,False)
                         cSetVisible(self,75,True)
                         cSetVisible(self,83,False)
                         cSetVisible(self,82,True)


                 elif sound_yellow:
                     cSetVisible(self,32,False)
                     cSetVisible(self,33,True)
                     cSetVisible(self,39,False)
                     cSetVisible(self,38,True)

                     if english_enabled:
                         cSetVisible(self,76,False)
                         cSetVisible(self,77,True)
                         cSetVisible(self,83,False)
                         cSetVisible(self,82,True)


                 elif changelanguage_yellow:
                     cSetVisible(self,34,False)
                     cSetVisible(self,35,True)
                     cSetVisible(self,39,False)
                     cSetVisible(self,38,True)

                     if english_enabled:
                         cSetVisible(self,78,False)
                         cSetVisible(self,79,True)
                         cSetVisible(self,83,False)
                         cSetVisible(self,82,True)


                 elif changepin_yellow:
                     cSetVisible(self,36,False)
                     cSetVisible(self,37,True)
                     cSetVisible(self,39,False)
                     cSetVisible(self,38,True)

                     if english_enabled:
                         cSetVisible(self,80,False)
                         cSetVisible(self,81,True)
                         cSetVisible(self,83,False)
                         cSetVisible(self,82,True)


                 elif viewrestrictions_yellow:
                     pass


                 elif removechannels_yellow:
                     cSetVisible(self,40,False)
                     cSetVisible(self,41,True)
                     cSetVisible(self,39,False)
                     cSetVisible(self,38,True)

                     if english_enabled:
                         cSetVisible(self,84,False)
                         cSetVisible(self,85,True)
                         cSetVisible(self,83,False)
                         cSetVisible(self,82,True)


                 elif systemdetails_yellow:
                     cSetVisible(self,42,False)
                     cSetVisible(self,43,True)
                     cSetVisible(self,39,False)
                     cSetVisible(self,38,True)

                     if english_enabled:
                         cSetVisible(self,86,False)
                         cSetVisible(self,87,True)
                         cSetVisible(self,83,False)
                         cSetVisible(self,82,True)


                 elif speedtest_yellow:
                     cSetVisible(self,44,False)
                     cSetVisible(self,45,True)
                     cSetVisible(self,39,False)
                     cSetVisible(self,38,True)

                     if english_enabled:
                         cSetVisible(self,88,False)
                         cSetVisible(self,89,True)
                         cSetVisible(self,83,False)
                         cSetVisible(self,82,True)




             elif changepin_enabled:
                 if PIN_1_enabled:
                     if PIN_1_enabled == True:
                         cSetVisible(self,4009,False)
                         cSetVisible(self,4013,True)
                     elif PIN_1_enabled == False:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                 elif PIN_2_enabled:
                     if PIN_2_enabled == True:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                     elif PIN_2_enabled == False:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                 elif PIN_3_enabled:
                     if PIN_3_enabled == True:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                     elif PIN_3_enabled == False:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                 elif PIN_4_enabled:
                     if PIN_4_enabled == True:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                     elif PIN_4_enabled == False:
                         pass




         if action == ACTION_NUMBER6:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,11,False)
                     cSetVisible(self,10,True)
                     cSetVisible(self,21,False)
                     cSetVisible(self,20,True)


                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,55,True)
                         cSetVisible(self,65,False)
                         cSetVisible(self,64,True)


                 elif entertainment_yellow:
                     cSetVisible(self,12,False)
                     cSetVisible(self,13,True)
                     cSetVisible(self,21,False)
                     cSetVisible(self,20,True)


                     if english_enabled:
                         cSetVisible(self,56,False)
                         cSetVisible(self,57,True)
                         cSetVisible(self,65,False)
                         cSetVisible(self,64,True)


                 elif movies_yellow:
                     cSetVisible(self,14,False)
                     cSetVisible(self,15,True)
                     cSetVisible(self,21,False)
                     cSetVisible(self,20,True)


                     if english_enabled:
                         cSetVisible(self,58,False)
                         cSetVisible(self,59,True)
                         cSetVisible(self,65,False)
                         cSetVisible(self,64,True)


                 elif kids_yellow:
                     cSetVisible(self,16,False)
                     cSetVisible(self,17,True)
                     cSetVisible(self,21,False)
                     cSetVisible(self,20,True)


                     if english_enabled:
                         cSetVisible(self,60,False)
                         cSetVisible(self,61,True)
                         cSetVisible(self,65,False)
                         cSetVisible(self,64,True)


                 elif sports_yellow:
                     cSetVisible(self,18,False)
                     cSetVisible(self,19,True)
                     cSetVisible(self,21,False)
                     cSetVisible(self,20,True)


                     if english_enabled:
                         cSetVisible(self,62,False)
                         cSetVisible(self,63,True)
                         cSetVisible(self,65,False)
                         cSetVisible(self,64,True)


                 elif news_yellow:
                     pass


                 elif documentaries_yellow:
                     cSetVisible(self,22,False)
                     cSetVisible(self,23,True)
                     cSetVisible(self,21,False)
                     cSetVisible(self,20,True)


                     if english_enabled:
                         cSetVisible(self,66,False)
                         cSetVisible(self,67,True)
                         cSetVisible(self,65,False)
                         cSetVisible(self,64,True)


                 elif musicradio_yellow:
                     cSetVisible(self,24,False)
                     cSetVisible(self,25,True)
                     cSetVisible(self,21,False)
                     cSetVisible(self,20,True)


                     if english_enabled:
                         cSetVisible(self,68,False)
                         cSetVisible(self,69,True)
                         cSetVisible(self,65,False)
                         cSetVisible(self,64,True)


                 elif adult_yellow:
                     cSetVisible(self,26,False)
                     cSetVisible(self,27,True)
                     cSetVisible(self,21,False)
                     cSetVisible(self,20,True)


                     if english_enabled:
                         cSetVisible(self,70,False)
                         cSetVisible(self,71,True)
                         cSetVisible(self,65,False)
                         cSetVisible(self,64,True)


                 elif favourites_yellow:
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,True)
                     cSetVisible(self,21,False)
                     cSetVisible(self,20,True)


                     if english_enabled:
                         cSetVisible(self,72,False)
                         cSetVisible(self,73,True)
                         cSetVisible(self,65,False)
                         cSetVisible(self,64,True)




             elif settings_yellow:
                 if picture_yellow:
                     cSetVisible(self,30,False)
                     cSetVisible(self,31,True)
                     cSetVisible(self,41,False)
                     cSetVisible(self,40,True)

                     if english_enabled:
                         cSetVisible(self,74,False)
                         cSetVisible(self,75,True)
                         cSetVisible(self,85,False)
                         cSetVisible(self,84,True)


                 elif sound_yellow:
                     cSetVisible(self,32,False)
                     cSetVisible(self,33,True)
                     cSetVisible(self,41,False)
                     cSetVisible(self,40,True)

                     if english_enabled:
                         cSetVisible(self,76,False)
                         cSetVisible(self,77,True)
                         cSetVisible(self,85,False)
                         cSetVisible(self,84,True)


                 elif changelanguage_yellow:
                     cSetVisible(self,34,False)
                     cSetVisible(self,35,True)
                     cSetVisible(self,41,False)
                     cSetVisible(self,40,True)

                     if english_enabled:
                         cSetVisible(self,78,False)
                         cSetVisible(self,79,True)
                         cSetVisible(self,85,False)
                         cSetVisible(self,84,True)


                 elif changepin_yellow:
                     cSetVisible(self,36,False)
                     cSetVisible(self,37,True)
                     cSetVisible(self,41,False)
                     cSetVisible(self,40,True)

                     if english_enabled:
                         cSetVisible(self,80,False)
                         cSetVisible(self,81,True)
                         cSetVisible(self,85,False)
                         cSetVisible(self,84,True)


                 elif viewrestrictions_yellow:
                     cSetVisible(self,38,False)
                     cSetVisible(self,39,True)
                     cSetVisible(self,41,False)
                     cSetVisible(self,40,True)

                     if english_enabled:
                         cSetVisible(self,82,False)
                         cSetVisible(self,83,True)
                         cSetVisible(self,85,False)
                         cSetVisible(self,84,True)


                 elif removechannels_yellow:
                     pass


                 elif systemdetails_yellow:
                     cSetVisible(self,42,False)
                     cSetVisible(self,43,True)
                     cSetVisible(self,41,False)
                     cSetVisible(self,40,True)

                     if english_enabled:
                         cSetVisible(self,86,False)
                         cSetVisible(self,87,True)
                         cSetVisible(self,85,False)
                         cSetVisible(self,84,True)


                 elif speedtest_yellow:
                     cSetVisible(self,44,False)
                     cSetVisible(self,45,True)
                     cSetVisible(self,41,False)
                     cSetVisible(self,40,True)

                     if english_enabled:
                         cSetVisible(self,88,False)
                         cSetVisible(self,89,True)
                         cSetVisible(self,85,False)
                         cSetVisible(self,84,True)




             elif changepin_enabled:
                 if PIN_1_enabled:
                     if PIN_1_enabled == True:
                         cSetVisible(self,4009,False)
                         cSetVisible(self,4013,True)
                     elif PIN_1_enabled == False:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                 elif PIN_2_enabled:
                     if PIN_2_enabled == True:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                     elif PIN_2_enabled == False:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                 elif PIN_3_enabled:
                     if PIN_3_enabled == True:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                     elif PIN_3_enabled == False:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                 elif PIN_4_enabled:
                     if PIN_4_enabled == True:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                     elif PIN_4_enabled == False:
                         pass




         if action == ACTION_NUMBER7:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,11,False)
                     cSetVisible(self,10,True)
                     cSetVisible(self,23,False)
                     cSetVisible(self,22,True)


                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,55,True)
                         cSetVisible(self,67,False)
                         cSetVisible(self,66,True)


                 elif entertainment_yellow:
                     cSetVisible(self,12,False)
                     cSetVisible(self,13,True)
                     cSetVisible(self,23,False)
                     cSetVisible(self,22,True)


                     if english_enabled:
                         cSetVisible(self,56,False)
                         cSetVisible(self,57,True)
                         cSetVisible(self,67,False)
                         cSetVisible(self,66,True)


                 elif movies_yellow:
                     cSetVisible(self,14,False)
                     cSetVisible(self,15,True)
                     cSetVisible(self,23,False)
                     cSetVisible(self,22,True)


                     if english_enabled:
                         cSetVisible(self,58,False)
                         cSetVisible(self,59,True)
                         cSetVisible(self,67,False)
                         cSetVisible(self,66,True)


                 elif kids_yellow:
                     cSetVisible(self,16,False)
                     cSetVisible(self,17,True)
                     cSetVisible(self,23,False)
                     cSetVisible(self,22,True)


                     if english_enabled:
                         cSetVisible(self,60,False)
                         cSetVisible(self,61,True)
                         cSetVisible(self,67,False)
                         cSetVisible(self,66,True)


                 elif sports_yellow:
                     cSetVisible(self,18,False)
                     cSetVisible(self,19,True)
                     cSetVisible(self,23,False)
                     cSetVisible(self,22,True)


                     if english_enabled:
                         cSetVisible(self,62,False)
                         cSetVisible(self,63,True)
                         cSetVisible(self,67,False)
                         cSetVisible(self,66,True)


                 elif news_yellow:
                     cSetVisible(self,20,False)
                     cSetVisible(self,21,True)
                     cSetVisible(self,23,False)
                     cSetVisible(self,22,True)


                     if english_enabled:
                         cSetVisible(self,64,False)
                         cSetVisible(self,65,True)
                         cSetVisible(self,67,False)
                         cSetVisible(self,66,True)


                 elif documentaries_yellow:
                     pass


                 elif musicradio_yellow:
                     cSetVisible(self,24,False)
                     cSetVisible(self,25,True)
                     cSetVisible(self,23,False)
                     cSetVisible(self,22,True)


                     if english_enabled:
                         cSetVisible(self,68,False)
                         cSetVisible(self,69,True)
                         cSetVisible(self,67,False)
                         cSetVisible(self,66,True)


                 elif adult_yellow:
                     cSetVisible(self,26,False)
                     cSetVisible(self,27,True)
                     cSetVisible(self,23,False)
                     cSetVisible(self,22,True)


                     if english_enabled:
                         cSetVisible(self,70,False)
                         cSetVisible(self,71,True)
                         cSetVisible(self,67,False)
                         cSetVisible(self,66,True)


                 elif favourites_yellow:
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,True)
                     cSetVisible(self,23,False)
                     cSetVisible(self,22,True)


                     if english_enabled:
                         cSetVisible(self,72,False)
                         cSetVisible(self,73,True)
                         cSetVisible(self,67,False)
                         cSetVisible(self,66,True)




             elif settings_yellow:
                 if picture_yellow:
                     cSetVisible(self,30,False)
                     cSetVisible(self,31,True)
                     cSetVisible(self,43,False)
                     cSetVisible(self,42,True)

                     if english_enabled:
                         cSetVisible(self,74,False)
                         cSetVisible(self,75,True)
                         cSetVisible(self,87,False)
                         cSetVisible(self,86,True)


                 elif sound_yellow:
                     cSetVisible(self,32,False)
                     cSetVisible(self,33,True)
                     cSetVisible(self,43,False)
                     cSetVisible(self,42,True)

                     if english_enabled:
                         cSetVisible(self,76,False)
                         cSetVisible(self,77,True)
                         cSetVisible(self,87,False)
                         cSetVisible(self,86,True)


                 elif changelanguage_yellow:
                     cSetVisible(self,34,False)
                     cSetVisible(self,35,True)
                     cSetVisible(self,43,False)
                     cSetVisible(self,42,True)

                     if english_enabled:
                         cSetVisible(self,78,False)
                         cSetVisible(self,79,True)
                         cSetVisible(self,87,False)
                         cSetVisible(self,86,True)


                 elif changepin_yellow:
                     cSetVisible(self,36,False)
                     cSetVisible(self,37,True)
                     cSetVisible(self,43,False)
                     cSetVisible(self,42,True)

                     if english_enabled:
                         cSetVisible(self,80,False)
                         cSetVisible(self,81,True)
                         cSetVisible(self,87,False)
                         cSetVisible(self,86,True)


                 elif viewrestrictions_yellow:
                     cSetVisible(self,38,False)
                     cSetVisible(self,39,True)
                     cSetVisible(self,43,False)
                     cSetVisible(self,42,True)

                     if english_enabled:
                         cSetVisible(self,82,False)
                         cSetVisible(self,83,True)
                         cSetVisible(self,87,False)
                         cSetVisible(self,86,True)


                 elif removechannels_yellow:
                     cSetVisible(self,40,False)
                     cSetVisible(self,41,True)
                     cSetVisible(self,43,False)
                     cSetVisible(self,42,True)

                     if english_enabled:
                         cSetVisible(self,84,False)
                         cSetVisible(self,85,True)
                         cSetVisible(self,87,False)
                         cSetVisible(self,86,True)


                 elif systemdetails_yellow:
                     pass


                 elif speedtest_yellow:
                     cSetVisible(self,44,False)
                     cSetVisible(self,45,True)
                     cSetVisible(self,43,False)
                     cSetVisible(self,42,True)

                     if english_enabled:
                         cSetVisible(self,88,False)
                         cSetVisible(self,89,True)
                         cSetVisible(self,87,False)
                         cSetVisible(self,86,True)




             elif changepin_enabled:
                 if PIN_1_enabled:
                     if PIN_1_enabled == True:
                         cSetVisible(self,4009,False)
                         cSetVisible(self,4013,True)
                     elif PIN_1_enabled == False:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                 elif PIN_2_enabled:
                     if PIN_2_enabled == True:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                     elif PIN_2_enabled == False:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                 elif PIN_3_enabled:
                     if PIN_3_enabled == True:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                     elif PIN_3_enabled == False:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                 elif PIN_4_enabled:
                     if PIN_4_enabled == True:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                     elif PIN_4_enabled == False:
                         pass




         if action == ACTION_NUMBER8:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,11,False)
                     cSetVisible(self,10,True)
                     cSetVisible(self,25,False)
                     cSetVisible(self,24,True)


                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,55,True)
                         cSetVisible(self,69,False)
                         cSetVisible(self,68,True)


                 elif entertainment_yellow:
                     cSetVisible(self,12,False)
                     cSetVisible(self,13,True)
                     cSetVisible(self,25,False)
                     cSetVisible(self,24,True)


                     if english_enabled:
                         cSetVisible(self,56,False)
                         cSetVisible(self,57,True)
                         cSetVisible(self,69,False)
                         cSetVisible(self,68,True)


                 elif movies_yellow:
                     cSetVisible(self,14,False)
                     cSetVisible(self,15,True)
                     cSetVisible(self,25,False)
                     cSetVisible(self,24,True)


                     if english_enabled:
                         cSetVisible(self,58,False)
                         cSetVisible(self,59,True)
                         cSetVisible(self,69,False)
                         cSetVisible(self,68,True)


                 elif kids_yellow:
                     cSetVisible(self,16,False)
                     cSetVisible(self,17,True)
                     cSetVisible(self,25,False)
                     cSetVisible(self,24,True)


                     if english_enabled:
                         cSetVisible(self,60,False)
                         cSetVisible(self,61,True)
                         cSetVisible(self,69,False)
                         cSetVisible(self,68,True)


                 elif sports_yellow:
                     cSetVisible(self,18,False)
                     cSetVisible(self,19,True)
                     cSetVisible(self,25,False)
                     cSetVisible(self,24,True)


                     if english_enabled:
                         cSetVisible(self,62,False)
                         cSetVisible(self,63,True)
                         cSetVisible(self,69,False)
                         cSetVisible(self,68,True)


                 elif news_yellow:
                     cSetVisible(self,20,False)
                     cSetVisible(self,21,True)
                     cSetVisible(self,25,False)
                     cSetVisible(self,24,True)


                     if english_enabled:
                         cSetVisible(self,64,False)
                         cSetVisible(self,65,True)
                         cSetVisible(self,69,False)
                         cSetVisible(self,68,True)


                 elif documentaries_yellow:
                     cSetVisible(self,22,False)
                     cSetVisible(self,23,True)
                     cSetVisible(self,25,False)
                     cSetVisible(self,24,True)


                     if english_enabled:
                         cSetVisible(self,66,False)
                         cSetVisible(self,67,True)
                         cSetVisible(self,69,False)
                         cSetVisible(self,68,True)


                 elif musicradio_yellow:
                     pass


                 elif adult_yellow:
                     cSetVisible(self,26,False)
                     cSetVisible(self,27,True)
                     cSetVisible(self,25,False)
                     cSetVisible(self,24,True)


                     if english_enabled:
                         cSetVisible(self,70,False)
                         cSetVisible(self,71,True)
                         cSetVisible(self,69,False)
                         cSetVisible(self,68,True)


                 elif favourites_yellow:
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,True)
                     cSetVisible(self,25,False)
                     cSetVisible(self,24,True)


                     if english_enabled:
                         cSetVisible(self,72,False)
                         cSetVisible(self,73,True)
                         cSetVisible(self,69,False)
                         cSetVisible(self,68,True)




             elif settings_yellow:
                 if picture_yellow:
                     cSetVisible(self,30,False)
                     cSetVisible(self,31,True)
                     cSetVisible(self,45,False)
                     cSetVisible(self,44,True)

                     if english_enabled:
                         cSetVisible(self,74,False)
                         cSetVisible(self,75,True)
                         cSetVisible(self,89,False)
                         cSetVisible(self,88,True)


                 elif sound_yellow:
                     cSetVisible(self,32,False)
                     cSetVisible(self,33,True)
                     cSetVisible(self,45,False)
                     cSetVisible(self,44,True)

                     if english_enabled:
                         cSetVisible(self,76,False)
                         cSetVisible(self,77,True)
                         cSetVisible(self,89,False)
                         cSetVisible(self,88,True)


                 elif changelanguage_yellow:
                     cSetVisible(self,34,False)
                     cSetVisible(self,35,True)
                     cSetVisible(self,45,False)
                     cSetVisible(self,44,True)

                     if english_enabled:
                         cSetVisible(self,78,False)
                         cSetVisible(self,79,True)
                         cSetVisible(self,89,False)
                         cSetVisible(self,88,True)


                 elif changepin_yellow:
                     cSetVisible(self,36,False)
                     cSetVisible(self,37,True)
                     cSetVisible(self,45,False)
                     cSetVisible(self,44,True)

                     if english_enabled:
                         cSetVisible(self,80,False)
                         cSetVisible(self,81,True)
                         cSetVisible(self,89,False)
                         cSetVisible(self,88,True)


                 elif viewrestrictions_yellow:
                     cSetVisible(self,38,False)
                     cSetVisible(self,39,True)
                     cSetVisible(self,45,False)
                     cSetVisible(self,44,True)

                     if english_enabled:
                         cSetVisible(self,82,False)
                         cSetVisible(self,83,True)
                         cSetVisible(self,89,False)
                         cSetVisible(self,88,True)


                 elif removechannels_yellow:
                     cSetVisible(self,40,False)
                     cSetVisible(self,41,True)
                     cSetVisible(self,45,False)
                     cSetVisible(self,44,True)

                     if english_enabled:
                         cSetVisible(self,84,False)
                         cSetVisible(self,85,True)
                         cSetVisible(self,89,False)
                         cSetVisible(self,88,True)


                 elif systemdetails_yellow:
                     cSetVisible(self,42,False)
                     cSetVisible(self,43,True)
                     cSetVisible(self,45,False)
                     cSetVisible(self,44,True)

                     if english_enabled:
                         cSetVisible(self,86,False)
                         cSetVisible(self,87,True)
                         cSetVisible(self,89,False)
                         cSetVisible(self,88,True)


                 elif speedtest_yellow:
                     pass



             elif changepin_enabled:
                 if PIN_1_enabled:
                     if PIN_1_enabled == True:
                         cSetVisible(self,4009,False)
                         cSetVisible(self,4013,True)
                     elif PIN_1_enabled == False:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                 elif PIN_2_enabled:
                     if PIN_2_enabled == True:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                     elif PIN_2_enabled == False:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                 elif PIN_3_enabled:
                     if PIN_3_enabled == True:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                     elif PIN_3_enabled == False:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                 elif PIN_4_enabled:
                     if PIN_4_enabled == True:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                     elif PIN_4_enabled == False:
                         pass




         if action == ACTION_NUMBER9:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,11,False)
                     cSetVisible(self,10,True)
                     cSetVisible(self,27,False)
                     cSetVisible(self,26,True)


                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,55,True)
                         cSetVisible(self,71,False)
                         cSetVisible(self,70,True)


                 elif entertainment_yellow:
                     cSetVisible(self,12,False)
                     cSetVisible(self,13,True)
                     cSetVisible(self,27,False)
                     cSetVisible(self,26,True)


                     if english_enabled:
                         cSetVisible(self,56,False)
                         cSetVisible(self,57,True)
                         cSetVisible(self,71,False)
                         cSetVisible(self,70,True)


                 elif movies_yellow:
                     cSetVisible(self,14,False)
                     cSetVisible(self,15,True)
                     cSetVisible(self,27,False)
                     cSetVisible(self,26,True)


                     if english_enabled:
                         cSetVisible(self,58,False)
                         cSetVisible(self,59,True)
                         cSetVisible(self,71,False)
                         cSetVisible(self,70,True)


                 elif kids_yellow:
                     cSetVisible(self,16,False)
                     cSetVisible(self,17,True)
                     cSetVisible(self,27,False)
                     cSetVisible(self,26,True)


                     if english_enabled:
                         cSetVisible(self,60,False)
                         cSetVisible(self,61,True)
                         cSetVisible(self,71,False)
                         cSetVisible(self,70,True)


                 elif sports_yellow:
                     cSetVisible(self,18,False)
                     cSetVisible(self,19,True)
                     cSetVisible(self,27,False)
                     cSetVisible(self,26,True)


                     if english_enabled:
                         cSetVisible(self,62,False)
                         cSetVisible(self,63,True)
                         cSetVisible(self,71,False)
                         cSetVisible(self,70,True)


                 elif news_yellow:
                     cSetVisible(self,20,False)
                     cSetVisible(self,21,True)
                     cSetVisible(self,27,False)
                     cSetVisible(self,26,True)


                     if english_enabled:
                         cSetVisible(self,64,False)
                         cSetVisible(self,65,True)
                         cSetVisible(self,71,False)
                         cSetVisible(self,70,True)


                 elif documentaries_yellow:
                     cSetVisible(self,22,False)
                     cSetVisible(self,23,True)
                     cSetVisible(self,27,False)
                     cSetVisible(self,26,True)


                     if english_enabled:
                         cSetVisible(self,66,False)
                         cSetVisible(self,67,True)
                         cSetVisible(self,71,False)
                         cSetVisible(self,70,True)


                 elif musicradio_yellow:
                     cSetVisible(self,24,False)
                     cSetVisible(self,25,True)
                     cSetVisible(self,27,False)
                     cSetVisible(self,26,True)


                     if english_enabled:
                         cSetVisible(self,68,False)
                         cSetVisible(self,69,True)
                         cSetVisible(self,71,False)
                         cSetVisible(self,70,True)


                 elif adult_yellow:
                     pass


                 elif favourites_yellow:
                     cSetVisible(self,28,False)
                     cSetVisible(self,29,True)
                     cSetVisible(self,27,False)
                     cSetVisible(self,26,True)


                     if english_enabled:
                         cSetVisible(self,72,False)
                         cSetVisible(self,73,True)
                         cSetVisible(self,71,False)
                         cSetVisible(self,70,True)




             elif changepin_enabled:
                 if PIN_1_enabled:
                     if PIN_1_enabled == True:
                         cSetVisible(self,4009,False)
                         cSetVisible(self,4013,True)
                     elif PIN_1_enabled == False:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                 elif PIN_2_enabled:
                     if PIN_2_enabled == True:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                     elif PIN_2_enabled == False:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                 elif PIN_3_enabled:
                     if PIN_3_enabled == True:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                     elif PIN_3_enabled == False:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                 elif PIN_4_enabled:
                     if PIN_4_enabled == True:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                     elif PIN_4_enabled == False:
                         pass


                     elif PIN_4_enabled:
                         if PIN_4_enabled == True:
                             cSetVisible(self,4012,False)
                             cSetVisible(self,4016,True)
                         elif PIN_4_enabled == False:
                             pass




         if action == ACTION_NUMBER0:
             if tvguide_yellow:
                 if allchannels_yellow:
                     cSetVisible(self,11,False)
                     cSetVisible(self,10,True)
                     cSetVisible(self,29,False)
                     cSetVisible(self,28,True)


                     if english_enabled:
                         cSetVisible(self,54,False)
                         cSetVisible(self,55,True)
                         cSetVisible(self,73,False)
                         cSetVisible(self,72,True)


                 elif entertainment_yellow:
                     cSetVisible(self,12,False)
                     cSetVisible(self,13,True)
                     cSetVisible(self,29,False)
                     cSetVisible(self,28,True)


                     if english_enabled:
                         cSetVisible(self,56,False)
                         cSetVisible(self,57,True)
                         cSetVisible(self,73,False)
                         cSetVisible(self,72,True)


                 elif movies_yellow:
                     cSetVisible(self,14,False)
                     cSetVisible(self,15,True)
                     cSetVisible(self,29,False)
                     cSetVisible(self,28,True)


                     if english_enabled:
                         cSetVisible(self,58,False)
                         cSetVisible(self,59,True)
                         cSetVisible(self,73,False)
                         cSetVisible(self,72,True)


                 elif kids_yellow:
                     cSetVisible(self,16,False)
                     cSetVisible(self,17,True)
                     cSetVisible(self,29,False)
                     cSetVisible(self,28,True)


                     if english_enabled:
                         cSetVisible(self,60,False)
                         cSetVisible(self,61,True)
                         cSetVisible(self,73,False)
                         cSetVisible(self,72,True)


                 elif sports_yellow:
                     cSetVisible(self,18,False)
                     cSetVisible(self,19,True)
                     cSetVisible(self,29,False)
                     cSetVisible(self,28,True)


                     if english_enabled:
                         cSetVisible(self,62,False)
                         cSetVisible(self,63,True)
                         cSetVisible(self,73,False)
                         cSetVisible(self,72,True)


                 elif news_yellow:
                     cSetVisible(self,20,False)
                     cSetVisible(self,21,True)
                     cSetVisible(self,29,False)
                     cSetVisible(self,28,True)


                     if english_enabled:
                         cSetVisible(self,64,False)
                         cSetVisible(self,65,True)
                         cSetVisible(self,73,False)
                         cSetVisible(self,72,True)


                 elif documentaries_yellow:
                     cSetVisible(self,22,False)
                     cSetVisible(self,23,True)
                     cSetVisible(self,29,False)
                     cSetVisible(self,28,True)


                     if english_enabled:
                         cSetVisible(self,66,False)
                         cSetVisible(self,67,True)
                         cSetVisible(self,73,False)
                         cSetVisible(self,72,True)


                 elif musicradio_yellow:
                     cSetVisible(self,24,False)
                     cSetVisible(self,25,True)
                     cSetVisible(self,29,False)
                     cSetVisible(self,28,True)


                     if english_enabled:
                         cSetVisible(self,68,False)
                         cSetVisible(self,69,True)
                         cSetVisible(self,73,False)
                         cSetVisible(self,72,True)


                 elif adult_yellow:
                     cSetVisible(self,26,False)
                     cSetVisible(self,27,True)
                     cSetVisible(self,29,False)
                     cSetVisible(self,28,True)


                     if english_enabled:
                         cSetVisible(self,70,False)
                         cSetVisible(self,71,True)
                         cSetVisible(self,73,False)
                         cSetVisible(self,72,True)


                 elif favourites_yellow:
                     pass




             elif changepin_enabled:
                 if PIN_1_enabled:
                     if PIN_1_enabled == True:
                         cSetVisible(self,4009,False)
                         cSetVisible(self,4013,True)
                     elif PIN_1_enabled == False:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                 elif PIN_2_enabled:
                     if PIN_2_enabled == True:
                         cSetVisible(self,4010,False)
                         cSetVisible(self,4014,True)
                     elif PIN_2_enabled == False:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                 elif PIN_3_enabled:
                     if PIN_3_enabled == True:
                         cSetVisible(self,4011,False)
                         cSetVisible(self,4015,True)
                     elif PIN_3_enabled == False:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                 elif PIN_4_enabled:
                     if PIN_4_enabled == True:
                         cSetVisible(self,4012,False)
                         cSetVisible(self,4016,True)
                     elif PIN_4_enabled == False:
                         pass
