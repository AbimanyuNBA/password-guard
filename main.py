import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook
import random
import string

#baca file password umum
with open("password_umum.txt", "r", encoding="utf-8", errors="ignore") as file:
 daftar_password_umum = file.read().splitlines()

#fungsi cek password
def cekpw():
    cekpassword = entry_cekpassword.get()

    # hapus isi tabel lama
    for row in tree.get_children():
        tree.delete(row)

    if cekpassword == "":
        messagebox.showerror("Error", "Input tidak boleh kosong")
        return

    if cekpassword in daftar_password_umum:
        messagebox.showwarning("Peringatan", "Password terlalu umum")
        
    #cekpanajng pw
    panjang = len(cekpassword)
    
    # cek huruf besar,kecil,angka,dan simbol
    besar = any(c.isupper() for c in cekpassword)
    kecil = any(c.islower() for c in cekpassword)
    angka = any(c.isdigit() for c in cekpassword)

    daftar_simbol = "!@#$%^&*()"
    simbol = any(c in daftar_simbol for c in cekpassword)

    score = 0
#memebrikan validasi jaki skornya lebih dri 8 makan akan bertmabah 1
    if panjang >= 8:
        score += 1
    if besar:
        score += 1
    if kecil:
        score += 1
    if angka:
        score += 1
    if simbol:
        score += 1
#validasi level keamanan
    if score <= 2:
        strength = "Weak"
    elif score == 3:
        strength = "Medium"
    else:
        strength = "Strong"


#buat indikator
    indikator = "\u2588" * score + "\u2591" * (5 - score)

# menentukan warna
    if strength == "Weak":
       warna = "red"
    elif strength == "Medium":
       warna = "orange"
    else:
       warna = "green"

    if strength == "Weak":
        estimasi = "Beberapa detik"
    elif strength == "Medium":
        estimasi = "Beberapa hari"
    else:
        estimasi = "Ratusan tahun"

    password_umum = "Ya" if cekpassword in daftar_password_umum else "Tidak"

    besar = "Ada" if besar else "Tidak"
    kecil = "Ada" if kecil else "Tidak"
    angka = "Ada" if angka else "Tidak"
    simbol = "Ada" if simbol else "Tidak"
  
  #letak di table
    tree.insert("", "end", values=(
        panjang,
        besar,
        kecil,
        angka,
        simbol,
        password_umum
    ))
    #panggil var nya
    hasil_keamananpw.config(text=f"Kekuatan password: {strength}")

    hasil_indikatorpw.config(text=f"Indikator password: {'\u2588' * score}", fg=warna)

    hasil_bobol.config(text=f"Estimasi dibobol password: {estimasi}")
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

    hasil_label.config(text=f"Hasil generate pw {password}")

#GUI
root = tk.Tk()
root.title("Password Generator")
root.geometry("1000x800")

#input cek pw
tk.Label(root,text="cek password").pack()
entry_cekpassword = tk.Entry(root)
entry_cekpassword.pack()

#button cek pw

tk.Button(root, text="cek Password", command=cekpw).pack(pady=10)

#table
columns = ("panjang password", "huruf besar", "huruf kecil", "angka", "simbol", "passsword umum")
tree = ttk.Treeview(root,columns=columns, show="headings")

for col in columns:
    tree.heading(col,text=col)
    tree.column(col, width=120)
tree.pack(pady=10)    



#konfigure warna
tree.tag_configure("lulus")


#hasil keamanan pw
hasil_keamananpw = tk.Label(root, text="kekuatan password:", font=("Arial",9))
hasil_keamananpw.pack()

hasil_indikatorpw = tk.Label(root, text="indikator password:", font=("Arial",9))
hasil_indikatorpw.pack()

hasil_bobol = tk.Label(root, text="estimasi dibobol password:", font=("Arial",9))
hasil_bobol.pack()

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
hasil_label = tk.Label(root, text="hasil generete:", font=("Arial",9))
hasil_label.pack()

root.mainloop()