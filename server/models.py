from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # serialization rules
    serialize_rules = ('-reviews.customer',)

    #relationship to review
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')

    #association proxy to items
    items = association_proxy('reviews', 'item', creator=lambda item_obj:Review(item=item_obj))


    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    #serialization rules
    serialize_rules = ('-reviews.item',)

    #relationship to review
    reviews =db.relationship('Review', back_populates='item', cascade='all,  delete-orphan')

    #association proxy to customers
    customers = association_proxy('reviews', 'customer', creator=lambda customer_obj:Review(customer=customer_obj))

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
    
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    #table columns including foreign id for association object
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    #serialization rules
    serialize_rules = ('-customer.reviews', '-item.reviews')

    #relationship to customers
    customer = db.relationship('Customer', back_populates='reviews')

    #relationship to items
    item =db.relationship('Item', back_populates='reviews')
