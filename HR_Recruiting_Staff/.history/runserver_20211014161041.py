from HR_Recruiting_Staff import app
from OpenSSL import SSL

if __name__ == "__main__":
    context = ('local.crt', 'local.key')
    app.run(debug=True,port=5000,ssl_context=context)