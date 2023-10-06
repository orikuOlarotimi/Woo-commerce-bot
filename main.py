from flask import Flask, jsonify, request
import requests
import json
from pprint import pprint

app = Flask(__name__)


@app.route('/product/<search>', methods=['GET'])
def get_products(search):
    # search_query = search
    # params = {
    #     "search": search_query
    # }
    url = "https://wordpress-409974-3635319.cloudwaysapps.com/wp-json/wc/v3/products?search=" + search
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic Y2tfYTQ1ZTVlZGVhYTUwOTdjYzNhNDVmMzI2NzdjMTc5YWU2NWUxNjJkNzpjc19mOGJkZDY0MzZmYzZhYzY2OWZmYzgzNTJkOTZhMWYzOTI1MDQxZmJj'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    datas = response.json()
    if len(datas) == 0:
        return jsonify({"status": "notfound"})
    products = []
    count = 0
    for data in datas:
        product_data = {
            "name": data['name'],
            "image_url": data['images'][0]['src'],
            "price": data['price'],
            "id": data['id'],
            "status": "success"
        }
        products.append(product_data)

    message = ""
    for product in products:
        count += 1
        product['index'] = count
        message += f"{count} Name: {product['name']} \n image: {product['image_url']} \n {product['price']}\n\n"

    return {"message": message, 'products': products, "status": "success"}


