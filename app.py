# from flask import Flask, Response
# import cv2
# app = Flask(__name__)
# video = cv2.VideoCapture(0)
# @app.route('/')
# def index():
#     return "Default Message"
# def gen(video):
#     while True:
#         success, image = video.read()
#         ret, jpeg = cv2.imencode('.jpg', image)
#         frame = jpeg.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
# @app.route('/video_feed')
# def video_feed():
#     global video
#     return Response(gen(video),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=3000, threaded=True)

# import the necessary packages
from flask import Flask, render_template, Response, redirect, url_for, request


import pandas as pd

counter=0

from camera import VideoCamera,name



app = Flask(__name__)
@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')
def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')





@app.route('/dashboard/<did>', methods = ['GET'])


def dashboard(did):
    # df1 = pd.read_csv("C:/Users/moksh/OneDrive/Documents/ucc/Thesis/Database/ProjectDatabase.csv")
    # # print("Dashboard",did)
    # df2 = df1[(df1["Enrollment Number"] == int(did))]
    # pathex=df2['Timetable'].to_string(index=False)
    # htmldf=pd.read_excel(pathex.strip(),engine='openpyxl')
    # htmldf.fillna('', inplace=True)
    # print("HTMLDF",htmldf)
    # # print(df1)
    # # print("dash df2",df2)
    # return htmldf.to_html()

    #df1 = pd.read_csv("C:/Users/moksh/OneDrive/Documents/ucc/Thesis/Database/ProjectDatabase.csv")
    # print("Dashboard",did)
    #df2 = df1[(df1["Enrollment Number"] == int(did))]
    #pathex = df2['Timetableimg'].to_string(index=False)
    # images = glob.glob(os.path.join(pathex, '*.jpg'))
    #print(pathex)
    # image = Image.open(pathex.strip())
    fname='assets/'+did+'.JPG'

    return render_template('dashboard.html',tt = fname)
# def timetable(did):
#     df1 = pd.read_csv("C:/Users/moksh/OneDrive/Documents/ucc/Thesis/Database/ProjectDatabase.csv")
#     # print("Dashboard",did)
#     df2 = df1[(df1["Enrollment Number"] == int(did))]
#     pathex1 = df2['Timetableimg'].to_string(index=False)
#     # return Response(gen(VideoCamera()),
#     #                 mimetype='multipart/x-mixed-replace; boundary=frame')
#     return send_file(pathex1, mimetype='image/gif')




@app.route('/login',methods=['GET', 'POST'])
def login():
    global counter
    from camera import name
    lname=name
    print("Login:",lname)
    error = None
    if request.method == 'POST':
        if request.form['username'] == name:

            df = pd.read_csv('./data/ProjectDatabase.csv')

            # print(df)
            # # id=int(request.form['id']
            # print(request.form['username'],request.form['id'])
            # print((df[(df["Name"] == request.form['username']) & (df["Enrollment Number"] == int(request.form['id']))]))
            if not ((df[(df["Name"] == request.form['username']) & (df["Enrollment Number"] == int(request.form['id']))]).empty):
                print("Welcome")
                return redirect(url_for('dashboard',did=request.form['id']))
            else:
                if counter>=3:
                    # print(counter)

                    counter=0
                    return redirect('/')
                else:
                    print("Wrong Credentials")
                    error = 'Invalid Credentials. Please try again.'
                    counter+=1


        else:

            if counter>=3:
                counter=0
                return redirect('/')
            else:
                counter+=1
                error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)


if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port='5000', debug=True)
