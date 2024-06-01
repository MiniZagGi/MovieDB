import requests
import mysql.connector

def get_movie_details(api_key, title, year):
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

def get_movie_by_id(api_key, movie_id):
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

def get_movie_directors(api_key, movie_id):
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(credits_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Error fetching movie credits from TMDb API")
    
    credits = response.json()
    
    directors = [{'name': crew_member['name']} for crew_member in credits['crew'] if crew_member['job'] == 'Director']
    return directors

def find_movie(cursor, title, release_year):
    '''Search local database for movie and retuns that if found else None'''
    select_query = """
        SELECT `MovieID` FROM `Movie` WHERE `Title` = %s AND `ReleaseYear` = %s
    """
    cursor.execute(select_query, (title, release_year))
    result = cursor.fetchone()
    return result[0] if result else None

def insert_movie(cursor, title, release_year):
    movie_id = find_movie(cursor, title, release_year)
    if movie_id:
        return movie_id
    
    insert_query = """
        INSERT INTO `Movie` (`Title`, `ReleaseYear`)
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (title, release_year))
    return cursor.lastrowid

def insert_director(cursor, full_name):
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

def insert_movie_director_relation(cursor, movie_id, director_id):
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
    select_query = "SELECT `MediaTypeID` FROM `MediaType` WHERE `Type` = %s"
    cursor.execute(select_query, (media_type,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        raise ValueError(f"Media type '{media_type}' not found in database")

def is_media_backed_up(cursor, movie_id, media_type_id):
    select_query = """
        SELECT `IsBackedUp` FROM `Movie_MediaType` WHERE `Movie_MovieID` = %s AND `MediaType_MediaTypeID` = %s
    """
    cursor.execute(select_query, (movie_id, media_type_id))
    result = cursor.fetchone()
    return result[0] if result else False

def update_backup_status(cursor, movie_id, media_type_id, status):
    update_query = """
        INSERT INTO `Movie_MediaType` (`Movie_MovieID`, `MediaType_MediaTypeID`, `IsBackedUp`) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE `IsBackedUp` = %s
    """
    cursor.execute(update_query, (movie_id, media_type_id, status, status))

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

    # Asks the user for a movie to search for
    title = str(input("Enter movie title: "))
    year = int(input("Enter movie release year: "))

    try:
        # Processes the resutalt of the user search. Then makes a list to print
        search_results = get_movie_details(api_key, title, year)
        if search_results:
            print("Movies found:")
            for i, movie in enumerate(search_results):
                print(f"{i+1}. {movie['title']} (Release Date: {movie['release_date']})")
            
            selected_movie_index = int(input("Select the movie number you want details for: ")) - 1
            selected_movie = search_results[selected_movie_index]
            # Gets only the id value from the selected_movie. This is used to then search by ID
            movie_id = selected_movie['id']

            # Get details of the chosen movie
            movie_details = get_movie_by_id(api_key, movie_id)
            directors = get_movie_directors(api_key, movie_id)


            printMovieDetails(movie_details, directors)

            # Insert the movie into the database or find the existing one. The movie_ID from local database is used to create a relationship with director
            movie_db_id = insert_movie(cursor, movie_details['title'], movie_details['release_date'].split('-')[0])

            # Insert directors and their relationships with the movie
            for director in directors:
                director_id = insert_director(cursor, director['name'])
                insert_movie_director_relation(cursor, movie_db_id, director_id)

            # Handle media types and backup statuses
            media_types = ['DVD', 'Blu-Ray', 'UHD']
            for media_type in media_types:
                media_type_id = get_media_type_id(cursor, media_type)
                backed_up = is_media_backed_up(cursor, movie_db_id, media_type_id)
                if backed_up is None:
                    own_status = input(f"Do you own the movie in {media_type}? (yes/no): ").strip().lower() == 'yes'
                    if own_status:
                        is_backed_up = input(f"Has this movie been backed up on {media_type}? (yes/no): ").strip().lower() == 'yes'
                        update_backup_status(cursor, movie_db_id, media_type_id, is_backed_up)
                else:
                    print(f"The movie is already backed up on {media_type}.")
            
            db_connection.commit()

        else:
            print("No movie found for the given title and year.")
    except Exception as e:
        print(str(e))
    finally:
        cursor.close()
        db_connection.close()

if __name__ == "__main__":
    main()
