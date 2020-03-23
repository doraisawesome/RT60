# Program: RT60
# Description: This program uses the Sabine equation to calculates the amount of time that
#   it takes for the acoustical energy to drop by 60dB. It will ask user for the room demesion
#   and the material the room is made out of.
#
# Author: Wen Du
# Class: SD93 Scripting
# Instructor: Gary Bourgeois

import random

# load from AC.txt
materials = {}
newMaterials = {}
materialsFileName = "AC.txt"

createRoom = "Create a new room"
addMaterial = "Add a new material"
loadRooms = "Show RT60 of saved rooms"
saveData = "Save"
quitCalc = "Quit"
yes = "Yes"
no = "No"
mainMenuOptions = [createRoom, addMaterial, loadRooms, saveData, quitCalc]
quitMenuOptions = [yes, no]
randomDimentions = "Randomize room dimentions(height, width, length)"
inputDimentions = "Type in room dimentions manually"
createRoomOptions = [randomDimentions, inputDimentions]

# load from RoomMeasurement.txt
rooms = {}
newRooms = {}
roomDataFileName = "RoomMeasurement.txt"

def getUserChoice(options):
    '''
    Generates a numbered menu with given options and returns a valid user choice

    Parameters
    ----------
    options : list
        A list that contains menu options

    Returns
    -------
    int
        User's choice from printed menu
    '''    
    for item in options:
        print(options.index(item) + 1, ". ", item, sep='')
    userChoice = ''

    while not isinstance(userChoice, int):
        try:
            print("Please choose one option from the menu: ")
            userChoice = input("-> ")
            userChoice = int(userChoice)
            while userChoice - 1 not in range(len(options)):
                print("Oops! What you typed is not an option.")
                print("Try again.")
                userChoice = input("-> ")
                userChoice = int(userChoice)
            break
        except ValueError: 
            print("Oops! Not a valid choice...")
            print("Try again.")
    return userChoice

def createNewRoom():
    '''
    Creates a new room from user inputs and updates room dictionary 
    '''
    print('How would you like to measure your room?')
    choice = getUserChoice(createRoomOptions)
    if createRoomOptions[choice - 1] == randomDimentions:
        measurements = randomizeDimentions()
    else:
        measurements = takeRoomMeasurements()
    print("How would you like to name this room?")
    roomName = input("-> ")

    ''' Display a menu of available materials to user then get corresponding 
        coefficient from user's choice '''
    print("What material is this room made out of?")
    materialOptions = list(materials.keys())
    materialCoefficients = list(materials.values())
    materialChoice = getUserChoice(materialOptions)
    materialChoiceCoeff = materialCoefficients[materialChoice - 1]

    ''' Calculate the time that it takes for the acoustical energy to drop by 60dB '''
    decayTime = calculateRT60(measurements, materialChoiceCoeff)
    print()
    print("Reverberation decay time of this room is:", decayTime, 'sec')
    print("-----------------------------------------")
    print()
    measurements.append(materialChoiceCoeff)
    newRooms.update({roomName: measurements})

def randomizeDimentions():
    return [random.uniform(1, 20), random.uniform(1, 20), random.uniform(1, 20)]

def addNewMaterial():
    materialName = input("Name of the material you would like to add: ")
    materialCoeff = ''
    while not isinstance(materialCoeff, float):
        try:
            materialCoeff = input("Absoption coefficient of this material is: ")
            materialCoeff = float(materialCoeff)
            while materialCoeff <= 0:
                print("Oops! Not a valid measurement.")
                print("Try again.")
                materialCoeff = input("Absoption coefficient of this material is: ")
                materialCoeff = float(materialCoeff)
            break
        except ValueError: 
            print("Oops! Not a valid measurement.")
            print("Try again.")
    newMaterials.update({materialName: materialCoeff})

def calculateVolume(height, width, length):
    volume = height * width * length
    return volume


def calculateSurfaceArea(height, width, length):
    surfaceArea = (height * width * 2) + (height * length * 2) + (width * length * 2)
    return surfaceArea


def calculateDecayTime(volume, surfaceArea, absorptionCoeff):
    '''
    Calculates the reverberation decay time using Sabine's equation

    Parameters
    ----------
    volume : float
        Volume of the room that is being calculated
    surfaceArea: float
        Surface area of the room that is being calculated
    absorptionCoeff: float
        Absorption coefficient of the material that current
        room is made out of

    Returns
    -------
    float
        Time that it takes for the acoustical energy to drop by 60dB

    '''
    decayTime = (0.16 * volume) / (surfaceArea * absorptionCoeff)
    return decayTime


