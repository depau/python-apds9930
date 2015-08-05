# -*- coding: utf-8 -*-

REPEATED_BYTE         = 0x80
AUTO_INCREMENT        = 0xA0
SPECIAL_FN            = 0xE0

# APDS-9930 I2C address
APDS9930_I2C_ADDR     = 0x39

# Command register modes
REPEATED_BYTE         = 0x80
AUTO_INCREMENT        = 0xA0
SPECIAL_FN            = 0xE0

# Error code for returned values
ERROR                 = 0xFF

# Acceptable device IDs
APDS9930_IDs          = [0x39]

# Misc parameters
FIFO_PAUSE_TIME       = 30      # Wait period (ms) between FIFO reads

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
