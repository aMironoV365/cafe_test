# Test Project Django

Проект что-то типо удаленных заказов, когда сидишь за столиком в маке и тд

## 🚀 Возможности

- Управление заказами через базовый фронт(удаление, создание, изменения и просмотр)
- Работа с меню через DRF


## Технологии

- Python 3.12.8
- pytest 8.3.5
- Django 5.1.7
- DRF 3.15.2
- redis 5.2.1
## ⚙️ Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/aMironoV365/cafe_test.git
   cd cafe_test
   ```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## 🚀 Запуск(настоятельно рекомендую запуск через 🐳Docker)

1. Запуск сервера:

```bash
docker-compose up --build
```

2. Сервис будет доступен по адресу:
```bash
http://localhost:8000
```

## 📊 API Endpoints

- api/products - Информация об апи, доступно создание, удаление, редактирование и просмотр продуктов из меню

## 📊 Endpoints

- orders/create/ - Создание заказа
- orders/list/ - Просмотр списка заказов
- orders/<int:pk> - Просмотр заказа по его ID
- orders/<int:pk>/update - Редактирование заказа по его ID
- orders/<int:pk>/delete - Архивация заказа по его ID

## 🧪 Тестирование

1. Тестирование API:
```bash
pytest
```

2. Тестирование Заказов:
```bash
python manage.py test orders
```

Тесты включают:

- Тестирование эндпоинтов API
- Проверку работы с базой данных
- Тестирование всех view представлений