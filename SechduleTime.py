import schedule
import time
import threading
from datetime import datetime, time as dtime

# Define your job function
def job():
    print("Market is open, running the job...")

# Function to check if the market is currently open
def is_market_open():
    now = datetime.now().time()
    market_open_time = dtime(9, 0)  # Market opens at 9:00 AM
    market_close_time = dtime(16, 0)  # Market closes at 4:00 PM
    return market_open_time <= now <= market_close_time

# Function to start the job at market open
def start_job():
    print("Starting the job...")
    while is_market_open():
        job()
        time.sleep(60)  # Run the job every minute during market hours
    print("Market is closed, stopping the job...")

# Schedule the start and stop times
schedule.every().day.at("09:00").do(start_job)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Run the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()
