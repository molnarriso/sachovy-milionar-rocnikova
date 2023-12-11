import tkinter as tk
import random
import time
from tkinter import PhotoImage
from PIL import Image, ImageTk

class RectangleButton(tk.Canvas):
    def __init__(self, master, letter, option_text, game, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.letter = letter
        self.option_text = option_text
        self.game = game
        self.bind("<Button-1>", self.handle_click)

        self.create_rectangle(10, 10, 110, 90, outline="black", fill="white", width=2)
        self.create_text(20, 50, anchor=tk.W, text=letter, font=("Helvetica", 18, "bold"))
        self.create_text(40, 50, anchor=tk.W, text=option_text, font=("Helvetica", 14))

    def handle_click(self, event):
        if not self.game.answered:
            self.game.answer_question(self.letter)

class ChessMilionaireGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Šachový milionár")
        self.root.geometry("1200x800")

        self.questions = [
            {"question": "Ktorý veľmajster sa nachádza na obrázku?", "image": "kasparov.jpg", "options": ["Garry Kasparov", "Magnus Carlsen", "Viswanathan Anand", "Bobby Fischer"], "correct_option": "Garry Kasparov"},
            # Ďalšie otázky ...
        ]

        self.current_question = 0
        self.score = 0
        self.timer_start = 0
        self.answered = False
        self.letters = ["A", "B", "C", "D"]
        self.create_widgets()

    def create_widgets(self):
        self.intro_label = tk.Label(self.root, text="Vitaj na šachovom milionárovi!", font=("Helvetica", 24))
        self.intro_label.pack()

        self.start_button = tk.Button(self.root, text="ZAČAŤ", command=self.start_game, font=("Helvetica", 18))
        self.start_button.pack()

        self.img_label = tk.Label(self.root)
        self.img_label.pack()

        self.question_label = tk.Label(self.root, text="", font=("Helvetica", 18))
        self.question_label.pack()

        self.option_frame = tk.Frame(self.root)
        self.option_frame.pack()

        self.option_buttons = []
        for i in range(4):
            rect_button = RectangleButton(self.option_frame, letter=self.letters[i], option_text="", game=self, width=120, height=100, bg="white", bd=0, highlightthickness=0, relief="flat")
            rect_button.grid(row=i // 2, column=i % 2, pady=10, padx=10, sticky="w")
            self.option_buttons.append(rect_button)

        self.timer_label = tk.Label(self.root, text="", font=("Helvetica", 18))
        self.timer_label.pack()

        self.hint_button = tk.Button(self.root, text="?", command=self.use_hint, font=("Helvetica", 16))
        self.hint_button.pack(side=tk.LEFT, padx=10)

        self.fifty_fifty_button = tk.Button(self.root, text="50/50", command=self.use_fifty_fifty, font=("Helvetica", 16))
        self.fifty_fifty_button.pack(side=tk.LEFT, padx=10)

        self.next_question_button = tk.Button(self.root, text="Ďalej", command=self.load_question, font=("Helvetica", 16))
        self.next_question_button.pack(side=tk.TOP, pady=10)

    def start_game(self):
        self.intro_label.pack_forget()
        self.start_button.pack_forget()
        self.load_question()

    def load_question(self):
        if self.current_question < len(self.questions):
            self.answered = False
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data["question"], wraplength=800)

            image_path = question_data["image"]
            pil_image = Image.open(image_path)
            pil_image = pil_image.resize((pil_image.width // 2, pil_image.height // 2))
            tk_image = ImageTk.PhotoImage(pil_image)

            self.img_label.config(image=tk_image)
            self.img_label.image = tk_image

            options = question_data["options"]
            random.shuffle(options)

            for i in range(4):
                self.option_buttons[i].delete("all")
                self.option_buttons[i].create_rectangle(10, 10, 110, 90, outline="black", fill="white", width=2)
                self.option_buttons[i].create_text(20, 50, anchor=tk.W, text=self.letters[i], font=("Helvetica", 18, "bold"))
                self.option_buttons[i].create_text(40, 50, anchor=tk.W, text=options[i], font=("Helvetica", 14))
                self.option_buttons[i].letter = self.letters[i]  # Priradíme prvé písmeno možnosti k tlačidlu

            self.next_question_button.pack_forget()
            self.timer_start = time.time()
            self.update_timer()
        else:
            self.show_final_score()

    def answer_question(self, selected_option):
        if not self.answered:
            self.answered = True
            question_data = self.questions[self.current_question]

            correct_option_index = question_data["options"].index(question_data["correct_option"])
            if selected_option == question_data["correct_option"][0]:
                self.option_buttons[correct_option_index].itemconfig(1, fill="green")
                self.score += 1
            else:
                selected_option_index = question_data["options"].index(selected_option)
                self.option_buttons[selected_option_index].itemconfig(1, fill="red")
                self.option_buttons[correct_option_index].itemconfig(1, fill="green")

            elapsed_time = int(time.time() - self.timer_start)
            self.timer_label.config(text=f"Čas: {elapsed_time} s")
            self.current_question += 1
            self.next_question_button.pack(side=tk.TOP, pady=10)

    def update_timer(self):
        elapsed_time = int(time.time() - self.timer_start)
        self.timer_label.config(text=f"Čas: {elapsed_time} s")
        if not self.answered:
            self.root.after(1000, self.update_timer)

    def use_hint(self):
        question_data = self.questions[self.current_question]
        correct_option_index = question_data["options"].index(question_data["correct_option"])
        self.option_buttons[correct_option_index].itemconfig(1, fill="green")

        self.hint_button.config(state=tk.DISABLED)

    def use_fifty_fifty(self):
        if not self.answered:
            question_data = self.questions[self.current_question]

            if len(question_data["options"]) > 2:
                options_to_remove = random.sample(range(4), 2)
                for i in options_to_remove:
                    if question_data["options"][i] != question_data["correct_option"]:
                        self.option_buttons[i].delete("all")

            self.fifty_fifty_button.config(state=tk.DISABLED)

    def show_final_score(self):
        self.question_label.config(text=f"Gratulujem! Dosiahol si skóre {self.score} bodov.")
        self.timer_label.config(text="Hra skončila")
        for button in self.option_buttons:
            button.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = ChessMilionaireGame()
    game.run()
