from flask import Flask, Blueprint, render_template, request, jsonify, url_for, redirect, Response
import jsonify


import requests
import json

import psycopg2
from psycopg2.extras import RealDictCursor
import os

from .. import models

general_bp = Blueprint("general_bp", __name__ , template_folder="templates/general", static_url_path="/static")
@general_bp.route("/")
def home():
    products = models.Product("fashion")
    popular_items = products.popular_items(5)
    return render_template("index.html", title="Home", products=popular_items)

@general_bp.route("/apiproduct", methods = ['get'])
def apiproduct():
	return {"id": "octank"}, 200



@general_bp.route("/analytic")
def analytics():
	#return redirect('https://57gq98nfmg.execute-api.us-east-1.amazonaws.com/test/anonymous-embed-sample')
        pass



# @general_bp.route("/search")
# def search():
#     return render_template("index.html", title="Home")

# @general_bp.route("/search")
# def search():
#     query = request.args['keyword']
#     products = requests.get("http://localhost:5000/api/products/groceries/"+query)
#     return render_template("search_results.html",search_results={"products":products.json(), "number":len(products.json())}, title=query)
