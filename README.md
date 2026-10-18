# OnlineCourse — Django exam project

Учебный Django-проект по семи требованиям с предоставленных скриншотов. Содержит курсы, уроки, админку, экзамен с несколькими правильными вариантами, проверку результатов и тесты. Интерфейс на английском, как в задании.

## Самый простой вариант на Windows

Распакуйте архив и запустите `START_WINDOWS.bat` двойным щелчком. Нужны установленный Python 3.12+ и интернет для установки пакетов. Сохраните выведенный пароль. Не закрывайте окно сервера.

Чтобы получить два снимка, при работающем сервере запустите `MAKE_SCREENSHOTS_WINDOWS.bat`. Он установит браузер для снимков и откроет папку с результатом. Альтернатива без установки на компьютер — GitHub Actions ниже.

Ваши адреса для сдачи находятся в `SUBMISSION_LINKS.txt`; имя аккаунта уже заполнено: `mimasek135`.

## Быстрый запуск на Windows

Установите Python 3.12 или новее. Откройте PowerShell в папке, где находится `manage.py`:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py runserver
```

Команда `seed_demo` выводит логин `demo_admin` и случайный пароль. Сохраните пароль: он нужен для входа на сайт и в админку. Повторный запуск не меняет существующий пароль. При необходимости задайте новый: `.\.venv\Scripts\python.exe manage.py changepassword demo_admin`.

Откройте http://127.0.0.1:8000/ — сайт; http://127.0.0.1:8000/admin/ — админка. Это локальные адреса, доступные на вашем компьютере. Публичные GitHub-ссылки относятся к исходному коду; публикация репозитория сама по себе не размещает Django-сайт в интернете.

## macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_demo
.venv/bin/python manage.py runserver
```

## Загрузка на GitHub без команд Git

1. Распакуйте архив. Создайте **Public** репозиторий `onlinecourse-project` в своём аккаунте GitHub.
2. Выберите **uploading an existing file** (либо **Add file → Upload files**).
3. Перетащите содержимое папки `onlinecourse-project`, а не сам ZIP. В корне репозитория должны быть `manage.py`, `requirements.txt`, папки `config`, `onlinecourse`, `scripts`.
4. Убедитесь, что добавлены `.github/workflows/check-and-screenshots.yml` и `.gitignore`. Скрытую папку `.github` можно добавить через Git или через **Add file → Create new file**, указав полный путь и скопировав содержимое YAML из архива.
5. Нажмите **Commit changes**. Рабочая ветка должна называться `main`; если она другая, укажите её в генераторе ссылок через `--branch`.
6. Откройте вкладку **Actions**, дождитесь успешного запуска **Check project and capture screenshots**. Если нужен повторный запуск, используйте **Run workflow**.
7. Откройте завершённый запуск и скачайте внизу **Artifacts → assignment-screenshots**. Распакуйте — получите настоящие `03-admin-site.png` и `07-final.png`.

Не загружайте `.venv`, `db.sqlite3`, пароли и файлы `__pycache__`. В исходном архиве их нет.

Вариант через Git, если он установлен (из папки проекта):

```bash
git init
git add .
git commit -m "Add Django online course exam project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/onlinecourse-project.git
git push -u origin main
```

Сначала создайте пустой репозиторий, замените `YOUR_USERNAME` на свой логин. GitHub попросит войти в аккаунт. Прямой загрузки в аккаунт из этого чата не выполнялось.

## Что сдавать

| Задание | Файл / действие |
|---|---|
| 1 | Публичная ссылка на `onlinecourse/models.py`: модели Question, Choice, Submission |
| 2 | Публичная ссылка на `onlinecourse/admin.py`: семь моделей в импорте; QuestionInline, ChoiceInline, QuestionAdmin, LessonAdmin |
| 3 | Загрузить изображение `03-admin-site.png`, показывающее разделы Authentication and Authorization и OnlineCourse |
| 4 | Публичная ссылка на `onlinecourse/templates/onlinecourse/course_details_bootstrap.html` |
| 5 | Публичная ссылка на `onlinecourse/views.py`: функции submit и show_exam_result |
| 6 | Публичная ссылка на `onlinecourse/urls.py`: пути submit и show_exam_result |
| 7 | Загрузить изображение `07-final.png`: Congratulations!, 100%, результаты вопросов |

Чтобы получить пять адресов для своего аккаунта:

```powershell
py scripts/github_links.py YOUR_USERNAME
```

Это генератор адресов: ссылки начнут работать после загрузки файлов в указанный публичный репозиторий. Для другого имени: `py scripts/github_links.py YOUR_USERNAME --repo MY_REPOSITORY`.

На GitHub также можно открыть нужный файл и скопировать адрес из браузера. Проверьте ссылку в режиме инкогнито, чтобы убедиться, что она публичная.

## Получение скриншотов на своём компьютере

Войдите в `/admin/` и сделайте снимок страницы со списком моделей. Назовите его `03-admin-site.png`.

На странице курса войдите как `demo_admin`. Для успешного примера выберите: 1 — **ForeignKey**, 2 — **urls.py**, 3 — **Use POST** и **Include a CSRF token**. Нажмите **Submit exam**, сделайте снимок с Congratulations!, оценкой и всеми результатами, назовите `07-final.png`.

Для автоматического получения снимков: оставьте сервер запущенным, откройте второй PowerShell в папке проекта:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-screenshots.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe scripts/capture_screenshots.py
```

Скрипт создаёт реальную попытку экзамена и сохраняет два PNG в `screenshots/`. Он использует существующий локальный аккаунт demo_admin и текущую базу; пароль не требуется. Запускайте этот служебный скрипт только для своей локальной учебной базы.

## Проверки

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test
```

Тесты проверяют успешную сдачу, неполные/лишние ответы, отклонение чужих вариантов, приватность результатов, POST и CSRF. В GitHub Actions эти проверки выполняются перед получением скриншотов.

В среде подготовки архива установка Django и браузера была недоступна из-за ограничений сети. Выполнена проверка синтаксиса Python; Django-тесты, миграции и снимки в этой среде не запускались. Готовых снимков в архиве нет: получите их через Actions или локально по инструкции выше.

## Как объяснить проект

- Course содержит уроки Lesson и вопросы Question; у каждого вопроса есть варианты Choice.
- Enrollment связывает пользователя и курс. Submission хранит попытку и выбранные варианты.
- GET страницы курса показывает уроки и форму. POST submit проверяет ID вариантов и записывает попытку.
- show_exam_result доступен владельцу попытки; баллы за вопрос начисляются только при точном совпадении всех выбранных и правильных вариантов. Порог сдачи — 80%.
- Для оформления подключён Bootstrap 5.3.3; локальный CSS обеспечивает базовый вид без CDN.

Настройки предназначены для локальной демонстрации. Для публичного хостинга задайте DJANGO_SECRET_KEY, DJANGO_DEBUG=0 и DJANGO_ALLOWED_HOSTS, настройте HTTPS и сбор статики.
