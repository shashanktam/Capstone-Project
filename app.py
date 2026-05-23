from flask import Flask, render_template, request, session, redirect, url_for, flash
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

    recommend = Resource.query.filter_by(Status='Available').all()
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
    res_id = prod.res_id
    title = prod.title
    author = prod.author
    desc = prod.Description
    token = prod.token
    img = prod.img
    owner = User.query.filter_by(user_id=prod.owner_id).first()
    return render_template('dashboard.html', req="product_page", res_id=res_id, title=title, author=author, desc=desc, token=token, img=img, owner=owner.name)  

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

@app.route('/profile', methods=['GET','POST'])
def profile():
    if request.method == 'GET':
        user = User.query.get(session["u_id"])
        active_l = Resource.query.filter_by(owner_id=session['u_id']).count()
        t_comp = Trades.query.filter(
                    (Trades.provider_id == session['u_id']) | (Trades.receiver_id == session['u_id'])
                        ).count()
        return render_template('dashboard.html', req='profile', user=user, active_listings=active_l, completed_trades=t_comp)
    
@app.route('/approve-request/<int:req_id>', methods=['POST'])
def approve_request(req_id):
    if 'u_id' not in session:
        return redirect(url_for('signin'))

    try:
        # Fetch the request and the attached resource
        trade_request = Requests.query.get(req_id)
        resource = Resource.query.get(trade_request.res_id)

        # Security Check: Ensure the person clicking approve is the actual owner of the book!
        if resource.owner_id != session['u_id']:
            flash('Unauthorized: You do not own this resource.', 'error')
            return redirect(url_for('manage_trades'))

        # Update the status to lock in the match
        trade_request.status = 'Matched'
        db.session.commit()
        
        flash('Trade approved! Waiting for the requester to confirm receipt.', 'success')

    except Exception as e:
        db.session.rollback()
        flash('An error occurred while approving. Please try again.', 'error')
        print(f"Approval Error: {e}")

    return redirect(url_for('manage_trades'))

@app.route('/reject-request/<int:req_id>', methods=['POST'])
def reject_request(req_id):
    if 'u_id' not in session:
        return redirect(url_for('signin'))

    try:
        # Fetch the request and the attached resource
        trade_request = Requests.query.get(req_id)
        resource = Resource.query.get(trade_request.res_id)

        # Security Check: Only the owner can reject the request
        if resource.owner_id != session['u_id']:
            flash('Unauthorized: You do not own this resource.', 'error')
            return redirect(url_for('manage_trades'))

        # 1. Update the request status so the requester knows what happened
        trade_request.status = 'Rejected'
        
        # 2. Free up the book so it appears in the marketplace again
        resource.status = 'Available' 

        # Commit changes
        db.session.commit()
        
        flash('Request rejected. The book is back in the public marketplace.', 'success')

    except Exception as e:
        db.session.rollback()
        flash('An error occurred while rejecting. Please try again.', 'error')
        print(f"Rejection Error: {e}")

    return redirect(url_for('manage_trades'))

@app.route('/manage-trades')
def manage_trades():
    if 'u_id' not in session:
        return redirect(url_for('signin'))

    current_user_id = session['u_id']

    # 1. OUTGOING: Books I want from others
    outgoing_requests = Requests.query.filter(
        Requests.requestor_id == current_user_id,
        Requests.status.in_(['Pending', 'Matched'])
    ).all()

    # 2. INCOMING: People who want MY books
    my_resources = Resource.query.filter_by(owner_id=current_user_id).all()
    my_resource_ids = [r.res_id for r in my_resources]
    
    incoming_requests = Requests.query.filter(
        Requests.res_id.in_(my_resource_ids),
        Requests.status == 'Pending'
    ).all()
    for req in incoming_requests:
        requester = User.query.get(req.requestor_id)
        # We attach a temporary variable 'requester_name' to the object
        req.requester_name = requester.name if requester else "Unknown User"

    # 3. HISTORY: Completed Trades
    trade_history = Trades.query.filter(
        (Trades.receiver_id == current_user_id) | (Trades.provider_id == current_user_id)
    ).order_by(Trades.t_id.desc()).all()

    return render_template('dashboard.html', 
                           req='manage-trades',
                           ongoing=outgoing_requests, 
                           incoming=incoming_requests, 
                           history=trade_history)

