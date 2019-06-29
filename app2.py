import tkinter
#import psycopg2
import mysql.connector


class App(tkinter.Frame):
    lbl1 = "ID"
    lbl2 = "First name"
    lbl3 = "Last name"
    lbl4 = "Password"
    
    def __init__(self, master):
        super(App, self).__init__(master)
        self.grid()
        self.create_widgets()
        

    def create_widgets(self):
        lblWidth = 10
        btnWidth = lblWidth
        entWidth = 50
        txtWidth = entWidth
        entBackground = "white"
        txtBackground = entBackground

        padx = 5
        pady = padx
        
        self.lblid = tkinter.Label(self)
        self.lblid["text"] = App.lbl1
        self.lblid["width"] = lblWidth
        self.lblid.grid(row = 0, column = 0, padx = padx, pady = pady)

        self.entid = tkinter.Entry(self)
        self.entid["text"] = ""
        self.entid["width"] = entWidth
        self.entid["background"] = entBackground
        self.entid.grid(row = 0, column = 1, padx = padx, pady = pady)

        self.lblfname = tkinter.Label(self)
        self.lblfname["text"] = App.lbl2
        self.lblfname["width"] = lblWidth
        self.lblfname.grid(row = 1, column = 0, padx = padx, pady = pady)

        self.entfname = tkinter.Entry(self)
        self.entfname["text"] = ""
        self.entfname["width"] = entWidth
        self.entfname["background"] = entBackground
        self.entfname.grid(row = 1, column = 1, padx = padx, pady = pady)

        self.lbllname = tkinter.Label(self)
        self.lbllname["text"] = App.lbl3
        self.lbllname["width"] = lblWidth
        self.lbllname.grid(row = 2, column = 0, padx = padx, pady = pady)

        self.entlname = tkinter.Entry(self)
        self.entlname["text"] = ""
        self.entlname["width"] = entWidth
        self.entlname["background"] = entBackground
        self.entlname.grid(row = 2, column = 1, padx = padx, pady = pady)
        
        self.txtResult = tkinter.Text(self)
        self.txtResult["width"] = txtWidth
        self.txtResult["background"] = txtBackground
        self.txtResult.grid(row = 3, column = 1, rowspan = 4, padx = padx, pady = pady)
        
        self.btnSelect = tkinter.Button(self)
        self.btnSelect["text"] = "Select"
        self.btnSelect["command"] = lambda: self.db_command("Select")
        self.btnSelect["width"] = btnWidth
        self.btnSelect.grid(row = 3, column = 0, padx = padx, pady = pady)
        
        self.btnInsert = tkinter.Button(self)
        self.btnInsert["text"] = "Insert"
        self.btnInsert["command"] = lambda: self.db_command("Insert")
        self.btnInsert["width"] = btnWidth
        self.btnInsert.grid(row = 4, column = 0, padx = padx, pady = pady)

        self.btnUpdate = tkinter.Button(self)
        self.btnUpdate["text"] = "Update"
        self.btnUpdate["command"] = lambda: self.db_command("Update")
        self.btnUpdate["width"] = btnWidth
        self.btnUpdate.grid(row = 5, column = 0, padx = padx, pady = pady)

        self.btnDelete = tkinter.Button(self)
        self.btnDelete["text"] = "Delete"
        self.btnDelete["command"] = lambda: self.db_command("Delete")
        self.btnDelete["width"] = btnWidth
        self.btnDelete.grid(row = 6, column = 0, padx = padx, pady = pady)

        self.lblpwd = tkinter.Label(self)
        self.lblpwd["text"] = App.lbl4
        self.lblpwd["width"] = lblWidth
        self.lblpwd.grid(row = 7, column = 0, padx = padx, pady = pady)

        self.entpwd = tkinter.Entry(self)
        self.entpwd["text"] = ""
        self.entpwd["show"] = "*"
        self.entpwd["width"] = entWidth
        self.entpwd["background"] = entBackground
        self.entpwd.grid(row = 7, column = 1, padx = padx, pady = pady)


    def db_command(self, cmd = ""):
        #db = "python"
        db = "mydb"
        #usr = "postgres"
        usr = "root"
        pwd = self.entpwd.get()
        hst = "127.0.0.1"
        #prt = "5432"
        
        conn = ""
        
        try:
##            conn = psycopg2.connect(
##                dbname = db,
##                user = usr,
##                password = pwd,
##                host = hst,
##                port = prt
##                )
            conn = mysql.connector.connect(
                database = db,
                user = usr,
                password = pwd,
                host = hst
                )
            
            self.txtResult.delete(0.0, tkinter.END)
            cur = conn.cursor()

            #tbl = "test"
            tbl = "testtest"

            if cmd == "Select":
                cur.execute("select * from " + tbl + ";")
                recs = cur.fetchall()
                
                for rec in recs:
                    self.txtResult.insert(tkinter.END, App.lbl1 + ": " + str(rec[0]) + "\n")
                    self.txtResult.insert(tkinter.END, App.lbl2 + ": " + rec[1] + "\n")
                    self.txtResult.insert(tkinter.END, App.lbl3 + ": " + rec[2] + "\n\n")
                    
            else:
                fld1 = "id" #primary key

                if cmd == "Delete":
                    cur.execute("delete from " + tbl + " where " + fld1 + "=" + self.entid.get() + ";")

                else:
                    fld2 = "fname"
                    fld3 = "lname"

                    if cmd == "Insert":
                        cur.execute(
                            "insert into " + tbl + "(" + fld1 + "," + fld2 + "," + fld3 + ") values (%s, %s, %s);",
                            (self.entid.get(), self.entfname.get(), self.entlname.get())
                            )

                    elif cmd == "Update":
                        cur.execute(
                            "update " + tbl + " set " + fld2 + "=%s," + fld3 + "=%s where " + fld1 + "=%s;",
                            (self.entfname.get(), self.entlname.get(), self.entid.get())
                            )

                    else: #not Insert, Update, Delete, Select 
                        raise Exception("Unknown command " + cmd)

                conn.commit()
                #self.txtResult.insert(tkinter.END, cur.statusmessage)
                self.txtResult.insert(tkinter.END, str(cur.rowcount) + " row(s) affected")

            cur.close()
            self.entid.delete(0, tkinter.END)
            self.entfname.delete(0, tkinter.END)
            self.entlname.delete(0, tkinter.END)
            
        #except (Exception, psycopg2.Error) as err:
        except (Exception, mysql.connector.Error) as err:
            self.txtResult.insert(tkinter.END, err)
            
        finally:
            if(conn):
                conn.close()


                
root = tkinter.Tk()
root.title("")
root.geometry("600x600")
app = App(root)
root.mainloop()
