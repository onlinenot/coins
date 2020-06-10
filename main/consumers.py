import json
import asyncio
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from django.http import JsonResponse
from django.conf import settings
import requests
from .models import Coin


URL = settings.API_URL
SKIP = 0
LIMIT = 30


class CoinsConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connicted")
        await self.send({
            "type": "websocket.accept",
        })

        while 1:
            await asyncio.sleep(3)
            coins = await self.get_coins()
            await self.send({
                "type": "websocket.send",
                "text": json.dumps(coins)
            })

    async def websocket_receive(self, event):
        print("sended")
        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })

    async def websocket_disconnect(self, event):
        print("disconnect")
        await self.send({
            "type": "websocket.disconnect",
        })

    @database_sync_to_async
    def get_coins(self,):
        context = {}
        response = {}
        try:
            response = requests.get(f"{URL}?skip={SKIP}&limit={LIMIT}")
        except Exception as err:
            # TODO: Return Http error
            return print(f'ERROR: {err}')

        else:
            response = response.json()
            for item in response["coins"]:
                Coin.objects.update_or_create(
                    name=item["name"],
                    coin_id=item["id"],
                    symbol=item["symbol"],
                    icon=item["icon"],
                    defaults={
                        "price": float(item['price']),
                    }
                )
        return response["coins"]
