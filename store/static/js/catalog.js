function validatePrice() {
    const input = document.getElementById('price');
    const value = input.value;

    const normalizedValue = value.replace(',', '.');
    if (!/^\d*\.?\d*$/.test(normalizedValue)) {
        input.setCustomValidity('Введите корректное число');
    } else {
        input.setCustomValidity('');
    }
    
    input.value = normalizedValue;
}

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('changeModal');
    const close = document.querySelector('.close');
    const numberElement = document.getElementById('number_id');

    document.querySelectorAll('.open-modal').forEach(button => {
        button.addEventListener('click', function() {
            const numberId = this.getAttribute('data-id');
            const priceElement = document.getElementById('price_' + numberId);
            
            const roomType = document.getElementById('roomType_' + numberId).textContent;
            const price = priceElement.textContent;
            const numberOfBeds = document.getElementById('numberOfBeds_' + numberId).textContent;
            const floor = document.getElementById('floor_' + numberId).textContent;
            const numberOfRooms = document.getElementById('numberOfRooms_' + numberId).textContent;

            document.getElementById('number_id').value = numberId;
            document.getElementById('room_type').value = roomType;
            document.getElementById('price').value = price;
            document.getElementById('number_of_beds').value = numberOfBeds;
            document.getElementById('floor').value = floor;
            document.getElementById('number_of_rooms').value = numberOfRooms;

            modal.style.display = 'block';
        });
    });

    close.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    // Обработчик отправки формы
    document.getElementById('changeForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // предотвращает стандартное поведение формы

        // Отправка данных формы через Fetch API
        const formData = new FormData(this);
        
        const response = await fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // чтобы сервер мог распознать AJAX запрос
            }
        });

        if (response.ok) {
            alert('Изменения успешно сохранены.');
            // Закрытие модального окна
            modal.style.display = 'none';
            // Перезагрузка страницы
            location.reload();
        } else {
            // Обработка ошибки
            lert('Ошибка при сохранении изменений.');
            const errorData = await response.json();
            console.error('Ошибка:', errorData);
        }
    });


    // Обработчик отправки формы с нормализацией цены
    document.getElementById('changeForm').addEventListener('submit', function(event) {
        const input = document.getElementById('price');
        const finalPrice = input.value.replace(',', '.'); // Заменяем запятую на точку
        input.value = finalPrice; // Устанавливаем нормализованное значение обратно
    });
});

document.getElementById('bookingForm').addEventListener('submit', function(event) {
    const checkinDate = new Date(document.getElementById('checkin').value);
    const checkoutDate = new Date(document.getElementById('checkout').value);
    const today = new Date();

    // Устанавливаем время на полночь для корректного сравнения
    today.setHours(0, 0, 0, 0);

    // Проверяем, что даты не в прошлом и что дата выезда больше даты заезда
    if (checkinDate < today) {
        alert('Дата заезда не может быть в прошлом.');
        event.preventDefault(); // Отменяем отправку формы
    } else if (checkoutDate <= checkinDate) {
        alert('Дата выезда должна быть позже даты заезда.');
        event.preventDefault(); // Отменяем отправку формы
    }
});

