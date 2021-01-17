import requests, re, random, string, copy
from bs4 import BeautifulSoup
from cmu_112_graphics import *
from Recipe import *
from RecipeDepositoryScraper import *
from SortAlgorithms import*
from AllRecipesScraper import*
#This file is handles the entire backend. It recieves the information from the User Interphace, 
#and begins one of 2 process, either the backtracking algorithm, or the recipe search.

#The pluralization Bug Fix is necessary to offset the difference between words such as "egg" and "eggs".
def pluralizationBugFix(targetIngredientList): 
    hasMultipleWords = False #This will also look to see if there is multiple words, which is another bug fix handled within the Sorting Algorithm File
    newIngredientList = copy.deepcopy(targetIngredientList)
    for ingr in targetIngredientList: #loop through every ingredient
        ingr = ingr.strip()
        length = len(ingr)
        if " " in ingr: 
            hasMultipleWords = True #if there is multiple words, then set to True 
        if ingr[length-2:length] == "es": #These cases are generalized grammar rules. 
            newIngredientList.append(ingr[0:-3])
        elif ingr[length-1:length] == "s": 
            newIngredientList.append(ingr[0:-1])
        else: 
            newIngredientList.append(str(ingr+"s"))
            newIngredientList.append(str(ingr+"es"))
    #By the end of this, we should have both the singularized version and plural version within the ingredientsList
    return newIngredientList, hasMultipleWords 
    
