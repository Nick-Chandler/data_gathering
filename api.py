from fastapi import FastAPI, Request
import uvicorn, threading
from PoolInfo import PoolInfo
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()


def worker(pool_info: PoolInfo):
    pool_info.dump_to_file()
    print("Done dumping to file")
    return

@app.post("/ps_data")
async def ps_data(payload: List[PoolInfo]):
    pool_info = PoolInfo.model_validate(payload[0])
    threading.Thread(target=worker, args=(pool_info,)).start()
    return {"message": "Data received"}


@app.get("/")
async def root():
    return {"message": "All good"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)