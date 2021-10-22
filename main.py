from flask import Flask, render_template, request, redirect
from models import db, ProductModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_table():
  db.create_all()


@app.route('/data/create', methods=['GET', 'POST'])
def create():
  if request.method == 'GET':
    return render_template('create.html')

  if request.method == 'POST':
    stock = request.form["stock"]
    nombre_producto = request.form['nombre_producto']
    precio = request.form["precio"]
    producto = ProductModel(stock=stock, nombre_producto=nombre_producto, precio=precio)
    db.session.add(producto)
    db.session.commit()
    return redirect('/data')


@app.route('/data')
def getProducts():
  productos = ProductModel.query.all()
  return render_template('products.html', productos=productos)


@app.route('/data/<int:id>')
def getProduct(id):
  product = ProductModel.query.filter_by(id=id).first()
  if product:
    return render_template('product.html', product=product)


@app.route('/data/<int:id>', methods=['GET', 'POST'])
def sellProduct(id):
  product = ProductModel.query.filter_by(id=id).first()
  if request.method == 'POST':
    comision = 0
    if product and product.stock > 0:
      nombre_producto = product.nombre_producto
      stock = product.stock - 1
      precio = product.precio
      comision = precio * 0.05
      producto = ProductModel(stock=stock, nombre_producto=nombre_producto, precio=precio)

      db.session.delete(product)
      db.session.commit()
      db.session.add(producto)
      db.session.commit()
  return render_template('product.html', product=product, comision=comision)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
  product = ProductModel.query.filter_by(id=id).first()
  if request.method == 'POST':
    db.session.delete(product)
    db.session.commit()
    redirect('/data')

  return render_template('delete.html')

app.run(debug=True)
