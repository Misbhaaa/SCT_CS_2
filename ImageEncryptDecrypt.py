from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from PIL import Image
import os
import platform
import subprocess

class ImageEncryptor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryptor/Decryptor")
        self.root.geometry("400x250")
        self.root.resizable(False, False)  
        self.selected_file = None

        Label(root, text="Select an Image File:", font=("Arial", 12)).pack(pady=10)
        self.file_label = Label(root, text="No file selected", fg="grey", font=("Arial", 10))
        self.file_label.pack()

        Button(root, text="Browse", command=self.choose_file, width=15).pack(pady=5)

        Label(root, text="Enter Key (0-255):", font=("Arial", 12)).pack(pady=10)
        self.key_entry = Entry(root, font=("Arial", 10))
        self.key_entry.pack()

        Button(root, text="Encrypt", command=self.encrypt_action, width=20, bg="green", fg="white", font=("Arial", 10)).pack(pady=10)
        Button(root, text="Decrypt", command=self.decrypt_action, width=20, bg="blue", fg="white", font=("Arial", 10)).pack()

    def choose_file(self):
        self.selected_file = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if self.selected_file:
            self.file_label.config(text=os.path.basename(self.selected_file))

    def open_file(self, file_path):
        """Open the file with the default image viewer based on the operating system."""
        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            else:
                messagebox.showwarning("Warning", "Automatic file opening not supported on this OS.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {str(e)}")

    def encrypt_decrypt_image(self, file_path, key, mode):
        try:
            img = Image.open(file_path).convert("RGB")
            pixels = img.load()

            for x in range(img.width):
                for y in range(img.height):
                    r, g, b = pixels[x, y]
                    pixels[x, y] = (r ^ key, g ^ key, b ^ key)

            base, ext = os.path.splitext(file_path)
            if mode == "encrypt":
                out_path = f"{base}_encrypted{ext}"
            else:
                if base.endswith("_encrypted"):
                    base = base[:-10]  
                out_path = f"{base}_decrypted{ext}"

            if os.path.exists(out_path):
                if not messagebox.askyesno("Overwrite?", f"{out_path} already exists. Overwrite?"):
                    return

            img.save(out_path)
            messagebox.showinfo("Success", f"{mode.title()}ed image saved as:\n{out_path}")
            
            self.open_file(out_path)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to {mode} image: {str(e)}")

    def encrypt_action(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select an image.")
            return
        try:
            key = int(self.key_entry.get())
            if not 0 <= key <= 255:
                messagebox.showerror("Error", "Key must be an integer between 0 and 255.")
                return
            self.encrypt_decrypt_image(self.selected_file, key, "encrypt")
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")

    def decrypt_action(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select an image.")
            return
        try:
            key = int(self.key_entry.get())
            if not 0 <= key <= 255:
                messagebox.showerror("Error", "Key must be an integer between 0 and 255.")
                return
            self.encrypt_decrypt_image(self.selected_file, key, "decrypt")
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")


if __name__ == "__main__":
    root = Tk()
    root.attributes("-topmost", True)
    app = ImageEncryptor(root)
    root.mainloop()
