
from flask import Flask,render_template,url_for,redirect,request
import model

app = Flask(__name__)




@app.route('/',methods = ['POST','GET'])
@app.route('/home',methods = ['POST','GET'])
def home():
    return render_template("home.html")


@app.route('/ioi',methods = ['POST','GET'])
def ioi():
    return render_template("ioi.html")

@app.route('/decodeioi',methods = ['POST','GET'])
def decodeioi():
    if request.method == 'POST':
        decode_image=request.form['image-to-unmerge']
        decoded_image=request.form['unmerged-image']
        model.unmerge(decode_image,decoded_image)
        return render_template('ioi.html',zzz="Result: images unmerged")
    else:
         return render_template("decodeimage.html") 
@app.route('/encodeioi',methods = ['POST','GET'])
def encodeioi():
    if request.method == 'POST':
        image_one=request.form['image-one']
        image_two=request.form['image-two']
        output=request.form['output']

        model.merge(image_one,image_two,output)
        return render_template('ioi.html',zzz="Result: images merged")
    else:
         return render_template("encodeimage.html")  

@app.route('/toi',methods = ['POST','GET'])
def toi():
    return render_template("toi.html")

@app.route('/decodetoi',methods = ['POST','GET'])
def decodetoi():
    if request.method == 'POST':
        decode_image=request.form['decode-image-name']
        zzz=model.SteganographyDOI.decode_text(decode_image)
        return render_template('toi.html',zzz="Result"+zzz)
    else:
         return render_template("decodetext.html")    
@app.route('/encodetoi',methods = ['POST','GET'])
def encodetoi():
        if request.method == 'POST':
    
            selected_image = request.form['image-name']
            data = request.form['data']
            output = request.form['output']

            model.SteganographyDOI.encode_text(selected_image,data,output)
            
            return render_template('toi.html',zzz="Image Stegnogated")
        else:
         return render_template("encodetext.html")

# @app.route('/<book>')
# def book(book):
#     # final_list=model.bookRecommendation(book)
#     url_list=model.imgUrlList(final_list)
#     return render_template('book.html',final_list=final_list,book_selected=book,url_list=url_list)

# @app.route('/<knn>_test')
# def knn(knn):
#     # final_book_list=model.methodTwo(knn)
#     url_list=model.imgUrlList(final_book_list)
#     return render_template('knn.html',final_book_list=final_book_list,book_selected=knn,url_list=url_list)






@app.route('/data')
def data():
    return render_template("data.html")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=False)