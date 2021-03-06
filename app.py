from os import path
from datetime import datetime
from textwrap import dedent
from time import sleep

from plyer import notification
import requests
import simpleaudio as sa

##########################
# PUT YOUR SETTINGS HERE #
##########################
DELAY = 300  # seconds
LOW_PRICE_NOTIFICATION = 1300
HIGH_PRICE_NOTIFICATION = 1800
SHOULD_PLAY_AUDIO = True

# This file has to exist in the `sounds` directory.
AUDIO_FILENAME = "notification.wav"


# The URL for the API
URL = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD"


def log(message):
    """
    Prints a log message to the terminal.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now}\t{message}")


def fetch_price():
    """
    This function gets the ETH price data.

    It returns a number like 1432.79.
    """
    # Fetch the data from the URL
    response = requests.get(URL)

    # the price data
    data = response.json()

    # take a peek at the data if you want
    log(f"got data from API: {data}")

    # 1 ETH is worth:
    # bitcoins = data.get("BTC")
    dollars = data.get("USD")
    return dollars


def send_notifiction(price):
    """
    This function pops up notifications.
    """
    title = f"ETH Price: {price}"
    message = "body"

    # this prints a message to the terminal
    print(dedent(f"""\
    =====================
    ETH PRICE: {price}
    =====================
    """))

    if SHOULD_PLAY_AUDIO:
        play_sound()

    notification.notify(
        title=title,
        message=message,
        timeout=300  # displaying time
    )


def should_notify(price):
    """
    This function checks to see if the price should send a notification.
    """
    if price <= LOW_PRICE_NOTIFICATION or price >= HIGH_PRICE_NOTIFICATION:
        log(f"sending notification for {price}!")
        return True
    else:
        log(f"price of {price} is not worth a notification")
        return False


def play_sound():
    """
    Play an audio notification.
    """
    filename = path.join("sounds", AUDIO_FILENAME)
    wave_obj = sa.WaveObject.from_wave_file(filename)
    wave_obj.play()


if __name__ == "__main__":
    # loop forever
    while True:
        price = fetch_price()
        if should_notify(price):
            send_notifiction(price)

        # This is where it delays
        sleep(DELAY)
