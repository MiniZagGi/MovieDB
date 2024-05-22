import requests
import json
import pprint
# Used to parse URL safely
from urllib.parse import quote

def getUserSearch(prompt):
    '''Validates input is not empty'''
    while True:
        user_input = input(prompt)
        if user_input:  # This will be False if the string is empty
            # Make the title url safe
            user_input = quote(user_input)
            return user_input
        else:
            print("Invalid input. Please enter a non-empty string.")

def getMovieYear(prompt):
    '''Asks the user for a year. Checks if the year is after 1800. 0 for skip'''
    while True:
        try:
            user_input = int(input(prompt))
            if user_input == 0:
                # 0 is used to skip year. If the user doesen't know the year.
                user_input = ""
                return user_input
            elif user_input < 1800:
                print("Please enter a year later than 1800")
            else:
                return user_input
        except ValueError:
            print("Invalid input. Please enter a number.")

def getMovieInfo(prompt):
    '''Expands the movie information based on the user input from list. Has to be int'''
    try:
        userInput = int(input(prompt))
        pprint.pprint(movieData["results"][userInput])
    except ValueError:
        print("Invalid input. Please enter an integer.")

# Asks the user for what movie title to search for and the relesse year
title = getUserSearch("Enter a movie title: ")
year = getMovieYear("Enter a year: ")

url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=False&language=en-US&primary_release_year={year}&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1MDZkZmY0MDJkNWFkNjZmZmZiODI5MTQwZjM3ZDM0ZCIsInN1YiI6IjY2MDBiYTAzNzcwNzAwMDE3YzBlMzI5NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Xg5LpL6NiJXcfV70lohf33uCfI0mq21K0wNdaDTDeAM"
}

response = requests.get(url, headers=headers)

movieData = response.json()

for i, movie in enumerate(movieData["results"]):
    print(f"{i}: {movie['title']} MovieID: {movie['id']}")

# Print the movie in the list
getMovieInfo("Enter a movie from the list")

#print(data['results'][0]['title'])

# Goals

# 1. Print out all the movies found in a list # DONE
# 2. Make it so a user can choose to print all information about a movie on the list # DONE
# 3. Make user input search for movies # DONE

# 4. Create the gerna table and populate it with data from the MovieDB
# 5. Prepare the movie data to be put into the DB
