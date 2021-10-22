from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class ProductModel(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key=True)
  stock = db.Column(db.Integer())
  nombre_producto = db.Column(db.String())
  precio = db.Column(db.Float())

  def __init__(self, stock, nombre_producto, precio):
    self.stock = stock
    self.nombre_producto = nombre_producto
    self.precio = precio


  






  
  



