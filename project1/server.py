from flask import Flask, render_template, request, redirect, session, flash
from mysqlconn import connectToMySQL
from flask_bcrypt import Bcrypt    
import os    
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret' 
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template('login.html')


@app.route('/log',methods=['POST'])
def logIn():
    is_valid = True

    if len(request.form['username']) < 1:
        is_valid = False
        flash("Please enter your username")
    if len(request.form['password']) < 1:
        is_valid = False
        flash("Please enter your password")
    if not is_valid:
        return redirect("/")
    else:
        mysql = connectToMySQL('project1')
        query = "SELECT * FROM users WHERE username = %(u)s"
        data = {
            'u': request.form['username']
        }
        user = mysql.query_db(query, data)
        if user:
            hashed_password = user[0]['password']
            if bcrypt.check_password_hash(hashed_password, request.form['password']):
                session['user_id'] = user[0]['user_id']
                return redirect("/success",)
            else:
                flash("Password is invalid")
                return redirect("/")
        else:
            flash("Please use a valid email address")
            return redirect("/")
    


@app.route('/reg',methods=['POST'])
def add_users1():
    is_valid = True
    
    if len(request.form['firstname']) < 2:
        is_valid = False
        flash("First name must be at least 2 characters long")
    if len(request.form['lastname']) < 2:
        is_valid = False
        flash("Last name must be at least 2 characters long")
    if len(request.form['password']) < 8:
        is_valid = False
        flash("Password must be at least 8 characters long")
    if len(request.form['username'])<1:
        is_valid=False
        flash("Fill in the username")


    mysql= connectToMySQL('project1')
    validate_email_query = 'SELECT user_id FROM users WHERE email=%(email)s;'
    form_data = {
        'email': request.form['email']
    }
    existing_users =mysql.query_db(validate_email_query, form_data)

    if existing_users:
        flash("Email already in use")
        is_valid = False

    mysql= connectToMySQL('project1')
    validate_email_query1 = 'SELECT user_id FROM users WHERE username=%(u)s;'
    form_data1 = {
        'u': request.form['username']
    }
    existing_users1 =mysql.query_db(validate_email_query1, form_data1)

    if existing_users1:
        flash("Username already in use")
        is_valid = False
    
    if is_valid:
        mysql = connectToMySQL('project1')
        # build my query
        query = "INSERT into users (firstName, lastName, email,username, password) VALUES (%(fn)s, %(ln)s, %(email)s, %(u)s, %(pass)s)"
        # pass revlevant to with my query
        data = {
            'fn': request.form['firstname'],
            'ln': request.form['lastname'],
            'pass': bcrypt.generate_password_hash(request.form['password']),
            'email': request.form['email'],
            'u':request.form['username']
        }
        # commit the query
        user_id = mysql.query_db(query, data)
        session['user_id'] = user_id

        return redirect("/success")
    else: # otherwise, reidrect and show errors
        return redirect("/register")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/register')
def add_users():
    return render_template('signup.html')

@app.route('/success')
def home():
    if 'user_id' not in session:
        return redirect('/')

    mysql = connectToMySQL('project1')
    query = "SELECT * FROM users WHERE users.user_id = %(id)s"
    data = {'id': session['user_id']}
    user = mysql.query_db(query, data)

    mysql = connectToMySQL('project1')
    query = "SELECT user_id1 FROM followed_user WHERE user_id = %(id)s"
    data = {'id': session['user_id']}
    followed_users = [user['user_id1'] for user in mysql.query_db(query, data)]
    
    if followed_users:
        mysql = connectToMySQL('project1')
        query = "SELECT * FROM users WHERE users.user_id = %(id)s"
        data = {'id': session['user_id']}
        user = mysql.query_db(query, data)

        mysql = connectToMySQL('project1')
        query = "SELECT users.user_id,users.username,posts.content,posts.post_id,count(likes.post_id) as tot,count(comments.post_id) as tot1 FROM posts join users on posts.user_id = users.user_id left join likes on posts.post_id= likes.post_id left join comments on comments.post_id=posts.post_id where posts.user_id in %(f)s or users.user_id=%(u)s group by posts.post_id order by posts.post_id desc"
        data1={
            'f':tuple(followed_users),
            'u':session['user_id']
        }
        photos = mysql.query_db(query,data1) 
        return render_template("home.html", user=user[0],photoss=photos)
    return render_template("home.html",user=user[0])