def getCuisineFromInput(targetIngredientList,antiList, cuisineChoice, mode, createRecipePlan = None, calMin=None, calMax=None, numberOfRecipesWanted=None, tolerance = 0): 
    targetIngredientList, hasMultipleWords = pluralizationBugFix(targetIngredientList) #get the new search list 
    #I chose to create a dictionary of categories to links, since searching from the main page of a site is highly innefficient, and due to the way the sites are organized, quite difficult
    choiceDict = {
        "Appetizers":["https://www.allrecipes.com/recipes/76/appetizers-and-snacks/","https://www.therecipedepository.com/category/appetizers"],
        "Asian Fusion":["https://www.therecipedepository.com/category/asian-fusion"],
        "Bacon":["https://www.allrecipes.com/recipes/669/meat-and-poultry/pork/bacon/","https://www.therecipedepository.com/category/bacon"],
        "Barbeque":["https://www.allrecipes.com/recipes/88/bbq-grilling/","https://www.therecipedepository.com/category/barbeque"], 
        "Beverages":["https://www.allrecipes.com/recipes/77/drinks/","https://www.therecipedepository.com/category/beverages"],
        "Breads":["https://www.allrecipes.com/recipes/156/bread/","https://www.therecipedepository.com/category/breads"],
        "Breakfast":["https://www.allrecipes.com/recipes/78/breakfast-and-brunch/","https://www.therecipedepository.com/category/breakfast"],
        "Brunch":["https://www.therecipedepository.com/category/brunch", "https://www.allrecipes.com/recipes/78/breakfast-and-brunch/"],
        "Candy":["https://www.allrecipes.com/recipes/372/desserts/candy/","https://www.therecipedepository.com/category/candy"], 
        "Casseroles":["https://www.allrecipes.com/recipes/249/main-dish/casseroles/","https://www.therecipedepository.com/category/casseroles"], 
        "Cheese":["https://www.allrecipes.com/recipes/16106/ingredients/dairy/cheese/","https://www.therecipedepository.com/category/cheese"], 
        "Chicken":["https://www.allrecipes.com/recipes/92/meat-and-poultry/","https://www.therecipedepository.com/category/chicken"],
        "Chinese":["https://www.allrecipes.com/recipes/695/world-cuisine/asian/chinese/","https://www.therecipedepository.com/category/chinese"],  
        "Desserts":["https://www.allrecipes.com/recipes/79/desserts/","https://www.allrecipes.com/recipes/372/desserts/candy/", "https://www.therecipedepository.com/category/deserts"],
        "Dinner":["https://www.allrecipes.com/recipes/17562/dinner/"], 
        "Fish":["https://www.allrecipes.com/recipes/411/seafood/fish/", "https://www.therecipedepository.com/category/fish"], 
        "French":["https://www.allrecipes.com/recipes/721/world-cuisine/european/french/","https://www.therecipedepository.com/category/french"], 
        "Fruit":["https://www.allrecipes.com/recipes/1058/fruits-and-vegetables/fruits/","https://www.therecipedepository.com/category/fruit"],
        "German":["https://www.allrecipes.com/recipes/722/world-cuisine/european/german/","https://www.therecipedepository.com/category/german"], 
        "Greek":["https://www.allrecipes.com/recipes/731/world-cuisine/european/greek/","https://www.therecipedepository.com/category/greek"], 
        "Grill":["https://www.allrecipes.com/recipes/88/bbq-grilling/","https://www.therecipedepository.com/category/grill"], 
        "Healthy Choices":["https://www.allrecipes.com/recipes/84/healthy-recipes/","https://www.therecipedepository.com/category/healthy-choices"], 
        "Holiday & Seasonal":["https://www.allrecipes.com/recipes/85/holidays-and-events/","https://www.therecipedepository.com/category/holiday-and-seasonal"], 
        "Indian":["https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/","https://www.therecipedepository.com/category/indian"], 
        "Italian":["https://www.allrecipes.com/recipes/723/world-cuisine/european/italian/","https://www.therecipedepository.com/category/italian"], 
        "Japanese":["https://www.allrecipes.com/recipes/699/world-cuisine/asian/japanese/","https://www.therecipedepository.com/category/japanese"], 
        "Lamb":["https://www.allrecipes.com/recipes/203/meat-and-poultry/lamb/","https://www.therecipedepository.com/category/lamb"], 
        "Lunch":["https://www.allrecipes.com/recipes/17561/lunch/"],
        "Mexican":["https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/","https://www.therecipedepository.com/category/mexican"], 
        "Pasta":["https://www.allrecipes.com/recipes/95/pasta-and-noodles/","https://www.therecipedepository.com/category/pasta"], 
        "Pizza":["https://www.therecipedepository.com/category/pizza"], 
        "Quick and Easy":["https://www.allrecipes.com/recipes/1947/everyday-cooking/quick-and-easy/"],
        "Salads":["https://www.allrecipes.com/recipes/96/salad/"],
        "Sandwiches":["https://www.allrecipes.com/recipes/251/main-dish/sandwiches/","https://www.therecipedepository.com/category/sandwhiches"],
        "Seafood":["https://www.allrecipes.com/recipes/93/seafood/","https://www.therecipedepository.com/category/seafood"], 
        "Slow Cooker":["https://www.allrecipes.com/recipes/253/everyday-cooking/slow-cooker/","https://www.therecipedepository.com/category/slow-cooker"], 
        "Soups":["https://www.allrecipes.com/recipes/94/soups-stews-and-chili/"],
        "Spanish":["https://www.allrecipes.com/recipes/726/world-cuisine/european/spanish/"],
        "Snacks":["https://www.therecipedepository.com/category/snacks"], 
        "Thai":["https://www.allrecipes.com/recipes/702/world-cuisine/asian/thai/","https://www.therecipedepository.com/category/thai"], 
        "Turkey":["https://www.allrecipes.com/recipes/206/meat-and-poultry/turkey/","https://www.therecipedepository.com/category/turkey"], 
        "Vegan":["https://www.allrecipes.com/recipes/1227/everyday-cooking/vegan/"], 
        "Vegetables":["https://www.allrecipes.com/recipes/1059/fruits-and-vegetables/vegetables/","https://www.therecipedepository.com/category/vegetables"],
        "Vegetarian":["https://www.allrecipes.com/recipes/87/everyday-cooking/vegetarian/","https://www.therecipedepository.com/category/vegetarian"], 
        }
    if cuisineChoice == "Surprise Me": 
        chosenCuisineLinks = choiceDict[random.choice(list(choiceDict))]
    else: chosenCuisineLinks = choiceDict[cuisineChoice]
    if createRecipePlan == True: #Create Recipe Plan is the boolean corresponding to begin the backtracking algorithm process
        return planRecipe(targetIngredientList,antiList, chosenCuisineLinks, mode, hasMultipleWords, calMin, calMax, createRecipePlan,numberOfRecipesWanted, tolerance)
    else: #else, we are going to start the recipe search process
        return getRecipeFromTargetIngredients(targetIngredientList, antiList, chosenCuisineLinks, mode, hasMultipleWords, createRecipePlan)
   
