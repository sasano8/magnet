from typing import List
from libs import generator
from fastapi.responses import PlainTextResponse, HTMLResponse
import hjson
from magnet import get_db, Session, default_query, CommonQuery, Depends
from magnet.vendors import cbv, InferringRouter, TemplateView


router = InferringRouter()


@cbv(router)
class TradeProfileView:

    @router.post("/test_request", response_class=HTMLResponse)
    def test_request(self):
        import requests
        res = requests.get("https://example.com/")
        return res.text

    @router.post("/pytest", response_class=PlainTextResponse)
    def exec_pytest(self):
        from main import exec_pytest
        result = exec_pytest()
        return result

    @router.post("/json_to_pydantic", response_class=PlainTextResponse)
    async def json_to_pydantic(self, json: str = "{}"):
        dic = hjson.loads(json)

        model_name = "Dummy"
        code = generator.dump_pydantic_code_from_json(
            __model_name=model_name,
            data=dic,
            indent=4,
            require_default=False,
            set_default_from_json=False
        )
        return code

