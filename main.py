#import hin framwork(Flask)
from flask import Flask,render_template
#import hin other python files and classes
from backend.auth import Authentication

#Main file
#Amo it pag run han system

class Car_Rental:
    def __init__(self):
        self.app = Flask(__name__)

        #replacement hiya for (@app.route('/')
        self.app.add_url_rule('/', 'index', self.show_login_page, methods=['GET'])
        
        Authentication(self.app)
        
    #pag call han html file or a login page pag ig run na an system
    def show_login_page(self):
        return render_template('login.html')
    
    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    app = Car_Rental()
    app.run()



