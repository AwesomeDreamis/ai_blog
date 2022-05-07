# Блог на джанго с симуляцией жизни

Блог реализованный на джанго.

### Установка

```commandline
pip install -r requirements.txt
```

### Запуск
- зайти в виртуальное окружение
- запустить проект
- при желании запустить симуляцию жизни перейдя по ссылке 'blog_life/' 
или находясь в виртуальном окружении, написать в консоль команду
"python manage.py loadlife <seconds> <user_on> <post_on> <comment_on> <like_save_on> <sub_on> <user_weight> <post_weight> <comment_weight> <like_save_weight> <sub_weight>"

  
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
- теги
- логика ботов
- поиск по api
- переработать отображение изображений в постах