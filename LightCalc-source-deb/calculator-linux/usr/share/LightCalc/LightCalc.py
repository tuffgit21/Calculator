import ast
import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import webbrowser

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "theme_settings.txt")
Version = "v"+"2.0"+"-"+"release"
root = ctk.CTk()
# Themes
ctk.set_appearance_mode("system")

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


def set_theme(theme_name):
	ctk.set_appearance_mode(theme_name)
	save_theme(theme_name)

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)

link_font_normal = ctk.CTkFont(size=13)
link_font_hover = ctk.CTkFont(size=13, underline=True)


def open_url(url):
    """Opens the specified URL in the default web browser."""
    webbrowser.open_new_tab(url)

def show_custom_messagebox():
    # Create a top-level window
    msg_box = ctk.CTkToplevel()
    msg_box._iconbitmap_method_called = True  # keep the root window icon
    msg_box.title("More Projects")
    msg_box.geometry("300x120")
    msg_box.resizable(False, False)

    # Make it modal (force focus)
    msg_box.grab_set()

    # Regular text description
    label_text = ctk.CTkLabel(msg_box, text="For more Projects, please visit this site")
    label_text.pack(padx=10, pady=10)

    # Clickable hyperlink label
    url = "https://tuffgit21.github.io/#work"
    link_label = ctk.CTkLabel(msg_box, text="Click Here for projects", text_color="blue")
    link_label.pack(pady=5)

    # Bind mouse click and hover effects to the link
    link_label.bind("<Button-1>", lambda e: open_url(url))
    link_label.bind("<Enter>", lambda e: link_label.configure(font=link_font_hover))
    link_label.bind("<Leave>", lambda e: link_label.configure(font=link_font_normal))

    # Close button
    close_button = ctk.CTkButton(msg_box, text="OK", width=80, command=msg_box.destroy)
    close_button.pack(pady=10)
def About():
	messagebox.showinfo("About",f"LightCalc {Version}\nHere is a lightweight and Open-source Calculator made by tuffgit21, made specifically for systems without Calculator.")
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
root._iconbitmap_method_called = True  # stop customtkinter from replacing the icon after 200ms
root.title(f"LightCalc {Version}")
root.geometry("300x350")
root.resizable(False, False)
output_font = ctk.CTkFont(family="Courier New", size=16)
output_box = ctk.CTkTextbox(root, height=72, width=284, wrap="word", font=output_font)
output_box.configure(state="disabled")
regular_buttons = []

# Configure grid for a calculator-like layout
for c in range(4):
	root.columnconfigure(c, weight=1, uniform="col")
root.rowconfigure(0, weight=0)
for r in range(1, 6):
	root.rowconfigure(r, weight=1)

output_box.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=8, pady=8)

def _get_expr():
	output_box.configure(state="normal")
	expr = output_box.get("1.0", "end-1c")
	output_box.configure(state="disabled")
	return expr

