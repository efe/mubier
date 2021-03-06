import pickledb
import sentry_sdk

from flask import Flask, request, render_template
from utils import get_today, get_yesterday
from sentry_sdk.integrations.flask import FlaskIntegration


sentry_sdk.init(
    dsn="https://9e951a2256c847219b8f059806d497bf@o93698.ingest.sentry.io/5541173",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    today = get_today()

    db = pickledb.load('/mubier/mubier/json.db', True, False)
    movies = db.get(today)

    if movies is False:
        # serve cold data.
        yesterday = get_yesterday()
        movies = db.get(yesterday)

    order = int(request.args.get('order', 0))
    movie = movies[order]

    try:
        movies[order + 1]
        next_url = f"/?order={order + 1}"
    except IndexError:
        next_url = "/"

    movie["next_url"] = next_url

    return render_template('index.html', **movie)
