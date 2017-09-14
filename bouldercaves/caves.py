"""
These are the (encoded) caves from Boulderdash I  on the Commodore-64.
More info including the decoding algorithm:
https://www.elmerproductions.com/sp/peterb/rawCaveData.html#rawCaveDataFormat

Written by Irmen de Jong (irmen@razorvine.net)
License: MIT open-source.
"""

from typing import Sequence, List


CAVES = [
    ("A - Intro",
     "Pick up jewels and exit before time is up.",
     [0x01, 0x14, 0x0A, 0x0F, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x96, 0x6E, 0x46, 0x28, 0x1E, 0x08, 0x0B, 0x09,
      0xD4, 0x20, 0x00, 0x10, 0x14, 0x00, 0x3C, 0x32, 0x09, 0x00, 0x42, 0x01, 0x09, 0x1E, 0x02, 0x42, 0x09, 0x10, 0x1E, 0x02, 0x25, 0x03,
      0x04, 0x04, 0x26, 0x12, 0xFF]
     ),
    ("B - Rooms",
     "Pick up jewels, but you must move boulders to get all jewels.",
     [0x02, 0x14, 0x14, 0x32, 0x03, 0x00, 0x01, 0x57, 0x58, 0x0A, 0x0C, 0x09, 0x0D, 0x0A, 0x96, 0x6E, 0x46, 0x46, 0x46, 0x0A, 0x04, 0x09,
      0x00, 0x00, 0x00, 0x10, 0x14, 0x08, 0x3C, 0x32, 0x09, 0x02, 0x42, 0x01, 0x08, 0x26, 0x02, 0x42, 0x01, 0x0F, 0x26, 0x02, 0x42, 0x08,
      0x03, 0x14, 0x04, 0x42, 0x10, 0x03, 0x14, 0x04, 0x42, 0x18, 0x03, 0x14, 0x04, 0x42, 0x20, 0x03, 0x14, 0x04, 0x40, 0x01, 0x05, 0x26,
      0x02, 0x40, 0x01, 0x0B, 0x26, 0x02, 0x40, 0x01, 0x12, 0x26, 0x02, 0x40, 0x14, 0x03, 0x14, 0x04, 0x25, 0x12, 0x15, 0x04, 0x12, 0x16,
      0xFF]
     ),
    ("C - Maze",
     "Pick up jewels. You must get every jewel to exit.",
     [0x03, 0x00, 0x0F, 0x00, 0x00, 0x32, 0x36, 0x34, 0x37, 0x18, 0x17, 0x18, 0x17, 0x15, 0x96, 0x64, 0x5A, 0x50, 0x46, 0x09, 0x08, 0x09,
      0x04, 0x00, 0x02, 0x10, 0x14, 0x00, 0x64, 0x32, 0x09, 0x00, 0x25, 0x03, 0x04, 0x04, 0x27, 0x14, 0xFF]
     ),
    ("D - Butterflies",
     "Drop boulders on butterflies to create jewels.",
     [0x04, 0x14, 0x05, 0x14, 0x00, 0x6E, 0x70, 0x73, 0x77, 0x24, 0x24, 0x24, 0x24, 0x24, 0x78, 0x64, 0x50, 0x3C, 0x32, 0x04, 0x08, 0x09,
      0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 0x25, 0x01, 0x03, 0x04, 0x26, 0x16, 0x81, 0x08, 0x0A, 0x04, 0x04, 0x00,
      0x30, 0x0A, 0x0B, 0x81, 0x10, 0x0A, 0x04, 0x04, 0x00, 0x30, 0x12, 0x0B, 0x81, 0x18, 0x0A, 0x04, 0x04, 0x00, 0x30, 0x1A, 0x0B, 0x81,
      0x20, 0x0A, 0x04, 0x04, 0x00, 0x30, 0x22, 0x0B, 0xFF]
     ),
    ("Intermission 1",
     "Bonus level!",
     [0x11, 0x14, 0x1E, 0x00, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x06, 0x06, 0x06, 0x06, 0x06, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0E, 0x02, 0x09,
      0x00, 0x00, 0x00, 0x14, 0x00, 0x00, 0xFF, 0x09, 0x00, 0x00, 0x87, 0x00, 0x02, 0x28, 0x16, 0x07, 0x87, 0x00, 0x02, 0x14, 0x0C, 0x00,
      0x32, 0x0A, 0x0C, 0x10, 0x0A, 0x04, 0x01, 0x0A, 0x05, 0x25, 0x03, 0x05, 0x04, 0x12, 0x0C, 0xFF]
     ),

    ("E - Guards",
     "The jewels are there for grabbing, but they are guarded by the deadly fireflies.",
     [0x05, 0x14, 0x32, 0x5A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x05, 0x06, 0x07, 0x08, 0x96, 0x78, 0x5A, 0x3C, 0x1E, 0x09, 0x0A, 0x09,
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x25, 0x01, 0x03, 0x04, 0x27, 0x16, 0x80, 0x08, 0x0A, 0x03, 0x03, 0x00,
      0x80, 0x10, 0x0A, 0x03, 0x03, 0x00, 0x80, 0x18, 0x0A, 0x03, 0x03, 0x00, 0x80, 0x20, 0x0A, 0x03, 0x03, 0x00, 0x14, 0x09, 0x0C, 0x08,
      0x0A, 0x0A, 0x14, 0x11, 0x0C, 0x08, 0x12, 0x0A, 0x14, 0x19, 0x0C, 0x08, 0x1A, 0x0A, 0x14, 0x21, 0x0C, 0x08, 0x22, 0x0A, 0x80, 0x08,
      0x10, 0x03, 0x03, 0x00, 0x80, 0x10, 0x10, 0x03, 0x03, 0x00, 0x80, 0x18, 0x10, 0x03, 0x03, 0x00, 0x80, 0x20, 0x10, 0x03, 0x03, 0x00,
      0x14, 0x09, 0x12, 0x08, 0x0A, 0x10, 0x14, 0x11, 0x12, 0x08, 0x12, 0x10, 0x14, 0x19, 0x12, 0x08, 0x1A, 0x10, 0x14, 0x21, 0x12, 0x08,
      0x22, 0x10, 0xFF]
     ),
    ("F - Firefly dens",
     "Each firefly is guarding a jewel.",
     [0x06, 0x14, 0x28, 0x3C, 0x00, 0x14, 0x15, 0x16, 0x17, 0x04, 0x06, 0x07, 0x08, 0x08, 0x96, 0x78, 0x64, 0x5A, 0x50, 0x0E, 0x0A, 0x09,
      0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x32, 0x00, 0x00, 0x00, 0x82, 0x01, 0x03, 0x0A, 0x04, 0x00, 0x82, 0x01, 0x06, 0x0A, 0x04, 0x00,
      0x82, 0x01, 0x09, 0x0A, 0x04, 0x00, 0x82, 0x01, 0x0C, 0x0A, 0x04, 0x00, 0x41, 0x0A, 0x03, 0x0D, 0x04, 0x14, 0x03, 0x05, 0x08, 0x04,
      0x05, 0x14, 0x03, 0x08, 0x08, 0x04, 0x08, 0x14, 0x03, 0x0B, 0x08, 0x04, 0x0B, 0x14, 0x03, 0x0E, 0x08, 0x04, 0x0E, 0x82, 0x1D, 0x03,
      0x0A, 0x04, 0x00, 0x82, 0x1D, 0x06, 0x0A, 0x04, 0x00, 0x82, 0x1D, 0x09, 0x0A, 0x04, 0x00, 0x82, 0x1D, 0x0C, 0x0A, 0x04, 0x00, 0x41,
      0x1D, 0x03, 0x0D, 0x04, 0x14, 0x24, 0x05, 0x08, 0x23, 0x05, 0x14, 0x24, 0x08, 0x08, 0x23, 0x08, 0x14, 0x24, 0x0B, 0x08, 0x23, 0x0B,
      0x14, 0x24, 0x0E, 0x08, 0x23, 0x0E, 0x25, 0x03, 0x14, 0x04, 0x26, 0x14, 0xFF]
     ),
    ("G - Amoeba",
     "Surround the amoeba with boulders. Pick up jewels when it suffocates.",
     [0x07, 0x4B, 0x0A, 0x14, 0x02, 0x07, 0x08, 0x0A, 0x09, 0x0F, 0x14, 0x19, 0x19, 0x19, 0x78, 0x78, 0x78, 0x78, 0x78, 0x09, 0x0A, 0x0D,
      0x00, 0x00, 0x00, 0x10, 0x08, 0x00, 0x64, 0x28, 0x02, 0x00, 0x42, 0x01, 0x07, 0x0C, 0x02, 0x42, 0x1C, 0x05, 0x0B, 0x02, 0x7A, 0x13,
      0x15, 0x02, 0x02, 0x14, 0x04, 0x06, 0x14, 0x04, 0x0E, 0x14, 0x04, 0x16, 0x14, 0x22, 0x04, 0x14, 0x22, 0x0C, 0x14, 0x22, 0x16, 0x25,
      0x14, 0x03, 0x04, 0x27, 0x07, 0xFF]
     ),
    ("H - Enchanted wall",
     "Activate the enchanted wall and create as many jewels as you can.",
     [0x08, 0x14, 0x0A, 0x14, 0x01, 0x03, 0x04, 0x05, 0x06, 0x0A, 0x0F, 0x14, 0x14, 0x14, 0x78, 0x6E, 0x64, 0x5A, 0x50, 0x02, 0x0E, 0x09,
      0x00, 0x00, 0x00, 0x10, 0x08, 0x00, 0x5A, 0x32, 0x02, 0x00, 0x14, 0x04, 0x06, 0x14, 0x22, 0x04, 0x14, 0x22, 0x0C, 0x04, 0x00, 0x05,
      0x25, 0x14, 0x03, 0x42, 0x01, 0x07, 0x0C, 0x02, 0x42, 0x01, 0x0F, 0x0C, 0x02, 0x42, 0x1C, 0x05, 0x0B, 0x02, 0x42, 0x1C, 0x0D, 0x0B,
      0x02, 0x43, 0x0E, 0x11, 0x08, 0x02, 0x14, 0x0C, 0x10, 0x00, 0x0E, 0x12, 0x14, 0x13, 0x12, 0x41, 0x0E, 0x0F, 0x08, 0x02, 0xFF]
     ),
    ("Intermission 2",
     "Bonus level!",
     [0x12, 0x14, 0x0A, 0x00, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x10, 0x10, 0x10, 0x10, 0x10, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x06, 0x0F, 0x09,
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x87, 0x00, 0x02, 0x28, 0x16, 0x07, 0x87, 0x00, 0x02, 0x14, 0x0C, 0x01,
      0x50, 0x01, 0x03, 0x09, 0x03, 0x48, 0x02, 0x03, 0x08, 0x03, 0x54, 0x01, 0x05, 0x08, 0x03, 0x50, 0x01, 0x06, 0x07, 0x03, 0x50, 0x12,
      0x03, 0x09, 0x05, 0x54, 0x12, 0x05, 0x08, 0x05, 0x50, 0x12, 0x06, 0x07, 0x05, 0x25, 0x01, 0x04, 0x04, 0x12, 0x04, 0xFF]
     ),

    ("I - Greed",
     "You have to get a lot of jewels here, lucky there are so many.",
     [0x09, 0x14, 0x05, 0x0A, 0x64, 0x89, 0x8C, 0xFB, 0x33, 0x4B, 0x4B, 0x50, 0x55, 0x5A, 0x96, 0x96, 0x82, 0x82, 0x78, 0x08, 0x04, 0x09,
      0x00, 0x00, 0x10, 0x14, 0x00, 0x00, 0xF0, 0x78, 0x00, 0x00, 0x82, 0x05, 0x0A, 0x0D, 0x0D, 0x00, 0x01, 0x0C, 0x0A, 0x82, 0x19, 0x0A,
      0x0D, 0x0D, 0x00, 0x01, 0x1F, 0x0A, 0x42, 0x11, 0x12, 0x09, 0x02, 0x40, 0x11, 0x13, 0x09, 0x02, 0x25, 0x07, 0x0C, 0x04, 0x08, 0x0C,
      0xFF]
     ),
    ("J - Tracks",
     "Get the jewels, avoid the fireflies.",
     [0x0A, 0x14, 0x19, 0x3C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x96, 0x82, 0x78, 0x6E, 0x64, 0x06, 0x08, 0x09,
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x25, 0x0D, 0x03, 0x04, 0x27, 0x16, 0x54, 0x05, 0x04, 0x11, 0x03, 0x54,
      0x15, 0x04, 0x11, 0x05, 0x80, 0x05, 0x0B, 0x11, 0x03, 0x08, 0xC2, 0x01, 0x04, 0x15, 0x11, 0x00, 0x0D, 0x04, 0xC2, 0x07, 0x06, 0x0D,
      0x0D, 0x00, 0x0D, 0x06, 0xC2, 0x09, 0x08, 0x09, 0x09, 0x00, 0x0D, 0x08, 0xC2, 0x0B, 0x0A, 0x05, 0x05, 0x00, 0x0D, 0x0A, 0x82, 0x03,
      0x06, 0x03, 0x0F, 0x08, 0x00, 0x04, 0x06, 0x54, 0x04, 0x10, 0x04, 0x04, 0xFF]
     ),
    ("K - Crowd",
     "You must move a lot of boulders around in some tight spaces.",
     [0x0B, 0x14, 0x32, 0x00, 0x00, 0x04, 0x66, 0x97, 0x64, 0x06, 0x06, 0x06, 0x06, 0x06, 0x78, 0x78, 0x96, 0x96, 0xF0, 0x0B, 0x08, 0x09,
      0x00, 0x00, 0x00, 0x10, 0x08, 0x00, 0x64, 0x50, 0x02, 0x00, 0x42, 0x0A, 0x03, 0x09, 0x04, 0x42, 0x14, 0x03, 0x09, 0x04, 0x42, 0x1E,
      0x03, 0x09, 0x04, 0x42, 0x09, 0x16, 0x09, 0x00, 0x42, 0x0C, 0x0F, 0x11, 0x02, 0x42, 0x05, 0x0B, 0x09, 0x02, 0x42, 0x0F, 0x0B, 0x09,
      0x02, 0x42, 0x19, 0x0B, 0x09, 0x02, 0x42, 0x1C, 0x13, 0x0B, 0x01, 0x14, 0x04, 0x03, 0x14, 0x0E, 0x03, 0x14, 0x18, 0x03, 0x14, 0x22,
      0x03, 0x14, 0x04, 0x16, 0x14, 0x23, 0x15, 0x25, 0x14, 0x14, 0x04, 0x26, 0x11, 0xFF]
     ),
    ("L - Walls",
     "Drop a boulder on a firefly at the right time to blast through walls.",
     [0x0C, 0x14, 0x14, 0x00, 0x00, 0x3C, 0x02, 0x3B, 0x66, 0x13, 0x13, 0x0E, 0x10, 0x15, 0xB4, 0xAA, 0xA0, 0xA0, 0xA0, 0x0C, 0x0A, 0x09,
      0x00, 0x00, 0x00, 0x10, 0x14, 0x00, 0x3C, 0x32, 0x09, 0x00, 0x42, 0x0A, 0x05, 0x12, 0x04, 0x42, 0x0E, 0x05, 0x12, 0x04, 0x42, 0x12,
      0x05, 0x12, 0x04, 0x42, 0x16, 0x05, 0x12, 0x04, 0x42, 0x02, 0x06, 0x0B, 0x02, 0x42, 0x02, 0x0A, 0x0B, 0x02, 0x42, 0x02, 0x0E, 0x0F,
      0x02, 0x42, 0x02, 0x12, 0x0B, 0x02, 0x81, 0x1E, 0x04, 0x04, 0x04, 0x00, 0x08, 0x20, 0x05, 0x81, 0x1E, 0x09, 0x04, 0x04, 0x00, 0x08,
      0x20, 0x0A, 0x81, 0x1E, 0x0E, 0x04, 0x04, 0x00, 0x08, 0x20, 0x0F, 0x25, 0x03, 0x14, 0x04, 0x27, 0x16, 0xFF]
     ),
    ("Intermission 3",
     "Bonus level!",
     [0x13, 0x04, 0x0A, 0x00, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0E, 0x0E, 0x0E, 0x0E, 0x0E, 0x14, 0x14, 0x14, 0x14, 0x14, 0x06, 0x08, 0x09,
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x87, 0x00, 0x02, 0x28, 0x16, 0x07, 0x87, 0x00, 0x02, 0x14, 0x0C, 0x00,
      0x54, 0x01, 0x0C, 0x12, 0x02, 0x88, 0x0F, 0x09, 0x04, 0x04, 0x08, 0x25, 0x08, 0x03, 0x04, 0x12, 0x07, 0xFF]
     ),

    ("M - Apocalypse",
     "Bring the butterflies and amoeba together and watch the jewels fly.",
     [0x0D, 0x8C, 0x05, 0x08, 0x00, 0x01, 0x02, 0x03, 0x04, 0x32, 0x37, 0x3C, 0x46, 0x50, 0xA0, 0x9B, 0x96, 0x91, 0x8C, 0x06, 0x08, 0x0D,
      0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x28, 0x00, 0x00, 0x00, 0x25, 0x12, 0x03, 0x04, 0x0A, 0x03, 0x3A, 0x14, 0x03, 0x42, 0x05, 0x12,
      0x1E, 0x02, 0x70, 0x05, 0x13, 0x1E, 0x02, 0x50, 0x05, 0x14, 0x1E, 0x02, 0xC1, 0x05, 0x15, 0x1E, 0x02, 0xFF]
     ),
    ("N - Zigzag",
     "Magically transform the butterflies into jewels, but don't waste any boulders.",
     [0x0E, 0x14, 0x0A, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1E, 0x23, 0x28, 0x2A, 0x2D, 0x96, 0x91, 0x8C, 0x87, 0x82, 0x0C, 0x08, 0x09,
      0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x81, 0x0A, 0x0A, 0x0D, 0x0D, 0x00, 0x70, 0x0B, 0x0B, 0x0C, 0x03, 0xC1,
      0x0C, 0x0A, 0x03, 0x0D, 0xC1, 0x10, 0x0A, 0x03, 0x0D, 0xC1, 0x14, 0x0A, 0x03, 0x0D, 0x50, 0x16, 0x08, 0x0C, 0x02, 0x48, 0x16, 0x07,
      0x0C, 0x02, 0xC1, 0x17, 0x06, 0x03, 0x04, 0xC1, 0x1B, 0x06, 0x03, 0x04, 0xC1, 0x1F, 0x06, 0x03, 0x04, 0x25, 0x03, 0x03, 0x04, 0x27,
      0x14, 0xFF]
     ),
    ("O - Funnel",
     "There is an enchanted wall at the bottom of the rock tunnel.",
     [0x0F, 0x08, 0x0A, 0x14, 0x01, 0x1D, 0x1E, 0x1F, 0x20, 0x0F, 0x14, 0x14, 0x19, 0x1E, 0x78, 0x78, 0x78, 0x78, 0x8C, 0x08, 0x0E, 0x09,
      0x00, 0x00, 0x00, 0x10, 0x08, 0x00, 0x64, 0x50, 0x02, 0x00, 0x42, 0x02, 0x04, 0x0A, 0x03, 0x42, 0x0F, 0x0D, 0x0A, 0x01, 0x41, 0x0C,
      0x0E, 0x03, 0x02, 0x43, 0x0C, 0x0F, 0x03, 0x02, 0x04, 0x14, 0x16, 0x25, 0x14, 0x03, 0xFF]
     ),
    ("P - Enchanted boxes",
     "The top of each room is an enchanted wall, but you'll have to blast your way inside.",
     [0x10, 0x14, 0x0A, 0x14, 0x01, 0x78, 0x81, 0x7E, 0x7B, 0x0C, 0x0F, 0x0F, 0x0F, 0x0C, 0x96, 0x96, 0x96, 0x96, 0x96, 0x09, 0x0A, 0x09,
      0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x32, 0x00, 0x00, 0x00, 0x25, 0x01, 0x03, 0x04, 0x27, 0x04, 0x81, 0x08, 0x13, 0x04, 0x04, 0x00,
      0x08, 0x0A, 0x14, 0xC2, 0x07, 0x0A, 0x06, 0x08, 0x43, 0x07, 0x0A, 0x06, 0x02, 0x81, 0x10, 0x13, 0x04, 0x04, 0x00, 0x08, 0x12, 0x14,
      0xC2, 0x0F, 0x0A, 0x06, 0x08, 0x43, 0x0F, 0x0A, 0x06, 0x02, 0x81, 0x18, 0x13, 0x04, 0x04, 0x00, 0x08, 0x1A, 0x14, 0x81, 0x20, 0x13,
      0x04, 0x04, 0x00, 0x08, 0x22, 0x14, 0xFF]
     ),
    ("Intermission 4",
     "Bonus level!",
     [0x14, 0x03, 0x1E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06, 0x06, 0x06, 0x06, 0x14, 0x14, 0x14, 0x14, 0x14, 0x06, 0x08, 0x09,
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x87, 0x00, 0x02, 0x28, 0x16, 0x07, 0x87, 0x00, 0x02, 0x14, 0x0C, 0x01,
      0xD0, 0x0B, 0x03, 0x03, 0x02, 0x80, 0x0B, 0x07, 0x03, 0x06, 0x00, 0x43, 0x0B, 0x06, 0x03, 0x02, 0x43, 0x0B, 0x0A, 0x03, 0x02, 0x50,
      0x08, 0x07, 0x03, 0x03, 0x25, 0x03, 0x03, 0x04, 0x09, 0x0A, 0xFF]
     )
]


