#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Load in the necessary libraries

import requests 
from bs4 import BeautifulSoup as bs


# In[3]:


# Load our first page

r = requests.get("https://keithgalli.github.io/web-scraping/example.html")

# Convert to a beautiful soup object

soup = bs(r.content)

# Print out our html

print(soup.prettify())


# In[4]:


# Start Using BeautifulSoup to Scrape

soup.find_all('a')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]


# In[5]:


first_header = soup.find("h2")

headers = soup.find_all("h2")
print(headers)


# In[6]:


# Pass in a list of elements to look for

first_header = soup.find(["h1", "h2"])

headers = soup.find_all(["h1", "h2"])
headers


# In[7]:


# You can pass in attributes to the find/find_all function
paragraph = soup.find_all("p", attrs = {"id": "paragraph-id"})
paragraph


# In[8]:


# You can nest find/find_all calls
body = soup.find('body')
div = body.find('div')
header = div.find('h1')
body


# In[9]:


# We can search specific strings inour find/find_all calls
import re

paragraphs = soup.find_all("p", string = re.compile("Some"))
paragraphs

headers = soup.find_all("h2", string = re.compile("(H|h)eader"))
headers


# In[10]:


# Select (CSS selector)

print(soup.body.prettify())


# In[11]:


content = soup.select("div p")
content


# In[12]:


paragraphs = soup.select("h2 ~ p")
paragraphs


# In[13]:


bold_text = soup.select("p#paragraph-id b")
bold_text


# In[14]:


paragraphs = soup.select("body > p")
print(paragraphs)

for paragraph in paragraphs:
    print(paragraph.select("i"))


# In[15]:


# Grab by element with specific property
soup.select("[align=middle]")


# In[16]:


# Get different properties of the HTML

header = soup.find("h2")
header.string

div = soup.find("div")
print(div.prettify())
print(div.get_text())


# In[17]:


# Get a specific property from an element

link = soup.find("a")
link['href']

paragraphs = soup.select("p#paragraph-id")
paragraphs[0]['id']


# In[19]:


# Path Syntax 
print(soup.body.prettify())


# In[20]:


# Know the terms: Parent, Sibling, Child

soup.body.find("div").find_next_siblings()


# In[21]:



r = requests.get("https://keithgalli.github.io/web-scraping/webpage.html")

webpage = bs(r.content)

print(webpage.prettify())


# In[22]:


## Grabbing all social links on webpage in 3 different ways

links = webpage.select("ul.socials a")
actual_links = [link['href']for link in links]
actual_links


# In[23]:


ulist = webpage.find("ul", attrs = {"class": "socials"})
links = ulist.find_all("a")
actual_links = [link['href']for link in links]
actual_links


# In[24]:


links = webpage.select("li.social a")
actual_links = [link['href']for link in links]
actual_links


# In[49]:


## Scrape an HTML table into a Pandas Dataframe

import pandas as pd

table = webpage.select("table.hockey-stats")[0]
columns = table.find("thead").find_all("th")
column_names = [c.string for c in columns]

table_rows = table.find("tbody").find_all("tr")
l = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [str(tr.get_text()).strip()for tr in td]
    l.append(row)
    
df = pd.DataFrame(l, columns = column_names)
df.head()


# In[50]:


import pandas as pd

table = webpage.select("table.hockey-stats")[0]
columns = table.find("thead").find_all("th")
column_names = [c.string for c in columns]

table_rows = table.find("tbody").find_all("tr")
l = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [str(tr.get_text()).strip()for tr in td]
    l.append(row)
    
df = pd.DataFrame(l, columns = column_names)
df['Team']


# In[51]:


import pandas as pd

table = webpage.select("table.hockey-stats")[0]
columns = table.find("thead").find_all("th")
column_names = [c.string for c in columns]

table_rows = table.find("tbody").find_all("tr")
l = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [str(tr.get_text()).strip()for tr in td]
    l.append(row)
    
df = pd.DataFrame(l, columns = column_names)
df.loc[df['Team'] != "Did not play"].sum()


# In[52]:


## Grab all fun facts that contain the word "is"

import re

facts = webpage.select("ul.fun-facts li")
facts_with_is = [fact.find(string = re.compile("is"))for fact in facts]
facts_with_is = [fact.find_parent().get_text()for fact in facts_with_is if fact]
facts_with_is


# In[59]:


## Download an Image

import requests 
from bs4 import BeautifulSoup as bs

url = "https://keithgalli.github.io/web-scraping/"
r = requests.get(url + "webpage.html")

webpage = bs(r.content)

images = webpage.select("div.row div.column img")
image_url = images[0]['src']
full_url = url + image_url

img_data = requests.get(full_url).content
with open('lake_como.jpg', 'wb') as handler:
    handler.write(img_data)
    


# In[61]:


## Mystery Challenge

files = webpage.select("div.block a")
relative_files = [f['href']for f in files]

url = "https://keithgalli.github.io/web-scraping/"
for f in relative_files:
    full_url = url + f
    page = requests.get(full_url)
    bs_page = bs(page.content)
    secret_word_element = bs_page.find("p", attrs = {"id": "secret-word"})
    secret_word = secret_word_element.string
    print(secret_word)


# In[ ]:




