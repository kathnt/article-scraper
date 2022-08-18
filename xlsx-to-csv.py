import xlrd
import csv
import zipfile
from datetime import date, timedelta
import pandas as pd
from pathlib import Path

# source

#src_abbr = input("source abbrv: ")
src_abbr = ''


# keyword
keyword = 'climate'
results_list_name = '//.xlsx'

# start
start_month = 8
start_day = 17
start_year = 2021

# end
end_month = 12
end_day = 31
end_year = 2021

# number of days to add
add_date = 31


def unzip_to_csv(start_month, start_day, start_year, end_month, end_day, end_year):
  
  start_date = date(start_year, start_month, start_day)
  end_date = date(end_year, end_month, end_day)
  #delta = timedelta(days=60)

  while start_date <= end_date:
 
    date_str = start_date.strftime("%Y-%m-%d")

    file_name = date_str + '-' + src_abbr + '-' + keyword
    path = '/home/Downloads/' + src_abbr + '/' + file_name + '.ZIP'
    file_path = Path(path)
    if file_path.is_file():
      with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall('/home/Downloads/' + src_abbr + '/' + file_name)
  
    start_date += timedelta(days=add_date)


#######################

  start_date = date(start_year, start_month, start_day)
  end_date = date(end_year, end_month, end_day)
  #delta = timedelta(days=60)

  count = 0

  while start_date <= end_date:
  
    date_str = start_date.strftime("%Y-%m-%d")

    file_name = date_str + '-' + src_abbr + '-' + keyword
    path = '/home/Downloads/' + src_abbr + '/' + file_name + '/' + results_list_name
    print(path)


    file_path = Path(path)
    if file_path.is_file():
      #print('ssss')

      read_file = pd.read_excel(path)
   
      csv_name = '/home/Downloads/' + src_abbr + '/' + file_name + '.csv'

      read_file.to_csv(csv_name, index = None, header = False, sep = '\t')

    start_date += timedelta(days=add_date)




unzip_to_csv(start_month, start_day, start_year, end_month, end_day, end_year)

#unzip_to_csv(1,1,1980,1,1,1980)



# if some days have no articles





