import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import pyttsx3

class PDFReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Reader")
        self.root.geometry("600x400")

        self.pdf_text = ""
        self.pdf_file = None

        # Віджет для тексту
        self.text_area = tk.Text(self.root, wrap='word', width=70, height=20)
        self.text_area.pack(pady=20)

        # Кнопки
        self.load_button = tk.Button(self.root, text="Завантажити PDF", command=self.load_pdf)
        self.load_button.pack(pady=5)

        self.paragraph_button = tk.Button(self.root, text="Показати параграфи", command=self.show_paragraphs)
        self.paragraph_button.pack(pady=5)

        self.speak_button = tk.Button(self.root, text="Озвучити текст", command=self.speak_text)
        self.speak_button.pack(pady=5)

        self.book_list_label = tk.Label(self.root, text="Список завантажених книг:")
        self.book_list_label.pack(pady=10)

        self.book_list = tk.Listbox(self.root, width=70, height=5)
        self.book_list.pack(pady=10)

        # Ініціалізація для озвучування
        self.speaker = pyttsx3.init()

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    self.pdf_text = ""
                    for page in reader.pages:
                        self.pdf_text += page.extract_text()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, self.pdf_text)

                self.pdf_file = file_path
                self.book_list.insert(tk.END, file_path.split("/")[-1])
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося завантажити PDF: {e}")

    def show_paragraphs(self):
        if not self.pdf_text:
            messagebox.showwarning("Попередження", "Будь ласка, спочатку завантажте PDF.")
            return

        paragraphs = self.pdf_text.split("\n\n")  # Припускаємо, що параграфи відокремлені двома новими рядками
        self.paragraph_window = tk.Toplevel(self.root)
        self.paragraph_window.title("Параграфи")

        self.paragraph_listbox = tk.Listbox(self.paragraph_window, width=50, height=10)
        for paragraph in paragraphs:
            self.paragraph_listbox.insert(tk.END, paragraph[:50] + "...")
        self.paragraph_listbox.pack(pady=10)

    def speak_text(self):
        # Отримуємо виділений текст в основному текстовому віджеті
        try:
            selected_paragraph = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            selected_paragraph = ""  # Якщо нічого не виділено

        # Якщо текст виділений, озвучуємо його
        if selected_paragraph.strip():
            self.speaker.say(selected_paragraph)
            self.speaker.runAndWait()
        else:
            # Якщо текст не виділений, озвучуємо весь документ
            if self.pdf_text.strip():
                self.speaker.say(self.pdf_text)
                self.speaker.runAndWait()
            else:
                messagebox.showwarning("Попередження", "Немає тексту для озвучення.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFReaderApp(root)
    root.mainloop()
