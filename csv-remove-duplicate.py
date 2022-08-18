import pandas as pd
from difflib import SequenceMatcher
from datetime import datetime, timedelta
import time

# source

src_abbr = input("source abbrv: ")




# date
date_str = '01011980-12312021'


def similar(a, b):
  return SequenceMatcher(None, a, b).ratio()


# make data from csv
data = pd.read_csv('/home/Downloads/' + src_abbr + '/' + src_abbr + '-with-dup.csv', sep = '\t', names = ["Title","Source","","Date"])

# sort by title
data.sort_values("Title", inplace = True)

# make temporary column to compare case insensitive
data["Title-upper"] = data["Title"].astype(str).str.upper()

print(len(data))

# drop duplicates
data.drop_duplicates(subset = ["Title-upper", "Date"], inplace = True)

print(len(data))

# drop temporary column
data.drop("Title-upper", axis = 1, inplace = True)

data_copy = data.copy()

w_file = open("/home/Downloads/" + src_abbr + "/" + "dropped-" + src_abbr + ".txt", 'w')


prev_title = ""
prev_date = datetime.fromisoformat("1980-01-01")
num_drop = 0
num_art = 0

for ind in data.index:
  # print(ind)
  # print(prev_title)
  current_title = data["Title"][ind]
  # num_art += 1
  # print(num_art)
  # print(current_title)
  
  sim_ratio =  similar(prev_title,current_title)
  # print("similartiy: " + str(sim_ratio))
  # print('------------------------')
  # time.sleep(1)
  date = datetime.fromisoformat(data["Date"][ind])

  if sim_ratio > 0.9:
    # print("CHECKING DUPLICATE...\n")
    prev_minus_one = prev_date - timedelta(days=7)
    prev_plus_one = prev_date + timedelta(days=7)

    if (prev_minus_one <= date) and (prev_plus_one >= date):
      # print("dopped current row...\n")
      # print('======------======------======-----=====')
      data_copy.drop(ind, inplace = True)
      num_drop += 1
      w_file.write(str(num_drop) + '.\n')
      w_file.write("already in list:\t" + prev_title + '\n')
      w_file.write("dropped as dup: \t" + current_title + '\n')
      w_file.write(str(sim_ratio) + '\n')
      w_file.write('---------------\n')



  elif sim_ratio > 0.7:
    # print("CHECKING DUPLICATE...\n")
    prev_minus_one = prev_date - timedelta(days=3)
    prev_plus_one = prev_date + timedelta(days=3)

    if (prev_minus_one <= date) and (prev_plus_one >= date):
      # print("dopped current row...\n")
      # print('======------======------======-----=====')
      data_copy.drop(ind, inplace = True)
      num_drop += 1
      w_file.write(str(num_drop) + '.\n')
      w_file.write("already in list:\t" + prev_title + '\n')
      w_file.write("dropped as dup: \t" + current_title + '\n')
      w_file.write(str(sim_ratio) + '\n')
      w_file.write('---------------\n')

    # else:
      # prev_title = current_title
      # prev_date = date
  
  # else:
  prev_title = current_title
  prev_date = date

print(len(data_copy))

w_file.close()

data_copy.to_csv("/home/Downloads/"  + src_abbr + "/" + src_abbr + '-' + date_str + "-no-dup.csv", index = False, sep = '\t')



