from selenium import webdriver
import os
import time


# os.environ['PATH'] = r"C:\Selenium"

def getbalance():
    # driver = webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    # open site
    driver.get('https://autosweeprfidapps.com/balanceinquiry/')
    driver.implicitly_wait(20)
    # click and input username
    # acct_in = driver.find_element_by_css_selector('input[class="form-control"]')
    time.sleep(2)
    acct_in = driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/form/div[1]/input')
    acct_in.send_keys("EMAIL")
    # click and input password
    # acct_pass = driver.find_element_by_css_selector('input[placeholder="Password"]')
    time.sleep(2)
    acct_pass = driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/form/div[2]/input')
    acct_pass.send_keys("PASSWD")
    # click log in button
    time.sleep(2)
    driver.find_element_by_css_selector('button[class="btn btn-lg btn-info btn-block"]').click()
    # click get balance button
    time.sleep(2)
    driver.find_element_by_css_selector('button[class="btn btn-success btnBalance"]').click()
    time.sleep(10)
    pat = "//*[@id='modalBalance']/div/div/div[2]/h3"
    balance = driver.find_element_by_xpath(pat).get_attribute("innerHTML")
    if len(balance) > 0:
        return balance
    else:
        return 'Not Available'


def compare():
    # import the modules
    import imaplib
    import email
    # establish connection with Gmail
    server = "imap.gmail.com"
    imap = imaplib.IMAP4_SSL(server)

    # intantiate the username and the password
    username = "ALERT_MAIL"
    password = "AM_PASSWD"

    # login into the gmail account
    imap.login(username, password)

    # select the e-mails
    res, messages = imap.select('"[Gmail]/Sent Mail"')

    # calculates the total number of sent messages
    messages = int(messages[0])

    # determine the number of e-mails to be fetched
    n = 1

    # iterating over the e-mails
    for i in range(messages, messages - n, -1):
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])

                # getting the sender's mail id
                # From = msg["From"]

                # getting the subject of the sent mail
                subject = msg["Subject"]

                # printing the details
                return subject


def email_alert(subj, body, to):
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subj
    msg['to'] = to
    user = "ALERT_MAIL"
    msg['from'] = user
    passwd = "AM_PASSWD"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, passwd)
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    try:
        myBalance = getbalance()
        last_sent = compare()
        if myBalance not in last_sent:
            email_alert(f"AUTOSWEEP BALANCE2: {myBalance}", myBalance, "EMAIL")
        else:
            email_alert(f"AUTOSWEEP BALANCE2: {myBalance}", f"your previous balance was {last_sent[-7:]}",
                        'ecejgq@gmail.com')
    except:
        email_alert('ERROR: ', 'ERROR', "EMAIL")
