import tkinter as tk
from tkinter import font
import ast
import os
from tkinter import messagebox
import webbrowser
try:
	import winreg
except ImportError:
	winreg = None

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "theme_settings.txt")
Version = "v"+"1.5"+"-"+"release"
root = tk.Tk()
# Themes
root.configure(bg="#f0f0f0")
dark_mode = False

theme_choice = tk.StringVar(value="light")


def load_saved_theme():
	if not os.path.exists(CONFIG_PATH):
		return "light"
	try:
		with open(CONFIG_PATH, "r", encoding="utf-8") as f:
			stored = f.read().strip().lower()
		if stored in {"light", "dark", "system"}:
			return stored
	except OSError:
		pass
	return "light"


def save_theme(theme_name):
	try:
		with open(CONFIG_PATH, "w", encoding="utf-8") as f:
			f.write(theme_name)
	except OSError:
		pass


def is_system_dark_mode():
	if winreg is None:
		return False
	try:
		with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
			try:
				value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
				return value == 0
			except FileNotFoundError:
				return False
	except OSError:
		return False


def set_theme(theme_name):
	global dark_mode
	if theme_name == "system":
		resolved_theme = "dark" if is_system_dark_mode() else "light"
		selected_theme = "system"
	else:
		resolved_theme = theme_name
		selected_theme = theme_name
	dark_mode = resolved_theme == "dark"
	save_theme(selected_theme)
	theme = {
		"light": {
			"bg": "#f0f0f0",
			"fg": "#111111",
			"output_bg": "lightgray",
			"output_fg": "black",
			"button_bg": "#f2f2f2",
			"button_fg": "#111111",
			"special_bg": "#e8e8e8",
			"special_fg": "#111111",
			"equal_bg": "#add8e6",
			"equal_fg": "#111111",
			"clear_bg": "#ff0000",
			"clear_fg": "black",
		},
		"dark": {
			"bg": "#1f1f1f",
			"fg": "#f5f5f5",
			"output_bg": "#2b2b2b",
			"output_fg": "#f5f5f5",
			"button_bg": "#333333",
			"button_fg": "#f5f5f5",
			"special_bg": "#444444",
			"special_fg": "#f5f5f5",
			"equal_bg": "#3b82f6",
			"equal_fg": "#ffffff",
			"clear_bg": "#ff0000",
			"clear_fg": "#000000",
		},
	}[resolved_theme]

	root.configure(bg=theme["bg"])
	output_box.configure(bg=theme["output_bg"], fg=theme["output_fg"])
	for button in regular_buttons:
		button.configure(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["button_bg"])
	Clear_button.configure(bg=theme["clear_bg"], fg=theme["clear_fg"], activebackground=theme["clear_bg"])
	Delete_button.configure(bg=theme["clear_bg"], fg=theme["clear_fg"], activebackground=theme["clear_bg"])
	Equal_btn.configure(bg=theme["equal_bg"], fg=theme["equal_fg"], activebackground=theme["equal_bg"])
	menu_bar.configure(bg=theme["bg"], fg=theme["fg"])
	file_menu.configure(bg=theme["bg"], fg=theme["fg"])
	for child in file_menu.winfo_children():
		if hasattr(child, "configure"):
			child.configure(bg=theme["bg"], fg=theme["fg"])

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
def open_url(url):
    """Opens the specified URL in the default web browser."""
    webbrowser.open_new_tab(url)

def show_custom_messagebox():
    # Create a top-level window
    msg_box = tk.Toplevel()
    msg_box.title("More Projects")
    msg_box.geometry("300x120")
    msg_box.resizable(False, False)
    
    # Make it modal (force focus)
    msg_box.grab_set()
    
    # Regular text description
    label_text = tk.Label(msg_box, text="For more Projects, please visit these sites", padx=10, pady=10)
    label_text.pack()
    
    # Clickable hyperlink label
    url = "https://tuffgit21.github.io/#work"
    link_label = tk.Label(msg_box, text="Click Here for projects", fg="blue", cursor="hand2")
    link_label.pack(pady=5)
    
    # Bind mouse click and hover effects to the link
    link_label.bind("<Button-1>", lambda e: open_url(url))
    link_label.bind("<Enter>", lambda e: link_label.config(font=("TkDefaultFont", 9, "underline")))
    link_label.bind("<Leave>", lambda e: link_label.config(font=("TkDefaultFont", 9, "normal")))

    # Close button
    close_button = tk.Button(msg_box, text="OK", width=10, command=msg_box.destroy)
    close_button.pack(pady=10)
def About():
	messagebox.showinfo("About",f"Calculator {Version}\nHere is a lightweight and Open-source Calculator made by tuffgit21, made specifically for systems without Calculator.")
