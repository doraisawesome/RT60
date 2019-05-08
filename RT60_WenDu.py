# Program: RT60
# Description: This program uses the Sabine equation to calculates the amount of time that
#   it takes for the acoustical energy to drop by 60dB. It will ask user for the room demesion
#   and the material the room is made out of.
#
# Author: Wen Du
# Class: SD93 Scripting
# Instructor: Gary Bourgeois


def outputMenu(options):
    '''
    Generates a numbered menu with given options and returns user's choice

    Parameters
    ----------
    options : list
        A list that contains menu options

    Returns
    -------
    int
        User's choice from printed menu

    '''
    print()
    print("Please choose one option from the menu: ")
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
        question = "What is the " + item + " of this room in meters? "
        answer = float(input(question))
        while answer < 0:
            print("Oops! Not a valid measurement.")
            print("Try again.")
            answer = float(input(question))
        measurements.append(answer)
    return measurements


def RT60():
    print("---------------------------")
    print("Welcome to RT60 Version 1.0")
    print("---------------------------")

    mainMenuOptions = ["Start Calculation", "Quit"]

    '''
    A 2D list with: first row a list of material options and
    second row a list of absorption coefficient in respect to each material
    '''
    materials = [["Brick Wall (unpainted)", "Brick Wall (painted)", "Interior Plaster", "Poured Concrete", "Carpeting"], [0.02, 0.01, 0.02, 0.01, 0.1]]

    choice = int(outputMenu(mainMenuOptions))

    ''' check if user chooses to start or quit '''
    toQuit = mainMenuOptions[choice - 1] == mainMenuOptions[1]
    toStart = mainMenuOptions[choice - 1] == mainMenuOptions[0]

    while not toQuit:
        if toStart:
            ''' get room measurements and calculates room volume and room surface area for later use'''
            measurements = takeRoomMeasurements()
            height = measurements[0]
            width = measurements[1]
            length = measurements[2]
            roomVolume = calculateVolume(height, width, length)
            roomSurfaceArea = calculateSurfaceArea(height, width, length)

            ''' Display a menu of available materials to user then get corresponding 
                coefficient from user's choice '''
            print("What material is this room made out of?")
            materialOptions = materials[0]
            materialChoice = int(outputMenu(materialOptions))
            materialChoiceCoeff = materials[1][materialChoice - 1]

            ''' Calculate the time that it takes for the acoustical energy to drop by 60dB '''
            decayTime = calculateDecayTime(roomVolume, roomSurfaceArea, materialChoiceCoeff)
            print("Reverberation decay time of this room is:", decayTime, 'sec')
        else:
            print("Oops! What you typed is not an option from the menu, plese try again.")

        print("-------------------")
        print("Want to start a new calculation? ")
        choice = outputMenu(mainMenuOptions)
    print("Bye :)")

RT60()


