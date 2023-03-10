import requests 
import pandas as pd 
from bs4 import BeautifulSoup 
import spacy
import numerizer
from fractions import Fraction
import copy
from recipe_scrapers import scrape_me
from collections import defaultdict 
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

def contains_meat():
    meat = []
    for ingredient in ingredients:
        ingredient = ingredient.lower()
        if ingredient.__contains__("pork"):
            meat.append("pork")
        if ingredient.__contains__("sausage"):
            meat.append("sausage")
        if ingredient.__contains__("chicken"):
            meat.append("chicken")
        if ingredient.__contains__("turkey"):
            meat.append("turkey")
        if ingredient.__contains__("ground beef"):
            meat.append("ground beef")
        elif ingredient.__contains__("beef"):
            meat.append("beef")
        if ingredient.__contains__("steak"):
            meat.append("steak")
        if ingredient.__contains__("lamb"):
            meat.append("lamb")
        if ingredient.__contains__("veal"):
            meat.append("veal")
        if ingredient.__contains__("bacon"):
            meat.append("bacon")
        if ingredient.__contains__("duck"):
            meat.append("duck")
        if ingredient.__contains__("chuck"):
            meat.append("chuck")
        if ingredient.__contains__("liver"):
            meat.append("liver")
    return meat

def contains_vegoptions():
    veggies = []
    for ingredient in ingredients:
        ingredient = ingredient.lower()
        if ingredient.__contains__("tofu"):
            veggies.append("tofu")
        if ingredient.__contains__("beans"):
            veggies.append("beans")
        if ingredient.__contains__("lentils"):
            veggies.append("lentils")
        if ingredient.__contains__("patty"):
            veggies.append("veggie patty")
        if ingredient.__contains__("chickpeas"):
            veggies.append("chickpeas")
        if ingredient.__contains__("eggplant"):
            veggies.append("eggplant")
    return veggies

un_to_healthy = {}
un_to_healthy["sugar"] = ["agave", "honey", "applesauce", "stevia"]
un_to_healthy["butter"] = ["low-fat butter", "ghee"]
un_to_healthy["olive oil"] = ["low-fat butter", "applesauce", "ghee"]
un_to_healthy["vegetable oil"] = ["low-fat butter", "applesauce", "ghee"]
un_to_healthy["canola oil"] = ["low-fat butter", "applesauce", "ghee"]
un_to_healthy["coconut oil"] = ["low-fat butter", "applesauce", "ghee"]
un_to_healthy["peanut oil"] = ["low-fat butter", "applesauce", "ghee"]
un_to_healthy["sesame oil"] = ["low-fat butter", "applesauce", "ghee"]
un_to_healthy["avocado oil"] = ["low-fat butter", "applesauce", "ghee"]
un_to_healthy["bacon"] = ["turkey bacon", "veggie bacon"]
un_to_healthy["pasta"] = ["whole-wheat pasta", "zucchini noodles"]
un_to_healthy["spaghetti"] = ["whole-wheat spaghetti", "zucchini noodles"]
un_to_healthy["rice"] = ["brown rice", "riced vegetables"]
un_to_healthy["ground beef"] = ["ground turkey"]
un_to_healthy["beef"] = ["chicken", "turkey", "beans", "chickpeas", "lentils", "salmon", "fish"]
un_to_healthy["steak"] = ["chicken", "turkey", "beans","chickpeas", "lentils", "fish", "salmon"]
un_to_healthy["burger"] = ["turkey burger", "veggie burger", "bean burger"]
healthyoptions = []
for index in un_to_healthy:
    thelist = un_to_healthy[index]
    for word in thelist:
        if word not in healthyoptions:
            healthyoptions.append(word)

