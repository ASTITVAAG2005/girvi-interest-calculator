from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        price = float(request.form['price'])
        rate = request.form['rate']
        if rate == 'custom':
            rate = float(request.form['custom_rate'])
        else:
            rate = float(rate)

        arrival_date = datetime.strptime(request.form['arrival_date'], '%Y-%m-%d')
        departure_type = request.form['departure_type']

        if departure_type == 'today':
            departure_date = datetime.today()
        elif departure_type == 'yesterday':
            departure_date = datetime.today() - timedelta(days=1)
        else:
            departure_date = datetime.strptime(request.form['departure_date'], '%Y-%m-%d')

        # Calculate duration
        total_days = (departure_date - arrival_date).days
        months = total_days // 30
        days = total_days % 30

        # Calculate interest
        monthly_interest = (price * rate) / 100
        total_interest = months * monthly_interest + (monthly_interest / 30) * days

        # Total price
        total_price = price + total_interest

        return render_template('index.html', total_interest=total_interest, total_price=total_price)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
