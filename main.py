from flask import Flask,redirect, url_for, render_template,request
import pickle
import sklearn
import numpy as np

#app id: laptopprice-395105
app=Flask(__name__)

def prediction(lst):
    filepath='laptop/predictor.pickle'
    with open(filepath, 'rb') as file:
        model=pickle.load(file)

    pred= model.predict([lst])
    return pred

@app.route('/',methods=['GET'])
def home_page():
    return render_template('home.html')

@app.route('/style_transfer',methods=['POST','GET'])
def home_style():
    return render_template('style_transfer.html')

@app.route('/laptop', methods=['POST','GET'])
def home():
    pred=0
    if request.method =='POST':
        ram=request.form['ram']
        weight=request.form['weight']
        touchscreen=request.form.getlist('touchscreen')
        ips=request.form.getlist('ips')
        FullHD=request.form.getlist('FullHD')

        company=request.form['company']
        typename=request.form['typename']
        opsys=request.form['opsys']
        cpu=request.form['cpu']
        gpu=request.form['gpu']

        feature_list=[]
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))
        feature_list.append(len(FullHD))

        company_list=['acer','apple', 'asus', 'dell', 'hp','lenovo', 'msi', 'toshiba', 'other']
        typename_list=['2in1Convertible', 'Gaming', 'Netbook','Notebook', 'Ultrabook', 'Workstation']
        opsys_list=['Linux','Mac','Windows','Other']
        cpu_list=['AMD','Intel Celeron Dual','Intel Core M','Intel Core i3','Intel Core i5','Intel Core i7','Intel Pentium Quad','other']
        gpu_list=['AMD','Intel','Nvidia']

        #creating company array
        def traverse(lst, value):
            for item in lst:
                if item==value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)

        traverse(company_list,company)
        traverse(typename_list,typename)
        traverse(opsys_list,opsys)
        traverse(cpu_list, cpu)
        traverse(gpu_list,gpu)

        pred=prediction(feature_list)*353.54
        pred=np.round(pred[0])

        print("prediction", pred)
        print('fl', feature_list)

        return render_template("laptop.html",pred=pred)
    else:
        return render_template('laptop.html')
 
if __name__=="__main__":
    app.run(debug=True)
