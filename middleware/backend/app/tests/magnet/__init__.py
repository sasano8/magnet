from fastapi.testclient import TestClient
import main


client = TestClient(main.app)



