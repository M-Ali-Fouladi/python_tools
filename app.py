from flask import Flask, render_template, request, jsonify
from reportlab.pdfgen import canvas
import cv2
from pyzbar.pyzbar import decode
import sqlite3
from barcode import Code128
from barcode.writer import ImageWriter
import os

app = Flask(__name__)
# Function to create the SQLite table
def create_table():
    connection = sqlite3.connect('barcode_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT,
            quantity INTEGER,
            price INTEGER,
            product_name TEXT
        )
    ''')
    connection.commit()
    connection.close()
# ... (Your database setup and functions remain unchanged)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = decode(gray)

        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')

            # Check if barcode is already in the database
       
            cap.release()
            cv2.destroyAllWindows()
            return render_template('form.html', barcode=barcode_data)

        cv2.imshow('Barcode Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    barcode = request.form['barcode']
    quantity = request.form['quantity']
    product_name=request.form['product_name']
    price=request.form['price']
    
    
    # Perform any additional processing, e.g., updating the database with quantity
    
    connection = sqlite3.connect('barcode_database.db')
    cursor = connection.cursor()
    #cursor.execute('UPDATE products SET quantity = ? and product_name = ? WHERE barcode = ?', (quantity,product_name, barcode))
    cursor.execute('INSERT INTO products (barcode, quantity, product_name,price) VALUES (?, ?, ?, ?)', (barcode, quantity, product_name,price))
    connection.commit()
      # Generate PDF
    generate_pdf(barcode, quantity, product_name, price)
    connection.close()

    return f'Successfully processed form for barcode {barcode} with quantity {quantity} and name {product_name}'

#@app.route('/generate_pdf', methods=['POST'])
def generate_pdf(barcode, quantity, product_name, price):


    barcode_filename = f'barcode_{barcode}'
    code = Code128(barcode, writer=ImageWriter())
    code.save(barcode_filename)

    custom_width = 2.0  # in inches 2*72=144
    custom_height = 2.0  # in inches 2*72=144
    # Create a PDF file
    pdf_filename = f'invoice_{barcode}.pdf'
    pdf = canvas.Canvas(pdf_filename,pagesize=(custom_width*72, custom_height*72)) # 1 inch = 72 points

        # Set font size
    font_size = 8  # Adjust the font size as needed
    pdf.setFont("Helvetica", font_size)
    
    pdf.rect(2,2 ,140 , 140)   # from 2,2 to 140,140 drawing a rectangle
    pdf.rect(4,4 ,136 , 136)  # from 4,4 to 136,136 drawing a rectangle
    
    # Write information to the PDF
    #pdf.drawString(100, 800, f'Barcode: {barcode}')
    pdf.drawString(5,125 , f'Product Name: {product_name}')  # x=144,y=144 overally
    pdf.drawString(5,100, f'Quantity: {quantity}')
    pdf.drawString(5,70, f'Price: {price}')

 
    pdf.drawInlineImage(barcode_filename+'.png', 45, 10,width=50,height=35)
    # Add more information as needed

    # Save the PDF
    pdf.save()

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
