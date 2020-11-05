# -*- coding: utf-8 -*-
import pandas as pd
import json
from urllib import request, parse

#variables
server_domain_name = "https://qusynthesize.qusandbox.com"
token = "YOUR API KEY HERE"
random_data_request = "/random_data"
data_fields_request = "/data_fields"
data_request = "/data"
anon_data_request = "/anonymize_data"

dataset_name = "credit"
entries_to_retrieve = "100"
columns_to_anonymize = [1, 2, 3]

# without api key, access is denied
try:
    url = request.urlopen(server_domain_name + data_request + \
                                 "?dataset_name=" + dataset_name + \
                                 "&amount=" + entries_to_retrieve)
    print(url.read())
except Exception as x:
    print('Without api key, access is denied:')
    print(x)

# with incorrect api key, access is denied
try:
    url = request.urlopen(server_domain_name + data_request + \
                                 "?dataset_name=" + dataset_name + \
                                 "&amount=" + entries_to_retrieve + \
                                 "&access_token=" + "foo")
    print(url.read())
except Exception as x:
    print('With incorrect api key, access is denied:')
    print(x)

# please make sure you have inserted the api key you are given
try:
    url = request.urlopen(server_domain_name + data_request + \
                                 "?dataset_name=" + dataset_name + \
                                 "&amount=" + entries_to_retrieve + \
                                 "&access_token=" + token)
    print("Now let's look at some api functionalities")
except Exception as x:
    raise Exception('please make sure you have inserted the api key you are given')

# get a taste of the dataset by retrieving a random data point
with request.urlopen(server_domain_name + random_data_request + \
                            "?dataset_name=" + dataset_name + \
                            "&access_token=" + token) as url:
    data = json.loads(url.read())
    #print(data)
    df = pd.read_json(data)
    print('/random_data: One row of the ' + dataset_name + ' dataset looks like this:')
    print(df)

# retrieve a list of all data fields
with request.urlopen(server_domain_name + data_fields_request + \
                            "?dataset_name=" + dataset_name + \
                            "&access_token=" + token) as url:
    data = json.loads(url.read())
    print('/data_fields: The ' + dataset_name + ' dataset has these fields:')
    print(data)

# now let's get some portion of the data
with request.urlopen(server_domain_name + data_request + \
                            "?dataset_name=" + dataset_name + \
                            "&amount=" + entries_to_retrieve + \
                            "&access_token=" + token) as url:
    data = json.loads(url.read())
    #print(data)
    df = pd.read_json(data)
    print ('/data: The retrieved data has {} observations/rows and {} variables/columns.' \
       .format(df.shape[0], df.shape[1]))

print('Some stats of this dataset:')
print(df.describe())

# a sample of original column 2; we will compare it with anonymized data
print('A sample of original column 2; we will compare it with anonymized data')
print(df.iloc[:10,2])

# get data and anonymize selected columns
send_data = {"columns_to_anonymize":columns_to_anonymize}
send_data = json.dumps(send_data).encode('utf8')
req = request.Request(server_domain_name + anon_data_request + \
                            "?dataset_name=" + dataset_name + \
                            "&amount=" + entries_to_retrieve + \
                            "&access_token=" + token,
                            data=send_data, method='PUT')
with request.urlopen(req) as url:
    data = json.loads(url.read())
    df_anonymized = pd.read_json(data)
    print ('/anonymize_data: The retrieved anonymized dataset has {} observations/rows and {} variables/columns.' \
       .format(df.shape[0], df.shape[1]))

# column 2 is anonymized
print('Column 2 is anonymized')
print(df_anonymized.iloc[:10,2])
