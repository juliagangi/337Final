import requests 
import pandas as pd 
from bs4 import BeautifulSoup 
import spacy
import numerizer
from fractions import Fraction
import copy
from recipe_scrapers import scrape_me
nlp = spacy.load("en_core_web_sm")
  
# link for extract html data 
def getdata(url): 
    r = requests.get(url) 
    return r.text 

htmldata = getdata('https://www.foodnetwork.com/recipes/ingredient-substitution-guide') 
soup = BeautifulSoup(htmldata, 'html.parser') 
data = '' 


body = soup.find_all("p")
body = body[2:77]
keys = []
replacements = []
replacementdict = {}
for data in body:
    data = data.text
    data = data.lower()
    data = data.split(":")
    if len(data)>2:
        counter=1
        newvalue = ""
        while counter<len(data):
            newvalue+=data[counter]
            newvalue+=":"
            counter+=1
        newvalue = newvalue[:-1]
        data[1] = newvalue
    data[-1] = data[-1][1:]
    if data[0].__contains__("("):
        data[0] = data[0].split("(")
        data[0] = data[0][0][:-1]
    keys.append(data[0])
    replacements.append(data[1])
    replacementdict[data[0]] = data[1]

replacementdict["flour"] = 'flour alternatives include chickpea flour, rice flour, almond flour, and buckwheat flour'
replacementdict["cheese"] = "replace cheese with nutritional yeast or the following cheeses: Parmesan, pecorino, mozzarella, goat, brie, feta, Monterey Jack, cheddar, pepper jack, American, provolone"
replacementdict["pasta"] = "couscous, potatoes, egg noodles, zucchini noodles, spaghetti squash, eggplant"
replacementdict["rice"] = "barley, quinoa, cauliflower"
replacementdict["carrots"] = "potatoes, celery"
replacementdict["potatoes"] = "carrots, celery"
replacementdict["garlic"] = "onion"
replacementdict["onions"] = "shallots, leeks, scallions"
replacementdict["oil"] = "can be replaced with ghee, butter, or various other oils such as canola, avocado, olive, and coconut"
replacementdict["vegetarian"] = "meats may be replaced with other meats, veggie/bean patties, seitan, lentils, and tofu"


def print_ingredients():
    print("Ingredients:")
    for ingredient in ingredients:
        print(ingredient)

def print_directions():
    print("Directions:")
    counter=1
    for step in steps:
        stepcounter = "Step "
        stepcounter += str(counter)
        stepcounter+=":"
        print(stepcounter)
        print(step)
        counter+=1


def ingredient_info(ingredients):
    ingredient_dict = {}
    units = ['cup', 'cups', 'ml', 'mls', 'liters', 'L', 'ounces', 'oz', 'lb', 'lbs', 'pounds', 'pound', 'teaspoon', 'teaspoons', 'tsp', 'tablespoon', 'tablespoons', 'tbsp']    
    for ingredient in ingredients:
        split_str = ingredient.lower().split()
        quant = split_str[0]
        i = 1
        try:
            curr_quant = float(split_str[1])
            quant = split_str[0:2]
            i = 2
        except:
            if split_str[1] == 'or' or split_str[1] == 'and':
                quant = split_str[0:3]
                i = 3
            if split_str[1].__contains__('/'):
                quant = split_str[0:2]
                i = 2
        unit = ''
        while split_str[i] in units:
            if unit == '':
                unit = unit + split_str[i]
            else:
                unit = unit + ' ' + split_str[i]
            i = i + 1
        ingredient = ''
        looking_for_end = False
        prep = ''
        while i < len(split_str):
            if split_str[i] == 'of':
                i = i + 1
            elif looking_for_end:
                if nlp(split_str[i])[0].tag_ == 'VBN' or nlp(split_str[i])[0].tag_ == 'VBD':
                    word = split_str[i]
                    if nlp(word[len(word)-1])[0].pos_ == 'PUNCT':
                        word = word[0:len(word)-1]
                    if prep == '':
                        prep = word
                    else:
                        prep = prep + ' and ' + word
                    i = i + 1
                else:
                    i = i + 1
            elif split_str[i][len(split_str[i])-1] == ',':
                if ingredient == '':
                    ingredient = split_str[i][0:len(split_str[i])-1]
                else:
                    ingredient = ingredient + ' ' + split_str[i][0:len(split_str[i])-1]
                i = i + 1
                looking_for_end = True
            elif nlp(split_str[i])[0].tag_ == 'VBN' or nlp(split_str[i])[0].tag_ == 'VBD':
                if prep == '':
                    prep = split_str[i]
                else:
                    prep = prep + ' and ' + split_str[i]
                i = i + 1
            else:
                if ingredient == '':
                    ingredient = split_str[i]
                else:
                    ingredient = ingredient + ' ' + split_str[i]
                i = i + 1
        ingredient_dict[ingredient] = [quant, unit, prep]
    return ingredient_dict


