# Yatube API

REST API для социальной сети **Yatube**, где пользователи могут публиковать посты, объединяться в группы и оставлять комментарии.

Проект реализован на **Django REST Framework** в рамках учебного спринта.

## 🚀 Функциональность

* Аутентификация по токену
* Публикация постов
* Комментирование постов
* Просмотр информации о группах
* Ограничения доступа: изменения — только для авторов, остальным доступно только чтение

## 📦 Установка и запуск

```bash
# Клонируйте репозиторий
https://github.com/<your-username>/api_yatube.git
cd api_yatube

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt

# Выполните миграции
python manage.py migrate

# Запустите сервер
python manage.py runserver
```

## 🔐 Аутентификация

Получите токен:

```http
POST /api/v1/api-token-auth/
{
  "username": "your_username",
  "password": "your_password"
}
```

В ответе вы получите токен:

```json
{
  "token": "your_token"
}
```

Используйте его в заголовке `Authorization: Token your_token` для всех запросов.

## 🔧 Основные эндпоинты

| Метод                   | URL                                              | Описание                                     |
| ----------------------- | ------------------------------------------------ | -------------------------------------------- |
| POST                    | /api/v1/api-token-auth/                          | Получение токена                             |
| GET, POST               | /api/v1/posts/                                   | Список постов / создание поста               |
| GET, PUT, PATCH, DELETE | /api/v1/posts/{post\_id}/                        | Получение / изменение / удаление поста       |
| GET                     | /api/v1/groups/                                  | Список групп                                 |
| GET                     | /api/v1/groups/{group\_id}/                      | Информация о группе                          |
| GET, POST               | /api/v1/posts/{post\_id}/comments/               | Комментарии к посту / добавление комментария |
| GET, PUT, PATCH, DELETE | /api/v1/posts/{post\_id}/comments/{comment\_id}/ | Работа с конкретным комментарием             |

## 📌 Примеры запросов

**Создание поста:**

```http
POST /api/v1/posts/
Authorization: Token your_token

{
  "text": "Новый пост в Yatube",
  "group": 1
}
```

**Создание комментария:**

```http
POST /api/v1/posts/14/comments/
Authorization: Token your_token

{
  "text": "Отличный пост!"
}
```

**Получение информации о группе:**

```http
GET /api/v1/groups/2/
```

## 🛠 Технологии

* Python 3.10+
* Django 4.x
* Django REST Framework
* TokenAuthentication

## 🧪 Тестирование

Для удобства тестирования можно использовать Postman. В папке `postman_collection` находится коллекция с готовыми запросами.

## 📄 Лицензия

Проект создан в учебных целях. Все права принадлежат автору.
