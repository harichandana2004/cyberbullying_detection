from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Initialize Flask app
app = Flask(__name__)

# Load the trained model and tokenizer
model = tf.keras.models.load_model('cyberbullying_detection_model.h5')
with open('tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)

# Define max_sequence_length (same as during training)
max_sequence_length = 500

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input text from the user
    input_text = request.form['comment']

    # Preprocess the text
    input_sequence = tokenizer.texts_to_sequences([input_text])
    input_padded = pad_sequences(input_sequence, maxlen=max_sequence_length)

    # Make a prediction
    prediction = model.predict(input_padded)[0][0]

    # Determine the label
    result = "Cyberbullying" if prediction > 0.5 else "Non-Cyberbullying"

    return render_template('index.html', text=input_text, result=result)

if __name__ == '__main__':
    app.run(debug=True)
