import requests, re, random, string
from bs4 import BeautifulSoup
from cmu_112_graphics import *
from Recipe import *
# from RecipeWebscraper import *
from SortAlgorithms import*

#This file contains the scraper for recipedepository.com. It webscrapes through the entire cuisine page, and then scrapes through the most recipe and gathers all of the necessary information. 
# It then creates a Recipe Object. After each Recipe Object is created, if it contains at least one of the ingredients in the target set, it is the destructively sorted by being based into the Filter function, which is in the 
#Sort Algorithms File. Please note that this website is also highly inconsistent in its html, requiring me to take a more 
#brute force method to parse through and clean the webscraped data. 
#citation, recipes webscraped from : https://www.therecipedepository.com/
#mode #can be "mainFilter", "byCookTime", "byRating", sif wanting to backtrack: mode = "RecipePlanner"
def getRecipesFromCuisine(targetIngredientSet, antiList, recipeList,recipeIndexList, cuisineUrl, mode, hasMultipleWords, createRecipePlan = None): 
    recipeUrls =[]
    result = requests.get(cuisineUrl)
    source = result.content
    # print(f'checking {cuisineUrl} for recipes with {targetIngredientSet}')
    soup = BeautifulSoup(source, "lxml")
    for recipe in soup.find_all("a", attrs={"href": re.compile("/recipe")}): #a-tags contain urls
        recipeUrls.append(recipe.attrs["href"])
    for link in recipeUrls: 
        # print(link)
        newUrl = "https://www.therecipedepository.com" + link
        newRecipe, recipeIndex, webscrapedIngredientsNum = getIngredientsFromRecipe(targetIngredientSet, antiList, recipeList, recipeIndexList, newUrl, mode, hasMultipleWords)
        if recipeIndex!=None: 
            if (mode == "mainFilter" and recipeIndex < webscrapedIngredientsNum) or (mode == "byCookTime" and newRecipe.totalCookTime !=0 and newRecipe.totalCookTime != None) or (mode == "byRating" and newRecipe.rating!= None): #has at least half of the ingredients
                filter(recipeIndex, newRecipe, recipeIndexList, recipeList, webscrapedIngredientsNum, mode, hasMultipleWords)
    return recipeList, recipeIndexList
def getIngredientsFromRecipe(targetIngredientSet, antiList, recipeList, recipeIndexList, url, mode,hasMultipleWords):
    #Note: Recipedepository does not have nutritional value. This attribute of looking for calories was added after recipedepository was chosen as a site to webscrape from. 
    calories = None
    recipeIndex = 0
    numInTargetList = 0
    prepTime = None
    cookTime = None
    starRating = None
    #initialize bs4 
    recipe = requests.get(url)
    src = recipe.content #get all of the html from the page
    soup = BeautifulSoup(src,"lxml") #allow BS4 to parse

    recipeName = (soup.find('h3')).get_text() #gets the text from the recipeName
    
    #lets get the raw data of ingredients
    webscrapedIngredients = soup.find_all("div", attrs = {"class": "ingredients"})
    afterParsed=[] #for some reason creates 2D list
    for element in ReplaceTagsForSearch(str(webscrapedIngredients)): 
        if element.strip() != "" and element.strip() != '[' and element.strip() != ']': 
            afterParsed.append(element)
    #calculate the number of extra ingredients required
    recipeIndex, webscrapedIngredientsNum = CalcIndex(targetIngredientSet, antiList, afterParsed, hasMultipleWords)
    recipeDetails = soup.find("ul",  attrs = {"class" : "recipe-details row"})
    details = recipeDetails.find_all("li")
    for element in details: 
        if element.find("span", attrs = {"itemprop":"prepTime"})!= None:  #get preptime
            prep = (element.find("span", attrs = {"itemprop":"prepTime"}))
            prepTime = prep.attrs["content"]
        elif element.find("span", attrs = {"itemprop":"cookTime"})!= None: #get cookTime
            cook = element.find("span", attrs = {"itemprop":"cookTime"})
            cookTime = cook.attrs["content"]
        elif element.find("span", attrs = {"class":"star-rating"})!= None:#get the Rating
            starRating = element.find("span", attrs = {"class":"star-rating"})
            starRating = calculateStarRating(starRating)
    if prepTime != None and cookTime !=None: #edge cases
        totalCookTime = calcTotalTime(prepTime, cookTime) #these are usually displayed as if a clock, so we need to standardize the format
    else: totalCookTime = None

    #get procedure
    finalProcedure = []
    procedure = soup.find("div", attrs = {"class": "directions"})
    procedure = replaceTags(str(procedure))
    newRecipe = Recipe(recipeName, afterParsed, procedure, totalCookTime, starRating, calories)
    print(recipeName, recipeIndex)
    return newRecipe, recipeIndex, webscrapedIngredientsNum

