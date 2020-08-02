import requests
from django.shortcuts import render
from requests.utils import requote_uri
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = 'https://hyderabad.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_.jpg'


# Create your views here.
def home(request):
    return render(request, 'myapp/base.html')


def newsearch(request):
    s = request.POST.get('search_one')
    models.Search.objects.create(search=s)
    final_url = BASE_CRAIGSLIST_URL.format(requote_uri(s))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://images.craigslist.org/images/peace.jpg'



        final_postings.append((post_title,post_url,post_price,post_image_url))

    context = {

        'search': s,
        'final_postings':final_postings,
    }
    return render(request, 'myapp/newsearch.html', context)
