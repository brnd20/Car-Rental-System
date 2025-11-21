from flask import Flask, render_template, request
from database.mydatabase import Database
from werkzeug.security import generate_password_hash, check_password_hash

class Authentication:
    def __init__(self, app):
        self.app = app
        self.mydatabase = Database().get_connection()
        

        self.app.add_url_rule('/register', 'register', self.register_user, methods=['GET', 'POST'])
        self.app.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        
        
    #gin c-check kun mayda hiya account ha database
    def check_login(self, username):
        try:
            cursor = self.mydatabase.cursor()
            query = "SELECT Password FROM customers WHERE Username=%s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()  
            print("DB result:", result)  # debug
            if result:
                return result[0]  
            else:
                print("No such username found")
                return None
        except Exception as e:
            print("Database error:", e)
            return None
        
    #after ma check if mayda account it user ma login na
    def login(self):
        if request.method == 'POST':
            username = request.form.get('username').strip().lower()
            password = request.form.get('password').strip()

            hashed_password = self.check_login(username)

            
            if hashed_password and check_password_hash(hashed_password, password):
                return "Naka login na"
            else:
                return "Invalid username or password."
        else:
            return render_template('login.html')

    #gin kakada an data ha database
    def register_user(self):
        if 'first_name' in request.form:
                # gin kukuha an input has user ha "form" an "<form></form> ha html"
                username = request.form.get('username')
                password = request.form.get('password')
                first_name = request.form.get('first_name')
                middle_name = request.form.get('middle_name')
                last_name = request.form.get('last_name')
                email = request.form.get('email')
                address = request.form.get('address')
                phone_number = request.form.get('phone')
                
                #ig encrypt niya an password han user
                encrypted_pass = generate_password_hash(password, method='pbkdf2:sha256')
                
                try: 
                    #pag check if mayda kapareho na username o email
                    cursor = self.mydatabase.cursor()
                    cursor.execute("SELECT * FROM customers WHERE Username=%s OR Email=%s", (username, email))
                    if cursor.fetchone():
                        return "Username or email already exists."
                    
                    #amo na ini an syntax han pag kada han data or inputs han user ha database
                    query = """
                        INSERT INTO customers (First_Name, Middle_Name, Last_Name, Address, Email, Phone_Number, Username, Password)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """  
                    data = (first_name, middle_name, last_name, address, email, phone_number, username, encrypted_pass)
                    cursor.execute(query, data)
                    self.mydatabase.commit()
                    
                    return f'Nakada na ha database'
                    
                except Exception as e:
                    return f"An error occurred: {e}"
        else:
            return render_template('register.html')
