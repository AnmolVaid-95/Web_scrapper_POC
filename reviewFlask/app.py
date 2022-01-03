from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST': # This will only work if request is in form of POST
        try:
            searchString = request.form['content'].replace(" ","") # User defined string to search object
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString # Creating a url and concatenating the user defined object with the website link and creating our url
            uClient = uReq(flipkart_url) # Using request function to go to the url and open it || import urlopen as uReq || uReq is alias of urlopen
            flipkartPage = uClient.read() # Reading the content from url
            uClient.close() # closing the url as we have read all details in this url
            flipkart_html = bs(flipkartPage, "html.parser") # After ftetching the content we create a parser to parse the content of html tree
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"}) # Finding the particular
            del bigboxes[0:3] # Going to particular location and fetch deleting the contents from 1,2 and 3 location
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href'] # Going to the particular product link using base url || after reaching the product we will scrap the whole data
            prodRes = requests.get(productLink) # Bring the content of the product link using request module.
            prodRes.encoding='utf-8' # Making encoding utf-8, it is equivalent to English character
            prod_html = bs(prodRes.text, "html.parser") # Creating a parser so that we will parse the content of html tree
            print(prod_html) # Printing the content of the content that we have got
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"}) # From that particular content we go to particular div tag and storing the result in a variable

            filename = searchString + ".csv" # Creating a file in csv format with  and creating the file name based on the string that you have searched for
            fw = open(filename, "w") # Opening the file in WRITE mode, this command will overwrite the file if this file exist already
            headers = "Product, Customer Name, Rating, Heading, Comment \n" # Creating the columns that we will add into our file
            fw.write(headers) # Writing the headers in file
            reviews = []  # Creating a empty list with name review and we will append all the text that we have in parser using for loop
            for commentbox in commentboxes: # Using for loop to append the text in list and then add it in csv file
                try:
                    #name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text # Writing name in csv file

                except:
                    name = 'No Name'

                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text # Writing rating in csv file


                except:
                    rating = 'No Rating'

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text # Writing comment head of te comments column in csv file

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text # Writing customer comment in csv file
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment} # After completion of above commands we store the value on a dictionary
                reviews.append(mydict) # Appendig the dictionary into the list in each iteration. Thus adding all reviews
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)]) # Making our reviw will n-1
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)
