#web scrape the beginning

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50,50,500,300)
        self.setWindowTitle("WebScraper")
        #any time we want to add a file menu we can reuse these 4 lines
        extractAction = QtWidgets.QAction("&Click Here To Close Window", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)

        #editor
        openEditor = QtWidgets.QAction("&Editor", self)
        openEditor.setShortcut("Ctrl+E")
        openEditor.setStatusTip('Open Editor')
        openEditor.triggered.connect(self.editor)
        
        #save file
        saveFile = QtWidgets.QAction("&Save File", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)

        #open file
        openFile = QtWidgets.QAction("&Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)

        #scrape and save
        scrapeFile = QtWidgets.QAction("&Save File", self)
        scrapeFile.setShortcut("Ctrl+G")
        scrapeFile.setStatusTip('Save File')
        scrapeFile.triggered.connect(self.webscrape)
        
        self.statusBar()

        mainMenu = self.menuBar()
        #file menu
        fileMenu = mainMenu.addMenu('&File')
        #openfile
        fileMenu.addAction(openFile)
        #savefile
        fileMenu.addAction(saveFile)
        #editor menu
        editorMenu = mainMenu.addMenu("&Editor")
        editorMenu.addAction(openEditor)
        #scrape menu
        scrapeMenu = mainMenu.addMenu("&WebScrape")
        scrapeMenu.addAction(scrapeFile)
        #quit menu
        quitMenu = mainMenu.addMenu("&Quit")
        quitMenu.addAction(extractAction)
        
        self.home()


    def file_save(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self,'Save File')

        #check if file exists
        if filename[0]:
            file = open(filename[0],'w')

            #convert to plain text
            text = self.textEdit.toPlainText()
            
            file.write(text)
            file.close()
        
    def file_open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,'Open File')

        #specify home directory /C or /User  /directory and etc.
        #filename = QtWidgets.QFileDialog.getOpenFileName(self,'Open File','/Users')
        #print(type(name))

        #check if file exists
        if filename[0]:
            
            file = open(filename[0],'r')

            #call editor to load the file into
            if file:
               self.editor()

            with file:
                text = file.read()
                self.textEdit.setText(text)
                
    def editor(self):
        self.textEdit = QtWidgets.QTextEdit()
        self.setCentralWidget(self.textEdit)
        
    def home(self):
        """
        btn = QtWidgets.QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())
        btn.move(200,200)
        """
        self.show()
        
    def close_application(self):
        choice = QtWidgets.QMessageBox.question(self,'Extract',
                                                "Quitting?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            print("Quiting Now!")
            sys.exit()
        else:
            #print("Well, stay if you must.")
            pass

    def webscrape(self):
    
        theurl = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20cards'

        #open up connection and download the page
        uClient = uReq(theurl)
        page_raw = uClient.read()
        uClient.close()

        #html parser
        page_soup = soup(page_raw, "html.parser")
        #grabs each item
        the_containers = page_soup.findAll("div",{"class":"item-container"})
        container = the_containers[0]

        #print(container.find('a',"item-brand"))
        #spec_brand = container.find("li","price-ship").text.strip()
        #print(spec_brand)

        #write a cvs file to the pytest directory
        name = QtWidgets.QFileDialog.getSaveFileName(self,'Save File')

        if name[0]:
            
            f = open(name[0], "w")
            headers = "brand, product_name, shipping_cost\n"
            f.write(headers)

            for container in the_containers:
                spec_brand = container.find("div", "item-branding").a.img["title"]
                spec_title = container.a.img["title"]
                shipping_cost = container.find("li","price-ship").text.strip()

                #print("brand: " + spec_brand)
                #print("product_name: " + spec_title)
                #print("shipping_cost: " + shipping_cost)
                f.write(spec_brand + "," + spec_title.replace(",","|") + ","+ shipping_cost+"\n")

            f.close()
        

def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    #app.exec_() <--Qt5 and up
    sys.exit(app.exec_())

run()
    
    
