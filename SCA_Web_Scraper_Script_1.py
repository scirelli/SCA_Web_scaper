#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 07:41:27 2018

@author: ccirelli2
"""

'''PURPOSE

The purpose of this script is to scrape data from the Stanford Law Securities
Class Action Web page and convert it to structured data for ML training. 
'''


'''NOTES

1.) Page Order:  It is not clear that the page order coincides with the dates, i.e. they are not chronological. 
                We should record the page number next to the date in order to test this idea. 
                We should also take the range of the first page to last in order to know where the scraper should stop. 
                Then we can convert this into a numerical representation of what our scraper has to trasverse in order to scrape
                the entirety of the side. 

'''





## Import Libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import string
from nltk.stem import *
stemmer = PorterStemmer()
from nltk import corpus
import nltk


## Import Modules
import SCA_Web_Scraper_Module_1 as scraper_1



## WEB PAGE OBJECTS____________________________________________________________ 
'''Structure Web Page List of Cases
Root =              http://securities.stanford.edu/
Specific Cases =    filings-case.html?id=106716
?id =               Specific case Id.  Need to identify range.  These are the 
                    pages that we would iterate over. You could also look into
                    downloading each page to your laptop maybe using bash curl. 
'''
Url = 'http://securities.stanford.edu/filings-case.html?id='
Last = 106716
First = 101474 
First_minus_one= 101473



## PETRI DISH SECTION___________________________________________________________
'''Test code before adding to scaper'''
# Get Titles From Range of Articles
def loop_over_artilces_test(Url, Start):  
    
    # Create Lists to Capture values
    Defendant_list = []

    # Loop over article range
    for x in range(0,1):
        Start +=1
    
        # Create Beautiful Soup Object per article
        html = urlopen(Url + str(Start))
        bsObj = BeautifulSoup(html.read(), 'lxml')
    
        # Scrape Data Points
        data = scraper_1.get_plaintiff_firm(bsObj)
        print(data)
    return None

#loop_over_artilces_test(Url, First_minus_one)



## SCRAPER_______________________________________________________________________

def SCA_data_scraper(Url, Start, Write_to_excel):  
    '''Inputs

    '''

    print('Starting up Scraper...VROOM!...VROOM!', '\n')

    # LISTS TO CAPTURE DATA POINTS-------------------------------------
    # Summary Section
    Defendant_list = []
    Case_Status_list = []
    Filing_date_list = []
    Close_date_list = []
    Case_summary_list = []
    # Company Section
    Sector_list = []
    Industry_list = []
    Ticker_symbol_list = []
    Status_2_list = []
    Headquarters_list = []
    Company_market_list = []
    # First Filed Complaint
    First_court_list = []
    First_docket_list = []
    First_judge_list = []
    First_date_filed_list = []
    First_class_period_start_list = []
    First_class_period_end_list = []
    # Referenced Complaint
    Ref_court_list = []
    Ref_docket_list = []
    Ref_judget_list = []
    Ref_date_filed_list = []
    Ref_class_period_start_list = []
    Ref_class_period_end_list = []
    # Law Firms
    Plaintiff_firm_list = []
    Defendant_firm_list = []

    # Article Counter
    Count = 0

    # START LOOP OVER ARTICLES_________________________________________________
    
    # Create a range over which to iterate the loop. 
    upper_bound = 2500
    range_value = range(0, upper_bound)
    
    # Start Loop 
    for x in range_value:
        
        # First Page to Start Iteration
        Start +=1
         
        # Progress Recorder
        Count +=1       
        scraper_1.progress_recorder(Count, upper_bound)          

        # Create Beautiful Soup Object per article
        html = urlopen(Url + str(Start))
        bsObj = BeautifulSoup(html.read(), 'lxml')

        # SUMMARY SECTION----------------------------------------------

        # Scrape Defendant Value
        Defendant = scraper_1.get_defendant(bsObj)
        if Defendant == None:
           Defendant_list.append(None) 
        else:
            Defendant_list.append(Defendant)
           
        # Scrape Status
        # ******Note these if statements should be moved to the module
        Status = scraper_1.get_case_status(bsObj)
        if Status == None:
            Case_Status_list.append(None)
        elif 'DISMISSED' in Status:
            Case_Status_list.append('Dismissed')
        elif 'SETTLED' in Status:
            Case_Status_list.append('Settled')
        else:
            Case_Status_list.append('Unknown')

        # Scrape Filing Date
        Filing_date = scraper_1.get_filing_date(bsObj)
        if Filing_date == None:
            Filing_date.append(None)
        else:
            Filing_date_list.append(Filing_date)
      
        # Scrape Close Date
        Close_date = scraper_1.get_close_date(bsObj)
        if Close_date == None:
            Close_date_list.append(None)
        else:
            Close_date_list.append(Close_date)

        # Scrape Case Summary
        Case_summary = scraper_1.get_case_summary(bsObj)
        Case_summary_list.append(Case_summary)

        # COMPANY SECTION-------------------------------------------------_
        
        # Sector
        Sector = scraper_1.get_company_data_points(bsObj, 'Sector')
        Sector_list.append(Sector)
        # Industry
        Industry = scraper_1.get_company_data_points(bsObj, 'Industry')
        Industry_list.append(Industry)
        # Symbol
        Ticker_symbol = scraper_1.get_company_data_points(bsObj, 'Symbol')
        Ticker_symbol_list.append(Ticker_symbol)
        # Status
        Status_2 = scraper_1.get_company_data_points(bsObj, 'Status')
        Status_2_list.append(Status_2)
        # Headquarters
        Headquarters = scraper_1.get_company_data_points(bsObj, 'Headquarters')
        Headquarters_list.append(Headquarters)
        # Company Market
        Company_market = scraper_1.get_company_data_points(bsObj, 'Company Market')
        Company_market_list.append(Company_market)


        # FIRST FILED COMPLAINT SECTION------------------------------------
        
        # Court
        Court = scraper_1.get_first_complaint_data_points(bsObj, 'Court')
        First_court_list.append(Court)
        # Docket
        Docket = scraper_1.get_first_complaint_data_points(bsObj, 'Docket')
        First_docket_list.append(Docket)
        # Judge
        Judge = scraper_1.get_first_complaint_data_points(bsObj, 'Judge')
        First_judge_list.append(Judge)
        # Date Filed
        Date_filed = scraper_1.get_first_complaint_data_points(bsObj, 'Date Filed')
        First_date_filed_list.append(Date_filed)
        # Class Period Start
        Class_period_start = scraper_1.get_first_complaint_data_points(bsObj, 'Class Period Start')
        First_class_period_start_list.append(Class_period_start)
        # Class Period End
        Class_period_end = scraper_1.get_first_complaint_data_points(bsObj, 'Class Period End')
        First_class_period_end_list.append(Class_period_end)

        
        # REFERENCED FILED COMPLAINT SECTION---------------------------------------

        # Court
        Ref_court = scraper_1.get_referenced_complaint_data_points(bsObj, 'Court')
        Ref_court_list.append(Ref_court)
        # Docket
        Ref_docket = scraper_1.get_referenced_complaint_data_points(bsObj, 'Docket')
        Ref_docket_list.append(Ref_docket)
        # Judge
        Ref_judge = scraper_1.get_referenced_complaint_data_points(bsObj, 'Judge')
        Ref_judget_list.append(Ref_judge)
        # Date Filed
        Ref_date_filed = scraper_1.get_referenced_complaint_data_points(bsObj, 'Date Filed')
        Ref_date_filed_list.append(Ref_date_filed)
        # Class Period Start
        Ref_class_period_start = scraper_1.get_referenced_complaint_data_points(bsObj, 'Class Period Start')
        Ref_class_period_start_list.append(Ref_class_period_start)
        # Class Period End
        Ref_class_period_end = scraper_1.get_referenced_complaint_data_points(bsObj, 'Class Period End')
        Ref_class_period_end_list.append(Ref_class_period_end)

        # LAW FIRM SECTION---------------------------------------------------------

        # Plaintiff Firm
        Plaintiff_firm = scraper_1.get_plaintiff_firm(bsObj)
        Plaintiff_firm_list.append(Plaintiff_firm)
        # Defense Counsel
        # TBD

    # Combined Metrics
    '''Add duration from filing - close date'''


    # DATA ORGANIZATION SECTION----------------------------------------------------

    # Create DataFrame to House Values
    df = pd.DataFrame({})
    df['Defendant'] = Defendant_list
    df['Case_Status'] = Case_Status_list 
    df['Filing_date'] = Filing_date_list
    df['Close_date'] = Close_date_list
    df['Case_summary'] = Case_summary_list
    df['Sector'] = Sector_list
    df['Industry'] = Industry_list
    df['Ticker_symbol'] = Ticker_symbol_list
    df['Status_2'] = Status_2_list
    df['Headquarters'] = Headquarters_list
    df['Company_Market'] = Company_market_list
    df['First_Court'] = First_court_list
    df['First_Docket'] = First_docket_list
    df['First_Judge'] = First_judge_list
    df['First_Date_Filed'] = First_date_filed_list
    df['First_Class_Period_Start'] = First_class_period_start_list
    df['First_Class_Period_End'] = First_class_period_end_list
    df['Ref_Court'] = Ref_court_list
    df['Ref_Docket'] = Ref_docket_list
    df['Ref_Judge'] = Ref_judget_list
    df['Ref_Date_Filed'] = Ref_date_filed_list
    df['Ref_Class_Period_Start'] = Ref_class_period_start_list
    df['Ref_Class_Period_End'] = Ref_class_period_end_list
    df['Plaintiff_Firm'] = Plaintiff_firm_list

    # Write to Excel
    if Write_to_excel == True:
        scraper_1.write_to_excel(df, 'SCA_scraper_data_export')
    else:
        print(df)
    
    return None

SCA_data_scraper(Url, First_minus_one, True)  


