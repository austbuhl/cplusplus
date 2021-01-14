from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_URL = 'https://newyork.craigslist.org/search/?query={}'
BASE_IMG_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
  return render(request, 'base.html')

def new_search(request):
  search = request.POST.get('search')
  models.Search.objects.create(search=search)

  search_url = BASE_URL.format(quote_plus(search))

  response = requests.get(search_url)
  data = response.text

  soup = BeautifulSoup(data, features='html.parser')
  
  listings = soup.find_all('li', {'class': 'result-row'})

  final_listings = []

  for listing in listings:
    title = listing.find(class_='result-title').text
    url = listing.find('a').get('href')

    if listing.find(class_='result-price'):
      price = listing.find(class_='result-price').text
    else: 
      price = 'N/A'

    if listing.find(class_='result-image').get('data-ids'):
      image_id = listing.find(class_='result-image').get('data-ids').split(',')[0][2:]
      image_url = BASE_IMG_URL.format(image_id)
    else:
      image_url = 'https://craigslist.org/images/peace.jpg'

    final_listings.append((title, url, price, image_url))

  


  search_results = {
    'search': search,
    'final_listings': final_listings
  }

  return render(request, 'my_app/new_search.html', search_results)