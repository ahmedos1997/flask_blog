
from flask import Flask , render_template, request, url_for , redirect , Blueprint, g, flash , abort
import functools
import sqlite3

DATABASE = 'blog.db'

bp = Blueprint('blog', __name__, url_prefix='/posts')




def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def login_required(func):
    @functools.wraps(func)
    def wrapped_func(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return func(**kwargs)
    return wrapped_func 

def get_post(post_id, check_author = True):
    post = get_db().execute('SELECT * FROM posts WHERE id = ?', (post_id, )).fetchone()

    if post is None:
        abort(404, f'المقالة ذات المعرف {post_id} غير موجودة')
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post


@bp.route('/')
def index():
    connection = get_db()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

@bp.route('/<int:post_id>')
def show(post_id):
    post = get_post(post_id, check_author=False)
    return render_template('show.html', post=post)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method=='POST':
        connection = get_db()
        title = request.form['title']
        body = request.form['body']
        connection.execute('INSERT INTO posts (title, body, author_id) VALUES (?,?,?)', (title, body , g.user['id']))
        connection.commit()
        connection.close()
        return redirect('/posts')
    return render_template('create.html')



@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'العنوان مطلوب'
        if error is not None:
            flash(error)    
        else:
            db = get_db()
            db.execute('UPDATE posts SET title = ?, body = ? WHERE id= ?', (title, body, post_id))
            db.commit()
            db.close()
            return redirect(url_for('blog.index'))
    return render_template('create.html', post=post)    

@bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    post = get_post(post_id)
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    db.commit()
    db.close()
    return redirect(url_for('blog.index'))
