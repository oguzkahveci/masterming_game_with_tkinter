import tkinter as tk
from tkinter import Canvas, Entry, Button, messagebox, Label
import random
"""
tkinter gui ile görselleştirdiğimiz bu oyunda 13 tane tahmin hakkını gösteren toplar,
siyah ve beyaz peg sayılarımız ve bununla beraber çıktıyı elde edeceğimiz yapıları
ekleyerek projeyi oluşturdum. İlk ödevde verdiğiniz proje ile birleştirerek sade bir gui
ile kullanıma sundum.
"""
def generate_secret_code():
    renkler = ['R', 'G', 'B', 'Y', 'C', 'M']
    code = []
    while len(code) < 4:
        color = random.choice(renkler)
        if code.count(color) < 2:
            code.append(color)
    return code

def evaluate_guess(secret_code, guess):
    siyah_pegs = sum(s == g for s, g in zip(secret_code, guess))
    beyaz_pegs = 0
    for color in set(secret_code):
        beyaz_pegs += min(secret_code.count(color), guess.count(color))
    beyaz_pegs -= siyah_pegs
    return siyah_pegs, beyaz_pegs

COLORS = {
    'R': 'red',
    'G': 'green',
    'B': 'blue',
    'Y': 'yellow',
    'C': 'cyan',
    'M': 'magenta'
}

class GameApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Renk Tahmin Oyunu")
        self.secret_code = generate_secret_code()
        self.attempts = 12

        self.canvas = Canvas(window, width=500, height=700)  
        self.canvas.pack()

        self.guess_entry = Entry(window)
        self.guess_entry.pack()

        self.submit_button = Button(window, text="Tahmin Et", command=self.evaluate_guess_UI)
        self.submit_button.pack()

        self.info_label = Label(window, text="Renkler: R=Red, G=Green, B=Blue, Y=Yellow, C=Cyan, M=Magenta. Giriş yaparken R G B Y şeklinde girin.")
        self.info_label.pack()

        self.circles = [[self.create_circle(i, j) for i in range(4)] for j in range(13)]
        self.peg_labels = [self.create_peg_label(j) for j in range(13)]  

    def create_circle(self, col, row):
        x = col * 100 + 50
        y = row * 50 + 50
        return self.canvas.create_oval(x, y, x + 50, y + 50, fill='white')

    def create_peg_label(self, row):
        y = row * 50 + 75  
        return self.canvas.create_text(450, y, text="") 

    def draw_circles(self, color_codes, row):
        for i, color_code in enumerate(color_codes):
            color = COLORS.get(color_code.upper(), 'white')
            self.canvas.itemconfig(self.circles[row][i], fill=color)

    def update_peg_label(self, siyah_pegs, beyaz_pegs, row):
        text = f"B:{beyaz_pegs}, W:{siyah_pegs}"
        self.canvas.itemconfig(self.peg_labels[row], text=text)

    def evaluate_guess_UI(self):
        guess = self.guess_entry.get().upper().split()

        if len(guess) != 4 or not all(color in ['R', 'G', 'B', 'Y', 'C', 'M'] for color in guess):
            messagebox.showerror("Hata", "Geçersiz giriş yaptınız, renkler kümesinden lütfen 4 renk giriş yapın ve aynı renkten max 2 defa girin (R G B Y C M)")
            return

        self.draw_circles(guess, 12 - self.attempts)

        siyah_pegs, beyaz_pegs = evaluate_guess(self.secret_code, guess)
        self.update_peg_label(siyah_pegs, beyaz_pegs, 12 - self.attempts)

        if siyah_pegs == 4:
            messagebox.showinfo("Tebrikler", f"Tebrikler, gizli kodu {13 - self.attempts} denemede çözdünüz.")
        else:
            messagebox.showinfo("Sonuç", f"Sonuç: {siyah_pegs} siyah, {beyaz_pegs} beyaz. Kalan hakkınız: {self.attempts}")

        self.attempts -= 1

        if self.attempts < 0:
            messagebox.showinfo("Game Over", f"Tahmin hakkınız doldu. Gizli kod: {' '.join(self.secret_code)}")

window = tk.Tk()
app = GameApp(window)
window.mainloop()