# The format of the demo data is as follows.
# The low nybble of each byte indicates the direction that Rockford is to move
# ($0 = end of demo, $7 = Right, $B = Left, $D = Down, $E = Up, $F = no movement).
# The high nybble indicates the number of times (number of frames) to apply that movement.
# The demo finishes when it hits $00. So for example,
# $FF means no movement for 15 turns, $1E means move up one space, $77 means move right 7 spaces, etc.
CAVE_A_DEMO = [
    0x4F, 0x1E, 0x77, 0x2D, 0x97, 0x4F, 0x2D, 0x47, 0x3E, 0x1B, 0x4F, 0x1E, 0xB7, 0x1D, 0x27,
    0x4F, 0x6D, 0x17, 0x4D, 0x3B, 0x4F, 0x1D, 0x1B, 0x47, 0x3B, 0x4F, 0x4E, 0x5B, 0x3E, 0x5B, 0x4D,
    0x3B, 0x5F, 0x3E, 0xAB, 0x1E, 0x3B, 0x1D, 0x6B, 0x4D, 0x17, 0x4F, 0x3D, 0x47, 0x4D, 0x4B, 0x2E,
    0x27, 0x3E, 0xA7, 0xA7, 0x1D, 0x47, 0x1D, 0x47, 0x2D, 0x5F, 0x57, 0x4E, 0x57, 0x6F, 0x1D, 0x00
]

