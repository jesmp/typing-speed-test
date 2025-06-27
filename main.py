# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from data import get_sentence
import time
import random

class TypingTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")

        self.difficulty = tk.StringVar(value="easy")
        self.sentence = ""
        self.start_time = None
        self.end_time = None
        self.time_limit = 60
        self.correct_chars = 0
        self.total_chars = 0
        self.running = False

        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        # Difficulty selection
        difficulty_frame = ttk.Frame(frame)
        difficulty_frame.pack()
        ttk.Label(difficulty_frame, text="Select Difficulty:").pack(side="left")
        for level in ["easy", "medium", "hard"]:
            ttk.Radiobutton(difficulty_frame, text=level.title(), variable=self.difficulty, value=level).pack(side="left")

        # Sentence display
        self.sentence_display = tk.Text(frame, height=3, wrap="word", font=("Courier", 14), bg="#f0f0f0")
        self.sentence_display.pack(fill="x", pady=10)
        self.sentence_display.config(state="disabled")

        # Typing input
        self.text_input = tk.Text(frame, height=3, wrap="word", font=("Courier", 14))
        self.text_input.pack(fill="x")
        self.text_input.bind("<KeyRelease>", self.on_key_release)

        # Stats
        self.stats_label = ttk.Label(frame, text="WPM: 0 | Accuracy: 0% | Time: 60s")
        self.stats_label.pack(pady=10)

        # Start button
        ttk.Button(frame, text="Start Test", command=self.start_test).pack()

    def start_test(self):
        self.running = True
        self.start_time = time.time()
        self.end_time = self.start_time + self.time_limit
        self.correct_chars = 0
        self.total_chars = 0
        self.text_input.config(state="normal")
        self.text_input.delete("1.0", "end")
        self.new_sentence()
        self.update_timer()

    def update_timer(self):
        if not self.running:
            return
        remaining = int(self.end_time - time.time())
        if remaining <= 0:
            self.running = False
            self.text_input.config(state="disabled")
            self.show_results()
        else:
            self.stats_label.config(text=f"WPM: {self.get_wpm()} | Accuracy: {self.get_accuracy()}% | Time: {remaining}s")
            self.root.after(1000, self.update_timer)

    def on_key_release(self, event):
        if not self.running:
            return
        typed = self.text_input.get("1.0", "end-1c")
        target = self.sentence

        self.total_chars += 1 if event.char and event.keysym != 'BackSpace' else 0
        self.correct_chars += 1 if len(typed) <= len(target) and typed[-1:] == target[len(typed)-1:len(typed)] else 0 if event.char and event.keysym != 'BackSpace' else 0

        # Apply color tags
        self.text_input.tag_remove("correct", "1.0", "end")
        self.text_input.tag_remove("incorrect", "1.0", "end")
        for i in range(len(typed)):
            tag = "correct" if i < len(target) and typed[i] == target[i] else "incorrect"
            self.text_input.tag_add(tag, f"1.{i}", f"1.{i+1}")

        self.text_input.tag_config("correct", foreground="green")
        self.text_input.tag_config("incorrect", foreground="red")

        if typed.strip() == target:
            self.text_input.delete("1.0", "end")
            self.new_sentence()

    def new_sentence(self):
        self.sentence = get_sentence(self.difficulty.get())
        self.sentence_display.config(state="normal")
        self.sentence_display.delete("1.0", "end")
        self.sentence_display.insert("1.0", self.sentence)
        self.sentence_display.config(state="disabled")

    def get_wpm(self):
        elapsed = max(self.time_limit, 1)
        return int((self.correct_chars / 5) / (elapsed / 60))

    def get_accuracy(self):
        return round((self.correct_chars / self.total_chars) * 100, 2) if self.total_chars else 0

    def show_results(self):
        wpm = self.get_wpm()
        accuracy = self.get_accuracy()
        messagebox.showinfo("Test Complete", f"Your results:\n\nWPM: {wpm}\nAccuracy: {accuracy}%")
        self.stats_label.config(text=f"WPM: {wpm} | Accuracy: {accuracy}% | Time: 0s")

if __name__ == '__main__':
    root = tk.Tk()
    app = TypingTest(root)
    root.mainloop()
