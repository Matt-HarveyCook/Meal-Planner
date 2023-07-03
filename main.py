import mysql.connector
from mysql.connector import Error

from todoist_api_python.api import TodoistAPI
import mysql.connector

import numpy as np

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rocket08",
        database="recipes"
    )

def getRanking (item, list):
    for i, x in enumerate(list):
        if item == x[0]:
            #print(i, x.index(1))
            print("this is the position of it "+str(i))
            return i
            break


def convertIdToIngredient (ingredientID):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT ingredientsName from ingredients where ingredientsID = '" + str(ingredientID) +"'")

    myresult = mycursor.fetchall()

    for x in myresult:
        return x[0]

def convertIdToMeal (mealNameID):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT mealName from mealName where mealNameID = '" + str(mealNameID) +"'")

    myresult = mycursor.fetchall()

    for x in myresult:
        return x[0]

def getIngredientPrice (ingredientID):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT ingredientPrice from ingredients where ingredientsID = '" + str(ingredientID) +"'")

    myresult = mycursor.fetchall()

    for x in myresult:
        return x[0]

# checks whether the recipe can be made from the list of things already in the fridge
def recipeCheck(recipe, fridge):
    missingIngredients = 0
    priceForIngredients = 0.0
    neededIngredients =[]
    for x in range(len(recipe)):
        #print("this is fridge x 1: ")
        #print(str(len(recipe)))
        #print(fridge[x][1])
        if any(recipe[x][0] in sublist for sublist in fridge) :
            nmull = 9
            #print("you got " + str(convertIdToIngredient(recipe[x][0])))
            #print("it cost this much "+ str(getIngredientPrice(recipe[x][0])))
            #print("this is missing ingredients "+str(missingIngredients))
        else:
            #print("you dont got " + str(convertIdToIngredient(recipe[x][0])))
            #print("it cost this much "+ str(getIngredientPrice(recipe[x][0])))
            neededIngredients.append(int(recipe[x][0]))
            print("this is adding to needed "+ str(recipe[x][0]))
            missingIngredients=missingIngredients+1
            priceForIngredients = priceForIngredients+getIngredientPrice(recipe[x][0])
            print("add this price "+ str(getIngredientPrice(recipe[x][0])))
            #print("this is missing ingredients " + str(missingIngredients))

    if missingIngredients == 0:
        #print("you can make this meal")
        #missingIngredients = 0
        return [True, 0, 0.0, []]
    else:
        #print("you cannot make this meal")
        temp = missingIngredients
        #missingIngredients = 0
        return [False, missingIngredients, round(priceForIngredients, 2), neededIngredients]


# used to upload a task to the project folder by running program
def uploadTaskToInbox(task, description):  # this is the unique key for the user which is found in the settings
    api = TodoistAPI('e10620749702d653d0063fe5ac1c3379cc93cfa2')

    try:
        # assigns a projects variable to retreive the projects
        projects = api.get_projects()
        print(projects)

        shoppingID=0
        for i, x in enumerate(projects):
            if "Shopping List" == x.name:
                # print(i, x.index(1))
                shoppingID= x.id

        task = api.add_task(content=task, description=description, project_id=shoppingID)
        print(task)

    except Exception as error:
        print(error)


def convertIngredientToID (ingredient):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT ingredientsID from ingredients where ingredientsName = '" + ingredient +"'")

    myresult = mycursor.fetchall()

    for x in myresult:
        return x[0]


if __name__ == '__main__':
    fridge = [["Garlic", 8], ["Onion", 3], ["Bacon", 4], ["Soy Sauce", 100] , ["Lamb Mince", 100]]
    for x in fridge:
        x[0] = convertIngredientToID(x[0])

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM recipes.meal")

    myresult = mycursor.fetchall()


    ingredientList = []

    for x in myresult:
        ingredientList.append(x)

    ingredientListInt = []
    for x in range(len(ingredientList)):
        ingredientListInt.append(list(map(int, ingredientList[x])))

    print(ingredientListInt)
    pos = 1
    temp = []
    scoreList = []
    for k in range(len(ingredientListInt)):
        if ingredientListInt[k][0] == pos:
            temp.append([ingredientListInt[k][1],ingredientListInt[k][2]])
        else:
            print("jawn")
            print("this is temp" +str(temp))
            scoreList.append([pos, recipeCheck(temp, fridge)[0], recipeCheck(temp, fridge)[1], recipeCheck(temp, fridge)[2], recipeCheck(temp, fridge)[3] ])
            pos=pos+1
            temp.clear()
            temp.append([ingredientListInt[k][1], ingredientListInt[k][2]])
    #temp.append([ingredientListInt[k][1],ingredientListInt[k][2]])
    print("this is temp" + str(temp))


    scoreList.append([pos, recipeCheck(temp, fridge)[0], recipeCheck(temp, fridge)[1], recipeCheck(temp, fridge)[2], recipeCheck(temp, fridge)[3] ])
    print("this is the score list "+str(scoreList))
    numOfIngList = sorted(scoreList, key=lambda x: x[2], reverse=False)
    priceOfIngList = sorted(scoreList, key=lambda x: x[3], reverse=False)
    print("this is the list in order of the number of ingredeitns required "+str(numOfIngList))
    print("this is the list in order of the price of ingredeitns required " + str(priceOfIngList))




    #print("this is position based on missing ingredients "+str(getRanking(2, numOfIngList)))
    #print("this is position based on the price " + str(getRanking(2, priceOfIngList)))
    print("this recipe requires the fewest ingredients: " + str(convertIdToMeal(numOfIngList[0][0])))
    print("this recipe requires the cheapest ingredients: " + str(convertIdToMeal(priceOfIngList[0][0])))

    #print(recipeCheck())

    overallRanking = []
    for x in range(len(numOfIngList)):
        print(str(x+1))
        meanPos = getRanking(x+1, numOfIngList) + getRanking(x+1, priceOfIngList)
        print("this is the mean pos "+ str(meanPos/2))
        overallRanking.append([x+1, meanPos/2, numOfIngList[getRanking(x+1, numOfIngList)][4]])
        overallRanking = sorted(overallRanking, key=lambda x: x[1], reverse=False)
        print("this is overall ranking "+ str(overallRanking))

    print("to make "+ str(convertIdToMeal(overallRanking[0][0])) + " you need to buy: " )
    for x in range(len(overallRanking[0][2])):
        print(str(convertIdToIngredient(overallRanking[0][2][x])))
        uploadTaskToInbox( str(convertIdToIngredient(overallRanking[0][2][x])) , str(convertIdToMeal(overallRanking[0][0])))