colorpalette_contrast = (  # this is a Commodore-64 palette with more contrast
    0x000000,  # 0 = black
    0xFFFFFF,  # 1 = white
    0x68372B,  # 2 = red
    0x70A4B2,  # 3 = cyan
    0x6F3D86,  # 4 = purple
    0x588D43,  # 5 = green
    0x352879,  # 6 = blue
    0xB8C76F,  # 7 = yellow
    0x6F4F25,  # 8 = orange
    0x433900,  # 9 = brown
    0x9A6759,  # 10 = light red
    0x444444,  # 11 = dark grey
    0x6C6C6C,  # 12 = medium grey
    0x9AD284,  # 13 = light green
    0x6C5EB5,  # 14 = light blue
    0x959595,  # 15 = light grey
)

colorpalette = (  # this is a lighter Commodore-64 palette
    0x000000,  # 0 = black
    0xFFFFFF,  # 1 = white
    0x984B43,  # 2 = red
    0x79C1C8,  # 3 = cyan
    0x9B51A5,  # 4 = purple
    0x68AE5C,  # 5 = green
    0x52429D,  # 6 = blue
    0xC9D684,  # 7 = yellow
    0x9B6739,  # 8 = orange
    0x6A5400,  # 9 = brown
    0xC37B75,  # 10 = light red
    0x636363,  # 11 = dark grey
    0x8A8A8A,  # 12 = medium grey
    0xA3E599,  # 13 = light green
    0x8A7BCE,  # 14 = light blue
    0xADADAD,  # 15 = light grey
)