theme_menu = tk.Menu(file_menu, tearoff=0)
theme_menu.add_radiobutton(label="Light", value="light", variable=theme_choice, command=lambda: set_theme("light"))
theme_menu.add_radiobutton(label="Dark", value="dark", variable=theme_choice, command=lambda: set_theme("dark"))
theme_menu.add_radiobutton(label="System Default", value="system", variable=theme_choice, command=lambda: set_theme("system"))
file_menu.add_cascade(label="Theme", menu=theme_menu)
file_menu.add_separator()
file_menu.add_command(label="About", command=About)
file_menu.add_command(label="More Projects", command=show_custom_messagebox)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="View", menu=file_menu)
root.config(menu=menu_bar)
icon_path = os.path.join(os.path.dirname(__file__), "calculator.png")
icon = tk.PhotoImage(file=icon_path)
root.iconphoto(True, icon)
root.title(f"Calculator {Version}")
root.geometry("300x350")
root.resizable(False, False)
output_font = font.Font(family="Courier New", size=16, weight="normal")
output_box = tk.Text(root, height=3, width=31, state="disabled", wrap="word", bg="lightgray", fg="black", font=output_font)
regular_buttons = []

# Configure grid for a calculator-like layout
for c in range(4):
	root.columnconfigure(c, weight=1, uniform="col")
root.rowconfigure(0, weight=0)
for r in range(1, 6):
	root.rowconfigure(r, weight=1)

output_box.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=8, pady=8)

def _get_expr():
	output_box.config(state="normal")
	expr = output_box.get("1.0", "end-1c")
	output_box.config(state="disabled")
	return expr

def _set_expr(text):
	output_box.config(state="normal")
	output_box.delete("1.0", "end")
	output_box.insert("end", text)
	output_box.config(state="disabled")

def append_char(ch):
	s = _get_expr()
	_set_expr(s + str(ch))

def Clear():
	_set_expr("")

def Delete():
	s = _get_expr()
	# If an error is shown, prevent deletion until cleared
	if s == "Math Error":
		return
	_set_expr(s[:-1])

def _safe_eval(expr):
	# Evaluate a math expression using AST, allow only basic arithmetic
	node = ast.parse(expr, mode="eval").body

	def _eval(n):
		if isinstance(n, ast.BinOp):
			left = _eval(n.left)
			right = _eval(n.right)
			if isinstance(n.op, ast.Add):
				return left + right
			if isinstance(n.op, ast.Sub):
				return left - right
			if isinstance(n.op, ast.Mult):
				return left * right
			if isinstance(n.op, ast.Div):
				return left / right
			if isinstance(n.op, ast.Mod):
				return left % right
			if isinstance(n.op, ast.Pow):
				return left ** right
			raise ValueError("unsupported operator")
		if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
			return -_eval(n.operand)
		if isinstance(n, ast.Constant):
			if isinstance(n.value, (int, float)):
				return n.value
			raise ValueError("unsupported constant")
		if isinstance(n, ast.Num):
			return n.n
		raise ValueError("unsupported expression")

	return _eval(node)

def Equal():
	expr = _get_expr().strip()
	if not expr:
		return
	try:
		result = _safe_eval(expr)
		if isinstance(result, float) and result.is_integer():
			result = int(result)
		_set_expr(str(result))
	except Exception:
		_set_expr("Math Error")

def toggle_parentheses():
	s = _get_expr()
	# if there are more '(' than ')', close one, otherwise open
	if s.count('(') > s.count(')'):
		append_char(')')
	else:
		append_char('(')

def on_key_press(event):
	key = event.char
	keysym = event.keysym
	
	# Number keys
	if key in '0123456789':
		append_char(key)
	# Operators
	elif key in '+-*/%':
		append_char(key)
	# Decimal point
	elif key == '.':
		append_char(key)
	# Parentheses
	elif key == '(':
		append_char('(')
	elif key == ')':
		append_char(')')
	# Equals / Enter
	elif keysym in ('Return', 'equal'):
		Equal()
	# Delete / Backspace
	elif keysym == 'BackSpace':
		Delete()
	# Clear
	elif key.lower() == 'c':
		Clear()

