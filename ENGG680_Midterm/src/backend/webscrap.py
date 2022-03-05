"""
Ex3: Imagine we want to send out an email to all professors of ECE department. We have the list of the professors and their contact email in the following link. Write a program that explore the provided html link and create a list of professors email.
Link: https://schulich.ucalgary.ca/electrical-computer/faculty-members
"""

import requests
from bs4 import BeautifulSoup

# get webpage
response = requests.get('https://schulich.ucalgary.ca/electrical-computer/faculty-members', verify=False)
# parse with bs
soup = BeautifulSoup(response.text, 'lxml')
# print(soup)

import re
email_pattern = re.compile("\w+@\w+\.ca")
email_lists = []

paragraph_tag = '<p>'

# for profs in soup.find('div', class_='col-sm-12 two-col').find_all('p'):
#     for info in profs.stripped_strings:
#         print(info)
#         email = re.findall(email_pattern,info)
#         if len(email) > 0:
#             email_lists.append(email)
    
#     print('------')


# for h_type in soup.find_all('div', class_='col-sm-12').find_all('h2'):
#     if h_type.h2.get_text(strip=True) == "Newest faculty members":
#         for profs in soup.find('div', class_='col-sm-12 two-col').find_all('p'):
#             for info in profs.stripped_strings:
#                 print(info)
#                 email = re.findall(email_pattern,info)
#                 if len(email) > 0:
#                     email_lists.append(email)
    
#     print('------')

for div in soup.find_all('div', class_='layout-blocks-ucws-text container-fluid roundable block text'):
    # for item in div.find_all(class_='mall-list-item-name')[0].text:
        # if info == "Newest faculty members":
    h2_something = div.find('h2')
    if h2_something:
        for st in (h2_something.stripped_strings):
            # print(st)
            if st.strip() == "Newest faculty members":
                print("[]")
                print('************')
                # for st in (div.stripped_strings):
                    # print("\t\t", st)
                for d in div.find('div', class_='col-sm-12 two-col').find_all('p'):
                    # print(str(d).strip(), "==>")
                    # str_paragraph_onlyName_within_div = str(d).strip().split("\n")[0]
                    # str_paragraph_onlyName_within_div = str_paragraph_onlyName_within_div[len(paragraph_tag) : str_paragraph_onlyName_within_div.find('<')]
                    # print(str_paragraph_onlyName_within_div, "==>")
                    for st in d.stripped_strings:
                        if "@" in st or "View profile" in st:
                            continue
                        else:
                            print(st)
                    # for st in d:
                    #     # print(str(st))
                    #     if not str(st).startswith("<a "):
                    #         print(str(st))
        # if tmp.strip() == "Newest faculty members":
        #     print(tmp)
      
    print('----')
    