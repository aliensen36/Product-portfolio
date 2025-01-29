# Product & Project Management Service

Этот проект предоставляет REST API для управления продуктами и проектами, связанными с ними. Это часть личного кабинета Кловери.  

## 📋 Функциональность

- **Управление продуктами**: создание, просмотр, обновление и удаление продуктов.
- **Управление проектами**: создание, просмотр, обновление и удаление проектов, связанных с продуктами.
- **Отображение проектов, связанных с продуктами**.

---

## 🛠️ Установка и запуск проекта

### Шаг 1: Клонируйте репозиторий
```bash

# Clone with SSH
git clone git@git.cloveri.com:cloveri.start/start/product-portfolio.git

# Clone with HTTPS
git clone https://git.infra.cloveri.com/cloveri.start/start/product-portfolio.git
```

### Шаг 2: Создайте виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows
```

### Шаг 3: Установите зависимости
```bash
pip install -r requirements.txt # Установка из файла
python -m pip freeze > requirements.txt # Обновление списка зависимостей
```

### Шаг 4: Примените миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### Шаг 5: Создайте суперпользователя
```bash
python manage.py createsuperuser
```

### Шаг 6: Запустите сервер разработки
```bash
python manage.py runserver
```
Адрес сервера: http://127.0.0.1:8000/  
Администартивная панель: http://127.0.0.1:8000/admin

### 🔗 Эндпоинты API

#### Продукты
| Метод   | URL                     | Описание                       |
|---------|-------------------------|--------------------------------|
| `GET`   | `/api/products/`        | Получить список продуктов      |
| `POST`  | `/api/products/`        | Создать новый продукт          |
| `GET`   | `/api/products/{id}/`   | Получить продукт по ID         |
| `PUT`   | `/api/products/{id}/`   | Обновить продукт по ID         |
| `DELETE`| `/api/products/{id}/`   | Удалить продукт по ID          |

#### Проекты
| Метод   | URL                     | Описание                       |
|---------|-------------------------|--------------------------------|
| `GET`   | `/api/projects/`        | Получить список проектов       |
| `POST`  | `/api/projects/`        | Создать новый проект           |
| `GET`   | `/api/projects/{id}/`   | Получить проект по ID          |
| `PUT`   | `/api/projects/{id}/`   | Обновить проект по ID          |
| `DELETE`| `/api/projects/{id}/`   | Удалить проект по ID           |

### 🛠️ Технологии

- **Backend**: Django, Django REST Framework  
- **База данных**: SQLite (по умолчанию, можно заменить на PostgreSQL)  
- **Язык программирования**: Python 3.9+  
- **Контейнеризация**: Docker
- **Документация API**: OpenAPI  


### 📄 Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в LICENSE.

### 📧 Контакты
Если у вас есть вопросы или предложения, вы можете связаться с разработчиками:

Email: 
GitHub:
