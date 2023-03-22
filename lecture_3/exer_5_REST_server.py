#!/usr/bin/env python
# encoding: utf8
#
# Copyright © Ruben Ruiz Torrubiano <ruben.ruiz at fh-krems dot ac dot at>,
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    3. Neither the name of the owner nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

pets = {}

#every bird has : name species and color
"""

birds = {
    'bird1': {'name': 'bird1', 'species': 'eagle', 'color': 'white'},
}


"""

birds = {}

class Pets(Resource):
    def get(self, pet_name):
        return {pet_name: pets[pet_name]}

    def put(self, pet_name):
        pets[pet_name] = request.form['data']
        return {pet_name: pets[pet_name]}
    
    #delete pet from pets
    def delete(self, pet_name):
        del pets[pet_name]
        return {'status': 'success'}
    
    def post(self, pet_name):
        if pet_name in pets:
            pet_name = pet_name + '_1'
        
        pets[pet_name] = request.form['data']
        return {pet_name: pets[pet_name]}
    
class Birds(Resource):
    def get(self, bird_name):
        return {bird_name: birds[bird_name]}
    
    def post(self, bird_name):
        if bird_name in birds:
            bird_name = bird_name + '_1'
        
        birds[bird_name] = request.form['data']
        return {bird_name: birds[bird_name]}
    def delete(self, bird_name):
        del birds[bird_name]
        return {'status': 'success'}


api.add_resource(Pets, '/pets/api/<string:pet_name>')

if __name__ == '__main__':
    app.run(debug=True)
