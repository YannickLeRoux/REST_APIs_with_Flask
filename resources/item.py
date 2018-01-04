from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):  # Defining the resource
    parser = reqparse.RequestParser()
        # price and store_id are gonna be the only field accepted, any other entered is gonna
        # be deleted and not passed to the api. IT BELONGS TO THE CLASS Item!
        # True for every instance
    parser.add_argument('price',
            type = float,
            required = True,
            help = 'This message cannot be left blank'
            )
    parser.add_argument('store_id',
            type = int,
            required = True,
            help = 'Every Item needs a store_id'
            )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'message':'Item not found'}, 404


    def post(self, name):
        '''
        Creates an item. Can use force=True or silent=True in get_json().
        force skip read the header content-type, silent doesnt return an error
        but just 'None'
        '''        
        if ItemModel.find_by_name(name):
            return {'message':"Item named '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args() # check the data is valid
 
        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured whem inserting the item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
        
        return {'message':'Item has been deleted'}


    def put(self, name):
        data = Item.parser.parse_args() # check the data is valid
        
        item = ItemModel.find_by_name(name)        

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
            # could write **data as well
        else:
            item.price = data['price']

        item.save_to_db()
        
        return item.json()


class ItemList(Resource):

    def get(self):
        items = ItemModel.query.all()
        return {'items': [item.json() for item in ItemModel.query.all()]}
        


