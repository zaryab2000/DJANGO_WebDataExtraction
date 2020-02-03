from django.shortcuts import render,redirect
from .forms import UrlForm

import operator
import requests
from nltk.corpus import stopwords
import urllib.request
from bs4 import BeautifulSoup
from collections import Counter
from django.contrib import messages
from textblob.sentiments import NaiveBayesAnalyzer


from .models import Url


stop_words = set(stopwords.words('english'))
common_txt = ['|','1','2','3','4','5','6','7','8','9','10','&','@','The','A','What','_','−','It','You','-']

def tag_visible(element):
	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
	    return False
	if isinstance(element, Comment):
	    return False
	return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')

    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)





def home(request):
	db = Url.objects.all()
	form = UrlForm(request.POST or None)
	if form.is_valid():
		url_name = form.cleaned_data.get('url')
		check = Url.objects.filter(url=url_name).exists() 
		if check==True:
			data=Url.objects.filter(url=url_name)
			messages.success(request, f'THIS URL IS ALEREADY PRESENT IN DATABASE')
			con={
				'datas':data
			}

			return render(request,'main/result2.html',con)
		else:

			html = urllib.request.urlopen(url_name).read()
			text_data = text_from_html(html)
			words = text_data.split()
			words=[w for w in words if not w in stop_words]
			words=[w for w in words if not w in common_txt]
			count = Counter(words)
			top_10 = count.most_common(10)
			
			
			data = Url()
			data.url=url_name
			data.words=top_10
			data.save()
			return redirect('result')
	context={
		'form':form
	}
	return render(request, 'main/base.html',context)


def result(request):
	data = Url.objects.all().order_by('-id')
	messages.success(request, f'THIS URL IS NEEWLY ADDED TO DATABASE')

	context={
		'datas':data,
		
	}
	return render(request,'main/result.html',context)