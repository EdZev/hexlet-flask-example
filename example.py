import os
from flask import (
    Flask,
    redirect,
    request,
    render_template,
    get_flashed_messages,
    flash,
    url_for
    )
from user_repository import UserRepository

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


repo = UserRepository(app.config['DATABASE_URL'])


@app.before_request
def before():
    print(f"Request path: {request.path}")


@app.after_request
def after(response):
    # print(f'response!!! - {response}')
    return response


@app.get('/')
def hello_get():
    return render_template('layout.html')


@app.post('/')
def hello_post():
    return 'Hello POST!\n'


@app.get('/users')
def users_get():
    list_users = repo.get_content()
    messages = get_flashed_messages(with_categories=True)
    query = request.args.get('query', None)
    if query is None:
        return render_template(
            'users/index.html',
            users=list_users,
            search='',
            messages=messages
        )
    filtered_users = [user for user in list_users if query in user['name']]
    no_users = [{'name': "there's no one yet", 'email': ''}]
    users = filtered_users if filtered_users else no_users
    return render_template(
        'users/index.html',
        users=users,
        search=query,
        messages=messages
    )


@app.get('/users/new')
def new_user():
    user_data = {
        'name': '',
        'email': ''
    }
    errors = {}
    return render_template(
        "users/new-user-form.html",
        user=user_data,
        errors=errors
    )


@app.post('/users')
def users_post():
    user_data = request.form.to_dict()
    errors = validate(user_data)
    messages = get_flashed_messages(with_categories=True)
    if errors:
        flash('The form was filled out incorrectly', 'error')
        return render_template(
            "users/new-user-form.html",
            user=user_data,
            errors=errors,
            messages=messages
        ), 422
    user = {
        "name": user_data['name'],
        "email": user_data['email']
    }
    repo.save(user)
    flash(f"User {user['name']} added successfully", 'success')
    return redirect(url_for('users_get'), code=302)


@app.get('/users/<id>/edit')
def user_edit(id):
    user = repo.find(id)
    errors = []
    return render_template(
        'users/edit-user-form.html',
        user=user,
        errors=errors
    )


@app.route('/users/<id>/path', methods=['POST', 'UPDATE'])
def user_path(id):
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            'users/edit-user-form.html',
            user=data,
            errors=errors
        ), 422
    user = {
        'id': id,
        'name': data['name'],
        'email': data['email']
    }
    repo.save(user)
    flash(f"User {user['name']} has been updated", 'success')
    return redirect(url_for('users_post'))


@app.route('/users/<id>/delete', methods=['POST', 'DELETE'])
def users_delete(id):
    repo.destroy(id)
    flash('User has been deleted', 'success')
    return redirect(url_for('users_post'))


@app.errorhandler(404)
def not_found(error):
    print(error)
    return f'Oops!\n {error}', 404


def validate(user_data):
    errors = {}
    if len(user_data['name']) < 3:
        errors['name'] = "The name must be > three characters"
    if not user_data['email']:
        errors['email'] = "Can't be blank"
    return errors
