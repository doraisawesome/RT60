# Program: RT60
# Description: This program uses the Sabine equation to calculates the amount of time that
#   it takes for the acoustical energy to drop by 60dB. It will ask user for the room demesion
#   and the material the room is made out of.
#
# Author: Wen Du
# Class: SD93 Scripting

mainMenuOptions = ["Start", "Quit"]

# A 2D list with: first row a list of material options and 
#    second row a list of absorption coefficient in respect to each material
materials = [["Brick Wall (unpainted)", "Brick Wall (painted)", "Interior Plaster", "Poured Concrete", "Carpeting"], [0.02, 0.01, 0.02, 0.01, 0.1]]


def outputMenu(options):
    """
    This function generates a numbered menu with given options and returns user's choice

    Parameters
    ----------
    options : list
        A list that contains menu options

    Returns
    -------
    int
        User's choice from printed menu

    """
    for item in options:
        print(options.index(item) + 1, ". ", item, sep='')
    userChoice = input("-> ")
    return userChoice


def calculateVolume(height, width, length):
    volume = height * width * length
    return volume


def calculateSurfaceArea(height, width, length):
    surfaceArea = (height * width * 2) + (height * length * 2) + (width * length * 2)
    return surfaceArea


def calculateReverbTime(volume, surfaceArea, absorptionCoeff):
    decayTime = (0.16 * volume) / (surfaceArea * absorptionCoeff)
    return decayTime


def takeRoomMeasurements():
    demensionsToMeasure = ['height', 'width', 'length']
    measurements = []
    for item in demensionsToMeasure:
        question = "What is the " + item + " of this room in meters? "
        answer = float(input(question))
        while answer < 0:
            print("Oops! Not a valid measurement.")
            print("Try again.")
            answer = float(input(question))
        measurements.append(answer)
    return measurements

def RT60():
    print("-------------------")
    print("Welcome to RT60 Version 1.0!")
    choice = outputMenu(mainMenuOptions)
    while choice != "2":
        if choice == "1":
            measurements = takeRoomMeasurements()

            # Display a menu of available materials to the user
            materialOptions = materials[0]
            materialChoice = int(outputMenu(materialOptions))
            materialChoiceCoeff = materials[1][materialChoice - 1]
            height = measurements[0]
            width = measurements[1]
            length = measurements[2]
            roomVolume = calculateVolume(height, width, length)
            roomSurfaceArea = calculateSurfaceArea(height, width, length)
            reverberationTime = calculateReverbTime(roomVolume, roomSurfaceArea, materialChoiceCoeff)
            print("Reverberation of this room is:", reverberationTime, 'sec')
            print("-------------------")
            print("Want to try again? ")
        else:
            print("Oops! Number you typed is not an option from the menu, plese try again.")
        choice = outputMenu(mainMenuOptions)
    print("Bye :)")

RT60()


