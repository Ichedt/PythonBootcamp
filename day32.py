"""
Day 32 - Automated Birthday Wisher

tags: SMTP, datetime module
"""
import random
import smtplib
import datetime as dt
import pandas

SENDER_EMAIL = "gabriel1234@example.com"
SENDER_PASSWORD = "123456"

# Get today's date
today = dt.datetime.now()
today_tuple = (today.month, today.day)

# Read the birthdays file
data = pandas.read_csv("day32/birthdays.csv")

# Create the birthdays dictionary - using dict comprehension
birthdays_dict = {
    (data_row["month"], data_row["day"]): data_row
    for (index, data_row) in data.iterrows()
}

# Check if there's a birthday that matches today's date
if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    file_path = f"day32/letter_templates/letter{random.randint(1,3)}.txt"
    # Replace the [NAME] with the person's name
    with open(file_path, encoding="utf-8") as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])

    # Send the letter
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # Start the secure connection
        connection.starttls()
        # Login with the senders credentials
        connection.login(SENDER_EMAIL, SENDER_PASSWORD)
        # Set contents and send it
        connection.sendmail(
            from_addr=SENDER_EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday\n\n{contents}",
        )
    # Instead of manually closing the connection, use "with"
    # connection.close()
