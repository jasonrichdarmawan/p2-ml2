from keras.models import load_model
from tensorflow.io import decode_image
from tensorflow.keras.utils import save_img
import numpy as np
from utils import converter, db_df, db_captcha, captcha
from flask import Flask, request, jsonify
import uuid
from random import shuffle

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

    save_img(path=f'static/{y_pred[0]}/{file.filename}', x=image)

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
    candidates = db_df.sample_random(n=1).reset_index(drop=True)
    candidates_uuid = [str(uuid.uuid4()) for i in range(len(candidates))]
    
    target = candidates.sample(n=1)
    target_uuid = candidates_uuid[target.index.tolist()[0]]
    print(target_uuid)
    
    db_captcha.set(request.remote_addr, target_uuid)
    
    encoded_images = []
    for candidate_uuid, image_path in zip(candidates_uuid, candidates['path'].values):
        encoded_images.append(
            [candidate_uuid, captcha.load_image(image_path)]
        )
        
    shuffle(encoded_images)
    
    return jsonify(
        target=target['kind'].values[0],
        options=encoded_images
    )

@app.route('/captcha', methods=['POST'])
def post_CAPTCHA():
    args = request.json
    
    target = args.get("target_uuid")
    if target == None:
        return "", 400
    
    return jsonify(
        result=db_captcha.validate(request.remote_addr, target)
    )
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)