from django.shortcuts import render, redirect, reverse
from .models import ImageUpload
from .forms import ImgForm
from google.cloud import vision 
import requests
import json
import io
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "serviceAccountToken.json"

#esg API
def sustainability(name):
    
    url = f'https://esgapiservice.com/api/authorization/search?q={name}&token=66b0034b9254f3338c356fc3461bc661'.format(name=name)
    response = requests.get(url)
    data = response.json()
    rating = data[0]["total_grade"]
    print(rating)
    return rating
    
#Fruity API
def scrape_all_fruits(fruit):

    url = f'https://fruityvice.com/api/fruit/{fruit}'.format(fruit=fruit)
    response = requests.get(url)
    data = response.json()
    name1 = data["name"]
    nutrition1 = data["nutritions"]
    print(name1, "\n" ,nutrition1)

    return nutrition1

#CLOUD VISION API
def label_detector(path):
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.logo_detection(image = image)
    logos = response.logo_annotations
   # print("Logos: ", logos)
    for logo in logos:
        print(logo.description)
        return logo.description

    if response.error.message:
        raise Exception(
            '{}\nerror'.format(response.error.message)
        )
    
def localize_objects(path):
    client = vision.ImageAnnotatorClient()
    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))

    for object_ in objects:
            print('\n{} (confidence: {})'.format(object_.name, object_.score))
            name = object_.name
            #score = object_.score 
            numberOfObjects = len(objects)
            #print('Normalized bounding polygon vertices: ')
            # for vertex in object_.bounding_poly.normalized_vertices:
                # print(' - ({}, {})'.format(vertex.x, vertex.y))
            #n = name
            return name, numberOfObjects

#name1 = localize_objects(path = "./dyno/static/banana.jpg")
name1 = 1

def index(request):
    a = 10

    imgForm = ImgForm()

    #if theres a post request in this case the button from the form
    if request.method == "POST":
        #save the image from the post request to the image model in the db
        try:
            imgForm = ImgForm(request.POST, request.FILES)
            if imgForm.is_valid():
                imgForm.save()

                return redirect(reverse('info'))
        except:
            print("error")

    return render(request, 'index.html', {
        "a": a,
        "imgform": imgForm,
    })

def info(request):

    if request.method == "POST":
        return redirect(reverse(index))

    #get the path of the latest image uploaded by id
    imgPath = str(ImageUpload.objects.latest('id').image)
    newPath = "/Users/marcodeanda/Desktop/dynoproject/dynoproj/images/" + imgPath
    #run the AI function with this path
    imgData = localize_objects(path = newPath)
    try:
        objName = imgData[0]
        objCount = imgData[1]

    except:
        objName = "Object Not Recognized"
        objCount = "NA"

    imgLabel = label_detector(path=newPath)
    try:
        objLabel = imgLabel
    except:
        objLabel = "NA"

    try:
        rating = sustainability(objLabel)
    except:
        rating = "NA"
        

    try:
        fruitInfo = scrape_all_fruits(objName)
        calorieNum = fruitInfo["calories"]
        carbNum = fruitInfo["carbohydrates"]
        sugarNum = fruitInfo["sugar"]
        proteinNum = fruitInfo["protein"]
    except:
        fruitInfo = "NA"
        calorieNum = "NA"
        carbNum = "NA"
        sugarNum = "NA"
        proteinNum = "NA"

    return render(request, 'info.html', {
        "name": objName,
        #use this to show image
        "path": imgPath,
        "count": objCount,
        "calories": calorieNum,
        "carbs": carbNum,
        "sugar": sugarNum,
        "protein": proteinNum,
        "label": objLabel,
        "rating": rating,
    })