import pickledb
import time
from utils import fetch_movies_of_today, get_today


while True:
    today = get_today()

    db = pickledb.load('/mubier/mubier/json.db', True, False)
    movies = db.get(today)

    if movies is False:
        movies = fetch_movies_of_today()
        db.set(today, movies)

    print("Sleeping for 5 minutes.")
    time.sleep(60*5)
    print("Waking up.")
