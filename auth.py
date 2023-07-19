from flask import Blueprint, request, redirect, render_template, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from blog import get_db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        error = None

        if not username:
            error = 'اسم المستخدم مطلوب'
        if not email:
            error ='الريد الالكتروني مطلوب'
        if not password:
            error = 'كلمة المرور مطلوبة'


        if error == None:
            db = get_db()
            

            try:
                db.execute('INSERT INTO users (username, email, password) VALUES (?,?,?)',(username, email, generate_password_hash(password)))
                db.commit()
                db.close()
            except db.IntegrityError:
                error = f'{username} مسجل بالفعل'
            else:
                return redirect(url_for('auth.login'))    
            flash(error)        
    return render_template('auth/register.html')       

@bp.route('/login', methods=['GET','POST'])  
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if g.user :
            return redirect(url_for('blog.index'))
        if not email:
            error = 'البريد الالكتروني غير موجود'
        elif not check_password_hash(user['password'], password):
            error = 'كلمة المرور خاطئة'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('blog.index'))
        
        flash(error)            
    return render_template('auth/login.html')     

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id == None:
        g.user = None  
    else:
        g.user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id, )).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))
