# -*- coding: utf-8 -*-

"""
Constants and default values used by the library
------------------------------------------------

These values are defined in the :py:data:`apds9930.values` module.


COMMAND register modes (see :py:meth:`~apds9930.APDS9930_I2C_Base.write_byte`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:data:`REPEATED_BYTE` = :py:data:`0x80`

:py:data:`AUTO_INCREMENT` = :py:data:`0xA0`

:py:data:`SPECIAL_FN` = :py:data:`0xE0`


APDS-9930 I2C address
~~~~~~~~~~~~~~~~~~~~~

:py:data:`APDS9930_I2C_ADDR` = :py:data:`0x39`


Acceptable device IDs
~~~~~~~~~~~~~~~~~~~~~

:py:data:`APDS9930_IDs` = :py:data:`[0x39]`


APDS-9930 register addresses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:data:`APDS9930_ENABLE` = :py:data:`0x00`

:py:data:`APDS9930_ATIME` = :py:data:`0x01`

:py:data:`APDS9930_WTIME` = :py:data:`0x03`

:py:data:`APDS9930_AILTL` = :py:data:`0x04`

:py:data:`APDS9930_AILTH` = :py:data:`0x05`

:py:data:`APDS9930_AIHTL` = :py:data:`0x06`

:py:data:`APDS9930_AIHTH` = :py:data:`0x07`

:py:data:`APDS9930_PILTL` = :py:data:`0x08`

:py:data:`APDS9930_PILTH` = :py:data:`0x09`

:py:data:`APDS9930_PIHTL` = :py:data:`0x0A`

:py:data:`APDS9930_PIHTH` = :py:data:`0x0B`

:py:data:`APDS9930_PERS` = :py:data:`0x0C`

:py:data:`APDS9930_CONFIG` = :py:data:`0x0D`

:py:data:`APDS9930_PPULSE` = :py:data:`0x0E`

:py:data:`APDS9930_CONTROL` = :py:data:`0x0F`

:py:data:`APDS9930_ID` = :py:data:`0x12`

:py:data:`APDS9930_STATUS` = :py:data:`0x13`

:py:data:`APDS9930_Ch0DATAL` = :py:data:`0x14`

:py:data:`APDS9930_Ch0DATAH` = :py:data:`0x15`

:py:data:`APDS9930_Ch1DATAL` = :py:data:`0x16`

:py:data:`APDS9930_Ch1DATAH` = :py:data:`0x17`

:py:data:`APDS9930_PDATAL` = :py:data:`0x18`

:py:data:`APDS9930_PDATAH` = :py:data:`0x19`

:py:data:`APDS9930_POFFSET` = :py:data:`0x1E`


List for printing purposes and for iteration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:data:`REGISTERS` = :py:data:`{registers}`


Bit fields
~~~~~~~~~~

:py:data:`APDS9930_PON` = :py:data:`0b00000001`

:py:data:`APDS9930_AEN` = :py:data:`0b00000010`

:py:data:`APDS9930_PEN` = :py:data:`0b00000100`

:py:data:`APDS9930_WEN` = :py:data:`0b00001000`

:py:data:`APSD9930_AIEN` = :py:data:`0b00010000`

:py:data:`APDS9930_PIEN` = :py:data:`0b00100000`

:py:data:`APDS9930_SAI` = :py:data:`0b01000000`


On/Off definitions
~~~~~~~~~~~~~~~~~~

:py:data:`OFF` = :py:data:`0`

:py:data:`ON` = :py:data:`1`


Acceptable parameters for :py:meth:`~apds9930.APDS9930.set_mode`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:data:`POWER` = :py:data:`0`

:py:data:`AMBIENT_LIGHT` = :py:data:`1`

:py:data:`PROXIMITY` = :py:data:`2`

:py:data:`WAIT` = :py:data:`3`

:py:data:`AMBIENT_LIGHT_INT` = :py:data:`4`

:py:data:`PROXIMITY_INT` = :py:data:`5`

:py:data:`SLEEP_AFTER_INT` = :py:data:`6`

:py:data:`ALL` = :py:data:`7`



LED Drive values (:py:attr:`~apds9930.APDS9930.led_drive`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:data:`LED_DRIVE_100MA` = :py:data:`0`

:py:data:`LED_DRIVE_50MA` = :py:data:`1`

:py:data:`LED_DRIVE_25MA` = :py:data:`2`

:py:data:`LED_DRIVE_12_5MA` = :py:data:`3`



Proximity Gain (PGAIN) values (:py:attr:`~apds9930.APDS9930.proximity_gain`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:data:`PGAIN_1X` = :py:data:`0`

:py:data:`PGAIN_2X` = :py:data:`1`

:py:data:`PGAIN_4X` = :py:data:`2`

:py:data:`PGAIN_8X` = :py:data:`3`



ALS Gain (AGAIN) values (:py:attr:`~apds9930.APDS9930.ambient_light_gain`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:data:`AGAIN_1X` = :py:data:`0`

:py:data:`AGAIN_8X` = :py:data:`1`

:py:data:`AGAIN_16X` = :py:data:`2`

:py:data:`AGAIN_120X` = :py:data:`3`



Interrupt clear values
~~~~~~~~~~~~~~~~~~~~~~

:py:data:`CLEAR_PROX_INT` = :py:data:`0xE5`

:py:data:`CLEAR_ALS_INT` = :py:data:`0xE6`

:py:data:`CLEAR_ALL_INTS` = :py:data:`0xE7`



Default values
~~~~~~~~~~~~~~

:py:data:`DEFAULT_ATIME` = :py:data:`0xFF`

:py:data:`DEFAULT_WTIME` = :py:data:`0xFF`

:py:data:`DEFAULT_PTIME` = :py:data:`0xFF`

:py:data:`DEFAULT_PPULSE` = :py:data:`0x08`

:py:data:`DEFAULT_POFFSET` = :py:data:`0`

:py:data:`DEFAULT_CONFIG` = :py:data:`0`

:py:data:`DEFAULT_PDRIVE` = :py:data:`LED_DRIVE_100MA`

:py:data:`DEFAULT_PDIODE` = :py:data:`2`

:py:data:`DEFAULT_PGAIN` = :py:data:`PGAIN_8X`

:py:data:`DEFAULT_AGAIN` = :py:data:`AGAIN_16X`

:py:data:`DEFAULT_PILT` = :py:data:`0`

:py:data:`DEFAULT_PIHT` = :py:data:`50`

:py:data:`DEFAULT_AILT` = :py:data:`0xFFFF`

:py:data:`DEFAULT_AIHT` = :py:data:`0`

:py:data:`DEFAULT_PERS` = :py:data:`0x22`



ALS coefficients
~~~~~~~~~~~~~~~~

:py:data:`DF` = :py:data:`52`

:py:data:`GA` = :py:data:`0.49`

:py:data:`B` = :py:data:`1.862`

:py:data:`C` = :py:data:`0.746`

:py:data:`D` = :py:data:`1.291`


"""


