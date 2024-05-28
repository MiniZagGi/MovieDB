import requests

def get_movie_details(api_key, title, year):
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

    # Get the first search result (most relevant)
    movie = search_results['results'][0]
    
    movie_id = movie['id']
    movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    
    response = requests.get(movie_details_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Error fetching movie details from TMDb API")
    
    movie_details = response.json()
    
    return {
        "title": movie_details['title'],
        "release_year": movie_details['release_date'].split("-")[0],
        "directors": get_movie_directors(api_key, movie_id),
        "overview": movie_details.get('overview', 'N/A'),
        "genres": [genre['name'] for genre in movie_details.get('genres', [])]
    }

def get_movie_directors(api_key, movie_id):
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(credits_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Error fetching movie credits from TMDb API")
    
    credits = response.json()
    
    directors = [crew_member['name'] for crew_member in credits['crew'] if crew_member['job'] == 'Director']
    return directors

def main():
    api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1MDZkZmY0MDJkNWFkNjZmZmZiODI5MTQwZjM3ZDM0ZCIsInN1YiI6IjY2MDBiYTAzNzcwNzAwMDE3YzBlMzI5NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Xg5LpL6NiJXcfV70lohf33uCfI0mq21K0wNdaDTDeAM"  # Replace with your TMDb Bearer token
    title = input("Enter movie title: ")
    year = input("Enter movie release year: ")

    try:
        movie_details = get_movie_details(api_key, title, year)
        if movie_details:
            print(f"Title: {movie_details['title']}")
            print(f"Release Year: {movie_details['release_year']}")
            print(f"Directors: {', '.join(movie_details['directors'])}")
            print(f"Overview: {movie_details['overview']}")
            #print(f"Genres: {', '.join(movie_details['genres'])}")
            print(f"Genres: {movie_details['genres']}")
        else:
            print("No movie found for the given title and year.")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
