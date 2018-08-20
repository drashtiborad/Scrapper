import re

import requests
from bs4 import BeautifulSoup

from connection import execute


def func(url):
    s = requests.Session()
    r = s.get(url, headers={
        "user-agent": "Mozilla/5.0 (X11; Linux     x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"})
    page = BeautifulSoup(r.text, 'html.parser')
    link = page.findAll('a', {'class': 'jobLink'})
    count = 0
    for i in link:
        if i.text:
            job_link = "https://www.glassdoor.co.in" + i['href']
            job_id = int(re.findall(r'[0-9]{10}$', job_link)[0])
            query = 'select job_id from naukri_banglore where job_id={} and platform="Glassdoor"'.format(job_id)
            data = [int(t[0]) for t in execute(query)]

            if job_id not in data:
                count = count + 1
                job = s.get(job_link, headers={
                    "user-agent":
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"})
                job_details = BeautifulSoup(job.text, 'html.parser')
                title = job_details.find('h2', {'class': 'noMargTop margBotXs strong'})
                if title:
                    title = title.text.encode('utf8')
                else:
                    print(job_link)
                    continue
                cmpny_name = job_details.find('span', {'class': 'strong ib'})
                if cmpny_name:
                    cmpny_name = cmpny_name.text.strip().encode('utf8')
                else:
                    print(job_link)
                    continue

                try:
                    job_desc1 = job_details.find('div', {'class': 'jobDesc '})
                    if job_desc1:
                        job_desc1 = job_desc1.text.encode("utf-8")
                except:
                    job_desc1 = job_details.find('div', {'class': 'jobDescriptionContent desc module pad noMargBot'})
                    if job_desc1:
                        job_desc1 = job_desc1.text.encode("utf-8")
                if job_desc1:
                    query = 'insert into naukri_banglore(job_id, job_title, job_description,' \
                            'company,job_link,platform) values (%s, %s, %s, %s, %s, %s)'
                    values = (job_id, title, job_desc1, cmpny_name, job_link, 'Glassdoor')
                    execute(query, values)
                else:
                    print(job_link)
                    continue

    print(count)


s1 = requests.Session()
url = 'https://www.glassdoor.co.in/Job/bengaluru-jobs-SRCH_IL.0,9_IC2940587.htm'
r = s1.get(url, headers={
    "user-agent":
        "Mozilla/5.0 (X11; Linux     x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"})

page = BeautifulSoup(r.text, 'html.parser')
job_num = page.find('p', {'class': 'jobsCount'}).text
job_count = int("".join(job_num.split()[0].split(",")))
m = int(job_count / 90)
print(m)
for i in range(2, m + 2):
    page_link = url.split(".htm")[0] + "_IP{}".format(i) + ".htm"
    func(page_link)
