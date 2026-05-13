from flask import Flask, render_template, request, session, redirect, url_for
from models import *
import os

app.config['SECRET_KEY']="libris_for_students_by_students_2026"

# UPLOAD_FOLDER = 'static/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

STATIC_FOLDER = os.path.join(app.root_path, 'static')

PRODUCT_UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads', 'products')
REQUEST_UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads', 'requests')


app.config['PRODUCT_UPLOAD_FOLDER'] = PRODUCT_UPLOAD_FOLDER
app.config['REQUEST_UPLOAD_FOLDER'] = REQUEST_UPLOAD_FOLDER

os.makedirs(PRODUCT_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REQUEST_UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET','POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    elif request.method == 'POST':
        data = request.form
        name = data.get('name')
        email = data.get('email')
        password_in = data.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            return render_template('signin.html',error_message="Email not registered !")
        else:
            curr_password = user.password
            if curr_password == password_in:
                session["n"] = name
                session["u_id"] = user.user_id
                session["mail"] = email
                session["pwd"] = password_in
                return redirect(url_for('home'))
            else:
                return render_template('signin.html', error_message="Incorrect Password !")


            
@app.route('/home', methods=['GET'])
def home():
    name = session.get("n",None)
    mail = session.get("mail",None)
    pwd = session.get("pwd",None)

    recommend = Resource.query.all()
    if name:
        return render_template('dashboard.html',name=name,req="Home",products=recommend)
    else:
        return "<b> Unauthorised access !! </b> <a href='/'>Login here</a>"

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        data = request.form
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        dob = data.get('dob')
        gender = data.get('gender')
        branch = data.get('branch')
        semester = data.get('semester')

        user = User.query.filter_by(email=email).first()
        if not user:
            user1 = User(email=email, name=name, dob=dob,password=password, gender=gender, branch=branch, semester=semester)
            db.session.add(user1)
            db.session.flush()
            id = User.user_id
            user1.credits = 500 
            db.session.commit()
        
            return render_template('signin.html')
        
        else:
            return "User already exist"
        
@app.route('/resources',methods=['GET','POST'])
def resources():
    if request.method == 'GET':
        current_resource = Resource.query.filter_by(owner_id=session.get('u_id')).all()
        return render_template('dashboard.html', req="Resources", u_resources=current_resource)

@app.route('/resources/add',methods=['GET','POST'])
def add():
    if request.method == 'GET':
        return render_template('dashboard.html', req="add")
    
    elif request.method == 'POST':
        data = request.form
        res_name = data.get("res_name")
        auth_name = data.get("auth_name")
        res_type = data.get("res_type")
        token = data.get("token")
        desc = data.get("desc")
        img = request.files.get("img")

        ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png')

        if img and img.filename != '':

            if not img.filename.lower().endswith(ALLOWED_EXTENSIONS):
                return render_template('dashboard.html', req="add", msg="Please upload a valid image (.jpg, .png, .jpeg) !")
            
            filename = img.filename.lower()
            img_path = os.path.join(app.config['PRODUCT_UPLOAD_FOLDER'], filename)
            img.save(img_path)

            new_res = Resource(
                title=data.get("res_name"),
                author=data.get("auth_name"),
                type=data.get("res_type"),
                token=int(data.get("token")), 
                Description=data.get("desc"),
                img=img.filename, 
                owner_id=session.get("u_id")
            )
            db.session.add(new_res)
            db.session.commit()

            return redirect(url_for('resources'))

@app.route('/products/<res_id>',methods=['GET','POST'])
def product(res_id):
    prod = Resource.query.filter_by(res_id=res_id).first()
    title = prod.title
    author = prod.author
    desc = prod.Description
    token = prod.token
    img = prod.img
    return render_template('dashboard.html', req="product_page", title=title, author=author, desc=desc, token=token, img=img)  

@app.route('/resources/<res_id>/cancel', methods=['POST'])
def res_cancel(res_id):
    res = Resource.query.filter_by(res_id=res_id).first()
    
    if res:
        # --- NEW: FILE SYSTEM DELETION ---
        filename = res.img
        
        if filename and filename != 'Book.jpg':
            
            file_path = os.path.join(app.config['PRODUCT_UPLOAD_FOLDER'], filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)

    db.session.delete(res)
    db.session.commit()
    return redirect(url_for('resources'))  
            

@app.route('/requests',methods=['GET','POST'])
def requests():
    if request.method == 'GET':
        current_request = Requests.query.filter_by(requestor_id=session.get('u_id')).all()
        return render_template('dashboard.html', req="Requests", u_requests=current_request)
    
    elif request.method == 'POST':
        title = request.form.get('req_name')
        author = request.form.get('auth_name')
        type = request.form.get('req_type')
        desc = request.form.get('desc')
        img = request.files.get('img')

        ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png')

        if img and img.filename != '':

            if not img.filename.lower().endswith(ALLOWED_EXTENSIONS):
                return redirect(url_for('req_add', msg="Please upload a valid image (.jpg, .png, .jpeg) !"))
            
            filename = img.filename.lower()
            img_path = os.path.join(app.config['REQUEST_UPLOAD_FOLDER'], filename)
            img.save(img_path)
        
            new_req = Requests(
                    title=title,
                    author=author,
                    type=type,
                    Description=desc,
                    img=filename,
                    requestor_id=session.get('u_id'),
                    status="Pending" 
                )
            db.session.add(new_req)
            db.session.commit()

        else:
            new_req = Requests(
                    title=title,
                    author=author,
                    type=type,
                    Description=desc,
                    requestor_id=session.get('u_id'),
                    status="Pending" 
                )
            db.session.add(new_req)
            db.session.commit()
        return redirect(url_for('requests'))
    

@app.route('/requests/add',methods=['GET'])
def req_add():
    return render_template('dashboard.html', req="add-request")

@app.route('/requests/<id>/cancel', methods=['POST'])
def req_cancel(id):
    req = Requests.query.filter_by(req_id=id).first()
    
    if req:
        # --- NEW: FILE SYSTEM DELETION ---
        filename = req.img
        
        if filename and filename != 'Book.jpg':
            
            file_path = os.path.join(app.config['REQUEST_UPLOAD_FOLDER'], filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)

    db.session.delete(req)
    db.session.commit()
    return redirect(url_for('requests'))

        
@app.route('/logout', methods=['GET'])
def logout():
    session.pop("name",None)
    session.pop("u_id",None)
    session.pop("mail",None)
    session.pop("pwd",None)
    return redirect(url_for('signin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)        