def takeRoomMeasurements():
    '''
    Asks user for the height, width and length of a room in meters

    Returns
    -------
    list
        A list contains mesurements of height, width and length of a room
        and each item is a float number

    '''
    demensionsToMeasure = ['height', 'width', 'length']
    measurements = []
    for item in demensionsToMeasure:
        answer = ''
        while not isinstance(answer, float):
            try:
                question = "Please enter the " + item + " of this room (unit: meter)? "
                print(question)
                answer = input("-> ")
                answer = float(answer)
                while answer <= 0:
                    print("Oops! Not a valid measurement.")
                    print("Try again.")
                    answer = input("-> ")
                    answer = float(answer)
                break
            except ValueError: 
                print("Oops! Not a valid measurement.")
                print("Try again.")
        measurements.append(answer)
    return measurements

def loadRoomData(printData):
    '''
    Load room dictionary data from RoomMeasurement.txt into the program
    ''' 
    in_file = open(roomDataFileName, "rt")
    while True:
        in_line = in_file.readline()
        if not in_line:
            break
        name, measurementData = in_line.split(":")
        measurementData = measurementData.strip('][\n').split(',')
        measurements = []
        for item in measurementData:
            measurements.append(float(item))
        rooms.update({name: measurements})
        
        if (printData):
            materialAC = measurements[3]
            decayTime = calculateRT60(measurements, materialAC)
            print("Decay time of", name, "is", decayTime, 'sec')
    in_file.close()

def loadACData():
    '''
    Load absorption coefficient dictionary data from RoomMeasurement.txt into the program
    ''' 
    in_file = open(materialsFileName, "rt")
    while True:
        in_line = in_file.readline()
        if not in_line:
            break
        name, AC = in_line.split(":")
        AC = AC.strip('\n')
        materials.update({name: float(AC)})
    in_file.close()

def saveRoomMeasurements():
    '''
    Save absorption coefficient dictionary data to AC.txt into the program
    ''' 
    rooms.update(newRooms)
    out_file = open(roomDataFileName, "wt")
    for k, v in rooms.items():
        out_file.write(k + ":" + str(v) + "\n")
    out_file.close()

def saveAC():
    '''
    Save absorption coefficient dictionary data to AC.txt into the program
    '''
    materials.update(newMaterials)
    out_file = open(materialsFileName, "wt")
    for k, v in materials.items():
        out_file.write(k + ":" + str(v) + "\n")
    out_file.close()

def calculateRT60(measurements, AC):
    '''
    Use measurements to calculate room volume and surface area then take them
    into Sabine's equation to calculate decay time

    Parameters
    ----------
    measurements : List
        List with height, length and width of the room that is being calculated
    AC: float
        Absorption coefficient of the material that current
        room is made out of

    Returns
    -------
    float
        Time that it takes for the acoustical energy to drop by 60dB

    '''
    height = measurements[0]
    width = measurements[1]
    length = measurements[2]
    roomVolume = calculateVolume(height, width, length)
    roomSurfaceArea = calculateSurfaceArea(height, width, length)
    decayTime = calculateDecayTime(roomVolume, roomSurfaceArea, AC)
    return decayTime

def RT60():
    print("---------------------------")
    print("Welcome to RT60 Version 2.0")
    print("---------------------------")
    print()
    loadRoomData(False)
    loadACData()
    print("What would you like to do? ")
    choice = getUserChoice(mainMenuOptions)
    print()
    
    ''' check if user chooses to start or quit '''
    toStart = choice in range(1, 5)
    while toStart:
        option =  mainMenuOptions[choice - 1]
        if option == createRoom:
            createNewRoom()
        elif option == addMaterial:
            addNewMaterial()
        elif option == loadRooms:
            print("Loading data................")
            loadRoomData(True)
        elif option == saveData:
            saveRoomMeasurements()
            saveAC()
            print("Data Saved!")
        print("-----------------------------------------")
        print("What would you like to do next? ")

        choice = getUserChoice(mainMenuOptions)
        print()
        toStart = choice in range(1, 5)
    # Ask user to save before quiting
    print('Do you want to save before quit?')
    choice = getUserChoice(quitMenuOptions)
    option = quitMenuOptions[choice - 1]
    if option == yes:
        saveRoomMeasurements()
        saveAC()
        print("Data Saved!")
    print("Bye :)")

RT60()



