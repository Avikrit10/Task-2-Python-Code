# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 16:42:41 2019

@author: garv2
"""

import pdfquery
import re
import os, shutil
import pyodbc
import datetime
import io
import re
from datetime import date
import smtplib
import openpyxl
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import random

import re

def extract_text_from_pdf(pdf_path):
    

    
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    print(text)
    
    
    dem = re.search("Demand/fixed charge.{10}", text)
    dem = dem.group()
    dem = dem.replace("Demand/fixed charge", " ")
    dem = dem.split(".")
    dem = dem[0] + "." + dem[1][:2]
    print(dem)
    
    wheel = re.search("Wheeling Charges.{10}", text)
    wheel = wheel.group()
    wheel = wheel.replace("Wheeling Charges", " ")
    wheel = wheel.split(".")
    wheel = wheel[0] + "." + wheel[1][:2]
    print(wheel)
    
    ec = re.search("Energy charge.{10}", text)
    ec = ec.group()
    ec = ec.replace("Energy charge", " ")
    ec = ec.split(".")
    ec = ec[0] + "." + ec[1][:2]
    print(ec)
    
    ge = re.search("Government Electricity Duty.{50}", text)
    ge = ge.group()
    ge = ge.replace("Government Electricity Duty", " ")
    ge = ge.split("%")
    ge = ge[1].split(".")
    ge = ge[0] + "." + ge[1][:2]
    print(ge)
    
    ma = re.search("Mah.Govt.Tax on sale of electricity.{50}", text)
    ma = ma.group()
    ma = ma.replace("Mah.Govt.Tax on sale of electricity", " ")
    ma = ma.split("unit")
    ma = ma[1].split(".")
    ma = ma[0] + "." + ma[1][:2]
    print(ma)
    
    amt = re.search("Current month's bill amount.{50}", text)
    amt = amt.group()
    amt = amt.replace("Current month's bill amount(A)", " ")
    amt = amt.split(".")
    amt = amt[0] + "." + amt[1][:2]
    print(amt)
    
    dp = re.search("Digital Payment Discount.{50}", text)
    dp = dp.group()
    dp = dp.replace("Digital Payment Discount", " ")
    dp = dp.split(".")
    dp = dp[0] + "." + dp[1][:2]
    print(dp)
    
    pd = re.search("Payment received upto.{30}", text)
    pd = pd.group()
    pd = pd.replace("Payment received upto", " ")
    if "-" in pd:
        pd = pd.split("-")
        pd = pd[0] + "-" + pd[1] + "-" + pd[2][:4]
    else:
        pd = pd.split(".")
        pd = pd[0] + "." + pd[1] + "." + pd[2][:4]
        
    print(pd)
   
    pr = re.search("Payment received upto.{30}",text)
    pr = pr.group()
    pr = pr.replace("Payment received upto", " ")
    pr = pr.replace(pd, " ")
    pr = pr.split(".")
    pr = pr[0] + "." + pr[1][:2]
    print(pr)
    
    md = re.search("Meter reading date.{100}", text)
    md = md.group().split("-")
    md = md[0][-2:] + "-" + md[1] + "-" + md[2][:4]
    print(md)
    
    pmd = re.search("Meter reading date.{100}", text)
    pmd = pmd.group().split("-")
    pmd = pmd[2][-2:] + "-" + pmd[3] + "-" + pmd[4][:4]
    print(pmd)
    
    sd = re.search("Your security deposit.{50}",text)
    sd = sd.group()
    sd = sd.replace("Your security deposit (SD) with us", " ")
    sd = sd.split(".")
    sd = sd[0] + "." + sd[1][:2]
    print(sd)
    
    dpc = re.search("Total bill amount with DPC.{30}", text)
    dpc = dpc.group()
    dpc = dpc.replace("Total bill amount with DPC", " ")
    dpc = dpc.split(".")
    dpc = dpc[0] + "." + dpc[1][:2]
    print(dpc)
    
    CoD = re.search("Contract Demand.{20}", text)
    CoD = CoD.group()
    CoD = CoD.replace("Contract Demand", " ").split(".")
    CoD = CoD[0] + "." + CoD[1][:5] 
    print(CoD)
    
    PF = re.search("Power Factor.{40}",text)
    PF = PF.group().replace("Power Factor (PF) penalty/incentive", " ").split(".")
    PF = PF[0] + "." + PF[1][:2]
    print(PF)
    
    number = re.search("Meter No..{7}", text)
    number = number.group().replace("Meter No.", " ")
    print(number)
    
    mf = re.search("Multiplying Factor.{1}", text)
    mf = mf.group().replace("Multiplying Factor", " ")
    print(mf)
    
    redpr = re.search("Energy consumptionReadingPresent.{50}", text)
    redprk = redpr.group().replace("Energy consumptionReadingPresent", " ").split(".")
    z = redprk
    z = z[0] + "." + z[1][:2]
    print(z)
    
    redprv = re.search("Energy consumptionReadingPresent.{50}", text)
    redprv = redprv.group().replace("Energy consumptionReadingPresent", " ")
    redprv = redprv.replace(z," ")
    redprv = redprv.replace("Previous", " ").split(".")
    y = redprv
    y = y[0] + "." + y[1][:2]
    print(y)
    
    total = re.search(" Factor1Energy consumption.{100}", text)
    total = total.group().split("TOD")
    total = total[0].split("(kWh)")
    total = total[1]
    n = len(total)
    m = int(n/2)
    total = total[-m:]
    #total = "".join(total).split("(kWh)")
    print(total)
    
    
    



extract_text_from_pdf(r'C:\Users\garv2\Desktop\Adani-Greater than 20_IN-1016301-107020.pdf')   

    