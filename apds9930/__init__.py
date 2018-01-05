#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module allows you to interface with an Avago APDS-9930 I2C
ambient light and proximity sensor from Python.

The bindings are easy to use: just create an instance of the
APDS9930 class passing the bus number as a parameter, and optionally
the device's I2C address, if it differs from the default (0x39, 57).

Almost all features are provided through properties, which can just
be read or set to retrieve or send the value to/from the device.

Methods are provided to do some more complex operations that require
a minimum pre-initialization: :py:meth:`~APDS9930.enable_proximity_sensor` and
:py:meth:`~APDS9930.enable_ambient_light_sensor`. Those two sensors can also be enabled
manually by setting the required settings first and then setting
:py:attr:`~APDS9930.power` and :py:attr:`~APDS9930.proximity_sensor` or :py:attr:`~APDS9930.ambient_light_sensor` to True to turn
them on.
"""

__all__ = ("APDS9930", "regs")

import smbus
from .values import *

class APDS9930_I2C_Base(object):
    """
    Base class for APDS9930 that provides basic I2C communication
    methods, specifically adapted for this device.

    bus must be an integer curresponding to
    the I2C bus you want to use. address is the I2C address of the
    device.
    """
    def __init__(self, bus, address):
        self._bus = smbus.SMBus()
        self._bus.open(bus)
        self.address = address

    def write_byte(self, data):
        """
        Write a byte to the specified address. Useful to interact with
        the COMMAND register directly.
        """
        self._bus.write_byte(self.address, data)

    def write_byte_data(self, reg, data, mode=AUTO_INCREMENT):
        """
        Write a byte to a specific register. mode can be found in
        apds9930.values, and can be :py:const:`~apds9930.values.AUTO_INCREMENT`, :py:const:`~apds9930.values.REPEATED_BYTE`
        or :py:const:`~apds9930.values.SPECIAL_FN`. Check the device's datasheet for more information.
        """
        self._bus.write_byte_data(self.address, reg | mode, data)

    def write_block_data(self, reg, data, mode=AUTO_INCREMENT):
        """
        Write a block starting from a specific register. Mode should
        be set to :py:const:`~apds9930.values.AUTO_INCREMENT`, so that the device automatically
        selects the following register before writing the next byte.
        """
        self._bus.write_i2c_block_data(self.address, reg | mode, data)

    def read_byte(self):
        """
        Read a byte from the I2C bus.
        """
        return self._bus.read_byte(self.address)

    def read_byte_data(self, reg, mode=AUTO_INCREMENT):
        """
        Read a byte from the specified address.
        """
        return self._bus.read_byte_data(self.address, reg | mode)

    def read_block_data(self, reg, len, mode=AUTO_INCREMENT):
        """
        Read a block with size len starting from the specified address.
        """
        return self._bus.read_i2c_block_data(self.address, reg | mode, len)

    def close(self):
        """
        Close the I2C bus.
        """
        self._bus.close()

class APDS9930(APDS9930_I2C_Base):
    """
    The APDS-9930 I2C interface class. Pass the :py:data:`~bus` number and,
    if it's different from 0x39 (57), the device :py:data:`address` as arguments.

    The device is initialized with the default settings. bus must be an
    int curresponding to the number of the I2C bus you want to use.
    :py:data:`address` is optional and is the I2C address of the device, if different
    from the default (0x39).
    """

    def __init__(self, bus, address=APDS9930_I2C_ADDR):
        super(APDS9930, self).__init__(bus, address)

        self.address = HexInt(self.address) # For aesthetic purposes only

        # Check device ID against preset values
        if self.id not in APDS9930_IDs:
            raise SensorError("Device ID not recognized: {0}".format(hex(self.id)))
        
        # Turn off all features (set ENABLE to 0x00)
        self.set_mode(ALL, OFF)

        # Set default values for ambient light and proximity registers
        self.write_byte_data(APDS9930_ATIME, DEFAULT_ATIME)
        self.write_byte_data(APDS9930_WTIME, DEFAULT_WTIME)
        self.write_byte_data(APDS9930_PPULSE, DEFAULT_PPULSE)
        self.write_byte_data(APDS9930_POFFSET, DEFAULT_POFFSET)
        self.write_byte_data(APDS9930_CONFIG, DEFAULT_CONFIG)

        self.led_drive = DEFAULT_PDRIVE
        self.proximity_gain = DEFAULT_PGAIN
        self.ambient_light_gain = DEFAULT_AGAIN
        self.proximity_diode = DEFAULT_PDIODE
        self.proximity_int_low_threshold = DEFAULT_PILT
        self.proximity_int_high_threshold = DEFAULT_PIHT
        self.light_int_low_threshold = DEFAULT_AILT
        self.light_int_high_threshold = DEFAULT_AIHT

        self.write_byte_data(APDS9930_PERS, DEFAULT_PERS)

    @property
    def id(self):
        """
        The ID of the device, stored in the ID register.
        """
        return HexInt(self.read_byte_data(APDS9930_ID))
    
    @property
    def mode(self):
        """
        The value of the ENABLE register, which stores
        the enabled features of the sensor. You should not set this
        property directly unless you know what you're doing. Use :py:meth:`.set_mode`
        and/or the specific feature methods instead.
        """
        return BinInt(self.read_byte_data(APDS9930_ENABLE), byte=True)
    @mode.setter
    def mode(self, value):
        self.write_byte_data(APDS9930_ENABLE, value)

    def get_mode(self, mode):
        """
        Gets the state of a specific feature in the ENABLE
        register. Good values for mode are:

        ======================= ===
        Mode                     # 
        ======================= ===
        POWER                    0
        AMBIENT_LIGHT            1
        PROXIMITY                2
        WAIT                     3
        AMBIENT_LIGHT_INT        4
        PROXIMITY_INT            5
        SLEEP_AFTER_INT          6
        ======================= ===

        The specified feature is either enabled or disabled depending
        on whether the method returns True or False
        """
        return bool((self.mode & (1 << mode)) >> mode)

    def set_mode(self, mode, enable):
        """
        Like :py:meth:`.get_mode`, but changes the mode instead. The :py:data:`~enable` argument
        determines whether the feature specified by mode will be enabled or
        disabled. The method accepts one additional argument as :py:data:`~mode`,

        ======================= ===
        Mode                     # 
        ======================= ===
        ALL                      7
        ======================= ===

        which enables or disables all features at once.

        The specified feature will either be enabled or disabled depending
        on whether :py:data:`enable` is True or False
        """
        reg_val = self.mode

        if mode >= 0 and mode <= 6:
            if enable:
                reg_val |= 1 << mode
            else:
                reg_val &= -(1 << mode)
        elif mode == ALL:
            reg_val = 0x7F if enable else 0x00

        self.mode = reg_val

    @property
    def power(self):
        """
        Turn on or off the internal oscillator (mode, boolean).
        """
        return self.get_mode(POWER)
    @power.setter
    def power(self, value):
        self.set_mode(POWER, value)

    @property
    def ambient_light_sensor(self):
        """
        Enable or disable the ambient light sensor (mode, boolean).
        """
        return self.get_mode(AMBIENT_LIGHT)
    @ambient_light_sensor.setter
    def ambient_light_sensor(self, value):
        self.set_mode(AMBIENT_LIGHT, value)
        
    @property
    def proximity_sensor(self):
        """
        Enable or disable the proximity sensor (mode, boolean).
        """
        return self.get_mode(PROXIMITY)
    @proximity_sensor.setter
    def proximity_sensor(self, value):
        self.set_mode(PROXIMITY, value)
        
    @property
    def wait_timer(self):
        """
        Enable or disable the wait timer feature (mode, boolean).
        """
        return self.get_mode(WAIT)
    @wait_timer.setter
    def wait_timer(self, value):
        self.set_mode(WAIT, value)
        
    @property
    def enable_ambient_light_interrupt(self):
        """
        Enable or disable the ambient light interrupt (mode, boolean).
        """
        return self.get_mode(AMBIENT_LIGHT_INT)
    @enable_ambient_light_interrupt.setter
    def enable_ambient_light_interrupt(self, value):
        self.set_mode(AMBIENT_LIGHT_INT, value)
        
    @property
    def enable_proximity_interrupt(self):
        """
        Enable or disable the proximity interrupt (mode, boolean).
        """
        return self.get_mode(PROXIMITY_INT)
    @enable_proximity_interrupt.setter
    def enable_proximity_interrupt(self, value):
        self.set_mode(PROXIMITY_INT, value)
        
    @property
    def sleep_after_interrupt(self):
        """
        Enable or disable the sleep after interrupt feature. If True,
        the device will power down after an interrupt has been generated
        (mode, boolean).
        """
        return self.get_mode(SLEEP_AFTER_INT)
    @sleep_after_interrupt.setter
    def sleep_after_interrupt(self, value):
        self.set_mode(SLEEP_AFTER_INT, value)

    def enable_ambient_light_sensor(self, interrupt=False):
        """
        Set all the needed values to turn on the ambient light
        sensor and turn it on.
        If interrupt is True, ALS interrupts will also be enabled.
        """

        self.ambient_light_gain = DEFAULT_AGAIN
        self.ambient_light_interrupt = interrupt
        self.power = True
        self.ambient_light_sensor = True

    def enable_proximity_sensor(self, interrupt=False):
        """
        Set all the needed values to turn on the proximity
        sensor and turn it on.
        If interrupt is True, proximity interrupts will also
        be enabled.
        """

        self.proximity_gain = DEFAULT_PGAIN
        self.led_drive = DEFAULT_PDRIVE
        self.proximity_diode = DEFAULT_PDIODE
        self.enable_proximity_interrupt = interrupt
        self.power = True
        self.proximity_sensor = True


    @property
    def ch0_light(self):
        """
        Light data from channel 0. Read-only.
        """
        l = self.read_byte_data(APDS9930_Ch0DATAL)
        h = self.read_byte_data(APDS9930_Ch0DATAH)

        return l + (h << 8)

    @property
    def ch1_light(self):
        """
        Light data from channel 1. Read-only.
        """
        l = self.read_byte_data(APDS9930_Ch1DATAL)
        h = self.read_byte_data(APDS9930_Ch1DATAH)

        return l + (h << 8)

    @property
    def ambient_light(self):
        """
        Ambient light value in lux (read-only).
        """
        ch0, ch1 = self.ch0_light, self.ch1_light
        return self.ambient_to_lux(ch0, ch1)

    def ambient_to_lux(self, ch0, ch1):
        """
        Accepts data from both channels and returns a value
        in lux (according to the datasheet).
        """

        ALSIT = 2.73 * (256 - DEFAULT_ATIME)
        iac = max(ch0 - B * ch1, C * ch0 - D * ch1)
        lpc = GA * DF / (ALSIT * self.ambient_light_gain)
        return iac * lpc

    @property
    def proximity(self):
        """
        Proximity data. Read-only.
        """
        l = self.read_byte_data(APDS9930_PDATAL)
        h = self.read_byte_data(APDS9930_PDATAH)

        return l + (h << 8)

    @property
    def proximity_int_low_threshold(self):
        """
        Proximity interrupt low threshold.
        """
        l = self.read_byte_data(APDS9930_PILTL)
        h = self.read_byte_data(APDS9930_PILTH)

        return l + (h << 8)
    @proximity_int_low_threshold.setter
    def proximity_int_low_threshold(self, value):
        h = value >> 8
        l = value & 0x00FF

        self.write_byte_data(APDS9930_PILTL, l)
        self.write_byte_data(APDS9930_PILTH, h)

    @property
    def proximity_int_high_threshold(self):
        """
        Proximity interrupt high threshold.
        """
        l = self.read_byte_data(APDS9930_PIHTL)
        h = self.read_byte_data(APDS9930_PIHTH)

        return l + (h << 8)
    @proximity_int_high_threshold.setter
    def proximity_int_high_threshold(self, value):
        h = value >> 8
        l = value & 0x00FF

        self.write_byte_data(APDS9930_PIHTL, l)
        self.write_byte_data(APDS9930_PIHTH, h)

    @property
    def led_drive(self):
        """
        LED drive strength for proximity and ALS. Good values
        are:

        ======== ============== ============================================
        Value    LED Current    :py:data:`apds9930.values` constant name
        ======== ============== ============================================
        0        100 mA         :py:const:`~apds9930.values.LED_DRIVE_100MA`
        1        50 mA          :py:const:`~apds9930.values.LED_DRIVE_50MA`
        2        25 mA          :py:const:`~apds9930.values.LED_DRIVE_25MA`
        3        12.5 mA        :py:const:`~apds9930.values.LED_DRIVE_12_5MA`
        ======== ============== ============================================
        """
        reg_val = self.read_byte_data(APDS9930_CONTROL)
        v =  (reg_val >> 6) & 3     # 3 = 00000011

        return DictReprInt(v, mapping={0: "LED_DRIVE_100MA",
                                       1: "LED_DRIVE_50MA",
                                       2: "LED_DRIVE_25MA",
                                       3: "LED_DRIVE_12_5MA"})

    @led_drive.setter
    def led_drive(self, value):
        reg_val = self.read_byte_data(APDS9930_CONTROL)

        value &= 3                # 3 = 00000011
        value = value << 6
        reg_val &= int("00111111", 2)
        reg_val |= value

        self.write_byte_data(APDS9930_CONTROL, reg_val)

    @property
    def proximity_gain(self):
        """
        Receiver gain for proximity detection. Good values are:

        ======= ========== ====================================
        Value   Gain       :py:data:`apds9930.values` constant name
        ======= ========== ====================================
        0       1x         :py:const:`~apds9930.values.PGAIN_1X`
        1       2x         :py:const:`~apds9930.values.PGAIN_2X`
        2       4x         :py:const:`~apds9930.values.PGAIN_4X`
        3       8x         :py:const:`~apds9930.values.PGAIN_8X`
        ======= ========== ====================================
        """
        reg_val = self.read_byte_data(APDS9930_CONTROL)
        v = (reg_val >> 2) & 3     # 3 = 00000011

        return DictReprInt(v, mapping={0: "PGAIN_1X",
                                       1: "PGAIN_2X",
                                       2: "PGAIN_4X",
                                       3: "PGAIN_8X"})

    @proximity_gain.setter
    def proximity_gain(self, value):
        reg_val = self.read_byte_data(APDS9930_CONTROL)

        value &= 3                # 3 = 00000011
        value = value << 2
        reg_val &= int("11110011", 2)
        reg_val |= value

        self.write_byte_data(APDS9930_CONTROL, reg_val)

    @property
    def proximity_diode(self):
        """
        Diode used for proximity sensor. Good values are:

        ======= ===============
        Value   Diode selection
        ======= ===============
        0       Reserved
        1       Reserved
        2       Use Ch1 diode
        3       Reserved
        ======= ===============
        """
        reg_val = self.read_byte_data(APDS9930_CONTROL)
        v = (reg_val >> 4) & 3     # 3 = 00000011

        return DictReprInt(v, mapping={2: "Ch1 diode"})

    @proximity_diode.setter
    def proximity_diode(self, value):
        reg_val = self.read_byte_data(APDS9930_CONTROL)

        value &= 3                # 3 = 00000011
        value = value << 4
        reg_val &= int("11001111", 2)
        reg_val |= value

        self.write_byte_data(APDS9930_CONTROL, reg_val)

    @property
    def ambient_light_gain(self):
        """
        Receiver gain for ambient light sensor. Good values are:

        ======= ========= ======================================
        Value   Gain      :py:data:`apds9930.values` constant name
        ======= ========= ======================================
        0       1x        :py:const:`~apds9930.values.AGAIN_1X`
        1       4x        :py:const:`~apds9930.values.AGAIN_8X`
        2       16x       :py:const:`~apds9930.values.AGAIN_16X`
        3       64x       :py:const:`~apds9930.values.AGAIN_120X`
        ======= ========= ======================================
        """
        reg_val = self.read_byte_data(APDS9930_CONTROL)
        v = reg_val & 3     # 3 = 00000011

        return DictReprInt(v, mapping={0: "AGAIN_1X",
                                       1: "AGAIN_8X",
                                       2: "AGAIN_16X",
                                       3: "AGAIN_120X"})

    @ambient_light_gain.setter
    def ambient_light_gain(self, value):
        reg_val = self.read_byte_data(APDS9930_CONTROL)

        value &= 3                # 3 = 00000011
        reg_val &= int("11111100", 2)
        reg_val |= value

        self.write_byte_data(APDS9930_CONTROL, reg_val)

    @property
    def ambient_light_int_low_threshold(self):
        """
        Ambient light interrupt low threshold.
        """
        l = self.read_byte_data(APDS9930_AILTL)
        h = self.read_byte_data(APDS9930_AILTH)

        return l + (h << 8)
    @ambient_light_int_low_threshold.setter
    def ambient_light_int_low_threshold(self, value):
        h = value >> 8
        l = value & 0x00FF

        self.write_byte_data(APDS9930_AILTL, l)
        self.write_byte_data(APDS9930_AILTH, h)

    @property
    def ambient_light_int_high_threshold(self):
        """
        Ambient light interrupt high threshold.
        """
        l = self.read_byte_data(APDS9930_AIHTL)
        h = self.read_byte_data(APDS9930_AIHTH)

        return l + (h << 8)
    @ambient_light_int_high_threshold.setter
    def ambient_light_int_high_threshold(self, value):
        h = value >> 8
        l = value & 0x00FF

        self.write_byte_data(APDS9930_AIHTL, l)
        self.write_byte_data(APDS9930_AIHTH, h)

    @property
    def ambient_light_interrupt(self):
        """
        If True, the device is asserting an ambient light interrupt.
        Set it to None to clear it.
        """
        val = self.read_byte_data(APDS9930_STATUS)
        return bool((val >> 4) & 1)
    @ambient_light_interrupt.setter
    def ambient_light_interrupt(self, value):
        if not value:
            self.write_byte(CLEAR_ALS_INT)

    @property
    def proximity_interrupt(self):
        """
        If True, the device is asserting a proximity interrupt.
        Set it to None to clear it.
        """
        val = self.read_byte_data(APDS9930_STATUS)
        return bool((val >> 5) & 1)
    @proximity_interrupt.setter
    def proximity_interrupt(self, value):
        if not value:
            self.write_byte(CLEAR_PROX_INT)
    
    def clear_all_interrupts(self):
        """
        Clear all interrupts.
        """
        self.write_byte(CLEAR_ALL_INTS)

    def dump_registers(self):
        """
        Debug: read all the registers from the device and
        **print** them.
        """
        print "   REGISTER       DECIMAL  HEXADECIMAL     BINARY"
        for reg in REGISTERS:
            val = self.read_byte_data(REGISTERS[reg])
            print "{:<4}  {:>9}    dec {:<3}   hex {:<4}   bin {:08d}".format(hex(REGISTERS[reg]),
                                                                           reg + ":",
                                                                           str(int(val)),
                                                                           hex(val),
                                                                           int(bin(val)[2:]))


class HexInt(int):
    """
    Integer that represents itself as a hex number.
    """
    def __repr__(self):
        return hex(self)

class BinInt(int):
    """
    Integer that represents itself as a binary number.
    If byte is True, the integer will be padded with zeroes
    so that it uses at least 8 binary digits.
    """
    byte = False
    def __init__(self, n, base=10, byte=False):
        self.byte = byte
        if type(n) == int:
            return super(BinInt, self).__init__(n)
        else:
            return super(BinInt, self).__init__(n, base)

    def __new__(cls, n, base=10, byte=False):
        if type(n) == int:
            obj = int.__new__(cls, n)
        else:
            obj = int.__new__(cls, n, base)
        obj.byte = byte
        return obj

    def __repr__(self):
        if self.byte:
            return "0b{:08d}".format(int(bin(self)[2:]))
        else:
            return bin(self)

class DictReprInt(int):
    """
    Integer that represents itself with a name rather than
    a value. Specify the name mappings in the "mapping" argument.
    """
    mapping = {}

    def __init__(self, n, base=10, mapping={}):
        self.mapping = mapping
        if type(n) == int:
            return super(DictReprInt, self).__init__(n)
        else:
            return super(DictReprInt, self).__init__(n, base)

    def __new__(cls, n, base=10, mapping={}):
        if type(n) == int:
            obj = int.__new__(cls, n)
        else:
            obj = int.__new__(cls, n, base)
        obj.mapping = mapping
        return obj

    def __repr__(self):
        if int(self) in self.mapping:
            return super(DictReprInt, self).__repr__() + " = " + self.mapping[self]
        else:
            return super(DictReprInt, self).__repr__()

class SensorError(EnvironmentError):
    """
    Raised when a non-I2C-specific error occurs (for example, the
    device ID is not recognized, which usually means the device is
    not hooked up properly).

    If issues with the I2C occur, an IOError will be raised.
    """
    pass
