# restaurant/views.py
from django.shortcuts import render, redirect, HttpResponse
from .models import Dish, Order, OrderDish

def welcome(request):
    return HttpResponse('<h1>Welcome To Zomoto</h1>')

def menu(request):
    dishes = Dish.objects.all()
    return render(request, 'menu.html', {'dishes': dishes})

def add_dish(request):
    if request.method == 'POST':
        dish_name = request.POST.get('dish_name')
        price = request.POST.get('price')
        availability = request.POST.get('availability', False)
        Dish.objects.create(dish_name=dish_name, price=price, availability=availability)
        return redirect('menu')


def take_order(request):
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        dish_ids = request.POST.getlist('dish')
        order = Order.objects.create(customer_name=customer_name)

        for dish_id in dish_ids:
            dish = Dish.objects.get(pk=dish_id)
            OrderDish.objects.create(order=order, dish=dish)
            dish.availability = False
            dish.save()

        return redirect('orders')  # Redirect to the 'orders' view
    else:
        dishes = Dish.objects.all()
        return render(request, 'take_order.html', {'dishes': dishes})


def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST['status']
        order = Order.objects.get(pk=order_id)
        order.status = new_status
        order.save()
        return redirect('orders')  # Redirect to the 'orders' view
    else:
        order = Order.objects.get(pk=order_id)
        return render(request, 'update_order_status.html', {'order': order})

def orders(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': orders})
