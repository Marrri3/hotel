from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, get_object_or_404
from products.models import *
from products.forms import *
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    context = {
        'title': 'FOUR SEASON - home'
    }
    return render(request, 'products/index.html', context)

def about(request):
    context = {
        'title': 'FOUR SEASON - about'
    }
    return render(request,'products/index2.html', context)

def profile(request): #функция изменения профиля
    from datetime import datetime
    user_id = request.user.id

    if request.method == 'POST': #Проверка  метода запроса 
        form = UserProfileForm(instance=request.user, data=request.POST) #создание объекты формы с данными
        if form.is_valid(): #проверка вводимых данных
            form.save() #сохранение измененных данных
            return HttpResponseRedirect(reverse('index3')) 
    else:
        form = UserProfileForm(instance=request.user) 

    reservations = reservation.objects.filter(guest_id=user_id).order_by('start_date')

    formatted_reservations = []
    for reservationItem in reservations:
        # Убедитесь, что start_date и end_date имеют значения
        if reservationItem.start_date and reservationItem.end_date:
        # Преобразуем DateField в datetime
            from_date = datetime.combine(reservationItem.start_date, datetime.min.time())
            to_date = datetime.combine(reservationItem.end_date, datetime.min.time())
            date_of_purchases = datetime.combine(reservationItem.date, datetime.min.time())

            formatted_reservations.append({
                'from_date': from_date.strftime('%d.%m.%Y'),
                'to_date': to_date.strftime('%d.%m.%Y'),
                'date_of_purchases': date_of_purchases.strftime('%d.%m.%Y'),  # Предполагается, что hotel_number - это объект
                'price': reservationItem.total_price  # Предполагается, что price - это число
            })


    context = {
        'title': 'FOUR SEASON - profile',
        'form': form,
        'reservations': formatted_reservations,  # Здесь нужно использовать formatted_reservations
    }

    return render(request, 'products/index3.html', context)  # Отображение шаблона с данными

def custom_logout(request): #функция выхода из аккаунта
    logout(request) #выход из аккаунта
    return redirect('index')

def catalog(request):
    from django.db.models import Q
    from datetime import datetime

    context = {
        'title': 'CATALOG',
    }
    
    form = BookingForm(request.POST or None)
    
    # Получаем все номера при каждом запросе
    numbers = hotel_number.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            # Обработка данных формы
            checkin = form.cleaned_data['checkin']
            checkout = form.cleaned_data['checkout']
            room_type = form.cleaned_data['room_type']
            rooms = form.cleaned_data['rooms']

            # Сохранение данных формы в сессии (если нужно)
            request.session['checkin'] = checkin.strftime('%Y-%m-%d')
            request.session['checkout'] = checkout.strftime('%Y-%m-%d')
            request.session['room_type'] = room_type
            request.session['rooms'] = rooms
            
            # Применение фильтрации
            checkin_date = datetime.strptime(checkin.strftime('%Y-%m-%d'), '%Y-%m-%d')
            checkout_date = datetime.strptime(checkout.strftime('%Y-%m-%d'), '%Y-%m-%d')

            # Фильтрация номеров
            numbers = hotel_number.objects.filter(
                characteristics_id__type=room_type,
                characteristics_id__number_of_rooms=rooms
            ).exclude(
                Q(reservation__start_date__lt=checkout_date) &
                Q(reservation__end_date__gt=checkin_date)
            )

    # Подготовка данных для отображения
    numbers_data = [{'id': number.id, 'image': number.image.url, 'characteristics': number.characteristics_id} for number in numbers]
    context['numbers'] = numbers_data

    return render(request, 'products/index4.html', {'form': form, 'title': context['title'], 'numbers': context['numbers']})