# Reuse existing buttons but place them on the root grid to form a keypad layout
button_font = font.Font(family="Ubuntu",size=16,weight="bold")
Delete_font = font.Font(family="Ubuntu",size=11,weight="bold")
Clear_button = tk.Button(root, text=" C ", command=Clear, bg="red", fg="black",font=button_font)
Clear_button.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=4, pady=4)
Delete_button = tk.Button(root, text=" ⌫ ", command=Delete, bg="red", fg="black",font=Delete_font)
Delete_button.grid(row=1, column=1, columnspan=1, sticky="nsew", padx=4, pady=4)
Modulo_btn = tk.Button(root, text=" % ", command=lambda: append_char('%'),font=button_font)
Modulo_btn.grid(row=1, column=2, columnspan=1, sticky="nsew", padx=4, pady=4)
Divise_btn = tk.Button(root, text=" / ", command=lambda: append_char('/'),font=button_font)
Divise_btn.grid(row=1, column=3, columnspan=1, sticky="nsew", padx=4, pady=4)
Number7_btn = tk.Button(root, text=" 7 ", command=lambda: append_char('7'),font=button_font)
Number7_btn.grid(row=2, column=0, columnspan=1, sticky="nsew", padx=4, pady=4)
Number8_btn = tk.Button(root, text=" 8 ", command=lambda: append_char('8'),font=button_font)
Number8_btn.grid(row=2, column=1, columnspan=1, sticky="nsew", padx=4, pady=4)
Number9_btn = tk.Button(root, text=" 9 ", command=lambda: append_char('9'),font=button_font)
Number9_btn.grid(row=2, column=2, columnspan=1, sticky="nsew", padx=4, pady=4)
Multiply_btn = tk.Button(root, text=" * ", command=lambda: append_char('*'),font=button_font)
Multiply_btn.grid(row=2, column=3, columnspan=1, sticky="nsew", padx=4, pady=4)
Number4_btn = tk.Button(root, text=" 4 ", command=lambda: append_char('4'),font=button_font)
Number4_btn.grid(row=3, column=0, columnspan=1, sticky="nsew", padx=4, pady=4)
Number5_btn = tk.Button(root, text=" 5 ", command=lambda: append_char('5'),font=button_font)
Number5_btn.grid(row=3, column=1, columnspan=1, sticky="nsew", padx=4, pady=4)
Number6_btn = tk.Button(root, text=" 6 ", command=lambda: append_char('6'),font=button_font)
Number6_btn.grid(row=3, column=2, columnspan=1, sticky="nsew", padx=4, pady=4)
Minus_btn = tk.Button(root, text=" - ", command=lambda: append_char('-'),font=button_font)
Minus_btn.grid(row=3, column=3, columnspan=1, sticky="nsew", padx=4, pady=4)
Number1_btn = tk.Button(root, text=" 1 ", command=lambda: append_char('1'),font=button_font)
Number1_btn.grid(row=4, column=0, columnspan=1, sticky="nsew", padx=4, pady=4)
Number2_btn = tk.Button(root, text=" 2 ", command=lambda: append_char('2'),font=button_font)
Number2_btn.grid(row=4, column=1, columnspan=1, sticky="nsew", padx=4, pady=4)
Number3_btn = tk.Button(root, text=" 3 ", command=lambda: append_char('3'),font=button_font)
Number3_btn.grid(row=4, column=2, columnspan=1, sticky="nsew", padx=4, pady=4)
Sum_btn = tk.Button(root, text=" + ", command=lambda: append_char('+'),font=button_font)
Sum_btn.grid(row=4, column=3, columnspan=1, sticky="nsew", padx=4, pady=4)
Parentheses_btn = tk.Button(root, text=" ( ) ", command=toggle_parentheses,font=button_font)
Parentheses_btn.grid(row=5, column=0, columnspan=1, sticky="nsew", padx=4, pady=4)
Number0_btn = tk.Button(root, text=" 0 ", command=lambda: append_char('0'),font=button_font)
Number0_btn.grid(row=5, column=1, columnspan=1, sticky="nsew", padx=4, pady=4)
Dot_btn = tk.Button(root, text=" . ", command=lambda: append_char('.'),font=button_font)
Dot_btn.grid(row=5, column=2, columnspan=1, sticky="nsew", padx=4, pady=4)
Equal_btn = tk.Button(root, text=" = ", command=Equal, bg="lightblue",font=button_font)
Equal_btn.grid(row=5, column=3, columnspan=1, sticky="nsew", padx=4, pady=4)

regular_buttons = [
	Modulo_btn, Divise_btn, Number7_btn, Number8_btn, Number9_btn, Multiply_btn,
	Number4_btn, Number5_btn, Number6_btn, Minus_btn,
	Number1_btn, Number2_btn, Number3_btn, Sum_btn,
	Parentheses_btn, Number0_btn, Dot_btn,
]

initial_theme = load_saved_theme()
theme_choice.set(initial_theme)
set_theme(initial_theme)

# Bind keyboard input
root.bind('<Key>', on_key_press)

root.mainloop()
