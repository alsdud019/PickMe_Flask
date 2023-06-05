import os

from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/imgTest', methods=['POST'])
def img_test_post():
   img_receive = request.files['image']
   img_byte = img_receive.read()
   im = Image.open(BytesIO(img_byte))
   #print(im.size)
   #print(im.format)
   #file_path = 'D:/2023/PickMeBack_flask/venv/'
   im.save('./static/test.jpg',im.format)

   return jsonify(
      {
         "all_ingredient_name": ["에탄올", "메틸파라벤", "구아닌", "벤조페논-3"]
      })

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=False)
