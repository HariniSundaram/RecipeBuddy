#This file contains the Recipe Class. By OOP-ifying recipes, I am able to easily access and store important attributes. This makes it easier
#to standardize display formats of the recipies, no matter where they were webscraped from. 
class Recipe(object): 

    def __init__(self, recipeName, ingredientString, procedure, time, rating, cal): 
        self.recipeName = recipeName
        self.ingredients = ingredientString
        self.procedure = str(procedure)
        self.totalCookTime = time
        self.rating = rating
        self.totalCalories = cal
    
    def getProcedure(self): 
        return self.procedure
    
    def getIngredients(self): 
        return self.ingredients

    def __str__(self): 
        return self.recipeName
    
    def __repr__(self): 
        return self.recipeName
    
    def getHashables(self): 
        return (self.recipeName)

    def __eq__(self, other):
        if (isinstance(other, Recipe) and self.recipeName == other.recipeName and self.rating == other.rating and self.totalCookTime == other.totalCookTime): 
            return True
        else: 
            return False

    def __hash__(self): 
        return hash(self.getHashables())
##The following 4 methods are used for the display in the UI
    #calculates how many lines the ingredients will take up, given a maximum width
    def getIngredientLineCount(self, ingredientBoxWidth):
        printLastWord = False
        fontSize = 9
        lineCounter =0
        ingredientBoxWidth = 330
        for element in self.ingredients: 
            if len(element) * fontSize <= ingredientBoxWidth: 
                    lineCounter +=1
            else: 
                counter = 0
                for word in element.split():
                    if (counter + len(word) + 1)* fontSize < ingredientBoxWidth:
                        counter += len(word) + 1
                    elif (counter + len(word) + 1)* fontSize >= ingredientBoxWidth:
                        printLastWord = True
                        counter = len(word)+ 1
                        lineCounter +=1 
                    if printLastWord == True and word == element.split()[-1]:
                        lineCounter+=1
                        counter = 0 
        return lineCounter
    
    #formats the ingredientList such that the maximum width is within the bounds
    def getFormattedIngredientList(self, ingredientBoxWidth): 
        formattedList = []
        printLastWord = False
        wordsDisplayedSoFar = []
        fontSize = 9
        for element in self.ingredients: 
            if element[0] == '[': 
                element = element[1:]
            if len(element) * fontSize <= ingredientBoxWidth: 
                    wordsDisplayedSoFar.append(element)
                    formattedList.append(element)
            else: 
                counter = 0
                displayStr = ''
                # print(element)
                for word in element.split():
                    # print(word)
                    if (counter + len(word) + 1)* fontSize < ingredientBoxWidth:
                        displayStr = displayStr + word + " "
                        counter += len(word)
                    elif (counter + len(word) + 1)* fontSize >= ingredientBoxWidth:
                        printLastWord = True
                        # print(displayStr)
                        wordsDisplayedSoFar.append(displayStr)
                        formattedList.append(displayStr)                     
                        displayStr = word + " "
                        counter = len(word)+ 1
                    if printLastWord == True and displayStr not in wordsDisplayedSoFar:
                        formattedList.append(word)
                        wordsDisplayedSoFar.append(word)
                        printLastWord = False
                        displayStr = ''
        return formattedList

    # #calculates how many lines the procedure will take up, given a maximum width
    def procLineCounter(self, width):
        letterCounter = 0
        procLineCounter = 0
        fontSize = 8
        for word in self.procedure.split(): 
            if word!= "\n" and word !="\r":
                if (letterCounter + len(word) + 1)* fontSize < width:
                    letterCounter += len(word) + 1
                else:
                    procLineCounter +=1
                    letterCounter = len(word) + 1
        return procLineCounter

    #formats the procedure into a list such that the maximum width is within the bounds
    def formatProcedure(self, width): 
        counter = 0
        displayStr = ''
        procedureList = []
        fontSize = 7
        for word in self.procedure.split(): 
            if word!= "\n" and word !="\r":
                if (counter + len(word) + 1)* fontSize < width:
                    displayStr = displayStr + str(word) + " "
                    counter += len(word) + 1
                else:
                    procedureList.append(displayStr)
                    displayStr = str(word) + " "
                    counter = len(word) + 1
        return procedureList