
# Amazon Price Tracker

This Python script automatically tracks the price of a product on Amazon, logs the price history in a CSV file, and sends an email alert when the price changes.

Read more about it [here:]([url](https://www.xda-developers.com/built-own-price-tracker-amazon-python/)) 



## Features
- Scrapes the price of an Amazon product at regular intervals.
- Logs the price history with timestamps in a CSV file.
- Sends an email alert when the price changes.
- Runs every hour to check for price updates.

## Prerequisites
Before running the script, ensure you have the following:

- Python 3.x installed
- Required libraries: `requests`, `beautifulsoup4`, `schedule`

  Install them by running:
  ```bash
  pip install requests beautifulsoup4 schedule
  ```

- A Gmail account for sending email alerts.

## Setup

1. **Amazon URL**: 
   - Replace `url = '#'` in the script with the actual Amazon product URL you want to track.
   
2. **Email Configuration**:
   - Replace the following placeholders in the script with your email details:
     - `sender_email`: Your Gmail address (used to send emails).
     - `receiver_email`: The email address where you want to receive alerts.
     - `email_password`: Your Gmail app password (use an [App Password](https://support.google.com/accounts/answer/185833) if two-factor authentication is enabled).
   
3. **CSV File**: 
   - `csv_file = 'price_history.csv'` stores the price history. The script appends new prices with timestamps to this file.

## How It Works

1. **Price Scraping**:
   - The script uses the `requests` library to retrieve the Amazon product page HTML and parses it with `BeautifulSoup` to extract the product price.

2. **Price Logging**:
   - The price is logged into a CSV file (`price_history.csv`) along with the timestamp.

3. **Email Alert**:
   - If the price changes compared to the last recorded price, the script sends an email alert to the specified receiver.
   
4. **Scheduler**:
   - The script uses the `schedule` library to check the price every hour.

## Running the Script

To run the script, use the following command:

```bash
python amazon_price_tracker.py
```

The script will run indefinitely, checking for price updates every hour and logging them in the CSV file.

## Customization

- **Interval**: 
  - By default, the price is checked every hour. You can modify this by changing the line:
    ```python
    schedule.every(1).hours.do(track_price)
    ```
    to a different interval, such as minutes or days:
    ```python
    schedule.every(30).minutes.do(track_price)
    ```

## Troubleshooting

- If the price element is not found, ensure the class names used in the script (`a-price-whole`, `a-price-fraction`) match the current HTML structure of the Amazon product page.

## Disclaimer

This script is intended for educational purposes only. It relies on web scraping, which may violate Amazon's terms of service, so use it responsibly.

## License

This project is licensed under the MIT License.
