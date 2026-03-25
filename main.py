import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook
import random
import string
import os

dataPassword = []

def cekPassword():
    password = entryPassword.get()

    if password == "":
        messagebox.showwarning("Peringatan", "Password belum diisi")
        return

    if not os.path.exists("password_umum.txt"):
        messagebox.showerror("Error", "File password_umum.txt tidak ditemukan")
        return

    with open("password_umum.txt", "r") as file:
        daftar = [line.strip() for line in file]

    if password in daftar:
        messagebox.showerror("Rentan", "Password terlalu umum dan mudah ditebak")
    else:
        messagebox.showinfo("Aman", "Password tidak ada di daftar umum")

def estimasiCrack():
    password = entryPassword.get()

    if password == "":
        messagebox.showwarning("Peringatan", "Password belum diisi")
        return

    charset = 0

    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(not c.isalnum() for c in password):
        charset += 32

    panjang = len(password)
    kombinasi = charset ** panjang

    laptop = kombinasi / 1_000_000
    gpu = kombinasi / 1_000_000_000
    superc = kombinasi / 1_000_000_000_000

    def formatWaktu(detik):
        if detik < 60:
            return f"{int(detik)} detik"
        menit = detik / 60
        if menit < 60:
            return f"{int(menit)} menit"
        jam = menit / 60
        if jam < 24:
            return f"{int(jam)} jam"
        hari = jam / 24
        if hari < 365:
            return f"{int(hari)} hari"
        tahun = hari / 365
        return f"{int(tahun)} tahun"

    hasil = f"""
Laptop biasa : {formatWaktu(laptop)}
GPU kuat : {formatWaktu(gpu)}
Supercomputer : {formatWaktu(superc)}
"""

    messagebox.showinfo("Estimasi Crack", hasil)

def generatePassword():
    length = entryLength.get()

    if length == "":
        messagebox.showwarning("Peringatan", "Panjang password harus diisi")
        return

    try:
        length = int(length)
    except:
        messagebox.showerror("Error", "Panjang harus angka")
        return

    chars = ""

    if varLower.get():
        chars += string.ascii_lowercase
    if varUpper.get():
        chars += string.ascii_uppercase
    if varNumber.get():
        chars += string.digits
    if varSymbol.get():
        chars += string.punctuation

    if chars == "":
        messagebox.showwarning("Peringatan", "Pilih minimal satu opsi karakter")
        return

    password = "".join(random.choice(chars) for _ in range(length))
    entryPassword.delete(0, tk.END)
    entryPassword.insert(0, password)


def tambahData():
    Website = entryWebsite.get()
    username = entryUsername.get()
    password = entryPassword.get()

    if Website == "" or username == "" or password == "":
        messagebox.showwarning("Peringatan", "Semua field harus diisi")
        return

    dataPassword.append([Website, username, password])

    tree.insert("", "end", values=(Website, username, password))

    entryWebsite.delete(0, tk.END)
    entryUsername.delete(0, tk.END)
    entryPassword.delete(0, tk.END)


def simpanExcel():
    if len(dataPassword) == 0:
        messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan")
        return

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Password Manager"

    sheet.append(["Akun", "Username", "Password"])

    for data in dataPassword:
        sheet.append(data)

    try:
        workbook.save("password_manager.xlsx")
        messagebox.showinfo("Sukses", "Data berhasil disimpan ke password_manager.xlsx")
    except:
        messagebox.showerror("Error", "Gagal menyimpan file")


root = tk.Tk()
root.title("Password Manager")
root.geometry("650x450")

frameInput = tk.Frame(root)
frameInput.pack(pady=10)

tk.Label(frameInput, text="Website : https://").grid(row=0, column=0)
entryWebsite = tk.Entry(frameInput)
entryWebsite.grid(row=0, column=1)

tk.Label(frameInput, text="Username atau Email : ").grid(row=1, column=0)
entryUsername = tk.Entry(frameInput)
entryUsername.grid(row=1, column=1)

tk.Label(frameInput, text="Password : ").grid(row=2, column=0)
entryPassword = tk.Entry(frameInput, width=25)
entryPassword.grid(row=2, column=1)

tk.Button(frameInput, text="Cek Kerentanan", command=cekPassword).grid(row=2, column=3, padx=5)

frameGenerate = tk.Frame(root)
frameGenerate.pack(pady=5)

tk.Label(frameGenerate, text="Length").grid(row=0, column=0)
entryLength = tk.Entry(frameGenerate, width=5)
entryLength.grid(row=0, column=1)

varLower = tk.IntVar()
varUpper = tk.IntVar()
varNumber = tk.IntVar()
varSymbol = tk.IntVar()

tk.Checkbutton(frameGenerate, text="Lowercase", variable=varLower).grid(row=0, column=2)
tk.Checkbutton(frameGenerate, text="Uppercase", variable=varUpper).grid(row=0, column=3)
tk.Checkbutton(frameGenerate, text="Angka", variable=varNumber).grid(row=0, column=4)
tk.Checkbutton(frameGenerate, text="Symbol", variable=varSymbol).grid(row=0, column=5)

tk.Button(frameGenerate, text="Generate", command=generatePassword).grid(row=0, column=6, padx=5)
tk.Button(frameGenerate, text="Estimasi Crack", command=estimasiCrack).grid(row=0, column=8, padx=5)

tk.Button(root, text="Tambah Data", command=tambahData).pack(pady=5)

tk.Button(root, text="Simpan ke Excel", command=simpanExcel).pack(pady=5)

columns = ("Website", "Username", "Password")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
    
tree.pack(expand=True, fill="both", pady=10)

root.mainloop()