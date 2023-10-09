import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

HB_API = "Hyperbeam API KEY here"

#hyperbeam api won't let you create any more sessions than your limit
#so im not tracking # of current sessions in flask
def create_session(url):
    payload = {"start_url": url,"timeout":{"absolute": 300,"warning": None,"offline": 15}}
    headers = {'Authorization': f'Bearer {HB_API}'}

    response = requests.request("POST", "https://engine.hyperbeam.com/v0/vm", json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()['embed_url']
    else:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
     if request.method == 'GET':
         return render_template("index.html")
     if request.method == 'POST':
         if request.form['url']:
             url = request.form['url'].strip()
             embed_url = create_session(url)
             if embed_url != False:
                 return redirect(embed_url, code=302)
             else:
                 return "Session creation failed. Try again later."

if __name__ == '__main__':
    app.run(debug=False)
