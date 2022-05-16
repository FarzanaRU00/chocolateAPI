from flask import Flask, request, jsonify, render_template, url_for, flash, redirect
# Flask and render_template() function is needed for db connection
# flash function stores flashed messages (users cannot submit an invalid form) in the client’s browser session, which requires setting a secret key to secure sessions that remember information from one request to another.
from flask_cors import CORS
from controllers import chocolates
from werkzeug import exceptions
import sqlite3
# import sqlite3 module to connect it to your db

# from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
# created a flask application called app
CORS(app)
# mail = Mail(app)

# app.config['MAIL_SERVER'] = ''
# app.config['MAIL_PORT'] =
# app.config['MAIL_USERNAME'] =
# app.config['MAIL_PASSWORD'] = ''
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

def get_db_connection():
    conn = sqlite3.connect('chocolates.db')
    conn.row_factory = sqlite3.Row
    return conn
# function opens a connection to our db

@app.route('/chocolates/:id')
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM chocolates WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():
    conn = get_db_connection()
    chocolates = conn.execute('SELECT * FROM chocolates').fetchall()
    conn.close()
    return render_template('index.html', chocolates=chocolates)
    

@app.route('/welcome')
def home():
    return render_template('welcome.html')
    return jsonify({'message': 'Welcome to the chocolate API!'}), 200
# jsonify requires the messages and sends back json data rather than a html

# ...


# creates a route for users to add a new post to the db which would appear on the index page
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']

        if not name:
            flash('Name is required!')
        elif not country:
            flash('Country is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO chocolates (name, country) VALUES (?, ?)',
                         (name, country))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

# we use the ? placeholder to safely insert data into the table

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM chocolates WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['name']))
    return redirect(url_for('index'))

@app.route('/chocolates', methods=['GET', 'POST'])
def chocolates_handler():
    fns = {
        'GET': chocolates.index,
        'POST': chocolates.create
    }
    resp, code = fns[request.method](request)
    return jsonify(resp), code

@app.route('/chocolates/<int:chocolate_id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def chocolate_id_handler(chocolate_id):
    fns = {
        'GET': chocolates.show,
        'PATCH': chocolates.update,
        'PUT': chocolates.update,
        'DELETE': chocolates.destroy
    }
    resp, code = fns[request.method](request, chocolate_id)
    return jsonify(resp), code

@app.route('/chocolates/country/<country>', methods=['GET'])
def choc_country_handler(country):
    fns = {
        'GET': chocolates.show_by_country
    }
    response, code = fns[request.method](request, country)
    return jsonify(response), code

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Oops! {err}'}, 404

@app.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return {'message': f'Oops! {err}'}, 400

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'message': f"It's not you, it's us"}, 500

if __name__ == "__main__":
    app.run(debug=True)

