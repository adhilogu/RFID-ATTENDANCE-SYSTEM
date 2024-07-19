import sqlite3
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from PIL import Image, ImageTk
import io


# Function to fetch and display the selected image
def display_image(event):
    selected_index = listbox.curselection()
    if not selected_index:
        return

    image_id = listbox.get(selected_index[0])

    try:
        # Fetch the image from the database
        conn = sqlite3.connect('photos.db')
        c = conn.cursor()
        c.execute("SELECT image FROM photos WHERE id=?", (image_id,))
        image_data = c.fetchone()[0]
        conn.close()

        # Convert the image data back to an image
        img_byte_arr = io.BytesIO(image_data)
        img = Image.open(img_byte_arr)

        # Display the image in the Tkinter window
        img_tk = ImageTk.PhotoImage(img)
        panel.img_tk = img_tk  # Keep a reference to avoid garbage collection
        panel.config(image=img_tk)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to retrieve image from database: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display image: {e}")


# Function to populate the listbox with image IDs
def load_image_ids():
    try:
        # Fetch all image IDs from the database
        conn = sqlite3.connect('photos.db')
        c = conn.cursor()
        c.execute("SELECT id FROM photos")
        image_ids = c.fetchall()
        conn.close()

        # Populate the listbox with image IDs
        listbox.delete(0, tk.END)
        for image_id in image_ids:
            listbox.insert(tk.END, image_id[0])
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to load image IDs: {e}")


# Set up the Tkinter window
root = tk.Tk()
root.title("View Saved Photos")

# Create a listbox to display image IDs
listbox = Listbox(root)
listbox.pack(side=tk.LEFT, fill=tk.Y)

# Add a scrollbar to the listbox
scrollbar = Scrollbar(root, orient="vertical")
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

# Bind the listbox selection event to the display function
listbox.bind('<<ListboxSelect>>', display_image)

# Create a panel to display the image
panel = tk.Label(root)
panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Load image IDs into the listbox
load_image_ids()
root.mainloop()
