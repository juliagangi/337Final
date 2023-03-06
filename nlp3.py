


def ingredient_questions(question,step,curr_ingr):
    units = ['cup', 'cups', 'ml', 'mls', 'liters', 'L', 'ounces', 'oz', 'lb', 'lbs', 'pounds', 'pound', 'teaspoon', 'teaspoons', 'tsp', 'tablespoon', 'tablespoons', 'tbsp']
    question = question.lower()
    step = step.lower()
    ingredient_dict = ingredient_info(ingredients)
    quant = False 
    time = False
    temp = False
    kw = ''
    if question.__contains__("double"):
        kw = "factor"
        factor = 2
    elif question.__contains__("triple"):
        kw = "factor"
        factor = 3    
    if kw == "factor":
        find_ingr = []
        for ingredient in ingredient_dict:
            if question.__contains__(ingredient) or question.__contains__(plural(ingredient)):
                find_ingr.append(ingredient)
            elif len(ingredient.split()) > 1:
                found = 0
                for element in ingredient.split():
                    if question.__contains__(element) and nlp(element)[0].pos_ == 'NOUN':
                        find_ingr.append(ingredient)
                        found = 1
                        break
                if not found and question.__contains__(plural(ingredient.split()[len(ingredient.split())-1])):
                    find_ingr.append(ingredient)
        if len(find_ingr) == 0:
            response = []
            for ingredient in ingredient_dict:
                lst = ingredient_dict[ingredient]
                quantity = multiply(lst[0],factor)
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
            for a_response in response:
                print(a_response)
            return ['',1]
        else:
            response = []
            for ingredient in find_ingr:
                lst = ingredient_dict[ingredient]
                quantity = multiply(lst[0],factor)
                unit = lst[1]
                t1 = ' '
                t2 = ' '
                if unit == '':
                    t1 = ''
                    if quantity != '1' and nlp(ingredient[len(ingredient)-1])[0].tag_ == 'NN':#ingredient[len(ingredient)-1] != 's':
                        ingredient = ingredient + 's'
                else:
                    if quantity != '1' and nlp(unit)[0].tag_ == 'NN':#unit[len(unit)-1] != 's':
                        unit = unit + 's'
                print('You need ' + quantity + t1 + unit + t2 + ingredient)  
            return ['',1]
    return ['','']   

def multiply(num,factor):
    num = num.split()
    if num.__contains__('or'):
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
        return ' '.join(num)
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


