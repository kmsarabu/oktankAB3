from flask import Blueprint, render_template, jsonify, session, request, redirect, url_for
from flask_images import resized_img_src
from app.models import Kart
import json

cart_bp = Blueprint("cart_bp", __name__, template_folder = "templates")

@cart_bp.route("/addToCart")
def addToCart():
    if not session or (session and 'email' not in session):
        return redirect(url_for('auth_bp.main'))
    else:
        productId = int(request.args.get('productId'))
        qty = request.args.get('qty', 1)
        Kart().add(productId, session['email'], qty)
        cartList = session.get('Kart', [])
        cartList.append(productId)
        session['Kart'] = cartList
        #return redirect(url_for('products_bp.view') + "?id={}".format(productId))
        return redirect(url_for('cart_bp.cart'))

@cart_bp.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('auth_bp.home'))
    email = session['email']
    productId = int(request.args.get('productId'))
    Kart().remove(productId, session['email'])
    if 'Kart' in session:
        session['Kart'].remove(productId)
    return redirect(url_for('cart_bp.cart'))

@cart_bp.route("/view")
def main():
	return render_template("cart/view.html")

@cart_bp.route("/cart")
def cart():
    if 'email' not in session:
        return redirect(url_for('auth_bp.main'))
    email = session['email']
    firstName = "Krishna"
    productsList = []
    if 'Kart' in session:
        productsList = session.get('Kart', [])
    if not productsList:
        return redirect(url_for('general_bp.home'))
    products = Kart().getProducts(productsList)
    for product in products:
       product['qty'] = productsList.count(product['productid'])
    #products = Kart().view(email)
    totalPrice = 0
    noOfItems = 0
    for row in products:
        totalPrice += row.get('price') * row.get('qty')
        noOfItems += 1
    return render_template("cart/cart.html", products = products, totalPrice=round(totalPrice,2), loggedIn=True, firstName=firstName, noOfItems=noOfItems)

