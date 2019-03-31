from django.shortcuts import render, redirect
import os
import numpy as np
import random
from surprise import NormalPredictor
from movies.MovieLens import MovieLens
from movies.ContentKNNAlgorithm import ContentKNNAlgorithm
from movies.Evaluator import Evaluator
from joblib import load
from movierec.settings import algo, dataset, Info
from bs4 import BeautifulSoup
import requests
import re
import random
import pandas as pd
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


# class counter():
# 	count = 0
# 	def inc(self):
# 		self.count = (self.count + 1) % 5
# 		return self.count
# 	def count_print(self):
# 		print(self.count)


info = Info()
ml = MovieLens()
genres = ['Adventure', 'Action', 'Romance', 'Comedy', 'Tragedy', 'Thrill', 'Adult', 'Horrer', 'Sci-Fi']
countrys= ['USA', 'LONDON', 'AUSTRALIA', 'CHINA', 'JAPAN', 'CANADA', 'KOREA', 'SINGAPORE']




def getYears(movie_name):
	p = re.compile(r"(?:\((\d{4})\))?\s*$")
	m = p.search(movie_name)
	return m.group(1)

def LoadMovieLensData():
	
	data 		= ml.loadMovieLensLatestSmall()
	rankings 	= ml.getPopularityRanks()
	return (ml, data, rankings)

def Scraping(movie_id):
	rating = pd.read_csv('/home/manzars/Downloads/movie/src/movies/ml-latest-small/ratings.csv')
	p = rating.loc[(rating.movieId == movie_id)].iloc[:, 2:3].values
	total = 0
	for i in range(len(p)):
	    total = total + float(p[i])
	avg = total/len(p)
	rating = round(avg, 2)


	link = pd.read_csv('/home/manzars/Downloads/movie/src/movies/ml-latest-small/links.csv', converters={"imdbId":str})
	p = link.loc[(link.movieId == movie_id)].iloc[:, 1:2].values
	x = str(p[0][0])
	print(x)

	req 	= requests.get('http://www.imdb.com/title/tt' + x)
	soup 	= BeautifulSoup(req.text, 'lxml')
	tag 	= soup.findAll('div', {'class': 'poster'})

	try:
		link 	= tag[0].img.attrs['src'] 
	except:
		link = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
	return link, rating


def generate_recommendation(user_id):
	np.random.seed(0)
	random.seed(0)

	(ml, evaluationData, rankings) = LoadMovieLensData()

	testset = dataset.GetAntiTestSetForUser(user_id)
	predictions = algo.GetAlgorithm().test(testset)

	recommendations = []
	for userID, movieID, actualRating, estimatedRating, _ in predictions:
		intMovieID = int(movieID)
		recommendations.append((intMovieID, estimatedRating))

	recommendations.sort(key=lambda x: x[1], reverse=True)
	recom = []

	for ratings in recommendations[:20]:
		recom.append(ml.getMovieName(ratings[0]))

	return recom


def index_view(request,*args,**kwargs):

	
	if(request.user.is_authenticated):
		name = request.user.username
		total = 0
		for i in name:
			total += ord(i)
		total = total % 671
		if(len(info.recommendations) == 0):
			recom = generate_recommendation(total)
			movie_id = []
			for rec in recom:
				movie_id.append(ml.getMovieID(rec))
			year = []
			for movie in recom:
				year.append(getYears(movie))
			link, rating = [], []
			for ids in movie_id:
				link.append(Scraping(ids)[0])
				rating.append(Scraping(ids)[1])

				info.links = link
				info.ratings = rating
				info.movies_ids = movie_id
				info.recommendations = recom
				info.years = year

			contex = {
				'name': info.recommendations,
				'link': info.links,
				'rating': info.ratings,
				'year': info.years,
				'ids': info.movies_ids
			}
		else:
			contex = {
				'name': info.recommendations,
				'link': info.links,
				'rating': info.ratings,
				'year': info.years,
				'ids': info.movies_ids
			}
		return render(request,"web/index.html",contex)

	else:

		return HttpResponseRedirect(reverse('login'))
	

def login_view(request,*args,**kwargs):

	contex = {}
	if(request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if(user):
			login(request, user)
			return HttpResponseRedirect(reverse('index'))

		else:
			contex['error'] = "Provide Valid Information"
			return render(request, 'web/login.html', contex)
	else:
		return render(request,"web/login.html",{})




# def register_view(request,*args,**kwargs):
# 	if (request.method == 'POST'):
# 		form = UserRegisterForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			username = form.cleaned_data.get('username')
# 			messages.success(request, f'Account created for {username}!')
# 			print(username)
# 			return redirect('index')
# 	else:
# 		form = UserRegisterForm()
# 		print("im here	")
# 	return render(request, 'web/register.html', {'form': form})



def single_view(request,*args,**kwargs):

	if(request.user.is_authenticated):
		ids = int(request.GET['id'])
		print(type(ids), "ids")
		count = 0
		for x in info.movies_ids:
			if(x == ids):
				break
			count += 1
			print(type(x), "x")
		print(count, "count")
		poster = info.links[count]
		year = info.years[count]
		country = random.choice(countrys)
		genre = random.choice(genres)
		rat = info.ratings[count]
		print(poster, year, country, genre)

		recom = []
		rate = []
		link = []
		for i in range(3):
			p = random.randint(8, 19)
			recom.append(info.recommendations[p])
			link.append(info.links[p])
			rate.append(info.ratings[p])
			
			



		contex = {
		'age': 18,
		'country': country,
		'genre': genre,
		'year': year,
		'poster_link': poster,
		'rating': rat,
		'recommendations': recom,
		'rate': rate,
		'recom': recom,
		'link': link
		}


		return render(request,"web/single.html",contex)
	else:
		return HttpResponseRedirect(reverse('login'))


def logout_view(request,*args,**kwargs):
	if(request.method == 'POST'):
		logout(request)
		info.links = []
		info.ratings = []
		info.movies_ids = []
		info.recommendations = []
		info.years = []
		return HttpResponseRedirect(reverse('login'))

















