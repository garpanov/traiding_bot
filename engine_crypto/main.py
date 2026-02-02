import websockets
import asyncio
import json
from httpx import AsyncClient, Limits

import models_pd

url_binance = "wss://stream.binance.com:443/ws/!ticker@arr"
limits = Limits(max_keepalive_connections=5, max_connections=10)
client = AsyncClient(limits=limits, timeout=0.5)
async def main():
    async with websockets.connect(url_binance) as websocket:
        while True:
            try:
                data = await websocket.recv()
                good_data = json.loads(data)
                currency = ["ETHUSDT", "PAXGUSDT"]
                data_for_db = []
                if good_data:
                    try:
                        for item in good_data:
                            if item["s"] in currency:
                                data_for_db.append(models_pd.CheckPricePD(currency=item["s"], price=item["c"], code_exchange=1))
                        created_model = models_pd.ListCheckPricePD(data=data_for_db)

                        response = await client.post("http://bd:8080/actual_price", json=created_model.model_dump())

                    except Exception as e:
                        print(f"error with db, data - {response}.\n\n{e}")
            except Exception as e:
                print(f"error with exchange - {e}")




# url_binance = "wss://fstream.binance.com/stream?streams=ethusdt@miniTicker/paxgusdt@miniTicker/btcusdt@miniTicker/solusdt@miniTicker"
#
# async def main():
#     async with websockets.connect(url_binance) as websocket:
#         while True:
#             data = await websocket.recv()
#             good_data = json.loads(data)
#             print(good_data)

if __name__ == "__main__":
    asyncio.run(main())