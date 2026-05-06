# Suspiria Website

Официальный сайт альт-метал группы Suspiria из Липецка.
Размещён через GitHub Pages.

## 🚀 Функционал

* 🎵 Встроенный аудиоплеер с кнопкой play/stop
* 📰 Блог с постами (текст, картинка, автор, дата)
* 🔍 Фильтрация постов блога по автору и диапазону дат
* 📝 Гостевая книга / форма обратной связи (Formspree)
* 🎸 Страницы: о группе, участники, дискография, концерты, контакты
* 📱 Адаптивная вёрстка — сайдбар скрывается под кнопку на мобилке

## 🛠️ Технологии

* HTML5 / CSS3
* JavaScript (vanilla)
* Python + Tkinter — десктопный редактор блога (`blog_editor.py`)
* Formspree — обработка формы обратной связи

## 📰 Блог-редактор

`blog_editor.py` — Python/Tkinter приложение для управления блогом:

* Создание постов (автор, дата, текст, картинка)
* Удаление постов
* Git push прямо из интерфейса

Запуск: `python blog_editor.py`

## 📦 Структура проекта

```
/index.html
/pages/
  blog.html
/assets/
  /images/
    /blog/
  /gif/
  /audio/
/css/
  style.css
/js/
  player.js
  form.js
  sidebar.js
  blog-filter.js
/blog_editor.py
```

## 🌐 Деплой

Сайт хостится через GitHub Pages.
