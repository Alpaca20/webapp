from flask import Flask, render_template
from dict import Articles

app = Flask(__name__)

Articles = Articles()

@app.route('/')
def index():
	return 'hi dictionary'

@app.route('/articles')
def articles():
	return render_template('articles.html', articles = Articles)

@app.route('/article/<int:id>')
def article(id):
	return render_template('article.html', id = id, articles = Articles)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8888)