def getRecipeFromTargetIngredients(targetIngredientList, antiList, chosenCuisineLinks, mode, hasMultipleWords, createRecipePlan): 
    recipeList = [] #all possible Recipes for given ingredients
    recipeIndexList = [] #stores the number of extra ingredients needed
    targetIngredientSet = set(targetIngredientList) #convert to set for efficiency
    for link in chosenCuisineLinks: #loop through the links corresponding to the cuisine key
        if "therecipedepository" in str(link): #send links to the respective webscraper file
            # pass
            getRecipesFromCuisine(targetIngredientSet, antiList, recipeList, recipeIndexList, link, mode, hasMultipleWords, createRecipePlan = createRecipePlan)
        elif "allrecipes" in str(link): 
            webScrapeFromCuisine(targetIngredientSet, antiList, recipeList,recipeIndexList, link, mode, hasMultipleWords)
    return recipeList, recipeIndexList # will return an ordered list of recipes, along with a list containing the number of extra ingredients required for each recipe.

def planRecipe(targetIngredientList, antiList, chosenCuisineLinks, mode, hasMultipleWords, calMin, calMax, createRecipePlan, numberOfRecipesWanted, tolerance): 
    recipeList = [] #all possible Recipes for given ingredients
    recipeIndexList = [] #stores the number of extra ingredients needed
    targetIngredientSet = set(targetIngredientList) #convert to set for efficiency
    for link in chosenCuisineLinks: 
        if "allrecipes" in str(link): #all recipes is the only one that stores nutritional value, for efficiency, only go through those links
            recipeList, recipeIndex = webScrapeFromCuisine(targetIngredientSet, antiList, recipeList, recipeIndexList, link, mode, hasMultipleWords, createRecipePlan = True, calorieMin = calMin, calorieMax = calMax, tolerance = tolerance)
    # after this, we have recipeList, recipeIndexList with only the 0 extra ingredients
    recipePlanSolution = []
    alreadyTried = []#holds the previously attempted recipes
    solution =  recipePlanSolver(recipePlanSolution, antiList, recipeList, calMin, calMax, alreadyTried, numberOfRecipesWanted)
    if solution == None: 
        return "No exact solutions"
    else:
        return solution

#citation, referenced Recursion lecture: https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#nQueens
def recipePlanSolver(recipePlanSolution, antiList, recipeList, calMin, calMax, alreadyTried, numberOfRecipesWanted): 
    if (len(recipePlanSolution) == numberOfRecipesWanted): #if we have found the necessary amount of recipes
        return recipePlanSolution
    else:
        # try to place the NewRecipe the next position of the list, and then recursively solve the rest of the columns
        for newRecipe in recipeList:
            if newRecipe not in recipePlanSolution and newRecipe.totalCalories!=None and newRecipe.totalCookTime !=0 and recipeIsLegal(recipePlanSolution, newRecipe, calMin, calMax) and newRecipe not in alreadyTried :
                recipePlanSolution.append(newRecipe) # place the recipe and hope it works
                solution = recipePlanSolver(recipePlanSolution, antiList, recipeList, calMin, calMax, alreadyTried, numberOfRecipesWanted)
                if (solution != None):
                    # it worked!
                    return solution
                alreadyTried.append(recipePlanSolution.pop()) # pick up the wrongly recipe
        #if no solution
        return None

def recipeIsLegal(recipePlanSolution, newRecipe, calMin, calMax): 
    total = 0
    for element in recipePlanSolution: 
        total +=element.totalCalories #the sum of all of the calories must be within the margin
    if calMin <= newRecipe.totalCalories + total and newRecipe.totalCalories + total <= calMax: 
        return True
    else: 
        return False
