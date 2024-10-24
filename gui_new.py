import tkinter as tk
from tkinter import ttk
from langchain_ollama import OllamaLLM
import PyPDF2
import os

def read_pdf_file(file_path, page_numbers):
    try:
        # Open the PDF file in read-binary mode
        with open(file_path, 'rb') as file:
            # Create a PyPDF2 reader object
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            if page_numbers == "all":
                page_numbers = list(range(num_pages))
            else:
                try:
                    page_numbers = [int(page_number) for page_number in page_numbers.split(',')]
                    page_numbers = [page_number - 1 for page_number in page_numbers]  # Adjust for zero-based indexing
                except ValueError:
                    print("Invalid page numbers. Please enter valid integers separated by commas.")
                    return None

            # Initialize an empty string to store the PDF contents
            pdf_contents = ''

            # Iterate over each page in the PDF
            for page_number in page_numbers:
                if 0 <= page_number < num_pages:
                    pdf_contents += pdf_reader.pages[page_number].extract_text()
                else:
                    print(f"Page {page_number + 1} is out of range.")

            # Return the PDF contents as a string
            return pdf_contents

    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

def summarize_pdf(file_path, page_numbers):
    pdf_contents = read_pdf_file(file_path, page_numbers)
    if pdf_contents:
        model = OllamaLLM(model="llama3.2")
        results = model.invoke(pdf_contents + "Summarize the data in a understandable manner, while giving atleast 500 words of the page content without ommitting keywords or formulas or definitions")
        return results
    else:
        return "Failed to read PDF file."

def generate_summary():
    file_path = file_entry.get()
    page_numbers = page_entry.get()
    summary = summarize_pdf(file_path, page_numbers)
    summary_text.delete(1.0, tk.END)
    summary_text.insert(tk.END, summary)

# Create the GUI
root = tk.Tk()
root.title("PDF Summarizer")
root.geometry("700x600")  # Set a fixed window size

# Use a modern theme
style = ttk.Style()
style.theme_use("alt")  # Use a modern theme

# Define a custom style for our widgets
style.configure("TFrame", background="#2e2e2e")
style.configure("TLabel", background="#2e2e2e", foreground="#ffffff", font=("Helvetica", 12))
style.configure("TEntry", fieldbackground="#3e3e3e", foreground="#ffffff", font=("Helvetica", 10))
style.configure("TButton", foreground="#ffffff", background="#4caf50", font=("Helvetica", 10, "bold"))

# Create a ttk.Frame as the main container
main_frame = ttk.Frame(root, padding="20 20 20 20")
main_frame.pack(fill="both", expand=True)

# Create rounded widgets
file_label = ttk.Label(main_frame, text="Enter file path:")
file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

file_entry = ttk.Entry(main_frame, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=10)

page_label = ttk.Label(main_frame, text="Enter page numbers (comma-separated, or 'all'):")
page_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

page_entry = ttk.Entry(main_frame, width=50)
page_entry.grid(row=1, column=1, padx=10, pady=10)

generate_button = ttk.Button(main_frame, text="Generate Summary", command=generate_summary)
generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

summary_text = tk.Text(main_frame, width=80, height=20, bg="#1e1e1e", fg="#ffffff", font=("Helvetica", 10), wrap="word")
summary_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()