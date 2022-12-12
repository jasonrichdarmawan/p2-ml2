from keras.models import load_model
from tensorflow.io import decode_image
import numpy as np
from utils import converter, db
from flask import Flask, request, jsonify, send_from_directory

preprocessor = load_model(filepath='./model/preprocessor.h5')
model = load_model(filepath='./model/seq_5.h5')
model.trainable = False

app = Flask(__name__)

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "", 400
    
    file = request.files['file']
    if file.filename == '':
        return "", 400

    if file.filename.split(".")[-1] not in ALLOWED_EXTENSIONS:
        return "", 400
    
    image = decode_image(contents=file.read())
    image = preprocessor(image)
    images = np.array([image])

    y_pred = converter.int_to_kinds(np.argmax(model.predict(images), axis=1))

    return jsonify(
        prediction=y_pred[0],
        similar=db.sample(y_pred[0])
    )
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)