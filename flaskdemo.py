from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'

@app.route('/')
def home():
    """Home page route."""
    return render_template("home.html")

@app.route('/about')
def about():
    """About page route."""
    return render_template("about.html")

@app.route('/search', methods=['POST', 'GET'])
def search():
    """Search page route. Return either form page to search, or search results."""
    if request.method == 'POST':
        search_term = request.form['search']
        if not search_term:
            return render_template("results.html", error="Please enter a search term.")
        session['search_term'] = search_term
        return redirect(url_for('results'))
    return render_template("search.html")

@app.route('/results')
def results():
    """Results page route. Render the search results."""
    search_term = session['search_term']
    try:
        page = wikipedia.page(search_term, auto_suggest=False)
        return render_template("results.html", page=page)
    except wikipedia.exceptions.PageError:
        return render_template("results.html", error=f'Page id "{search_term}" does not match any pages.')
    except wikipedia.exceptions.DisambiguationError as e:
        return render_template("results.html", error="The following are some.", options=e.options)

if __name__ == '__main__':
    app.run()
