# Боты-викторины для Telegram и VK

Поболтать с ботом можно в [чате в VK](https://vk.com/club216618579) или в [телеграме](https://t.me/echoquiz_bot)

## Как установить

**Важно!** Предварительно должен быть установлен python версии не выше 3.9.x.

Скачайте код:
```sh
git clone git@github.com:danceandfight/historyquiz.git
```

Перейдите в каталог проекта:
```sh
cd historyquiz
```
Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии. 

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`

Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Зарегестрируйте нового бота с помощью `@BotFather` в телеграме. Вам потребуется его токен, который выдаст `@BotFather` после регистрации.

Создайте новую группу в [VK](vk.com) и получите токен группы в меню `Настройки/Работа с API`.

Зарегестрируйтесь и создайте новую базу данных [Redis](https://redis.io). Вам потребуются `host`, `port` и `password`.

Создайте файл `.env` в каталоге `historyquiz/` и положите туда код такого вида, заменив токены на свои:
```sh
TELEGRAM_BOT_TOKEN=1234546789:ASFGRrogjRHrtweog-bRTHrhwmniireeoWW
VK_TOKEN='vk1.a.qokPsGegrJtr...'
REDIS_HOST='redis-18012.c293.eu-central-1-1.ec2.cloud.redislabs.com'
REDIS_PORT=18012
REDIS_PASSWORD='zMdDfsw243t0gkrsdmw32s0m03cmsamV'
```

## Как пользоваться

Функция `get_quiz_questions` позволяет выбирать из какого файла будут использоваться вопросы, для этого, пока что, используются индексы списка.

Запустите telegram бота:

```sh
python tg_bot.py
```
Начните беседу, вызвав комманду `/start`

Запустите vk бота:
```sh
python vk_bot.py
```
Поприветствуйте его командой `Привет!`

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).