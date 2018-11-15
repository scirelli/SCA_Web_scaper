###  PUPROSE IS TO HOUSE THE FUNCTIONS FOR THE DATA ANALYSIS SCRIPT


# Import Libraries
import pandas as pd


def sql_query(conn, Query):
    '''
    conn:       Mysql connection
    Query:      Query to pass to function as a string. 
    Purpose:  General function to turn an SQL query into pandas df
    '''
    Query = (Query)
    df = pd.read_sql_query(Query, conn)
    return df



def query1_count_groupby_year():
    '''Purpose:  Get number of lawsuits filled by year'''

    Query = '''SELECT
            YEAR_FILED
            ,COUNT(defendant_name)

            FROM SCA_data
            GROUP BY YEAR_FILED;
            '''
    return Query


def query2_count_groupby_year_case_status():
    '''Purpose:  Get number of lawsuits filled by year'''

    Query = '''
            SELECT
            case_status
            ,YEAR_FILED
            ,COUNT(defendant_name) AS 'Count'
            FROM SCA_data
            WHERE YEAR_FILED > 2009
            AND case_status IS NOT NULL
            GROUP BY case_status, YEAR_FILED;            

            '''
    return Query


def limit_dataframe_casetype_year(df, case_type, year):
    '''
    Purpose:    Index the original sql query to return only data for dismissed and < 2018 > 2010
    Input:      dataframe grouped by year and case status
                case_type: can be 'Dismissed', 'Settled', 'Ongoing'
                year:  Should be the year that you want to exclude. 
    return:     filtered dataframe for status and year. 
    '''
    limit_case_status = df.case_status == case_type
    limit_year = df.YEAR_FILED != year
    df_index_case_status = df[limit_case_status]
    df_dismissed_final = df_index_case_status[limit_year]
    return df_dismissed_final


def get_settled(df):
    Not_dismissed = df.case_status == 'Settled'
    Yr_2010_2017 = df.YEAR_FILED != '2018'
    df_index_not_dismissed = df[Not_dismissed]
    df_not_dismissed_final = df_index_not_dismissed[Yr_2010_2017]
    return df_not_dismissed_final


def get_count_all_allegations_by_year_for_dismissed():

    Query = '''
            SELECT
            YEAR_FILED
            ,COUNT(Merger)          AS Merger_count
            ,COUNT(Net_Income)      AS NetIncome_count
            ,COUNT(Cash_Flow)       AS CashFlow_count
            ,COUNT(Proxy_violation) AS ProxyViolation_count
            ,COUNT(Related_parties) AS RelatedParties_count
            ,COUNT(Stock_Drop)      AS StockDrop_count
            ,COUNT(Revenue_Rec)     AS RevRec_count
            ,COUNT(Customers)       AS Customers_count
            ,COUNT(Fourth_Quarter)  AS Q4_count
            ,COUNT(Third_Quarter)   AS Q3_count
            ,COUNT(Corporate_Governance) AS CorpGov_count
            ,COUNT(Conflicts_Interest) AS ConflictInt_count
            ,COUNT(Accounting)      AS Accounting_count
            ,COUNT(Fees)            AS Fees_count
            ,COUNT(Failed_disclose) AS FailedDisclose_count
            ,COUNT(False_misleading) AS FalseMisleading_count
            ,COUNT(Commissions)     AS Commissions_count
            ,COUNT(Bankruptcy)      AS Bankruptcy_count
            ,COUNT(Secondary_Offering) AS SecondaryOffering_count
            ,COUNT(IPO)             AS IPO_count
            ,COUNT(1934_Exchange_Act) AS 1934_Act_count
            ,COUNT(Derivative)      AS Derivative_count
            ,COUNT(10b5) AS 10B5_count
            ,COUNT(1933_Act)        AS 1933_Act_count
            ,COUNT(Heavy_trading)   AS HeavyTrading_count
            ,COUNT(Sexual_Misconduct) AS SexualMisconduct_count
            ,COUNT(class_action)    AS ClassAction_count
            ,COUNT(ERISA)           AS ERISA_count
            ,COUNT(FCPA)            AS FCPA_count
            ,COUNT(SEC_Investigation) AS SEC_investigation_count
            ,COUNT(Data_breach)     AS DataBreach_count
            ,COUNT(Proxy)           AS Proxy_count

            FROM SCA_data
            WHERE case_status = 'Dismissed'
            AND YEAR_FILED IS NOT NULL 
            GROUP BY YEAR_FILED;
            '''
    return Query

   
