import os
from tkinter import Tk, Button, filedialog, Label, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.root.geometry("300x150")
        
        self.label = Label(root, text="Select images to convert to PDF")
        self.label.pack(pady=10)

        self.select_button = Button(root, text="Select Images", command=self.select_images)
        self.select_button.pack(pady=5)

        self.convert_button = Button(root, text="Convert to PDF", command=self.convert_to_pdf, state='disabled')
        self.convert_button.pack(pady=5)

        self.images = []

    def select_images(self):
        filetypes = [("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        self.images = filedialog.askopenfilenames(title="Select Images", filetypes=filetypes)
        if self.images:
            self.convert_button.config(state='normal')
            messagebox.showinfo("Images Selected", f"{len(self.images)} images selected.")
        else:
            messagebox.showwarning("No Selection", "No images were selected.")

    def convert_to_pdf(self):
        if not self.images:
            messagebox.showerror("Error", "No images selected.")
            return
        
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                   filetypes=[("PDF files", "*.pdf")],
                                                   title="Save PDF as")
        if not output_path:
            return

        try:
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter

            for img_path in self.images:
                img = Image.open(img_path)
                img_width, img_height = img.size

                # Resize image to fit within the page size
                aspect = img_height / img_width
                max_width = width - 100
                max_height = height - 100

                if img_width > max_width:
                    img_width = max_width
                    img_height = aspect * img_width

                if img_height > max_height:
                    img_height = max_height
                    img_width = img_height / aspect

                x = (width - img_width) / 2
                y = (height - img_height) / 2

                img_temp = img.convert("RGB")
                temp_path = "temp_image.jpg"
                img_temp.save(temp_path)

                c.drawImage(temp_path, x, y, img_width, img_height)
                c.showPage()

            c.save()
            os.remove(temp_path)
            messagebox.showinfo("Success", f"PDF saved at:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Conversion Failed", str(e))

# Run the GUI
if __name__ == "__main__":
    root = Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()
