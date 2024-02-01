import requests 
from bs4 import BeautifulSoup

with open('search_intern.html') as f:
    soup=BeautifulSoup(f,'lxml')


featured_containers=soup.find_all('section',class_='scholarshipslistFeaturedcard_listCard__EqaBe')
scholarship_containers=soup.find_all('section',class_='scholarshipslistcard_listCard__3oVnA')

for container in featured_containers:
    title_element=container.find('h4')
    title=title_element.find('span').text
    link=title_element.find('a').href
    award_element=container.find('article',class_='scholarshipslistFeaturedcard_box__pUHnL')
    award=award_element.find('span').text

    print(title,award)

for container in scholarship_containers:
    title_element=container.find('h4')
    title=title_element.find('span').text
    link=title_element.find('a').href
    award_element=container.find('article',class_='scholarshipslistcard_box__S_Oby')
    award=award_element.find('span').text

    print(title,award)
# extra details - go into links provided - soup.find('article',class_='brandScholarshipDetails_contentBoxWrapper___GQGi')
# this gives all the finer details -  eligibility and preferences, documents required