# https://www.youtube.com/watch?v=GMppyAPbLYk

from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class MovieRatingModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  views = db.Column(db.Integer, nullable=False)
  rating = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return f"Movie(name={name}, views={views}, rating={rating})"


# db.create_all()



#######################################################################################

class HelloWorld(Resource):
# http://127.0.0.1:5000/helloworld/tim/19
# get returns 
  def get(self, name, test):
    return {"name": name, "test": test}

  def post(self):
    return {"data": "POSTED"}

api.add_resource(HelloWorld, "/helloworld/<string:name>/<int:test>")

#######################################################################################

names = {"tim": {"age": 19, "gender": "male"},
         "bill": {"age": 70, "gender": "male"}}

class NameData(Resource):
# http://127.0.0.1:5000/namedata/tim
# get returns {"age": 19,"gender": "male"}

  def get(self, name):
    return names[name]

  def post(self):
    return {"data": "POSTED"}

api.add_resource(NameData, "/namedata/<string:name>/")

#########################################################################################
##################### REST API Memory Example ###########################################
#########################################################################################

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)


videos = {}

def abort_video_id_doesnt_exist(video_id):
  """ aborts video if not found in data """
  if video_id not in videos:
    abort(404, message="Video not found")

def abort_video_id_exists(video_id):
  if video_id in videos:
    abort(409, message="Video already exists with that ID")

class Video(Resource):
  def get(self, video_id):
    abort_video_id_doesnt_exist(video_id)
    return videos[video_id]

  def put(self, video_id):
    abort_video_id_exists(video_id)
    args = video_put_args.parse_args()
    videos[video_id] = args
    return videos[video_id], 201

  def delete(self, video_id):
    abort_video_id_doesnt_exist(video_id)
    del videos[video_id]
    return '', 204

api.add_resource(Video, "/video/<int:video_id>")


#########################################################################################
##################### REST API DB Example ###############################################
#########################################################################################

movie_put_args = reqparse.RequestParser()
movie_put_args.add_argument("name", type=str, help="Name of the movie", required=True)
movie_put_args.add_argument("views", type=int, help="Views of the movie", required=True)
movie_put_args.add_argument("rating", type=int, help="Rating on the movie", required=True)

movie_update_args = reqparse.RequestParser()
movie_update_args.add_argument("name", type=str, help="Name of the movie")
movie_update_args.add_argument("views", type=int, help="Views of the movie")
movie_update_args.add_argument("rating", type=int, help="Rating on the movie")

resource_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'views': fields.Integer,
  'rating': fields.Integer
}

class MovieRatings(Resource):
  @marshal_with(resource_fields) #serializes db query into json
  def get(self, movie_id):
    result = MovieRatingModel.query.filter_by(id=movie_id).first()
    if not result:
      abort(404, message="Could not find video with that id")
    return result

  @marshal_with(resource_fields)
  def put(self, movie_id):
    args = movie_put_args.parse_args()
    result = MovieRatingModel.query.filter_by(id=movie_id).first()
    if result:
      abort(409, message="Video id taken..")
    movie = MovieRatingModel(id=movie_id, name=args['name'], views=args['views'], rating=args['rating'])
    db.session.add(movie)
    db.session.commit()
    return movie, 201

  @marshal_with(resource_fields)
  def patch(self, movie_id):
    args = movie_update_args.parse_args()
    result = MovieRatingModel.query.filter_by(id=movie_id).first()
    if not result:
      abort(404, message="Could not find video with that id")

    if args['name']:
      result.name = args['name']
    if args['views']:
      result.views = args['views']
    if args['rating']:
      result.rating = args['rating']

    db.session.commit()

    return result

  # def delete(self, movie_id):
  #   abort_video_id_doesnt_exist(video_id)
  #   del videos[video_id]
  #   return '', 204

api.add_resource(MovieRatings, "/movie/<int:movie_id>")

##########################################################################################




@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/test')
def say_hello():
  return 'Hello from Server'


if __name__ == "__main__":
  app.run(debug=True)