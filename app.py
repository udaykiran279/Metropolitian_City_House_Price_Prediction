from flask import Flask,render_template,request,redirect
import pandas as pd
import pickle
import datetime

app=Flask(__name__)
df=pd.read_csv("Metro Areas.csv")
model=pickle.load(open("model.pkl","rb"))


@app.route("/")
def home():
    cities=sorted(df["City"].unique()) 

    #locations=sorted(df["Location"].unique())

    return render_template("index.html",cities=cities)

@app.route("/_home1",methods=["GET","POST"])
def home1():

    cityval=[i for i in request.form.values()]
    print(cityval)
    locas=list(sorted(df[df["City"]==cityval[0]]["Location"].unique()))
    print(locas)
    return render_template("index1.html",locas=locas,city=cityval[0])

@app.route("/predict",methods=["GET","POST"])

def predict():
    inputs=[i for i in request.form.values()]
    print(inputs)
    predvalue=[int(i) for i in inputs[2:4]]
    if inputs[4]=="Yes":
        inputs[4]=1
    else:
        inputs[4]=0
    predvalue.append(inputs[4])
    print(predvalue)

    newdf=df[df["Location"]==inputs[1]]
    x=newdf.iloc[:,2:5]
    y=newdf.iloc[:,5]
    model.fit(x,y)
    k=model.predict([predvalue])[0]
    if inputs[4]==1:
        inputs[4]="Yes"
    else:
        inputs[4]="No"
    now=datetime.datetime.now()
    url="https://www.google.com/maps/place/"
    sp="+".join(inputs[1].split())
    print(sp)
    viewmap=url+sp
    print(viewmap)

    return render_template("submit.html",viewmap=viewmap,pred_val="₹ "+str(int(abs(k))),cit=inputs[0],locs=inputs[1],sqft=inputs[2],bhk=inputs[3],capar=inputs[4])


if __name__=='__main__':
    app.run(debug=True)








