import os,json
from flask import Flask, jsonify, render_template, redirect, url_for, request
from urllib import urlopen

app = Flask(__name__)

def keywords(term):
    keyword = term
    global pos_cnt1
    if keyword == "":
        pos_cnt1 = 0
        return ""
    

    final=""
    ekeyword = keyword
    nkeyword = ekeyword.splitlines()

    pos_cnt1 = len(nkeyword)

    for i in range(0,len(nkeyword)):
        if i == 0:
            nkeyword[i] = "\\\\\"" + nkeyword[i] + "\\\\\""
        else:
            nkeyword[i] = " OR "+"\\\\\"" + nkeyword[i] + "\\\\\""

    for i in range(0,len(nkeyword)):
        final+=nkeyword[i]

    final = "(" + final + ")"

    return final

def context(contxt):
    keyword = contxt
    global pos_cnt2
    if keyword == "":
        pos_cnt2 = 0
        return ""
    

    final=""
    ekeyword = keyword
    nkeyword = ekeyword.splitlines()

    pos_cnt2 = len(nkeyword)

    for i in range(0,len(nkeyword)):
        if i == 0:
            nkeyword[i] = "\\\\\"" + nkeyword[i] + "\\\\\""
        else:
            nkeyword[i] = " OR "+"\\\\\"" + nkeyword[i] + "\\\\\""

    for i in range(0,len(nkeyword)):
        final+=nkeyword[i]

    final = "(" + final + ")"

    return final

def exclude(excl):
    keyword = excl
    global neg_cnt
    if keyword == "":
        neg_cnt=0
        return ""
    

    final=""
    ekeyword = keyword
    nkeyword = ekeyword.splitlines()

    neg_cnt = len(nkeyword)

    for i in range(0,len(nkeyword)):
        if i == 0:
            nkeyword[i] = "\\\\\"" + nkeyword[i] + "\\\\\""
        else:
            nkeyword[i] = " OR "+"\\\\\"" + nkeyword[i] + "\\\\\""

    for i in range(0,len(nkeyword)):
        final+=nkeyword[i]

    final = "-(" + final + ")"

    return final

@app.route('/',methods = ['GET','POST'])
def Query():
    x=""
    xx=""
    y=""
    final=""
    z=""
    if request.method == 'POST':
        term=request.form['keywords']
        contxt=request.form['context']
        excl=request.form['excludes']
        x = str(keywords(term))
        xx = str(context(contxt))
        y = str(exclude(excl))
        z = "-is:retweet"
        final = "{\"value\":\""+x+" "+xx+" "+y+" "+z+"\"},"

        pos = pos_cnt1 + pos_cnt2

        if (pos > 30 or neg_cnt > 50):
            final = "Error : Keywords exceeded"

        if (len(final)>1024):
            final = "Error : Character limit exceeded > 1024 chars"

    return render_template('index.html',final=final)



port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port),debug=True)