from django.shortcuts import render, redirect
import time                # for generating order wait time 
import random              # to randomize the daily special
import datetime            # to calculate readytime

# Create your views here.
images = [
    # the krusty krab
    "https://static.wikia.nocookie.net/nickelodeon/images/7/77/KrustyKrabStock.png/revision/latest?cb=20230420021225",
    # krabby patty
    "https://i.ytimg.com/vi/k5e1HPeusiA/hqdefault.jpg",
    # kelp shake
    "https://static.wikia.nocookie.net/spongebob/images/0/05/Best_Frenemies_012.png/revision/latest?cb=20191117235659",
    # coral bits
    "https://static.wikia.nocookie.net/spongebob/images/7/7e/Coral_Bits_HD.PNG/revision/latest?cb=20211118144751",
    # deluxe krabby patty
    "https://static.wikia.nocookie.net/spongebob/images/9/9b/Deluxe_Krabby_Patty.jpg/revision/latest?cb=20140113015823",
    # kids meal
    "https://static.wikia.nocookie.net/spongebob/images/5/5b/Yours%2C_Mine_and_Mine_014.png"
    
]

daily_special = [
    # pretty patty
    "https://static.wikia.nocookie.net/spongebob/images/9/9a/Patty_Hype_056.png/revision/latest?cb=20191126035035",
    # jelly patty
    "https://static.wikia.nocookie.net/spongebob/images/0/02/Jelly_Patty.png/revision/latest?cb=20210923000313",
    # pipsqueak patty
    "https://static.wikia.nocookie.net/spongebob/images/0/05/Mermaid_Man_and_Barnacle_Boy_V_023.png/revision/latest/scale-to-width-down/1200?cb=20200810154951",
    # nasty patty
    "https://static.wikia.nocookie.net/spongebob/images/b/b9/Nasty_Patty_061.png",
    # pizza
    "https://static.wikia.nocookie.net/spongebob/images/5/5f/Krusty_Krab_Pizza.png/revision/latest?cb=20230812043541",
    
]

daily_special_menu = [
    'Pretty Patty', 'Jelly Patty', 'Pipsqueak Patty', 'All Organic, Vegan, Gluten-Free, Soy-Free, Krabby Patty', 'Krusty Krab Pizza'
]

def main(request):
    template_name = 'restaurant/main.html'

    context = {
        "krusty_krab" : images[0],
        "current_time" : time.ctime()
    }

    return render(request, template_name, context)


def order(request):
    template_name = 'restaurant/order.html'

    context = {
        "krabby_patty" : images[1],
        "kelp_shake" : images[2],
        "coral_bits" : images[3],
        "deluxe" : images[4],
        "kids_meal" : images[5],
        "daily_special" : random.choice(daily_special_menu)
    }

    return render(request, template_name, context)

def confirmation(request):
    template_name = 'restaurant/confirmation.html'

    print(request)
    
    if request.POST:
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        items = request.POST.getlist('items[]')  # Get selected items
        order_items = []
        order_total = 0

        
        # calculate the wait time
        wait = random.randint(30, 60)
        current_time = datetime.datetime.now()
        time_to_add = datetime.timedelta(minutes=wait)
        new_time = current_time + time_to_add

        for item in items:
            o_name, price = item.split(",")  # Split the item name and price
            price = int(price)  # Convert price to an integer
            order_items.append({'name': o_name})
            order_total += price  # Calculate total price

        context = {
            'order_items': order_items,
            "order_total" : order_total,
            "name" : name,
            "phone" : phone,
            "email" : email,
            "readytime" : new_time
        }

        return render(request, template_name, context)
    
    return redirect("order")

