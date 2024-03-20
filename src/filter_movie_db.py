from langdetect import detect
import json

def _filter_movie_json():
    with open("src/movies.json", encoding="utf8") as my_file:
        for line in my_file: 
            movie_json = json.loads(line)
            title = movie_json["original_title"]
            pop = movie_json["popularity"]
            try:
                if(detect(title) == 'en' and pop > 26):
                    print(f"{title}")
                    with open("src/filtered_movies.json", "a", encoding="utf8") as filtered_file:
                        filtered_file.write(line)
            except Exception as e: 
                print(e)

_filter_movie_json()