@app.route('/request-book/<int:res_id>', methods=['POST'])
def request_book(res_id):
    # Security: Ensure user is logged in
    if 'u_id' not in session:
        return redirect(url_for('signin'))
    
    current_user_id = session['u_id']
    
    # Fetch the relevant database objects
    requester = User.query.get(current_user_id)
    resource = Resource.query.get(res_id)
    provider = User.query.get(resource.owner_id)

    # --- Pre-Transaction Validation Checks ---
    if not resource or resource.Status != 'Available':
        flash('This resource is no longer available.', 'error')
        return redirect(url_for('dashboard'))
        
    if resource.owner_id == current_user_id:
        flash('You cannot request your own book!', 'error')
        return redirect(url_for('dashboard'))

    if requester.credits < resource.token:
        flash('Insufficient tokens to complete this request.', 'error')
        return redirect(url_for('dashboard'))

    # --- The Atomic Transaction Engine ---
    try:

        # Step 2: Update the resource status so no one else can buy it
        resource.Status = 'Pending' 

        # Step 3: Create the official log in the Requests table
        new_request = Requests(
            requestor_id=current_user_id, 
            res_id=resource.res_id, 
            title=resource.title,               
            type=resource.type,      
            author=resource.author,           
            Description=resource.Description, 
            status='Pending'
        )
        db.session.add(new_request)

        # Step 4: Commit all changes to the database AT ONCE
        db.session.commit()
        flash('Request successful! Tokens have been transferred.', 'success')

    except Exception as e:
        # If ANYTHING fails above, undo everything!
        db.session.rollback()
        flash('A network error occurred. Your tokens are safe. Please try again.', 'error')
        print(f"Transaction Error: {e}") 

    return redirect(url_for('manage_trades'))

@app.route('/complete-trade/<int:req_id>', methods=['POST'])
def complete_trade(req_id):
    # Security: Ensure user is logged in
    if 'u_id' not in session:
        return redirect(url_for('signin'))

    current_user_id = session['u_id']

    try:
        # 1. Fetch the necessary database objects
        trade_request = Requests.query.get(req_id)
        resource = Resource.query.get(trade_request.res_id)
        provider = User.query.get(resource.owner_id)
        receiver = User.query.get(trade_request.requestor_id)

        # Pre-Transaction Validation
        if not trade_request or trade_request.status != 'Matched':
            flash('Invalid request or already completed.', 'error')
            return redirect(url_for('manage_trades'))

        # Security Check: Only the person receiving the book can confirm they got it!
        if current_user_id != receiver.user_id:
            flash('Unauthorized: Only the receiver can confirm this trade.', 'error')
            return redirect(url_for('manage_trades'))

        # --- THE ATOMIC TRANSACTION ---
        
        # Step 2: Transfer the tokens
        receiver.credits -= resource.token
        provider.credits += resource.token

        # Step 3: Write to the permanent Ledger (Your new Trades table!)
        new_trade_log = Trades(
            res_id=resource.res_id,
            provider_id=provider.user_id,
            receiver_id=receiver.user_id,
            tokens_exchanged=resource.token
        )
        db.session.add(new_trade_log)

        # Step 4: Update the statuses to remove them from the active marketplace
        trade_request.status = 'Completed'
        resource.Status = 'Traded' 

        # Step 5: Commit EVERYTHING to the database at once
        db.session.commit()
        flash('Trade successful! Tokens have been transferred and the ledger updated.', 'success')

    except Exception as e:
        # If any step above fails (e.g., database crash), wipe the slate clean
        db.session.rollback()
        flash('Transaction failed. Your tokens are safe.', 'error')
        print(f"Ledger Transaction Error: {e}") 

    return redirect(url_for('manage_trades'))
        
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


