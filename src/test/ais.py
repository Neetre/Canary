import os
import asyncio
import websockets
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()


# types: 80 - crude oil tanker, 52 - tag, 70 - container ship
AIS_KEY = os.getenv("AIS_KEY")


def log_timestamp() -> str:
    return f"[{datetime.now(timezone.utc)}]"


def log_message_details(message_count: int, message: dict) -> None:
    message_type = message.get("MessageType", "<missing>")
    print(f"{log_timestamp()} Message #{message_count} type: {message_type}")

    payload = message.get("Message", {})

    if message_type == "PositionReport":
        ais_message = payload.get("PositionReport", {})
        ship_id = ais_message.get("UserID", "<missing>")
        latitude = ais_message.get("Latitude", "<missing>")
        longitude = ais_message.get("Longitude", "<missing>")
        print(
            f"{log_timestamp()} PositionReport ShipId: {ship_id} "
            f"Latitude: {latitude} Longitude: {longitude}"
        )
        return

    if message_type == "ShipStaticData":
        ais_message = payload.get("ShipStaticData", {})
        ship_id = ais_message.get("UserID", "<missing>")
        ship_name = ais_message.get("Name", "<missing>")
        call_sign = ais_message.get("CallSign", "<missing>")
        destination = ais_message.get("Destination", "<missing>")
        ship_type = ais_message.get("Type", "<missing>")
        print(
            f"{log_timestamp()} ShipStaticData ShipId: {ship_id} "
            f"Name: {ship_name} CallSign: {call_sign} "
            f"Destination: {destination} Type: {ship_type}"
        )
        return

    print(f"{log_timestamp()} Ignoring unsupported message type")

async def connect_ais_stream():
    stream_url = "wss://stream.aisstream.io/v0/stream"
    print(f"{log_timestamp()} Connecting to {stream_url} ...")

    try:
        async with websockets.connect(stream_url) as websocket:
            print(f"{log_timestamp()} Connected to AIS stream")

            subscribe_message = {
                "APIKey": AIS_KEY,  # Required!
                "BoundingBoxes": [[[45.67846371941379, 13.637118081142999], [45.58209125942948, 13.849391849361284]]],  # Required!
                # "FiltersShipMMSI": ["368207620", "367719770", "211476060"],  # Optional!
                "FilterMessageTypes": ["PositionReport", "ShipStaticData"],  # Optional!
            }

            subscribe_message_json = json.dumps(subscribe_message)
            print(f"{log_timestamp()} Sending subscription message: {subscribe_message_json}")
            await websocket.send(subscribe_message_json)
            print(f"{log_timestamp()} Subscription sent")

            message_count = 0
            async for message_json in websocket:
                message_count += 1
                print(f"{log_timestamp()} Received message #{message_count} ({len(message_json)} bytes)")

                message = json.loads(message_json)
                log_message_details(message_count, message)
    except websockets.exceptions.ConnectionClosed as exc:
        print(f"{log_timestamp()} Connection closed: code={exc.code} reason={exc.reason}")
    except Exception as exc:
        print(f"{log_timestamp()} Stream error: {type(exc).__name__}: {exc}")

if __name__ == "__main__":
    asyncio.run(connect_ais_stream())