def calcTotalTime(prepTime, cookTime): 
    prep = calcIndividualTime(prepTime)
    cook = calcIndividualTime(cookTime)
    return prep + cook
def calcIndividualTime(time): 
    return int(time[0:2])*60 + int(time[3:])
def calculateStarRating(webscrapedStarRating): 
    starRating = 0
    for rating in webscrapedStarRating.find_all("span"):
        if rating.attrs["class"] == ['full-star']: 
            starRating +=1
    return starRating
def replaceTags(webscrapedString): #procedure should just be a string, such that everything is in one continuous string. 
    removebrTags = (webscrapedString.replace("<br>", ""))
    removebrTags =removebrTags.replace("<h4>Ingredients</h4>", "")
    removebrTags =removebrTags.replace('<div class="directions" itemprop="recipeInstructions">', "")
    removebrTags =removebrTags.replace("\n", "")
    removebrTags =removebrTags.replace("<h4>Directions</h4>", "")
    removebrTags =removebrTags.replace("<br/>", "")
    removebrTags =removebrTags.replace("<ol>", "")
    removebrTags =removebrTags.replace("</ul>", "")
    removebrTags =removebrTags.replace("<ul>", "")
    removebrTags =removebrTags.replace("</ol>", "")
    removebrTags = removebrTags.replace("<p>", "")
    removebrTags = removebrTags.replace("</p>", "")
    removebrTags = removebrTags.replace('<div class="ingredients">', "")
    removebrTags = removebrTags.replace('<div class="ingredients">', "")
    removebrTags = removebrTags.replace('</div>', "")
    removebrTags = removebrTags.replace('<div>', "")
    removebrTags = removebrTags.replace('<li class="ingredient" itemprop="ingredients">', "")
    removebrTags = removebrTags.replace('<li class="ingredient">', "")
    removebrTags = removebrTags.replace('class="instruction">', "")
    removebrTags = removebrTags.replace('<li', "")
    removebrTags = removebrTags.replace('</li>', "")
    return removebrTags

 #the ingredients however must be a list of strings, but can contain multiple words within each ingredient line, 
 # as a result wwe replace the major tags with a indicator, and then split it by that indicator to create the distinctions
def ReplaceTagsForSearch(webscrapedString): 
    afterParsed = [] 
    removebrTags = webscrapedString.replace("<br>", "")
    removebrTags =removebrTags.replace("<h4>Ingredients</h4>", "")
    removebrTags =removebrTags.replace('<div class="directions" itemprop="recipeInstructions">\n<h4>Directions</h4>', "")
    removebrTags =removebrTags.replace("<br/>", "!!")
    removebrTags = removebrTags.replace("<p>", "")
    removebrTags =removebrTags.replace("\n", "")
    removebrTags =removebrTags.replace("\r", "")
    removebrTags =removebrTags.replace("<ul>", "")
    removebrTags =removebrTags.replace("</ul>", "")
    removebrTags = removebrTags.replace("</p>", "!!")
    removebrTags = removebrTags.replace('<div class="ingredients">', "")
    removebrTags = removebrTags.replace('<div class="ingredients">', "")
    removebrTags = removebrTags.replace('</div>', "")
    removebrTags = removebrTags.replace('<div>', "!!")
    removebrTags = removebrTags.replace('<li class="ingredient" itemprop="ingredients">', "")
    removebrTags = removebrTags.replace('<li class="ingredient">', "")
    removebrTags = removebrTags.replace('</li>', "!!")
    if "!!" in removebrTags: 
        for element in removebrTags.split("!!"):
            afterParsed.append(element) 
    return afterParsed
