from fastapi.responses import HTMLResponse
from fastapi import Query
from magnet import logger, rabbitmq, app, PagenationQuery
import magnet.user.views
import magnet.ingester.views
import magnet.research.views
import magnet.executor.views
import magnet.crawler.views
import magnet.trader.views
import magnet.develop.views
from libs.pydantic import funnel

@app.get("/", response_class=HTMLResponse)
async def root():
    # return {"message": "Hello World"}
    return """
    <html>
    <head>
        <title>hello my application.</title>
    </head>
    <body>
        <a href="docs">docs</a><br>
        <a href="redoc">redoc</a><br>
        <a href="http://localhost:8888">jupyter</a><br>
        <a href="http://localhost:8501">streamlit</a><br>
        <code>
        sudo jupyter contrib nbextension install<br>
        sudo jupyter nbextensions_configurator enable<br>
        sudoをつけないとファイルの更新に失敗する。matplotlibを実行できない
        sudo jupyter notebook --ip=0.0.0.0 --allow-root --notebook-dir=jupyter --NotebookApp.token='' --NotebookApp.password='' &<br>
        streamlit run magnet/streamlit_ui/main.py<br>
        </code>
    </body>
    </html>
    """

# @app.get("/mytest")
# @model_overload
# async def mytest(q: CommonQuery):
# # async def mytest(skip: int = Query(0, alias="from"), limit: int = 100, query: dict = {}):
#     return 1

app.include_router(magnet.user.views.router, prefix="/users")
app.include_router(magnet.research.views.router, prefix="/research")
app.include_router(magnet.crawler.views.router, prefix="/crawler")
app.include_router(magnet.executor.views.router, prefix="/executor")
app.include_router(magnet.ingester.views.router, prefix="/ingester")
app.include_router(magnet.trader.views.router, prefix="/trader")
app.include_router(magnet.develop.views.router, prefix="/develop")


@app.on_event("startup")
async def startup_event():
    logger.info("startup fastapi app!!!!!!!!")



@app.on_event("shutdown")
def shutdown_event():
    logger.info("shutdown fastapi app!!!!!!!")



logger.info(f"[STARTUP EVENT]: {len(app.router.on_startup)}")
for event in app.router.on_startup:
    logger.info(f"{event.__module__}.{event.__name__}")

logger.info(f"[SHUTDOWN EVENT]: {len(app.router.on_shutdown)}")
for event in app.router.on_shutdown:
    logger.info(f"{event.__module__}.{event.__name__}")


def exec_pytest():
    # ログイン時にscope=["me", "items"]を要求すると、最後の要素しか反映されない
    # pytestをpythonから起動するには？？
    # pytest.main(["--cov", "-s"])
    # 対象のテストのみ実行するには？
    # pytest.main(["test_mod.py::test_func"])
    # pytest.main(["test_mod.py::TestClass::test_func"])
    # pytest.main(["--pyargs", "pkg.testing"])  # パッケージでの指定
    # テスト一覧を列挙するには？

    import subprocess
    # result = subprocess.run(['pytest'], stdout=subprocess.PIPE)
    # print(result.returncode)
    # import os
    # import pytest
    # cd = os.getcwd()
    # result = pytest.main()
    # return result.stdout

    import pytest
    import sys
    from io import StringIO

    original_output = sys.stdout
    tmp_output = StringIO()

    try:
        sys.stdout = tmp_output
        # pytest.main(["-s", "tests"])
        pytest.main(["-s"])
        result = tmp_output.getvalue()
    except Exception as e:
        result = str(e)
    finally:
        sys.stdout = original_output
        tmp_output.close()

    return result

"""
jupyterを同梱させたい
やらなきゃいけないこと

1. docker jupyter用ポートを開ける
2. jupyter用のカレントディレクトリを設定
3. jupyterを起動ポート指定
4. 

https://github.com/tiangolo/fastapi/issues/199
apiへjupyterへのリダイレクトを追加する
@app.get("/redirected")
async def redirected():
    logger.debug("debug message")
    return {"message": "you've been redirected"}
"""

