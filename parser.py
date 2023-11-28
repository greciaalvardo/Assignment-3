# Name: Grecia Alvarado
# Assignment 3 problem 5

from bs4 import BeautifulSoup
from pymongo import MongoClient

def parse_html(html):
    bs = BeautifulSoup(html, 'html.parser')
    professors = bs.find_all('div', class_='clearfix')
    #print(faculty_list)
    print(len(professors))
    prof_info = []

    #get name, title office, email, and website
    for prof in professors:
        name = prof.find('h2').text.strip() if prof.find('h2') else ""
        title = prof.find('strong', string='Title').next_sibling.strip() if prof.find('strong', string='Title') else ""
        office = prof.find('strong', string='Office').next_sibling.strip() if prof.find('strong', string='Office') else ""
        phone = prof.find('strong', string='Phone').next_sibling.strip() if prof.find('strong', string='Phone') else ""
        email = prof.find('strong', string='Email').find_next('a').text.strip() if prof.find('strong', string='Email') else ""
        website = prof.find('strong', string='Web').find_next('a')['href'].strip() if prof.find('strong', string='Web') else ""
        faculty_info = {
            'name': name,
            'title': title,
            'office': office,
            'phone': phone,
            'email': email,
            'website': website}

        prof_info.append(faculty_info)
    return prof_info

if __name__ == "__main__":

    client = MongoClient()
    db = client.crawler_info
    pages = db.documents
    collection = pages.find_one({"URL": "/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"})
    prof_data = parse_html(collection['HTML'])

    # put data in mongodb
    print(prof_data)
    client = MongoClient()
    db = client.crawler_info
    professors = db.professors

    for prof in prof_data:
        professors.insert_one(prof)
