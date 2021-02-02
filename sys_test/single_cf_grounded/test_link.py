# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2019 Bitcraze AB
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
import struct
import numpy as np

import cflib.crtp
from cflib.crtp.crtpstack import CRTPPacket
from cflib.crtp.crtpstack import CRTPPort


class TestConnection(unittest.TestCase):
    def setUp(self):
        cflib.crtp.init_drivers(enable_debug_driver=False)

    # def test_scan(self):
    #     start_time = time.time()
    #     result = cflib.crtp.scan_interfaces()
    #     end_time = time.time()
    #     uris = [uri for (uri, msg) in result]
    #     self.assertEqual(len(uris), 2)
    #     self.assertIn("radio://*/80/2M/E7E7E7E7E7", uris)
    #     self.assertIn("usb://0", uris)
    #     self.assertLess(end_time - start_time, 2)

    def test_latency_radio(self):
        result = self.latency("radio://0/80/2M/E7E7E7E7E7")
        self.assertLess(result, 8)

    # def test_latency_usb(self):
    #     result = self.latency("usb://0")
    #     self.assertLess(result, 8)

    def test_bandwidth_radio(self):
        result = self.bandwidth("radio://0/80/2M/E7E7E7E7E7")
        self.assertGreater(result, 450)

    # def test_bandwidth_usb(self):
    #     result = self.bandwidth("usb://0")
    #     self.assertLess(result, 8)

    def latency(self, uri, count = 500):
        link = cflib.crtp.get_link_driver(uri)
        # # wait until no more packets in queue
        # while True:
        #     pk = link.receive_packet(0.5)
        #     print(pk)
        #     if not pk or pk.header == 0xFF:
        #         break

        pk = CRTPPacket()
        pk.set_header(CRTPPort.LINKCTRL, 0)  # Echo channel

        latencies = []
        for i in range(count):
            pk.data = struct.pack('<I', i)

            start_time = time.time()
            link.send_packet(pk)
            while True:
                pk_ack = link.receive_packet(-1)
                if pk_ack.port == CRTPPort.LINKCTRL and pk_ack.channel == 0:
                    break
            end_time = time.time()

            # make sure we actually received the expected value
            i_recv, = struct.unpack('<I', pk_ack.data)
            self.assertEqual(i, i_recv)
            latencies.append((end_time - start_time) * 1000)
        link.close()
        result = np.min(latencies)
        print("Latency for {}: {:.2f} ms".format(uri, result))
        return result

    def bandwidth(self, uri, count = 500):
        link = cflib.crtp.get_link_driver(uri, link_error_callback=self.error_cb)
        # # wait until no more packets in queue
        # while True:
        #     pk = link.receive_packet(0.5)
        #     if not pk:
        #         break

        pk = CRTPPacket()
        pk.set_header(CRTPPort.LINKCTRL, 0)  # Echo channel

        # enqueue packets
        start_time = time.time()
        for i in range(count):
            pk.data = struct.pack('<I', i)
            link.send_packet(pk)

        # get the result
        for i in range(count):
            while True:
                pk_ack = link.receive_packet(-1)
                if pk_ack.port == CRTPPort.LINKCTRL and pk_ack.channel == 0:
                    break
            # make sure we actually received the expected value
            i_recv, = struct.unpack('<I', pk_ack.data)
            self.assertEqual(i, i_recv)
        end_time = time.time()
        link.close()
        result = count / (end_time - start_time)
        print("Bandwith for {}: {:.2f} packets/s".format(uri, result))
        return result

    def error_cb(self, error):
        self.assertIsNone(None, error)


if __name__ == '__main__':
    unittest.main()