healthy_to_un = {}
healthy_to_un["agave"] = ["sugar"]
healthy_to_un["honey"] = ["sugar"]
healthy_to_un["applesauce"] = ["sugar"]
healthy_to_un["stevia"] = ["sugar"]
healthy_to_un["low-fat butter"] = ["butter", "olive oil", "vegetable oil", "canola oil", "coconut oil", "peanut oil", "sesame oil", "avocado oil"]
healthy_to_un["applesauce"] = ["butter", "olive oil", "vegetable oil", "canola oil", "coconut oil", "peanut oil", "sesame oil", "avocado oil"]
healthy_to_un["ghee"] = ["butter", "olive oil", "vegetable oil", "canola oil", "coconut oil", "peanut oil", "sesame oil", "avocado oil"]
healthy_to_un["turkey bacon"] = ["bacon"]
healthy_to_un["veggie bacon"] = ["bacon"]
healthy_to_un["whole-wheat pasta"] = ["pasta"]
healthy_to_un["whole-wheat spaghetti"] = ["spagetti"]
healthy_to_un["zucchini noodles"] = ["pasta"]
healthy_to_un["brown rice"] = ["rice"]
healthy_to_un["ground turkey"] = ["ground beef"]
healthy_to_un["chicken"] = ["beef", "steak"]
healthy_to_un["turkey"] = ["beef", "steak"]
healthy_to_un["beans"] = ["beef", "steak"]
healthy_to_un["chickpeas"] = ["beef", "steak"]
healthy_to_un["lentils"] = ["beef", "steak"]
healthy_to_un["salmon"] = ["beef", "steak"]
healthy_to_un["turkey burger"] = ["burger"]
healthy_to_un["veggie burger"] = ["burger"]
healthy_to_un["bean burger"] = ["burger"]

def healthy():
    unhealthy_items = []
    for ingredient in ingredients:
        ingredient = ingredient.lower()
        if ingredient.__contains__("sugar") and "sugar" not in unhealthy_items:
            unhealthy_items.append("sugar")
        if ingredient.__contains__("butter") and "butter" not in unhealthy_items:
            unhealthy_items.append("butter")
        if ingredient.__contains__("olive oil") and "olive oil" not in unhealthy_items:
            unhealthy_items.append("olive oil")
        if ingredient.__contains__("canola oil") and "canola oil" not in unhealthy_items:
            unhealthy_items.append("canola oil")
        if ingredient.__contains__("coconut oil") and "coconut oil" not in unhealthy_items:
            unhealthy_items.append("coconut oil")
        if ingredient.__contains__("avocado oil") and "avocado oil" not in unhealthy_items:
            unhealthy_items.append("avocado oil")
        if ingredient.__contains__("vegetable oil") and "vegetable oil" not in unhealthy_items:
            unhealthy_items.append("vegetable oil")
        if ingredient.__contains__("peanut oil") and "peanut oil" not in unhealthy_items:
            unhealthy_items.append("peanut oil")
        if ingredient.__contains__("sesame oil") and "sesame oil" not in unhealthy_items:
            unhealthy_items.append("sesame oil")
        if ingredient.__contains__("bacon") and "bacon" not in unhealthy_items:
            unhealthy_items.append("bacon")
        if ingredient.__contains__("pasta") and "pasta" not in unhealthy_items:
            unhealthy_items.append("pasta")
        if ingredient.__contains__("spaghetti") and "spaghetti" not in unhealthy_items:
            unhealthy_items.append("spaghetti")
        if ingredient.__contains__("rice") and "rice" not in unhealthy_items:
            unhealthy_items.append("rice")
        if ingredient.__contains__("ground beef") and "ground beef" not in unhealthy_items:
            unhealthy_items.append("ground beef")
        elif ingredient.__contains__("beef") and "beef" not in unhealthy_items:
            unhealthy_items.append("beef")
        if ingredient.__contains__("burger") and "burger" not in unhealthy_items:
            unhealthy_items.append("burger")
        if ingredient.__contains__("steak") and "steak" not in unhealthy_items:
            unhealthy_items.append("steak")
    return unhealthy_items

def unhealthy():
    healthy_items = []
    for food in healthyoptions:
        for ingredient in ingredients:
            if ingredient.__contains__(food):
                healthy_items.append(food)
    return healthy_items



        
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
def direction_methods(steps):
    method_dict = defaultdict(list)

    for i in range(len(steps)):
        step = steps[i]
        wordArr = step.lower().split()
        for word in wordArr:
            #print( nlp(word)[0].tag_)
            if nlp(word)[0].tag_ == 'VB' and word !='sauce' and word != 'oven':
                method_dict[i+1].append(word)

    return method_dict

