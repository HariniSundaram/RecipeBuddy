import requests, re, random, string
from bs4 import BeautifulSoup
from cmu_112_graphics import *
from Recipe import *
from SortAlgorithms import*
#This file contains the scraper from Allrecipes.com. It webscrapes through the entire cuisine page, possibly recursively calls itself if there is a "load more" button 
#and opens every recipe. From here it scrapes through the inner most recipe and gathers all of the necessary information. It then creates a Recipe Object. 
# After each Recipe Object is created, if it contains at least one of the ingredients in the target set, it is the destructively sorted by being based into the Filter function, which is in the 
#Sort Algorithms File. 
#citation of recipe source: https://www.allrecipes.com/

#Starting fromt the outermost category link
#code citation, referenced documentation of BeautifulSoup
def webScrapeFromCuisine(targetIngredientSet, antiList, recipeList,recipeIndexList, cuisineUrl, mode, hasMultipleWords, createRecipePlan = False, calorieMin = None, calorieMax = None, recursivePageCounter = 1, tolerance = 0):
    recipeUrlsSet = set()
    result = requests.get(cuisineUrl)
    source = result.content
    soup = BeautifulSoup(source, "lxml")
    block1 = soup.find_all("div", attrs = {"class": "component category-page-list karma-content-container category-page-body"}) #In All recipes, there are usually 3 blocks of content which contain recipes
    block2 = soup.find("div", attrs = {"class": "component category-page-videos category-page-body"})
    block3 = soup.find("div", attrs = {"class": "category-page-list-related component category-page-list karma-content-container category-page-body"})
    for element in block1: 
        for recipe in element.find_all("a", attrs={"href": re.compile("https://www.allrecipes.com/recipe/")}): #only get recipes which have this tag in it, they are the ones which are usable recipes
            if "www.twitter.com" not in str(recipe) and "www.pinterest.com" not in str(recipe) and "www.facebook.com" not in str(recipe) and "mailto:" not in str(recipe) and "sms://" not in str(recipe): 
                recipeUrlsSet.add(recipe.attrs["href"])
    if block2!=None: # we need to case for this, as there is some inconsistency across the recipes
        for recipe in block2.find_all("a", attrs={"href": re.compile("https://www.allrecipes.com/recipe/")}): 
            if "www.twitter.com" not in str(recipe) and "www.pinterest.com" not in str(recipe) and "www.facebook.com" not in str(recipe) and "mailto:" not in str(recipe) and "sms://" not in str(recipe): 
                recipeUrlsSet.add(recipe.attrs["href"])
    if block3!=None: 
        for recipe in block3.find_all("a", attrs={"href": re.compile("https://www.allrecipes.com/recipe/")}):
            if "www.twitter.com" not in str(recipe) and "www.pinterest.com" not in str(recipe) and "www.facebook.com" not in str(recipe) and "mailto:" not in str(recipe) and "sms://" not in str(recipe): 
                recipeUrlsSet.add(recipe.attrs["href"])
    
    #check if there is a "Load More Button", allRecipes creates seperate links for new pages, allowing me to webscrape it
    loadPresent = soup.find("a", attrs = {"id": "category-page-list-related-load-more-button"})
    nextPresent = soup.find("a", attrs = {"class": "category-page-list-related-nav-next-button"})
    #if there is, recursively call webscrapeFromCuisine. Base case is when you reach either no more load more pages or the 5th page
    # print(f"pageCounter is {recursivePageCounter}")
    if recursivePageCounter != 10: #for now, stop at the 10th page, base case
        if loadPresent != None: 
            webScrapeFromCuisine(targetIngredientSet, antiList, recipeList ,recipeIndexList, loadPresent.attrs["href"], mode, hasMultipleWords, createRecipePlan = createRecipePlan, calorieMin = calorieMin, calorieMax = calorieMax, recursivePageCounter = recursivePageCounter + 1) 
        elif nextPresent!= None: 
            webScrapeFromCuisine(targetIngredientSet, antiList, recipeList ,recipeIndexList, nextPresent.attrs["href"], mode, hasMultipleWords, createRecipePlan = createRecipePlan, calorieMin = calorieMin, calorieMax = calorieMax, recursivePageCounter = recursivePageCounter + 1)
    #if we are calling this from the backtracking algorithm, then we want to return recipes that require 0 extra ingredients, or a recipe Index of 0
    if createRecipePlan == True: 
        for link in recipeUrlsSet: 
            newRecipe, recipeIndex, webscrapedIngredientsNum = webScrapeFromRecipe(targetIngredientSet, antiList, recipeList, recipeIndexList, link, mode, hasMultipleWords)
            if recipeIndex!= None and recipeIndex <= tolerance: 
                filter(recipeIndex, newRecipe, recipeIndexList, recipeList, webscrapedIngredientsNum, mode, hasMultipleWords)
                # recipeList.append(newRecipe)#for the backtracking algorithm, because all of the recipes have 0 extra ingredients, it doesnt need to be in a sorted order
                # recipeIndexList.append(recipeIndex)
        return recipeList, recipeIndexList
    else: # if we are going through the standard recipe search, then we need to sort the recipe each time a new recipe is searched through
        for link in recipeUrlsSet: 
            newRecipe, recipeIndex, webscrapedIngredientsNum = webScrapeFromRecipe(targetIngredientSet, antiList, recipeList, recipeIndexList, link, mode,hasMultipleWords)
            if recipeIndex!= None and ((mode == "mainFilter" and recipeIndex < webscrapedIngredientsNum) or (mode == "byCookTime" and newRecipe.totalCookTime !=0 and newRecipe.totalCookTime != None) or (mode == "byRating" and newRecipe.rating!= None)): #has at least half of the ingredients
                #check if there is atleast 1 ingredient from the scraped website in the User's ingredient List
                filter(recipeIndex, newRecipe, recipeIndexList, recipeList, webscrapedIngredientsNum, mode, hasMultipleWords)
        return recipeList, recipeIndexList
