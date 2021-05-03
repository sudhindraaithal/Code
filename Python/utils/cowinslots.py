import requests
import smtplib
import json
from datetime import timedelta, date

vaccine_data = ['name', 'fee_type', 'date', 'available_capacity', 'fee', 'min_age_limit', 'vaccine', 'slots']
pincodes = ['560097','560064','560092','560054','560003','560013']
slots="\n"

for numOfDays in range(0,14):
    today = date.today() + timedelta(days=numOfDays)
    for pincode in pincodes:
        resp = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode='+str(pincode)+'&date='+today.strftime('%d-%m-%Y'))


        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        #print(resp.json().items())
        for key, value in resp.json().items():
            for items in value:
                if items["available_capacity"] >= 0 and items["min_age_limit"] == 18:
                    for data in vaccine_data:
                        slots = slots + data + ":" + str(items[data]) + "\n"
                slots += "\n"
            
       
fromaddr = 'from@gmail.com'
toaddrs  = 'to@gmail.com'
subject = 'Cowin slots'
username = 'user name'
password = 'pwd'
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, slots)
server.quit()