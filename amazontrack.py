import requests
from bs4 import BeautifulSoup
import csv
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import schedule
import time

# URL of the Amazon product page
url = '#'  # Replace with actual product URL

# Email credentials and settings
sender_email = '#'
receiver_email = '#'
email_password = '#'
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# CSV file to save price history
csv_file = 'price_history.csv'

# Function to send an email when the price changes
def send_email(new_price):
    subject = f"Price Change Alert! New Price: ${new_price}"
    body = f"The price has changed to ${new_price}. Check it out here: {url}"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Set up the server and send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, email_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print(f"Email sent! New price: ${new_price}")

# Function to scrape the price from the Amazon page
def check_price():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the Amazon price element
    price_whole_element = soup.find('span', class_='a-price-whole')
    price_fraction_element = soup.find('span', class_='a-price-fraction')

    # Print raw values from Amazon
    print(f"Raw price whole: {price_whole_element.text if price_whole_element else 'Not found'}")
    print(f"Raw price fraction: {price_fraction_element.text if price_fraction_element else 'Not found'}")

    if price_whole_element and price_fraction_element:
        price_whole = price_whole_element.text.strip().replace(',', '')  # Remove commas like 1,299
        price_fraction = price_fraction_element.text.strip()

        # Sanitize the values and remove any unexpected characters
        price_whole = ''.join(filter(str.isdigit, price_whole))  # Keep only digits
        price_fraction = ''.join(filter(str.isdigit, price_fraction))  # Keep only digits

        # Combine the sanitized parts and convert to float
        current_price = float(f"{price_whole}.{price_fraction}")
        return current_price
    else:
        print("Price not found on the page.")
        return None
    
# Function to log price into the CSV
def log_price(price):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, price])

# Main function to check price and send email if changed
def track_price():
    try:
        new_price = check_price()
        if new_price is not None:
            try:
                with open(csv_file, 'r') as file:
                    last_line = list(csv.reader(file))[-1]
                    last_price = float(last_line[1])
            except (FileNotFoundError, IndexError):
                last_price = None

            if last_price is None or new_price != last_price:
                log_price(new_price)
                send_email(new_price)
            else:
                print(f"No price change. Current price: ${new_price}")
        else:
            print("Failed to retrieve the price.")
    except Exception as e:
        print(f"Error: {e}")

# Schedule the task to run every hour
schedule.every(1).hours.do(track_price)

# Run
while True:
    schedule.run_pending()
    time.sleep(1)