def get_count_all_allegations_all_years():

    Query = '''
            SELECT
            YEAR_FILED
            ,COUNT(Merger)          AS Merger_count
            ,COUNT(Net_Income)      AS NetIncome_count
            ,COUNT(Cash_Flow)       AS CashFlow_count
            ,COUNT(Proxy_violation) AS ProxyViolation_count
            ,COUNT(Related_parties) AS RelatedParties_count
            ,COUNT(Stock_Drop)      AS StockDrop_count
            ,COUNT(Revenue_Rec)     AS RevRec_count
            ,COUNT(Customers)       AS Customers_count
            ,COUNT(Fourth_Quarter)  AS Q4_count
            ,COUNT(Third_Quarter)   AS Q3_count
            ,COUNT(Corporate_Governance) AS CorpGov_count
            ,COUNT(Conflicts_Interest) AS ConflictInt_count
            ,COUNT(Accounting)      AS Accounting_count
            ,COUNT(Fees)            AS Fees_count
            ,COUNT(Failed_disclose) AS FailedDisclose_count
            ,COUNT(False_misleading) AS FalseMisleading_count
            ,COUNT(Commissions)     AS Commissions_count
            ,COUNT(Bankruptcy)      AS Bankruptcy_count
            ,COUNT(Secondary_Offering) AS SecondaryOffering_count
            ,COUNT(IPO)             AS IPO_count
            ,COUNT(1934_Exchange_Act) AS 1934_Act_count
            ,COUNT(Derivative)      AS Derivative_count
            ,COUNT(10b5) AS 10B5_count
            ,COUNT(1933_Act)        AS 1933_Act_count
            ,COUNT(Heavy_trading)   AS HeavyTrading_count
            ,COUNT(Sexual_Misconduct) AS SexualMisconduct_count
            ,COUNT(class_action)    AS ClassAction_count
            ,COUNT(ERISA)           AS ERISA_count
            ,COUNT(FCPA)            AS FCPA_count
            ,COUNT(SEC_Investigation) AS SEC_investigation_count
            ,COUNT(Data_breach)     AS DataBreach_count
            ,COUNT(Proxy)           AS Proxy_count

            FROM SCA_data
            WHERE YEAR_FILED IS NOT NULL
            GROUP BY YEAR_FILED;
            '''
    return Query






def get_dismissal_rate_by_claim_category(category, case_status):
    '''
    Input:      
                category:   A string that represents the attribute from our data for which you want
                to use in the group statement in order to see the dismissal rate for the sub
                groups of this category. Note that the input must be the same as the column name 
                from our MySQL table. 
                case_status: The status of the case (Dismissed, Settled, Ongoing) for which
                you want to filter the information.  Must be a string. 
    Format:     The string function 'format' will insert into the SQL statement the values the
                user choses for category and case_status
    Note:       The input {} to the conditional statement in the where clause needs to be wrapped in 
                quotes. 
    Output:     SQL query statement as a string

    '''

    Query = '''
            SELECT 

            {}
            ,COUNT(*) AS 'COUNT {}'

            FROM SCA_data
            WHERE YEAR_FILED IS NOT NULL
            AND case_status = '{}'
            GROUP BY {};
            '''.format(category, case_status, case_status, category)
    return Query