def ingredient_info(ingredients):
    ingredient_dict = {}
    units = ['cup', 'cups', 'ml', 'mls', 'liters', 'L', 'ounces', 'oz', 'lb', 'lbs', 'stick', 'sticks', 'pounds', 'pound', 'teaspoon', 'teaspoons', 'tsp', 'tablespoon', 'tablespoons', 'tbsp']    
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
    units = ['cup', 'cups', 'ml', 'mls', 'liters', 'L', 'ounces', 'oz', 'lb', 'lbs', 'stick', 'pounds', 'pound', 'teaspoon', 'teaspoons', 'tsp', 'tablespoon', 'tablespoons', 'tbsp']    
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
            if quantity != '1' and (nlp(ingredient[len(ingredient)-1])[0].tag_ == 'NN' or ingredient[len(ingredient)-1] != 's'):
                ingredient = ingredient + 's'
        else:
            if quantity != '1' and (nlp(unit)[0].tag_ == 'NN' or unit[len(unit)-1] != 's'):
                unit = unit + 's'
            elif quantity == '1' and (nlp(unit)[0].tag_ == 'NNS' or unit[len(unit)-1] == 's'):
                unit = unit[0:len(unit)-1]
        if prep == '':
            t3 = ''
        curr_response = quantity + t1 + unit + t2 + ingredient + t3 + prep
        response.append(curr_response)
    new_ingredients = []
    print("These are the new ingredients: ")
    for a_response in response:
        print(a_response)
        new_ingredients.append(a_response)
    print("These are the new steps: ")
    i = 0
    for step in steps:
        step = step.split()
        newstep = copy.deepcopy(step) 
        for unit in units:
            if step.__contains__(unit):
                index = step.index(unit) - 1
                num = step[index]
                if nlp(unit)[0].tag_ == 'NN' or unit[len(unit)-1] != 's' and num > 1:
                    newstep[index+1] = unit + 's'
                if nlp(unit)[0].tag_ == 'NNS' or unit[len(unit)-1] == 's' and num == 1:
                    newstep[index+1] = unit[0:len(unit)-1]          
                try:
                    f = float(num)
                    newstep[index] = multiply(num,factor)
                except:
                    continue
        i = i + 1
        print('step ' + str(i) + ': ' + ' '.join(newstep))
    return new_ingredients


def multiply(num,factor):
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
    
def method_transformations():
    method_arr = [['mix','whisk','beat'],['rub','pat','marinate'],['bake','roast','air fry','saute','steam','sear','saut??','saute','fry','grill','barbecue','broil','toast'],['chop','slice','dice','julienne','cut','cube','mince','cleave'],['boil','steam'],['smash','mash','cut']]
    counter = 1
    new_steps = []
    for step in steps:
        stepcounter = "Step "
        stepcounter+=str(counter)
        stepcounter+=":"
        print(stepcounter, step)
        in_step = method_dict[counter] 
        stri = "Here are the replaceable actions used in this step: "
        ctr = 0
        replaceable = []
        for action in in_step:
            for arr in method_arr:
                if action.lower() in arr:
                    stri = stri + action + ', '
                    replaceable.append(action.lower())
                    ctr+=1
                    break
        if ctr == 0:
            print("There are no replaceable actions in this step.")
            counter+=1
            new_steps.append(step)
            input("Press Enter to move to the next step\n")
            continue            
        print(stri[0:len(stri)-2])
        for action in replaceable:
            choice = input("\nWould you like to replace "+"'"+action+"'? Enter 'yes' or 'no': ")
            if choice.lower() == 'yes':
                found = False
                for array in method_arr:
                    if action in array:
                        stri = "Here are your replacement options for "+"'"+action+"'"+": "
                        for method in array:
                            if method != action:
                                stri = stri + method + ', '
                        print(stri[0:len(stri)-2])
                        new = input("Which option do you prefer? ")
                        index = in_step.index(action)
                        step = step.lower().split()
                        oldi = step.index(action)
                        step[oldi] = new
                        step = ' '.join(step)
                        method_dict[counter][index] = new
                        found = True
                        break
                if not found:
                    print("I can't find any replacements for that action.")
            continue
        new_steps.append(step)    
        counter+=1
        input("Press Enter to move to the next step\n")
    print("These are the new steps:")
    counter = 1
    for step in new_steps:
        stepcounter = "Step "
        stepcounter+=str(counter)
        stepcounter+=":"
        print(stepcounter, step)
        counter+=1
    return new_steps      

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
print("I am equipped to handle scaling, substitutions, method transformations, and ingredient transformations.")
print("My ingredient transformations include adapting the recipe to the greek style, to healthy, to unhealthy, to vegetarian, to non-vegetarian, and to gluten-free.")
url = input("Please enter the URL of a recipe: ")

