from dotenv import load_dotenv
load_dotenv('.env')

import uvicorn
from fastapi import FastAPI
import time

from logger_config import log_execution_time, logger, log
import hw_logger


hw_logger.start_hw_logger()
app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/test_log")
async def test_log():
    log('black', 'this is black color log only in terminal')
    log('red', 'this is red color log only in terminal')
    log('green', 'this is green color log only in terminal')
    log('yellow', 'this is yellow color log only in terminal')
    log('blue', 'this is blue color log only in terminal')
    log('magenta', 'this is magenta color log only in terminal')
    log('cyan', 'this is cyan color log only in terminal')
    log('white', '''this is white color log only in terminal''')
    return 'success'
    

@app.get("/test_logger")
async def test_log():
    logger.debug("This is a debug message both terminal and ~.log")
    logger.info("This is an info message both terminal and ~.log")
    logger.warning("This is a warning message both terminal and ~.log")
    logger.error("This is an error message both terminal and ~.log")
    logger.critical("This is a critical message both terminal and ~.log")
    return 'success'


@app.get("/test_log_execution_time")
@log_execution_time
async def test_log():
    time.sleep(3)
    return 'success'


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


