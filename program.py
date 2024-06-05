import requests
import mysql.connector
from flask import Flask, render_template

####

####


def get_movie_details(api_key: str, title: str, year):
    """
    Retrieves movie details from the TMDb API based on the provided title and year.

    Parameters:
    - api_key (str): The API key for accessing the TMDb API.
    - title (str): The title of the movie to search for.
    - year (int): The year of the movie to search for.

    Returns:
    - list: A list of movie details matching the search criteria. If no results are found, returns None.
    """
    search_url = "https://api.themoviedb.org/3/search/movie"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "query": title,
        "year": year
    }
    
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception("Error fetching data from TMDb API")
    
    search_results = response.json()
    if not search_results['results']:
        return None

    return search_results['results']

def get_movie_info_by_id(api_key: str, movie_id: int):
    """
    Retrieves movie information from The Movie Database (TMDb) API based on the provided movie ID.

    Parameters:
    - api_key (str): The API key for accessing TMDb API.
    - movie_id (int): The ID of the movie to retrieve information for.

    Returns:
    - dict: A dictionary containing the movie information in JSON format.

    Raises:
    - Exception: If the API request fails or returns a non-200 status code.
    """

    # Construct the URL for the API request
    search_url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    # Make the API request
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Error fetching data from TMDb API")
    
    search_results = response.json()

    return search_results

def get_movie_directors(api_key, movie_id: int):
    """
    Retrieves the directors of a movie from the TMDb API.

    Parameters:
    - api_key (str): The API key for accessing the TMDb API.
    - movie_id (int): The ID of the movie.

    Returns:
    - list: A list of dictionaries containing the names of the directors.

    Raises:
    - Exception: If there is an error fetching movie credits from the TMDb API.
    """
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(credits_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Error fetching movie credits from TMDb API")
    
    credits = response.json()
    
    # Gets the directors name from the credits and returns only directors
    directors = [{'name': crew_member['name']} for crew_member in credits['crew'] if crew_member['job'] == 'Director']
    return directors

def find_movie_local(cursor, title, release_year):
    '''
    Search local database for a movie with the given title and release year.

    Parameters:
        cursor (cursor): The database cursor object.
        title (str): The title of the movie to search for.
        release_year (int): The release year of the movie to search for.

    Returns:
        int or None: The MovieID of the found local movie, or None if no movie is found.
    '''
    select_query = """
        SELECT `MovieID` FROM `Movie` WHERE `Title` = %s AND `ReleaseYear` = %s
    """
    cursor.execute(select_query, (title, release_year))
    result = cursor.fetchone()
    return result[0] if result else None

def insert_movie(cursor, title, release_year):
    """
    Inserts a movie into the database if it doesn't already exist.

    Args:
        cursor: The database cursor object.
        title (str): The title of the movie.
        release_year (int): The release year of the movie.

    Returns:
        int: The ID of the inserted movie for use in fx. relation tables like movie_director

    """
    movie_id = find_movie_local(cursor, title, release_year)
    if movie_id:
        return movie_id
    
    insert_query = """
        INSERT INTO `Movie` (`Title`, `ReleaseYear`)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (title, release_year))
    return cursor.lastrowid

def insert_director(cursor: str, full_name: str):
    """
    Inserts a director into the database if they don't already exist and returns the DirectorID.

    Args:
        cursor: The database cursor object.
        full_name (str): The full name of the director.

    Returns:
        int: The DirectorID of the inserted or existing director.
    """
    # Checks if the director exits
    first_name, last_name = full_name.split(' ', 1)
    select_query = """
        SELECT `DirectorID` FROM `Director` WHERE `FirstName` = %s AND `LastName` = %s
    """
    cursor.execute(select_query, (first_name, last_name))
    result = cursor.fetchone()
    if result:
        return result[0]
    # Insert the new director
    insert_query = """
        INSERT INTO `Director` (`FirstName`, `LastName`)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (first_name, last_name))
    return cursor.lastrowid

