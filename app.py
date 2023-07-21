from flask import Flask, render_template, request
import requests
import json

#Filename: app.py
#Name: Sanay Vastani
#Category: Internet Applications
#Application Name: foodAware
#Description: foodAware is a Python program built using the Flask framework for detecting allergens
#in packaged food items. Users enter UPC code on the index.html page and results are shown in the results.html page.
#Application uses HTML/CSS for rendering responsive pages and USDA Food API for food ingredients details.

#Create a Flask application to process web requeest
app = Flask(__name__)

#Router for the default function to handle the main landing page and render index.html page
@app.route("/")
def index():
    return render_template("index.html")

#Router to launch the Contacts.html page when someone clicks on the Contact Link
@app.route("/contact")
def contact():
    return render_template("Contact.html")


#Router to launch the results page after the "Submit" button is clicked on landing page (index.html)
@app.route('/results', methods=['POST'])
def results():
#Process only POST requests. POST method is more secure when submitting data from a form
#Parse all input values from the form into variables to run the allergy check
     if request.method == 'POST':
        upc = request.form.get('productUPC')
        almond = request.form.get('almond')
        walnut = request.form.get('walnut')
        pecan = request.form.get('pecan')
        milk = request.form.get('milk')
        peanut = request.form.get('peanut')
#Make an array of allergens for iterating through
        allergenList = [almond, walnut, pecan, peanut, milk]
#Construct the USDA URL to invoke the REST API for Food details. The URL contains the secure API key.
        USDA_URL = "https://api.nal.usda.gov/fdc/v1/foods/search?query=" +upc+ "&dataType=Branded&sortBy=fdcId&sortOrder=asc&api_key=CGbjqQl1DAGNhfTOsSTzrGs8z3LxkyJEa45A9Aji"
        print (USDA_URL)
        response = requests.get(USDA_URL)
#Check if the call was succesful. 200 means success.
        if response.status_code != 200:
                message = "The USDA URL {} is not responding. Please try again".format(USDA_URL)
                return render_template("results.html", msg=message)
#Retrieve the response from the API call as a JSON object.
        json_object = response.json()
#Check if there was no data returned. Usually for invalid UPC codes.
        if json_object['totalHits'] == 0:
            message = "The UPC code you entered was not found in the USDA database, Please check the code and try again."
            return render_template("results.html", msg=message)

# For loop for retrieving the key-value pair of the response JSON object
# Use  print(json_object['foods'][0]) to print the JSON object to console
        for i in json_object['foods']:
            fdcId = i['fdcId']
            description = i['description']
            gtinUpc = i['gtinUpc']
            ingredients = i['ingredients']
            brandOwner = i['brandOwner']
            brandName = i['brandName']
#Define array to caoture the matches of allergens in the ingredients list
        allergensInFood = []
#Call the allergen checking function. Returns an array of allergens found in the ingredients list.
        allergensInFood = checkAllergens(allergenList, ingredients)
        if len(allergensInFood) > 0:
            message = "CAUTION: Food item contains: "
            for i in range(len(allergensInFood)):
                message = message + " " + allergensInFood[i] +","
#Remove the last comma from the string to make it look grammatically correct.
            message = message[:-1]
            return render_template("results.html", msg=message, desc=description, brandNm=brandName, ing=ingredients )
        else:
            message = "The food is free of allergens."
            return render_template("results.html", msg=message, desc=description, brandNm=brandName, ing=ingredients)


#Funtion that does the checking of allergens from a list of ingredients that are passed into it.
def checkAllergens(allergenList, ingredients):
    allergenFound =[]
#For each allergen selected by the user, check if it exists in the ingredients list.
    for i in range(len(allergenList)):
        if (type(allergenList[i]) == str):    #Type checking to a string
            if (ingredients.find(allergenList[i]) != -1):
                allergenFound.append(allergenList[i])
#Found the allergen so append to the array storing found allergens
    return allergenFound