def plural(ingredient):
    if len(ingredient.split()) == 0:
        if nlp(ingredient)[0].tag_ == 'NN': # singular
            return ingredient+'s'
        elif nlp(ingredient)[0].tag_ == 'NNS' or ingredient[len(ingredient)-1] == 's': # plural
            return ingredient[0:len(ingredient)-1]  
    else:      
        lastword = ingredient.split()[len(ingredient.split())-1]
        if nlp(lastword)[0].tag_ == 'NN': # singular
            return ingredient+'s'
        elif nlp(lastword)[0].tag_ == 'NNS' or lastword[len(lastword)-1] == 's': # plural
            return ingredient[0:len(ingredient)-1]
    return ingredient


def scaling_questions(factor):
    units = ['cup', 'cups', 'ml', 'mls', 'liters', 'L', 'ounces', 'oz', 'lb', 'lbs', 'pounds', 'pound', 'teaspoon', 'teaspoons', 'tsp', 'tablespoon', 'tablespoons', 'tbsp']    
    ingredient_dict = ingredient_info(ingredients)
    new_dict = copy.deepcopy(ingredient_dict)
    response = []
    for ingredient in new_dict:
        lst = ingredient_dict[ingredient]
        quantity = multiply(lst[0],factor)
        new_dict[ingredient][0] = quantity
        unit = lst[1]
        prep = lst[2]
        t1 = ' '
        t2 = ' '
        t3 = ', '
        if unit == '':
            t1 = ''
            if quantity != '1' and nlp(ingredient[len(ingredient)-1])[0].tag_ == 'NN':#ingredient[len(ingredient)-1] != 's':
                ingredient = ingredient + 's'
        else:
            if quantity != '1' and nlp(unit)[0].tag_ == 'NN':#unit[len(unit)-1] != 's':
                unit = unit + 's'
        if prep == '':
            t3 = ''
        curr_response = quantity + t1 + unit + t2 + ingredient + t3 + prep
        response.append(curr_response)
    print("Here is the updated ingredients list: ")
    for a_response in response:
        print(a_response)
    print("Here are the updated directions: ")
    i = 0
    for step in steps:
        step = step.split()
        newstep = copy.deepcopy(step) 
        for unit in units:
            if step.__contains__(unit):
                index = step.index(unit) - 1
                num = step[index]
                if nlp(unit)[0].tag_ == 'NN' or unit[len(unit)-1] != 's':
                    newstep[index+1] = unit + 's'
                try:
                    f = float(num)
                    newstep[index] = multiply(num,factor)
                except:
                    continue
        i = i + 1
        print('step ' + str(i) + ': ' + ' '.join(newstep))


def multiply(num,factor):
    print(num)
    if num.__contains__('-'):
        midindex = num.index('-')
        num1 = factor*float(num[0:midindex])
        num2 = factor*float(num[midindex+1:len(num)])
        if str(num1)[len(str(num1))-2:len(str(num1))] == '.0':
            num1 = str(num1)[0:len(str(num1))-2]
        if str(num2)[len(str(num2))-2:len(str(num2))] == '.0':
            num2 = str(num2)[0:len(str(num2))-2]
        return num1+'-'+num2
    if num.__contains__('or') or num.__contains__('and'):
        for i in range(len(num)):
            digit = num[i]
            if digit != 'or':
                try:
                    converted = int(digit)
                    mult = converted*factor
                    num[i] = str(mult)
                except:
                    try:
                        converted = float(digit)
                        mult = converted*factor
                        if str(mult)[len(str(mult))-2:len(str(mult))] == '.0':
                            num[i] = str(mult)[0:len(str(mult))-2]
                        else:
                            num[i] = str(mult)
                    except:
                        if digit.__contains__('/'):
                            middle_index = digit.index('/')
                            dividend = int(digit[0:middle_index])
                            divisor = int(digit[middle_index+1:len(digit)])
                            quotient = factor*dividend/divisor
                            if str(quotient)[len(str(quotient))-2:len(str(quotient))] == '.0':
                                num[i] = str(quotient)[0:len(str(quotient))-2]
                            else:
                                num[i] = str(quotient)                            
                        else:
                            num[i] = digit
        num1 = num[0]
        num2 = num[2]
        if str(int(num1)) == num1 and str(int(num2)) == num2:
            return str(int(num1)+int(num2))
        return ' '.join(num)
    num = num.split()
    sum = 0
    for digit in num:
        try:
            converted = int(digit)
            mult = converted*factor
            sum = sum + mult
        except:
            try:
                converted = float(digit)
                mult = converted*factor
                sum = sum + mult 
            except:
                if digit.__contains__('/'):
                    middle_index = digit.index('/')
                    dividend = int(digit[0:middle_index])
                    divisor = int(digit[middle_index+1:len(digit)])
                    sum = sum + factor*dividend/divisor 
                else:
                    if sum == 0:
                        sum = digit
                    else:
                        sum = str(sum) + digit
    if len(str(sum).split()) > 1:
        return ' '.join(str(sum))
    else:
        if len(str(sum)) > 2 and str(sum)[len(str(sum))-2:len(str(sum))] == '.0':
            return str(sum)[0:len(str(sum))-2]
        return str(sum)


