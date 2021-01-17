import requests, re, random, string
from bs4 import BeautifulSoup
from cmu_112_graphics import *
from Recipe import *
from main import *
from CSVReader import*
#This file contains the entire user interphase. It calls both the main file along with the CSVReader file, which both handle all of
#back end aspects. I use 

red = "#e37c5f"
orange = "#e8a87c"
purple = "#c38c9d"
lightBlue = "#7fc3b0"
darkPurple = "#885372"
lightPink = "#e6aea4"
grey = "#b0bcb5"
aqua = "#3fb4a2"

def parser(stringOfIngr): 
        newList = []
        for element in stringOfIngr.split(","): 
            newList.append(element.lower().strip())
        return newList

class SplashScreenMode(Mode): 
    def appStarted(mode): 
        mode.headerHeight = 70
        mode.footerHeight = 60
        mode.margin = 40
        mode.descriptionBoxWidth = 260
        mode.descriptionBoxHeight = 100
        mode.widthBetweenBlocks = 20
        mode.block1Width = 300
        mode.block1Height = 500
        mode.block2Width = (mode.width - mode.margin) - mode.margin + mode.block1Width + mode.widthBetweenBlocks
        mode.block2Height= 250
        mode.block3Height = 340
        mode.block3Width = 200
        mode.block4Height = (mode.block3Width - mode.widthBetweenBlocks)
        mode.block4Width = (mode.block2Width-mode.widthBetweenBlocks)//2
        
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height, fill = "#80c7b9", outline = "#80c7b9")
        #title box: 
        canvas.create_rectangle(mode.margin, mode.margin, mode.width - mode.margin, mode.margin + mode.headerHeight, fill = orange, outline = orange )
        canvas.create_text(mode.width//2, mode.headerHeight//2 + mode.margin -5, text = "RECIPE BUDDY", font = "Noteworthy-Light 60 bold", fill = "brown")
        #descriptionTextBox:
        leftElementHeight = mode.margin + mode.headerHeight
        canvas.create_rectangle(mode.margin+20, leftElementHeight + mode.widthBetweenBlocks, mode.margin + 20 + mode.descriptionBoxWidth, leftElementHeight + mode.widthBetweenBlocks + mode.descriptionBoxHeight, fill = red, outline = red)
        canvas.create_text(mode.margin + 20 + mode.descriptionBoxWidth//2, leftElementHeight + mode.widthBetweenBlocks +mode.descriptionBoxHeight//2, text = "Recipe Buddy is the solution\nto all of your culinary problems.\nClick a button to start!", font = "Didot 17 bold", fill = 'brown')
        #box1: searchby ingredients
        leftElementHeight += mode.widthBetweenBlocks + mode.descriptionBoxHeight
        canvas.create_rectangle(mode.margin, leftElementHeight + mode.widthBetweenBlocks, mode.margin + mode.block1Width, mode.height - mode.footerHeight, fill = orange, outline = orange)
        canvas.create_text(mode.margin + mode.block1Width//2, (leftElementHeight + mode.widthBetweenBlocks + mode.widthBetweenBlocks + mode.height - mode.footerHeight)//2 - 50, text = "  Start New\nRecipe Search", font = "Noteworthy-Light 50", fill = "white", anchor = S)
        canvas.create_text(mode.margin + mode.block1Width//2, (leftElementHeight + mode.widthBetweenBlocks + mode.widthBetweenBlocks + mode.height - mode.footerHeight)//2 + 50, text = "Explore new recipes\nbased on ingredients\nthat you already have", font = "Didot 28", fill = "brown")
        #box2; recipe planner
        canvas.create_rectangle(mode.margin + mode.block1Width + mode.widthBetweenBlocks, mode.margin + mode.headerHeight + mode.widthBetweenBlocks, mode.width - mode.margin, mode.margin + mode.headerHeight + mode.widthBetweenBlocks + mode.block2Height, fill = purple, outline =  purple)
        canvas.create_text((mode.margin + mode.block1Width + mode.widthBetweenBlocks + mode.width - mode.margin)//2, mode.margin + mode.headerHeight + mode.widthBetweenBlocks + mode.block2Height//2 - 70, text = "Recipe Planner", font = "Noteworthy-Light 50", fill = "white")
        canvas.create_text((mode.margin + mode.block1Width + mode.widthBetweenBlocks + mode.width - mode.margin)//2, mode.margin + mode.headerHeight + mode.widthBetweenBlocks + mode.block2Height//2 + 10, text = "Sit back and have recipes curated ", font = "Didot 25", fill = "brown", anchor = CENTER)
        canvas.create_text((mode.margin + mode.block1Width + mode.widthBetweenBlocks + mode.width - mode.margin)//2, mode.margin + mode.headerHeight + mode.widthBetweenBlocks + mode.block2Height//2 + 40, text = "based on your caloric goals,", font = "Didot 25", fill = "brown", anchor = CENTER)
        canvas.create_text((mode.margin + mode.block1Width + mode.widthBetweenBlocks + mode.width - mode.margin)//2, mode.margin + mode.headerHeight + mode.widthBetweenBlocks + mode.block2Height//2 + 70, text = "ingredients you have,", font = "Didot 25", fill = "brown", anchor = CENTER)
        canvas.create_text((mode.margin + mode.block1Width + mode.widthBetweenBlocks + mode.width - mode.margin)//2, mode.margin + mode.headerHeight + mode.widthBetweenBlocks + mode.block2Height//2 + 100, text = "and cuisine preference", font = "Didot 25", fill = "brown", anchor = CENTER)
        #box3: create new Recipe
        canvas.create_rectangle(mode.margin + mode.block1Width + mode.widthBetweenBlocks, mode.height - mode.footerHeight - mode.block3Height, mode.margin + mode.block1Width + mode.widthBetweenBlocks+mode.block3Width, mode.height - mode.footerHeight, fill = red, outline =  red)
        canvas.create_text(mode.margin + mode.block1Width + mode.widthBetweenBlocks + mode.block3Width//2, mode.height - mode.footerHeight - mode.block3Height + mode.widthBetweenBlocks//2 + mode.block3Width//2, text = "Create My\nOwn Recipe", font = "Noteworthy-Light 34", fill = "white")
        canvas.create_text(mode.margin + mode.block1Width + mode.widthBetweenBlocks + mode.block3Width//2 + 5, mode.height - mode.footerHeight - mode.block3Height + mode.widthBetweenBlocks//2 + mode.block3Width//2 +150, text = "One place\nfor all your\nrecipes", font = "Didot 25", fill = "brown")
        #box4: view my recipes
        canvas.create_rectangle(mode.margin + mode.block4Width + 2* mode.widthBetweenBlocks, mode.height - mode.footerHeight - 2*mode.block4Height + mode.widthBetweenBlocks, mode.width - mode.margin, mode.height - mode.footerHeight - mode.block4Height, fill = orange, outline = orange)
        canvas.create_text((mode.margin + mode.block4Width + 2* mode.widthBetweenBlocks + mode.width - mode.margin)//2, (mode.height - mode.footerHeight - 2*mode.block4Height + mode.widthBetweenBlocks + mode.height - mode.footerHeight - mode.block4Height )//2, text = "View My\nRecipes", font = "Noteworthy-Light 30", fill = "white")
        #box5: view favorites
        canvas.create_rectangle(mode.margin + mode.block4Width + 2* mode.widthBetweenBlocks, mode.height - mode.footerHeight - mode.block4Height + mode.widthBetweenBlocks, mode.width - mode.margin, mode.height - mode.footerHeight,fill = purple, outline = purple)
        canvas.create_text((mode.margin + mode.block4Width + 2* mode.widthBetweenBlocks + mode.width - mode.margin)//2, (mode.height - mode.footerHeight - mode.block4Height + mode.widthBetweenBlocks + mode.height - mode.footerHeight )//2, text = "View\nFavorities", font = "Noteworthy-Light 30", fill = "white")

    def mousePressed(mode, event): #contains the pseudo-buttons
        if (mode.margin <= event.x and event.x <= mode.margin + mode.block1Width) and (mode.margin + mode.headerHeight + mode.widthBetweenBlocks + mode.descriptionBoxHeight + mode.widthBetweenBlocks <= event.y and event.y <= mode.height - mode.footerHeight):
            mode.app.setActiveMode(mode.app.searchByIngrMode)
        elif (mode.margin + mode.block1Width + mode.widthBetweenBlocks<= event.x and event.x <= mode.width - mode.margin) and (mode.margin + mode.headerHeight + mode.widthBetweenBlocks <= event.y and event.y <=mode.margin + mode.headerHeight + mode.widthBetweenBlocks + mode.block2Height): 
            mode.app.setActiveMode(mode.app.recipePlanMode)

        elif (mode.margin + mode.block1Width + mode.widthBetweenBlocks<= event.x and event.x <= mode.margin + mode.block1Width + mode.widthBetweenBlocks+mode.block3Width) and (mode.margin + mode.block1Width + mode.widthBetweenBlocks+mode.block3Width, mode.height - mode.footerHeight): 
            mode.app.setActiveMode(mode.app.createNewRecipeMode)

        elif (mode.margin + mode.block4Width + 2* mode.widthBetweenBlocks<= event.x and event.x <= mode.width - mode.margin) and (mode.height - mode.footerHeight - mode.block4Height + mode.widthBetweenBlocks <= event.y and event.y <= mode.height - mode.footerHeight): 
            mode.app.setActiveMode(mode.app.viewFavoritesMode)
            
        elif (mode.margin + mode.block4Width + 2* mode.widthBetweenBlocks<= event.x and event.x <= mode.width - mode.margin) and (mode.height - mode.footerHeight - 2*mode.block4Height + mode.widthBetweenBlocks <= event.y and event.y <= mode.width - mode.margin, mode.height - mode.footerHeight - mode.block4Height): 
            mode.app.setActiveMode(mode.app.viewMyRecipesMode)

class SearchByIngrMode(Mode): 
    def appStarted(mode): 
        print("in search")
        mode.cuisineClicked = False
        mode.recipesDisplayed = False
        mode.recipeHasBeenChosen = False
        mode.ingredientsEntered = False
        mode.margin = 150
        mode.sideMargin = 50

        mode.cuisineClicked = False #if cuisine has been clicked, should move to next page
        mode.ingredientsEntered = False #if all ingredients are entered
        mode.recipesDisplayed = False # if the webscraped recipes are displayed
        mode.ingredientInput = [] #contains all entered ingredients
        mode.recipeDirections = None #stores webscraped procedure of recipe?
        mode.chosenRecipe = None 
        mode.possibleModes = ["mainFilter", "byCookTime", "byRating"]
        mode.modeIndex = 0
        mode.filterMode = mode.possibleModes[mode.modeIndex]
        mode.antiIngredientsEntered = False 
        mode.antiList = []
        mode.categoryRows = 9
        mode.categoryCols = 5
        mode.recipes = None
        mode.recipeOrder = None
        mode.scrollY = 0
        mode.scrollBarWidth = 35
        mode.scrollBarHeight = 100

        mode.isInFavorites = None
        mode.FavoritesBookMarkWidth = 150
        mode.FavoritesBookMarkHeight = 50

        mode.backClicked = False 
        mode.backButtonWidth = 70
        mode.backButtonHeight = 40

        mode.categories=[['Appetizers', 'Asian Fusion', 'Bacon', 'Barbeque', 'Beverages'], 
                            ['Breads', 'Breakfast', 'Brunch', 'Candy', 'Casseroles'],
                            ['Cheese', 'Chicken', 'Chinese', 'Desserts', 'Dinner'],
                            ['Fish', 'French', 'Fruit', 'German', 'Greek'],
                            ['Grill', 'Healthy Choices', 'Holiday & Seasonal', 'Indian', 'Italian'],
                            ['Japanese', 'Lamb', 'Lunch', 'Mexican', 'Pasta'],
                            ['Pizza', "Quick and Easy", 'Salads', 'Sandwiches', 'Seafood'], 
                            ['Slow Cooker', 'Soups', 'Spanish', 'Snacks', 'Thai'],
                            ['Turkey', 'Vegan', 'Vegetables', 'Vegetarian', "Surprise Me"]]
    
    def keyPressed(mode,event): 
        if mode.ingredientsEntered == False: #if we are allowed to keep entering ingredients
            prompt = "Please enter ingredients either individually or as a list seperated by commas"
            if event.key == "Enter": #checks if we are done
                mode.ingredientsEntered = True 
            elif event.key == "Down":
                mode.modeIndex = (mode.modeIndex + 1)%3
                mode.filterMode = mode.possibleModes[mode.modeIndex]
            else: 
                tempEnter = mode.getUserInput(prompt)
                if tempEnter!= None: mode.ingredientInput.extend(parser(tempEnter))   
        elif mode.antiIngredientsEntered == False: 
            prompt = "Please enter ingredients you do not have, and do not want appearing in recipes, individually or as a list seperated by commas"
            if event.key == "Enter": #checks if we are done
                mode.antiIngredientsEntered = True 
            elif event.key == "Down":
                mode.modeIndex = (mode.modeIndex + 1)%3
                mode.filterMode = mode.possibleModes[mode.modeIndex]
            else: 
                tempEnter = mode.getUserInput(prompt)
                print("entered anti")
                if tempEnter!= None: mode.antiList.extend(parser(tempEnter))   
        if mode.ingredientsEntered == True and mode.antiIngredientsEntered== True: 
            mode.recipes, mode.recipeOrder = getCuisineFromInput(mode.ingredientInput, mode.antiList, mode.cuisineChoice, mode.filterMode)
            print(mode.recipes)
            mode.recipesDisplayed = True # mode.createIngredientList(event)

    def mousePressed(mode, event):
        if mode.recipeHasBeenChosen: 
            mode.isInFavorites = checkFavorites(mode.chosenRecipe)
            if event.x <= mode.backButtonWidth and event.y - mode.scrollY <=mode.backButtonHeight: 
                mode.backClicked = True 
                mode.recipeHasBeenChosen = False
                mode.chosenRecipe = None
                mode.isInFavorites = None
                mode.backClicked = False
            elif mode.width - mode.scrollBarWidth - 50 - mode.FavoritesBookMarkWidth<= event.x  and event.x <= mode.width - mode.scrollBarWidth - 50 and 0 - mode.scrollY <= event.y and event.y <= mode.FavoritesBookMarkHeight - mode.scrollY: 
                if mode.isInFavorites == True: 
                    removeFavorites(mode.chosenRecipe)
                    mode.isInFavorites = False
                elif mode.isInFavorites == False: 
                    addFavorites(mode.chosenRecipe)
                    mode.isInFavorites = True
        elif mode.cuisineClicked == False:# and app.cuisineDisplayed == True: #if currently the cuisine has not been chosen
            if mode.pointInGrid(event.x, event.y): 
                row, col = mode.getCell(event.x, event.y)
                mode.cuisineChoice = mode.categories[row][col]
                mode.cuisineClicked = True #after cuisine is clicked, no longer accept cuisine clicks
        elif mode.recipesDisplayed == True and mode.recipeHasBeenChosen == False: 
            if event.x <= mode.backButtonWidth and event.y - mode.scrollY <=mode.backButtonHeight: 
                mode.appStarted()
                mode.app.setActiveMode(mode.app.splashScreenMode)
            if event.y >= 100 - mode.scrollY and mode.sideMargin<=event.x and event.x <= mode.width - mode.scrollBarWidth: 
                row = int(event.y + mode.scrollY - 100)//120 # each recipe is spaced 50 away, CHANGE
                mode.chosenRecipe = mode.recipes[row] #store the correct recipe depending on the mouse position
                mode.recipeHasBeenChosen = True 

    def mouseDragged(mode,event): 
        if mode.recipesDisplayed: 
            mode.scrollY = event.y

    def pointInGrid(mode, x, y): #from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
        # return True if (x, y) is inside the grid defined by app.
        return ((mode.sideMargin <= x <= mode.width-mode.sideMargin) and (mode.margin <= y <= mode.height-mode.margin))
    
    def getCellBounds(mode, row, col): #from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
        gridWidth  = mode.width - 2*mode.sideMargin
        gridHeight = mode.height - 2*mode.margin
        cellWidth = gridWidth / mode.categoryCols
        cellHeight = gridHeight / mode.categoryRows
        x0 = mode.sideMargin + col * cellWidth
        x1 = mode.sideMargin + (col+1) * cellWidth
        y0 = mode.margin + row * cellHeight
        y1 = mode.margin + (row+1) * cellHeight
        return (x0, y0, x1, y1)

    def getCell(mode, x, y): #from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
        gridWidth  = mode.width - 2*mode.sideMargin
        gridHeight = mode.height - 2*mode.margin
        cellWidth  = gridWidth / mode.categoryCols
        cellHeight = gridHeight / mode.categoryRows
        row = int((y - mode.margin) / cellHeight)
        col = int((x - mode.sideMargin) / cellWidth)
        return (row, col)

    def drawCuisineScreen(mode, canvas): 
        canvas.create_rectangle(0,0,mode.width,mode.height, fill = lightBlue, outline = lightBlue)
        canvas.create_text(mode.width//2, 75, text = "Please choose your cuisine", font = "Noteworthy-Light 50 bold", fill = "#046570")
    
    def drawCuisineSelection(mode,canvas): 
        for row in range(mode.categoryRows): 
            for col in range(mode.categoryCols):
                x0,y0,x1,y1 = mode.getCellBounds(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill = orange, outline = red, width = 5)
                if mode.categories[row][col] == "Holiday & Seasonal": 
                    canvas.create_text((x0+x1)/2,(y0+y1)/2, text = "Holiday & \n Seasonal", font = "Didot 16 bold", fill = "brown")
                elif mode.categories[row][col] == "Healthy Choices": 
                    canvas.create_text((x0+x1)/2,(y0+y1)/2, text = "Healthy \n Choices", font = "Didot 17 bold", fill = "brown")
                else: 
                    canvas.create_text((x0+x1)/2,(y0+y1)/2, text = mode.categories[row][col], font = "Didot 18 bold", fill = "brown")
    def drawFavoritesBookmark(mode,canvas): 
        if mode.isInFavorites == True: 
            color = lightPink
        else: color = aqua
        canvas.create_rectangle(mode.width - mode.scrollBarWidth - 50 - mode.FavoritesBookMarkWidth,0 - mode.scrollY, mode.width - mode.scrollBarWidth - 50, mode.FavoritesBookMarkHeight - mode.scrollY, fill = color, outline = color)
        canvas.create_text(mode.width - mode.scrollBarWidth - 50 - mode.FavoritesBookMarkWidth//2, mode.FavoritesBookMarkHeight//2 - mode.scrollY, text = "Favorite", fill = "white")
    
    def drawBackButton(mode,canvas): 
        canvas.create_polygon(5, mode.backButtonHeight//2-mode.scrollY, mode.backButtonWidth//2, mode.backButtonHeight - 5-mode.scrollY,mode.backButtonWidth//2, mode.backButtonHeight//2 +  10-mode.scrollY, mode.backButtonWidth, mode.backButtonHeight//2 +  10-mode.scrollY, mode.backButtonWidth,mode.backButtonHeight//2 -  10-mode.scrollY, mode.backButtonWidth//2, mode.backButtonHeight//2 -10-mode.scrollY,mode.backButtonWidth//2, 5-mode.scrollY, 5, mode.backButtonHeight//2-mode.scrollY, fill = purple)
    
    def displayRecipeSpecifics(mode, canvas): 
        canvas.delete("all")
        canvas.create_rectangle(0,0,mode.width,mode.height, fill = lightBlue, outline = lightBlue)
        mode.drawFavoritesBookmark(canvas)
        mode.drawScrollBar(canvas)
        mode.drawBackButton(canvas)
        titleHeight = 80
       
        canvas.create_rectangle(mode.backButtonWidth, mode.FavoritesBookMarkHeight + 30 - mode.scrollY, mode.width - mode.backButtonWidth, mode.FavoritesBookMarkHeight + 50 + titleHeight-mode.scrollY, fill = red, outline = red)
        canvas.create_text(mode.backButtonWidth +20, mode.FavoritesBookMarkHeight + 30 +titleHeight//2 - mode.scrollY, text = f"'{mode.chosenRecipe.recipeName}'", font = "Noteworthy-Light 40 bold", anchor = W, fill = "white")
        
        infoBoxWidth = 250
        infoBoxHeight = 200
        canvas.create_rectangle(mode.sideMargin, mode.FavoritesBookMarkHeight + 80 + titleHeight-mode.scrollY, mode.sideMargin + infoBoxWidth,  mode.FavoritesBookMarkHeight + 80 + titleHeight+ infoBoxHeight - mode.scrollY, fill = orange, outline = orange)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + infoBoxHeight//4 - mode.scrollY, text = f"Total Cook Time: {mode.chosenRecipe.totalCookTime}", font = "Helvetica 20 bold", fill = "brown", anchor = W)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + infoBoxHeight//2 - mode.scrollY, text = f"Rating: {mode.chosenRecipe.rating}", font = "Helvetica 20 bold",fill = "brown",  anchor = W)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + 3*infoBoxHeight//4 - mode.scrollY, text = f"Calories: {mode.chosenRecipe.totalCalories}", font = "Helvetica 20 bold",fill = "brown", anchor = W)
    
        ingredientBoxWidth = 300
        newStart = mode.FavoritesBookMarkHeight + 80 + titleHeight + infoBoxHeight  + 40
        ingredientLineCount = mode.chosenRecipe.getIngredientLineCount(330)
        canvas.create_rectangle(mode.sideMargin, newStart - mode.scrollY, mode.sideMargin + ingredientBoxWidth, newStart+ 40* ingredientLineCount + 20- mode.scrollY, fill = red, outline = red)
        canvas.create_text(ingredientBoxWidth//2, newStart - mode.scrollY+ 25, text = f"Ingredients:", font = "Noteworthy-Light 30", anchor = W)

        incr = newStart + 60
        ingredientBoxWidth = 330
        printLastWord = False
        wordsDisplayedSoFar = []

        for element in mode.chosenRecipe.getFormattedIngredientList(330): 
            incr +=30
            canvas.create_text(mode.sideMargin +10, incr - mode.scrollY, text = f"{element}", font = f"Helvetica 15 bold", anchor = W)

        ingredientBoxWidth = 300
        ProcedureBoxWidth = 330
        start = mode.FavoritesBookMarkHeight + 80 + titleHeight
        fontSize = 7
       
        procLineCounter = mode.chosenRecipe.procLineCounter(330)
        canvas.create_rectangle(mode.sideMargin + ingredientBoxWidth + 30,start - mode.scrollY, mode.width - mode.scrollBarWidth -10, start - mode.scrollY + 30*procLineCounter + 120, fill = purple, outline = purple)
        displayStr = ''
        
        canvas.create_text((ingredientBoxWidth+ mode.width - mode.scrollBarWidth)//2, start + 30 - mode.scrollY, text = "Procedure:", font = f"Noteworthy-Light 30", anchor = W)
        incr = start + 70
        for element in mode.chosenRecipe.formatProcedure(330):
            canvas.create_text(mode.sideMargin + ingredientBoxWidth+ 40, incr-mode.scrollY, text = f"{element}", font = f"Helvetica 15 bold", anchor = W)
            incr+=30
        canvas.create_text(mode.sideMargin + ingredientBoxWidth+ 40, incr-mode.scrollY, text = f"{displayStr}", font = f"Helvetica 15 bold", anchor = W)
        incr+=30

    def drawEnterIngredients(mode,canvas): 
        canvas.delete("all")
        canvas.create_rectangle(0,0,mode.width,mode.height, fill = lightBlue, outline = lightBlue)
        canvas.create_text(mode.width//2, 70, text = "Enter the ingredients you have.", font = "Noteworthy-Light 50 bold", fill = darkPurple)
        canvas.create_text(mode.sideMargin-20, 150, text = "Press any key to start, press ENTER key when done.", font = "Noteworthy-Light 23 bold", fill = darkPurple, anchor = W)
        canvas.create_text(mode.sideMargin-20, 200, text = f"To change the filter, click DOWN key. The current sorting Filter is: ", font = "Noteworthy-Light 23", fill = darkPurple, anchor = W)
        text = 'mainFilter orders your recipes from those requiring least to greatest extra ingredients'
        if mode.filterMode == "byCookTime": 
            text = "byCookTime orders your recipes from least to greatest minutes required cook the dish"
        elif mode.filterMode == "byRating": 
            text = "byRating orders your recipes from greatest to least rating, from a scale from 1 to 5"
        canvas.create_text(mode.sideMargin-20, 250, text = text, font = "Noteworthy-Light 23", fill = darkPurple, anchor = W)

        canvas.create_text(mode.width - 10, 200, text = f"{mode.filterMode}", font = "Noteworthy-Light 25", fill = darkPurple, anchor = E)

        canvas.create_text(mode.width//2, 300, text = f"Ingredients Entered So Far:", font = "Noteworthy-Light 50 bold", fill = darkPurple)
        startingX = mode.sideMargin
        startingY = 320
        incrY = 30
        incrX = 200
        counter= 0 
        ingrPerLineMax = 14
        for element in mode.ingredientInput: 
            if counter <= ingrPerLineMax: 
                startingY+=incrY
                counter+=1
            else:
                startingX += incrX
                startingY = 350
                counter = 1
            canvas.create_text(startingX,startingY, text = f"- {element}", font = "Noteworthy-Light 15 bold", fill = "black", anchor = W)
        for element in mode.antiList: 
            if counter <= ingrPerLineMax: 
                startingY+=incrY
                counter+=1
            else:
                startingX += incrX
                startingY = 350
                counter = 1
            canvas.create_text(startingX,startingY, text = f"- {element}", font = "Noteworthy-Light 15 bold", anchor = W, fill = "red")
    def drawScrollBar(mode,canvas): 
        canvas.create_rectangle(mode.width - mode.scrollBarWidth, mode.scrollY - mode.scrollBarHeight//2, mode.width, mode.scrollY + mode.scrollBarHeight//2, fill = purple, outline = purple)
    def displayRecipe(mode, canvas): 
        canvas.delete("all")
        canvas.create_rectangle(0,0,mode.width,mode.height, fill = lightBlue, outline = lightBlue)
        mode.drawBackButton(canvas)
        mode.drawScrollBar(canvas)
        canvas.create_text(mode.sideMargin, 50 - mode.scrollY, text = f'These are {mode.cuisineChoice} recipes from your input', font = "Noteworthy-Light 25 bold", fill = "brown", anchor = W)
        canvas.create_text(mode.width - mode.sideMargin - mode.scrollBarWidth, 50 - mode.scrollY, text = f'Sorted by {mode.filterMode}', font = "Noteworthy-Light 25 bold", fill = "brown", anchor = E)
        
        recipeBoxWidth = mode.width - 2*mode.sideMargin
        recipeBoxHeight = 100
        recipeIncr = 20
        heightPlacement = 100
        if mode.recipes!= None: 
            for row in range(len(mode.recipes)):
                canvas.create_rectangle(mode.sideMargin-5, heightPlacement - mode.scrollY, mode.sideMargin + recipeBoxWidth, heightPlacement - mode.scrollY + recipeBoxHeight, fill = orange, outline = orange )
                canvas.create_text(mode.sideMargin, heightPlacement - mode.scrollY + recipeBoxHeight//2, text = f"{mode.recipes[row]}", font = "Noteworthy-Light 28 bold", fill = "brown", anchor = W)
                if mode.possibleModes[mode.modeIndex] == "mainFilter": canvas.create_text(mode.width - mode.sideMargin - mode.scrollBarWidth, heightPlacement - mode.scrollY+ recipeBoxHeight//4, text = f"No. of extra ingredients: {str(mode.recipeOrder[row])}", font = "Helvetica 15 bold", fill = "brown", anchor = E)
                canvas.create_text(mode.width - mode.sideMargin - mode.scrollBarWidth, heightPlacement - mode.scrollY+ recipeBoxHeight//2, text = f"Cook Time: {mode.recipes[row].totalCookTime}", font = "Helvetica 15 bold", fill = "brown", anchor = E)
                canvas.create_text(mode.width - mode.sideMargin - mode.scrollBarWidth, heightPlacement - mode.scrollY+ 3*recipeBoxHeight//4, text = f"Rating: {mode.recipes[row].rating}", font = "Helvetica 15 bold", fill = "brown", anchor = E)
                heightPlacement += recipeBoxHeight + recipeIncr
    
    def redrawAll(mode,canvas): 
        # print("hi")
        if mode.cuisineClicked == False: 
            mode.drawCuisineScreen(canvas)
            mode.drawCuisineSelection(canvas)
        elif mode.recipesDisplayed == True and mode.recipeHasBeenChosen == True: 
            mode.displayRecipeSpecifics(canvas)
        elif mode.cuisineClicked == True and mode.ingredientsEntered == True and mode.antiIngredientsEntered==True: 
            mode.displayRecipe(canvas)
        elif mode.cuisineClicked == True and (mode.ingredientsEntered == False or mode.antiIngredientsEntered==False): 
            mode.drawEnterIngredients(canvas)

class RecipePlanMode(Mode): 
    def appStarted(mode):
        print("in recipe Plan")
        mode.targetIngredientsEntered = False
        mode.ingredientInput= []
        mode.chosenCuisine = None
        mode.calorieMin = -1
        mode.calorieMax = -1
        mode.createRecipePlan = True
        mode.mode = 'mainFilter'
        mode.sideMargin = 50
        mode.recipes = None
        mode.entireFormFilled = False
        mode.numberOfRecipesDesired = 0
        mode.startingYPos = 100
        mode.YIncr = 50

        mode.recipeDisplayed = False
        mode.chosenRecipe = None
        mode.recipeClicked = False
        mode.backClicked = False 
        mode.backButtonWidth = 70
        mode.backButtonHeight = 40
        mode.maxExtraIngredients = 0
        mode.scrollY = 0
        mode.scrollBarWidth = 35
        mode.scrollBarHeight = 100
        mode.antiIngredientsEntered = False 
        mode.isInFavorites = None
        mode.FavoritesBookMarkWidth = 150
        mode.FavoritesBookMarkHeight = 50
        mode.antiList = []
        mode.categories = [['Appetizers', 'Asian Fusion', 'Bacon', 'Barbeque', 'Beverages, Breads', 'Breakfast', 'Brunch', 'Candy', 'Casseroles'],
                            ['Cheese', 'Chicken', 'Chinese', 'Desserts', 'Dinner','Fish', 'French', 'Fruit', 'German', 'Greek'],
                            ['Grill', 'Healthy Choices', 'Holiday & Seasonal', 'Indian', 'Italian', 'Japanese', 'Lamb', 'Lunch', 'Mexican', 'Pasta'],
                            ['Pizza', "Quick and Easy", 'Salads', 'Sandwiches', 'Seafood', 'Slow Cooker', 'Soups', 'Spanish', 'Snacks', 'Thai'],
                            ['Turkey', 'Vegan', 'Vegetables', 'Vegetarian', "Surprise Me"]]

    def mousePressed(mode,event): 
        if mode.chosenRecipe !=None:  
            mode.isInFavorites = checkFavorites(mode.chosenRecipe)
        if mode.recipeClicked and event.x <= mode.backButtonWidth and event.y - mode.scrollY <=mode.backButtonHeight: 
            mode.backClicked = True 
            mode.recipeClicked = False
            mode.chosenRecipe = None
            mode.backClicked = False
        elif mode.recipeClicked == False and event.x <= mode.backButtonWidth and event.y - mode.scrollY <=mode.backButtonHeight: 
            mode.appStarted()
            mode.app.setActiveMode(mode.app.splashScreenMode)
        elif mode.width - mode.scrollBarWidth - 50 - mode.FavoritesBookMarkWidth<= event.x  and event.x <= mode.width - mode.scrollBarWidth - 50 and 0 - mode.scrollY <= event.y and event.y <= mode.FavoritesBookMarkHeight - mode.scrollY: 
            if mode.isInFavorites == True: 
                removeFavorites(mode.chosenRecipe)
                mode.isInFavorites = False
                print("removed")
            elif mode.isInFavorites == False: 
                addFavorites(mode.chosenRecipe)
                mode.isInFavorites = True
                print("added")
        elif mode.recipeDisplayed and mode.recipeClicked == False: 
            if event.x <= mode.backButtonWidth and event.y - mode.scrollY <=mode.backButtonHeight: 
                mode.app.setActiveMode(mode.app.splashScreenMode)
            elif event.y >= 100 - mode.scrollY and mode.sideMargin<=event.x and event.x <= mode.width - mode.scrollBarWidth: 
                row = int(event.y + mode.scrollY - 150)//120 # each recipe is spaced 50 away, CHANGE
                print(row)
                mode.chosenRecipe = mode.recipes[row] #store the correct recipe depending on the mouse positio
                mode.recipeClicked = True 
        

    def drawBackButton(mode,canvas): 
        canvas.create_polygon(5, mode.backButtonHeight//2-mode.scrollY, mode.backButtonWidth//2, mode.backButtonHeight - 5-mode.scrollY,mode.backButtonWidth//2, mode.backButtonHeight//2 +  10-mode.scrollY, mode.backButtonWidth, mode.backButtonHeight//2 +  10-mode.scrollY, mode.backButtonWidth,mode.backButtonHeight//2 -  10-mode.scrollY, mode.backButtonWidth//2, mode.backButtonHeight//2 -10-mode.scrollY,mode.backButtonWidth//2, 5-mode.scrollY, 5, mode.backButtonHeight//2-mode.scrollY, fill = purple)
    def mouseDragged(mode,event): 
        if mode.recipeDisplayed: #and mode.chosenRecipe == None: 
            mode.scrollY = event.y
    def keyPressed(mode, event): 
        if mode.chosenCuisine == None: 
            prompt = "Please type in a valid cuisine you desire from the options above"
            tempEnter = mode.getUserInput(prompt)
            if tempEnter!= None: mode.chosenCuisine = tempEnter
        if mode.numberOfRecipesDesired == 0: 
            prompt = "Please enter how many recipes you want"
            try: 
                tempEnter = int(mode.getUserInput(prompt))
                mode.numberOfRecipesDesired = tempEnter
            except AttributeError: 
                pass
            except ValueError: 
                mode.numberOfRecipesDesired == 0
        if mode.calorieMin == -1: 
            prompt = "Please enter the total calorie minimum"
            try: 
                tempEnter = int(mode.getUserInput(prompt))
                mode.calorieMin = tempEnter
            except AttributeError: 
                pass
            except ValueError: 
                pass
        if mode.calorieMax == -1: 
            prompt = "Please enter the total calorie maximum "
            try: 
                tempEnter = int(mode.getUserInput(prompt))
                mode.calorieMax = tempEnter
            except AttributeError: 
                pass
            except ValueError: 
                pass
            prompt = "What is the Maximum Number of Extra Ingredients you want"
            try: 
                tempEnter = int(mode.getUserInput(prompt))
                mode.maxExtraIngredients = tempEnter
                print(mode.maxExtraIngredients)
            except AttributeError: 
                pass
            except ValueError: 
                pass
        if mode.targetIngredientsEntered == False: 
            if event.key == "Enter": 
                mode.targetIngredientsEntered = True
            else: 
                prompt = "Please enter ingredients either individually or as a list seperated by commas, press ENTER when done"
                tempEnter = mode.getUserInput(prompt)
                if tempEnter!= None: mode.ingredientInput.extend(parser(tempEnter))
                print(mode.ingredientInput)
        elif mode.antiIngredientsEntered == False: 
            prompt = "Please enter ingredients you do not have, and do not want appearing in recipes, individually or as a list seperated by commas, press ENTER when done"
            if event.key == "Enter": #checks if we are done
                mode.antiIngredientsEntered = True 
                mode.entireFormFilled = True
            else: 
                tempEnter = mode.getUserInput(prompt)
                print("entered anti")
                if tempEnter!= None: mode.antiList.extend(parser(tempEnter))  
        if mode.entireFormFilled == True:
            solution = getCuisineFromInput(mode.ingredientInput, mode.antiList, mode.chosenCuisine, mode.mode, createRecipePlan = mode.createRecipePlan, calMin=mode.calorieMin, calMax=mode.calorieMax, numberOfRecipesWanted=mode.numberOfRecipesDesired, tolerance = mode.maxExtraIngredients)
            # print(solution)
            if solution == "No exact solutions": mode.recipes = None
            else: mode.recipes = solution
            mode.recipeDisplayed = True
    def drawFavoritesBookmark(mode,canvas): 
        if mode.isInFavorites == True: 
            color = lightPink
        else: color = aqua
        canvas.create_rectangle(mode.width - mode.scrollBarWidth - 50 - mode.FavoritesBookMarkWidth,0 - mode.scrollY, mode.width - mode.scrollBarWidth - 50, mode.FavoritesBookMarkHeight - mode.scrollY, fill = color, outline = color)
        canvas.create_text(mode.width - mode.scrollBarWidth - 50 - mode.FavoritesBookMarkWidth//2, mode.FavoritesBookMarkHeight//2 - mode.scrollY, text = "Favorite", fill = "white")
    def drawScrollBar(mode,canvas): 
        canvas.create_rectangle(mode.width - mode.scrollBarWidth, mode.scrollY - mode.scrollBarHeight//2, mode.width, mode.scrollY + mode.scrollBarHeight//2, fill = purple, outline = purple)
    def displayRecipeSpecifics(mode,canvas,recipe): 
        canvas.delete("all")
        canvas.create_rectangle(0,0,mode.width, mode.height, fill = lightBlue, outline = lightBlue)
        mode.drawScrollBar(canvas)
        mode.drawBackButton(canvas)
        mode.drawFavoritesBookmark(canvas)

        titleHeight = 80
       
        canvas.create_rectangle(mode.backButtonWidth, mode.FavoritesBookMarkHeight + 30 - mode.scrollY, mode.width - mode.backButtonWidth, mode.FavoritesBookMarkHeight + 50 + titleHeight-mode.scrollY, fill = red, outline = red)
        canvas.create_text(mode.backButtonWidth +20, mode.FavoritesBookMarkHeight + 30 +titleHeight//2 - mode.scrollY, text = f"'{mode.chosenRecipe.recipeName}'", font = "Noteworthy-Light 40 bold", anchor = W, fill = "white")
        
        infoBoxWidth = 250
        infoBoxHeight = 200
        canvas.create_rectangle(mode.sideMargin, mode.FavoritesBookMarkHeight + 80 + titleHeight-mode.scrollY, mode.sideMargin + infoBoxWidth,  mode.FavoritesBookMarkHeight + 80 + titleHeight+ infoBoxHeight - mode.scrollY, fill = orange, outline = orange)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + infoBoxHeight//4 - mode.scrollY, text = f"Total Cook Time: {mode.chosenRecipe.totalCookTime}", font = "Helvetica 20 bold", fill = "brown", anchor = W)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + infoBoxHeight//2 - mode.scrollY, text = f"Rating: {mode.chosenRecipe.rating}", font = "Helvetica 20 bold",fill = "brown",  anchor = W)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + 3*infoBoxHeight//4 - mode.scrollY, text = f"Calories: {mode.chosenRecipe.totalCalories}", font = "Helvetica 20 bold",fill = "brown", anchor = W)
        
        ingrLineCounter = recipe.getIngredientLineCount(330)
        
        start = mode.FavoritesBookMarkHeight + 80 + titleHeight
        ingredientBoxWidth = 300
        newStart = mode.FavoritesBookMarkHeight + 80 + titleHeight+ infoBoxHeight  + 40
        incr = newStart + 60
        canvas.create_rectangle(mode.sideMargin, newStart - mode.scrollY, mode.sideMargin + ingredientBoxWidth, newStart+ 40* ingrLineCounter + 20- mode.scrollY, fill = red, outline = red)
        canvas.create_text(ingredientBoxWidth//2, newStart - mode.scrollY+ 25, text = f"Ingredients:", font = "Noteworthy-Light 30", anchor = W)
        for element in recipe.getFormattedIngredientList(330):
            canvas.create_text(mode.sideMargin +10, incr - mode.scrollY, text = f"{element}", font = f"Helvetica 13 bold", anchor = W)
            incr+=30
        
        ProcedureBoxWidth = 350
        start = mode.FavoritesBookMarkHeight + 80 + titleHeight
        fontSize = 7
        # print(type(mode.chosenRecipe.procedure))
        ingredientBoxWidth = 300
        ProcedureBoxWidth = 330
        procLineCounter = recipe.procLineCounter(330)
        canvas.create_rectangle(mode.sideMargin + ingredientBoxWidth + 30,start - mode.scrollY, mode.width - mode.scrollBarWidth -10, start - mode.scrollY + 25*procLineCounter + 100, fill = purple, outline = purple)
        # displayStr = ''
        
        canvas.create_text((ingredientBoxWidth+ mode.width - mode.scrollBarWidth)//2, start + 30 - mode.scrollY, text = "Procedure:", font = f"Noteworthy-Light 30", anchor = W)
        incr = start + 70
        for element in recipe.formatProcedure(330):
            canvas.create_text(mode.sideMargin + ingredientBoxWidth+ 40, incr-mode.scrollY, text = f"{element}", font = f"Helvetica 15 bold", anchor = W)
            incr+=30
        # canvas.create_text(mode.sideMargin + ingredientBoxWidth+ 40, incr-mode.scrollY, text = f"{displayStr}", font = f"Helvetica 15 bold", anchor = W)
    def redrawAll(mode, canvas): 
        canvas.create_rectangle(0,0,mode.width,mode.height, fill = lightBlue, outline = lightBlue)
        mode.drawBackButton(canvas)
        canvas.create_text(mode.width//2, 40 - mode.scrollY,text = "Generate Recipe Plan", font = "Noteworthy-Light 40 bold", fill = "white")

        if mode.entireFormFilled == False: 
            if mode.chosenCuisine == None: 
                catPosY = mode.sideMargin + 40
                canvas.create_text(mode.sideMargin, catPosY, text = f"Valid cuisines include:", font = "Helvetica 20 bold",fill = "white", anchor = W)
                for row in range(len(mode.categories)): 
                    catPosY += 30
                    canvas.create_text(mode.sideMargin,catPosY, text = f'{", ".join(mode.categories[row])}', font = "Helvetica 13 bold", fill = "white", anchor = W)
            elif mode.chosenCuisine != None: 
                canvas.create_rectangle(mode.sideMargin - 10, 70 - mode.scrollY, mode.width - mode.scrollBarWidth - 5, 180 - mode.scrollY, fill = orange, outline = orange)
                canvas.create_text(mode.sideMargin, 100, text = f"Chosen Cuisine: {mode.chosenCuisine}", font = "Helvetica 20 bold", fill = "brown", anchor = W)
            if  mode.numberOfRecipesDesired != 0: 
                canvas.create_text(mode.sideMargin, 150, text = f"Number of Recipes Desired: {mode.numberOfRecipesDesired}", font = "Helvetica 20 bold", fill = "brown", anchor = W)
            if  mode.calorieMin != -1 and mode.calorieMax != -1: 
                canvas.create_text(mode.width - 200, 100, text = f"Total Calorie Minimum: {mode.calorieMin}", fill = "brown", font = "Helvetica 20 bold")
                canvas.create_text(mode.width - 200, 150, text = f"Total Calorie Maximum: {mode.calorieMax}",  fill = "brown",font = "Helvetica 20 bold")
            if mode.ingredientInput!= []: 
                canvas.create_rectangle(mode.sideMargin-10, 200 , mode.width - mode.scrollBarWidth, mode.height-mode.sideMargin, fill = darkPurple, outline = darkPurple)
                canvas.create_text(mode.width//2, 230, text = "Ingredients:", font = "Helvetica 30 bold", fill = "white")
                
                startingX = mode.sideMargin + 10
                startingY = 240
                incrY = 30
                incrX = 150
                counter= 0 
                ingrPerLineMax = 15
                for element in mode.ingredientInput: 
                    if counter <= ingrPerLineMax: 
                        startingY+=incrY
                        counter+=1
                    else:
                        startingX += incrX
                        startingY = 270
                        counter = 1
                    canvas.create_text(startingX , startingY, text = f"- {element}", font = "Helvetica 15 bold", anchor = W, fill = "white")
                for element in mode.antiList: 
                    if counter <= ingrPerLineMax: 
                        startingY+=incrY
                        counter+=1
                    else:
                        startingX += incrX
                        startingY = 270
                        counter = 1
                    canvas.create_text(startingX,startingY, text = f"- {element}", font = "Helvetica 15 bold", anchor = W, fill = "red")
        else: 
            if mode.recipeDisplayed and mode.recipeClicked == False: 
                canvas.delete("all")
                canvas.create_rectangle(0,0,mode.width,mode.height, fill = lightBlue, outline = lightBlue)
                mode.drawScrollBar(canvas)
                mode.drawBackButton(canvas)
                startingYPos = mode.startingYPos
                if mode.recipes == None and mode.entireFormFilled: 
                    canvas.create_text(100, 100-mode.scrollY, text = "Unfortunately no recipes were found\nConsider trying again with more ingredients!", font = "Noteworth-Light 30 bold", anchor = W)
                else: 
                    recipeBoxWidth = mode.width - 2*mode.sideMargin
                    recipeBoxHeight = 100
                    recipeIncr = 20
                    heightPlacement = 150
                    canvas.create_text(mode.width//2, 100-mode.scrollY, text = f"Here is your Recipe Plan:", font = "Noteworthy-Light 30 bold", fill = "brown") 
                    for rec in mode.recipes:
                        canvas.create_rectangle(mode.sideMargin-5, heightPlacement - mode.scrollY, mode.sideMargin + recipeBoxWidth, heightPlacement - mode.scrollY + recipeBoxHeight, fill = orange, outline = orange )
                        canvas.create_text(mode.sideMargin, heightPlacement - mode.scrollY + recipeBoxHeight//2, text = f"{rec}", font = "Noteworthy-Light 30 bold", fill = "brown", anchor = W)
                        canvas.create_text(mode.width - mode.sideMargin - mode.scrollBarWidth, heightPlacement - mode.scrollY+ recipeBoxHeight//3, text = f"Cook Time: {rec.totalCookTime}", font = "Helvetica 15 bold", fill = "brown", anchor = E)
                        canvas.create_text(mode.width - mode.sideMargin - mode.scrollBarWidth, heightPlacement - mode.scrollY+ 2*recipeBoxHeight//3, text = f"Rating: {rec.rating}", font = "Helvetica 15 bold", fill = "brown", anchor = E)
                        heightPlacement += recipeBoxHeight + recipeIncr
            elif mode.recipeDisplayed and mode.recipeClicked: 
                mode.displayRecipeSpecifics(canvas, mode.chosenRecipe)
       
class CreateNewRecipeMode(Mode):
    def appStarted(mode): 
        print("in Create New Recipe")
        mode.newRecipeName = None
        mode.newRecipeProcedure = ''
        mode.newRecipeCookTime = None
        mode.newRecipeRating = None
        mode.ratingValid = False
        mode.calories = None 
        mode.ingredientInput = [] 
        mode.scrollY = 0
        mode.scrollBarWidth = 35
        mode.scrollBarHeight = 100

        mode.targetIngredientsEntered = False
        mode.recipeProcedureEntered = False
        mode.sideMargin = 50
        mode.ProcedureLineCounter = 0
        mode.procedureDoneButtonWidth = 100
        mode.procedureDoneButtonHeight= 80

        mode.backClicked = False 
        mode.backButtonWidth = 70
        mode.backButtonHeight = 40

        mode.newRecipeObject = None

    def mousePressed(mode,event): 
        if event.x <= mode.backButtonWidth and event.y - mode.scrollY <=mode.backButtonHeight: 
            mode.app.setActiveMode(mode.app.splashScreenMode)
        if mode.recipeProcedureEntered == False: 
            if mode.width - mode.scrollBarWidth - 10 - mode.procedureDoneButtonWidth - mode.scrollY <=event.x and event.x<=mode.width - mode.scrollBarWidth - 10 - mode.scrollY: 
                if 0 <=event.y and event.y <=mode.procedureDoneButtonHeight: 
                    print("Done")
                    mode.recipeProcedureEntered = True
                    mode.newRecipeObject = Recipe(mode.newRecipeName, " ".join(mode.ingredientInput), mode.newRecipeProcedure, mode.newRecipeCookTime, mode.newRecipeRating, mode.calories)
                    print(mode.newRecipeObject)
                    writeMyOwnRecipe(mode.newRecipeObject)
    
    def mouseDragged(mode,event): 
            mode.scrollY = event.y
    
    def createProcedureStr(mode,event): 
        print(mode.newRecipeProcedure)
        if event.key == "Enter": #checks if we are done
            mode.newRecipeProcedure =  mode.newRecipeProcedure +  "\n"
            mode.ProcedureLineCounter = 0
        elif event.key == "Delete": 
            mode.newRecipeProcedure = mode.newRecipeProcedure[:-1]
            mode.ProcedureLineCounter -= 1
        elif event.key == "Space":
            mode.newRecipeProcedure += " "
            mode.ProcedureLineCounter += 1
        elif (mode.ProcedureLineCounter +1) * 20 >= mode.width - 2*mode.sideMargin:
            mode.newRecipeProcedure = mode.newRecipeProcedure + "\n"
            mode.newRecipeProcedure += event.key
            mode.ProcedureLineCounter = 1
        else: 
            mode.newRecipeProcedure = mode.newRecipeProcedure + event.key
            mode.ProcedureLineCounter += 1
    
    def drawScrollBar(mode,canvas): 
        canvas.create_rectangle(mode.width - mode.scrollBarWidth, mode.scrollY - mode.scrollBarHeight//2, mode.width, mode.scrollY + mode.scrollBarHeight//2, fill = purple, outline = purple)
    
    def drawBackButton(mode,canvas): 
        canvas.create_polygon(5, mode.backButtonHeight//2-mode.scrollY, mode.backButtonWidth//2, mode.backButtonHeight - 5-mode.scrollY,mode.backButtonWidth//2, mode.backButtonHeight//2 +  10-mode.scrollY, mode.backButtonWidth, mode.backButtonHeight//2 +  10-mode.scrollY, mode.backButtonWidth,mode.backButtonHeight//2 -  10-mode.scrollY, mode.backButtonWidth//2, mode.backButtonHeight//2 -10-mode.scrollY,mode.backButtonWidth//2, 5-mode.scrollY, 5, mode.backButtonHeight//2-mode.scrollY, fill = purple)
    
    def keyPressed(mode,event): 
        if mode.newRecipeName == None: 
            prompt = "What is the name of your Recipe?"
            mode.newRecipeName = str(mode.getUserInput(prompt)) #get recipeName
        elif mode.newRecipeCookTime == None: 
            prompt = "In minutes, how long does it take to make your entire recipe?"#get cookTime
            mode.newRecipeCookTime = int(mode.getUserInput(prompt)) 
        elif mode.ratingValid == False: 
            prompt = "How would you rate your recipe on a scale from 0 to 5"#get rating
            rate = (mode.getUserInput(prompt))
            if 0 <= int(rate) and int(rate) <= 5: 
                mode.newRecipeRating = int(rate)
                mode.ratingValid = True
        elif mode.calories == None:
            prompt = "About how many calories are in your recipe?"#get calories
            mode.calories = int(mode.getUserInput(prompt))
        elif mode.targetIngredientsEntered == False: 
            if event.key == "Enter": #get ingredients
                mode.targetIngredientsEntered = True
            else: 
                prompt = "Please enter ingredients either individually or as a list seperated by commas. Press Enter key when done."
                tempEnter = mode.getUserInput(prompt)
                if tempEnter!= None: mode.ingredientInput.extend(parser(tempEnter))
        else: 
            mode.createProcedureStr(event)
    
    def drawDoneButton(mode,canvas): 
        canvas.create_rectangle(mode.width - mode.scrollBarWidth - 10 - mode.procedureDoneButtonWidth, 0 - mode.scrollY, mode.width - mode.scrollBarWidth - 10,  mode.procedureDoneButtonHeight - mode.scrollY, fill = darkPurple, outline = darkPurple)
        canvas.create_text(mode.width - mode.scrollBarWidth - 10 - mode.procedureDoneButtonWidth//2, 0 - mode.scrollY+ mode.procedureDoneButtonHeight //2, text = "Done!", font = "Noteworthy-Light 30", fill = "white")
    
    def redrawAll(mode, canvas): 
        canvas.create_rectangle(0,0,mode.width, mode.height, fill=lightBlue, outline = lightBlue)
        mode.drawScrollBar(canvas)
        mode.drawDoneButton(canvas)
        mode.drawBackButton(canvas)
        titleHeight = 80
        infoBoxWidth = 250
        infoBoxHeight = 200
        canvas.create_text(mode.width//2, mode.sideMargin-mode.scrollY, text = "Create My Recipe", font = "Noteworthy-Light 40", fill = "white")
        canvas.create_text(mode.width//2, mode.sideMargin + 60-mode.scrollY, text = "Press Any Key to start!", font = "Noteworthy-Light 30", fill = "white")
        if mode.newRecipeName != None: 
            canvas.delete("all")
            canvas.create_rectangle(0,0-mode.scrollY,mode.width, mode.height-mode.scrollY, fill=lightBlue, outline = lightBlue)
            mode.drawScrollBar(canvas)
            mode.drawDoneButton(canvas)
            mode.drawBackButton(canvas)
            canvas.create_text(mode.width//2, mode.sideMargin + 30- mode.scrollY, text = "Press Any Key To Continue!", font = "Noteworthy-Light 30", fill = "white")
            canvas.create_rectangle(mode.sideMargin, mode.procedureDoneButtonHeight + 30 - mode.scrollY, mode.width - mode.scrollBarWidth - 10, mode.procedureDoneButtonHeight + 30 + titleHeight-mode.scrollY, fill = red, outline = red)
            canvas.create_text(mode.width//2, mode.procedureDoneButtonHeight + 30 + titleHeight//2 - mode.scrollY, text = f"{mode.newRecipeName}", font = "Noteworthy-Light 40", fill = "white")
        if mode.newRecipeCookTime != None: 
            canvas.create_rectangle(mode.sideMargin, mode.procedureDoneButtonHeight +  80 + titleHeight-mode.scrollY, mode.sideMargin + infoBoxWidth,  mode.procedureDoneButtonHeight + 80 + titleHeight + infoBoxHeight - mode.scrollY, fill = orange, outline = orange)
            canvas.create_text(mode.sideMargin + 20, mode.procedureDoneButtonHeight + 80 + titleHeight + infoBoxHeight//4 - mode.scrollY, text = f"Total Cook Time: {mode.newRecipeCookTime}", font = "Helvetica 20 bold", fill = "brown", anchor = W)
        if mode.newRecipeRating != None and mode.ratingValid != False:
            canvas.create_text(mode.sideMargin + 20, mode.procedureDoneButtonHeight + 80 + titleHeight + infoBoxHeight//2 - mode.scrollY, text = f"Rating: {mode.newRecipeRating}", font = "Helvetica 20 bold",fill = "brown",  anchor = W)
        if mode.calories != None:
            canvas.create_text(mode.sideMargin + 20, mode.procedureDoneButtonHeight + 80 + titleHeight + 3*infoBoxHeight//4 - mode.scrollY, text = f"Calories: {mode.calories}", font = "Helvetica 20 bold",fill = "brown", anchor = W)
        if mode.ingredientInput!= []: 
            ingredientBoxWidth = 300
            fontSize = 8
            lineCounter = 0
            newStart = mode.procedureDoneButtonHeight + 80 + titleHeight + infoBoxHeight  + 40
            for element in mode.ingredientInput: 
                if len(element) * fontSize <= ingredientBoxWidth: 
                    lineCounter +=1
                else: 
                    counter = 0
                    for word in element.split():
                        if (counter + len(word) + 1)* fontSize < ingredientBoxWidth:
                            counter += len(word) + 1
                        else:
                            lineCounter +=1
                            counter = len(word)+ 1
            canvas.create_rectangle(mode.sideMargin, newStart - mode.scrollY, mode.sideMargin + ingredientBoxWidth, newStart+ 35*lineCounter + 60 - mode.scrollY, fill = red, outline = red)
            canvas.create_text(mode.sideMargin + ingredientBoxWidth//2, newStart + lineCounter - mode.scrollY+ 35, text = f"Ingredients:", font = "Noteworthy-Light 30")

            incr = newStart + 90
            for element in mode.ingredientInput: 
                if len(element) * fontSize <= ingredientBoxWidth: 
                        canvas.create_text(mode.sideMargin +10,  incr - mode.scrollY, text = f" - {element}", font = f"Helvetica 15 bold", anchor = W)
                        incr+=30
                else: 
                    counter = 0
                    displayStr = ''
                    for word in element.split():
                        if (counter + len(word) + 1)* fontSize < ingredientBoxWidth:
                            displayStr = displayStr + word + " "
                            counter += len(word) + 1
                        else:
                            canvas.create_text(mode.sideMargin + 10, incr- mode.scrollY, text = f"{displayStr}", font = f"Helvetica 15 bold", anchor = W)
                            incr+=30
                            displayStr = word + " "
                            counter = len(word)+ 1
            
            ProcedureBoxWidth = 350
            start = mode.procedureDoneButtonHeight + 80 + titleHeight
            fontSize = 7
            counter = 0
            procLineCounter = 0
            for word in mode.newRecipeProcedure.split(): 
                    if (counter + len(word) + 1)* fontSize < ingredientBoxWidth:
                        counter += len(word) + 1
                    else:
                        procLineCounter +=1
                        counter = len(word) + 1
            canvas.create_rectangle(mode.sideMargin + ingredientBoxWidth + 30,start - mode.scrollY,mode.width - mode.scrollBarWidth -10, start - mode.scrollY + 28*procLineCounter + 100, fill = purple, outline = purple)
            displayStr = ''
            canvas.create_text((ingredientBoxWidth+ mode.width - mode.scrollBarWidth)//2, start + 30 - mode.scrollY, text = "Procedure:", font = f"Noteworthy-Light 30", anchor = W)
            incr = start + 70

            for word in mode.newRecipeProcedure.split(): 
                if word!= "\n" and word !="\r":
                    # print(word)
                    if (counter + len(word) + 1)* fontSize < ProcedureBoxWidth:
                        displayStr = displayStr + str(word) + " "
                        counter += len(word) + 1
                    else:
                        
                        canvas.create_text(mode.sideMargin + ingredientBoxWidth + 40, incr - mode.scrollY, text = f"{displayStr}", font = f"Helvetica 15 bold", anchor = W)
                        incr+=30
                        displayStr = str(word) + " "
                        counter = len(word) + 1
            canvas.create_text(mode.sideMargin + ingredientBoxWidth+ 40, incr-mode.scrollY, text = f"{displayStr}", font = f"Helvetica 15 bold", anchor = W)       
        if mode.recipeProcedureEntered == True: 
            canvas.delete("all")
            canvas.create_rectangle(0,0,mode.width,mode.height, fill = lightBlue, outline = lightBlue)
            mode.drawBackButton(canvas)
            canvas.create_text(mode.width//2, mode.height//2 - mode.sideMargin, text = f"Recipe {mode.newRecipeObject} \nsuccessfully created", font = "Noteworthy-Light 50 bold")

class ViewMyRecipesMode(Mode): 
    def appStarted(mode): 
        print("in view my new recipes")
        mode.startingPosY = 70
        mode.incr = 50
        mode.myNewRecipes = readFromMyRecipes()
        mode.myChosenRecipe = None
        mode.recipeChosen = False
        mode.sideMargin = 50
        mode.backClicked = False 
        mode.backButtonWidth = 70
        mode.backButtonHeight = 40
        mode.scrollY = 0 
        mode.scrollBarWidth = 35
        mode.scrollBarHeight = 100
        mode.FavoritesBookMarkWidth = 150
        mode.FavoritesBookMarkHeight = 50
        
    def mousePressed(mode,event): 
        if mode.recipeChosen == True and event.x <= mode.backButtonWidth and event.y - mode.scrollY <=mode.backButtonHeight: 
            mode.backClicked = True 
            mode.recipeChosen = False
            mode.myChosenRecipe = None
            mode.backClicked = False
        elif mode.recipeChosen == False and event.x <= mode.backButtonWidth and event.y - mode.scrollY <=mode.backButtonHeight: 
            mode.app.setActiveMode(mode.app.splashScreenMode)
        elif event.y >= 100 - mode.scrollY and mode.sideMargin<=event.x and event.x <= mode.width - mode.scrollBarWidth and len(mode.myNewRecipes) != 0: 
            mode.myChosenRecipe = mode.myNewRecipes[int(event.y + mode.scrollY - 100)//120]
            mode.recipeChosen = True
            print(mode.myChosenRecipe)
        
    def mouseDragged(mode,event): 
        mode.scrollY = event.y 
    
    def drawScrollBar(mode,canvas): 
        canvas.create_rectangle(mode.width - mode.scrollBarWidth, mode.scrollY - mode.scrollBarHeight//2, mode.width, mode.scrollY + mode.scrollBarHeight//2, fill = purple, outline = purple)
    
    def drawBackButton(mode,canvas): 
        canvas.create_polygon(5, mode.backButtonHeight//2-mode.scrollY, mode.backButtonWidth//2, mode.backButtonHeight - 5-mode.scrollY,mode.backButtonWidth//2, mode.backButtonHeight//2 +  10-mode.scrollY, mode.backButtonWidth, mode.backButtonHeight//2 +  10-mode.scrollY, mode.backButtonWidth,mode.backButtonHeight//2 -  10-mode.scrollY, mode.backButtonWidth//2, mode.backButtonHeight//2 -10-mode.scrollY,mode.backButtonWidth//2, 5-mode.scrollY, 5, mode.backButtonHeight//2-mode.scrollY, fill = purple)
    
    def displayRecipeSpecifics(mode,canvas): 
        canvas.delete("all")
        canvas.create_rectangle(0,0,mode.width, mode.height, fill = lightBlue, outline = lightBlue)
        mode.drawScrollBar(canvas)
        mode.drawBackButton(canvas)
        titleHeight = 80
        canvas.create_rectangle(mode.backButtonWidth, mode.FavoritesBookMarkHeight + 30 - mode.scrollY, mode.width - mode.backButtonWidth, mode.FavoritesBookMarkHeight + 50 + titleHeight-mode.scrollY, fill = red, outline = red)
        canvas.create_text(mode.backButtonWidth +20, mode.FavoritesBookMarkHeight + 30 +titleHeight//2 - mode.scrollY, text = f"'{mode.myChosenRecipe.recipeName}'", font = "Noteworthy-Light 40 bold", anchor = W, fill = "white")
        
        infoBoxWidth = 250
        infoBoxHeight = 200
        canvas.create_rectangle(mode.sideMargin, mode.FavoritesBookMarkHeight + 80 + titleHeight-mode.scrollY, mode.sideMargin + infoBoxWidth,  mode.FavoritesBookMarkHeight + 80 + titleHeight+ infoBoxHeight - mode.scrollY, fill = orange, outline = orange)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + infoBoxHeight//4 - mode.scrollY, text = f"Total Cook Time: {mode.myChosenRecipe.totalCookTime}", font = "Helvetica 20 bold", fill = "brown", anchor = W)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + infoBoxHeight//2 - mode.scrollY, text = f"Rating: {mode.myChosenRecipe.rating}", font = "Helvetica 20 bold",fill = "brown",  anchor = W)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + 3*infoBoxHeight//4 - mode.scrollY, text = f"Calories: {mode.myChosenRecipe.totalCalories}", font = "Helvetica 20 bold",fill = "brown", anchor = W)
        
        printLastWord = False
        fontSize = 10
        lineCounter = 0
        ingredientBoxWidth = 330
        for element in mode.myChosenRecipe.ingredients.split(","): 
            if element[0] == "[": element = element[1:]
            if element[-1] == "]": element = element[:-1]
            if len(element) * fontSize <= ingredientBoxWidth: 
                lineCounter +=1
            else: 
                counter = 0
                for word in element.split():
                    if (counter + len(word) + 1)* fontSize <= ingredientBoxWidth:
                        counter += len(word)
                    elif (counter + len(word) + 1)* fontSize > ingredientBoxWidth:
                        printLastWord = True
                        counter = len(word)+ 1
                        lineCounter +=1 
                    if printLastWord == True and word == element.split()[-1]:
                        lineCounter+=1
                        counter = 0


        ingredientBoxWidth = 300
        newStart = mode.FavoritesBookMarkHeight + 80 + titleHeight+ infoBoxHeight  + 40
        canvas.create_rectangle(mode.sideMargin, newStart - mode.scrollY, mode.sideMargin + ingredientBoxWidth, newStart+ 40* lineCounter + 60- mode.scrollY, fill = red, outline = red)
        canvas.create_text(ingredientBoxWidth//2, newStart - mode.scrollY+ 25, text = f"Ingredients:", font = "Noteworthy-Light 30", anchor = W)
        
        ingredientBoxWidth = 300
        newStart = mode.FavoritesBookMarkHeight + 80 + titleHeight+ infoBoxHeight  + 40
        canvas.create_rectangle(mode.sideMargin, newStart - mode.scrollY, mode.sideMargin + ingredientBoxWidth, newStart+ 40* lineCounter + 60- mode.scrollY, fill = red, outline = red)
        canvas.create_text(ingredientBoxWidth//2, newStart - mode.scrollY+ 25, text = f"Ingredients:", font = "Noteworthy-Light 30", anchor = W)
       
        incr = newStart + 60

        ingredientBoxWidth = 330
        printLastWord = False
        wordsDisplayedSoFar = []
        for element in mode.myChosenRecipe.ingredients.split(","): 
            if element[0] == "[": element = element[1:]
            if element[-1] == "]": element = element[:-1]
            element = element.replace("\u2009", " ")
            if len(element) * fontSize <= ingredientBoxWidth: 
                    canvas.create_text(mode.sideMargin +10,  incr - mode.scrollY, text = f"{element}", font = f"Helvetica 15 bold", anchor = W)
                    incr+=30
                    wordsDisplayedSoFar.append(element)
                    
            else: 
                counter = 0
                displayStr = ''
                for word in element.split():
                    word = word.replace("\u2009", " ")
                    word = word.strip()
                    if (counter + len(word) + 1)* fontSize < ingredientBoxWidth:
                        displayStr = displayStr + str(word) + " "
                        counter += len(word)+1
                    elif (counter + len(word) + 1)* fontSize >= ingredientBoxWidth:
                        printLastWord = True
                        wordsDisplayedSoFar.append(displayStr)
                        canvas.create_text(mode.sideMargin + 10, incr- mode.scrollY, text = f"{displayStr}", font = f"Helvetica 15 bold", anchor = W)
                        incr+=30
                        displayStr = word + " "
                        counter = len(word)+ 1
                    if printLastWord == True and displayStr not in wordsDisplayedSoFar:
                        canvas.create_text(mode.sideMargin + 10, incr- mode.scrollY, text = f"{word}", font = f"Helvetica 15 bold", anchor = W)
                        incr+=30
                        printLastWord = False
                        displayStr = ''

        ingredientBoxWidth = 300
        ProcedureBoxWidth = 330
        start = mode.FavoritesBookMarkHeight + 80 + titleHeight
        fontSize = 7
        counter = 0
        procLineCounter = 0
        for word in mode.myChosenRecipe.getProcedure().split(): 
            if word!= "\n" and word !="\r":
                if (counter + len(word) + 1)* fontSize < ProcedureBoxWidth:
                    counter += len(word) + 1
                else:
                    procLineCounter +=1
                    counter = len(word) + 1
        canvas.create_rectangle(mode.sideMargin + ingredientBoxWidth + 30,start - mode.scrollY,mode.width - mode.scrollBarWidth -10, start - mode.scrollY + 30*procLineCounter + 120, fill = purple, outline = purple)
        displayStr = ''
        canvas.create_text((ingredientBoxWidth+ mode.width - mode.scrollBarWidth)//2, start + 30 - mode.scrollY, text = "Procedure:", font = f"Noteworthy-Light 30", anchor = W)
        incr = start + 70
        for word in mode.myChosenRecipe.getProcedure().split(): 
            if word!= "\n" and word !="\r":
                if (counter + len(word) + 1)* fontSize < ProcedureBoxWidth:
                    displayStr = displayStr + str(word) + " "
                    counter += len(word) + 1
                else:
                    
                    canvas.create_text(mode.sideMargin + ingredientBoxWidth + 40, incr - mode.scrollY, text = f"{displayStr}", font = f"Helvetica 15 bold", anchor = W)
                    incr+=30
                    displayStr = str(word) + " "
                    counter = len(word) + 1
        canvas.create_text(mode.sideMargin + ingredientBoxWidth+ 40, incr-mode.scrollY, text = f"{displayStr}", font = f"Helvetica 15 bold", anchor = W)
       
    def redrawAll(mode, canvas): 
        pos = 0
        recipeBoxWidth = mode.width - 2*mode.sideMargin
        recipeBoxHeight = 100
        recipeIncr = 20
        heightPlacement = 100
        canvas.create_rectangle(0,0,mode.width,mode.height, fill = lightBlue, outline = lightBlue)
        mode.drawBackButton(canvas)
        mode.drawScrollBar(canvas)
        if mode.recipeChosen == False and mode.myNewRecipes == None:
            canvas.create_text(mode.width//4, 50 - mode.scrollY, text = f"Create A Recipe In The Home Screen and See It Pop Up Here!", font = "Noteworthy-Light 40 bold", fill = "white")
        elif mode.recipeChosen == False and mode.myNewRecipes != None:
            canvas.create_text(mode.width//2, 50 - mode.scrollY, text = f'My Own Recipes', font = "Noteworthy-Light 50 bold", fill = "brown")
            for rec in mode.myNewRecipes:
                canvas.create_rectangle(mode.sideMargin-5, heightPlacement - mode.scrollY, mode.sideMargin + recipeBoxWidth, heightPlacement - mode.scrollY + recipeBoxHeight, fill = orange, outline = orange )
                canvas.create_text(mode.sideMargin+5, heightPlacement - mode.scrollY + recipeBoxHeight//2, text = f"{rec}", font = "Noteworthy-Light 30 bold", fill = "brown", anchor = W)
                canvas.create_text(mode.width - mode.sideMargin - mode.scrollBarWidth, heightPlacement - mode.scrollY+ recipeBoxHeight//3, text = f"Cook Time: {rec.totalCookTime}", font = "Helvetica 15 bold", fill = "brown", anchor = E)
                canvas.create_text(mode.width - mode.sideMargin - mode.scrollBarWidth, heightPlacement - mode.scrollY+ 2*recipeBoxHeight//3, text = f"Rating: {rec.rating}", font = "Helvetica 15 bold", fill = "brown", anchor = E)
                heightPlacement += recipeBoxHeight + recipeIncr
        else: 
            mode.displayRecipeSpecifics(canvas)
class ViewFavoritesMode(Mode): 
    def appStarted(mode): 
        print("in view favorite recipes")
        mode.startingPosY = 70
        mode.incr = 50
        mode.myFavoriteRecipes = readFromMyFavorites()
        mode.myChosenRecipe = None
        mode.sideMargin = 50
        mode.recipeHasBeenChosen = False
        mode.scrollY = 0
        mode.scrollBarWidth = 35
        mode.scrollBarHeight = 100
        mode.isInFavorites = True
        mode.FavoritesBookMarkWidth = 150
        mode.FavoritesBookMarkHeight = 50
        mode.backClicked = False 
        mode.backButtonWidth = 70
        mode.backButtonHeight = 40
    def mousePressed(mode,event): 
        if mode.recipeHasBeenChosen: 
            if mode.myChosenRecipe != None: 
                mode.isInFavorites = checkFavorites(mode.myChosenRecipe)
            if event.x <= mode.backButtonWidth and event.y - mode.scrollY <=mode.backButtonHeight: 
                mode.backClicked = True 
                mode.recipeHasBeenChosen = False
                mode.chosenRecipe = None
                mode.backClicked = False
            
            if mode.width - mode.scrollBarWidth - 50 - mode.FavoritesBookMarkWidth<= event.x  and event.x <= mode.width - mode.scrollBarWidth - 50 and 0 - mode.scrollY <= event.y and event.y <= mode.FavoritesBookMarkHeight - mode.scrollY: 
                if mode.isInFavorites == True: 
                    removeFavorites(mode.myChosenRecipe)
                    mode.myFavoriteRecipes = readFromMyFavorites()
                    mode.isInFavorites = False
                elif mode.isInFavorites == False: 
                    addFavorites(mode.myChosenRecipe)
                    mode.isInFavorites = True
        else: 
            if event.x <= mode.backButtonWidth and event.y - mode.scrollY <=mode.backButtonHeight: 
                mode.app.setActiveMode(mode.app.splashScreenMode)
            elif mode.startingPosY <= event.y  and event.x <= mode.width - mode.scrollBarWidth and len(mode.myFavoriteRecipes) != 0: 
                mode.myChosenRecipe = mode.myFavoriteRecipes[int(event.y + mode.scrollY - 150)//120]
                mode.recipeHasBeenChosen = True
                print(mode.myChosenRecipe)
    def mouseDragged(mode,event): 
            mode.scrollY = event.y
    
    def drawScrollBar(mode,canvas): 
        canvas.create_rectangle(mode.width - mode.scrollBarWidth, mode.scrollY - mode.scrollBarHeight//2, mode.width, mode.scrollY + mode.scrollBarHeight//2, fill = purple, outline = purple)
    
    def drawBackButton(mode,canvas): 
        canvas.create_polygon(5, mode.backButtonHeight//2-mode.scrollY, mode.backButtonWidth//2, mode.backButtonHeight - 5-mode.scrollY,mode.backButtonWidth//2, mode.backButtonHeight//2 +  10-mode.scrollY, mode.backButtonWidth, mode.backButtonHeight//2 +  10-mode.scrollY, mode.backButtonWidth,mode.backButtonHeight//2 -  10-mode.scrollY, mode.backButtonWidth//2, mode.backButtonHeight//2 -10-mode.scrollY,mode.backButtonWidth//2, 5-mode.scrollY, 5, mode.backButtonHeight//2-mode.scrollY, fill = purple)
    
    def drawFavoritesBookmark(mode,canvas): 
        if mode.isInFavorites == True: 
            color = lightPink
        else: color = aqua
        canvas.create_rectangle(mode.width - mode.scrollBarWidth - 50 - mode.FavoritesBookMarkWidth,0 - mode.scrollY, mode.width - mode.scrollBarWidth - 50, mode.FavoritesBookMarkHeight - mode.scrollY, fill = color,outline = color)
        canvas.create_text(mode.width - mode.scrollBarWidth - 50 - mode.FavoritesBookMarkWidth//2, mode.FavoritesBookMarkHeight//2 - mode.scrollY, text = "Favorite", fill = "white")
    
    def redrawAll(mode, canvas): 
        pos = 0
        canvas.create_rectangle(0,0,mode.width,mode.height, fill = lightBlue, outline = lightBlue)
        mode.drawBackButton(canvas)
        if mode.myFavoriteRecipes!= None: 
            mode.drawScrollBar(canvas)
            if mode.recipeHasBeenChosen == False: 
                canvas.create_text(mode.width//2, 50 - mode.scrollY, text = f'My Favorite Recipes', font = "Noteworthy-Light 50 bold", fill = "brown")
                recipeBoxWidth = mode.width - 2*mode.sideMargin
                recipeBoxHeight = 100
                recipeIncr = 20
                heightPlacement = 100
                if mode.myFavoriteRecipes!= None: 
                    for row in range(len(mode.myFavoriteRecipes)):
                        canvas.create_rectangle(mode.sideMargin-5, heightPlacement - mode.scrollY, mode.sideMargin + recipeBoxWidth, heightPlacement - mode.scrollY + recipeBoxHeight, fill = orange, outline = orange )
                        canvas.create_text(mode.sideMargin+5, heightPlacement - mode.scrollY + recipeBoxHeight//2, text = f"{mode.myFavoriteRecipes[row]}", font = "Noteworthy-Light 30 bold", fill = "brown", anchor = W)
                        canvas.create_text(mode.width - mode.sideMargin - mode.scrollBarWidth, heightPlacement - mode.scrollY+ recipeBoxHeight//3, text = f"Cook Time: {mode.myFavoriteRecipes[row].totalCookTime}", font = "Helvetica 15 bold", fill = "brown", anchor = E)
                        canvas.create_text(mode.width - mode.sideMargin - mode.scrollBarWidth, heightPlacement - mode.scrollY+ 2*recipeBoxHeight//3, text = f"Rating: {mode.myFavoriteRecipes[row].rating}", font = "Helvetica 15 bold", fill = "brown", anchor = E)
                        heightPlacement += recipeBoxHeight + recipeIncr
            if mode.myFavoriteRecipes!= None and mode.recipeHasBeenChosen: 
                mode.displaySpecifics(canvas)
                
    def displaySpecifics(mode,canvas): 
        canvas.delete("all")
        canvas.create_rectangle(0,0,mode.width, mode.height, fill = lightBlue, outline = lightBlue)
        mode.drawScrollBar(canvas)
        mode.drawBackButton(canvas)
        mode.drawFavoritesBookmark(canvas)
        titleHeight = 80
       
        canvas.create_rectangle(mode.backButtonWidth, mode.FavoritesBookMarkHeight + 30 - mode.scrollY, mode.width - mode.backButtonWidth, mode.FavoritesBookMarkHeight + 50 + titleHeight-mode.scrollY, fill = red, outline = red)
        canvas.create_text(mode.backButtonWidth +20, mode.FavoritesBookMarkHeight + 30 +titleHeight//2 - mode.scrollY, text = f"'{mode.myChosenRecipe.recipeName}'", font = "Noteworthy-Light 40 bold", anchor = W, fill = "white")
        
        infoBoxWidth = 250
        infoBoxHeight = 200
        canvas.create_rectangle(mode.sideMargin, mode.FavoritesBookMarkHeight + 80 + titleHeight-mode.scrollY, mode.sideMargin + infoBoxWidth,  mode.FavoritesBookMarkHeight + 80 + titleHeight+ infoBoxHeight - mode.scrollY, fill = orange, outline = orange)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + infoBoxHeight//4 - mode.scrollY, text = f"Total Cook Time: {mode.myChosenRecipe.totalCookTime}", font = "Helvetica 20 bold", fill = "brown", anchor = W)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + infoBoxHeight//2 - mode.scrollY, text = f"Rating: {mode.myChosenRecipe.rating}", font = "Helvetica 20 bold",fill = "brown",  anchor = W)
        canvas.create_text(mode.sideMargin + 20, mode.FavoritesBookMarkHeight + 80 + titleHeight + 3*infoBoxHeight//4 - mode.scrollY, text = f"Calories: {mode.myChosenRecipe.totalCalories}", font = "Helvetica 20 bold",fill = "brown", anchor = W)
        
        printLastWord = False
        fontSize = 10
        lineCounter =0
        ingredientBoxWidth = 330
        for element in mode.myChosenRecipe.ingredients.split(","): 
            
            if element[0] == "[": element = element[1:]
            if element[-1] == "]": element = element[:-1]
            if len(element) * fontSize <= ingredientBoxWidth: 
                lineCounter +=1
            else: 
                counter = 0
                for word in element.split():
                    if (counter + len(word) + 1)* fontSize <= ingredientBoxWidth:
                        counter += len(word)
                    elif (counter + len(word) + 1)* fontSize > ingredientBoxWidth:
                        printLastWord = True
                        counter = len(word)+ 1
                        lineCounter +=1 
                    if printLastWord == True and word == element.split()[-1]:
                        lineCounter+=1
                        counter = 0

        ingredientBoxWidth = 300
        newStart = mode.FavoritesBookMarkHeight + 80 + titleHeight+ infoBoxHeight  + 40
        canvas.create_rectangle(mode.sideMargin, newStart - mode.scrollY, mode.sideMargin + ingredientBoxWidth, newStart+ 40* lineCounter + 60- mode.scrollY, fill = red, outline = red)
        canvas.create_text(ingredientBoxWidth//2, newStart - mode.scrollY+ 25, text = f"Ingredients:", font = "Noteworthy-Light 30", anchor = W)
       
        incr = newStart + 60

        ingredientBoxWidth = 330
        printLastWord = False
        wordsDisplayedSoFar = []
        for element in mode.myChosenRecipe.ingredients.split(","): 
            if element[0] == "[": element = element[1:]
            if element[-1] == "]": element = element[:-1]
            element = element.replace("\u2009", " ")
            if len(element) * fontSize <= ingredientBoxWidth: 
                    canvas.create_text(mode.sideMargin +10,  incr - mode.scrollY, text = f"{element}", font = f"Helvetica 15 bold", anchor = W)
                    incr+=30
                    wordsDisplayedSoFar.append(element)
                    
            else: 
                counter = 0
                displayStr = ''
                for word in element.split():
                    word = word.replace("\u2009", " ")
                    word = word.strip()
                    if (counter + len(word) + 1)* fontSize < ingredientBoxWidth:
                        displayStr = displayStr + str(word) + " "
                        counter += len(word)+1
                    elif (counter + len(word) + 1)* fontSize >= ingredientBoxWidth:
                        printLastWord = True
                        wordsDisplayedSoFar.append(displayStr)
                        canvas.create_text(mode.sideMargin + 10, incr- mode.scrollY, text = f"{displayStr}", font = f"Helvetica 15 bold", anchor = W)
                        incr+=30
                        displayStr = word + " "
                        counter = len(word)+ 1
                    if printLastWord == True and displayStr not in wordsDisplayedSoFar:
                        canvas.create_text(mode.sideMargin + 10, incr- mode.scrollY, text = f"{word}", font = f"Helvetica 15 bold", anchor = W)
                        incr+=30
                        printLastWord = False
                        displayStr = ''
        ingredientBoxWidth = 300
        ProcedureBoxWidth = 330
        start = mode.FavoritesBookMarkHeight + 80 + titleHeight
        fontSize = 7
        counter = 0
        procLineCounter = 0
        for word in mode.myChosenRecipe.getProcedure().split(): 
            if word!= "\n" and word !="\r":
                if (counter + len(word) + 1)* fontSize < ProcedureBoxWidth:
                    counter += len(word) + 1
                else:
                    procLineCounter +=1
                    counter = len(word) + 1
        canvas.create_rectangle(mode.sideMargin + ingredientBoxWidth + 30,start - mode.scrollY,mode.width - mode.scrollBarWidth -10, start - mode.scrollY + 30*procLineCounter + 120, fill = purple, outline = purple)
        displayStr = ''
        canvas.create_text((ingredientBoxWidth+ mode.width - mode.scrollBarWidth)//2, start + 30 - mode.scrollY, text = "Procedure:", font = f"Noteworthy-Light 30", anchor = W)
        incr = start + 70
        for word in mode.myChosenRecipe.getProcedure().split(): 
            if word!= "\n" and word !="\r":
                if (counter + len(word) + 1)* fontSize < ProcedureBoxWidth:
                    displayStr = displayStr + str(word) + " "
                    counter += len(word) + 1
                else:
                    
                    canvas.create_text(mode.sideMargin + ingredientBoxWidth + 40, incr - mode.scrollY, text = f"{displayStr}", font = f"Helvetica 15 bold", anchor = W)
                    incr+=30
                    displayStr = str(word) + " "
                    counter = len(word) + 1
        canvas.create_text(mode.sideMargin + ingredientBoxWidth+ 40, incr-mode.scrollY, text = f"{displayStr}", font = f"Helvetica 15 bold", anchor = W)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.searchByIngrMode = SearchByIngrMode()
        app.recipePlanMode = RecipePlanMode()
        app.createNewRecipeMode = CreateNewRecipeMode()
        app.viewMyRecipesMode = ViewMyRecipesMode()
        app.viewFavoritesMode = ViewFavoritesMode()
        app.setActiveMode(app.splashScreenMode)
app = MyModalApp(width=800, height=800)