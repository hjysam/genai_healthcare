from fastapi import FastAPI
from engine import ask
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    query: str
    # price: float
    # is_offer: Union[bool, None] = None

@app.get("/ping",
        summary="helth check server active",
        description="")
async def ping():
    return {"Hello World"}

@app.post("/llm/gpt-rag",
        summary="llm engine",
        description="wrap from ask funtion in engine.py file")
async def wrap_ask1(item: Item):
    try:
        ai_response = ask(item.query)
        return {
            "errCode": "0",
            "msg": "",
            "data": {
                "reader_query": ai_response[0],
                "info_retrieved_source": ai_response[1],
                "ll_response": ai_response[2],
                "info_score": ai_response[3],
                "accuracy_score": str(ai_response[4]),      
                "accuracy_reasoning": str(ai_response[5]),
                "runtime_in_sec": str(ai_response[6]),
                "cost_usd": str(ai_response[7]),
                "query_token": str(ai_response[8]),
                "info_token": str(ai_response[9]),
                "respond_token": str(ai_response[10]),
                "total_token": str(ai_response[11])

            }
        }
    except Exception as e:
        return {
            "errCode": "2",
            "msg": f"{e}",
            "data": []
        }

