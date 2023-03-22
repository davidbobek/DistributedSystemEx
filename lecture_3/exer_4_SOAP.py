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

from spyne.application import Application
from spyne.decorator import srpc
from spyne.protocol.soap import Soap11
from spyne.service import ServiceBase
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer
from spyne.model.primitive import String
from spyne.server.wsgi import WsgiApplication

class HelloService(ServiceBase):
    """
    A simple Hello service that outputs 'Hello, <argument>'
    """
    
    #as many as we need to
    
    @srpc(String, _returns=String)
    def fibonacci_number(number):
        number = int(number)
        #calculate fibonacci number without recursion
        fibonacciSeries = [0,1]

        if number>2:
            for i in range(2, number):
                #next elment in series = sum of its previous two numbers
                nextElement = fibonacciSeries[i-1] + fibonacciSeries[i-2]
                #append the element to the series
                fibonacciSeries.append(nextElement)

        print(fibonacciSeries)
        return str(fibonacciSeries)
        
    
    @srpc(String, _returns=String)
    def say_hello(name):
        return "Hello, " + name + "!"
    
import logging

if __name__=='__main__':
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    application = Application([HelloService], 'ds_examples.soap.hello',
                              in_protocol=Soap11(), out_protocol=Soap11())

    wsgi_app = WsgiApplication(application)

    server = make_server('0.0.0.0', 2452, wsgi_app)

    print("listening to http://127.0.0.1:2452")
    print("wsdl is at: http://localhost:2452/?wsdl")

    server.serve_forever()
