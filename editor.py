import tkinter as tk
from tkinter import filedialog


class Editor:
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.root.title("Python Editor Tkinter")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        self.text_area: tk.Text = tk.Text(self.root, wrap="none", font=("Consolas", 8))

        self.text_area.pack(expand=True, fill="both")
        self.text_area.config(tabs=(24,))

        self.menu_bar: tk.Menu = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.curr_file: str = ""

        self.file_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.file_menu)
        self.file_menu.add_command(label="New File", command=self.new_file)
        self.file_menu.add_command(label="Open File", command=self.open_file)
        self.file_menu.add_command(label="Save File", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Run Code", command=self.run_code)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.template_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Templates", menu=self.template_menu)
        self.template_menu.add_command(
            label="PyGame Demo", command=lambda: self.show_template("pygame"))
        self.template_menu.add_command(
            label="Tkinter Demo", command=lambda: self.show_template("tkinter"))
        self.template_menu.add_command(
            label="Matplotlib Demo", command=lambda: self.show_template("matplotlib"))

    def update_title(self) -> None:
        if self.curr_file:
            self.root.title(f"Python Editor Tkinter - {self.curr_file}")
        else:
            self.root.title("Python Editor Tkinter")

    def new_file(self) -> None:
        self.text_area.delete("1.0", "end")
        self.curr_file = ""
        self.update_title()

    def open_file(self) -> None:
        self.curr_file = filedialog.askopenfilename(
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
        )
        if not self.curr_file:
            return
        self.text_area.delete("1.0", "end")
        with open(self.curr_file, "r", encoding="utf-8") as input_file:
            self.text_area.insert("1.0", input_file.read())
        self.update_title()

    def save_file(self) -> None:
        self.curr_file = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
        )
        if not self.curr_file:
            return
        with open(self.curr_file, "w", encoding="utf-8") as output_file:
            output_file.write(self.text_area.get("1.0", "end"))
        self.update_title()

    def run_code(self) -> None:
        if self.curr_file:
            with open(self.curr_file, "r", encoding="utf-8") as input_file:
                exec(input_file.read(), globals={})
        else:
            exec(self.text_area.get("1.0", "end"), globals={})

    code_templates: dict[str, str] = {
        "pygame": """import pygame

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyGame Demo")
clock = pygame.time.Clock()
dt = 0
player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    pygame.draw.circle(screen, "lightgreen", player_pos, 40)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_pos.x += 300 * dt

    # Wrap position
    if player_pos.x < 0:
        player_pos.x = SCREEN_WIDTH
    if player_pos.x > SCREEN_WIDTH:
        player_pos.x = 0
    if player_pos.y < 0:
        player_pos.y = SCREEN_HEIGHT
    if player_pos.y > SCREEN_HEIGHT:
        player_pos.y = 0

    pygame.display.flip()

pygame.quit()""",
        "tkinter": """import tkinter as tk

root = tk.Tk()
root.title("Tkinter Demo")
root.geometry("640x480")

app_font = ("Times New Roman", 16)
label = tk.Label(root, text="Hello, Tkinter!", font=app_font)
label.pack()
button = tk.Button(root, text="Click Me", font=app_font)
button.pack()
button.bind("<Button-1>", lambda _: label.config(text="Button Clicked!"))
root.mainloop()""",
        "matplotlib": """import matplotlib.pyplot as plt
import numpy as np

x_data = np.linspace(-10, 10, 1000)
y_data = np.sin(x_data)

plt.plot(x_data, y_data, color="blue")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.title("Matplotlib Demo")
plt.show()"""
    }

    def show_template(self, tpl_name: str) -> None:
        self.curr_file = ""
        self.text_area.delete("1.0", "end")
        tpl_code: str = Editor.code_templates[tpl_name]
        self.text_area.insert("1.0", tpl_code)
        self.update_title()

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    editor = Editor(root)
    editor.start()
