
from flask import Flask, render_template, request, redirect
app_test = Flask(__name__)

app_test.vars={}

app_test.questions={}
app_test.questions['How many eyes do you have?']=('1','2','3')
app_test.questions['Which fruit do you like best?']=('banana','mango','pineapple')
app_test.questions['Do you like cupcakes?']=('yes','no','maybe')

app_test.nquestions=len(app_test.questions)

@app_test.route('/index_test',methods=['GET','POST'])
def index_test():
    nquestions=app_test.nquestions
    if request.method=='GET':
        return render_template('userinfo.html',num=nquestions)
    else:
        #request was a post
        app_test.vars['name']=request.form['name']
        app_test.vars['age']=request.form['age']

        f=open('%s_%s.txt'%(app_test.vars['name'],app_test.vars['age']),'w')
        f.write('Name: %s\n'%(app_test.vars['name']))
        f.write('Age: %s\n\n'%(app_test.vars['age']))
        f.close()

        return redirect('/main_test')

@app_test.route('/main_test')
def main_test():
    if len(app_test.questions)==0:return render_template('end_test.html')
    return redirect('/next')

@app_test.route('/next',methods=['GET'])
def next_get():
    #for clarity
    n=app_test.nquestions-len(app_test.questions)+1
    q=list(app_test.questions.keys())[0]
    a1,a2,a3=list(app_test.questions.values())[0]

    app_test.currentq=q
    return render_template('layout_test.html',num=n,question=q,ans1=a1,ans2=a2,ans3=a3)

@app_test.route('/next', methods=['POST'])
def next_post():
    f = open('%s_%s.txt'%(app_test.vars['name'],app_test.vars['age']),'a') #a is for append
    f.write('%s\n'%(app_test.currentq))
    f.write('%s\n\n'%(request.form['answer_from_layout_test'])) #this was the 'name' on layout.html!
    f.close()

    del app_test.questions[app_test.currentq]

    return redirect('/main_test')

if __name__ == '__main__':
    app_test.run(debug=True)
