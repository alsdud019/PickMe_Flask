from flask import Flask, request, jsonify, render_template
import subprocess
import os

from PIL import Image
from io import BytesIO

app = Flask(__name__)


@app.route('/img2',methods=['POST'])
def img_post_test():
   print(request.files)
   image=request.files['image']
   print(image)
   return jsonify({'result':"image get!"})


@app.route('/imgTest', methods=['POST'])
def detect_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    img_receive = request.files['image']
    img_byte = img_receive.read()
    im = Image.open(BytesIO(img_byte))
    
    
    im.save('./static/test.jpg',im.format)
    
    # CRAFT 실행
    craft_path = r'./detect'
    subprocess.run(['python', os.path.join(craft_path, 'test.py')])

    # Recognition 실행
    recognition_path = r'./recog'
    subprocess.run(['python', os.path.join(recognition_path, 'demo.py')])

    # 결과 파일 읽기
    
    with open(os.path.join(recognition_path + '/result/', 'recog_result.txt'), 'r') as f:
        result = f.read()
        word_list = result.split(',')
        
    print(word_list)
    print(word_list[0])  
    
    return jsonify(
       {
          "all_ingredient_name": [word_list]
       })


if __name__ == '__main__':
    app.run('0.0.0.0',port=8080,debug=False)