def cooking_action(question,curdir):
    tagged = nlp(question)
    taggeddir = nlp(curdir)
    dirobjects = []
    verbsacting = []
    for tag in tagged:
        if tag.tag_ == "NN" or tag.tag_ == "NNS" or tag.tag_ == "NNP":
            dirobjects.append(tag)
    for tag in taggeddir:
        if tag.tag_=="VB" or tag.tag_ == "VBS" or tag.tag_ == "VBP":
            verbsacting.append(tag)
    answer = ""
    flag = False
    for theobjects in dirobjects:
        obj = str(theobjects)
        curdir = curdir.lower()
        obj = obj.lower()
        if curdir.__contains__(obj):
            flag = True
    if len(verbsacting) == 0 or flag == False or len(dirobjects) == 0:
        print("Sorry, the answer to your question is not in the current step")
        return
    elif len(verbsacting) == 1:
        theverb = str(verbsacting[0])
        answer += theverb
        answer+= " "
    else:
        counter = 0
        for verb in verbsacting:
            theverb = str(verb)
            if counter==len(verbsacting)-1:
                answer+="and"
                answer+=" "
                answer+=theverb
                answer+=" "
            else:
                answer+=theverb
                answer+=", "
            counter+=1
    if len(dirobjects)>1 or str(dirobjects[0])[-1]=="s":
        if len(dirobjects)==2:
            ingredient = ""
            for word in dirobjects:
                word = str(word)
                ingredient+=word
                ingredient+= " "
            ingredient = ingredient[:-1]
            sflag = False
            for ingr in ingredients:
                if ingredient in ingr:
                    sflag = True
            if sflag == True:
                answer+="it"
            elif flag==True:  
                answer+="them"
            else:
                answer = ""
        else:
            if flag==True:  
                answer+="them"
            else:
                answer = ""
    elif flag==True:
        answer+="it"
    else:
        answer = ""
    print(answer)
    return

print("My name is KitchenBot and I am here to help you modify the recipe you would like to make.")
print("I am equipped to handle scaling, substitutions, cuisine transformations, and dietary accomodations.")
url = input("Please enter the URL of a recipe: ")

scraper = scrape_me(url)
title = scraper.title()
ingredients = scraper.ingredients()
steps = scraper.instructions()
steps = steps.split('.')
counter = 0
while counter < len(steps):
    step = steps[counter]
    step = step.strip()
    steps[counter] = step
    counter+=1 


print("I see that you would like to make " + title[0:len(title)] + '.')
print("What would you like to change about the recipe?")

ansArr = ['Nothing','Step','Ingredient']
stepI = 0
curr_ingr = ''

while(True):

    preAns = ansArr[0]
    inpt = input("Enter text: ")

    doc = nlp(inpt)
    numDict = doc._.numerize()

    for k,v in numDict.items():
        if v.isnumeric():
            if int(v) < len(steps) and "step" in inpt.lower():
                print("step " + v + ": " + steps[int(v) - 1])
                stepI = int(v) - 1
        else:
            if int(v[0]) < len(steps) and "step" in inpt.lower():
                print("step " + v[0] + ": " + steps[int(v[0]) - 1])
                stepI = int(v[0]) - 1

    if "ingredient" in inpt.lower():
        print_ingredients()

    if "directions" in inpt.lower():
        print("These are the directions. Type 'next' or 'back' or simply type a number to navigate the steps!")
        print("step 1:", steps[0])

    if "repeat" in inpt.lower():
        print("step", str(stepI) + ":", steps[stepI])

    if "next" in inpt.lower():
        if stepI < len(steps) - 2:
            stepI += 1
            curr_ingr = ''
            print("step", str(stepI + 1) + ":", steps[stepI])
        else:
            print("There are no more steps!")

    if "back" in inpt.lower() or "prev" in inpt.lower():
        if stepI >= 1:
            stepI -= 1
            curr_ingr = ''
            print("step", str(stepI + 1) + ":", steps[stepI])
        else:
            print("There are no steps before this!")

    if inpt.lower().__contains__("double"):
        scaling_questions(2)
    
    elif inpt.lower().__contains__("triple"):
        scaling_questions(3)

    if "substitute" in inpt.lower() or "replace" in inpt.lower() or "substitution" in inpt.lower() or "replacement" in inpt.lower():
        newinpt = inpt.lower()
        newinpt = newinpt.split()
        theingredient = ""
        flag = False
        if newinpt.__contains__("cheese"):
            print(replacementdict["cheese"])
        elif newinpt.__contains__("oil"):
            print(replacementdict["oil"])
        elif newinpt.__contains__("turkey") or newinpt.__contains__("chicken") or newinpt.__contains__("beef") or newinpt.__contains__("pork"):
            print(replacementdict["vegetarian"])
        else:
            for word in newinpt:
                if flag==True:
                    theingredient+=word
                    theingredient+=" "
                if newinpt.__contains__("for"):
                    if word=="for":
                        flag = True
                else:
                    if word == "replace" or word=="substitute":
                        flag = True
            
            theingredient = theingredient[:-1]
            flag = False
            if theingredient in replacementdict:
                    print("Substitute", theingredient, "with:")
                    print(replacementdict[theingredient])
                    flag = True
            if flag==False:
                print("No replacements were found")