import requests
from bs4 import BeautifulSoup
import xlsxwriter

def extract():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'}
    url = f'https://www.linkedin.com/jobs/search?keywords=&location=Letterkenny%2C%20County%20Donegal%2C%20Ireland&locationId=&geoId=105127899&f_TPR=&distance=25&f_JT=F&position=1&pageNum=0'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('li')
    for item in divs:
        try: 
            title = item.find('span', class_ = 'sr-only').text.strip()
            company = item.find('h4', class_ = 'base-search-card__subtitle').text.strip()
            location  = item.find('span', class_ = 'job-search-card__location').text.strip()
            job = {
                'title': title,
                'company': company,
                'location': location
            }
            jobList.append(job)
        except:
            continue
    return

def toXlsx():
    rowNum = 1
    for item in jobList:
        outSheet.write(f"A{rowNum}", item['title'])
        outSheet.write(f"B{rowNum}", item['company'])
        outSheet.write(f"C{rowNum}", item['location'])
        rowNum +=1

# create file to write the job listings into
outWorkBook = xlsxwriter.Workbook('jobs.xlsx')
outSheet = outWorkBook.add_worksheet()
jobList = []

c = extract()
transform(c)
toXlsx()
outWorkBook.close()