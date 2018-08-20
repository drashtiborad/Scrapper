import re

import requests
from bs4 import BeautifulSoup

from connection import execute

s = requests.Session()
r = s.get('https://www.naukri.com/')


def func(url, payload):
    j = s.post(url, data=payload)
    print(j)
    page = BeautifulSoup(j.text, 'html.parser')
    # print(page)
    rows = page.findAll('div', {'class': 'row', 'type': 'tuple'})
    count = 0
    for i in rows:
        title, company, experience, location, job_desc, compensation, job_type = 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', \
                                                                                 'NULL', 'NULL'
        a_tag = i.find('a', {'class': 'content'})
        link = a_tag['href']
        jd = s.get(link)
        job_details = BeautifulSoup(jd.text, 'html.parser')
        job_title = job_details.find('h1', {'itemprop': 'title'})
        pattern = r'[0-9]{12}'
        job_id = int(re.findall(pattern, link)[0])
        query = 'select job_id from naukri_banglore where job_id={}'.format(job_id)
        data = [int(t[0]) for t in execute(query)]

        if job_id not in data:
            if job_title:
                title = job_title.text

            cmpny = job_details.find('a', {'itemprop': 'hiringOrganization'})
            if cmpny:
                company = cmpny.text
                # print(company)
                count = count + 1
            else:
                print(link)
            exp = job_details.find('span', {'itemprop': 'experienceRequirements'})
            if exp:
                experience = exp.text

            loc = job_details.find('div', {'itemprop': 'name'})
            if loc:
                location = loc.text

            desc = job_details.find('ul', {'itemprop': 'description'})
            if desc:
                job_desc = desc.text

            salary = job_details.find('span', {'itemprop': 'baseSalary'})
            if salary:
                compensation = salary.text

            emp_type = job_details.findAll('span', {'itemprop': 'occupationalCategory'})
            if emp_type:
                job_type = (emp_type)[-1].text.strip()

            query = 'insert into naukri_banglore(job_id, job_title, job_description, compensation, ' \
                    'job_type,company,experience,job_link) values (%s, %s, %s, %s, %s, %s, %s, %s)'
            values = (job_id, title, job_desc, compensation, job_type, company, experience, link)

            execute(query, values)
    print(count)


url = 'https://www.naukri.com/jobs-in-bangalore'
payload = {'qsb_section': 'homepage', 'ql': 'Bangalore', 'qp': None, 'qe': '0', 'app_id': '103', }
j = s.post(url, data=payload)
print(j)
page = BeautifulSoup(j.text, 'html.parser')
num = page.find('span', {'class': 'cnt'})
total_num = int(num.text.split(" ")[-1])
print(total_num)
loop = 0
k = 1

func(url, payload)
# update_link(url,payload)
if total_num > 50:
    for n in range(1, int(total_num / 50) + 1):
        k = k + 1
        print(url + '-{}'.format(k))
        func(url + '-{}'.format(k), payload)
