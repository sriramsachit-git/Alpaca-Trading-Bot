import json
import config
import websocket
from queue import Queue
import pandas as pd
import threading

API_KEY = config.API_KEY
SECRET_KEY = config.SECRET_KEY
TICKER_SYMBOL = config.TICKER_SYMBOL

df = pd.DataFrame()
message_count = 0

def on_open(ws):
    print("WebSocket connection opened")
    auth_data = {"action": "auth", "key": API_KEY, "secret": SECRET_KEY}
    ws.send(json.dumps(auth_data))
    listen_message = {
        "action": "subscribe",
        "bars": [TICKER_SYMBOL]
    }
    ws.send(json.dumps(listen_message))

def on_message(ws, message):
    global df, message_count
    d = json.loads(message)
    print(d)
    message_count += 1
    print(f"Message count: {message_count}")
    # Must ignore the first three messages 
    if message_count>3:
        dftemp = pd.read_json(json.dumps(d))
        df = pd.concat([df, dftemp], ignore_index=True)
 
        print("Message added to DataFrame")
        df.to_csv("LiveData.csv")

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Closed connection")

def start_websocket():
    socket = "wss://stream.data.alpaca.markets/v1beta3/crypto/us"
    ws = websocket.WebSocketApp(socket, on_open=lambda ws: on_open(ws), on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

def live():
    start_websocket()
    

def run_websocket_in_thread():
    thread = threading.Thread(target=start_websocket)
    thread.daemon = True
    thread.start()
    return thread


if __name__ == "__main__":
    start_websocket()