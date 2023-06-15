from tkinter import *
import socket
from tkinter import filedialog
from tkinter import messagebox
import os
from tkinter import ttk

root = Tk()
root.title("Swift Send")
root.geometry("406x475+320+150")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

selected_files = []  # Menyimpan daftar file yang dipilih

def Send():
    main = Toplevel(root)
    main.title("Send")
    main.geometry("406x475+800+150")
    main.resizable(False, False)

    def SelectFiles():
        global selected_files
        selected_files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                                    title="Select Image Files",
                                                    filetypes=(("Text Files", ".txt"), ("All Files", ".*")))
        for file in selected_files:
            file_path = os.path.basename(file)  # Ambil nama file saja dari path
            index = len(listview.get_children()) + 1
            listview.insert("", "end", text=index, values=(index, file_path))

    def Sender():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        port = 8080
        s.connect((IPAddress.get(), port))

        for file in selected_files:
            file_data = open(file, "rb").read(1024)
            while file_data:
                s.send(file_data)
                file_data = open(file, "rb").read(1024)

        s.close()
        print("Files have been transmitted successfully")
        messagebox.showinfo("File received", "Files have been transmitted successfully")
        listview.delete(*listview.get_children())  # Menghapus semua item dalam listview
        selected_files = []  # Mengosongkan daftar file yang dipilih

    bg_send = PhotoImage(file="images/bg_send4.png")
    Label(main, image=bg_send).place(x=-2, y=0)

    select_file = PhotoImage(file="images/select_file.png")
    select = Button(main, image=select_file, borderwidth=0, highlightthickness=0, command=SelectFiles)
    select.place(x=80, y=210)

    icon_send = PhotoImage(file="images/icon_send.png")
    send = Button(main, image=icon_send, borderwidth=0, highlightthickness=0, command=Sender)
    send.place(x=90, y=380)

    host = socket.gethostname()
    Label(main, text=f"ID: {host}", font=("Nunito Sans Normal", 15), bg="#FF2358", fg="Black").place(x=90, y=145)

    Label(main, text="Enter receiver IP address:", font=("Nunito Sans", 12, "bold"), bg="#f4fdfe").place(x=100, y=270)
    IPAddress = Entry(main, width=25, fg="Black", highlightthickness=0, relief='groove', borderwidth=2, bg="#D9D9D9",
                      font=("Nunito Sans Normal", 15))
    IPAddress.place(x=49, y=300)

    listview = ttk.Treeview(main, height=3, columns=("No.", "Name file"))
    listview.pack()

    listview.column("#0", width=0, stretch=NO)
    listview.column("No.", width=50, minwidth=50, anchor="center", stretch=NO)
    listview.column("Name file", width=300, minwidth=300, anchor="w", stretch=NO)

    listview.heading("#0", text="")
    listview.heading("No.", text="No.")
    listview.heading("Name file", text="Name file")
    listview.place(x=25, y=450)
    main.mainloop()


def Receive():
    window = Toplevel(root)
    window.title("Receiver")
    window.geometry("406x475+800+150")
    window.configure(bg="#f4fdfe")
    window.resizable(False, False)

    def Download():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 8080
        s.bind((host, port))
        s.listen(1)
        print("Waiting for incoming connection...")
        conn, addr = s.accept()
        save_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if save_path:
            with open(save_path, "wb") as file:
                while True:
                    file_data = conn.recv(1024)
                    if not file_data:
                        break
                    file.write(file_data)
            print("File has been received successfully")
            messagebox.showinfo("File received", "File has been received successfully")
        else:
            print("No save path selected")
        conn.close()

    bg_receive = PhotoImage(file="images/bg_receive4.png")
    Label(window, image=bg_receive).place(x=-2, y=0)

    Label(window, text="Sender ID", font=("Nunito Sans", 15), bg="#f4fdfe").place(x=20, y=220)
    SenderID = Entry(window, width=35, fg="Black", highlightthickness=0, relief="groove", borderwidth=2,
                     bg="#D9D9D9", font=("Nunito Sans Normal", 13))
    SenderID.place(x=23, y=250)
    SenderID.focus()

    Label(window, text="Save File As", font=("Nunito Sans", 15), bg="#f4fdfe").place(x=20, y=300)
    incoming_file = Entry(window, width=35, fg="Black", highlightthickness=0, relief="groove", borderwidth=2,
                          bg="#D9D9D9", font=("Nunito Sans Normal", 13))
    incoming_file.place(x=23, y=330)

    download = PhotoImage(file="images/download.png")
    select = Button(window, image=download, borderwidth=0, highlightthickness=0, command=Download)
    select.place(x=120, y=390)

    window.mainloop()


Label(root, text="SWIFT SEND", bg="#f4fdfe", font=("Nunito Sans Normal SemiBold", 18)).place(x=123, y=10)
Label(root, text="File Transfer App", bg="#f4fdfe", font=("Nunito Sans", 10)).place(x=148, y=40)

line_image = PhotoImage(file="images/line.png")
line = Label(root, image=line_image, bg="#f4fdfe", bd=0)
line.place(x=0, y=70)

send_image = PhotoImage(file="images/send.png")
send = Button(root, image=send_image, bg="#f4fdfe", bd=0, command=Send)
send.place(x=50, y=100)

receive_image = PhotoImage(file="images/receive.png")
receive = Button(root, image=receive_image, bg="#f4fdfe", bd=0, command=Receive)
receive.place(x=225, y=100)

icon_image = PhotoImage(file="images/icon1.png")
icon = Label(root, image=icon_image, bg="#f4fdfe", bd=0)
icon.place(x=0, y=300)

root.mainloop()
