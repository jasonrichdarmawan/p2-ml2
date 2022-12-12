from keras.models import load_model
from tensorflow.io import decode_image
import numpy as np
from utils import converter, db_df, db_captcha, captcha
from flask import Flask, request, jsonify, send_file

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
        similar=db_df.sample(y_pred[0])
    )

@app.route('/captcha', methods=['GET'])
def get_CAPTCHA():
    """
    Bad CAPTCHA Implementation.
    TODO: use websocket so we can store client target without accessing the entire database,
          / redis so we can store the client target in a dedicated database
    """
    candidate = db_df.sample_random(n=1)
    options = candidate['path'].str.split("/").str[-1]
    
    target = candidate.sample(n=1)
    
    db_captcha.set(request.remote_addr, target['path'].values[0].split("/")[-1])
    print(target['path'].values[0].split("/")[-1])
    
    encoded_images = []
    for image_path in candidate['path'].values:
        encoded_images.append(
            [image_path.split("/")[-1], captcha.load_image(image_path)]
        )
    
    return jsonify(
        target=target['kind'].values[0],
        options=encoded_images
    )

@app.route('/captcha', methods=['POST'])
def post_CAPTCHA():
    args = request.json
    
    target = args.get("target")
    if target == None:
        return "", 400
    
    return jsonify(
        result=db_captcha.validate(request.remote_addr, target)
    )
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)