REPEATED_BYTE         = 0x80
AUTO_INCREMENT        = 0xA0
SPECIAL_FN            = 0xE0

# APDS-9930 I2C address
APDS9930_I2C_ADDR     = 0x39

# Command register modes
REPEATED_BYTE         = 0x80
AUTO_INCREMENT        = 0xA0
SPECIAL_FN            = 0xE0

# Acceptable device IDs
APDS9930_IDs          = [0x39]

# APDS-9930 register addresses
APDS9930_ENABLE       = 0x00
APDS9930_ATIME        = 0x01
APDS9930_WTIME        = 0x03
APDS9930_AILTL        = 0x04
APDS9930_AILTH        = 0x05
APDS9930_AIHTL        = 0x06
APDS9930_AIHTH        = 0x07
APDS9930_PILTL        = 0x08
APDS9930_PILTH        = 0x09
APDS9930_PIHTL        = 0x0A
APDS9930_PIHTH        = 0x0B
APDS9930_PERS         = 0x0C
APDS9930_CONFIG       = 0x0D
APDS9930_PPULSE       = 0x0E
APDS9930_CONTROL      = 0x0F
APDS9930_ID           = 0x12
APDS9930_STATUS       = 0x13
APDS9930_Ch0DATAL     = 0x14
APDS9930_Ch0DATAH     = 0x15
APDS9930_Ch1DATAL     = 0x16
APDS9930_Ch1DATAH     = 0x17
APDS9930_PDATAL       = 0x18
APDS9930_PDATAH       = 0x19
APDS9930_POFFSET      = 0x1E

