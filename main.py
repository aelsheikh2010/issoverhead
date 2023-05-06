import requests
from datetime import datetime
import smtplib
import time
my_email = "testpython172000@gmail.com"
password = "ggrwqvecdgtfoxur"
MY_LAT = 31.452410 # Your latitude
MY_LONG = 391.695195 # Your longitude


def is_iss_over_head():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT + 5 >= iss_latitude >= MY_LAT - 5 and MY_LONG + 5 >= iss_longitude >= MY_LONG - 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now <= sunrise or time_now >= sunset:
        return True


while True:
    time.sleep(60)
    if is_iss_over_head() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"subject:Lookup\n\nThe Iss is above in the sky"
            )


# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



