# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 07/16/2022

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#########################################################
import os
import sys
import platform
import time
import datetime
import math
import collections
from copy import * #for deep_copy of dicts
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
#########################################################

#########################################################
if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input
######################################################### #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

class ProgramOfTimeScheduledEvents_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = -1
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PlayProgramFromThisStartingIndexIntoEventsList = 0
        self.ProgramCurrentlyRunningFlag = -1
        self.ProgramCurrentlyPausedFlag = -1
        self.ProgramCurrentlyInMemory_TotalNumberOfEventsInProgram = -1
        self.LastProgramEventIndex_AtTimeOfSoftwareLaunch = -11111
        self.ProgramCurrentlyRunning_IndexInto_AllActuators_TimestampInSecondsEventsList = -1
        self.ProgramElapsedTimeSeconds = -1.0
        self.ProgramStartTime = -11111.0
        self.ProgramPausedTime = -11111.0
        self.ProgramUnpausedTime = -11111.0
        self.ProgramPausedTime_CumulativeSum = -11111.0
        self.PlayCurrentProgramFromBeginning_FunctionNeedsToCalledFlag = -1
        self.PlayCurrentProgramFromPausedState_FunctionNeedsToCalledFlag = -1
        self.PauseRunningCurrentProgram_FunctionNeedsToCalledFlag = -1
        self.StopRunningCurrentProgram_FunctionNeedsToCalledFlag = -1
        self.ProgramDictOfListsOfEventTimestampsRelativeToZero = dict()
        self.AllActuators_TimestampInSecondsEventsList = list()
        self.StepThroughProgramPausingBetweenEventsFlag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.EventsToFireQueue = Queue.Queue()
        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: ERROR, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 0.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))

        #print("GUIparametersDict = " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Program_Dict" in setup_dict:
            self.Program_Dict = setup_dict["Program_Dict"]

        else:
            self.Program_Dict = dict([("ListOfEventDicts", [{"DeltaTsec_ToFireThisEventAfterPriorEvent":1.000, "Actuator":"DUMMY", "ValueToBeSet": 1, "StringToPrint": "DUMMY EVENT 1"}, {"DeltaTsec_ToFireThisEventAfterPriorEvent":2.000, "Actuator":"DUMMY", "ValueToBeSet": 2, "StringToPrint": "DUMMY EVENT 2"}, {"DeltaTsec_ToFireThisEventAfterPriorEvent":3.000, "Actuator":"DUMMY", "ValueToBeSet": 3, "StringToPrint": "DUMMY EVENT 3"}])])

        print("Program_Dict: " + str(self.Program_Dict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
        self.MainThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.USE_GUI_FLAG == 1:
            self.StartGUI(self.root)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
        #########################################################
        #########################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def __del__(self):
        pass
    #######################################################################################################################
    #######################################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_IntOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = int(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitTextEntryInput_IntOutputOnly(self, min_val, max_val, test_val, TextEntryObject):

        test_val = float(test_val)  # MUST HAVE THIS LINE TO CATCH STRINGS PASSED INTO THE FUNCTION

        if test_val > max_val:
            test_val = max_val
        elif test_val < min_val:
            test_val = min_val
        else:
            test_val = test_val

        test_val = int(test_val)

        if TextEntryObject != "":
            if isinstance(TextEntryObject, list) == 1:  # Check if the input 'TextEntryObject' is a list or not
                TextEntryObject[0].set(str(test_val))  # Reset the text, overwriting the bad value that was entered.
            else:
                TextEntryObject.set(str(test_val))  # Reset the text, overwriting the bad value that was entered.

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        self.MostRecentDataDict = dict([("EventsToFireQueue", self.EventsToFireQueue), ("Time", self.CurrentTime_CalculatedFromMainThread)])

        return self.MostRecentDataDict
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateProgramDict(self, NewProgramDict):

        self.Program_Dict = deepcopy(NewProgramDict)
        print("UpdateProgramDict Event fired! Program_Dict = " + str(self.Program_Dict))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromMainThread = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## unicorn
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for ProgramOfTimeScheduledEvents_ReubenPython2and3Class object.")

        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ###############################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ###############################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ###############################################

            ###################################################################################################### Start Control Law
            ######################################################################################################
            ######################################################################################################
            ######################################################################################################
            ######################################################################################################

            #######################################################################
            #######################################################################
            #######################################################################
            #######################################################################

            ###################################################
            if self.PlayCurrentProgramFromBeginning_FunctionNeedsToCalledFlag == 1:
                self.PlayCurrentProgramFromBeginning()
                self.PlayCurrentProgramFromBeginning_FunctionNeedsToCalledFlag = 0
            ###################################################

            ###################################################
            if self.PlayCurrentProgramFromPausedState_FunctionNeedsToCalledFlag == 1:
                self.PlayCurrentProgramFromPausedState()
                self.PlayCurrentProgramFromPausedState_FunctionNeedsToCalledFlag = 0
            ###################################################

            ###################################################
            if self.PauseRunningCurrentProgram_FunctionNeedsToCalledFlag == 1:
                self.PauseRunningCurrentProgram()
                self.PauseRunningCurrentProgram_FunctionNeedsToCalledFlag = 0
            ###################################################

            ###################################################
            if self.StopRunningCurrentProgram_FunctionNeedsToCalledFlag == 1:
                self.StopRunningCurrentProgram()
                self.StopRunningCurrentProgram_FunctionNeedsToCalledFlag = 0
            ###################################################

            #######################################################################
            #######################################################################
            #######################################################################
            #######################################################################

            #######################################################################
            #######################################################################
            #######################################################################
            #######################################################################
            if self.ProgramCurrentlyRunningFlag == 1 and self.ProgramCurrentlyPausedFlag == 0:

                ###################################################
                ###################################################
                ###################################################
                EventToCheck = self.AllActuators_TimestampInSecondsEventsList[self.ProgramCurrentlyRunning_IndexInto_AllActuators_TimestampInSecondsEventsList]
                EventToCheck_TimestampInSeconds = EventToCheck["EventTimestampInSeconds"]

                ###################################################
                EventToCheck_TimestampInSeconds_PlayProgramFromThisStartingIndexIntoEventsList = self.AllActuators_TimestampInSecondsEventsList[self.PlayProgramFromThisStartingIndexIntoEventsList]["EventTimestampInSeconds"]
                EventToCheck_TimestampInSeconds_FirstEvent = self.AllActuators_TimestampInSecondsEventsList[0]["EventTimestampInSeconds"]
                TimeSkippedFor_PlayProgramFromThisStartingIndexIntoEventsList = EventToCheck_TimestampInSeconds_PlayProgramFromThisStartingIndexIntoEventsList - EventToCheck_TimestampInSeconds_FirstEvent
                #print("TimeSkippedFor_PlayProgramFromThisStartingIndexIntoEventsList: " + str(TimeSkippedFor_PlayProgramFromThisStartingIndexIntoEventsList))
                #print("ProgramStartTime: " + str(ProgramStartTime) + "EventToCheck_TimestampInSeconds_FirstEvent: " + str(EventToCheck_TimestampInSeconds_FirstEvent))
                ###################################################

                if self.CurrentTime_CalculatedFromMainThread - self.ProgramPausedTime_CumulativeSum + TimeSkippedFor_PlayProgramFromThisStartingIndexIntoEventsList >= EventToCheck_TimestampInSeconds:

                    ###################################################
                    ###################################################
                    if self.StepThroughProgramPausingBetweenEventsFlag == 1:
                        self.PauseRunningCurrentProgramButtonResponse()
                    ###################################################
                    ###################################################

                    self.EventsToFireQueue.put(EventToCheck)

                    self.MyPrint_WithoutLogFile("Program now executing Event: " + str(EventToCheck))

                    ###################################################
                    ###################################################
                    if self.ProgramCurrentlyRunning_IndexInto_AllActuators_TimestampInSecondsEventsList < len(self.AllActuators_TimestampInSecondsEventsList) - 1:
                        NextEvent = self.AllActuators_TimestampInSecondsEventsList[self.ProgramCurrentlyRunning_IndexInto_AllActuators_TimestampInSecondsEventsList + 1]
                        NextTime = NextEvent["EventTimestampInSeconds"]
                        self.MyPrint_WithoutLogFile("The next Event will execute in " + str(NextTime-EventToCheck["EventTimestampInSeconds"]) + " seconds.")
                    ###################################################
                    ###################################################

                    self.ProgramCurrentlyRunning_IndexInto_AllActuators_TimestampInSecondsEventsList = self.ProgramCurrentlyRunning_IndexInto_AllActuators_TimestampInSecondsEventsList + 1

                    self.ProgramElapsedTimeSeconds = (self.CurrentTime_CalculatedFromMainThread - self.ProgramPausedTime_CumulativeSum + TimeSkippedFor_PlayProgramFromThisStartingIndexIntoEventsList - self.ProgramStartTime)

                    ###################################################
                    ###################################################
                    if self.ProgramCurrentlyRunning_IndexInto_AllActuators_TimestampInSecondsEventsList == self.ProgramCurrentlyInMemory_TotalNumberOfEventsInProgram:
                        self.MyPrint_WithoutLogFile("&&&&&&&&&&&&&&&&&&&& Successfully completed the program! &&&&&&&&&&&&&&&&&&&&")
                        self.StopRunningCurrentProgram()
                    ###################################################
                    ###################################################

                ###################################################
                ###################################################
                ###################################################

            #######################################################################
            #######################################################################
            #######################################################################
            #######################################################################

            ######################################################################################################
            ######################################################################################################
            ######################################################################################################
            ######################################################################################################
            ###################################################################################################### End Control Law

            ############################################### USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            ###############################################
            ###############################################
            self.UpdateFrequencyCalculation_MainThread()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                time.sleep(self.MainThread_TimeToSleepEachLoop)

            ###############################################
            ###############################################
            ###############################################

        ###############################################

        self.MyPrint_WithoutLogFile("Finished MainThread for ProgramOfTimeScheduledEvents_ReubenPython2and3Class object.")

        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for ProgramOfTimeScheduledEvents_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent):

        self.GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=(GuiParent,))
        self.GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        self.GUI_Thread_ThreadingObject.start()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for ProgramOfTimeScheduledEvents_ReubenPython2and3Class object.")

        ###########################################################
        ###########################################################
        self.root = parent
        self.parent = parent
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan = self.GUI_COLUMNSPAN,
                          sticky =self.GUI_STICKY)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150)  # RGB
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightBlueColor = '#%02x%02x%02x' % (150, 150, 255)  # RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.ButtonWidth = 20
        self.ButtonFontSize = 18
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.PlayButtonGuiFrame = Frame(self.myFrame)
        self.PlayButtonGuiFrame.grid(row=0,column=0,padx=self.GUI_PADX,pady=self.GUI_PADY,columnspan=1,rowspan=1)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.PlayCurrentProgramFromBeginningOrPausedStateButton = Button(self.PlayButtonGuiFrame, text="Play Program", state="normal", width=self.ButtonWidth, command=lambda i=1: self.PlayCurrentProgramFromBeginningOrPausedStateButtonResponse())
        self.PlayCurrentProgramFromBeginningOrPausedStateButton.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        self.PlayCurrentProgramFromBeginningOrPausedStateButton.config(font=("Helvetica", self.ButtonFontSize, "bold"))
        self.PlayCurrentProgramFromBeginningOrPausedStateButton.config(bg = self.TKinter_LightGreenColor)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.PlayProgramFromThisStartingIndexIntoEventsList_EntryLabel = Label(self.PlayButtonGuiFrame, text="Starting Index", width=2*self.ButtonWidth, font=("Helvetica", 10))
        self.PlayProgramFromThisStartingIndexIntoEventsList_EntryLabel.grid(row=0, column=1, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1, sticky='w')

        self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_TextContent_NeedsToBeUpdatedFlag = 0

        self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_StringVar = StringVar()

        self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_TextInputBox = Entry(self.PlayButtonGuiFrame,
                                            font=("Helvetica", int(8)),
                                            state="normal",
                                            width=self.ButtonWidth,
                                            textvariable=self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_StringVar,
                                            justify='center')

        self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_StringVar.set(str(self.PlayProgramFromThisStartingIndexIntoEventsList))
        self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_TextInputBox.grid(row=0, column=2, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1, sticky='w')
        self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_TextInputBox.bind('<Return>', lambda event: self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_EventResponse(event))
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.StepThroughProgramPausingBetweenEventsFlag_Checkbutton_Value = DoubleVar()

        self.StepThroughProgramPausingBetweenEventsFlag_Checkbutton = Checkbutton(self.PlayButtonGuiFrame,
                                           width=25,
                                           font=("Helvetica", int(10)),
                                           text="Enable StepThroughProgram",
                                           state="normal",
                                           variable=self.StepThroughProgramPausingBetweenEventsFlag_Checkbutton_Value)

        self.StepThroughProgramPausingBetweenEventsFlag_Checkbutton.grid(row=1, column=1, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=2, rowspan=1)
        self.StepThroughProgramPausingBetweenEventsFlag_Checkbutton.bind('<ButtonRelease-1>', lambda event, name="<ButtonRelease-1>": self.StepThroughProgramPausingBetweenEventsFlag_CheckButton_Response(event, name))
        self.StepThroughProgramPausingBetweenEventsFlag_Checkbutton_Value.set(self.StepThroughProgramPausingBetweenEventsFlag)

        if self.StepThroughProgramPausingBetweenEventsFlag == 1:
            self.StepThroughProgramPausingBetweenEventsFlag_Checkbutton.select()
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.PauseRunningCurrentProgramButton = Button(self.myFrame, text="Pause Program", state="normal", width=self.ButtonWidth, command=lambda i=1: self.PauseRunningCurrentProgramButtonResponse())
        self.PauseRunningCurrentProgramButton.grid(row=1, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1, sticky='w')
        self.PauseRunningCurrentProgramButton.config(font=("Helvetica", self.ButtonFontSize, "bold"))
        self.PauseRunningCurrentProgramButton.config(bg=self.TKinter_LightBlueColor)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.StopRunningCurrentProgramButton = Button(self.myFrame, text="Stop Program", state="normal", width=self.ButtonWidth, command=lambda i=1: self.StopRunningCurrentProgramButtonResponse())
        self.StopRunningCurrentProgramButton.grid(row=2, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1, sticky='w')
        self.StopRunningCurrentProgramButton.config(font=("Helvetica", self.ButtonFontSize, "bold"))
        self.StopRunningCurrentProgramButton.config(bg=self.TKinter_LightRedColor)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.ProgramInfoHUGEfontGuiLabel = Label(self.myFrame, text="ProgramInfoHUGEfontGuiLabel", width=80, font=("Helvetica", int(14), "bold"))
        self.ProgramInfoHUGEfontGuiLabel.grid(row=0, column=1, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.ProgramInfoGuiLabel = Label(self.myFrame, text="ProgramInfoGuiLabel", width=80, font=("Helvetica", int(10)))
        self.ProgramInfoGuiLabel.grid(row=1, column=1, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=3)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.PausedStatesAndValuesInfoGuiLabel = Label(self.myFrame, text="PausedStatesAndValuesInfoGuiLabel", width=50, font=("Helvetica", int(10)))
        self.PausedStatesAndValuesInfoGuiLabel.grid(row=0, column=2, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        print("$$$$$$$$$$ EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=10, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=10)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.GUI_ready_to_be_updated_flag = 1
        ###########################################################
        ###########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:

                    #########################################################
                    #########################################################
                    if self.ProgramCurrentlyRunningFlag == 1:
                        self.PlayCurrentProgramFromBeginningOrPausedStateButton["state"] = "disabled"
                        self.PauseRunningCurrentProgramButton["state"] = "normal"
                        self.StopRunningCurrentProgramButton["state"] = "normal"
                    else:
                        self.PlayCurrentProgramFromBeginningOrPausedStateButton["state"] = "normal"
                        self.PauseRunningCurrentProgramButton["state"] = "disabled"
                        self.StopRunningCurrentProgramButton["state"] = "disabled"
                    #########################################################
                    #########################################################

                    #########################################################
                    #########################################################
                    if self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_TextContent_NeedsToBeUpdatedFlag == 1:
                        self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_StringVar.set(str(self.PlayProgramFromThisStartingIndexIntoEventsList))
                        self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_TextContent_NeedsToBeUpdatedFlag = 0
                    #########################################################
                    #########################################################

                    #########################################################
                    #########################################################
                    if self.ProgramCurrentlyRunningFlag == 1:
                        if self.ProgramCurrentlyPausedFlag == 0:
                            self.ProgramInfoHUGEfontGuiLabel["text"] = "Program Playing"
                            self.ProgramInfoHUGEfontGuiLabel["fg"] = "green" #self.TKinter_LightGreenColor doesn't show well enough
                        else:
                            self.ProgramInfoHUGEfontGuiLabel["text"] = "Program Paused"
                            self.ProgramInfoHUGEfontGuiLabel["fg"] = self.TKinter_LightBlueColor
                    else:
                        self.ProgramInfoHUGEfontGuiLabel["text"] = "Program Stopped."
                        self.ProgramInfoHUGEfontGuiLabel["fg"] = self.TKinter_LightRedColor
                    #########################################################
                    #########################################################

                    #########################################################
                    #########################################################
                    ProgramInfoGuiLabel_TextToDisplay_temp = ""

                    ProgramInfoGuiLabel_TextToDisplay_temp = ProgramInfoGuiLabel_TextToDisplay_temp + \
                        "Time: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 6, 3) + \
                        "\nMain loop frequency (Hz): " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 3, 3) + \
                        "\nProgramCurrentlyRunningFlag: " + str(self.ProgramCurrentlyRunningFlag) + ", started at StartingIndexIntoEventsList = " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.PlayProgramFromThisStartingIndexIntoEventsList, 0, 3) + \
                        "\nProgramCurrentlyPausedFlag: " + str(self.ProgramCurrentlyPausedFlag) + \
                        "\nProgramStartTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ProgramStartTime, 0, 3) + \
                        "\nProgramPausedTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ProgramPausedTime, 0, 3) + \
                        "\nProgramUnpausedTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ProgramUnpausedTime, 0, 3) + \
                        "\nProgramPausedTime_CumulativeSum: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ProgramPausedTime_CumulativeSum, 0, 3) + \
                        "\nTotalNumberOfEventsInProgram: " + str(self.ProgramCurrentlyInMemory_TotalNumberOfEventsInProgram) + \
                        "\nProgramCurrentlyRunning_IndexInto_AllActuators_TimestampInSecondsEventsList: " + str(self.ProgramCurrentlyRunning_IndexInto_AllActuators_TimestampInSecondsEventsList) + \
                        "\nProgramElapsedTimeSeconds: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.ProgramElapsedTimeSeconds, 0, 3) + \
                        "\nStepThroughProgramPausingBetweenEventsFlag:" + str(self.StepThroughProgramPausingBetweenEventsFlag)

                    self.ProgramInfoGuiLabel["text"] = ProgramInfoGuiLabel_TextToDisplay_temp
                    #########################################################
                    #########################################################

                    #########################################################
                    #########################################################
                    PausedStatesAndValuesInfoGuiLabel_TextToDisplay_temp = ""
                    PausedStatesAndValuesInfoGuiLabel_TextToDisplay_temp = PausedStatesAndValuesInfoGuiLabel_TextToDisplay_temp

                    self.PausedStatesAndValuesInfoGuiLabel["text"] = PausedStatesAndValuesInfoGuiLabel_TextToDisplay_temp
                    #########################################################
                    #########################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("ProgramOfTimeScheduledEvents_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, input, print_result_flag = 0):

        result = isinstance(input, list)

        if print_result_flag == 1:
            self.MyPrint_WithoutLogFile("IsInputList: " + str(result))

        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers=4, number_of_decimal_places=3):
        IsListFlag = self.IsInputList(input)

        if IsListFlag == 0:
            float_number_list = [input]
        else:
            float_number_list = list(input)

        float_number_list_as_strings = []
        for element in float_number_list:
            try:
                element = float(element)
                prefix_string = "{:." + str(number_of_decimal_places) + "f}"
                element_as_string = prefix_string.format(element)
                float_number_list_as_strings.append(element_as_string)
            except:
                self.MyPrint_WithoutLogFile(self.TellWhichFileWereIn() + ": ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput ERROR: " + str(element) + " cannot be turned into a float")
                return -1

        StringToReturn = ""
        if IsListFlag == 0:
            StringToReturn = float_number_list_as_strings[0].zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
        else:
            StringToReturn = "["
            for index, StringElement in enumerate(float_number_list_as_strings):
                if float_number_list[index] >= 0:
                    StringElement = "+" + StringElement  # So that our strings always have either + or - signs to maintain the same string length

                StringElement = StringElement.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place

                if index != len(float_number_list_as_strings) - 1:
                    StringToReturn = StringToReturn + StringElement + ", "
                else:
                    StringToReturn = StringToReturn + StringElement + "]"

        return StringToReturn
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def PlayCurrentProgramFromBeginningOrPausedStateButtonResponse(self):

        if self.ProgramCurrentlyRunningFlag == 1:

            if self.ProgramCurrentlyPausedFlag == 1:
                print("PlayCurrentProgramFromPausedStateButtonResponse event fired!")
                self.PlayCurrentProgramFromPausedState_FunctionNeedsToCalledFlag = 1
            else:
                pass

        else:
            print("PlayCurrentProgramFromBeginningButtonResponse event fired!")
            self.PlayCurrentProgramFromBeginning_FunctionNeedsToCalledFlag = 1
    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def StepThroughProgramPausingBetweenEventsFlag_CheckButton_Response(self, event=None, name="default"):  # Have it accept 1 event argument for when it gets binded to Enter Key and Mouse Click

        try:
            temp_value = self.StepThroughProgramPausingBetweenEventsFlag_Checkbutton_Value.get()

            #######################
            if self.my_platform == "pi": #Raspberry Pi handles checkbuttons differently than Windows does
                if temp_value == 0:
                    VariableValue = 0 #Disabling
                elif temp_value == 1:
                    VariableValue = 1
                else:
                    print("StepThroughProgramPausingBetweenEventsFlag_CheckButton_Response ERROR, unexpected checkbutton value of " + str(temp_value))
                    return
            #######################

            #######################
            elif self.my_platform == "windows":
                if temp_value == 0:
                    VariableValue = 1 #Disabling
                elif temp_value == 1:
                    VariableValue = 0
                else:
                    print("StepThroughProgramPausingBetweenEventsFlag_CheckButton_Response ERROR, unexpected checkbutton value of " + str(temp_value))
                    return
            #######################

            #######################
            else:
                if temp_value == 0:
                    VariableValue = 0 #Disabling
                elif temp_value == 1:
                    VariableValue = 1
                else:
                    print("StepThroughProgramPausingBetweenEventsFlag_CheckButton_Response ERROR, unexpected checkbutton value of " + str(temp_value))
                    return
            #######################

            self.StepThroughProgramPausingBetweenEventsFlag = VariableValue
            print("StepThroughProgramPausingBetweenEventsFlag changed to " + str(self.StepThroughProgramPausingBetweenEventsFlag))
        except:
            pass
    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def PlayProgramFromThisStartingIndexIntoEventsList_Entry_EventResponse(self, event = None):

        try:
            PlayProgramFromThisStartingIndexIntoEventsList_TEMP = self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_StringVar.get()

            self.PlayProgramFromThisStartingIndexIntoEventsList = self.LimitTextEntryInput_IntOutputOnly(0.0, 5000.0, PlayProgramFromThisStartingIndexIntoEventsList_TEMP, self.PlayProgramFromThisStartingIndexIntoEventsList_Entry_StringVar)

            self.MyPrint_WithoutLogFile("PlayProgramFromThisStartingIndexIntoEventsList entry input: " + str(self.PlayProgramFromThisStartingIndexIntoEventsList))

        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("PlayProgramFromThisStartingIndexIntoEventsList_Entry_EventResponse ERROR: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def PauseRunningCurrentProgramButtonResponse(self):

        if self.ProgramCurrentlyRunningFlag == 1:
            print("PauseRunningCurrentProgramButtonResponse event fired!")

            if self.ProgramCurrentlyPausedFlag == 1:
                self.PlayCurrentProgramFromPausedState_FunctionNeedsToCalledFlag = 1
            else:
                self.PauseRunningCurrentProgram_FunctionNeedsToCalledFlag = 1

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def StopRunningCurrentProgramButtonResponse(self):

        if self.ProgramCurrentlyRunningFlag == 1:
            print("StopRunningCurrentProgramButtonResponse event fired!")
            self.StopRunningCurrentProgram_FunctionNeedsToCalledFlag = 1

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def PlayCurrentProgramFromBeginning(self):

        print("PlayCurrentProgramFromBeginning event fired!")

        try:

            #################################################################
            #################################################################
            ProgramStartTime_TEMP = self.CurrentTime_CalculatedFromMainThread

            #self.LoadAndParseJSONfile_Program() #Loads program JSON file, parses it, and updates Program_Dict.

            self.AllActuators_TimestampInSecondsEventsList = deepcopy(self.Program_Dict["ListOfEventDicts"])

            self.ProgramEventsCumulativeTime = 0.0
            for ListIndex, ListValue in enumerate(self.AllActuators_TimestampInSecondsEventsList):
                self.ProgramEventsCumulativeTime = self.ProgramEventsCumulativeTime + self.AllActuators_TimestampInSecondsEventsList[ListIndex]["DeltaTsec_ToFireThisEventAfterPriorEvent"]
                self.AllActuators_TimestampInSecondsEventsList[ListIndex]["EventTimestampInSeconds"] = ProgramStartTime_TEMP + self.ProgramEventsCumulativeTime

            #################################################################
            #################################################################

            #################################################################
            #################################################################
            for EventIndex, EventElement in enumerate(self.AllActuators_TimestampInSecondsEventsList):
                EventElement["EventIndex"] = EventIndex
            #################################################################
            #################################################################

            ################################################################# Check for Duplicate events
            #################################################################
            AllActuators_TimestampInSecondsEventsList_NoDuplicateEventsDict = dict()
            AllActuators_TimestampInSecondsEventsList_DuplicateEventsDict = dict()

            for EventElement in self.AllActuators_TimestampInSecondsEventsList:

                EventElementTime = EventElement["EventTimestampInSeconds"]

                #################################################################
                if EventElementTime not in AllActuators_TimestampInSecondsEventsList_NoDuplicateEventsDict:

                    AllActuators_TimestampInSecondsEventsList_NoDuplicateEventsDict[EventElementTime] = list([EventElement]) #Add the entire event

                #################################################################

                #################################################################
                elif EventElementTime in AllActuators_TimestampInSecondsEventsList_NoDuplicateEventsDict:
                    EventToBeSwitchedBetweenDicts = deepcopy(AllActuators_TimestampInSecondsEventsList_NoDuplicateEventsDict[EventElementTime])
                    del AllActuators_TimestampInSecondsEventsList_NoDuplicateEventsDict[EventElementTime]
                    #print("POPPED " + str(EventElementTime) + ", " + str(EventElement))

                    if EventElementTime not in AllActuators_TimestampInSecondsEventsList_DuplicateEventsDict:
                        AllActuators_TimestampInSecondsEventsList_DuplicateEventsDict[EventElementTime] = deepcopy(EventToBeSwitchedBetweenDicts + list([EventElement])) #Append the entire event
                    else:
                        ExistingListInDuplicates = AllActuators_TimestampInSecondsEventsList_DuplicateEventsDict[EventElementTime]
                        AllActuators_TimestampInSecondsEventsList_DuplicateEventsDict[EventElementTime] = deepcopy(ExistingListInDuplicates + EventToBeSwitchedBetweenDicts + list([EventElement])) #Append the entire event
                #################################################################

            #################################################################
            NumberOfNotDuplicates = 0
            for NotDuplicateElementTime in AllActuators_TimestampInSecondsEventsList_NoDuplicateEventsDict:
                NumberOfNotDuplicates = NumberOfNotDuplicates + len(AllActuators_TimestampInSecondsEventsList_NoDuplicateEventsDict[NotDuplicateElementTime])
                print("NOT DUPLICATE EVENT: " + str(AllActuators_TimestampInSecondsEventsList_NoDuplicateEventsDict[NotDuplicateElementTime]))

            NumberOfDuplicates = 0
            for DuplicateElementTime in AllActuators_TimestampInSecondsEventsList_DuplicateEventsDict:
                NumberOfDuplicates = NumberOfDuplicates + len(AllActuators_TimestampInSecondsEventsList_DuplicateEventsDict[DuplicateElementTime])
                print("DUPLICATE EVENT (len = " + str(len(AllActuators_TimestampInSecondsEventsList_DuplicateEventsDict[DuplicateElementTime])) + "): " + str(AllActuators_TimestampInSecondsEventsList_DuplicateEventsDict[DuplicateElementTime]))
            #################################################################

            #################################################################
            print("Length of AllActuators_TimestampInSecondsEventsList = " + str(len(self.AllActuators_TimestampInSecondsEventsList)))
            print("Length of NoDuplicates = " + str(NumberOfNotDuplicates))
            print("Length of Duplicates = " + str(NumberOfDuplicates))
            print("Length of NoDuplicated AND Duplicates TOGETHER = " + str(NumberOfNotDuplicates + NumberOfDuplicates))
            #################################################################

            #################################################################
            #################################################################

            #################################################################
            #################################################################
            if NumberOfDuplicates == 0:

                self.ProgramCurrentlyRunningFlag = 1
                self.ProgramCurrentlyInMemory_TotalNumberOfEventsInProgram = len(self.AllActuators_TimestampInSecondsEventsList)
                self.ProgramCurrentlyPausedFlag = 0
                self.ProgramElapsedTimeSeconds = 0.0
                self.ProgramPausedTime = 0.0
                self.ProgramUnpausedTime = 0.0
                self.ProgramPausedTime_CumulativeSum = 0.0

                self.PlayProgramFromThisStartingIndexIntoEventsList = self.LimitNumber_IntOutputOnly(0, self.ProgramCurrentlyInMemory_TotalNumberOfEventsInProgram, self.PlayProgramFromThisStartingIndexIntoEventsList)

                self.ProgramCurrentlyRunning_IndexInto_AllActuators_TimestampInSecondsEventsList = self.PlayProgramFromThisStartingIndexIntoEventsList

                self.ProgramStartTime = ProgramStartTime_TEMP
                # print("PlayCurrentProgramFromBeginning: ProgramStartTime = " + str(self.ProgramStartTime))

            else:
                self.MyPrint_WithoutLogFile("$$$$$$$$$$$$$$$$$$$$$$$$$$ PlayCurrentProgramFromBeginning ERROR: Duplicate event timestamps were found, will not play program. $$$$$$$$$$$$$$$$$$$$$$$$$$")
            #################################################################
            #################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("PlayCurrentProgramFromBeginning, exceptions: %s" % exceptions)
            traceback.print_exc()
    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def PlayCurrentProgramFromPausedState(self):

        print("PlayCurrentProgramFromPausedState event fired!")

        self.ProgramCurrentlyPausedFlag = 0
        self.ProgramUnpausedTime = self.CurrentTime_CalculatedFromMainThread
        self.ProgramPausedTime_CumulativeSum = self.ProgramPausedTime_CumulativeSum + (self.ProgramUnpausedTime - self.ProgramPausedTime)

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def PauseRunningCurrentProgram(self):

        print("PauseRunningCurrentProgram event fired!")

        self.ProgramCurrentlyPausedFlag = 1
        self.ProgramPausedTime = self.CurrentTime_CalculatedFromMainThread

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def SetAllActuatorsStatesOnOrOffCleanlyFromMainLoop(self):

        self.EventsToFireQueue.put(dict([("DeltaTsec_ToFireThisEventAfterPriorEvent", 0.001), ("Actuator","SetAllActuatorsStatesOnOrOffCleanlyFromMainLoop"), ("ValueToBeSet", 0), ("StringToPrint", "SetAllActuatorsStatesOnOrOffCleanlyFromMainLoop")]))
        #print("SetAllActuatorsStatesOnOrOffCleanlyFromMainLoop event fired!")

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def StopRunningCurrentProgram(self):

        print("StopRunningCurrentProgram event fired!")

        self.ProgramCurrentlyRunningFlag = 0
        self.ProgramCurrentlyPausedFlag = -1
        self.ProgramCurrentlyRunning_IndexInto_AllActuators_TimestampInSecondsEventsList = -1
        self.ProgramElapsedTimeSeconds = -1.0
        self.ProgramCurrentlyInMemory_TotalNumberOfEventsInProgram = -1
        self.ProgramStartTime = -11111.0
        self.ProgramPausedTime = -11111.0
        self.ProgramUnpausedTime = -11111.0
        self.ProgramPausedTime_CumulativeSum = -11111.0

        self.SetAllActuatorsStatesOnOrOffCleanlyFromMainLoop()
    #######################################################################################################################
    #######################################################################################################################