# List for printing purposes and for iteration
REGISTERS = {"ENABLE": 0x00, "ATIME": 0x01, "WTIME": 0x03, "AILTL": 0x04, "AILTH": 0x05, "AIHTL": 0x06, "AIHTH": 0x07, "PILTL": 0x08, "PILTH": 0x09, "PIHTL": 0x0A, "PIHTH": 0x0B, "PERS": 0x0C, "CONFIG": 0x0D, "PPULSE": 0x0E, "CONTROL": 0x0F, "ID": 0x12, "STATUS": 0x13, "Ch0DATAL": 0x14, "Ch0DATAH": 0x15, "Ch1DATAL": 0x16, "Ch1DATAH": 0x17, "PDATAL": 0x18, "PDATAH": 0x19, "POFFSET": 0x1E}

# Bit fields
APDS9930_PON          = int("00000001", 2)
APDS9930_AEN          = int("00000010", 2)
APDS9930_PEN          = int("00000100", 2)
APDS9930_WEN          = int("00001000", 2)
APSD9930_AIEN         = int("00010000", 2)
APDS9930_PIEN         = int("00100000", 2)
APDS9930_SAI          = int("01000000", 2)

# On/Off definitions
OFF                   = 0
ON                    = 1

# Acceptable parameters for setMode
POWER                 = 0
AMBIENT_LIGHT         = 1
PROXIMITY             = 2
WAIT                  = 3
AMBIENT_LIGHT_INT     = 4
PROXIMITY_INT         = 5
SLEEP_AFTER_INT       = 6
ALL                   = 7

# LED Drive values
LED_DRIVE_100MA       = 0
LED_DRIVE_50MA        = 1
LED_DRIVE_25MA        = 2
LED_DRIVE_12_5MA      = 3

# Proximity Gain (PGAIN) values
PGAIN_1X              = 0
PGAIN_2X              = 1
PGAIN_4X              = 2
PGAIN_8X              = 3

# ALS Gain (AGAIN) values
AGAIN_1X              = 0
AGAIN_8X              = 1
AGAIN_16X             = 2
AGAIN_120X            = 3

# Interrupt clear values
CLEAR_PROX_INT        = 0xE5
CLEAR_ALS_INT         = 0xE6
CLEAR_ALL_INTS        = 0xE7

# Default values
DEFAULT_ATIME         = 0xFF
DEFAULT_WTIME         = 0xFF
DEFAULT_PTIME         = 0xFF
DEFAULT_PPULSE        = 0x08
DEFAULT_POFFSET       = 0       # 0 offset
DEFAULT_CONFIG        = 0
DEFAULT_PDRIVE        = LED_DRIVE_100MA
DEFAULT_PDIODE        = 2
DEFAULT_PGAIN         = PGAIN_8X
DEFAULT_AGAIN         = AGAIN_16X
DEFAULT_PILT          = 0       # Low proximity threshold
DEFAULT_PIHT          = 50      # High proximity threshold
DEFAULT_AILT          = 0xFFFF  # Force interrupt for calibration
DEFAULT_AIHT          = 0
DEFAULT_PERS          = 0x22    # 2 consecutive prox or ALS for int.

# ALS coefficients
DF                    = 52
GA                    = 0.49
B                     = 1.862
C                     = 0.746
D                     = 1.291
