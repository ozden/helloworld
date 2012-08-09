import webapp2
import cgi
import re

def escape_html(s):
    return cgi.escape(s, quote = True)

form = """
<form method="post">
    What is your birthday?
    <br>
    <label>
        Month
        <input type="text" name="month" value="%(month)s">
    </label>
    <label>
        Day
        <input type="text" name="day" value="%(day)s">
    </label>
    <label>
        Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br><br>
    <input type="submit">
</form>
"""

formrot="""
<form method="post">
    <br>
    <label>
        <h1>Enter some text to ROT13:</h1>
        <textarea rows="7" cols="66" name="text">%(text)s</textarea>
    </label>
    <br><br>
    <input type="submit" value="Submit">
</form>
"""

formsignup="""
<h2>Signup</h2>
<form method="post">
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(error_username)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(error_password)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(error_verify)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(error_email)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>"""

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                        'September', 'October', 'November', 'December']

def valid_day(day):
        if(day and day.isdigit()):
                day = int(day)
        if(day < 32 and day > 0):
                return day

def valid_month(month):
        if(month):
                month = month.capitalize()
        if(month in months):
                return month

def valid_year(year):
        if(year and year.isdigit()):
                year = int(year)
        if(year < 2020 and year > 1980):
                return year

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, Udacity!')

class WasYourBirthday(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form %{"error": error,
                                       "month": escape_html(month),
                                       "day": escape_html(day),
                                       "year": escape_html(year)})

    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not(month and day and year):
            self.write_form("That doesn't look valid to me, friend.", user_month, user_day, user_year)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")
                    
class Rot13(webapp2.RequestHandler):
    
    def write_form(self,text=""):
        self.response.out.write(formrot % {"text": escape_html(text)})
        
    def get(self):
        self.write_form()
        
    def post(self):
        text=self.request.get('text')
        if text:
            rot13 = text.encode('rot13')
        self.write_form(rot13)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

class SignUp(webapp2.RequestHandler):
    
    def write_form(self, username="", email="", error_username="", error_password="", error_verify="", error_email=""):
        self.response.out.write(formsignup %{"username": escape_html(username),
                                             "email": escape_html(email),
                                             "error_username": escape_html(error_username),
                                             "error_password": escape_html(error_password),
                                             "error_verify": escape_html(error_verify),
                                             "error_email": escape_html(error_email)
                                            })
        
    def get(self):
        self.write_form()
    
    def post(self):
        username=self.request.get('username')
        password=self.request.get('password')
        verify=self.request.get('verify')
        email=self.request.get('email')
        
    

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/birthday',WasYourBirthday),
                               ('/thanks', ThanksHandler),
                               ('/unit2/rot13',Rot13),
                               ('/unit2/signup',SignUp)],
                              debug=True)
