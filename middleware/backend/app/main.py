import os
from typing import List
from fastapi import BackgroundTasks, FastAPI, Query

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get("/research/dramatiq")
# async def exec_dramatiq():
#     import dramatiq_crawler
#     dramatiq_crawler.count_words.send("http://example.com")

@app.post("/rabbitmq/task")
async def post_task(msg: str):
    import myworker
    myworker.hello.delay(msg)
    return {
        "message": "accepted."
    }

@app.get("/research/default")
async def exec_research_default(option_keywords: List[str] = Query(["破産"]), deps: int = 0,
                                keywords: List[str] = Query(None)):
    import crawler

    keywords = filter(lambda keyword: keyword, keywords)
    print(111)

    for keyword in keywords:
        crawler.exec_crawler.delay(keyword, [], deps)
    return {"message": "Hello World"}


@app.get("/robot/google")
async def exec_google(keyword: str, option_keywords: List[str] = Query(None), deps: int = 0):
    import crawler
    crawler.exec_crawler.delay(keyword, option_keywords, deps)
    return {"message": "Hello World"}


# async def get_page():
#     from selenium import webdriver
#     from selenium.webdriver import DesiredCapabilities
# 
#     connector = ""
#     chrome_option = webdriver.ChromeOptions()
#     chrome_option.add_argument('--blink-settings=imagesEnabled=false')
# 
#     if bool(os.environ['IS_SELENIUM_DEBUG']):
#         connector = "http://selenium-debug:4444/wd/hub"
#     else:
#         connector = "http://selenium:4444/wd/hub"
# 
#     driver = webdriver.Remote(command_executor=connector,
#                               desired_capabilities=DesiredCapabilities.CHROME.copy(), options=chrome_option)
#     try:
#         driver.get('https://qiita.com/advent-calendar/2017/docker')
#         title = driver.title
#         text = driver.find_element_by_css_selector('article').text
#     finally:
#         driver.quit()
# 
#     return {"message": "Hello World"}


@app.post("/test/background")
async def test_background(msg: str, background_tasks: BackgroundTasks):
    """10秒後にサーバの標準出力にメッセージを出力する"""

    def send_message(msg: str):
        import time
        time.sleep(10)
        print(msg)

    background_tasks.add_task(send_message, msg=msg)
    return {"message": "Notification sent in the background"}


@app.get("/queue/test")
async def enqueue():
    import crawler
    # client_sentry = Client(settings.SENTRY_DSN)

    # crawler.app.send_task()
    crawler.task_wait.delay(3, 6)

    # task = celery_app.send_task(
    #     "worker.celery_worker.test_celery", args=[word])
    # background_task.add_task(background_on_message, task)
    return {"message": "Word received"}


if __name__ == "__main__":
    import uvicorn

    os.environ['IS_SELENIUM_DEBUG'] = 'True'
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

