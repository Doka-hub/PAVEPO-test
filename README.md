Тестовое задание для PAVEPO
==============================
### Задание

Реализовать сервис по загрузке аудио-файлов от пользователей, используя FastAPI, SQLAlchemy и Docker. Пользователи могут давать файлам имя в самом API.
Авторизацию пользователей реализовать через Яндекс.
Файлы хранить локально, хранилище использовать не нужно.
Использовать асинхронный код.
БД - PostgreSQL 16.


Ожидаемый результат:
1. Готовое API с возможностью авторизации через Яндекс с последующей аутентификацией к запросам через внутренние токены API.
Доступные эндпоинты:
   - авторизация через яндекс
   - обновление внутреннего access_token;
   - получение, изменение данных пользователя,
   - удаление пользователя от имени суперпользователя;
   - получение информации о аудио файлах пользователя: название файлов и путь в локальном хранилище.
2. Документация по развертыванию сервиса и БД в Docker.

Все коммиты вести от самого начала разработки. Код разместить в GitHub в открытом репозитории / дать доступ в приватный.

### Quickstart
Зарегистрировать яндекс приложение можно тут - https://oauth.yandex.ru/client/new/id

Callback URL - `https://your_domain.com/api/v1/auth/yandex`, затем скопировать `YANDEX_CLIENT_ID` и `YANDEX_CLIENT_SECRET` в `.env` файл

1. Скопировать `dists/.env.dist` в `.env` и заменить значения переменных на свои
2. Скопировать `dists/db.env.dist` в `db.env` и заменить значения переменных на свои
3. Запуск через докер
```bash
docker compose up --build -d
```

### Примечание
Так как для аутентификации через яндекс необходимо яндекс приложение (https://oauth.yandex.ru/client/new/id), для локального теста вы можете использовать ngrok:
```bash 
ngrok http 8000
```
Ссылку нужно вставить в приложение яндекса в качестве callback url.
URL для авторизации: `https://url_from_ngrok/api/v1/auth/yandex`