def webScrapeFromRecipe(targetIngredientSet, antiList, recipeList, recipeIndexList, url, mode, hasMultipleWords):
    ingredientList = []
    cookTime = None
    numInTargetList = 0
    recipe = requests.get(url)
    src = recipe.content #get all of the html from the page
    soup = BeautifulSoup(src,"lxml") #allow BS4 to parse
    recipeName = (soup.find('h1')).get_text() #gets the text from the recipeName
    #find ingredients: 
    ingr = soup.find('ul', attrs = {"class": "ingredients-section"})
    ingr = ingr.find_all("span", attrs = {"class" : "ingredients-item-name"})
    for item in ingr: 
        ingredientList.append(((item.get_text()).strip()).replace("\n", "").replace("\u2009", " "))
    #find cooktime: 
    time = soup.find("div", attrs = {"class": "two-subcol-content-wrapper"})
    time = time.find_all("div", attrs = {"class": "recipe-meta-item"})
    for item in time: 
        something = item.find("div", attrs = {"class": "recipe-meta-item-header"})
        if something.get_text().strip() =="total:":
            cookTime = item.find("div", attrs = {"class": "recipe-meta-item-body"}).get_text().strip()
            cookTime = stripCookTime(cookTime)
    #find starRating: 
    rate = soup.find("div", attrs = {"class" : "component recipe-ratings"})
    rate = rate.find("a")
    rate = rate.find("span", attrs={"class" : "review-star-text"}).get_text().strip()
    starRating = rate.replace(" stars", "")
    if "Unrated" not in starRating: #Edge case
        starRating = float(starRating.replace("Rating: ", ""))
    #find procedure
    temp = []
    proc = soup.find("ul", attrs = {"class":"instructions-section"})
    for element in proc.get_text().split(): 
       temp.append(element)
    temp2 = " ".join(temp)
    procedure = stripProcedure(temp2)
    #find calories
    nutrition = soup.find("section", attrs = {"class":"nutrition-section container"}) #there are multiple "section body tags"
    if nutrition != None:#edge case
        nutrition = nutrition.find("div", attrs = {"class":"section-body"}).get_text()
        calories = int(nutrition.split()[0])
    else:
        calories = None 
    #create Recipe object
    newRecipe = Recipe(recipeName, ingredientList, procedure, cookTime, starRating, calories)
    #calculate the number of extra ingredients required
    recipeIndex, webscrapedIngredientsNum = CalcIndex(targetIngredientSet, antiList,  ingredientList, hasMultipleWords) 
    return newRecipe, recipeIndex, webscrapedIngredientsNum
def stripProcedure(WebscrapedProcedure): #necessary to get rid of unwanted tags that are someimes added into the html
    newString = WebscrapedProcedure.replace("\n", "") 
    newString = WebscrapedProcedure.replace("Advertisement", "")
    return newString
def stripCookTime(cookTime): # in cases such as hours instead of minutes, etc
    minuteTotal = 0
    words = cookTime.split()
    for index in range(len(words)):
        if words[index] == "hrs": 
            minuteTotal += int(words[index-1])*60
        elif words[index] == "mins": 
            minuteTotal += int(words[index-1])
    return minuteTotal
