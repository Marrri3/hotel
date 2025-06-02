document.querySelector('.add-btn').addEventListener('click', function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение кнопки

    const imageUpload = document.getElementById('image_upload').files[0];
    const roomType = document.getElementById('room_type').value;
    let price = document.getElementById('price').value;
    const numberOfBeds = document.getElementById('number_of_beds').value;
    const floor = document.getElementById('floor').value;
    const numberOfRooms = document.getElementById('number_of_rooms').value;

    // Замена запятой на точку
    price = price.replace(',', '.');

    // Проверка заполненности всех обязательных полей
    if (!imageUpload || !roomType || !price || !numberOfBeds || !floor || !numberOfRooms) {
        alert('Пожалуйста, заполните поля корректно');
        return; // Остановка выполнения, если есть пустые поля
    }

    // Валидация полей
    if (!validateData(price, numberOfBeds)) {
        return; // Остановка выполнения, если данные невалидные
    }

    const formData = new FormData();
    formData.append('image', imageUpload);
    formData.append('room_type', roomType);
    formData.append('price', price);
    formData.append('number_of_beds', numberOfBeds);
    formData.append('floor', floor);
    formData.append('number_of_rooms', numberOfRooms);

    fetch('/add/', { // Убедитесь, что этот URL соответствует вашему маршруту на сервере
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Получаем CSRF-токен
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            alert('Номер успешно добавлен.');
            window.location.href = '/FOURSEASON/catalog'; // Перенаправление на каталог
        } else {
            alert('Ошибка при добавлении номера.');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});

function validateData(price, numberOfBeds) {
    const priceField = document.getElementById('price');
    const bedsField = document.getElementById('number_of_beds');

    // Замена запятой на точку
    price = price.replace(',', '.');

    // Проверка на пустое значение
    if (!price) {
        priceField.setCustomValidity('Поле цены не должно быть пустым');
        priceField.reportValidity();
        return false;
    }

    // Валидация поля "Цена"
    if (!/^\d+([.,]\d+)?$/.test(price)) {
        priceField.setCustomValidity('Введите корректное число для цены');
        priceField.reportValidity();
        return false;
    } else {
        priceField.setCustomValidity(''); // Сбросить сообщение об ошибке
    }

    // Валидация поля "Количество кроватей"
    const numberOfBedsValue = parseInt(numberOfBeds);
    if (isNaN(numberOfBedsValue) || numberOfBedsValue < 1 || numberOfBedsValue > 3) {
        bedsField.setCustomValidity('Количество кроватей должно быть от 1 до 3');
        bedsField.reportValidity();
        return false;
    } else {
        bedsField.setCustomValidity(''); // Сбросить сообщение об ошибке
    }

    return true; // Валидация прошла успешно
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, начинается ли cookie с нужного имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Обработчик для поля ввода "Цена"
document.getElementById('price').addEventListener('input', function() {
    const normalizedValue = this.value.replace(',', '.');
    this.value = normalizedValue; // Обновляем значение с точкой
});

// Обработчик для поля ввода "Количество кроватей"
document.getElementById('number_of_beds').addEventListener('input', function() {
    validateData(document.getElementById('price').value.replace(',', '.'), this.value);
});

// Валидация при потере фокуса
document.getElementById('price').addEventListener('blur', function() {
    validateData(this.value.replace(',', '.'), document.getElementById('number_of_beds').value);
});