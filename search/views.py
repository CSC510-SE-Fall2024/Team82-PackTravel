"""Django views for ride search functionality"""
from django.shortcuts import render, redirect
from cachetools import LRUCache;
from utils import get_client
from request import views as requestsViews
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sys
sys.path.append("../cache")

#sys.path.append("../cache")
#from cache.timed_cache import lru_cache
# database connections
db_client = None
db_handle = None
users_collection = None
rides_collection = None

def initialize_database():
    """This method initializes handles to the different database collections"""
    global db_client, db_handle, users_collection, rides_collection
    db_client = get_client()
    db_handle = db_client.main
    users_collection = db_handle.users
    rides_collection = db_handle.rides



def get_recommended_ride(user_preferences, all_rides):
    """
    Finds and returns the most recommended ride for a user based on preferences.

    Parameters:
        user_preferences (dict): The logged-in user's preferences.
        all_rides (list): List of all available rides from the database.

    Returns:
        dict: The most recommended ride, or None if no suitable match is found.
    """
    ride_profiles = []  # To store ride-specific preferences

    for ride in all_rides:
        # Combine ride preferences into a single string for vectorization
        ride_preferences = f"{ride.get('travel_preferences', '')} {ride.get('likes', '')} {ride.get('is_smoker', False)} {ride.get('driver_gender', False)} {ride.get('travel_with_pets', False)}"
        ride_profiles.append(ride_preferences)

    # Combine user preferences into a single string
    user_profile = f"{user_preferences['travel_preferences']} {user_preferences['likes']} {user_preferences['is_smoker']} {user_preferences['driver_gender']} {user_preferences['travel_with_pets']}"

    # Create vector representations
    vectorizer = TfidfVectorizer()
    all_profiles = [user_profile] + ride_profiles  # User profile is the first vector
    preference_vectors = vectorizer.fit_transform(all_profiles)

    # Compute cosine similarity between the user and all rides
    similarity_scores = cosine_similarity(preference_vectors[0:1], preference_vectors[1:]).flatten()

    # Find the most similar ride
    most_similar_index = np.argmax(similarity_scores)
    #print(similarity_scores)
    if similarity_scores[most_similar_index] > 0:  # Ensure the similarity is significant
        return all_rides[most_similar_index]

    else:
        return all_rides[0]



def search_index(request):
    """This method processes the request to render available rides on the search page"""
    initialize_database()

    if not request.session.has_key("username"):
        request.session["alert"] = "Please login to view rides."
        return redirect("index")

    username = request.session["username"]
    user_data = users_collection.find_one({"username": username})
    all_rides = list(rides_collection.find({'owner': {'$ne' : username}}))
    processed = []
    user_preferences = {}

    for ride in all_rides:
        ride["id"] = ride.pop("_id")
        processed.append(ride)

    if user_data != None:    # Extract user preferences
        user_preferences = {
            "travel_preferences": user_data.get("travel_preferences", ""),
            "likes": user_data.get("likes", ""),
            "is_smoker": user_data.get("is_smoker", False),
            "travel_with_pets": user_data.get("travel_with_pets", False),
            "driver_gender": user_data.get("driver_gender", False),
        }
        recommended_ride = get_recommended_ride(user_preferences, processed)
    else:
        recommended_ride = processed[0]


    return render(request, "search/search.html", {"username": request.session["username"], "rides": processed, 'recommended_ride': recommended_ride})





def request_ride(request, ride_id):
    """This method processes the request from a user to be part of a ride"""
    initialize_database()

    if not request.session.has_key("username"):
        request.session["alert"] = "Please login to request rides."
        return redirect("index")

    # get ride information from db
    ride = rides_collection.find_one({"_id": ride_id})

    # validation - check for edge cases
    if ride is not None:
        if ride["availability"] == 0:
            message = "Ride has reached max capacity."
        elif ride["owner"] == request.session["username"]:
            message = "Owner of the ride cannot request own rides."
        elif request.session["username"] in ride["confirmed_users"]:
            message = "You are already a confirmed member of this ride."
        else:
            # add/update request to ride
            rides_collection.update_one({"_id": ride_id}, {"$addToSet": {"requested_users": request.session["username"]}})
            message = "Request successful."
        print(message)

    return redirect(requestsViews.requested_rides)
