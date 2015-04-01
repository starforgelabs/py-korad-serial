# py-korad-serial
Python library to interface with the Korad KA3005P and related programmable power supplies. 

# Overview

This provides a Python class which wraps the serial communication protocol, and works around a firmware bug or two. 

The object supports the python `with` statement to release the serial port automatically:

```python
from koradserial import KoradSerial

with KoradSerial('/dev/tty.usbmodemfd121') as power_supply:
    print "Model: ", power_supply.model
    print "Status: ", power_supply.status
```

# Requirements

This library uses the pyserial and enum34 libraries. 

# Unit Testing

Connect a small-value resistor (approximately 100Ω) across the positive and negative outputs. 

The unit tests exercise as much as I'm able given my equipment. 

# Class  Documentation

## KoradSerial Class

### Constructor `__init__(port, debug=False)`

The constructor takes a string containing the serial device to attach to. 
It attempts to connect to the power supply immediately. 

If `debug` is set to `True`, then `print` statements will detail the data sent and received.

###  `beep` Attribute

Turns the beep on  or off. 

**Note:** This functionality doesn't appear to work reliably on my units. 

```python
from koradserial import KoradSerial

with KoradSerial('/dev/tty.usbmodemfd121') as power_supply:
    . . .
    power_supply.beep.on()
    . . .
    power_supply.beep.off()
```

### `channels` Attribute

This is an array of channel objects.
Channel 1 is the first element of the array. 
Channel 2 is the second element of the array, etc. 

Thus, for single-channel power supplies `channels[0]` will give access to Channel 1.

Each channel has the following attributes: 

#### `current` Property (read/write) 

Sets or reads the current for the channel as a floating-point number.

Setting the current turns the output *off*.

#### `output_current` Property (read-only)

Returns the output current reported by the power supply as a floating-point number. 
If the output is off, this may be 0.0 or `None`. 

#### `output_voltage` Property (read-only)

Returns the output voltage reported by the power supply as a floating-point number.
If the output is off, this may be 0.0 or `None`. 

#### `voltage` Property (read/write) 

Sets or reads the voltage for the channel as a floating-point number.

Setting the voltage turns the output *off*.

### `close()` Method

Closes the serial port to the power supply.

### `is_open` Property (read-only)

Indicates whether the serial port to the power supply is open.

### `memories` Attribute

This is an array of memory settings.
Memory 1 is the first element of the array.
Memory 2 is the second element of the array.

Thus `memories[0]` will give access to Memory 1.

Each memory has the following attributes:

#### `recall()` Method

This selects the memory, which turns the output off and sets the channels' voltage and current.

#### `save()` Method

This saves the memory's settings.

**Note:** 

Apparently to save a setting to a memory one must do the following: 
* Select the memory with `recall()`.
* Set the channels' voltage and current.
* Save the memory with `save()`.


```python
from koradserial import KoradSerial

with KoradSerial('/dev/tty.usbmodemfd121') as power_supply:
    channel = power_supply.channels[0]
    m1 = power_supply.memories[0]
    
    m1.recall()
    channel.voltage = 1.00
    channel.current = 0.100
    m1.save()
```

### `model` Property (read-only)

Returns the power supply model information. 

### `open()` Method

Opens the serial port to the power supply.

###  `output` Attribute

Turns the output on or off. 

```python
from koradserial import KoradSerial

with KoradSerial('/dev/tty.usbmodemfd121') as power_supply:
    . . .
    power_supply.output.on()
    . . .
    power_supply.output.off()
```

###  `over_current_protection` Attribute

Turns the over current protection on or off. 

```python
from koradserial import KoradSerial

with KoradSerial('/dev/tty.usbmodemfd121') as power_supply:
    . . .
    power_supply.over_current_protection.on()
    . . .
    power_supply.over_current_protection.off()
```

###  `over_voltage_protection` Attribute

Turns the over voltage protection on or off. 

```python
from koradserial import KoradSerial

with KoradSerial('/dev/tty.usbmodemfd121') as power_supply:
    . . .
    power_supply.over_voltage_protection.on()
    . . .
    power_supply.over_voltage_protection.off()
```

### `status` Property (read-only)

Returns a `Status` object (documentation below) containing decoded status information. 

### `track()` Method

Sets the tracking method for multi-channel power supplies. 

**Note:** This is untested.

## `Status` Class

### `beep` Attribute

Indicates the beep on/off state.

**Note:** May not be reliable. 

### `channel1` Attribute

Indicates Channel 1's mode. 

### `channel2` Attribute

Indicates Channel 2's mode. 

### `lock` Attribute

Indicates the lock on/off state.

**Note:** May not be reliable. 

### `output` Attribute

Indicates whether the output is on or off.

### `raw` Attribute

This contains the raw value returned by the `STATUS?` command.

### `tracking` Attribute

Indicates the power supply's tracking state.

# Known Issues

*   Multi-channel functionality has not been tested due to lack of access to an appropriate power supply.
*   There is conflicting information  about the tracking values sent and received. 
    Somebody with a multi-channel power supply will need to verify the values.

