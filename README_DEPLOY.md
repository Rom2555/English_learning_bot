# Развертывание на VPS

## ⚠️ ВАЖНО: Безопасность

Никогда не коммитите учетные данные в Git! Все чувствительные данные должны храниться в переменных окружения.

## Настройка SSH-ключей (рекомендуется)

Использование SSH-ключей безопаснее, чем пароли.

### 1. Генерация SSH-ключа на локальной машине

```bash
# Windows (Git Bash или PowerShell)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Linux/Mac
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

### 2. Копирование публичного ключа на VPS

```bash
# Windows (Git Bash)
type C:\Users\ваше_имя\.ssh\id_rsa.pub | ssh root@ваш_ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Linux/Mac
ssh-copy-id root@ваш_ip
```

### 3. Отключение входа по паролю на VPS (опционально)

```bash
# Подключитесь к VPS
ssh root@ваш_ip

# Отредактируйте конфиг
nano /etc/ssh/sshd_config

# Измените:
PasswordAuthentication no

# Перезапустите SSH
systemctl restart sshd
```

## Методы деплоя

### Метод 1: Автоматический деплой через скрипт

#### Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
# Токен бота
TOKEN=ваш_токен_от_BotFather

# Настройки VPS
VPS_HOST=193.124.254.120
VPS_PORT=22
VPS_USER=root
VPS_PASSWORD=ваш_пароль
# или используйте SSH-ключ:
# VPS_KEY_PATH=C:\Users\ваше_имя\.ssh\id_rsa
VPS_REMOTE_DIR=/root/english_bot
```

#### Запуск деплоя

```bash
# Windows
python deploy.py

# Linux/Mac
python3 deploy.py
```

### Метод 2: Ручной деплой через Docker

#### 1. Подключение к VPS

```bash
ssh root@193.124.254.120
```

#### 2. Установка Docker и Docker Compose

```bash
apt update
apt install -y docker docker-compose
```

#### 3. Создание директории проекта

```bash
mkdir -p /root/english_bot
cd /root/english_bot
```

#### 4. Загрузка файлов

**С локальной машины:**
```bash
scp -r English_learning_bot/* root@193.124.254.120:/root/english_bot/
```

**Или клонирование из Git:**
```bash
git clone https://github.com/Rom2555/English_learning_bot.git .
```

#### 5. Создание .env файла

```bash
echo "TOKEN=ваш_токен" > .env
```

#### 6. Запуск бота

```bash
docker-compose up -d --build
```

#### 7. Просмотр логов

```bash
docker-compose logs -f
```

#### 8. Управление ботом

```bash
# Остановка
docker-compose stop

# Запуск
docker-compose start

# Перезапуск
docker-compose restart

# Удаление контейнеров
docker-compose down
```

### Метод 3: Запуск без Docker

#### 1. Подключение к VPS

```bash
ssh root@193.124.254.120
```

#### 2. Установка Python и зависимостей

```bash
apt update
apt install -y python3 python3-pip
```

#### 3. Создание директории и загрузка файлов

```bash
mkdir -p /root/english_bot
cd /root/english_bot
# Загрузите файлы проекта
```

#### 4. Создание виртуального окружения

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 5. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### 6. Создание .env файла

```bash
echo "TOKEN=ваш_токен" > .env
```

#### 7. Запуск бота

```bash
python main.py
```

#### 8. Запуск в фоне (с systemd)

Создайте файл сервиса `/etc/systemd/system/english-bot.service`:

```ini
[Unit]
Description=English Learning Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/english_bot
Environment="PATH=/root/english_bot/.venv/bin"
ExecStart=/root/english_bot/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Активируйте сервис:

```bash
systemctl daemon-reload
systemctl enable english-bot
systemctl start english-bot
systemctl status english-bot
```

## Мониторинг и логи

### Docker

```bash
# Просмотр логов
docker-compose logs -f

# Просмотр логов за последние 100 строк
docker-compose logs --tail=100

# Просмотр статуса контейнеров
docker-compose ps
```

### Systemd

```bash
# Просмотр логов
journalctl -u english-bot -f

# Просмотр статуса
systemctl status english-bot
```

## Обновление бота

### Docker

```bash
cd /root/english_bot
git pull  # или загрузите новые файлы
docker-compose down
docker-compose up -d --build
```

### Systemd

```bash
cd /root/english_bot
git pull  # или загрузите новые файлы
systemctl restart english-bot
```

## Резервное копирование базы данных

```bash
# Копирование базы данных с VPS
scp root@193.124.254.120:/root/english_bot/english_bot.db ./backup.db

# Автоматическое резервное копирование (cron)
# Добавьте в crontab:
# 0 3 * * * cp /root/english_bot/english_bot.db /root/english_bot/backup/english_bot_$(date +\%Y\%m\%d).db
```

## Решение проблем

### Бот не запускается

1. Проверьте логи: `docker-compose logs -f`
2. Убедитесь, что токен правильный
3. Проверьте, что порт не занят

### Ошибка подключения к VPS

1. Проверьте IP адрес и порт
2. Убедитесь, что SSH сервис запущен на VPS
3. Проверьте firewall настройки

### Проблемы с Docker

```bash
# Очистка Docker
docker system prune -a

# Переустановка Docker
apt remove docker docker-compose
apt install -y docker docker-compose
```
