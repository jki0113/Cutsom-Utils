import os
import time
import asyncio
import logging
import colorlog
from colorama import Fore, Style
from functools import wraps
from datetime import datetime
import sys

LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL').upper()
SYSTEM_LOGGER_PATH = os.environ.get('SYSTEM_LOGGER_PATH')
SHOW_LOGGER_TIMESTEP = os.environ.get('SHOW_LOGGER_TIMESTEP').upper() == 'TRUE'
SAVE_LOGGER_FILE = os.environ.get('SAVE_LOGGER_FILE').upper() == 'TRUE'


class ColoredFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        formatted_record = super().format(record)

        lines = formatted_record.split('\n')

        timestamp = lines[0].split('|')[0].strip()
        log_level_with_color = lines[0].split('|')[1].strip()

        first_line_content = '|'.join(lines[0].split('|')[2:])[1:]

        if SHOW_LOGGER_TIMESTEP:
            # PM2로 timestep logging option을 지정하지 않은 경우 timesteip 로깅 추가
            colored_lines = [f"{timestamp} | {log_level_with_color} | {first_line_content}"] + [f"{timestamp} | {log_level_with_color} | {line}" for line in lines[1:]]
        else:
            # PM2로 timestep logging option을 지정한 경우(권장) timestep 로깅 자동 지원
            colored_lines = [f"{log_level_with_color} | {first_line_content}"] + [f"{log_level_with_color} | {line}" for line in lines[1:]]

        return '\n'.join(colored_lines)
 
# 로거 설정
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOGGING_LEVEL))
ch = logging.StreamHandler()
ch.setLevel(getattr(logging, LOGGING_LEVEL))
log_colors = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'white,bg_red',
}

# 스트림 핸들러에 색상 포맷터를 적용
if SHOW_LOGGER_TIMESTEP:
    # PM2로 timestep logging option을 지정한 경우(권장) timestep 로깅 자동 지원
    ch_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)s | %(message)s",
        log_colors=log_colors,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
else:
    # PM2로 timestep logging option을 지정하지 않은 경우 timesteip 로깅 추가
    ch_formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s | %(message)s",
        log_colors=log_colors,
    )

if SAVE_LOGGER_FILE:
    file_path = os.path.join(SYSTEM_LOGGER_PATH, 'sys.log')
    fh = logging.FileHandler(file_path)
    fh.setLevel(getattr(logging, LOGGING_LEVEL))
    fh_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)

ch.setFormatter(ch_formatter)
logger.addHandler(ch)
logger.propagate = False

# 동기/비동기 함수의 실행 시간을 로깅하는 데코레이터
def log_execution_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        
        # pm2로 로깅을 처리하는 경우 logger로 발생하는 모든 로깅은 error log에 저장되기 때문에 변경 필요
        if SAVE_LOGGER_FILE:
            logger.info(f"{func.__name__} | called")
        else:
            log('green', f"{func.__name__} | called")

        start_time = time.time()
        if asyncio.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time

        # pm2로 로깅을 처리하는 경우 logger로 발생하는 모든 로깅은 error log에 저장되기 때문에 변경 필요
        if SAVE_LOGGER_FILE:
            logger.info(f"{func.__name__} | executed in {elapsed_time:.5f} seconds")
        else:
            log('green', f"{func.__name__} | executed in {elapsed_time:.5f} seconds")
            
        return result
    return wrapper

# 컬러 로그 메시지를 출력하는 함수 개발할 때만 사용
def log(color, text):
    color_prefix = f'{Style.BRIGHT}{getattr(Fore, color.upper())}'
    color_suffix = f'{Style.RESET_ALL}'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lines = str(text).split('\n')

    if SHOW_LOGGER_TIMESTEP:
        # PM2로 timestep logging option을 지정한 경우(권장) timestep 로깅 자동 지원
        colored_lines = [f"{color_prefix}{timestamp} | {line}{color_suffix}" for line in lines]
    else:
        # PM2로 timestep logging option을 지정하지 않은 경우 timesteip 로깅 추가
        colored_lines = [f"{color_prefix}{line}{color_suffix}" for line in lines]

    colored_message = '\n'.join(colored_lines)
    print(colored_message)
