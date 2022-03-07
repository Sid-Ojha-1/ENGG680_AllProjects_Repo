"""
Ex3: Imagine we want to send out an email to all professors of ECE department. We have the list of the professors and their contact email in the following link. Write a program that explore the provided html link and create a list of professors email.
Link: https://schulich.ucalgary.ca/electrical-computer/faculty-members
"""

from asyncio.windows_events import NULL
import requests
from bs4 import BeautifulSoup
import pandas as pd

# get webpage
response = requests.get('https://schulich.ucalgary.ca/electrical-software/faculty-members', verify=False)
# parse with bs
soup = BeautifulSoup(response.text, 'lxml')
# print(soup)

import re
email_pattern = re.compile("\w+@\w+\.ca")
email_lists = []

def addFirstName_LastName_Title_InDataFrame(df, informationString_about_professor, homepageURL):
    lastRow = len(df)
    row_lst = []
    print(informationString_about_professor)
    lst = informationString_about_professor.split(",")
    name = lst[0].replace("Dr.", "").strip()
    for n in name.split():
        row_lst.append(n.strip())
    row_lst.append(lst[-1].strip())
    row_lst.append(homepageURL.strip())
    df.loc[lastRow] = row_lst

def extractPhoneNumberAndRoomNumber(siteURL):
    res = requests.get(siteURL, verify=False)
    soup_2 = BeautifulSoup(res.text, 'lxml')
    phoneNum = ""
    location = ""
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
    return (phoneNum + location)

paragraph_tag = '<p>'
df_newestFacultyMembers = pd.DataFrame(columns = ["firstname", "lastname", "title", "homepage"])

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
                            addFirstName_LastName_Title_InDataFrame(df_newestFacultyMembers, st, hmpage)

# print(df_newestFacultyMembers)

#Stage3: Explore the Data
df_newestFacultyMembers["Phone Number - Office"] = pd.NaT
directory_to_save_CSV_file = "../../data/"
given_file_name = "uofc_prof.csv"

for idx, row in df_newestFacultyMembers.iterrows():
    # extractPhoneNumberAndRoomNumber(row.homepage)
    df_newestFacultyMembers.loc[idx, "Phone Number - Office"] = extractPhoneNumberAndRoomNumber(row.homepage)

# print(df_newestFacultyMembers)

df_newestFacultyMembers.to_csv(directory_to_save_CSV_file + given_file_name, index=False)
