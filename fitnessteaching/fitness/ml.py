import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn.metrics.pairwise import pairwise_distances
from fitness.models import *
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans

# from matplotlib import pyplot as plt

# feature_list = ["email", "username", "password", "email_verified", "secure_token", "forgotten_token", "forgotten_token_created", "first_name", "last_name", "last_location_lat", "last_location_long", "user_avatar_dir", "age", "gender", "weight",
# "height", "blood_pressure_systolic", "blood_pressure_diastolic", "body_fat_percentage", "athlete", "heart_disease", "smoking", "medical_implant"]

num_of_clusters = 4
num_of_neighbours = 1
feature_list = ["age", "gender", "weight", "height", "athlete", "heart_disease", "smoking", "medical_implant"]

# debug
def print_users (users):
    print(users)
    for x in users:
        print("username = %s\n" % x.username)

# def get_pd (users):
#     a = []
#     for x in users:
#         b = []
#         for feature in feature_list:
#             exec("b.append(x.%s)" % feature)
#         a.append(b)
#     df = pd.DataFrame(a, columns=feature_list)
#     print(df)

def get_vectorized_users(users):
    a = []
    for x in users:
        b = {}
        for feature in feature_list:
            exec("b.update({\"%s\":x.%s})" % (feature, feature))
        a.append(b)
    vec = DictVectorizer()
    X = vec.fit_transform(a).toarray()
    return X, vec

# this function has to pass a vec for it
def get_predict_user (user, vec):
    a = []
    b = {}
    for feature in feature_list:
        exec("b.update({\"%s\":user.%s})" % (feature, feature))
    a.append(b)
    X = vec.transform(a).toarray()
    return X

def kmeans_plot(data, kmeans):
    h = .02
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower')
    plt.plot(data[:, 0], data[:, 1], 'k.', markersize=2)

    centroids = kmeans.cluster_centers_ # get the centroids
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()

# TO-DO : DEFINE K TO THE BEST
def get_kmeans (X):
    kmeans = KMeans(n_clusters = num_of_clusters, max_iter = 100, n_init = 10, init='k-means++', random_state=42)
    kmeans.fit(X)
    return kmeans

def classifiy_all_users(users):
    users = UserAccounts.objects.all()
    X, vec = get_vectorized_users(users)
    kmeans = get_kmeans(X)
    Y = kmeans.labels_
    i = 1
    for c in Y:
        temp = UserAccounts.objects.get(id=i)
        temp.classification = c
        temp.save()
        i += 1

def KNN (users, target_user, target_reviews):
    # update classification of users first, then run KNN
    classifiy_all_users(users)
    us, Y = [], []
    for review in target_reviews:
        us.append(review.user)
        Y.append(review.user.classification)
    # print("all target_reviews = %s\n" % target_reviews)
    # if no coresponding review is stored, then return None
    if len(us) == 0:
        return None, None
    X, vec = get_vectorized_users(us)
    print("users that are used to RECOMMEND, X = %s\n us = %s\n" % (X, us))
    neigh = KNeighborsClassifier(n_neighbors=num_of_neighbours)
    neigh.fit(X, Y)
    return neigh, vec

def give_recommendation (user_email):
    user_to_predict = UserAccounts.objects.get(email = user_email)
    users = UserAccounts.objects.all()
    target_reviews = VideosReview.objects.filter(target = user_to_predict.training_target)
    neigh, vec = KNN(users, user_to_predict, target_reviews)
    links = []
    if neigh == None:
        from random import shuffle
        all_review = VideosReview.objects.all()
        links = [ x.video.link for x in all_review ]
        shuffle(links)
        links = links[0:3]
    else:
        x = get_predict_user(user_to_predict, vec)
        predict_class = neigh.predict(x)
        users_from_class = UserAccounts.objects.filter(classification=predict_class)
        # print("predict_class = %s" % predict_class)
        # print("users_from_class = %s" % users_from_class)
        links = [ review.video.link for review in target_reviews if review.user.classification == predict_class ]
        # for review in target_reviews:
        #     print("review's user's class = %s, predict_class = %s\n" % (review.user.classification, predict_class))
        #     if review.user.classification == predict_class:
        #         print("match\n")
        # print("link = %s" % links)
    return links


# print(give_recommendation("z@z"))


# TO-DO : ONLY SELECT USERS THAT ARE SUITABLE TO RECOMMEND
# target_reviews
# temp_list = []
# for temp_user in users_from_class:
#     reviews = VideosReview.objects.filter(user=temp_user).filter(target=user_to_predict.training_target)
#     temp_list += [review.video for review in reviews if review not in temp_list]
# print(temp_list)
# videos = [x.video for x in reviews]
# links = []
# for my_video in videos:
#     # print(my_video.id)
#     links.append(FitnessVideo.objects.get(id=my_video.id).link)
# print("link = %s" % links)
