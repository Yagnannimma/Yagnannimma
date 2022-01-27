import requests
import smtplib
import time
from bs4 import BeautifulSoup
import datetime as d
import pandas as pd
import csv
import threading as th
import os

headers={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

class amzcheck:
    name=[]
    ti=[]
    pr=[]
    headerlist=['title','time','price']
    dict = {'name': name, 'time': ti, 'price': pr}
    df = pd.DataFrame(dict)
    df.to_csv('hi.csv',header=headerlist, mode='a', index=False)
    def __init__(self):
        print("process is intialized ")

    def check(self,link,limit,emai):
        self.url = link
        self.page = requests.get(self.url, headers=headers)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.title = self.soup.find(id="productTitle").get_text()

        #self.title=self.title.text
        self.sender = "amazonprice924@gmail.com"
        self.check_price(limit,emai)
        print(self.title)
        return

    def sendmail(self,price,emai):

        self.title = self.soup.find(id="productTitle").get_text()
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.sender, 'Yagnan@123')

        message = "the product "+(self.title).strip()+" has a drop in its price " \
                                            " hurry up now the price is ruppees "+str(price)
        s.sendmail(self.sender, emai, message)
        print("sent")
        s.quit()
        return

    # each=soup.findAll("span",{'class':"a-offscreen"})
    # print(each[0])

    def writetocsv(self,ct,price):
        self.title = self.soup.find(id="productTitle").get_text()
        with open('hi.csv','a',newline="") as File:
            w=csv.writer(File)
            w.writerow([self.title,ct,price])
        return

    def current_time(self,price):
        c = d.datetime.now()
        ct = c.strftime('%H:%M:%S')
        self.writetocsv(ct, price)
        return

    def check_price(self,limit,emai):

        while (True):
            price = self.soup.find('span', {'class': 'a-offscreen'}).string.strip()
            print(price)
            price = price.replace(',', '')[1:]
            price = float(price)
            print(price)
            if (price <= limit):
                print('buy')
                self.sendmail(price,emai)
            self.current_time(price)
            time.sleep(10)


if __name__=="__main__":
    os.remove('hi.csv')
    st=[]
    limit=[]
    print("*******-> welcome to amazon price tracker <-*******")
    n=int(input('enter the no of products :'))
    objs=[amzcheck() for i in range(n)]
    for i in range(n):
        st1=input('enter the html link of the product :')
        st.append(st1)
        limit1=int(input("enter the price limit of the product :"))
        limit.append(limit1)

    email=input("enter the email to which the details should be sent :")


    threads=[th.Thread(target=objs[i].check,args=(st[i],limit[i],email)) for i in range(n)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
