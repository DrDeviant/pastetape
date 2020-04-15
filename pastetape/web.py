from flask import Flask, flash, redirect, render_template, request, session, send_from_directory

app = Flask(__name__, static_url_path="/static")

@app.route("/")
def index():
    pass

@app.errorhandler(404)
def page_not_found(e):
    flash("Not found! Please check the URL and try again.")
    return redirect("/")