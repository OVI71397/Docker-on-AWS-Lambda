import requests
import pandas as pd
from itertools import product
from kiwi_api_key import kiwi_key
import json
import datetime as d
import boto3
from creds_aws import secret
from creds_aws import key
from io import StringIO

def form_lincks():
  ids = pd.read_csv('new_full_list_with_countries.csv')
  ids_sub = ids[ids.country_kiwi.isin(['United Arab Emirates', 'Iceland', 'Sri Lanka'])]
  ids_sub = ids_sub[['country_code', 'country_kiwi']]
  ids_sub.drop_duplicates(inplace=True)
  routs_list = list(product(ids_sub['country_code'], ids_sub['country_code']))
  route_df = pd.DataFrame(routs_list, columns=['countryCodeFrom', 'countryCodeTo'])
  from_day = int((d.date.today()).strftime("%d"))
  from_month = int((d.date.today()).strftime("%m"))
  from_year = int((d.date.today()).strftime("%Y"))
  to_day = int((d.date.today() + d.timedelta(days=180)).strftime("%d"))
  to_month = int((d.date.today() + d.timedelta(days=180)).strftime("%m"))
  to_year = int((d.date.today() + d.timedelta(days=180)).strftime("%Y"))
  links_plane = ["https://api.tequila.kiwi.com/v2/search?fly_from=" + from_code + "&fly_to=" + to_code + f"&date_from={from_day}%2F{from_month}%2F{from_year}&date_to={to_day}%2F{to_month}%2F{to_year}&curr=EUR&vehicle_type=aircraft&limit=1000" for from_code, to_code in zip(route_df['countryCodeFrom'], route_df['countryCodeTo'])]
  return links_plane


def api_call(url):
  headers = {
    'accepts': 'application/json',
    'apikey': kiwi_key
    }
  query = requests.get(url, headers=headers)
  if query.status_code==200:
    resp = json.loads(query.content.decode('utf-8'))
    resp_data = resp['data']
    resp_df = pd.DataFrame(resp_data)
    if len(resp_df) != 0:
      resp_df = pd.DataFrame({
        'flyFrom': resp_df['flyFrom'],
        'flyTo': resp_df['flyTo'],
        'cityFrom': resp_df['cityFrom'],
        'cityTo': resp_df['cityTo'],
        'countryFrom': pd.json_normalize(resp_df['countryFrom']).name,
        'countryTo': pd.json_normalize(resp_df['countryTo']).name,
        'countryCodeFrom': pd.json_normalize(resp_df['countryFrom']).code,
        'countryCodeTo': pd.json_normalize(resp_df['countryTo']).code,
        'distance': resp_df['distance'],
        'duration': pd.json_normalize(resp_df['duration']).total,
        'price_EUR': pd.json_normalize(resp_df['conversion']).EUR,
        'UTCarrival': resp_df['utc_arrival'],
        'UTCdeparture': resp_df['utc_departure']
        })
      return resp_df.groupby(['cityFrom', 'cityTo']).min('price_EUR')

def lambda_handler(event, context):
  links = form_lincks()
  result = map(api_call, links)
  result_list = list(result)
  result_df = pd.concat(result_list)
  result_df.reset_index(inplace=True)

  aws_access_key_id = key
  aws_secret_access_key = secret
  bucket_name = 'web-scraping3670333'
  s3_object_key = f'kiwi_flights/flights_{d.date.today()}.csv'
  csv_buffer = StringIO()
  result_df.to_csv(csv_buffer, index=False)
  s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
  s3.put_object(Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=s3_object_key)
  return print('Done')


