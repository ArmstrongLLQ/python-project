from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('index.html', title='Hello World!')

@app.route('/service')
def service():
	return 'service'

@app.route('/about')
def about():
	return 'about'

@app.route('/user/<username>')
def user(username):
	return 'user %s' % username

@app.route('/projects/')
def projects():
	return "this is project page"

@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html', method=request.method)


if __name__ == '__main__':
	app.run(debug=True)
