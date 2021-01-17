import csv
from Recipe import *
#This file contains all of the read and write functions for the CSV files. I use CSV files to store two thing: favorites, and the create-my-own recipes. 
#for the favorites, there is a toggle feature, requiring us to check the state of the recipe(if it is in the Favories CSV or not) as well. The comments 
#on this file is quite self-explanatory based on the names of the functions. 

#referenced from 112 TA Database Mini-lectures, Thank you to dataBase TA's :)

def writeMyOwnRecipe(myNewRecipe): 
    with open('myRecipes.csv', mode='a', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow([myNewRecipe.recipeName, myNewRecipe.ingredients, myNewRecipe.procedure, myNewRecipe.totalCookTime, myNewRecipe.rating, myNewRecipe.totalCalories])
        print('finished writing rows')

def readFromMyRecipes(): 
    myRecipeList = []
    with open('myRecipes.csv', mode='r') as f:
        reader = csv.reader(f)
        for recipeName, ingredients, procedure, cooktime, rating, calories in reader:
            newRecipe = Recipe(recipeName, ingredients, procedure, cooktime, rating, calories)
            myRecipeList.append(newRecipe)
    return myRecipeList

def addFavorites(favoritedRecipe): 
        with open('FavoritedRecipes.csv', mode='a', newline = '') as f:
            writer = csv.writer(f)
            if favoritedRecipe != None and checkFavorites(favoritedRecipe) == False:
                writer.writerow([favoritedRecipe.recipeName, favoritedRecipe.ingredients, favoritedRecipe.procedure, favoritedRecipe.totalCookTime, favoritedRecipe.rating, favoritedRecipe.totalCalories])
            print('finished writing rows')


def removeFavorites(FavoritedRecipe): 
    newLines = []
    with open('FavoritedRecipes.csv', 'r') as f:
        reader = csv.reader(f)
        for recipeName, ingredients, procedure, cooktime, rating, calories in reader:
            if FavoritedRecipe.recipeName != recipeName:
                print("found")
                newRecipe = Recipe(recipeName, ingredients, procedure, cooktime, rating, calories)
                newLines.append(newRecipe)
    with open('FavoritedRecipes.csv', 'w') as f:
        writer = csv.writer(f)
        for rec in newLines: 
            writer.writerow([rec.recipeName, rec.ingredients, rec.procedure, rec.totalCookTime, rec.rating, rec.totalCalories])
    print("removed")
    
def checkFavorites(rec1):
    try: 
        with open('FavoritedRecipes.csv', 'r') as f:
            reader = csv.reader(f)
            for recipeName, ingredients, procedure, cooktime, rating, calories in reader:
                if rec1.recipeName == recipeName: 
                    return True
            else: 
                return False
    except OSError: 
        addFavorites(None)
        return None

def readFromMyFavorites(): 
    try: 
        myRecipeList = []
        with open('FavoritedRecipes.csv', mode='r') as f:
            reader = csv.reader(f)
            for recipeName, ingredients, procedure, cooktime, rating, calories in reader:
                newRecipe = Recipe(recipeName, ingredients, procedure, cooktime, rating, calories)
                myRecipeList.append(newRecipe)
        return myRecipeList
    except OSError: 
        addFavorites(None)
        return None


