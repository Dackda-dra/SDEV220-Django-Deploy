#camelCase

#design a GUI for a library that must
# 1. Be able to add a book
# 2. store the book name, author, and genre
# 3. List all stored books
# 4. Check if a book in the list is available or not
# 5. check in/out selected book


# Update requirement -- 
# Seperate data retrieval and storage into their own class.
#Separate listbox into its own class
# Use SQL or JSON as data storage instead of a txt file



import tkinter as tk
import json
import tkinter.messagebox




#create global variables

# open file and extract stored names

class DataLoader:
    def __init__(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        self.bookNameList = data['BookNameList']
        self.bookAuthorList = data['BookAuthorList']
        self.bookGenreList = data['BookGenreList']
        self.bookAvailable = data['BookAvailable']





class library:
    

    #get lists
    def __init__(self, dl):
        self.data_loader = dl
    
    
    #functions
    def addBook(self):
        #create window
        addBookWindow = tk.Tk()
        #title window
        addBookWindow.title('Add a Book')
        
        # Create frames
        bookNameFrame = tk.Frame(addBookWindow)
        bookAuthorFrame  = tk.Frame(addBookWindow)
        bookGenreFrame  = tk.Frame(addBookWindow)
        bookAvailFrame = tk.Frame(addBookWindow)
        finishedFrame = tk.Frame(addBookWindow)
        
        #widgets for frames
        #--------------------------- Name
        bookNamePrompt = tk.Label(bookNameFrame,
                                    text='Enter book name: ')
        self.getBookName = tk.Entry(bookNameFrame,
                                        width=10,
                                        borderwidth=1,
                                        relief='solid')
        #---------------------------------------- Author
        bookAuthorPrompt = tk.Label(bookAuthorFrame,
                                    text='Enter book author: ')
        self.getBookAuthor = tk.Entry(bookAuthorFrame,
                                        width=10,
                                        borderwidth=1,
                                        relief='solid')
        #-------------------------------Genre
        bookGenrePrompt = tk.Label(bookGenreFrame,
                                    text='Enter book genre: ')
        self.getBookGenre = tk.Entry(bookGenreFrame,
                                        width=10,
                                        borderwidth=1,
                                        relief='solid')
        #initalizebool
        self.getBookAvailCB = tk.BooleanVar()
        
        #Check button fix, function on click that changes value.
        def toggleAvailability():
            self.getBookAvailCB.set(not self.getBookAvailCB.get())
        
        self.getBookAvail = tk.Checkbutton(bookAvailFrame,
                                           text='Is this book Available?',
                                           onvalue=True,
                                           offvalue=False,
                                           variable=self.getBookAvailCB,
                                           command=toggleAvailability)
        
        #------------------------------------done
        addButton = tk.Button(finishedFrame,
                                 text='Add Book',
                                 command=self.addBookCycle)
        quitButton = tk.Button(finishedFrame,
                                    text='Done',
                                    command=addBookWindow.destroy)
        
        
        
        #pack widgets
        bookNamePrompt.pack(side='left')
        self.getBookName.pack(side='right')
        bookAuthorPrompt.pack(side='left')
        self.getBookAuthor.pack(side='right')
        bookGenrePrompt.pack(side='left')
        self.getBookGenre.pack(side='right')
        self.getBookAvail.pack(side='right')
        addButton.pack(side='left')
        quitButton.pack(side='right')
        #pack frames
        bookNameFrame.pack()
        bookAuthorFrame.pack()
        bookGenreFrame.pack()
        bookAvailFrame.pack()
        finishedFrame.pack()
        
        
        
    #this adds a book to the lists
    def addBookCycle(self):
        #retrieve text
        bookName = str(self.getBookName.get())
        bookAuthor = str(self.getBookAuthor.get())
        bookGenre = str(self.getBookGenre.get())
        #book available check
        if self.getBookAvailCB.get() == False:
            bookAvail = 0
        else:
            bookAvail = 1
            
            
        # good flag not used currently, kept for ease of bug squashing/testing later
        nameFlag = True
        authorFlag = True
        genreFlag = True
        
                
            
        if nameFlag == True and authorFlag == True and genreFlag == True:
            #add to list
            dl.bookNameList.append(bookName)
            dl.bookAuthorList.append(bookAuthor)
            dl.bookGenreList.append(bookGenre)
            dl.bookAvailable.append(bookAvail)
            #save to db
            data = {"BookNameList": dl.bookNameList, "BookGenreList": dl.bookGenreList, "BookAuthorList": dl.bookAuthorList, "BookAvailable": dl.bookAvailable}
            with open("data.json", "w") as f:
                json.dump(data, f)
            
            
            
            #create new class in different program for addbookcycle, have it import 'add book' to get variables and child of addbook. #################################
        
    

  
            
        
    def quitSave(self): 
                
        #open file     
        data = {"BookNameList": dl.bookNameList, "BookGenreList": dl.bookGenreList, "BookAuthorList": dl.bookAuthorList, "BookAvailable": dl.bookAvailable}
        with open("data.json", "w") as f:
            json.dump(data, f)
            
        #finish
        #wanted to add close all windows here but didn't know how to check if window is open
        self.mainWindow.destroy()

    
    # create 6 frames
    
    def GUI(self):
        #create window
        self.mainWindow = tk.Tk()
        
        #title window
        self.mainWindow.title("Python Library")
        
        #create frames
        menuFrame = tk.Frame(self.mainWindow)
        buttonsFrame = tk.Frame(self.mainWindow)
        quitFrame = tk.Frame(self.mainWindow)
        
        #picture frame
        pictureFrame = tk.Frame(self.mainWindow)
        pictureFrame.place(anchor='center', relx=0.5, rely=0.5)
        
        
        #create picture
        

        
        #menuwidgets
        menuLabel = tk.Label(self.mainWindow,
                                         text='Select one of the below options')
        #button widgets
        
        addBookButton = tk.Button(buttonsFrame,
                                 text='Add Book',
                                 command=self.addBook)
        
       
        listBooksButton = tk.Button(buttonsFrame,
                                  text='List Books',
                                  command=lambda: listBooks.listbox(self))
        
        
        #quit widgets
        quitButton = tk.Button(quitFrame,
                                    text='Quit',
                                    command=self.quitSave)
        
        #pack widgets and labels
        menuLabel.pack()
        addBookButton.pack()
        listBooksButton.pack()
        quitButton.pack()
        
        #pack frames
        pictureFrame.pack()
        menuFrame.pack()
        buttonsFrame.pack()
        quitFrame.pack()
        
        #enter loop
        tk.mainloop()
        
        
        



class listBooks(library):
    
    #get info from file
    def __init__(self, dl):
        super().__init__(dl)
        
    def listbox(self):
        
        #create widget
        listOfBooksTestWindow = tk.Tk()
        listOfBooksTestWindow.title('List of Books')
        
        #create scroll bar
        listBooksScroll = tk.Scrollbar(listOfBooksTestWindow, orient='vertical')
        #createlistbox + scrollcmd
        self.listOfBooksTest = tk.Listbox(listOfBooksTestWindow, height='10', width='20', yscrollcommand=listBooksScroll.set)
        listBooksScroll.config(command=self.listOfBooksTest.yview)
        
        #createframe for buttons
        listButtonsFrame = tk.Frame(listOfBooksTestWindow)
        

        
       
        #create buttons for CheckIn,Out, Available
        checkInButton = tk.Button(listButtonsFrame,
                                  text='Check In',
                                  command=lambda: listBooks.checkIn(self))
        
        checkOutButton = tk.Button(listButtonsFrame,
                                           text='Check Out',
                                           command=lambda: listBooks.checkOut(self))
        
        checkAvailButton = tk.Button(listButtonsFrame,
                                          text='Check Availability',
                                          command=lambda: listBooks.checkAvail(self))
        
        deleteButton = tk.Button(listButtonsFrame,
                                 text='Delete',
                                 command=lambda: listBooks.delete(self))
        
        # quit button
    
        listQuitButton = tk.Button(listButtonsFrame,
                                    text='Done',
                                    command=listOfBooksTestWindow.destroy)
        
        
        #pack
        #self.listPictureLabel.pack()
        checkInButton.pack()
        checkOutButton.pack()
        checkAvailButton.pack()
        deleteButton.pack()
        listQuitButton.pack()
        listBooksScroll.pack(side='right', fill='y')
        self.listOfBooksTest.pack(side='left', fill='both', expand='1')
        #self.listPicture.pack()
        
        
        #pack frame
        listButtonsFrame.pack(side='bottom')
        
        #initialize var for listbox
        insertBookArray = ['','','']
        count = 0
            # populate list box
        for len in dl.bookNameList:
            insertBookArray[0] = dl.bookNameList[count]
            insertBookArray[1] = dl.bookAuthorList[count]
            insertBookArray[2] = dl.bookGenreList[count]
            insertBook = str(insertBookArray[0] + ' | ' + insertBookArray[1] + ' | ' + insertBookArray[2])
            self.listOfBooksTest.insert('end',insertBook)
            count = count + 1
            
            
            
    def checkIn(self):
       for item in self.listOfBooksTest.curselection():
           index = int(item)
           dl.bookAvailable[index] = 1

    def checkOut(self):
        for item in self.listOfBooksTest.curselection():
            index = int(item)
            dl.bookAvailable[index] = 0

        
    def checkAvail(self):
        for item in self.listOfBooksTest.curselection():
            index = int(item)
    
        if index != -1:
            getBookAvailbility = int(dl.bookAvailable[index])
            
            if getBookAvailbility == 1:
                tk.messagebox.showinfo('Results', dl.bookNameList[index] + ' is available.')
            else:
                tk.messagebox.showinfo('Results', dl.bookNameList[index] + ' is not available.')
        else:
            tk.messagebox.showerror('Error', 'Please select a book.')
            
    def delete(self):
        for item in self.listOfBooksTest.curselection():
            index = int(item)
            #to remove str need var
            deleteName = dl.bookNameList[index]
            deleteAuthor = dl.bookAuthorList[index]
            deleteGenre = dl.bookGenreList[index]
            deleteAvail = dl.bookAvailable[index]
            #remove str from list
            dl.bookNameList.remove(deleteName)
            dl.bookAuthorList.remove(deleteAuthor)
            dl.bookGenreList.remove(deleteGenre)
            dl.bookAvailable.remove(deleteAvail)
            #delete curselection, and save to db
            self.listOfBooksTest.delete(index)
            data = {"BookNameList": dl.bookNameList, "BookGenreList": dl.bookGenreList, "BookAuthorList": dl.bookAuthorList, "BookAvailable": dl.bookAvailable}
            with open("data.json", "w") as f:
                json.dump(data, f)
                
                
        
        
        
if __name__ == '__main__':
    
    dl = DataLoader("data.json")
    library = library(dl)       
    list_Books = listBooks(dl)
    final = library
    final.GUI()
    