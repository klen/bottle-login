""" Tests for `bottle-login` module. """

def test_bottle_login():
    import webtest
    from bottle import Bottle, request, redirect
    from bottle_login import LoginPlugin

    USERS = 'James', 'Mike', 'Bob'

    app = Bottle()
    app.config['SECRET_KEY'] = 'secret'

    login = app.install(LoginPlugin())

    @login.load_user
    def load_user_by_id(user_id):
        return USERS[user_id]

    @app.route('/')
    def index():
        user = login.get_user()
        return user

    @app.route('/signout')
    def signout():
        login.logout_user()
        return redirect('/')

    @app.route('/signin')
    def signin():
        user_id = int(request.GET.get('user_id'))
        login.login_user(user_id)
        return redirect('/')

    client = webtest.TestApp(app)
    response = client.get('/')
    assert response.body.decode('UTF-8') == ''

    response = client.get('/signin?user_id=1')
    response = client.get('/')
    assert response.body.decode('UTF-8') == 'Mike'

    response = client.get('/signout')
    response = client.get('/')
    assert response.body.decode('UTF-8') == ''

    response = client.get('/signin?user_id=2')
    response = client.get('/')
    assert response.body.decode('UTF-8') == 'Bob'
