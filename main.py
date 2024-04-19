import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

class ImageThresholdApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Thresholding with Live Preview")

        # Load image
        self.img_path = filedialog.askopenfilename()
        if not self.img_path:
            raise ValueError("No file selected")

        self.img = Image.open(self.img_path).convert("L")
        self.data = np.array(self.img)
        self.data = np.stack([self.data] * 3 + [np.ones(self.data.shape, dtype=self.data.dtype) * 255], axis=-1)
         # Slider for threshold
        self.threshold = tk.Scale(master, from_=0, to=255, orient='horizontal', label="Blackness Threshold")
        # Display the image
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.data.astype(np.uint8)))
        self.canvas = tk.Canvas(master, width=self.photo.width(), height=self.photo.height())
         # Wait until the window is mapped to the screen (visible)
        master.update_idletasks() 
        width = master.winfo_width()
        scale_length = int(width * 0.9)  # Calculate 90% of the window width
        self.threshold.config(length=scale_length)  # Set the new length
        self.threshold.pack(fill='x', padx=20)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.threshold.set(128)
        self.threshold.bind("<Motion>", self.update_image)

        # Button to save the modified image
        save_button = tk.Button(master, text="Save Image", command=self.save_image)
        save_button.pack()

    def update_image(self, event):
        threshold = self.threshold.get()
        mask = (self.data[:, :, 0] > threshold)
        processed_data = self.data.copy()
        processed_data[:, :, :3][mask] = [255, 255, 255]  # White
        processed_data[:, :, :3][~mask] = [0, 0, 0]       # Black

        # Update the photo
        new_photo = ImageTk.PhotoImage(image=Image.fromarray(processed_data.astype(np.uint8)))
        self.canvas.itemconfig(self.canvas.find_all()[0], image=new_photo)
        self.photo = new_photo  # Avoid garbage collection

    # new_img_path = ''
    def save_image(self):
        # Open a save file dialog to select the name and location to save the image
        new_img_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            title="Save Image As"
        )
        # Check if a file name was entered
        if new_img_path:
            # Save the current state of the processed image
            processed_image = Image.fromarray(self.data.astype(np.uint8))
            processed_image.save(new_img_path)
            print("Image saved as", new_img_path)
        else:
            print("Save image cancelled.")
    

    

# Create the main window and pass it to the ImageThresholdApp
root = tk.Tk()
app = ImageThresholdApp(root)
root.mainloop()
