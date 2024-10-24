import tkinter as tk
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
root.configure(bg="#f0f0f0")  # Set background color

# File entry box
file_label = tk.Label(root, text="Enter file path:", bg="#f0f0f0")
file_label.grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, width=50, bg="light blue", relief="groove")
file_entry.grid(row=0, column=1, padx=10, pady=10)

# Page numbers entry box
page_label = tk.Label(root, text="Enter page numbers (comma-separated, or 'all'):", bg="#f0f0f0")
page_label.grid(row=1, column=0, padx=10, pady=10)
page_entry = tk.Entry(root, width=50, bg="white", relief="groove")
page_entry.grid(row=1, column=1, padx=10, pady=10)

# Generate summary button
generate_button = tk.Button(root, text="Generate Summary", command=generate_summary, bg="#4caf50", fg="white", padx=10, pady=5)
generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Summary text box
summary_text = tk.Text(root, width=80, height=20, bg="white", relief="groove")
summary_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Apply styles
root.configure(bg="#f0f0f0")  # Set background color
file_entry.configure(bg="white", relief="groove")
page_entry.configure(bg="white", relief="groove")
generate_button.configure(bg="#4caf50", fg="white", padx=10, pady=5)
summary_text.configure(bg="white", relief="groove")

# Add shadows
root.after(1000, lambda: root.configure(highlightthickness=1, highlightcolor="black"))  # Add a slight shadow around the window

root.mainloop()