@app.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()

    url = "https://wordpress-409974-3635319.cloudwaysapps.com/wp-json/wc/v3/orders"

    payload = json.dumps({
        "payment_method": "bacs",
        "payment_method_title": "Direct Bank Transfer",
        "set_paid": True,
        'customer_id': data['customer_id'],
        "billing": {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "address_1": data['address'],
            "address_2": "",
            "city": data['city'],
            "state": data['state'],
            "postcode": data['postcode'],
            "country": data['country'],
            "email": data['email'],
            "phone": data['phone']
        },
        "shipping": {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "address_1": data['address'],
            "address_2": "",
            "city": data['city'],
            "state": data['state'],
            "postcode": data['postcode'],
            "country": data['country']
        },
        "line_items": [
            {
                "product_id": data['id'],
                "quantity": data['quantity']
            }
        ],
        "shipping_lines": [
            {
                "method_id": "flat_rate",
                "method_title": "Flat Rate",
                "total": "10.00"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic Y2tfYTQ1ZTVlZGVhYTUwOTdjYzNhNDVmMzI2NzdjMTc5YWU2NWUxNjJkNzpjc19mOGJkZDY0MzZmYzZhYzY2OWZmYzgzNTJkOTZhMWYzOTI1MDQxZmJj'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    payment_url = response['payment_url']
    pprint(response)

    info = {"payment_url": payment_url}
    return info


@app.route('/list', methods=['POST'])
def list_prod():
    search_detail = request.get_json()
    datal = {
        'search_option': search_detail['search_option'],
        "status": "success"
    }
    return jsonify(datal)


@app.route('/prod_des', methods=['POST'])
def prod_des():
    search_product = request.get_json()
    if len(search_product) == 0:
        return jsonify({"status": "notfound"})

    products_str = search_product['products']
    products_str = products_str.replace("'", '"')
    products = json.loads(products_str)

    produce = []
    for product in products:
        product_data = {
            "name": product['name'],
            "image_url": product['image_url'],
            "index": product['index'],
            "price": product['price'],
            "id": product['id'],
            "status": "success"
        }
        produce.append(product_data)
    search_option = int(search_product['search_option'])
    item = None
    message = ""

    for prod in products:
        if prod['index'] == search_option:
            prod['status'] = "success"
            return prod

    return {"status": "error"}


@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    url = "https://wordpress-409974-3635319.cloudwaysapps.com/wp-json/wc/v3/customers"

    payload = json.dumps({
        "email": data['email'],
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "username": data['username'],
        "password": data['password'],
        "billing": {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "company": "",
            "address_1": data['address'],
            "address_2": "",
            "city": data['city'],
            "state": data['state'],
            "postcode": data['postcode'],
            "country": data['country'],
            "email": data['email'],
            "phone": data['phone']
        },
        "shipping": {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "company": "",
            "address_1": data['address'],
            "address_2": "",
            "city": data['city'],
            "state": data['state'],
            "postcode": data['postcode'],
            "country": data['country']
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic Y2tfYTQ1ZTVlZGVhYTUwOTdjYzNhNDVmMzI2NzdjMTc5YWU2NWUxNjJkNzpjc19mOGJkZDY0MzZmYzZhYzY2OWZmYzgzNTJkOTZhMWYzOTI1MDQxZmJj'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    username = response['username']
    customer_id = response['id']
    info = {"username": username, "id": customer_id, "status": "success"}
    return info


@app.route('/customers/<id>/<email>', methods=['GET'])
def get_customer(id, email):
    url = "https://wordpress-409974-3635319.cloudwaysapps.com/wp-json/wc/v3/customers?id=" + id
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic Y2tfYTQ1ZTVlZGVhYTUwOTdjYzNhNDVmMzI2NzdjMTc5YWU2NWUxNjJkNzpjc19mOGJkZDY0MzZmYzZhYzY2OWZmYzgzNTJkOTZhMWYzOTI1MDQxZmJj'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    datas = response.json()
    found_customer = False
    for customer in datas:
        if int(customer['id']) == int(id) and str(customer['email']) == str(email):
            username = customer['username']
            found_customer = True
            break
    if found_customer:
        return {"status": "success", "username": username}
    else:
        return {"status": "error", "message": "Customer with ID  not found"}


@app.route('/list_order', methods=['POST'])
def list_order():
    customer_id = request.get_json()
    cust_id = {
        "order_id": customer_id['order_id']
    }
    return jsonify(cust_id)


@app.route('/orders/<customer>/<email>', methods=['GET'])
def list_customer_order(customer, email):
    url = "https://wordpress-409974-3635319.cloudwaysapps.com/wp-json/wc/v3/orders?customer=" + customer
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic Y2tfYTQ1ZTVlZGVhYTUwOTdjYzNhNDVmMzI2NzdjMTc5YWU2NWUxNjJkNzpjc19mOGJkZDY0MzZmYzZhYzY2OWZmYzgzNTJkOTZhMWYzOTI1MDQxZmJj'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    datas = response.json()
    for data in datas:
        if len(datas) == 0:
            return {"status": "error"}

        if int(data['customer_id']) == int(customer) and str(data['billing']['email']) == str(email):
            pprint(data)
            return {"status": "success", "data": data}
        else:
            pprint(data)
            return {"status": "invalid details"}


products = []


@app.route('/cart', methods=['POST'])
def cart():
    cart_details = request.get_json()
    pprint(cart_details)
    if len(cart_details) == 0:
        return jsonify({"status": "notfound"})

    count = 0

    items = {
        "name": cart_details['cart_product_name'],
        "image_url": cart_details['cart_image'],
        "price": cart_details['cart_price'],
        "id": cart_details['cart_id'],
        "status": "success"
    }

    products.append(items)
    message = ""
    for product in products:
        count += 1
        product['index'] = count
        message += f"{count} Name: {product['name']} \n image: {product['image_url']} \n {product['price']}\n\n"

    return {"message": message, 'products': products, "status": "success"}


@app.route('/list_cart', methods=['POST'])
def cart_no():
    cart_option = request.get_json()
    datal = {
        "cart_option": cart_option['cart_option'],
        "status": "success"
    }
    pprint(datal)
    return jsonify(datal)


@app.route('/cart_des', methods=['POST'])
def cart_des():
    search_product = request.get_json()
    if len(search_product) == 0:
        return jsonify({"status": "notfound"})
    products_str = search_product['cart_item']
    products_str = products_str.replace("'", '"')
    products = json.loads(products_str)

    produce = []
    for product in products:
        product_data = {
            "name": product['name'],
            "image_url": product['image_url'],
            "index": product['index'],
            "price": product['price'],
            "id": product['id'],
            "status": "success"
        }
        produce.append(product_data)
    search_option = int(search_product['cart_option'])
    item = None
    message = ""

    for prod in products:
        if prod['index'] == search_option:
            prod['status'] = "success"
            return prod

    return {"status": "error"}


if __name__ == '__main__':
    app.run()
