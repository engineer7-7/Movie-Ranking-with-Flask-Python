# import libraries
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

# create flask instance
app = Flask(__name__)

# create secret key
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# create form
class EditForm(FlaskForm):
    rating_form = StringField('Your Rating Out of 10', validators=[DataRequired()])
    review_form = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')


# create new form to add movie
class AddMovieForm(FlaskForm):
    movie_title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


# CREATE DB
# create base class
class Base(DeclarativeBase):
    pass


# create SQLAlchemy object
db = SQLAlchemy(model_class=Base)

# config the db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

# initialize the app with extension
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# finalize the creation of the table
with app.app_context():
    db.create_all()


# display route
@app.route("/")
def home():
    # query to get all the data based on ratins (asceding order)
    movie_ranking = db.session.execute(db.Select(Movie).order_by(Movie.rating.desc())).scalars().all()
    # enumerate to get the ranking
    for index, movie in enumerate(movie_ranking, start=1):
        movie.ranking = index
    db.session.commit()

    result = db.session.execute(db.select(Movie).order_by(Movie.rating.asc()))
    movies = result.scalars().all()

    return render_template("index.html", movies=movies)


# update route
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    movie_form = EditForm()
    movie_id = request.args.get('id')
    movie_to_update = db.get_or_404(Movie, movie_id)

    if movie_form.validate_on_submit() and request.method == 'POST':
        movie_to_update.rating = movie_form.rating_form.data
        movie_to_update.review = movie_form.review_form.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=movie_form, movie=movie_to_update)


# delete route
@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


# route for adding movies
@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    add_form = AddMovieForm()
    if add_form.validate_on_submit() and request.method == 'POST':
        url = f"https://api.themoviedb.org/3/search/movie?query={add_form.movie_title.data}&include_adult=false&language=en-US&page=1"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZWU4ZDA5OGIyNjhiN2Y4YTRhMzFlZmYyMGNjN2ZhYSIsIm5iZiI6MTczMDQ1NzY5MC43NTg1OTQzLCJzdWIiOiI2NzI0YWI3NWE2MTZiYmU3MTVlMWUzNDEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.n1YdM8RnpwskGE7cp_WzAF9pkqONGVXkdfavg4efdrY"
        }

        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            results = data['results']

        else:
            return f'Error with status code {response.status_code}'

        return render_template('select.html', results=results)
    return render_template('add.html', form=add_form)


@app.route('/new_add')
def add_new_movie():
    movie_id = request.args.get('id')
    if not movie_id:
        return 'No ID'
    else:
        img_url = "https://image.tmdb.org/t/p/w500/"
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZWU4ZDA5OGIyNjhiN2Y4YTRhMzFlZmYyMGNjN2ZhYSIsIm5iZiI6MTczMDQ1NzY5MC43NTg1OTQzLCJzdWIiOiI2NzI0YWI3NWE2MTZiYmU3MTVlMWUzNDEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.n1YdM8RnpwskGE7cp_WzAF9pkqONGVXkdfavg4efdrY"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            title = data['title']
            year = data['release_date']
            overview = data['overview']
            img_url = img_url + data['poster_path']
            with app.app_context():
                movie = Movie(id=movie_id, title=title, year=year, description=overview, img_url=img_url)
                db.session.add(movie)
                db.session.commit()

            return redirect(url_for('edit', id=movie_id))


if __name__ == '__main__':
    app.run(debug=True)
