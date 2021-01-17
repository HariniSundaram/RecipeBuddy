#This file contains everything relating to the sortiing algorithms. The "Recipe Index" is the number of extra ingredients that are 
#not in the User's ingredient list. 

def CalcIndex(targetIngredientSet, antiList, ingredientList, hasMultipleWords): 
    antiSet = set(antiList) #for efficiency, convert into set
    recipeIndex = 0
    numInTargetList = 0 # the number of target ingredients the webscraped recipe contains
    webscrapedIngredientsNum = len(ingredientList) # the number of ingredients in the webscraped list
    if hasMultipleWords == True: # if there are multiple words, we will compare also the combination of every pair of words against the target set
        for ingredientLine in ingredientList:
            ingrLine = ingredientLine.split()
            #we will first check the last ingredient of every ingredient(to ensure every element of the webscraped ingredient list is checked)
            if ingrLine[-1].replace(",", "") in antiSet: #if there is something that is in the anti-list, return None, as we don't want to display it
                recipeIndex = None
                webscrapedIngredientsNum = None
                return recipeIndex, webscrapedIngredientsNum 
            elif ingrLine[-1].replace(",", "") in targetIngredientSet: #if the last word is in the target set
                numInTargetList += 1
            for ingr in range(len(ingrLine)-1): 
                jointWord = str (ingrLine[ingr].lower())+ " " + str(ingrLine[ingr+1].lower())
                singWord = ingrLine[ingr] 
                singWord = singWord.replace(",", "")#edge cases
                jointWord = jointWord.replace(",", "")#edge cases
                if singWord in antiSet or jointWord in antiSet: #if there is something that is in the anti-list, return None
                    recipeIndex = None
                    webscrapedIngredientsNum = None
                    return recipeIndex, webscrapedIngredientsNum 
                if singWord in targetIngredientSet and (jointWord not in targetIngredientSet): #if the single word is in the targetSet
                    numInTargetList +=1
                if jointWord in targetIngredientSet: 
                    numInTargetList +=1
    else: #if there are no 2-worded ingredients, then we will do a similar process, except with each individual word
        for ingredientLine in ingredientList:
            for ingr in ingredientLine.split(): 
                if "," in ingr: 
                    ingr = ingr.replace(",", "")
                if ingr in antiSet: 
                    recipeIndex = None
                    webscrapedIngredientsNum = None
                    return recipeIndex, webscrapedIngredientsNum
                elif ingr in targetIngredientSet: 
                    numInTargetList +=1
    recipeIndex = webscrapedIngredientsNum - numInTargetList #the number of extra ingredients, 
    #is the total number of ingredients the recipe has minus the number of ingredients that are in the user's ingredient list
    
    if recipeIndex < 0: recipeIndex = 0 #if anything is double counted, then we know everything was atleast counted for once, hence it is just 0.
    return recipeIndex, webscrapedIngredientsNum
def filter(recipeIndex, newRecipe, recipeIndexList, recipeList, webscrapedIngredientsNum, mode, hasMultipleWords): #sends the recipe to the respective solting algorithm
    if mode == "mainFilter": #least to greatest index
        sortByRecipeIndexOrCookTime(recipeIndex, newRecipe, recipeIndexList, recipeList, webscrapedIngredientsNum)
    elif mode == "byCookTime": #least to greatest
        sortByRecipeIndexOrCookTime(newRecipe.totalCookTime, newRecipe, recipeIndexList, recipeList, webscrapedIngredientsNum)
    elif mode == "byRating": #greatest to least
        sortByRating(newRecipe.rating, newRecipe, recipeIndexList, recipeList, webscrapedIngredientsNum)

def sortByRating(starRating, newRecipe, recipeIndexList, recipeList, webscrapedIngredientsNum): 
    hasBeenAppended = False
    if newRecipe.recipeName == "VEGGIE PASTA IN ROUX RECIPE" or not isinstance(starRating, float): #edge case, poor html
        return
    elif starRating == 0: #if 0 star rating, add to the end
        recipeList.append(newRecipe)
        recipeIndexList.append(starRating)
    elif recipeList == []: # if empty list, just add it the recipe
        recipeList.append(newRecipe)
        recipeIndexList.append(starRating)
    else: 
        for spot in range(len(recipeIndexList)): #find the first index where the the rating is lower than the current rating
            if recipeIndexList[spot] <= starRating: #insert at that spot
                recipeList.insert(spot, newRecipe)
                recipeIndexList.insert(spot, starRating)
                hasBeenAppended = True
                break
            if hasBeenAppended == False: #if it hasnt been appended, then it must be the smallest, but not equal to 0
                recipeList.append(newRecipe)#add to the end
                recipeIndexList.append(starRating)
            
def sortByRecipeIndexOrCookTime(recipeIndex, newRecipe, recipeIndexList, recipeList, webscrapedIngredientsNum): 
    hasBeenAppended = False
    if recipeIndex == None: #edge case
        return
    elif recipeIndex == 0: #if 0 star rating, add to the beginning
        recipeList.insert(0,newRecipe)
        recipeIndexList.insert(0,recipeIndex)
    elif recipeList == []: 
        recipeList.append(newRecipe)# if empty list, just add it the recipe
        recipeIndexList.append(recipeIndex)
    else: 
        for spot in range(len(recipeIndexList)): 
            if recipeIndexList[spot] > recipeIndex: #find the first index where the the index is greater than the current rating
                recipeList.insert(spot, newRecipe) #insert at that spot
                recipeIndexList.insert(spot, recipeIndex)
                hasBeenAppended = True
                break
        if hasBeenAppended == False:# if not appened, it must be the largest, append to the end
            recipeList.append(newRecipe)
            recipeIndexList.append(recipeIndex)
