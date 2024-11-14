import streamlit as st
import base64
import os
import mysql.connector
from mysql.connector import Error

# Title for the app
st.title("Great to know you are In")

# Function to load and encode the image
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to your logo
logo_path = r"C:\Users\SuryaKrishna\Desktop\Stock_market_projapp\Stock_market_projappl\logo.png"

# Get the base64 encoded string of the image
logo_base64 = get_image_base64(logo_path)

# MySQL Database Connection
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootkp",
            database="stock_data_db"
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL Database: {e}")
        return None

# Function to execute SQL queries
def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return True
    except Error as e:
        st.error(f"Error executing query: {e}")
        return False
    finally:
        cursor.close()

# Function to check if user exists
def user_exists(connection, email):
    query = "SELECT * FROM users WHERE email = %s"
    cursor = connection.cursor(buffered=True)
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

# Function to register new user
def register_user(connection, full_name, email, mobile, password, referral_code):
    if user_exists(connection, email):
        return False, "User already exists"
    
    query = """INSERT INTO users (full_name, email, mobile, password, referral_code) 
               VALUES (%s, %s, %s, %s, %s)"""
    params = (full_name, email, mobile, password, referral_code)
    if execute_query(connection, query, params):
        return True, "User registered successfully"
    return False, "Error registering user"

# Function to authenticate user
def authenticate_user(connection, email, password):
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor = connection.cursor(buffered=True)
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