def insert_movie_director_relation(cursor, movie_id: int, director_id: int):
    select_query = """
        SELECT 1 FROM `Movie_Director` WHERE `Movie_MovieID` = %s AND `Director_DirectorID` = %s
    """
    cursor.execute(select_query, (movie_id, director_id))
    result = cursor.fetchone()
    if result:
        return
    
    insert_query = """
        INSERT INTO `Movie_Director` (`Movie_MovieID`, `Director_DirectorID`)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (movie_id, director_id))

def get_media_type_id(cursor, media_type):
    """
    Retrieves the MediaTypeID from the database based on the given media_type.

    Args:
        cursor: The database cursor object.
        media_type (str): The type of media.

    Returns:
        int: The MediaTypeID corresponding to the given media_type.

    Raises:
        ValueError: If the media_type is not found in the database.
    """
    select_query = "SELECT `MediaTypeID` FROM `MediaType` WHERE `Type` = %s"
    cursor.execute(select_query, (media_type,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        raise ValueError(f"Media type '{media_type}' not found in database")
    
def get_avalible_media_types(cursor):
    """
    Retrieves all available media types from the `MediaType` table.

    Args:
        cursor: The database cursor object.

    Returns:
        A tuple containing all the media types in the `MediaType` table.
    """
    select_query = "SELECT `Type` FROM `MediaType`"
    cursor.execute(select_query)
    result = cursor.fetchall()
    # returns a tuple
    return result

def is_media_backed_up(cursor, movie_id, media_type_id):
    """
    Checks if a specific media type for a movie is backed up.

    Args:
        cursor: The database cursor object.
        movie_id: The ID of the movie.
        media_type_id: The ID of the media type.

    Returns:
        True if the media type is backed up, False if it is not backed up, or None if there is no entry for the given movie and media type.
    """
    select_query = """
        SELECT `IsBackedUp` FROM `Movie_MediaType` WHERE `Movie_MovieID` = %s AND `MediaType_MediaTypeID` = %s
    """
    cursor.execute(select_query, (movie_id, media_type_id))
    resultTuple = cursor.fetchone()

    # Returns true or false if there is a row in table else return None
    if resultTuple is not None:
        result = bool(resultTuple[0])
        return result
    else:
         # returns None when a row with matching values does not exsit
        return None

def update_backup_status(cursor, movie_id, media_type_id, backup_status: bool, own_status: bool):
    """
    Updates the backup status and own status of a movie media type in the database.

    Args:
        cursor: The database cursor object.
        movie_id: The ID of the movie.
        media_type_id: The ID of the media type.
        backup_status: The backup status to be updated (True or False).
        own_status: The own status to be updated (True or False).

    Returns:
        None
    """
    update_query = """
        INSERT INTO `Movie_MediaType` (`Movie_MovieID`, `MediaType_MediaTypeID`, `IsBackedUp`) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE `IsBackedUp` = %s, `IsOwned` = %s
    """
    # There is multiple backup status's as values gets used one by one. 
    cursor.execute(update_query, (movie_id, media_type_id, backup_status, backup_status, own_status))

def get_all_movies(cursor):
    getMovies = """
    SELECT `Title` FROM `Movie`