class Cave:
    def __init__(self, index: int, name: str, description: str, width: int, height: int) -> None:
        self.index = index
        self.name = name
        self.description = description
        self.intermission = False
        self.width = width
        self.height = height
        self.map = bytearray(self.width * self.height)
        self.magicwall_millingtime = self.amoeba_slowgrowthtime = 0
        self.diamondvalue_initial = 0
        self.diamondvalue_extra = 0
        self.randomseed = 0
        self.diamonds_needed = 0
        self.amoebamaxsize = 0
        self.time = 0
        self.bgcolor1 = 0
        self.bgcolor2 = 0
        self.fgcolor = 0
        self.random_objects = (0, 0, 0, 0)
        self.random_probabilities = (0, 0, 0, 0)

    @classmethod
    def decode_from_lvl(cls, levelnumber: int) -> 'Cave':
        assert 0 < levelnumber <= len(CAVES)
        name, description, data = CAVES[levelnumber - 1]
        cave = cls(data[0], name, description, 40, 22)   # size hardcoded
        cave.intermission = name.lower().startswith("intermission")
        cave.magicwall_millingtime = cave.amoeba_slowgrowthtime = data[0x01]
        cave.diamondvalue_initial = data[0x02]
        cave.diamondvalue_extra = data[0x03]
        cave.randomseed = data[0x04]
        cave.diamonds_needed = data[0x09]
        cave.time = data[0x0e]
        cave.bgcolor1 = colorpalette[data[0x13]]
        cave.bgcolor2 = colorpalette[data[0x14]]
        cave.fgcolor = colorpalette[data[0x15]]
        cave.random_objects = data[0x18], data[0x19], data[0x1a], data[0x1b]
        cave.random_probabilities = data[0x1c], data[0x1d], data[0x1e], data[0x1f]
        cave.amoebamaxsize = int(cave.width * cave.height * 0.2273)
        cave.build_map(data[0x20:])
        return cave

    @staticmethod
    def bdrandom(seeds: List[int]) -> None:
        # the pseudo random generator that Boulder Dash uses
        assert len(seeds) == 2, "expected 2 seed numbers"
        assert 0 <= seeds[0] <= 0xFF, "expected seed 0 to be between 0 and 0xFF"
        assert 0 <= seeds[1] <= 0xFF, "expected seed 1 to be between 0 and 0xFF"
        tmp1 = (seeds[0] & 0x0001) * 0x0080
        tmp2 = (seeds[1] >> 1) & 0x007F
        result = seeds[1] + (seeds[1] & 0x0001) * 0x0080
        carry = (result > 0x00FF)
        result = result & 0x00FF
        result = result + carry + 0x13
        carry = (result > 0x00FF)
        seeds[1] = result & 0x00FF
        result = seeds[0] + carry + tmp1
        carry = (result > 0x00FF)
        result = result & 0x00FF
        result = result + carry + tmp2
        seeds[0] = result & 0x00FF
        assert 0 <= seeds[0] <= 0xFF, "expected seed 0 to STILL be between 0 and 0xFF"
        assert 0 <= seeds[1] <= 0xFF, "expected seed 0 to STILL be between 0 and 0xFF"

    def build_map(self, data: Sequence[int]) -> None:
        seeds = [0, self.randomseed]
        for y in range(1, self.height - 1):
            for x in range(0, self.width):
                obj = 0x01   # DIRT
                self.bdrandom(seeds)
                for randomobj, randomprob in zip(self.random_objects, self.random_probabilities):
                    if seeds[0] < randomprob:
                        obj = randomobj
                self.draw_single(obj, x, y)
        self.draw_rectangle(0x07, 0, 0, self.width, self.height)    # STEEL boundary

        n = 0
        while n < len(data) and data[n] < 0xff:
            obj = data[n] & 0x3f
            kind = (data[n] & 0xc0) >> 6
            x = data[n + 1]
            y = data[n + 2] - 2   # apparently need to adjust for top 2 lines where score is shown on c64
            if kind == 0:
                self.draw_single(obj, x, y)
                n += 3
            elif kind == 1:
                length = data[n + 3]
                direction = data[n + 4]
                self.draw_line(obj, x, y, length, direction)
                n += 5
            elif kind == 2:
                width = data[n + 3]
                height = data[n + 4]
                fillobject = data[n + 5]
                self.draw_rectangle(obj, x, y, width, height, fillobject)
                n += 6
            elif kind == 3:
                width = data[n + 3]
                height = data[n + 4]
                self.draw_rectangle(obj, x, y, width, height)
                n += 5
            else:
                raise ValueError("invalid cave instruction encountered")

    def draw_rectangle(self, obj: int, x1: int, y1: int, width: int, height: int, fillobject: int=None) -> None:
        self.draw_line(obj, x1, y1, width, 2)
        self.draw_line(obj, x1, y1 + height - 1, width, 2)
        self.draw_line(obj, x1, y1 + 1, height - 2, 4)
        self.draw_line(obj, x1 + width - 1, y1 + 1, height - 2, 4)
        if fillobject is not None:
            for y in range(y1 + 1, y1 + height - 1):
                self.draw_line(fillobject, x1 + 1, y, width - 2, 2)

    def draw_line(self, obj: int, x: int, y: int, length: int, direction: int) -> None:
        dx, dy = [
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1)][direction]
        for _ in range(length):
            self.draw_single(obj, x, y)
            x += dx
            y += dy

    def draw_single(self, obj: int, x: int, y: int) -> None:
        self.map[x + y * self.width] = obj
