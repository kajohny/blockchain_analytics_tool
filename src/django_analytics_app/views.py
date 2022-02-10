from django.db import IntegrityError
from django.shortcuts import render
from .models import Address
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np


def index(request):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://etherscan.io/accounts/1?ps=100") 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lists = soup.find_all('tr')

    res_addresses=[]
    res_balances=[]

    for list in lists:
        for address in list.find_all('a'):
            res_addresses.append(address.text.replace("\n", ","))

    array_addresses = np.array(res_addresses)
    for ch in ["[", "]" ,"'", " "]:
        res_addresses = str(res_addresses).replace(ch, "")
        
    balances = requests.get("https://api.etherscan.io/api?module=account&action=balancemulti&address=" + res_addresses + "&tag=latest&apikey=AQFDTFJZW2ZYVSWJF7M5KMS83SU6PVYYEJ",
    headers = {"accept": "application/json"})
    for balance in balances.json()['result']:
        res_balances.append(balance['balance'].replace("\n", ","))
    array_balances = np.array(res_balances)

    try:
        for i in range(len(array_balances)):
            Address.objects.create(address_name=array_addresses[i], address_balance=float(array_balances[i]) / 1e18)
            addresses = Address.objects.all()
    except IntegrityError:
        addresses = Address.objects.all()
        addresses.delete()
        for i in range(len(array_balances)):
            Address.objects.create(address_name=array_addresses[i], address_balance=float(array_balances[i]) / 1e18)
            addresses = Address.objects.all()

    
    
    context = {
        "addresses": addresses,
    }

    return render(request, 'chartapp/index.html', context)
