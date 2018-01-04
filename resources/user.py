from flask_restful import Resource, reqparse
from models.user import  UserModel


# class to create a user resource aka sign up 
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    
    # what argument should the parcer expect
    #in the json of the request
    parser.add_argument('username',
            type=str,
            required=True,
            help="This field cannot be left blank.")

    parser.add_argument('password',
            type=str,
            required=True,
            help="This field cannot be left blank.")

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'This user already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created succesfully"}, 201
