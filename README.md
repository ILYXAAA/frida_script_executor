# Frida Script Executor


![GitHub last commit](https://img.shields.io/github/last-commit/ILYXAAA/frida_script_executor)
<h1 align="left"><img src="https://codeshare.frida.re/static/images/logo.png" width="150px">
</h1>

> Данный проект представляет собой инструмент для автоматизированного запуска Frida-скриптов на устройствах, работающих на операционной системе Android. Используется фреймворк Frida для проведения анализа и взаимодействия с приложениями на уровне исполнения. Проект создан для удобства использования фреймворка Frida, позволяет не запоминать синтаксис и команды фреймворка.

---

## :boom:Возможности:

- Автоматизированная передача (push) frida-server файлов и сертификата BurpSuite, поднятие сервера на устройстве
- Запуск JS Frida-скриптов для динамического анализа мобильных приложений.

<h1 align="left"><img src="https://github.com/ILYXAAA/frida_script_executor/assets/107761814/2924bb68-1912-4af3-b891-eded0cdf59ac" width="400px">

## :memo: Требования:

- Python 3.x
- Устройство/эмулятор под ОС Android, с root и включенным режимом отладки.

## :cd: Установка и запуск:

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/ILYXAAA/frida_script_executor.git
    ```

2. Установите необходимые библиотеки:

    ```bash
    pip install -r requirements.txt
    ```

3. Запустите программу:

    ```bash
    python main.py
    ```

> [!IMPORTANT]
> Программа устанавливает соединение с устройством по адресу `127.0.0.1:21503` (Порт 21503 используется по умолчанию в эмуляторе Memu).
> При необходимости можно внести изменения в настройках:
![изображение](https://github.com/ILYXAAA/frida_script_executor/assets/107761814/393f09a6-6c20-4c05-a7b7-5e1a68735c10)

##

## Использование:

1. Подготовьте свои собственные скрипты на JavaScript для анализа приложения, либо скачайте с сайта [frida-share](https://codeshare.frida.re/).
2. Скопируйте ваши скрипты в каталог `/scripts`
3. Запустите программу.
4. Программа будет устанавливать соединение с Frida Server на устройстве с Android и загружать ваши скрипты для анализа приложения.
5. Проведите необходимые действия в приложении на устройстве, чтобы запустить анализ.
6. Наблюдайте вывод анализа в консоли, анализируйте трафик, если используете BurpSuite.


## :hourglass_flowing_sand: В планах:

- [ ] Вкладка с настройками (Более гибкая настройка программы под разные устройства).
- [ ] Расширение функциональности для обнаружения новых видов уязвимостей и потенциальных угроз.
- [ ] Улучшение пользовательского интерфейса для более удобного использования.
- [ ] Поддержка других операционных систем для анализа мобильных приложений.
