#!/usr/bin/env python3
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    from PIL import Image
except ImportError:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Pillow is required",
        "Pillow needs to be installed..\n\n"
        "To install Pillow correctly open your CMD and type:\npython -m pip install Pillow"
    )
    raise SystemExit(1)

TARGET = 1080
SCALED = 1072  
BORDER = (TARGET - SCALED) // 2  

def main():
    root = tk.Tk()
    root.withdraw()
    root.update()

    source = filedialog.askdirectory(title="Please select your folder with your PNG's")
    if not source:
        root.destroy()
        return

    source_path = Path(source)
    png_files = sorted(
        p for p in source_path.iterdir()
        if p.is_file() and p.suffix.lower() == ".png"
    )

    if not png_files:
        messagebox.showinfo("No PNG's were found.", "In this folder are no PNG's which can be converted.")
        root.destroy()
        return

    destination = filedialog.askdirectory(title="Please select the folder where your converted PNG's [1080x1080] should be stored.")
    if not destination:
        root.destroy()
        return

    destination_path = Path(destination)
    success = 0
    errors = []

    for path in png_files:
        try:
            with Image.open(path) as original:
                image = original.convert("RGBA")
                
                if image.size == (16, 16):
                    resized = image.resize((SCALED, SCALED), Image.Resampling.NEAREST)
                else:
                    w, h = image.size
                    scale = min(SCALED / w, SCALED / h)
                    new_size = (max(1, round(w * scale)), max(1, round(h * scale)))
                    resized = image.resize(new_size, Image.Resampling.NEAREST)

                canvas = Image.new("RGBA", (TARGET, TARGET), (0, 0, 0, 0))
                x = (TARGET - resized.width) // 2
                y = (TARGET - resized.height) // 2
                canvas.paste(resized, (x, y))
                canvas.save(destination_path / path.name, format="PNG")
                success += 1
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")

    summary = f"We're Done!'!\n\nConverted: {success} of {len(png_files)}\nDestination:\n{destination_path}"
    if errors:
        summary += "\n\nError:\n" + "\n".join(errors[:10])
        if len(errors) > 10:
            summary += f"\n… and {len(errors) - 10} more."
    messagebox.showinfo("Your PNG's were successfully converted!", summary)
    root.destroy()

if __name__ == "__main__":
    main()
