import flask
import pickle
import pandas as pd

# Use pickle to load in the pre-trained model
with open('Final_Model.sav', 'wb') as f:
    model = pickle.load(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')


# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return (flask.render_template('main.html'))

    if flask.request.method == 'POST':
        # Extract the input
        recency = flask.request.form['Recency(months)']
        frequency = flask.request.form['Frequency(times)']
        monetary = flask.request.form['Monetary(c.c.blood)']
        time = flask.request.form['Time(months)']




        # Make DataFrame for model
        input_variables = pd.DataFrame([[recency, frequency, monetary, time]],
                                       columns=['Recency(months)', 'Frequency(times)', 'Monetary(c.c.blood)', 'Time(months)'],
                                       dtype=float,
                                       index=['input'])

        # Get the model's prediction
        prediction = model.predict(input_variables)[0]

        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('main.html',
                                     original_input={'Recency': recency,
                                                     'Frequency': frequency,
                                                     'Monetary': monetary
                                                     'Time': time},
                                     result=prediction,
                                     )


if __name__ == '__main__':
    app.run()