"""
    cursor.execute(getMovies)
    resault = cursor.fetchall()

    print(resault)
    return resault

def printMovieDetails(movie_details, directors):
    """
    Prints the details of a movie.

    Args:
        movie_details (dict): A dictionary containing the details of the movie.
            It should have the following keys: 'title', 'release_date', 'overview', 'genres'.
        directors (list): A list of dictionaries containing the details of the directors.
            Each dictionary should have the key 'name'.

    Returns:
        None
    """
    print(f"Title: {movie_details['title']}")
    print(f"Release Year: {movie_details['release_date'].split('-')[0]}")
    print(f"Directors: {', '.join(director['name'] for director in directors)}")
    print(f"Overview: {movie_details.get('overview', 'N/A')}")
    print(f"Genres: {', '.join([genre['name'] for genre in movie_details.get('genres', [])])}")

def get_yes_or_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'no']:
            return response
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def jelly_movie_search(movie, payload, headers):
    try:
        url = f"https://jelly.local.mdal.dk/Items/?recursive=True&SourceType=Library&searchTerm={movie}&ParentId=ca66a3e7bbc66972778a197eb546edbf"
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
        return False
    try:
        jelly_movie = response.json()
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
        return False
    try:
        jelly_movie_name = jelly_movie['Items'][0]['Name']
    except (KeyError, IndexError) as e:
        print(f"Failed to access data from response: {e}")
        return False
    # check if movie is found and return
    return jelly_movie_name == movie



def main():
    api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1MDZkZmY0MDJkNWFkNjZmZmZiODI5MTQwZjM3ZDM0ZCIsInN1YiI6IjY2MDBiYTAzNzcwNzAwMDE3YzBlMzI5NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Xg5LpL6NiJXcfV70lohf33uCfI0mq21K0wNdaDTDeAM"  # Replace with your TMDb Bearer token

    # Database connection setup
    db_connection = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="MovieDB"
    )
    cursor = db_connection.cursor()
#### Jellyfin

    payload = {}
    headers = {
    'Authorization': 'MediaBrowser Token=5731b055aaa14a49826f53b950b4c75d'
    }


    # ob = response.json()
    # print(response.text)
    # film = ob['Items'][0]
    # print(film['Name'])

    # Jelly is put here for now. Have to make a swtich later
    
    # Update the backup state if movie is found
    movies = get_all_movies(cursor)
    for movie in movies:
        movieFound = jelly_movie_search(movie[0], payload, headers)
        if movieFound == True:
            print(f"{movie[0]} is found")
    try:
        while True:
            # Asks the user for a movie to search for
            title = str(input("Enter movie title: "))
            # Allows year to be empty. Sets to None if input is not an int
            try:
                year = int(input("Enter movie release year: "))
            except ValueError:
                year = None

            # Processes the resutalt of the user search. Then makes a list to print
            search_results = get_movie_details(api_key, title, year)
            if search_results:
                print("Movies found:")
                for i, movie in enumerate(search_results):
                    print(f"{i+1}. {movie['title']} (Release Date: {movie['release_date']})")
                
                # Gets the user to select the movie index they want to add to database
                selected_movie_index = int(input("Select the movie number you want details for: ")) - 1
                selected_movie = search_results[selected_movie_index]
                # Gets only the id value from the selected_movie. This is used to then search by ID on TMDB
                movie_id = selected_movie['id']

                # Get details of the chosen movie
                movie_details = get_movie_info_by_id(api_key, movie_id)
                directors = get_movie_directors(api_key, movie_id)
                # Print the movie details to screen
                printMovieDetails(movie_details, directors)
            else:
                print("No movie found for the given title and year.")
                
            # Insert the movie into the database or find the existing one. The movie_ID from local database is used to create a relationship with director
            movie_db_id = insert_movie(cursor, movie_details['title'], movie_details['release_date'].split('-')[0])

            # Insert directors and their relationships with the movie. Loops them and then calls insert_director and insert_movie_director_relation to create a relectionshiop with the movie
            for director in directors:
                director_id = insert_director(cursor, director['name'])
                insert_movie_director_relation(cursor, movie_db_id, director_id)

            # Handles backup state and is_owned state
            media_types = get_avalible_media_types(cursor)
            for media_type in media_types:
                media_type_id = get_media_type_id(cursor, media_type[0])
                backed_up = is_media_backed_up(cursor, movie_db_id, media_type_id)
                if backed_up is None:
                    # Gets True if user inputs yes otherrise False
                    own_status = get_yes_or_no(f"Do you own the movie in {media_type[0]}? (yes/no): ") == 'yes'
                    if own_status:
                        is_backed_up = get_yes_or_no(f"Has this movie been backed up on {media_type[0]}? (yes/no): ") == 'yes'
                        update_backup_status(cursor, movie_db_id, media_type_id, is_backed_up, own_status)
                else:
                    print(f"The movie is already backed up on {media_type[0]}.")
                    
            # commits to database. Nothing is done to the database before it is commited
            db_connection.commit()

            # Asks the user if there is more movies to add, if no then break out of the loop
            if get_yes_or_no("Want to add another movie? ") == 'no':
                break
    except Exception as e:
        print(str(e))
    finally:
        cursor.close()
        db_connection.close()
        

if __name__ == "__main__":
    main()
