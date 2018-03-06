from flask import Flask
from flask_restful import Resource, Api
class CheckForUpdates(Resource):
    def get(self):
        return {'h1' : 'You get some updates and are really happy!'}
