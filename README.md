# CryptoBot
Бот для отображения цен на криптовалюты в рублях

Реализована логика ответов по кнопкам

Реализована логика управления кнопками через панель администратора

Подключена БД SqLite3

<b>Для уставноки требуется:</b>

1) Скачать архив
2) Иметь Python на компьютере, бот был написан на последней на данный момент версии (11.1)
3) Создать новую папку и распаковать в неё архив
4) Открыть Cmd
5) С помощью команды cd путь перейти в папку с распакованными файлами
6) Прописать команду Python -m venv venv
7) Прописать venv\Scripts\activate (Должна появиться лычка (venv) перед командной строкой)
8) Установить зависимости проекта с помощью pip install -r requirements.txt
9) Прописать свои данные (Token и id администратора) в файле config.py
10) Запустить бота с помощью Python main.py

После запуска БД будет пустая и кнопки не появятся, для того чтобы выставить стандартные настройки
нужно прописать /admin и нажать кнопку /stock