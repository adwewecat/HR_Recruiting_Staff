from HR_Recruiting_Staff import app

from flask import Flask, jsonify
from OpenSSL import SSL


import ssl
context = ssl.SSLContext()
context.load_cert_chain('fullchain.pem', 'privkey.pem')

if __name__ == "__main__":
    context = ('local.crt', 'local.key')
    app.run(debug=True,port=5000,ssl_context=context)