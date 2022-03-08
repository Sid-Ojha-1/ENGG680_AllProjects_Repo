
import pandas as pd
from backend.webscrap import webscrap

def generate_reports(df):
    print("\n\n---------------------------")
    print("Displaying information about dataframe")
    print(df.info())

    print("\n---------------------------")

    print("Generating reports :-\n")
    print("Number of Assistant Professors -", df[df['title'] == 'Assistant Professor'].shape[0])
    print("Number of Professors -", df[df['title'] == 'Professor'].shape[0])
    print("Number of Senior Instructors -", df[df['title'] == 'Senior Instructor'].shape[0])
    print("Number of Instructors -", df[df['title'] == 'Instructor'].shape[0])
    print("Number of Associate Professors -", df[df['title'] == 'Associate Professor'].shape[0])

if __name__ == '__main__':
    wb = webscrap()
    wb.initialize_webscrapping()

    # Stage 4
    directory_to_save_CSV_file = "../data/"
    given_file_name = "uofc_prof.csv"
    data_all_prof = pd.read_csv(directory_to_save_CSV_file+given_file_name)
    generate_reports(data_all_prof)
