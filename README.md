# MaxGpiodSwitch
A Domoticz plugin that controls GPIO pins on a Raspberry Pi via libgpiod library.

## Key Features
Creates one Domoticz device per relay.

## Installation 

To install:
- Open terminal
- Run: `sudo pip3 install gpiod`
- Go in your Domoticz directory (e.g./home/pi/domoticz), open the plugins directory.
- Run: `git clone https://github.com/maxmar69/MaxGpiodSwitch`
- Restart Domoticz.

Once installed open domoticz web UI, navigate to the Hardware page. In the hardware dropdown there will be an entry called "Gpiod Switch plugin".

## Updating

To update:
- Open terminal
- Go in your Domoticz directory (e.g./home/pi/domoticz), open the plugins directory then the Gpiod Switch plugin directory.
- Run: `git pull`
- Restart Domoticz.


## Configuration 

### Fields:
#### Switches
Comma-delimited list of information for the creation of switch-type devices. 
Each pin must then have the following form:
PinNo:SwitchType:SwitchInitialStatus.
Where:
- **PinNo** is the GPIO number of the pin asocated to the switch (e.g.27).
- **SwitchType** 
  can be: `N` or `I` respectively for Normal or Inverted. 
  If Normal when the switch is on the PIN value will be high and when it is off it will be low. 
  If it is Inverted when the switch is on the PIN value will be low and when it is off it will be high. 
- **SwitchInitialStatus** 
  is the initial state of the switch: it can be set to 1 (On) or 0 (Off)
Example:
27:N:0,22:I:1 
Creates:
- one switch device linked to PIN 27, type normal, initally turned ON
- one switch device linked to PIN 22, type inverted, initally turned OFF

#### Chip path
The chip path in libgpiod represents the device file path that identifies a specific GPIO controller in the system. 
On Linux, GPIO controllers are exposed in the file system as devices under /dev and are called gpiochipX, where X is an integer identifying the chip.
Usually it can be set to `/dev/gpiochip0` so this is the defautl value.

#### Debug 
Can be usefull to increase the logging level for troubleshooting

## Change log

| Version | Information    |
| ------- | -------------- |
| 1.0.0   | Inital version |
