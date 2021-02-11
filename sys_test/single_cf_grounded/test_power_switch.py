# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2021 Bitcraze AB
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
import time
import unittest

import cflib.crtp
from cflib.utils.power_switch import PowerSwitch


class TestPowerSwitch(unittest.TestCase):
    def setUp(self):
        cflib.crtp.init_drivers(enable_debug_driver=False)

    def test_reboot(self):
        # ToDO: check that cf is connected
        s = PowerSwitch("radio://0/80/2M/E7E7E7E7E7")
        s.stm_power_down()
        # ToDo: check that cf is not connected
        s.stm_power_up()
        # ToDO: check that cf is connected


if __name__ == '__main__':
    unittest.main()