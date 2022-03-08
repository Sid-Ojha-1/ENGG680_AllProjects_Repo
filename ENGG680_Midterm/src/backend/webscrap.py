"""
Ex3: Imagine we want to send out an email to all professors of ECE department. We have the list of the professors and their contact email in the following link. Write a program that explore the provided html link and create a list of professors email.
Link: https://schulich.ucalgary.ca/electrical-computer/faculty-members
"""

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
#from tqdm import tqdm
import os

class webscrap():
        
    def __init__(self):
        pass

    def addFirstName_LastName_Title_OfNewestFacultyMembers_InDataFrame(self, df, informationString_about_professor, homepageURL):
        lastRow = len(df)
        row_lst = []
        # print(informationString_about_professor)
        lst = informationString_about_professor.split(",")
        name = lst[0].replace("Dr.", "").strip().split()
        # for n in name.split():
        #     row_lst.append(n.strip())
        row_lst.append(name[0])
        row_lst.append(" ".join(name[1:]))
        row_lst.append(lst[-1].strip())
        row_lst.append(homepageURL.strip())
        df.loc[lastRow] = row_lst

    def extractPhoneNumberAndRoomNumberOfNewestFacultyMembers(self, siteURL):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res = requests.get(siteURL, verify=False)
        soup_2 = BeautifulSoup(res.text, 'lxml')
        phoneNum = ""
        location = ""
        if siteURL.startswith("https://profiles.ucalgary.ca"):
            for div in soup_2.find_all('div', class_='contact-section col-sm-4'):
                h4_text = div.find('h4')
                if h4_text is not None and str(h4_text.get_text()) == "Phone number":
                    p_txt = div.find('p')
                    if p_txt is not None and "Office" in str(p_txt):
                        phNumber = p_txt.find('a')
                        phoneNum = phNumber.get_text() + " - "
                elif h4_text is not None and str(h4_text.get_text()) == "Location":
                    p_txt = div.find('p')
                    if p_txt is not None and "Office" in str(p_txt):
                        loc = p_txt.find('a')
                        location = loc.get_text()
        elif siteURL.startswith("https://schulich.ucalgary.ca"):
            for div_col in soup_2.find_all('div', class_='col-md-6'):
                for div in  div_col.find_all('div'):
                    h4_text = div.find('h4')
                    if h4_text is not None and str(h4_text.get_text()) == "Phone":
                        a_txt = div.find('div').find('a')
                        phoneNum = str(a_txt.get_text()).strip() + " - "
                    elif h4_text is not None and str(h4_text.get_text()) == "Location":
                        a_txt = div.find('div').find('a')
                        location = str(a_txt.get_text()).strip()

        return (phoneNum + location)

    def initialize_webscrapping(self):


        # webscrp = webscrap()
        # get webpage
        required_webpage_to_webscrap = 'https://schulich.ucalgary.ca/electrical-software/faculty-members'
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = requests.get(required_webpage_to_webscrap, verify=False)

        # parse with bs
        soup = BeautifulSoup(response.text, 'lxml')
        # print(soup)

        paragraph_tag = '<p>'
        df_FacultyMembers = pd.DataFrame(columns = ["firstname", "lastname", "title", "homepage"])

        # Creating dataframe of newest faculty members
        for div in soup.find_all('div', class_='layout-blocks-ucws-text container-fluid roundable block text'):
            h2_text = div.find('h2')
            if h2_text:
                for st in (h2_text.stripped_strings):
                    # print(st)
                    if st.strip() == "Newest faculty members":
                        for p_text in div.find('div', class_='col-sm-12 two-col').find_all('p'):
                            # print("==>", str(p_text).split("\n"))
                            hmpage = ""
                            for a_text in p_text.find_all('a'):
                                if "View profile" in a_text.get_text():
                                    hmpage = a_text['href']
                            for st in p_text.stripped_strings:
                                if not "@" in st and not "View profile" in st:
                                    self.addFirstName_LastName_Title_OfNewestFacultyMembers_InDataFrame(df_FacultyMembers, st, hmpage)

        #Creating dataframe of all professors
        for div_profile in soup.find_all('div', class_='row profiles'):
            for div_txt_chunk in div_profile.find_all('div', class_='text-chunk'):
                hmpage = ""
                informationString_about_professor = ""
                for p_txt in div_txt_chunk.find_all('p'):
                    a_txt = p_txt.find('a')
                    if a_txt:
                        informationString_about_professor += a_txt.get_text().strip() + ","
                        hmpage = "https://schulich.ucalgary.ca" + str(a_txt['href']) 
                    else:
                        title = [txt for txt in p_txt.stripped_strings]
                        if title is not None and len(title)>0:
                            informationString_about_professor += title[0]
                self.addFirstName_LastName_Title_OfNewestFacultyMembers_InDataFrame(df_FacultyMembers, informationString_about_professor, hmpage)
                
        print("Displaying Newest Faculty members first.")
        print(df_FacultyMembers.head())

        #Stage3: Explore the Data
        df_FacultyMembers["Phone Number - Office"] = pd.NaT
        directory_to_save_CSV_file = "../data/"
        given_file_name = "uofc_prof.csv"

        for idx, row in df_FacultyMembers.iterrows():
            # extractPhoneNumberAndRoomNumber(row.homepage)
            df_FacultyMembers.loc[idx, "Phone Number - Office"] = self.extractPhoneNumberAndRoomNumberOfNewestFacultyMembers(row.homepage)

        print(df_FacultyMembers.tail())

        if os.path.isdir(directory_to_save_CSV_file):
            for filename in os.listdir(directory_to_save_CSV_file):
                os.remove(os.path.join(directory_to_save_CSV_file, filename))

        df_FacultyMembers.to_csv(directory_to_save_CSV_file + given_file_name, index=False)


if __name__ == '__main__':
    wb = webscrap()
    wb.initialize_webscrapping()
