import json
import csv
import sys
import datetime
import pytz

def formatCookie(cookie):
    expire_date_str = cookie.get("ExpireDate", "")
    if expire_date_str:
        expire_date = datetime.datetime.fromisoformat(expire_date_str)
        expire_date = expire_date.replace(tzinfo=pytz.timezone('UTC'))
        expiration_timestamp = (expire_date - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    else:
        expiration_timestamp = None

    cookieTemplate = {
        "domain": cookie.get("Host", ""),
        "expirationDate": expiration_timestamp,
        "hostOnly": not cookie.get("Host", "").startswith("."),
        "httpOnly": cookie.get("IsHTTPOnly", False),
        "name": cookie.get("KeyName", ""),
        "path": cookie.get("Path", "/"),
        "secure": cookie.get("IsSecure", False),
        "session": not cookie.get("IsPersistent", False),
        "value": cookie.get("Value", "")
    }
    return cookieTemplate

def filterCookiesByHost(data, keyword):
    filteredCookies = []

    for cookie in data:
        if keyword in cookie.get('Host', ''):
            cookieTemplate = formatCookie(cookie)
            filteredCookies.append(cookieTemplate)

    return filteredCookies

def csv2Json(csv_file):
    cookies = []
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['IsSecure'] = row['IsSecure'].lower() == 'true'
            row['IsHTTPOnly'] = row['IsHTTPOnly'].lower() == 'true'
            row['HasExpire'] = row['HasExpire'].lower() == 'true'
            row['IsPersistent'] = row['IsPersistent'].lower() == 'true'
            cookies.append(row)
    return cookies

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 HackBrowserDataExtractor.py <JSON or CSV file> <keyword>")
        sys.exit(1)

    file_path = sys.argv[1]
    keyword = sys.argv[2]

    if file_path.endswith('.json'):
        with open(file_path, 'r') as file:
            data = json.load(file)
    elif file_path.endswith('.csv'):
        data = csv2Json(file_path)
    else:
        print("Please provide a JSON or CSV file.")
        sys.exit(1)

    filteredCookies = filterCookiesByHost(data, keyword)

    print(json.dumps(filteredCookies, indent=4))