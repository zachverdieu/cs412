from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random, time

# Create your views here.

menu = {
    "THE Biggie Burger": 10.00,
    "THE Big Bacon Burger":  11.00,
    "THE Big Veggie Burger": 12.00,
    "THE Big Back Burger": 15.00,
    "THE Mini Burger": 7.00,
}

specials = {
    "Cheesy Fries": 5.00,
    "Loaded Onion Rings": 6.00,
    "Jalepeño Poppers": 5.00,
    "Corndog": 5.00,
}

image = "https://thumbs.dreamstime.com/b/web-335609053.jpg"

def main(request):
    ''' Show main/home page to user'''

    template_name = "restaurant/main.html"

    context = {
        "time": time.ctime(),
        "image": image,
    }

    return render(request, template_name, context)

def order(request):
    ''' Show menu/order form for user to submit an order'''

    template_name = "restaurant/order.html"

    random_special = random.choice(list(specials.keys()))

    context = {
        "time": time.ctime(),
        "burger_1": list(menu.keys())[0],  
        "burger_2": list(menu.keys())[1],  
        "burger_3": list(menu.keys())[2],  
        "burger_4": list(menu.keys())[3],  
        "burger_5": list(menu.keys())[4],  
        "burger_1_price": menu["THE Biggie Burger"],  
        "burger_2_price": menu["THE Big Bacon Burger"],   
        "burger_3_price": menu["THE Big Veggie Burger"],
        "burger_4_price": menu["THE Big Back Burger"],
        "burger_5_price": menu["THE Mini Burger"],                        
        "special": random_special,
        "special_price": specials[random_special]
    }

    return render(request, template_name, context)

def confirmation(request):
    '''Process the form submission, and generate result'''

    template_name = "restaurant/confirmation.html"

    if request.POST:
        selected_items = []
        total = 0

        burgers = ["burger_1", "burger_2", "burger_3", "burger_4", "burger_5"]

        for key in burgers:
            burger_name = request.POST.get(key)
            if burger_name:
                if key == "burger_1":  
                    size = request.POST.get("burger_1_size", "single")
                    price = menu[burger_name]
                    if size == "double":
                        price += 3.00
                        burger_name = f"{burger_name} (Double)"
                    else:
                        burger_name = f"{burger_name} (Single)"
                else:
                    price = menu[burger_name]

                selected_items.append(burger_name)
                total += price

        special_item = request.POST.get("special")
        if special_item:
            selected_items.append(special_item)
            total += specials[special_item]

        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        instructions = request.POST.get("special_instructions", "")

        now = time.time()
        minutes = random.randint(30, 60)
        seconds = now + (minutes * 60)
        readytime = time.ctime(seconds)

        context = {
            "foods": selected_items,
            "total": total,
            "time": time.ctime(),
            "name": name,
            "phone": phone,
            "email": email,
            "special_instructions": instructions,
            "readytime": readytime,
        }
        
        return render(request, template_name, context)

    return HttpResponse("No order submitted.")
