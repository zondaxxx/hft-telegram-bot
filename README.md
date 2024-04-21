# HFT Bot - один из лучших и простейших ботов для создания тестов ученикам.
Этот бот разработан специально для образовательных целей, позволяя учителям создавать тесты и викторины для своих учеников в увлекательной и интерактивной форме. Используя возможности aiogram, фреймворка на Python для разработки Telegram-ботов, мы создали многофункциональную платформу для улучшения процесса обучения.
## Преимущества и фичи
* Вовлекайте своих учеников в интерактивные тесты и викторины
*  Получайте мгновенную обратную связь об успеваемости учащихся, чтобы отслеживать прогресс.
* Интуитивно понятный дизайн обеспечивает плавную навигацию и удобство использования.
* Легко управляйте тестами, просматривайте результаты и анализируйте данные c помощью панели мониторинга 
 > [!IMPORTANT]
 >  Установка бота по умолчанию сделана для корневой папки сервера на Linux. В случае запуска на Windows вам следует поменять директорию сохранения файлов в `test_input_output.py`
## Установка бота.
> [!TIP]
> Для запуска бота требуется создать **.env** файл и прописать в нем условие ```BOT_TOKEN = *ВАШ ТОКЕН*```

> [!CAUTION]
> Данная установка прописана только для Linux.
### 1. Импортируйте проект.
```
cd / (или любую директорию, как вам удобно)
git clone https://github.com/zondaxxx/hft-telegram-bot/
```
### 2. Установите библиотеки: (и Python)
```
pip install aiogram
pip install openpyxl
pip install aiosqlite
pip install pydantic
pip install pydantic-settings
pip install asyncio
```
### 3. Создайте бота в [BotFather](https://t.me/BotFather)
На этом шаге вам нужно вставить токен бота в .env который вы создали

### 4. Запустите бота
```
python3 bot.py
```


### Деплой бота на Linux-сервера
Для того чтобы запустить бота на сервере и закрыть консоль вам нужно прописать данные команды:
> [!CAUTION]
> Деплой бота в данном случае представлен для серверов на Ubuntu. В зависимости от вашей системы пакетный загрузчик может различаться
```
sudo apt install screen
```
```
screen
```
После активации вам нужно войти в нужную директорию
```
cd /path/to/the/bot
```
Далее запуск бота
```
python3 bot.py
```
После этого нужно прожать два сочетания клавиш: Ctrl + A, Ctrl + D (Строго по очереди)
Профит!
# Создано Zondaxxx
https://t.me/elemantery_bot - Тестовый бот, работает.
