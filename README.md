Описание программы: "Блокировщик сайтов с расписанием"
Назначение программы:
Программа предназначена для блокировки доступа к определенным сайтам на локальном компьютере. Она позволяет:

Добавлять сайты в черный список.

Блокировать доступ к этим сайтам в указанное время (по расписанию).

Управлять блокировкой вручную или автоматически.

Очищать список заблокированных сайтов и разблокировать их.

Программа использует файл hosts для перенаправления запросов к заблокированным сайтам на локальный адрес (127.0.0.1), что предотвращает доступ к ним.

Основные функции:
Добавление сайтов в черный список:

Пользователь может ввести список сайтов (по одному на строку), которые нужно заблокировать.

Сайты сохраняются в базе данных и записываются в файл websites_list.txt.

Блокировка сайтов по расписанию:

Пользователь может указать время начала и окончания блокировки.

Программа автоматически активирует блокировку в указанное время и снимает её по завершении.

Немедленная блокировка:

Пользователь может запустить блокировку вручную, без использования расписания.

Очистка списка сайтов:

Пользователь может удалить все сайты из черного списка, разблокировав их.

Данные удаляются из базы данных и файла websites_list.txt.

Защита паролем:

Программа защищена паролем. При первом запуске пользователь задает пароль, который требуется для доступа к функционалу программы.

Как работает программа:
База данных:

Используется SQLite для хранения пароля и списка сайтов.

Данные хранятся в файле app_data.db.

Файл websites_list.txt:

Содержит список сайтов, которые нужно заблокировать.

Используется для обновления файла hosts системы.

Расписание:

Программа использует библиотеку schedule для выполнения задач в указанное время.

Графический интерфейс:

Реализован с помощью библиотеки tkinter.

Пользователь может удобно управлять программой через кнопки и текстовые поля.

Преимущества программы:
Простота использования: интуитивно понятный интерфейс.

Гибкость: возможность блокировки сайтов как по расписанию, так и вручную.

Безопасность: защита паролем предотвращает несанкционированный доступ к настройкам.

Автоматизация: блокировка и разблокировка сайтов происходят автоматически по расписанию.

Пример использования:
Установка пароля:

При первом запуске программа запросит пароль, который будет использоваться для входа.

Добавление сайтов:

Введите сайты, которые нужно заблокировать, в текстовое поле (например, youtube.com, facebook.com).

Настройка расписания:

Укажите время начала и окончания блокировки (например, с 9:00 до 18:00).

Запуск блокировки:

Нажмите "Запуск по расписанию" или "Немедленный запуск".

Очистка списка:

Если нужно разблокировать все сайты, нажмите "Очистить список".

Технические требования:
Операционная система: Windows, macOS, Linux (с поддержкой Python).

Установленный Python 3.x.

Необходимые библиотеки: sqlite3, hashlib, schedule, tkinter.

Установка и запуск:
Установите Python 3.x, если он не установлен.


Установите необходимые библиотеки:
bash
pip install -r requirements.txt
Запустите программу:

Запуск
bash
main.py

Пример сценария использования:
Пользователь хочет ограничить доступ к социальным сетям в рабочее время.

Он добавляет сайты facebook.com, twitter.com, instagram.com в программу.

Устанавливает расписание блокировки с 9:00 до 18:00.

В указанное время доступ к сайтам блокируется, а после 18:00 — восстанавливается.

Заключение:
Программа "Блокировщик сайтов с расписанием" — это удобный инструмент для контроля доступа к нежелательным сайтам. Она подходит для использования как в личных целях, так и в рабочих условиях, где требуется ограничить доступ к отвлекающим ресурсам.

PS. Вместо websites_list.txt прписываем путь к hosts
