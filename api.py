from flask import Flask, request, jsonify
import subprocess
import os,csv,re

from PIL import Image
from io import BytesIO
from difflib import get_close_matches

app = Flask(__name__)

candidates=[] #단어 교정시 후보군
n=1 #최상위 표출 개수
cutoff = 0.5 #임계값

@app.route('/imgTest', methods=['POST'])
def detect_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    img_receive = request.files['image']
    img_byte = img_receive.read()
    im = Image.open(BytesIO(img_byte))

    im.save('./static/test.jpg',im.format)
    
    # CRAFT 실행
    craft_path = r'./detection'
    subprocess.run(['python', os.path.join(craft_path, 'test.py')])

    # Recognition 실행
    recognition_path = r'./recog'
    subprocess.run(['python', os.path.join(recognition_path, 'demo.py')])

    # 결과 파일 읽기
    
    with open(os.path.join(recognition_path + '/result/', 'recog_result.txt'), 'r', encoding= 'CP949') as f:
        result = f.read()
        word_list = list(result.split(','))

    word = re.sub("(,|/| |\(|\)|-|&)", "", word_list[0])
    if word.encode().isalnum() == True:  # 영어인경우
        english = "./csv/english.csv"
        candidates = loadCanditate(english)
        print("Correcting english words...")
        renew_total = correctWord(word_list, candidates)
        toggle = "english"
    else:  # 한글인경우
        korean = "./csv/korean.csv"
        candidates = loadCanditate(korean)
        print("Correcting korean words...")
        renew_total = correctWord(word_list, candidates)
        toggle = "korean"
    # print(word_list)
    # print(word_list[0])
    
    return jsonify(
       {
          "all_ingredient_name":renew_total,
           "language": toggle
       })

def loadCanditate(file_path):
   f=open(file_path,'r',encoding='utf-8-sig')
   rea = csv.reader(f)
   for row in rea:
      candidates.append(*row)
   return candidates


def correctWord(result,candidates):
   total=[]
   for word in result:
      if len(word)<=2 and word not in total: # 글자수가 2 이하인경우 그대로 저장
         total.append(word)
         continue
      else:
         close_matches = get_close_matches(word, candidates, n, cutoff)
         if len(close_matches) == 0: # 교정된 단어가 없는경우
            continue
         elif word not in total: #중복 결과 제거
            total.append(*close_matches)
   return total

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)