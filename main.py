"""---------------------------------------- Amazon Purchase Reminder ----------------------------------------
In this code, we write a program that works like https://camelcamelcamel.com/.
You have selected a product on Amazon, but the product price is too high for you.
Then you announce the link of the product page and the maximum price you are willing to buy.
This program checks the price of the product on a daily basis and when the price is lower than your desired price,
it sends you an email to remind you to buy.
"""

# ---------------------------------------- Add Required Library ----------------------------------------
import os
import ssl
from random import choice
from smtplib import SMTP

import requests
from bs4 import BeautifulSoup

# ---------------------------------------- Parameters Definition ----------------------------------------

email_from = "MY_EMAIL"
my_password = "MY_PASSWORD"
port = 587  # For starttls
amazon_endpoint = input("Enter the Amazon page link:\n")

# ---------------------------------------- Get Amazon Price ----------------------------------------

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
]
random_user_agent = choice(user_agents)
response = requests.get(amazon_endpoint, headers={
    "User-Agent": random_user_agent,
    "Accept-Language": "en-US,en;q=0.9,fa;q=0.8"
})
soup = BeautifulSoup(response.text, 'html.parser')
price_list = soup.select(".a-price span")[0].get_text()
price = price_list.split("€")
price = price[1]

# ---------------------------------------- Price Comparison ----------------------------------------

price_elasticity = input("What is the maximum you will pay for this item?\n")
email_to = input("Enter your email\n")
context = ssl.create_default_context()
message = f"Your product is now {price}"
if price < price_elasticity:
    with SMTP("smtp.gmail.com", port) as connection:
        connection.starttls(context=context)
        connection.login(user=os.getenv(email_from), password=os.getenv(my_password))
        connection.sendmail(from_addr=os.getenv(email_from), to_addrs=email_to,
                            msg=f"Subject: Shopping time\n\n{message}\n{amazon_endpoint}")
