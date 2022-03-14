########################

ProgramOfTimeScheduledEvents_ReubenPython2and3Class

Class to execute a "program" of time-scheduled-events (includes the ability to hook to Tkinter GUI).
For example, say that we wanted a solenoid to turn on at time = 1sec, a servo to spin at time = 1.5sec,
and then a beep to sound at 3.0sec. A simple JSON file with actuator names and timestamps could be
passed to this class to schedule those events, and this class would then fire them according to the schedule.
The GUI portion of this class includes "play", "pause", and "stop" buttons
(with a checkbox to allow pausing-between-events and a spinbox to enter a non-0-starting-index for events).

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision D, 03/13/2022

Verified working on: 
Python 2.7, 3.8.
Windows 8.1, 10 64-bit
Raspberry Pi Buster 
(no Mac testing yet)

########################  

########################### Python module installation instructions, all OS's

No special Python modules to be installed.

###########################

########################### Library/driver installation instructions, Windows/Linux/RaspberryPi

No libraries to be installed.

###########################
