import tkinter as tk
import random
import string

#fungsi generate pw
def generate_password():
    try:
        jumlah_huruf = int(entry_huruf.get())
        jumlah_angka = int(entry_angka.get())
        jumlah_simbol = int(entry_simbol.get())
    except:
        hasil_label.config(text="Input harus angka!")
        return
    
    #buet nilai e kosong luk
    password_list = []
    
    #buet perulangan masing masing huruf angka dan simbol biar progrm pack ngmbik berkali kali
    for i in range(jumlah_huruf):
        #ngambik huruf random
        password_list.append(random.choice(string.ascii_letters))

    for i in range(jumlah_angka):
        #ngambik  angka random
        password_list.append(random.choice(string.digits))

    for i in range(jumlah_simbol):
        #ngambik simbol random
        password_list.append(random.choice(string.punctuation))

    random.shuffle(password_list)

    password = "".join(password_list)

    hasil_label.config(text=password)

#GUI
root = tk.Tk()
root.title("Password Generator")
root.geometry("600x400")

#input generate pw
tk.Label(root, text="Jumlah Huruf").pack()
entry_huruf = tk.Entry(root)
entry_huruf.pack()

tk.Label(root, text="Jumlah Angka").pack()
entry_angka = tk.Entry(root)
entry_angka.pack()

tk.Label(root, text="Jumlah Simbol").pack()
entry_simbol = tk.Entry(root)
entry_simbol.pack()

#button
tk.Button(root, text="Generate Password", command=generate_password).pack(pady=10)

#output
hasil_label = tk.Label(root, text="", font=("Arial",12))
hasil_label.pack()

root.mainloop()