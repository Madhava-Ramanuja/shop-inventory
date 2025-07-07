from flask import Flask, render_template, request, redirect
from db_config import get_connection

app = Flask(__name__)

@app.route('/')
def index():
    selected_category = request.args.get('category')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all distinct categories for dropdown
    cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
    categories = [row['category'] for row in cursor.fetchall()]

    # Fetch products by selected category or all
    if selected_category and selected_category != "All":
        cursor.execute("SELECT * FROM products WHERE category = %s ORDER BY name", (selected_category,))
    else:
        cursor.execute("SELECT * FROM products ORDER BY category, name")
    rows = cursor.fetchall()
    conn.close()

    # Group products by category
    products_by_category = {}
    for row in rows:
        cat = row['category']
        if cat not in products_by_category:
            products_by_category[cat] = []
        products_by_category[cat].append(row)

    return render_template(
        'index.html',
        products_by_category=products_by_category,
        categories=categories,
        selected_category=selected_category or "All"
    )

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        category = request.form['category']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, quantity, category) VALUES (%s, %s, %s, %s)",
                       (name, price, quantity, category))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_product.html')

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        category = request.form['category']
        cursor.execute("""
            UPDATE products
            SET name = %s, price = %s, quantity = %s, category = %s
            WHERE product_id = %s
        """, (name, price, quantity, category, product_id))
        conn.commit()
        conn.close()
        return redirect('/')

    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('update_product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