def _set_expr(text):
	output_box.configure(state="normal")
	output_box.delete("1.0", "end")
	output_box.insert("end", text)
	output_box.configure(state="disabled")

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
button_font = ctk.CTkFont(family="Ubuntu", size=16, weight="bold")
Delete_font = ctk.CTkFont(family="Ubuntu", size=11, weight="bold")
Clear_button = ctk.CTkButton(root, text=" C ", command=Clear, fg_color="#ff0000", text_color="black", hover_color="#cc0000", font=button_font)
Clear_button.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=4, pady=4)
Delete_button = ctk.CTkButton(root, text=" ⌫ ", command=Delete, fg_color="#ff0000", text_color="black", hover_color="#cc0000", font=Delete_font)
Delete_button.grid(row=1, column=1, columnspan=1, sticky="nsew", padx=4, pady=4)
Modulo_btn = ctk.CTkButton(root, text=" % ", command=lambda: append_char('%'), font=button_font)
Modulo_btn.grid(row=1, column=2, columnspan=1, sticky="nsew", padx=4, pady=4)
Divise_btn = ctk.CTkButton(root, text=" / ", command=lambda: append_char('/'), font=button_font)
Divise_btn.grid(row=1, column=3, columnspan=1, sticky="nsew", padx=4, pady=4)
Number7_btn = ctk.CTkButton(root, text=" 7 ", command=lambda: append_char('7'), font=button_font)
Number7_btn.grid(row=2, column=0, columnspan=1, sticky="nsew", padx=4, pady=4)
Number8_btn = ctk.CTkButton(root, text=" 8 ", command=lambda: append_char('8'), font=button_font)
Number8_btn.grid(row=2, column=1, columnspan=1, sticky="nsew", padx=4, pady=4)
Number9_btn = ctk.CTkButton(root, text=" 9 ", command=lambda: append_char('9'), font=button_font)
Number9_btn.grid(row=2, column=2, columnspan=1, sticky="nsew", padx=4, pady=4)
Multiply_btn = ctk.CTkButton(root, text=" * ", command=lambda: append_char('*'), font=button_font)
Multiply_btn.grid(row=2, column=3, columnspan=1, sticky="nsew", padx=4, pady=4)
Number4_btn = ctk.CTkButton(root, text=" 4 ", command=lambda: append_char('4'), font=button_font)
Number4_btn.grid(row=3, column=0, columnspan=1, sticky="nsew", padx=4, pady=4)
Number5_btn = ctk.CTkButton(root, text=" 5 ", command=lambda: append_char('5'), font=button_font)
Number5_btn.grid(row=3, column=1, columnspan=1, sticky="nsew", padx=4, pady=4)
Number6_btn = ctk.CTkButton(root, text=" 6 ", command=lambda: append_char('6'), font=button_font)
Number6_btn.grid(row=3, column=2, columnspan=1, sticky="nsew", padx=4, pady=4)
Minus_btn = ctk.CTkButton(root, text=" - ", command=lambda: append_char('-'), font=button_font)
Minus_btn.grid(row=3, column=3, columnspan=1, sticky="nsew", padx=4, pady=4)
Number1_btn = ctk.CTkButton(root, text=" 1 ", command=lambda: append_char('1'), font=button_font)
Number1_btn.grid(row=4, column=0, columnspan=1, sticky="nsew", padx=4, pady=4)
Number2_btn = ctk.CTkButton(root, text=" 2 ", command=lambda: append_char('2'), font=button_font)
Number2_btn.grid(row=4, column=1, columnspan=1, sticky="nsew", padx=4, pady=4)
Number3_btn = ctk.CTkButton(root, text=" 3 ", command=lambda: append_char('3'), font=button_font)
Number3_btn.grid(row=4, column=2, columnspan=1, sticky="nsew", padx=4, pady=4)
Sum_btn = ctk.CTkButton(root, text=" + ", command=lambda: append_char('+'), font=button_font)
Sum_btn.grid(row=4, column=3, columnspan=1, sticky="nsew", padx=4, pady=4)
Parentheses_btn = ctk.CTkButton(root, text=" ( ) ", command=toggle_parentheses, font=button_font)
Parentheses_btn.grid(row=5, column=0, columnspan=1, sticky="nsew", padx=4, pady=4)
Number0_btn = ctk.CTkButton(root, text=" 0 ", command=lambda: append_char('0'), font=button_font)
Number0_btn.grid(row=5, column=1, columnspan=1, sticky="nsew", padx=4, pady=4)
Dot_btn = ctk.CTkButton(root, text=" . ", command=lambda: append_char('.'), font=button_font)
Dot_btn.grid(row=5, column=2, columnspan=1, sticky="nsew", padx=4, pady=4)
Equal_btn = ctk.CTkButton(root, text=" = ", command=Equal, fg_color="#add8e6", text_color="black", hover_color="#87ceeb", font=button_font)
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
