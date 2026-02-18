from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Product %r>' % self.name


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('index.html')

@app.route('/market')
def market():
    products = Products.query.all()
    return render_template('market.html' , products=products)

@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        amount = request.form['amount']
        description = request.form['description']

        product = Products(name=name, price=price, amount=amount, description=description)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/market')
        except:
            return 'Error while adding product'


    else:
        return render_template('create_product.html')

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)