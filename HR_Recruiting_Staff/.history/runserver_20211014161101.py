from HR_Recruiting_Staff import app
from OpenSSL import SSL

if __name__ == "__main__":
    context = ('local.crt', 'local.key')
    app.run(debug=True,ssl_context=context)