# Блог на джанго с симуляцией жизни

Блог реализованный на джанго.

### Установка

```commandline
pip install -r requirements.txt
```

### Запуск
- перейти в директорию приложения
- активировать виртуальное окружение
- запустить приложение

### Функция симуляции жизни
Имя и Фамилия генерируются с помощью 'https://randomuser.me/api/'.
На их основании генерируются Имя пользователя и электронная почта.
Изображение профиля генерируется на сайте 'https://picsum.photos/'

Логика постов в данный момент: описание случайных youtube видео из топ 10 различных стран.
Логика комментариев в данный момент: случайный из первых 20 комментариев к выбранному видео.
Вся информация для постов и комментариев получена с помощью YouTube Data API.

#### Запуск симуляции
Вариант 1:
- авторизоваться под профилем администратора
- перейти по ссылке 127.0.0.1:8000/blog_life/' 
- выставить необходимые параметры
- запустить (кнопка 'GO')
- завершить при необходимости (кнопка 'STOP')

Вариант 2:
- находясь в виртуальном окружении, написать в консоль команду
```
python manage.py loadlife <seconds> <user_enable> <post_enable> <comment_enable> <like_save_enable> <sub_enable> <user_weight> <post_weight> <comment_weight> <like_save_weight> <sub_weight>
```

<<fix>seconds> - время между итерациями,

<..._enable> - включить или выключить параметр (значения 1 или 0 соответственно)

<..._weight> - удельный вес параметра

---
  
### Urls
| URL                                 | описание                                                   |
|:------------------------------------|:-----------------------------------------------------------|
| admin/                              | панель администратора                                      |
| /                                   | страница с новостями от всех пользователей                 |
| <post_id>/                          | детальная страница новости                                 |
| create/                             | создать новость                                            |
| <post_id>/edit/                     | редактировать новость                                      |
| <post_id>/delete/                   | удалить новость                                            |
| <comment_id>/comment_delete/        | удалить комментарий                                        |
| need_moderation/                    | новости на которые пожаловались                            |
| contacts/                           | контакты                                                   |
| about/                              | информация о сайте                                         |
| custom_news/?format=<yaml/json/xml> | получить список новостей в желаемом формате                |
| -                                   | -                                                          |
| blog/<profile_id>/                  | блог пользователя                                          |
| blog/bookmarks/                     | сохранённые посты                                          |
| blog/subscriptions/                 | страница с постами от ваших подписок                       |
| blog/subscriptions_list/            | список подписок                                            |
| blog/subscribers_list/<profile_id>/ | список подписчиков                                         |
| -                                   | -                                                          |
| users/<profile_id>                  | просмотр профиля                                           |
| users/<profile_id>/edit/            | редактирование профиля                                     |
| users/login/                        | логин                                                      |
| users/register/                     | регистрация                                                |
| -                                   | -                                                          |
| api/...                             | api для users, profiles, posts, comments, images           |
| api/.../<item_id>/                  | детальные api для users, profiles, posts, comments, images |
| -                                   | -                                                          |
| blog_life/                          | настройки и запуск симуляции жизни в блоге                 |
| -                                   | -                                                          |
| rss/latest/feed/                    | получение списка новостей                                  |
| sitemap.xml                         | получение карты сайта                                      |
| swagger/                            | спецификации API и их методов                              |
----------------------------------------------------------------------------------------------------

### Предстоящие задачи:

- дописать тесты
- логирование
- теги для постов
- логика ботов
- поиск по api
- права доступа в api
- переработать отображение изображений в постах
- удалить лишние пакеты
- сделать раздел модерации
