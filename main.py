from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# БД - таблицы - записи
# таблица:
# id    title   price   isActive
# 1     some    100     true
# 2     some    100     true
# 3     some    100     true
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # поле не может быть пустым
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)  # устанавливается по умолчанию
    # text = db.Column(db.Text, nullable=False) тип текст не ограничивает количество символов, а стринг ограничивает


    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": 10000
    }
    url = checkout.url(data).get('checkout_url')
    return url

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "ошибка"
    else:
        return render_template('create.html')

with app.app_context():
    db.create_all()

app.run(host='0.0.0.0', port=5001)

if __name__ == '__main__':
    app.run(debug=False)

