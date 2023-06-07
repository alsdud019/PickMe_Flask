from flask import Flask, request, jsonify, render_template
import subprocess
import os

from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>이미지 업로드</h1>
    <p>사진을 골라주세요</p>
    <form method="POST" action="/UNITE" enctype="multipart/form-data" accept-charset="cp949">
        <input type="file" name="file">
        <input type="submit" value="업로드">
    </form>
    <br>
    '''


@app.route('/UNITE', methods=['POST'])
def detect_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    img_receive = request.files['file']
    img_byte = img_receive.read()
    im = Image.open(BytesIO(img_byte))
    
    
    # 파일 저장
    """
    upload_path = 'C:/Users/Owner/Desktop/capstone/CRAFT/CRAFT-pytorch/test/'
    img_receive.save(os.path.join(upload_path, img_receive.filename))
    """
    
    im.save('./static/test.jpg',im.format)
    
    # CRAFT 실행
    craft_path = r'./detect'
    subprocess.run(['python', os.path.join(craft_path, 'test.py')])

    # Recognition 실행
    recognition_path = r'./recog'
    subprocess.run(['python', os.path.join(recognition_path, 'demo.py')])

    # 결과 파일 읽기
    
    with open(os.path.join(recognition_path + '/result/', 'recog_result.txt'), 'r') as f:
        result = f.readlines()
        
    return jsonify(
       {
          "all_ingredient_name": ["에탄올", "메틸파라벤", "구아닌", "벤조페논-3"]
       })


if __name__ == '__main__':
    app.run(port = 8080)