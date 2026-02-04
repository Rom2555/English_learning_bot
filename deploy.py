"""Deploy script for English Learning Bot to VPS"""

import os
import sys
import paramiko
import time

# VPS credentials
HOST = "193.124.254.120"
PORT = 22
USERNAME = "root"
PASSWORD = "W4nZj0PBgBPQnWg"
REMOTE_DIR = "/root/english_bot"
LOCAL_DIR = r"C:\Users\furer\Documents\English_learning_bot"


def upload_directory(sftp, local_path, remote_path):
    """Upload directory recursively"""
    os.makedirs(local_path, exist_ok=True)
    for item in os.listdir(local_path):
        local_item = os.path.join(local_path, item)
        remote_item = os.path.join(remote_path, item)
        if os.path.isfile(local_item):
            print(f"Uploading {local_item} -> {remote_item}")
            sftp.put(local_item, remote_item)
        elif os.path.isdir(local_item):
            try:
                sftp.mkdir(remote_item)
            except:
                pass
            upload_directory(sftp, local_item, remote_item)


def run_command(ssh, command, timeout=120):
    """Execute command on remote server"""
    print(f"Executing: {command}")
    stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(output)
    if error:
        print(f"ERROR: {error}")
    return output, error


def main():
    # Get token from command line or .env
    TELEGRAM_TOKEN = None

    if len(sys.argv) > 1:
        TELEGRAM_TOKEN = sys.argv[1]
    else:
        # Try to get from local .env
        env_path = os.path.join(LOCAL_DIR, ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("TOKEN="):
                        TELEGRAM_TOKEN = line.split("=", 1)[1].strip()
                        break

    if not TELEGRAM_TOKEN:
        print("Telegram Token не найден!")
        print("Использование: python deploy.py <TOKEN>")
        print("Или создайте .env файл с TOKEN=ваш_токен")
        return

    print(f"Подключение к {HOST}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)
        print("Подключено!")

        sftp = ssh.open_sftp()

        # Create remote directory
        try:
            sftp.mkdir(REMOTE_DIR)
        except:
            pass

        # Upload files
        print("\nЗагрузка файлов...")
        for item in os.listdir(LOCAL_DIR):
            local_item = os.path.join(LOCAL_DIR, item)
            remote_item = os.path.join(REMOTE_DIR, item)
            # Skip .env file - we'll create it on server
            if item == '.env':
                continue
            if os.path.isfile(local_item):
                print(f"  {item}")
                sftp.put(local_item, remote_item)
            elif os.path.isdir(local_item):
                try:
                    sftp.mkdir(remote_item)
                except:
                    pass
                upload_directory(sftp, local_item, remote_item)

        sftp.close()

        # Create .env file on server
        print("\nСоздание .env файла...")
        env_content = f"TOKEN={TELEGRAM_TOKEN}\n"
        stdin, stdout, stderr = ssh.exec_command(f"echo '{env_content}' > {REMOTE_DIR}/.env")
        time.sleep(1)

        # Install Docker Compose if needed
        print("\nПроверка docker-compose...")
        output, _ = run_command(ssh, "which docker-compose")
        if not output.strip():
            print("Установка docker-compose...")
            run_command(ssh, "apt update")
            run_command(ssh, "apt install -y docker-compose")
        else:
            print("docker-compose уже установлен")

        # Build and run
        print("\nСборка и запуск бота...")
        run_command(ssh, f"cd {REMOTE_DIR} && docker-compose down 2>/dev/null || true")
        run_command(ssh, f"cd {REMOTE_DIR} && docker-compose up -d --build", timeout=300)

        print("\n" + "="*50)
        print("Готово! Бот запущен.")
        print("Просмотр логов: docker-compose logs -f")
        print("="*50)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        ssh.close()


if __name__ == "__main__":
    main()
