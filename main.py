import configparser
import ImageReader as IR
from os.path import exists
import os



#Config and Calibration
def create_config():
    print("------Configuration and Calibration------")
    print("About how many seconds does it take from when an object \nenters the camera frame to when it reaches the center?")
    LagTime = input()
    print("""The average pixel value will now be calculated, please \n run the 
    machine with nothing on it until calibration is complete.  Press enter to continue.""")
    input()
    ColorAverage = IR.ImageAverageCalibration()
    print("""We will now get the difference for the piece closest in color to your background.
     \nPlease place that piece on the machine \n and press enter when it is centered.""")
    input()
    PieceAverage = IR.ImageAverageCalibration()
    MinimumTolerance = (ColorAverage - PieceAverage) - 1
    print("""Minimum Tolerance Set. If you have issues where pieces are not detected \n
    please lower the tolerance. If the program is taking empty photos please raise the tolerance.
    \n It is located in config.ini under 'Calibration' and 'Minimum Tolerance'""")
    print("Calibration Complete.")

    #Generate Config File
    config = configparser.ConfigParser()
    config.add_section('Settings')
    config.add_section('Calibration')
    config.set('Settings', 'Lag Time', str(LagTime))
    config.set('Settings', 'Camera Source', '1')
    config.set('Calibration', 'Color Average', str(ColorAverage))
    config.set('Calibration', 'Minimum Tolerance', str(MinimumTolerance))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
    if not os.path.isdir('images'):
        os.mkdir('images')

    print("Config file created, to redo this setup delete config.ini and restart the program.")
    print("------END CONFIGURATION AND CALIBRATION------")
    print("")
    print("")
    print("Would you like to run the program now? (y/n)")
    if input() == "y":
        IR.Run()
    else:
        print("Exiting...")
        exit()

if exists("config.ini"):
    RunTest = True
    while RunTest:
        #print("Press enter to run test.")
        #input()
        #TestAverage = IR.GetTestImage()
        #print(TestAverage)
        #print("Run again? (y/n)")
        #if input() == "n":
            #RunTest = False
        IR.Run()
else:
    create_config()