def reservation_number(request, number_id):
    from datetime import datetime   

    number = get_object_or_404(hotel_number, id=number_id)

    checkin = request.session.get('checkin')
    checkout = request.session.get('checkout')
    room_type = request.session.get('room_type')
    number_of_rooms = request.session.get('rooms')

    # Преобразование дат из строкового формата в объекты даты
    checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
    checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
    nights = (checkout_date - checkin_date).days
    total_price = nights * number.characteristics_id.price

    if request.method == 'POST':
        # Сохранение данных бронирования
        new_reservation = reservation(
            hotel_number_id=number,
            guest_id=request.user,
            start_date=checkin_date,
            end_date=checkout_date,
            total_price=total_price,
            date=datetime.now()
        )
        new_reservation.save()

        return redirect('reservation_successfully')

    context = {
        'title': 'FOUR SEASON - reservation',
        'number': number,
        'form': reservation()  # Placeholder form; это просто для передачи csrf_token
    }
    return render(request, 'products/index5.html', context)

def reservation_successfully(request):
    context = {
        'title': 'FOUR SEASON'
    }
    return render(request, 'products/index6.html', context)



def authorization(request): #функция авторизации(входа в аккаунт) пользователя
    if request.method == 'POST': #Проверка  метода запроса 
        form = UserLoginForm(data=request.POST) #создание объекты формы с данными
        if form.is_valid(): #проверка вводимых данных
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password) #проверка аутентификации
            if user is not None:
                auth.login(request, user) #вход в систему 
                return HttpResponseRedirect(reverse('index')) #Перенос на страницу входа
    else:
        form = UserLoginForm() #создание пустой формы
    context = {
        'title': 'FOUR SEASON - authorization',
        'form': form
    }
    return render(request, 'products/index7.html', context) #отображение шаблона с данными


def registration(request): #функция регистрации пользователя
    if request.method == 'POST':   #Проверка  метода запроса 
        form = UserRegistrationForm(data=request.POST) #создание объекты формы с данными
        if form.is_valid(): #проверка вводимых данных
            form.save() #Сохранение данных в БД
            return HttpResponseRedirect(reverse('index7')) #Перенос на страницу входа
    else:
        form = UserRegistrationForm() #создание пустой формы
    context = {
        'title': 'FOUR SEASON - registration',
        'form': form,
    }
    return render(request,'products/index8.html', context) #отображение шаблона с данными

def update_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('number_id')
        room_type = request.POST.get('room_type')
        number_of_beds = request.POST.get('number_of_beds')
        price = request.POST.get('price')

        room = get_object_or_404(hotel_number, id=room_id)
        
        # Получаем объект characteristics через характеристику hotel_number
        room_characteristics = room.characteristics_id
        
        # Обновляем характеристики
        room_characteristics.type = room_type
        room_characteristics.number_of_beds = number_of_beds
        room_characteristics.price = price
        room_characteristics.save()  # Не забудьте сохранить изменения характеристик

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def delete_number(request, number_id):
    if request.method == 'DELETE':
        try:
            number = hotel_number.objects.get(id=number_id)
            number.delete()
            return JsonResponse({'message': 'Номер успешно удален.'}, status=200)
        except hotel_number.DoesNotExist:
            return JsonResponse({'error': 'Номер не найден.'}, status=404)
    return JsonResponse({'error': 'Неверный метод.'}, status=400)

def add_number(request):
    return render(request, 'products/index9.html')

@csrf_exempt  # Используйте это только если у вас есть проблемы с CSRF
def add_hotel_number(request):
    if request.method == 'POST':
        # Получаем данные из запроса
        room_type = request.POST.get('room_type')
        price = request.POST.get('price')
        number_of_beds = request.POST.get('number_of_beds')
        floor = request.POST.get('floor')
        number_of_rooms = request.POST.get('number_of_rooms')
        image = request.FILES.get('image')

        # Создаем объект characteristics
        char = characteristics(
            type=room_type,
            price=price,
            number_of_beds=number_of_beds,
            floor=floor,
            number_of_rooms=number_of_rooms
        )
        char.save()  # Сохраняем объект characteristics в базе данных

        # Создаем объект hotel_number, используя только что созданный characteristics
        hotel_num = hotel_number(
            image=image,
            characteristics_id=char  # Указываем внешний ключ на characteristics
        )
        hotel_num.save()  # Сохраняем объект hotel_number в базе данных

        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)