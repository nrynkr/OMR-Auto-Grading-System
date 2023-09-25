# # Import necessary libraries and modules
# from imutils.perspective import four_point_transform
# from imutils import contours
# import numpy as np
# import argparse
# import imutils
# import cv2
# import random
# from flask import Flask, render_template, request, redirect, url_for, flash

# def show_images(images, titles, kill_later=True):
#     for index, image in enumerate(images):
#         cv2.imshow(titles[index], image)
#     cv2.waitKey(0)
#     if kill_later:
#         cv2.destroyAllWindows()

# # Initialize Flask application
# app = Flask(__name__)

# # Define a secret key for session management (needed for flash messages)
# app.secret_key = 'your_secret_key'

# ANSWER_KEY = {
#     0: 1,
#     1: 4,
#     2: 0,
#     3: 3,
#     4: 1
# }

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # Check if a file was uploaded
#         if 'file' not in request.files:
#             flash('No file part', 'error')
#             return redirect(request.url)
        
#         file = request.files['file']

#         # Check if the file has a valid extension (e.g., .png, .jpg)
#         if file.filename == '':
#             flash('No selected file', 'error')
#             return redirect(request.url)
        
#         if file:
#             # Save the uploaded file temporarily
#             filename = 'uploaded_image.png'
#             file.save(filename)

#             # Process the uploaded image
#             image = cv2.imread(filename)
#             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#             # Image processing code
#             blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#             edged = cv2.Canny(blurred, 75, 200)

#             # Find contours in the edge map
#             cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             cnts = imutils.grab_contours(cnts)
#             docCnt = None

#             if len(cnts) > 0:
#                 cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
#                 for c in cnts:
#                     peri = cv2.arcLength(c, True)
#                     approx = cv2.approxPolyDP(c, 0.02 * peri, True)
#                     if len(approx) == 4:
#                         docCnt = approx
#                         break
            
#             if docCnt is not None:
#                 # Apply a four-point perspective transform
#                 paper = four_point_transform(image, docCnt.reshape(4, 2))
#                 warped = four_point_transform(gray, docCnt.reshape(4, 2))

#                 # Apply Otsu's thresholding method
#                 thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

#                 # Find contours in the thresholded image
#                 cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#                 cnts = imutils.grab_contours(cnts)
#                 questionCnts = []

#                 # Loop over the contours
#                 for c in cnts:
#                     (x, y, w, h) = cv2.boundingRect(c)
#                     ar = w / float(h)

#                     if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
#                         questionCnts.append(c)

#                 # Sort the question contours top-to-bottom
#                 questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
#                 correct = 0

#                 # Loop over the questions
#                 for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
#                     cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
#                     bubbled = None

#                     # Loop over the sorted contours
#                     for (j, c) in enumerate(cnts):
#                         mask = np.zeros(thresh.shape, dtype="uint8")
#                         cv2.drawContours(mask, [c], -1, 255, -1)

#                         mask = cv2.bitwise_and(thresh, thresh, mask=mask)
#                         total = cv2.countNonZero(mask)

#                         if bubbled is None or total > bubbled[0]:
#                             bubbled = (total, j)

#                     color = (0, 0, 255)
#                     k = ANSWER_KEY[q]

#                     if k == bubbled[1]:
#                         color = (0, 255, 0)
#                         correct += 1

#                     cv2.drawContours(paper, [cnts[k]], -1, color, 3)

#                 # Calculate the score
#                 total_questions = len(ANSWER_KEY)
#                 score = (correct / total_questions) * 100
#                 print("[INFO] score: {:.2f}%".format(score))
#                 cv2.putText(paper, "{:.2f}%".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
#                 cv2.imshow("Original", image)
#                 cv2.imshow("Exam", paper)
#                 cv2.waitKey(0)
#                 cv2.putText(image, "Score: {:.2f}%".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

