from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime, timedelta
app = Flask(__name__)
data = pd.read_csv('dataset/event data.csv.csv')
@app.route('/')
def index():
    return render_template('web.html')

@app.route('/submit', methods=['POST'])
def submit():
    Traffic_details = []
    def predict_traffic_jam(user_input_date, user_input_time, user_input_arrival, user_input_departure, date_match_tolerance=365):
        user_input_date = datetime.strptime(user_input_date, '%d/%m/%Y')
        
        date_range = (user_input_date - timedelta(days=date_match_tolerance), user_input_date + timedelta(days=date_match_tolerance))
        
        date_query = (pd.to_datetime(data['Date'], format='%d/%m/%Y') >= date_range[0]) & (pd.to_datetime(data['Date'], format='%d/%m/%Y') <= date_range[1])
        time_query = (data['Time'] == user_input_time)
        arrival_query = (data['Arrival_Place'] == user_input_arrival)
        departure_query = (data['Departure_Place'] == user_input_departure)
        
        query = date_query & time_query & arrival_query & departure_query
        filtered_data = data[query]

        if not filtered_data.empty:
            predicted_traffic_label = filtered_data['Traffic_Jam_Label'].values[0]
            traffic_speed = filtered_data['Traffic_Speed'].values[0]
            traffic_volume = filtered_data['Traffic_Volume'].values[0]
            weather_condition = filtered_data['Weather_Condition'].values[0]
            weather_attribute = filtered_data['Weather_Attribute'].values[0]
            event_type = filtered_data['Event_Type'].values[0]

            interpretation = f"Predicted traffic is {predicted_traffic_label} with a speed of {traffic_speed} km/h, a volume of {traffic_volume}, in {weather_condition} weather ({weather_attribute}). The event type is {event_type}."
            Traffic_details.append(predicted_traffic_label)
            Traffic_details.append(interpretation)
            return Traffic_details
        else:
            a="No data found for the given input."
            Traffic_details.append(a)
            return Traffic_details

    user_input_date = request.form['uid']
    user_input_time = request.form['uit']
    user_input_arrival = request.form['uia']
    user_input_departure = request.form['uip']

    Traffic_details = predict_traffic_jam(user_input_date, user_input_time, user_input_arrival, user_input_departure)
    result={
        "Predicted Traffic":Traffic_details
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
