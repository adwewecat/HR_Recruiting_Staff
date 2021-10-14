from HR_Recruiting_Staff import app
from OpenSSL import SSL
context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')  

if __name__ == "__main__":
    context = ('local.crt', 'local.key')
    app.run(debug=True,port=5000,ssl_context=context)