# HTML code embedded in Streamlit
html_code = f'''
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="utf-8">
  <title>Sign Up | Log In</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Raleway:wght@300&display=swap">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://apis.google.com/js/platform.js" async defer></script>
  <meta name="google-signin-client_id" content="YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: "Raleway", sans-serif; }}
    html, body {{ display: grid; height: 100%; width: 100%; place-items: center; background: -webkit-linear-gradient(left, #9896f0, #fbc8d5); }}
    ::selection {{ background: #12e8f0; color: #fff; }}
    .wrapper {{ overflow: hidden; max-width: 390px; background: #fff; padding: 30px; border-radius: 5px; box-shadow: 0px 15px 20px rgba(0, 0, 0, 0.1); text-align: center; }}
    .logo {{ margin-bottom: 20px; }}
    .logo img {{ width: 100px; height: auto; border-radius: 10px; }}
    .title-container {{ display: flex; align-items: center; justify-content: center; margin-bottom: 10px; }}
    .title {{ font-size: 24px; font-weight: bold; color: violet; margin-left: 10px; }}
    .powered-by {{ font-size: 14px; color: purple; margin-top: 5px; }}
    .wrapper .title-text {{ display: flex; width: 200%; }}
    .wrapper .title {{ width: 50%; font-size: 35px; font-weight: 600; text-align: center; transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55); }}
    .wrapper .slide-controls {{ position: relative; display: flex; height: 50px; width: 100%; overflow: hidden; margin: 30px 0 10px 0; justify-content: space-between; border: 1px solid lightgrey; border-radius: 5px; }}
    .slide-controls .slide {{ height: 100%; width: 100%; color: #fff; font-size: 18px; font-weight: 500; text-align: center; line-height: 48px; cursor: pointer; z-index: 1; transition: all 0.6s ease; }}
    .slide-controls label.signup {{ color: #000; }}
    .slide-controls .slider-tab {{ position: absolute; height: 100%; width: 50%; left: 0; z-index: 0; border-radius: 5px; background: -webkit-linear-gradient(left, #fbee97, #adedd5); transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55); }}
    input[type="radio"] {{ display: none; }}
    #signup:checked ~ .slider-tab {{ left: 50%; }}
    #signup:checked ~ label.signup {{ color: #fff; cursor: default; user-select: none; }}
    #signup:checked ~ label.login {{ color: #000; }}
    #login:checked ~ label.signup {{ color: #000; }}
    #login:checked ~ label.login {{ cursor: default; user-select: none; }}
    .wrapper .form-container {{ width: 100%; overflow: hidden; }}
    .form-container .form-inner {{ display: flex; width: 200%; }}
    .form-container .form-inner form {{ width: 50%; transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55); }}
    .form-inner form .field {{ height: 50px; width: 100%; margin-top: 20px; }}
    .form-inner form .field input {{ height: 100%; width: 100%; outline: none; padding-left: 15px; border-radius: 5px; border: 1px solid lightgrey; border-bottom-width: 2px; font-size: 17px; transition: all 0.3s ease; }}
    .form-inner form .field input:focus {{ border-color: #12e8f0; }}
    .form-inner form .field input::placeholder {{ color: #999; transition: all 0.3s ease; }}
    form .field input:focus::placeholder {{ color: #b3b3b3; }}
    .form-inner form .pass-link {{ margin-top: 5px; }}
    .form-inner form .signup-link {{ text-align: center; margin-top: 30px; }}
    .form-inner form .pass-link a, .form-inner form .signup-link a {{ color: #0e45dd; text-decoration: none; }}
    .form-inner form .pass-link a:hover, .form-inner form .signup-link a:hover {{ text-decoration: underline; }}
    form .btn {{ height: 50px; width: 100%; border-radius: 5px; position: relative; overflow: hidden; }}
    form .btn .btn-layer {{ height: 100%; width: 300%; position: absolute; left: -100%; background: -webkit-linear-gradient(right, #fbee97, #adedd5, #fbee97, #adedd5); border-radius: 5px; transition: all 0.4s ease; }}
    form .btn:hover .btn-layer {{ left: 0; }}
    form .btn input[type="submit"] {{ height: 100%; width: 100%; z-index: 2; position: relative; background: none; border: none; color: #fff; padding-left: 0; border-radius: 10px; font-size: 20px; font-weight: 500; cursor: pointer; }}
    .google-btn {{ display: flex; justify-content: center; align-items: center; background-color: #4285F4; color: white; height: 50px; border-radius: 5px; cursor: pointer; margin-top: 20px; }}
    .google-btn:hover {{ background-color: #357ae8; }}
    .google-icon {{ background: url('https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg') no-repeat center center; background-size: contain; height: 30px; width: 30px; margin-right: 10px; }}
    .google-btn span {{ font-size: 16px; }}
    .terms-checkbox {{ display: flex; align-items: center; margin-top: 20px; font-size: 14px; }}
    .terms-checkbox input {{ margin-right: 10px; }}
    .error-message {{ color: red; font-size: 14px; margin-top: 10px; }}
    .copyright {{ font-size: 12px; color: #999; margin-top: 20px; }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="logo">
      <div class="title-container">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo">
        <div class="title">Sentiments Decoder</div>
      </div>
      <div class="powered-by">Powered by Sentiments Decoder</div>
    </div>
    <div class="title-text">
      <div class="title login">Account</div>
      <div class="title signup">Account</div>
    </div>
    <div class="form-container">
      <div class="slide-controls">
        <input type="radio" name="slide" id="login" checked>
        <input type="radio" name="slide" id="signup">
        <label for="login" class="slide login">Login</label>
        <label for="signup" class="slide signup">SignUp</label>
        <div class="slider-tab"></div>
      </div>
      <div class="form-inner">
        <form action="#" class="login">
          <div class="field">
            <input type="text" placeholder="Email Address" required>
          </div>
          <div class="field">
            <input type="password" placeholder="Password" required>
          </div>
          <div class="pass-link">
            <a href="#">Reset password?</a>
          </div>
          <div class="field btn">
            <div class="btn-layer"></div>
            <input type="submit" value="Login">
          </div>
          <div class="google-btn" onclick="googleSignIn()">
            <div class="google-icon"></div>
            <span>Sign in with Google</span>
          </div>
          <div class="signup-link">Don't Have Account? <a href="">Create A New</a></div>
        </form>
        <form action="#" class="signup">
          <div class="field">
            <input type="text" placeholder="Full Name" required>
          </div>
          <div class="field">
            <input type="email" placeholder="Email" required>
          </div>
          <div class="field">
            <input type="tel" placeholder="Mobile Number" required>
          </div>
          <div class="field">
            <input type="password" placeholder="Password" required>
          </div>
          <div class="field">
            <input type="password" placeholder="Confirm Password" required>
          </div>
          <div class="field">
            <input type="text" placeholder="Referral Code (optional)">
          </div>
          <div class="terms-checkbox">
            <input type="checkbox" id="terms" required>
            <label for="terms">By signing up you agree to the <a href="https://marketsentimentsdecoder.com/terms-and-conditions/" target="_blank">Terms and Conditions</a> and <a href="https://marketsentimentsdecoder.com/privacy-policy/" target="_blank">Privacy Policy</a>.</label>
          </div>
          <div class="field btn">
            <div class="btn-layer"></div>
            <input type="submit" value="Sign Up">
          </div>
          <div class="google-btn" onclick="googleSignUp()">
            <div class="google-icon"></div>
            <span>Sign up with Google</span>
          </div>
          <div class="error-message" id="error-message"></div>
        </form>
      </div>
    </div>
    <div class="copyright">© 2024 Sentiments Decoder. All rights reserved.</div>
  </div>
  <script>
    const loginText = document.querySelector(".title-text .login");
    const loginForm = document.querySelector("form.login");
    const loginBtn = document.querySelector("label.login");
    const signupBtn = document.querySelector("label.signup");
    const signupLink = document.querySelector("form .signup-link a");
    signupBtn.onclick = (() => {{
      loginForm.style.marginLeft = "-50%";
      loginText.style.marginLeft = "-50%";
    }});
    loginBtn.onclick = (() => {{
      loginForm.style.marginLeft = "0%";
      loginText.style.marginLeft = "0%";
    }});
    signupLink.onclick = (() => {{
      signupBtn.click();
      return false;
    }});

    function googleSignIn() {{
      // Implement Google Sign-In logic here
      console.log("Google Sign-In clicked");
      // You'll need to use Google's OAuth 2.0 flow here
    }}

    function googleSignUp() {{
      // Implement Google Sign-Up logic here
      console.log("Google Sign-Up clicked");
      // You'll need to use Google's OAuth 2.0 flow here
    }}

    // Modify form submission handlers
    loginForm.onsubmit = (e) => {{
      e.preventDefault();
      const email = loginForm.querySelector('input[type="text"]').value;
      const password = loginForm.querySelector('input[type="password"]').value;
      
      // Send login data to Streamlit
      window.parent.postMessage({{
          type: 'login',
          email: email,
          password: password
      }}, '*');
    }};

    const signupForm = document.querySelector("form.signup");
    const errorMessage = document.getElementById("error-message");

    signupForm.onsubmit = (e) => {{
      e.preventDefault();
      const fullName = signupForm.querySelector('input[placeholder="Full Name"]').value;
      const email = signupForm.querySelector('input[type="email"]').value;
      const mobile = signupForm.querySelector('input[type="tel"]').value;
      const password = signupForm.querySelector('input[placeholder="Password"]').value;
      const confirmPassword = signupForm.querySelector('input[placeholder="Confirm Password"]').value;
      const referralCode = signupForm.querySelector('input[placeholder="Referral Code (optional)"]').value;
      const termsChecked = signupForm.querySelector('#terms').checked;

      if (password !== confirmPassword) {{
        errorMessage.textContent = "Passwords do not match.";
        return;
      }}

      if (!termsChecked) {{
        errorMessage.textContent = "Please accept the Terms and Conditions.";
        return;
      }}

      // Send signup data to Streamlit
      window.parent.postMessage({{
        type: 'signup',
        fullName: fullName,
        email: email,
        mobile: mobile,
        password: password,
        referralCode: referralCode
      }}, '*');
    }};
  </script>
</body>
</html>
'''

# Render the HTML code in the Streamlit app
st.components.v1.html(html_code, height=1000)

# Handle form submissions
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

if not st.session_state.form_submitted:
    connection = create_db_connection()
    if connection:
        placeholder = st.empty()
        
        # Listen for messages from JavaScript