#import get to call a get request on the site
from requests import get
from bs4 import BeautifulSoup
import numpy as np

response = get('https://losangeles.craigslist.org/search/apa?hasPic=1&availabilityMode=0') 
html_soup = BeautifulSoup(response.text, 'html.parser')

# Container for each posting
posts = html_soup.find_all('li', class_= 'result-row')


post_br = []		# Bedrooms
post_time = []		# Time 
post_sqft = []		# House Sqft
post_links = []		# Link to post
post_areas = []		# House area
post_titles = []	# House title
post_prices = []	# House price


for post in posts:

	if post.find('span', class_ = 'result-hood') is not None:

		post_datetime = post.find('time', class_= 'result-date')['datetime']
		post_time.append(post_datetime)

		#neighborhoods
		post_area = post.find('span', class_= 'result-hood').text
		post_areas.append(post_area)

		#title text
		post_title = post.find('a', class_='result-title hdrlnk')
		post_titles.append(post_title.text)

		#post link
		post_link = post_title['href']
		post_links.append(post_link)

		#removes the \n whitespace from each side,
		post_price = post.a.text.strip() 
		post_prices.append(post_price)

		if post.find('span', class_ = 'housing') is not None:
   
                #if the first element is accidentally square footage
			if 'ft2' in post.find('span', class_ = 'housing').text.split()[0]:

				#make bedroom nan
				bedroom_count = np.nan
				post_br.append(bedroom_count)

				#make sqft the first element
				sqft = int(post.find('span', class_ = 'housing').text.split()[0][:-3])
				post_sqft.append(sqft)

            #if the length of the housing details element is more than 2
			elif len(post.find('span', class_ = 'housing').text.split()) > 2:

				#therefore element 0 will be bedroom count
				bedroom_count = post.find('span', class_ = 'housing').text.replace("br", "").split()[0]
				post_br.append(bedroom_count)

				#and sqft will be number 3, so set these here and append
				sqft = int(post.find('span', class_ = 'housing').text.split()[2][:-3])
				post_sqft.append(sqft)

            #if there is num bedrooms but no sqft
			elif len(post.find('span', class_ = 'housing').text.split()) == 2:

				#therefore element 0 will be bedroom count
				bedroom_count = post.find('span', class_ = 'housing').text.replace("br", "").split()[0]
				post_br.append(bedroom_count)

				#and sqft will be number 3, so set these here and append
				sqft = np.nan
				post_sqft.append(sqft)                    

			else:
				bedroom_count = np.nan
				post_br.append(bedroom_count)

				sqft = np.nan
				post_sqft.append(sqft)
                
            #if none of those conditions catch, make bedroom nan, this won't be needed    
		else:
			bedroom_count = np.nan
			post_br.append(bedroom_count)

			sqft = np.nan
			post_sqft.append(sqft)
            #    bedroom_counts.append(bedroom_count)
                
            #    sqft = np.nan
            #    sqfts.append(sqft)

# print(type(posts)) #to double check that I got a ResultSet
# print(len(posts)) #to double check I got 120 (elements/page)

# print(posts[0].a.text.strip())
# post_one_datetime = posts[0].find('time', class_= 'result-date')['datetime']
# print(post_one_datetime)