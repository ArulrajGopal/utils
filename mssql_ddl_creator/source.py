from os import chdir
from datetime import date
import sys
from functools import reduce


path = sys.argv[1]
table_name = sys.argv[2]
separator =sys.argv[3]


f=open(path,'r')
all_records = f.readlines()
f.close()

all_records_count = len(all_records)

f=open(path,'r')
columns_list = f.readlines()[0].strip('\n')
f.close()

columns_list = columns_list.split(separator)
no_of_columns = len(columns_list)

f=open(path,'r')
all_values_stage_1 = f.readlines()[1:all_records_count]
f.close()

all_values_stage_2 = []
for i in all_values_stage_1:
  all_values_stage_2.append(i.strip('\n'))

all_values_stage_3=[]
for i in all_values_stage_2:
  all_values_stage_3.append(i.split(separator))

all_values_final=[]
for i in all_values_stage_3:
  i = tuple(i)
  all_values_final.append(i)

def convert_to_date(x):
  x1 = x.split('-')
  x2 = date(int(x1[0]),int(x1[1]),int(x1[2]))
  return (x2)

def find_type(x):
  try:
    int(x)
    return 'int'
  except ValueError:
    try:
      float(x)
      return 'float' 
    except:
      try:
        convert_to_date(x)
        return 'Date'
      except ValueError:
        return 'string'

max_len_schema = []
for i in range(no_of_columns):
  max_len_schema.append(0)


for j in range(len(columns_list)):
  for i in range(len(all_values_final)):
    if (len(all_values_final[i][j])) > max_len_schema[j]:
       max_len_schema[j] = len(all_values_final[i][j])

schema=[]
for j in range(len(columns_list)):
  for i in range(len(all_values_final)):
    if find_type(all_values_final[i][j]) == 'int':
      format = 'int'
    elif find_type(all_values_final[i][j]) == 'float':
      format = 'Dec'
    elif find_type(all_values_final[i][j]) == 'Date':
      format = 'Date'
    else: 
      format = 'string'
    break
  schema.append(format)

def returning(x):
  return(reduce(lambda i,j:str(i)+str(j),x))

#a = schema
#b = max_len_schema
#c = indexing
def sql_schema (a, b, c):
  if a[c] == 'int' or a[c] == 'Date':
    return(a[c])
  elif a[c] == 'string':
    return returning(('varchar(',2*b[c],')'))
  elif a[c] == 'Dec':
    return returning ((a[c],'(',b[c],',2)'))

print('drop table if exists '+table_name+';')
print('\n')
print('create table '+table_name+'(')
for i in range(len(columns_list)):
  if i == len(columns_list)-1:
    print(columns_list[i], sql_schema(schema, max_len_schema, i))
  else:
    print(columns_list[i], sql_schema(schema, max_len_schema, i),',')
print(');')
print('\n')
print('insert into '+table_name)
print('values')
if no_of_columns > 1:
  for i in range(len(all_values_final)):
    if i == len(all_values_final)-1:
      print(all_values_final[i],';')
    else:
      print(all_values_final[i],',')
elif no_of_columns == 1:
  for i in range(len(all_values_final)):
    if i == len(all_values_final)-1:
      print("('"+all_values_final[i][0]+"');")
    else:
      print("('"+all_values_final[i][0]+"'),")
print('\n')
print('select * from '+table_name)
