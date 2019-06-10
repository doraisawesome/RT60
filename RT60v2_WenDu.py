# Program: RT60
# Description: This program uses the Sabine equation to calculates the amount of time that
#   it takes for the acoustical energy to drop by 60dB. It will ask user for the room demesion
#   and the material the room is made out of.
#
# Author: Wen Du
# Class: SD93 Scripting
# Instructor: Gary Bourgeois

import random

materials = {
    "Brick Wall (unpainted)": 0.02, 
    "Brick Wall (painted)": 0.01,
    "Interior Plaster": 0.02,
    "Poured Concrete": 0.01,
    "Carpeting": 0.1
}
materialsFileName = "AC.txt"

createRoom = "Create a new room"
addMaterial = "Add a new material"
loadRooms = "Show RT60 of saved rooms"
saveData = "Save"
quitCalc = "Quit"
mainMenuOptions = [createRoom, addMaterial, loadRooms, saveData, quitCalc]
randomDimentions = "Randomize room dimentions(height, width, length)"
inputDimentions = "Type in room dimentions manually"
createRoomOptions = [randomDimentions, inputDimentions]

rooms = {}
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
    print("Please choose one option from the menu: ")
    for item in options:
        print(options.index(item) + 1, ". ", item, sep='')
    userChoice = int(input("-> "))

    while userChoice - 1 not in range(len(options)):
        print("Oops! What you typed is not an option.")
        print("Try again:")
        userChoice = int(input("-> "))  
    return userChoice

def createNewRoom():
    choice = getUserChoice(createRoomOptions)
    if createRoomOptions[choice - 1] == randomDimentions:
        measurements = randomizeDimentions()
    else:
        measurements = takeRoomMeasurements()
    print("How would you like to name this room?")
    roomName = input("-> ")

    # print()
    # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    height = measurements[0]
    width = measurements[1]
    length = measurements[2]
    roomVolume = calculateVolume(height, width, length)
    roomSurfaceArea = calculateSurfaceArea(height, width, length)

    ''' Display a menu of available materials to user then get corresponding 
        coefficient from user's choice '''
    print("What material is this room made out of?")
    materialOptions = list(materials.keys())
    materialCoefficients = list(materials.values())
    materialChoice = getUserChoice(materialOptions)
    materialChoiceCoeff = materialCoefficients[materialChoice - 1]

    ''' Calculate the time that it takes for the acoustical energy to drop by 60dB '''
    decayTime = calculateDecayTime(roomVolume, roomSurfaceArea, materialChoiceCoeff)
    print()
    print("Reverberation decay time of this room is:", decayTime, 'sec')
    print("-----------------------------------------")
    print()
    measurements.append(materialChoiceCoeff)
    rooms.update({roomName: measurements})

def randomizeDimentions():
    return [random.uniform(1, 20), random.uniform(1, 20), random.uniform(1, 20)]

def addNewMaterial():
    materialName = input("Name of the material you would like to add: ")
    materialCoeff = float(input("Absoption coefficient of this material is: "))
    materials.update({materialName: float(materialCoeff)})

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
        question = "Please enter the " + item + " of this room (unit: meter)? "
        answer = float(input(question))
        while answer <= 0:
            print("Oops! Not a valid measurement.")
            print("Try again.")
            answer = float(input(question))
        measurements.append(answer)
    return measurements

def loadRoomData():
    in_file = open(roomDataFileName, "rt")
    while True:
        in_line = in_file.readline()
        if not in_line:
            break
        in_line = in_line[:-1]
        name, measurements = in_line.split(",")
        materialAC = measurements[3]
        decayTime = calculateRT60(measurements, materialAC)
        print("Decay time of ", name, " is ", decayTime)
    in_file.close()

def saveRoomMeasurements():
    out_file = open(roomDataFileName, "wt")
    # for k, v in rooms.items():
    #     out_file.write(k + "," + str(v) + "\n")
    out_file.write(str(rooms))
    out_file.close()

def saveAC():
    out_file = open(materialsFileName, "wt")
    out_file.write(str(materials))
    out_file.close()

def calculateRT60(measurements, AC):
    height = measurements[0]
    width = measurements[1]
    length = measurements[2]
    # materialAC = measurements[3]
    roomVolume = calculateVolume(height, width, length)
    roomSurfaceArea = calculateSurfaceArea(height, width, length)
    decayTime = calculateDecayTime(roomVolume, roomSurfaceArea, AC)
    return decayTime

def RT60():
    print("---------------------------")
    print("Welcome to RT60 Version 2.0")
    print("---------------------------")
    print()
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
            loadRoomData()
        elif option == saveData:
            saveRoomMeasurements()
            saveAC()
            print("Data Saved!")
        print("-----------------------------------------")
        print("What would you like to do next? ")

        choice = getUserChoice(mainMenuOptions)
        print()
        toStart = choice in range(1, 5)
    print("Bye :)")

RT60()