scraper = scrape_me(url)
title = scraper.title()
ingredients = scraper.ingredients()
steps = scraper.instructions()
steps = steps.split('.')
counter = 0
while counter < len(steps) - 1:
    step = steps[counter]
    step = step.strip()
    steps[counter] = step
    counter+=1 
steps = steps[0:len(steps)-1]

method_dict = direction_methods(steps)

print("I see that you would like to make " + title[0:len(title)] + '.')
print("What would you like to change about the recipe? For example, say "+"'"+"make it vegetarian"+"'")

ansArr = ['Nothing','Step','Ingredient']
stepI = 0
curr_ingr = ''
healthyflag = False
unhealthyflag = False
while(True):

    preAns = ansArr[0]
    inpt = input("Enter text: ")
    doc = nlp(inpt)
    numDict = doc._.numerize()
    vegflag = False

    for k,v in numDict.items():
        if v.isnumeric():
            if int(v) < len(steps) and "step" in inpt.lower():
                print("step " + v + ": " + steps[int(v) - 1])
                stepI = int(v) - 1
        else:
            if int(v[0]) < len(steps) and "step" in inpt.lower():
                print("step " + v[0] + ": " + steps[int(v[0]) - 1])
                stepI = int(v[0]) - 1

    if healthyflag == False and unhealthyflag==False:
        if "chicken" in inpt.lower() or "ground beef" in inpt.lower() or "pork" in inpt.lower() or "steak" in inpt.lower() or "turkey" in inpt.lower() or "duck" in inpt.lower() or "fish" in inpt.lower():
            vegflag = False
            print("Keep in mind that replacing ingredients with a meat substitute can change the duration you want to cook for. Not all directions will be applicable, and it is unsafe to consume undercooked meat products.")
            replacement = inpt.lower()
            the_veg = contains_vegoptions()
            newingredients = []
            for ingr in ingredients:
                flag = False
                for item in the_veg:
                    if ingr.__contains__(item):
                        ingr = ingr.replace(item, replacement)
                        newingredients.append(ingr)
                        flag = True
                if flag==False:
                    newingredients.append(ingr)
            ingredients = newingredients
            newsteps = []
            for dir in steps:
                for item in the_veg:
                    if dir.__contains__(item):
                        dir = dir.replace(item, replacement)
                        newsteps.append(dir)
                        break
                    else:
                        newsteps.append(dir)
                        break
            steps = newsteps
            print("These are the new, non-vegetarian ingredients:")
            for ing in ingredients:
                print(ing)
            print("These are the new steps:")
            counter = 1
            for dir in steps:
                stepcounter = "Step "
                stepcounter+=str(counter)
                stepcounter+=":"
                print(stepcounter, dir)
                counter+=1
        elif "tofu" in inpt.lower() or "lentils" in inpt.lower() or "chickpeas" in inpt.lower() or "beans" in inpt.lower() or "eggplant" in inpt.lower():
            vegflag = False
            print("Keep in mind that replacing meat with a vegetarian substitute may change the duration you want to cook for. Not all directions will be applicable.")
            replacement = inpt.lower()
            the_meat = contains_meat()
            newingredients = []
            for ingr in ingredients:
                flag = False
                for item in the_meat:
                    if ingr.__contains__(item) and ingr.__contains__("flavored"):
                        string = item
                        string+= " flavored"
                        ingr = ingr.replace(string, "regular")
                        newingredients.append(ingr)
                        flag = True
                    elif ingr.__contains__(item):
                        ingr = ingr.replace(item, replacement)
                        newingredients.append(ingr)
                        flag = True
                if flag==False:
                    newingredients.append(ingr)
            ingredients = newingredients
            newsteps = []
            for dir in steps:
                for item in the_meat:
                    if dir.__contains__(item):
                        dir = dir.replace(item, replacement)
                        newsteps.append(dir)
                        break
                    else:
                        newsteps.append(dir)
                        break
            steps = newsteps
            print("These are the new, vegetarian ingredients:")
            for ing in ingredients:
                print(ing)
            print("These are the new steps:")
            counter = 1
            for dir in steps:
                stepcounter = "Step "
                stepcounter+=str(counter)
                stepcounter+=":"
                print(stepcounter, dir)
                counter+=1
        elif "healthy" in inpt.lower() and "un" not in inpt.lower():
            healthyflag = True
            bad_foods = healthy()
            replacements = len(bad_foods)
            if len(bad_foods) == 0:
                print("This recipe is already very healthy.")
            else:
                for food in bad_foods:
                    good_foods = un_to_healthy[food]
                    health_str = ""
                    for gfood in good_foods:
                        health_str+=gfood
                        health_str+=","
                        health_str+=" "
                    health_str = health_str[:-2]
                    print("You may replace", food, "with one of the following healthy options:", health_str)
                print("Input the", replacements, "healthy ingredients you want to substitute for the", replacements, "unhealthy ingredients")
        elif "healthy" in inpt.lower() and "un" in inpt.lower():
            unhealthstr = ""
            unhealthyflag = True
            good_foods = unhealthy()
            replacements = {}
            for food in good_foods:
                unhealthstr = ""
                replacements = healthy_to_un[food]
                for rep in replacements:
                    unhealthstr+=rep
                    unhealthstr+=", "
                print("You may replace", food, "with one of the following unhealthy options:", unhealthstr)
            print("You may also add extra oil, butter, or sugar to this recipe, or pan-fry ingredients to make it less healthy")
            print("Input the ingredients you would like to add to this recipe to make it less healthy.")
        elif "greek" in inpt.lower():
            units = ['cup', 'cups', 'ml', 'mls', 'liters', 'L', 'ounces', 'oz', 'lb', 'lbs', 'stick', 'sticks', 'pounds', 'pound', 'teaspoon', 'teaspoons', 'tsp', 'tablespoon', 'tablespoons', 'tbsp']
            notgreekherbs = ["dill", "cilantro", "jalapeno", "jalape??o", "basil", "cumin"]
            counter=0
            new = []
            for ingr in ingredients:
                flag = False
                newingr = ""
                for herb in notgreekherbs:
                    if herb in ingr.lower():
                        if counter==0:
                            counter+=1
                            newingr = "chopped thyme, to taste"
                            flag = True
                            new.append(newingr)
                        elif counter==1:
                            counter+=1
                            newingr = "chopped mint, to taste"
                            flag = True
                            new.append(newingr)
                        elif counter==2:
                            counter+=1
                            flag = True
                            newingr = "chopped oregano, to taste"
                            new.append(newingr)
                if "cheese" in ingr.lower():
                    ingr = ingr.split()
                    for word in ingr:
                        if word in units:
                            newingr+=word
                            newingr+=" "
                            break
                        else:
                            newingr+=word
                            newingr+=" "
                    newingr+="feta cheese"
                    new.append(newingr)
                elif "oil" in ingr.lower():
                    ingr = ingr.split()
                    for word in ingr:
                        if word in units:
                            newingr+=word
                            newingr+=" "
                            break
                        else:
                            newingr+=word
                            newingr+=" "
                    newingr+="olive oil"
                    new.append(newingr)
                elif "beans" in ingr.lower():
                    ingr = ingr.split()
                    for word in ingr:
                        if word in units:
                            newingr+=word
                            newingr+=" "
                            break
                        else:
                            newingr+=word
                            newingr+=" "
                    newingr+="chickpeas"
                    new.append(newingr)
                elif "bell pepper" in ingr.lower():
                    ingr = ingr.split()
                    for word in ingr:
                        if word in units:
                            newingr+=word
                            newingr+=" "
                            break
                        else:
                            newingr+=word
                            newingr+=" "
                    newingr+="green olives"
                    new.append(newingr)
                elif flag==False:
                    newingr = ingr
                    new.append(newingr)
            new.append("drizzle of tzaziki sauce")
            ingredients = new
            print("These are the new, greek ingredients")
            for ing in ingredients:
                print(ing)
            c = 0
            newsteps = []
            for dir in steps:
                for herb in notgreekherbs:
                    if dir.__contains__(herb):
                        if c == 0:
                            dir = dir.replace(herb, "thyme")
                            c+=1
                            continue
                        elif c == 1:
                            dir = dir.replace(herb, "mint")
                            c+=1
                            continue
                        elif c == 2:
                            dir = dir.replace(herb, "oregano")
                            c+=1
                            continue
                if dir.__contains__("bell pepper"):
                    dir = dir.replace("bell pepper", "green olives")
                if dir.__contains__("pepper") and "bell" not in dir:
                    dir = dir.replace("pepper", "green olives")
                if dir.__contains__("beans"):
                    dir = dir.replace("beans", "chickpeas")   
                if dir.__contains__("oil"):
                    dir = dir.replace("oil", "olive oil")
                if dir.__contains__("cheese"):
                    dir = dir.replace("cheese", "feta cheese")
                newsteps.append(dir)
            steps = newsteps
            print("These are the new steps:")
            counter = 1
            for dir in steps:
                stepcounter = "Step "
                stepcounter+=str(counter)
                stepcounter+=":"
                print(stepcounter, dir)
                counter+=1
        elif "gluten" in inpt.lower():
            units = ['cup', 'cups', 'ml', 'mls', 'liters', 'L', 'ounces', 'oz', 'lb', 'lbs', 'stick', 'sticks', 'pounds', 'pound', 'teaspoon', 'teaspoons', 'tsp', 'tablespoon', 'tablespoons', 'tbsp']
            new = []
            flag = False
            for ingr in ingredients:
                newingr = ""
                if "flour" in ingr.lower():
                    flag = True
                    ingr = ingr.split()
                    for word in ingr:
                        if word in units:
                            newingr+=word
                            newingr+=" "
                            break
                        else:
                            newingr+=word
                            newingr+=" "
                    newingr+="almond flour"
                    new.append(newingr)
                elif "bread" in ingr.lower():
                    flag = True
                    ingr = ingr.split()
                    for word in ingr:
                        if word in units:
                            newingr+=word
                            newingr+=" "
                            break
                        else:
                            newingr+=word
                            newingr+=" "
                    newingr+="gluten-free bread"
                    new.append(newingr)
                elif "pasta" in ingr.lower():
                    flag = True
                    ingr = ingr.split()
                    for word in ingr:
                        if word in units:
                            newingr+=word
                            newingr+=" "
                            break
                        else:
                            newingr+=word
                            newingr+=" "
                    newingr+="gluten-free pasta or rice"
                    new.append(newingr)
                elif "ladyfingers" in ingr.lower():
                    flag = True
                    newingr+="gluten-free ladyfingers or gluten-free cookies"
                    new.append(newingr)
                else:
                    new.append(ingr)
            newsteps = []
            for dir in steps:
                newingr = ""
                if "flour" in dir.lower():
                    dir = dir.replace("flour", "almond flour")
                    #newsteps.append(dir)
                if "bread" in dir.lower():
                    dir = dir.replace("bread", "gluten-free bread")
                    #newsteps.append(dir)
                if "pasta" in dir.lower():
                    dir = dir.replace("pasta", "gluten-free pasta or rice")
                if "ladyfingers" in dir.lower():
                    dir = dir.replace("ladyfingers", "gluten-free ladyfingers or gluten-free cookies")
                else:
                    dir = dir
                newsteps.append(dir)
                steps = newsteps
            if flag==False:
                print("This recipe is likely gluten-free already.")
            else:
                ingredients = new
                print("These are the new gluten-free ingredients:")
                for ingredient in ingredients:
                    print(ingredient)
                print("These are the new steps:")
                counter = 1
                for dir in steps:
                    stepcounter = "Step "
                    stepcounter+=str(counter)
                    stepcounter+=":"
                    print(stepcounter, dir)
                    counter+=1
        
        elif inpt.lower().__contains__("double"):
            ingredients = scaling_questions(2)

        elif inpt.lower().__contains__("half") or inpt.lower().__contains__("halv"):
            ingredients = scaling_questions(.5)
        
        elif inpt.lower().__contains__("triple"):
            ingredients = scaling_questions(3)
        
        elif inpt.lower().__contains__("method"):
            steps = method_transformations()
        
        elif "ingredient" in inpt.lower():
            print_ingredients()

        elif "directions" in inpt.lower():
            print("These are the directions. Type 'next' or 'back' or simply type a number to navigate the steps!")
            print("step 1:", steps[0])

        elif "repeat" in inpt.lower():
            print("step", str(stepI) + ":", steps[stepI])

        elif "next" in inpt.lower():
            if stepI < len(steps) - 2:
                stepI += 1
                curr_ingr = ''
                print("step", str(stepI + 1) + ":", steps[stepI])
            else:
                print("There are no more steps!")

        elif "back" in inpt.lower() or "prev" in inpt.lower():
            if stepI >= 1:
                stepI -= 1
                curr_ingr = ''
                print("step", str(stepI + 1) + ":", steps[stepI])
            else:
                print("There are no steps before this!")

        elif "vegetarian" in inpt.lower() and "non" not in inpt.lower():
            healthyflag = False
            the_meat = contains_meat()
            if len(the_meat)==0:
                print("This recipe is already vegetarian")
            else:
                for ingr in ingredients:
                    if ingr.__contains__("burger") or ingr.__contains__("patty"):
                        print("You may replace the meat patty with a bean burger, soy burger, impossible burger, mushroom burger, or veggie burger")
                        break
                    elif ingr.__contains__("flavored"):
                        print("You may choose to omit the", ingr, "entirely, or you may choose to use a vegetarian substitute.")
                        for item in the_meat:
                            if ingr.__contains__(item):
                                oldingr = ingr
                                ingr = ingr.replace(item, "regular")
                                print("In this case, you would replace the", oldingr, "with", ingr)
                                the_meat.remove(item)
                for item in the_meat:
                    if item != "burger":
                        print("You can choose to omit the", item, "entirely, or you may replace it with one of the following vegetarian substitutes:")
                        print("tofu, lentils, beans, chickpeas, or eggplant")
                vegflag = True
                print("What would you like to substitute for the meat?")
        elif "vegetarian" in inpt.lower() and "non" in inpt.lower():
            healthyflag = False
            the_meat = contains_meat()
            if len(the_meat)>0:
                print("This recipe is already contains meat")
            else:
                flag = False
                for ingr in ingredients:
                    if ingr.__contains__("burger") or ingr.__contains__("patty"):
                        print("You may replace the vegetarian patty with a beef patty or turkey patty")
                        flag = True
                        break
                    if ingr.__contains__("tofu"):
                        flag = True
                        print("You may replace the tofu with one of the following meat options:")
                    if ingr.__contains__("beans"):
                        flag = True
                        print("You may replace the beans with one of the following meat options:")
                    if ingr.__contains__("chickpeas"):
                        flag = True
                        print("You may replace the chickpeas with one of the following meat options:")
                    if ingr.__contains__("eggplant"):
                        flag = True
                        print("You may replace the eggplant with one of the following meat options:")
                    if ingr.__contains__("lentils"):
                        flag = True
                        print("You may replace the lentils with one of the following meat options:")
                if flag==False:
                    print("You may add one of the following meat options:")
                    print("chicken, ground beef, steak, turkey, duck, pork, or fish")
                else:
                    print("chicken, ground beef, steak, turkey, duck, pork, or fish")
                    print("What meat option you like to substitute in?")
        elif "substitute" in inpt.lower() or "replace" in inpt.lower() or "substitution" in inpt.lower() or "replacement" in inpt.lower():
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
    elif healthyflag==True:
            healthyflag = False
            inpt = inpt.replace(",", "")
            counter=0
            separate = inpt.lower().split()
            thestr = ""
            goodfoods = []
            while counter<len(separate)-2:
                thestr = ""
                thestr+=separate[counter]
                thestr+=" "
                thestr+=separate[counter+1]
                if thestr in healthyoptions:
                    goodfoods.append(thestr)
                    counter+=2  
                elif separate[counter] in healthyoptions:
                    goodfoods.append(separate[counter])
                    counter+=1
            if separate[-1] in healthyoptions:
                goodfoods.append(separate[-1])
            badfoods = healthy()
            newingredients = []
            newsteps = []
            counter=0
            units = ['cup', 'cups', 'ml', 'mls', 'liters', 'L', 'ounces', 'oz', 'lb', 'lbs', 'stick', 'pounds', 'pound', 'teaspoon', 'teaspoons', 'tsp', 'tablespoon', 'tablespoons', 'tbsp']
            for ingr in ingredients:
                foodcounter=0
                newingr = ""
                for food in badfoods:
                    if ingr.__contains__(food):
                        newingr = ""
                        ingr = ingr.split()
                        for word in ingr:
                            if word in units:
                                newingr+=word
                                newingr+=" "
                                newingr+=goodfoods[foodcounter]
                                break
                            else:
                                newingr+=word
                                newingr+=" "
                    else:
                        foodcounter+=1
                if newingr=="":
                    ingredients[counter] = ingr
                else:
                    ingredients[counter] = newingr
                counter+=1
            for ing in ingredients:
                print(ing)
            counter=0
            for dir in steps:
                foodcounter=0
                for food in badfoods:
                    if dir.__contains__(food):
                        dir = dir.replace(food, goodfoods[foodcounter])
                        foodcounter+=1
                    else:
                        foodcounter+=1
                steps[counter] = dir
                counter+=1
            print("These are the new steps:")
            counter = 1
            for dir in steps:
                stepcounter = "Step "
                stepcounter+=str(counter)
                stepcounter+=":"
                print(stepcounter, dir)
                counter+=1
    elif unhealthyflag==True:
        unhealthyflag = False
        goodfoods = unhealthy()
        inpt = inpt.lower().replace(",", "")
        additions = []
        if inpt.lower().__contains__("sugar"):
            additions.append("sugar")
        if inpt.lower().__contains__("butter"):
            additions.append("butter")
        if inpt.lower().__contains__("oil"):
            additions.append("oil")
        inpt = inpt.replace("sugar", "")
        inpt = inpt.replace("butter", "")
        inpt = inpt.replace("oil", "")
        inpt = inpt.split()
        counter=0
        foodcounter=0
        for ingr in ingredients:
            flag = False
            for word in goodfoods:
                if ingr.__contains__(word):
                    flag = True
                    replace = healthy_to_un[word]
                    rep = ""
                    for w in inpt:
                        if w in replace:
                            rep = w
                            break
                    ingr = ingr.replace(word, rep)
                    foodcounter+=1
                    ingredients[counter]=ingr
                    counter+=1
                    break
            if flag==False:
                ingredients[counter] = ingr
                counter+=1
        foodcounter=0
        counter=0
        for dir in steps:
            flag = False
            for word in goodfoods:
                if dir.__contains__(word):
                    flag = True
                    replace = healthy_to_un[word]
                    for w in replace:
                        if w in inpt:
                            dir = dir.replace(word, rep)
                    steps[counter]=dir
                    counter+=1
                    break
            if flag==False:
                steps[counter] = dir
                counter+=1
        counter=0
        newingredients = []
        for ingr in ingredients:
            newingr = ingr
            for extra in additions:
                if ingr.__contains__(extra):
                    newingr = "2x "
                    newingr+=ingr
                    newingr+=" "
                    ingredients[counter] = newingr
            newingredients.append(newingr)   
        ingredients = newingredients    
        print("These are the new, unhealthy ingredients:")
        for ing in ingredients:
            print(ing)
        print("These are the new steps:")
        counter = 1
        for dir in steps:
            stepcounter = "Step "
            stepcounter+=str(counter)
            stepcounter+=":"
            print(stepcounter, dir)
            counter+=1