import requests
from datetime import date


def get_data(casesper=100000):   
#1. Read in covid-19 data and sort
  endpoint = "https://api.covid19api.com/summary"
  response = requests.get(endpoint).json()

  covid19 = []
  for i in response['Countries']:
    covid19.append([i['Country']])

  covid19.sort(reverse=False)


#2. Read in population data and sort
  wb_pop_file = "D:\d2996479-edb9-45e0-b76f-44c3d7980535_Data.csv"

  wb  = []
  import csv
  with open(wb_pop_file, newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      global_pop = 0
      for row in reader:
        try:
          global_pop+=int(row['2020 [YR2020]'])
        except ValueError as e:
          #print(e)
          pass
        wb.append([row['Country Name'], row['2020 [YR2020]']])

  wb.sort(reverse=False)


#3. SQL join 
  count = 0
  for c in covid19:
    count+=1
    c.append('N/A')
    for w in wb:
      if c[0].replace(' ', '').upper() == w[0].replace(' ', '').upper(): #Viet Nam Vietnam
        #print('sqllll', c[0], w[0])
        c[1] = w[1]
        break


#4. Update the covid-19 data with population and calculations
  response['Global'].update({'Population': global_pop})
  response['Global'].update({'TotalConfirmed_per': (int(response['Global']['TotalConfirmed'])/int(response['Global']['Population'])) * casesper}) 
  response['Global'].update({'NewConfirmed_per': (int(response['Global']['NewConfirmed'])/int(response['Global']['Population'])) * casesper})
  response['Global'].update({'NewDeaths_per': (int(response['Global']['NewDeaths'])/int(response['Global']['Population'])) * casesper})
  response['Global'].update({'TotalDeaths_per': (int(response['Global']['TotalDeaths'])/int(response['Global']['Population'])) * casesper})
  response['Global'].update({'NewRecovered_per': (int(response['Global']['NewRecovered'])/int(response['Global']['Population'])) * casesper})
  response['Global'].update({'TotalRecovered_per': (int(response['Global']['TotalRecovered'])/int(response['Global']['Population'])) * casesper}) 
  for i in response['Countries']:
    i.update({'TotalConfirmed_per': 0})
    i.update({'NewConfirmed_per': 0})
    i.update({'NewDeaths_per': 0})
    i.update({'TotalDeaths_per': 0})
    i.update({'NewRecovered_per': 0})
    i.update({'TotalRecovered_per': 0})
    for a in covid19:
      if i['Country'] == a[0]:
        #print(i['Country'], a[0])
        i.update({'Population': a[1]})
        if i['Population'] == 'N/A':
          continue
        try:
          i.update({'TotalConfirmed_per': (int(i['TotalConfirmed'])/int(i['Population'])) * casesper})   
          i.update({'NewConfirmed_per': (int(i['NewConfirmed'])/int(i['Population'])) * casesper})
          i.update({'NewDeaths_per': (int(i['NewDeaths'])/int(i['Population'])) * casesper})
          i.update({'TotalDeaths_per': (int(i['TotalDeaths'])/int(i['Population'])) * casesper})
          i.update({'NewRecovered_per': (int(i['NewRecovered'])/int(i['Population'])) * casesper})
          i.update({'TotalRecovered_per': (int(i['TotalRecovered'])/int(i['Population'])) * casesper})
          break
        except ValueError as e:
          #print(e)
          pass

  return response
            

#5. Produce ranking tables
def table(data, measure, countryofi, casesper):
 
  response = data

  if 'per' in measure:
    print('\n\n', measure, ' '+'{:,.0f}'.format(casesper), sep='', end='\n\n')
  else:
    print('\n\n', measure, sep='', end='\n\n')
    
  print('Global', '{:,.0f}'.format(response['Global'][measure]))
  
  for i in response['Countries']:
    if i['Country'] == countryofi:
      print(i['Country'], '{:,.0f}'.format((i[measure])), end='\n\n')

  rank = sorted(response['Countries'], key = lambda i: i[measure], reverse = True)       
  count = 0
  for i in rank:
      count+=1
      print(count, i['Country'], '{:,.0f}'.format((i[measure])))
      if count == 10:
          break

        
#.6  Main
def main():
  print('Cases of covid-19 by country.')
  print('Date:', date.today())
  
  casesper = 100000
  data = get_data(casesper)
  coi = 'United Kingdom'
  table(data, 'TotalConfirmed', coi, casesper)
  table(data, 'TotalConfirmed_per', coi, casesper)
  table(data, 'NewConfirmed', coi, casesper)
  table(data, 'NewConfirmed_per', coi, casesper)
  table(data, 'NewDeaths', coi, casesper)
  table(data, 'NewDeaths_per', coi, casesper)
  table(data, 'TotalDeaths', coi, casesper)
  table(data, 'TotalDeaths_per', coi, casesper)
  table(data, 'NewRecovered', coi, casesper)
  table(data, 'NewRecovered_per', coi, casesper)
  table(data, 'TotalRecovered', coi, casesper)
  table(data, 'TotalRecovered_per', coi, casesper)


if __name__ == "__main__":
    main()


#End of code


