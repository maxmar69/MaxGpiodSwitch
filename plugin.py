# Gpiod Switch plugin
#
# Author: massimo.marconi@mail.com
#
#
"""
<plugin key="MaxGpiodSwitch" name="Gpiod Switch plugin" author="massimo.marconi@mail.com" version="1.0.0" wikilink="https://github.com/maxmar69/MaxGpiodSwitch" >
    <description>
        <h2>Gpiod Switch plugin</h2><br/>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li style="line-height:normal">Switches - Comma-delimited list of information for the creation of switch-type devices. 
                Format is: PinNo:SwitchType:SwitchInitialStatus where SwitchType may be 'N' for Normal or I for inverted. (e.g. 27:N:0)</li>
            <li style="line-height:normal">Chip path - chip_path of the GPIO controller where pins are connected (es. /dev/gpiochip0)</li>
            <li style="line-height:normal">Debug - Can be usefull to increase the logging level for troubleshooting</li>
        </ul>
    </description>
    <params>
        <param field="Mode1" label="Switches" width="400px"/>
        <param field="Mode2" label="Chip path" default="/dev/gpiochip0"/>
        <param field="Mode3" label="Debug" width="150px">
            <options>
                <option label="None" value="0"  default="true" />
                <option label="Python Only" value="2"/>
                <option label="Basic Debugging" value="62"/>
                <option label="Event Queue" value="128"/>
                <option label="All" value="-1"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz

#import time

import gpiod

from gpiod.line import Direction, Value

valoreGlobale={}


def get_line_intvalue(chip_path, line_offset):
    with gpiod.request_lines(
        chip_path,
        consumer="get_line_intvalue",
        config={line_offset: gpiod.LineSettings(direction=Direction.INPUT)},
    ) as request:
        value = request.get_value(line_offset)
        Domoticz.Log("Value="+str(value))
        if (value == Value.ACTIVE):
          return(1)
        else:
          return(0)  


def write_line_intvalue(chip_path, line_offset, line_type, intvalue):
    if (line_type == "I"):
      if (intvalue == 0):
         valore=Value.INACTIVE
      else:
         valore=Value.ACTIVE
    else:
      if (intvalue == 0):
         valore=Value.ACTIVE 
      else:    
        valore=Value.INACTIVE
       
    with gpiod.request_lines(
        chip_path,
        consumer="write_line_intvalue",
        config={line_offset: gpiod.LineSettings(direction=Direction.OUTPUT)},
    ) as request:
         request.set_value(line_offset, valore)
                     
                     
                         
                        
def onStart():
    global valoreGlobale
    if Parameters["Mode3"] != "0":
        Domoticz.Log("Parameter is: '"+Parameters["Mode3"]+"'")
        Domoticz.Debugging(int(Parameters["Mode3"]))
        DumpConfigToLog()

    # Process Device
    if (len(Parameters["Mode2"]) > 0):
       chip_path=Parameters["Mode2"]
    else:
       Domoticz.Error("Device field is empty")
       raise 
    
    # Process Output Pins
    Domoticz.Log("passo1")
    if (len(Parameters["Mode1"]) > 0):
        try:
            pins = Parameters["Mode1"].split(',')
            for pin in pins:
                items = pin.split(':')
                pinNo = int(items[0])
                pinType = items[1]
 
                if (len(items[2]) > 0):
                   pinInitial=int(items[2])
                else:
                   Domoticz.Error("No initial value set for pin "+str(pinNo) )
                   raise
                                
                valoreGlobale[pinNo] = {
                  "type": pinType,
                  "initial": pinInitial
                }    
                if not (pinNo in Devices):
                    Domoticz.Log("Creating device #"+items[0])
                    Domoticz.Device(Name="Pin "+items[0], Unit=pinNo, TypeName="On/Off").Create()
                Domoticz.Log("Set initial value for pin "+str(pinNo)+" to "+str(pinInitial) )
                write_line_intvalue(chip_path, pinNo, pinType, pinInitial )
                UpdateDevice(pinNo, pinInitial, "", 0)
                    
        except Exception as inst:
            Domoticz.Error("Exception in onStart, processing Output Pins")
            Domoticz.Error("Exception detail: '"+str(inst)+"'")
            raise

def onCommand(Unit, Command, Level, Hue):
    
    Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
    chip_path=Parameters["Mode2"]
    if (Command == "On"): 
       campo=1
    else: 
       campo=0
       
    write_line_intvalue(chip_path, Unit, valoreGlobale[Unit]["type"], campo)    
    UpdateDevice(Unit, campo, "", 0)

def onStop():
    Domoticz.Debug("onStop called")

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Log( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Log("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Log("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Log("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Log("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Log("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Log("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Log("Device LastLevel: " + str(Devices[x].LastLevel))
    return
    
def UpdateDevice(Unit, nValue, sValue, TimedOut):
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue) or (Devices[Unit].TimedOut != TimedOut):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return