app.config["IMAGE_UPLOADS"] = "static/img"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["file"]
            if image.filename == "":
                print("No filename")
                return redirect(request.url)
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print(filename)
                mysql = connectToMySQL('project1')
                query = "insert into posts (content,user_id) values (%(con)s,%(id)s);"
                data = {'id': session['user_id'],
                        'con':"../static/img/"+filename}
                mysql.query_db(query, data)
                return redirect('/profile')
            else:
                print("That file extension is not allowed")
                return redirect(request.url)
    return redirect('/profile')

@app.route('/profile')
def pr():
    mysql = connectToMySQL('project1')
    query = "SELECT * FROM users WHERE users.user_id = %(id)s"
    data = {'id': session['user_id']}
    user = mysql.query_db(query, data)

    mysql = connectToMySQL('project1')
    query = "SELECT users.username,posts.content,posts.post_id,count(likes.post_id) as tot FROM posts join users on posts.user_id = users.user_id left join likes on posts.post_id= likes.post_id where users.user_id=%(u)s  group by posts.post_id"
    data={'u':session['user_id']}
    photos = mysql.query_db(query,data)
    
    mysql = connectToMySQL('project1')
    query = "SELECT count(followed_user.user_id1) as tot from followed_user where followed_user.user_id=%(u)s group by followed_user.user_id"
    following = mysql.query_db(query,data) 

    mysql = connectToMySQL('project1')
    query = "SELECT count(followed_user.user_id) as tot1 from followed_user where followed_user.user_id1=%(u)s group by followed_user.user_id"
    followers = mysql.query_db(query,data) 
    return render_template('profile.html',photos=photos,user=user[0],followers=followers,following=following)

@app.route("/follow/<user_id>")
def follow_user(user_id):
    query = "INSERT INTO followed_user (user_id, user_id1) VALUES (%(uid)s, %(uid2)s)"
    mysql = connectToMySQL('project1')
    data = {
        'uid': session['user_id'],
        'uid2': user_id
    }
    mysql.query_db(query, data)
    return redirect("/discover")

@app.route('/discover')
def discover():
    mysql=connectToMySQL('project1')
    query="select users.username,users.user_id from users where users.user_id<>%(u)s"
    data={'u':session['user_id']}
    users=mysql.query_db(query,data)

    return render_template('discover.html',users=users)

@app.route("/detail/<user_id>")
def detail(user_id):
    if session['user_id']==user_id:
        print(user_id)
        return redirect('/profile')

    query='select users.username from users where user_id=%(t)s'
    data = {
        't': user_id
    }
    mysql = connectToMySQL('project1')
    user=mysql.query_db(query,data)

    query = "SELECT content as c,post_id FROM posts where user_id= %(t)s"
    mysql = connectToMySQL('project1')
    post=mysql.query_db(query, data)
    print(post)
    return render_template("profile1.html",user=user[0],post=post)

@app.route("/post/<post_id>/like")
def like_thought(post_id):
    query = "INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s, %(p_id)s)"
    data = {
        'user_id': session['user_id'],
        'p_id': post_id
    }
    mysql = connectToMySQL('project1')
    mysql.query_db(query, data)

    return redirect("/success")

@app.route("/posts/<post_id>/delete")
def delete_t(post_id):

    # if ON DELETE CASCADE is not set up for tweets DELETE likes first
    query = "DELETE FROM likes WHERE post_id = %(t)s"
    data = {
        't':post_id
    }
    mysql = connectToMySQL('project1')
    mysql.query_db(query, data)

    query = "DELETE FROM posts WHERE post_id = %(t)s"
    mysql = connectToMySQL('project1')
    mysql.query_db(query, data)
    return redirect("/success")

@app.route("/post/<post_id>",methods=['POST'])
def comment(post_id):
    query = "INSERT INTO comments ( post_id,user_id,content) VALUES (%(p_id)s, %(user_id)s,%(con)s)"
    data = {
        'user_id': session['user_id'],
        'p_id': post_id,
        'con':request.form['comment']
    }
    mysql = connectToMySQL('project1')
    mysql.query_db(query, data)
    return redirect("/phh/{}".format(post_id))

@app.route('/phh/<post_id>')
def post(post_id):
    query="SELECT post_id,content from posts where post_id=%(u)s"
    data={
        'u':post_id
    }
    mysql = connectToMySQL('project1')
    foto=mysql.query_db(query, data)

    query="select users.username,comments.content from users join comments on users.user_id=comments.user_id where comments.post_id=%(u)s"
    mysql = connectToMySQL('project1')
    comments=mysql.query_db(query, data)
    print(comments)
    return render_template('post.html',foto=foto[0],comments=comments)

if __name__ == "__main__":
    app.run(debug=True)
