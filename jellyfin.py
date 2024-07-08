import requests
import os

def search_movie(api_key: str, title: str, year):
  url = "https://jelly.local.mdal.dk/Items/"

  payload = {}
  headers = {
    "Authorization": f"MediaBrowser {api_key}"
  }

  params = {
      "recursive": True,
      "searchTerm": title,
      "years": year,
      "ParentId": "ca66a3e7bbc66972778a197eb546edbf"
  }

  response = requests.request("GET", url, headers=headers, params=params, data=payload)

  return response


def main():
  # Put your API in a varable and export it
  api_key = os.getenv('JELLY_API_KEY')

  # search for a movie
  movie_title: str = ""
  search_results = search_movie(api_key, movie_title, None)
  search_results = search_results.json()
  # movie = search_results["Items"][1]
  # print(movie['Name'])
  #print (type(search_results))
  #print(search_results)


  # Assuming search_results is a dictionary with a key 'Items' that contains a list
  # for i, movie in enumerate(search_results.get('Items', [])):
  #     # Assuming each movie in 'Items' is a dictionary that may have a 'Name' key
  #     movie_name = movie.get('Name', 'Unknown title')
  #     print(f"{i+1}. {movie_name}")





  # for i, movie in enumerate(search_results):
  #    print(f"{i+1}. {movie['Items'][0]} (Name: {movie['Name']})")
  movies_list = [movie.get('Name') for movie in search_results["Items"]]
  for movie_title in movies_list:
    print(movie_title)

# # Assuming search_results is a dictionary with an "Items" key that contains a list of movies
# for i, movie in enumerate(search_results["Items"]):
#     print(f"{i+1}. {movie.get('Name', 'Unknown name')}")


# Get a list of all movies from Jellyfin - DONE
# Search the local DB for movies in the list
if __name__ == "__main__":
  main()