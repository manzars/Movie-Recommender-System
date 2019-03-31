# -*- coding: utf-8 -*-
"""
Created on Fri May  4 16:25:39 2018

@author: Frank
"""


from movies.MovieLens import MovieLens
from movies.ContentKNNAlgorithm import ContentKNNAlgorithm
from movies.Evaluator import Evaluator
#from surprise import NormalPredictor
from joblib import dump, load
import random
import numpy as np

class ContentRecs:

    def LoadMovieLensData():
        ml = MovieLens()
        print("Loading movie ratings...")
        data = ml.loadMovieLensLatestSmall()
        print("\nComputing movie popularity ranks so we can measure novelty later...")
        rankings = ml.getPopularityRanks()
        return (ml, data, rankings)

    np.random.seed(0)
    random.seed(0)

    # Load up common data set for the recommender algorithms
    (ml, evaluationData, rankings) = LoadMovieLensData()

    # Construct an Evaluator to, you know, evaluate them
    evaluator = Evaluator(evaluationData, rankings)

    contentKNN = ContentKNNAlgorithm()
    evaluator.AddAlgorithm(contentKNN, "ContentKNN")

    # Just make random recommendations
    #Random = NormalPredictor()
    #evaluator.AddAlgorithm(Random, "Random")

    evaluator.Evaluate(False)

    (algo, dataset) = evaluator.SampleTopNRecs(ml)



    testset = dataset.GetAntiTestSetForUser(609)
    predictions = algo.GetAlgorithm().test(testset)

    dump(algo, 'algo.pkl')
    dump(dataset, 'dataset.pkl')


    '''
    algo = load('algo.pkl')

    dataset = load('dataset.pkl')
        
    recommendations = []

    print ("\nWe recommend:")
    for userID, movieID, actualRating, estimatedRating, _ in predictions:
        intMovieID = int(movieID)
        recommendations.append((intMovieID, estimatedRating))

    recommendations.sort(key=lambda x: x[1], reverse=True)

    for ratings in recommendations[:20]:
        print(ml.getMovieName(ratings[0]), ratings[1])
    '''