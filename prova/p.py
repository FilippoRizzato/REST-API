from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
 
app = Flask(__name__)
api = Api(app)
 
MOVIES = {
    'movie1': {'movie': 'superman vs batman', 'rating': '9/10', 'comment': 'meh'}}
 
 
def check_if_not_exists(movie_id):
    if movie_id not in MOVIES:
      abort(404, message="{} doesn't exist".format(movie_id))         
 
parser = reqparse.RequestParser()
parser.add_argument('movie')
parser.add_argument('rating')
parser.add_argument('comment')
 
class Movie(Resource):
    def get(self, movie_id):
        check_if_not_exists(movie_id)
        return MOVIES[movie_id]
 
    def delete(self, movie_id):
        check_if_not_exists(movie_id)
        del MOVIES[movie_id]
        return '', 204
 
    def put(self, movie_id):
        args = parser.parse_args()
        movie = {'movie': args['movie']}
        rating = {'rating': args['rating']}
        comment ={'comment': args['comment']}
        MOVIES[movie_id] = [movie, rating, comment]
        return movie, 201
 
class AllMovies(Resource):
    def get(self):
        return MOVIES
 
    def post(self):
        args = parser.parse_args()
        movie_id = int(max(MOVIES.keys()).lstrip('movie')) + 1
        movie_id = 'movie%i' % movie_id
        MOVIES[movie_id] = {'movie': args['movie'], 'rating': args['rating'], 'comment': args['comment']}
        return MOVIES[movie_id], 201
 
 
api.add_resource(AllMovies, '/movies')
api.add_resource(Movie, '/movies/')
 
 
if __name__ == '__main__':
    app.run(debug=True)