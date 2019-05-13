from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd

CPS_LINK = 'https://schoolinfo.cps.edu/schoolprofile/schooldetails.aspx?SchoolId='

CHI_NOT_299 = { 
                '070161100', 
                '150169000',
                '150169010',
                '150169020',
                '150169030',
                '150169040',
                '601054280',
                '651089000',
                '651089040'
                }

# def school_id_match(list_to_search, website_flag, retry_flag=None):
def school_id_match(list_to_search, website_flag, first_round=True):
    # Using Chrome to access web
    driver = webdriver.Chrome()
    # Open the website
    driver.get("http://google.com/")
    with open('CPS_ids.csv', 'a') as f:
        if first_round:
            f.write(f"ISBE_FacilityName,CPS_id_num,CPS_Match_Name\n")
        for query in list_to_search:
            # driver.find_element_by_tag_name("input").send_keys(query)
            driver.find_element_by_name("q").send_keys(query)
            driver.find_element_by_name("q").send_keys(Keys.ENTER)
            # driver.find_element_by_tag_name("input").send_keys(Keys.ENTER)
            
            # alternatively, find the search button element and click it.
            # driver.find_element_by_name("btnK").send_keys(Keys.ENTER)

            sleep(7)
            # driver.implicitly_wait(15)
            
            try:
                cps_page = driver.find_element_by_partial_link_text(website_flag).text
                details, id_num = cps_page.split('=')
                # print(f"Found link '{cps_page}' for '{query}' search!")
                f.write(f"{query},{id_num},{ details.splitlines()[0] }\n")
            except:
                try:
                    driver.back()
                    driver.find_element_by_name("q").send_keys(query + ' cps')
                    driver.find_element_by_name("q").send_keys(Keys.ENTER)
                    sleep(5)
                    # driver.implicitly_wait(15)

                    # check_flag = lambda x: website_flag if x == None else x
                    cps_page = driver.find_element_by_partial_link_text(website_flag).text
                    details, id_num = cps_page.split('=')
                    # print(f"Found link '{cps_page}' for '{query}' search!")
                    f.write(f"{query},{id_num},{ details.splitlines()[0] }\n")
                except:
                    f.write(f'{query},NA,NA\n')
                    driver.back()
                    continue
            
            sleep(5)
            driver.back()

    sleep(1)
    # driver.implicitly_wait(1)
    driver.quit()

    if __name__ == '__main__':
        isbe_list = pd.read_excel('dir_ed_entities.xls', sheet_name='Public Dist & Sch') 
        chicago_subset = isbe_list.loc[isbe_list['Region-2\nCounty-3\nDistrict-4'] == '150162990'] 
        chicago_subset = chicago_subset.loc[chicago_list['RecType']!='Dist']
        chicago_schools_list = chicago_subset.FacilityName.tolist()

        # optional, pickle dump list to recommence searching later
        # with open('school_list.pkl', 'wb') as f:                                                                    
        #      pickle.dump(chicago_schools_list, f) 

        # with open('school_list.pkl', 'rb') as f: 
        #     chicago_schools_list = pickle.load(f) 

        ss.school_id_match(list_to_search=chicago_schools_list, website_flag=ss.CPS_LINK, first_round=True)
        check_file = pd.read_csv('CPS_ids.csv')   

        excluded_noncharters = check_file.loc[(check_file['CPS_id_num'].isna()) & (~check_file['ISBE_FacilityName'].str.contains('Chtr'))]
        excluded_reg = excluded_noncharters['ISBE_FacilityName'].to_list()

        excluded_charters = check_file.loc[(check_file['CPS_id_num'].isna()) & (check_file['ISBE_FacilityName'].str.contains('Chtr'))]
        excluded_charters_list = excluded_charters['ISBE_FacilityName'].to_list()
        charters_cln = [s.replace('Chtr Sch ', '').replace('Chtr', '') for s in excluded_charters_list]

        ss.school_id_match(list_to_search=excluded_reg, website_flag='cps.edu', first_round=False) 
        
        ss.school_id_match(list_to_search=charters_cln, website_flag='cps.edu', first_round=False)

