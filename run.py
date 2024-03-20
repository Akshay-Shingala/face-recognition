from flask import Flask, request
import face_recognition
from urllib.request import urlopen
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_images():
    file1 = request.files.getlist('file1')
    url_list = request.form.getlist("file1")
    file1.extend(url_list)
    image_list = [f for f in file1 if face_count(f ,is_url=type(f) == str) == 1]
    
    print(image_list)
    # # Url  place of image 
    # url='https://cdn.zeebiz.com/sites/default/files/2023/10/05/263573-untitled-design-2023-10-05t091024122.jpg'
    # url="https://yudiz-python-s3.s3.ap-south-1.amazonaws.com/python-projects/InstaAI/deforum_motion_effect/amitabh_bachchan.jpeg"
    # print(face_count(url, is_url=True))
    
    if len(image_list) < 2:
        return 'Please upload four image files with exactly one face in each image.', 400
    
    base = image_list[0]
    compare_list = image_list[1:]
    results = face_compare(base,compare_list)
    print(results)
    return str(results)

def face_count(image, is_url=False):
    try:
        print(image)
        image = face_recognition.load_image_file(image if not is_url else urlopen(image))
        face_locations = face_recognition.face_locations(image)
        print(face_locations)

        return len(face_locations)
    except Exception as e:
        print("Error:",e)
        return 0

def face_compare(base,images):
    base_img = face_recognition.load_image_file(base if type(base) != str else urlopen(base))
    compare_img_list = [ face_recognition.load_image_file(f if type(f) != str else urlopen(f) ) for f in images]
    
    base_encoding = face_recognition.face_encodings(base_img)[0]
    compare_img_encoding_list = [ face_recognition.face_encodings(img)[0] for img in compare_img_list ]
    print(compare_img_encoding_list)
    results = face_recognition.compare_faces(compare_img_encoding_list, base_encoding)
    return results

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)