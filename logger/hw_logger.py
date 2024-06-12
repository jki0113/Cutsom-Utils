import os
import time
import psutil
from threading import Thread




def manage_log_size(log_file, max_lines=3000):
    """log가 최근 max_lines 까지만 작성되게 해주는 함수"""
    with open(log_file, 'r') as file:
        lines = file.readlines()

    if len(lines) > max_lines:
        with open(log_file, 'w') as file:
            file.writelines(lines[-max_lines:])


def write_hw_log():
    """특정 시간마다 HARDWARE_LOGGER_PATH에 로깅"""
    log_path = os.path.join(os.getenv('HARDWARE_LOGGER_PATH'), 'hw.log')
    with open(log_path, 'a') as hw_file:
        while True:
            cpu_percent = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            hw_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] | CPU: {cpu_percent}% | RAM: {ram}% | HDD: {disk}%\n")
            hw_file.flush()
            manage_log_size(log_path)
            time.sleep(30)

def start_hw_logger():
    thread = Thread(target=write_hw_log, daemon=True)
    thread.start()


if __name__ == "__main__":
    write_hw_log()