#             # Save the processed image to a file
#             result_image_filename = 'static/result_image.png'
#             cv2.imwrite(result_image_filename, image)

#             return render_template('index.html', score=score, result_image=result_image_filename)
    
#     return render_template('index.html')


# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for, flash, session
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import random

# Initialize Flask application
app = Flask(__name__)

# Define a secret key for session management (needed for flash messages)
app.secret_key = 'your_secret_key'

ANSWER_KEY = {
    0: 1,
    1: 4,
    2: 0,
    3: 3,
    4: 1
}

# Sample user data structure for in-memory storage
users = {'full_name':'keval','email':'kevalkrishna2002@gmail.com','password':"abc"}

def is_valid_login(full_name, email, password):
    # Replace this with your actual authentication logic
    # Check the provided Full name, email, and password against your database or authentication mechanism
    # If the credentials are valid, return True; otherwise, return False
    for user in users:
        if users['full_name'] == full_name and users['email'] == email and users['password'] == password:
            return True
    return False
        # print(user[0])
        # return user[0]

@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.files:
        upload_file()
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Replace this with your actual authentication logic
    if is_valid_login(full_name, email, password):
        # Store user data in session to remember login status
        session['full_name'] = full_name
        session['email'] = email
        # return redirect(url_for('templates\index.html'))
        print('abc---')
        return render_template('index.html')
    else:
        #flash('Invalid credentials!!!!. Please try again.', 'error')
        # return redirect(url_for('templates\login.html'))
        return render_template('login.html')



@app.route('/index', methods=['GET', 'POST'])
# def index():
def upload_file():
    if 'email' not in session:
        return redirect(url_for('index.html.')) 

    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']

        # Check if the file has a valid extension (e.g., .png, .jpg)
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file:
            # Save the uploaded file temporarily
            filename = 'uploaded_image.png'
            file.save(filename)

            # Process the uploaded image
            image = cv2.imread(filename)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Image processing code
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(blurred, 75, 200)

            # Find contours in the edge map
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            docCnt = None

            if len(cnts) > 0:
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
                for c in cnts:
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                    if len(approx) == 4:
                        docCnt = approx
                        break
            
            if docCnt is not None:
                # Apply a four-point perspective transform
                paper = four_point_transform(image, docCnt.reshape(4, 2))
                warped = four_point_transform(gray, docCnt.reshape(4, 2))

                # Apply Otsu's thresholding method
                thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

                # Find contours in the thresholded image
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                questionCnts = []

                # Loop over the contours
                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    ar = w / float(h)

                    if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                        questionCnts.append(c)

                # Sort the question contours top-to-bottom
                questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
                correct = 0

                # Loop over the questions
                for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
                    cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
                    bubbled = None

                    # Loop over the sorted contours
                    for (j, c) in enumerate(cnts):
                        mask = np.zeros(thresh.shape, dtype="uint8")
                        cv2.drawContours(mask, [c], -1, 255, -1)

                        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                        total = cv2.countNonZero(mask)

                        if bubbled is None or total > bubbled[0]:
                            bubbled = (total, j)

                    color = (0, 0, 255)
                    k = ANSWER_KEY[q]

                    if k == bubbled[1]:
                        color = (0, 255, 0)
                        correct += 1

                    cv2.drawContours(paper, [cnts[k]], -1, color, 3)

                # Calculate the score
                total_questions = len(ANSWER_KEY)
                score = (correct / total_questions) * 100
                print("[INFO] score: {:.2f}%".format(score))
                cv2.putText(paper, "{:.2f}%".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                cv2.imshow("Original", image)
                cv2.imshow("Exam", paper)
                cv2.waitKey(0)
                cv2.putText(image, "Score: {:.2f}%".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # Save the processed image to a file
            result_image_filename = 'static/result_image.png'
            cv2.imwrite(result_image_filename, image)

            return render_template('index.html', score=score, result_image=result_image_filename)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)