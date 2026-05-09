import tkinter as tk
from tkinter import ttk, messagebox
import math

def cross_product(a, b):
    """Calcula el producto vectorial a × b"""
    return (
        a[1]*b[2] - a[2]*b[1],
        -(a[0]*b[2] - a[2]*b[0]),
        a[0]*b[1] - a[1]*b[0]
    )

def magnitude(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def force_charge(q_uC, v, B):
    """F = q(v × B)"""
    q = q_uC * 1e-6
    vxB = cross_product(v, B)
    return tuple(q * c for c in vxB)

def force_conductor(P, Q, I, B):
    """F = I(L × B)   donde L = Q - P"""
    L = (Q[0]-P[0], Q[1]-P[1], Q[2]-P[2])
    LxB = cross_product(L, B)
    return tuple(I * c for c in LxB)

def fmt_vec(v, prec=4):
    def fmt(x):
        if abs(x) < 1e-10:
            x = 0.0
        return f"{x:+.{prec}e}"
    return f"⟨ {fmt(v[0])}, {fmt(v[1])}, {fmt(v[2])} ⟩"

DARK_BG   = "#0d1117"
PANEL_BG  = "#161b22"
ACCENT    = "#58a6ff"
ACCENT2   = "#3fb950"
ACCENT3   = "#f78166"
TEXT_PRI  = "#e6edf3"
TEXT_SEC  = "#8b949e"
BORDER    = "#30363d"
INPUT_BG  = "#21262d"

FONT_TITLE  = ("Courier New", 22, "bold")
FONT_LABEL  = ("Courier New", 10, "bold")
FONT_INPUT  = ("Courier New", 10)
FONT_RESULT = ("Courier New", 11)
FONT_SMALL  = ("Courier New", 9)


class VectorEntry(tk.Frame):
    """Widget de entrada para un vector 3D."""
    def __init__(self, parent, label, color=ACCENT, **kw):
        super().__init__(parent, bg=PANEL_BG, **kw)
        tk.Label(self, text=label, font=FONT_LABEL, fg=color,
                 bg=PANEL_BG).pack(anchor="w", pady=(0, 2))
        row = tk.Frame(self, bg=PANEL_BG)
        row.pack(fill="x")
        self.entries = []
        for ax in ("x", "y", "z"):
            f = tk.Frame(row, bg=PANEL_BG)
            f.pack(side="left", padx=(0, 8))
            tk.Label(f, text=ax, font=FONT_SMALL, fg=TEXT_SEC,
                     bg=PANEL_BG).pack(anchor="w")
            e = tk.Entry(f, width=9, font=FONT_INPUT,
                         bg=INPUT_BG, fg=TEXT_PRI, insertbackground=ACCENT,
                         relief="flat", highlightthickness=1,
                         highlightbackground=BORDER,
                         highlightcolor=color)
            e.pack()
            self.entries.append(e)

    def get(self):
        return tuple(float(e.get()) for e in self.entries)

    def set(self, vals):
        for e, v in zip(self.entries, vals):
            e.delete(0, "end")
            e.insert(0, str(v))


class ScalarEntry(tk.Frame):
    def __init__(self, parent, label, unit="", color=ACCENT, **kw):
        super().__init__(parent, bg=PANEL_BG, **kw)
        tk.Label(self, text=f"{label}  {unit}", font=FONT_LABEL,
                 fg=color, bg=PANEL_BG).pack(anchor="w", pady=(0, 2))
        self.entry = tk.Entry(self, width=14, font=FONT_INPUT,
                              bg=INPUT_BG, fg=TEXT_PRI, insertbackground=ACCENT,
                              relief="flat", highlightthickness=1,
                              highlightbackground=BORDER, highlightcolor=color)
        self.entry.pack(anchor="w")

    def get(self):
        return float(self.entry.get())

    def set(self, v):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(v))


class ResultBox(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=PANEL_BG, relief="flat",
                         highlightthickness=1, highlightbackground=BORDER, **kw)
        self.text = tk.Text(self, font=FONT_RESULT, bg=PANEL_BG,
                            fg=TEXT_PRI, relief="flat", state="disabled",
                            padx=14, pady=10, height=8, wrap="word",
                            selectbackground=ACCENT, cursor="arrow")
        self.text.pack(fill="both", expand=True)
        self.text.tag_config("title",  foreground=ACCENT,  font=("Courier New", 11, "bold"))
        self.text.tag_config("result", foreground=ACCENT2, font=("Courier New", 12, "bold"))
        self.text.tag_config("label",  foreground=TEXT_SEC, font=("Courier New", 10))
        self.text.tag_config("warn",   foreground=ACCENT3, font=("Courier New", 10, "italic"))

    def clear(self):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        self.text.config(state="disabled")

    def write(self, txt, tag=""):
        self.text.config(state="normal")
        self.text.insert("end", txt, tag)
        self.text.config(state="disabled")

class TabGeneral(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL_BG, padx=24, pady=20)
        tk.Label(self, text="Producto Vectorial  a × b",
                 font=FONT_TITLE, fg=ACCENT, bg=PANEL_BG).pack(anchor="w", pady=(0, 16))

        formula = "a × b = (a₂b₃−a₃b₂)î − (a₁b₃−a₃b₁)ĵ + (a₁b₂−a₂b₁)k̂"
        tk.Label(self, text=formula, font=FONT_SMALL,
                 fg=TEXT_SEC, bg=PANEL_BG).pack(anchor="w", pady=(0, 18))

        self.va = VectorEntry(self, "Vector  a", color=ACCENT)
        self.va.pack(fill="x", pady=(0, 12))
        self.vb = VectorEntry(self, "Vector  b", color=ACCENT2)
        self.vb.pack(fill="x", pady=(0, 18))

        btn = tk.Button(self, text="  Calcular  a × b  →",
                        font=FONT_LABEL, bg=ACCENT, fg=DARK_BG,
                        relief="flat", padx=18, pady=8, cursor="hand2",
                        activebackground="#79c0ff", activeforeground=DARK_BG,
                        command=self.calc)
        btn.pack(anchor="w", pady=(0, 18))

        self.result = ResultBox(self)
        self.result.pack(fill="both", expand=True)

    def calc(self):
        try:
            a = self.va.get()
            b = self.vb.get()
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos.")
            return
        r = cross_product(a, b)
        mag = magnitude(r)
        self.result.clear()
        self.result.write("Vectores de entrada\n", "title")
        self.result.write(f"  a = {fmt_vec(a)}\n", "label")
        self.result.write(f"  b = {fmt_vec(b)}\n\n", "label")
        self.result.write("Resultado  a × b\n", "title")
        self.result.write(f"  {fmt_vec(r)}\n\n", "result")
        self.result.write(f"  |a × b| = {mag:.6f}\n", "label")

class TabEscenario1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL_BG, padx=24, pady=20)
        tk.Label(self, text="Escenario 1 — Partícula Cargada",
                 font=FONT_TITLE, fg=ACCENT3, bg=PANEL_BG).pack(anchor="w", pady=(0, 6))
        tk.Label(self, text="F = q (v × B)",
                 font=("Courier New", 13, "bold"), fg=TEXT_SEC, bg=PANEL_BG).pack(anchor="w", pady=(0, 16))

        # Defaults del enunciado
        self.q_entry = ScalarEntry(self, "Carga  q", unit="[μC]", color=ACCENT3)
        self.q_entry.set(-10)
        self.q_entry.pack(fill="x", pady=(0, 12))

        self.vv = VectorEntry(self, "Velocidad  v  [× 10³ m/s]", color=ACCENT)
        self.vv.set([2, -3, 0.5])
        self.vv.pack(fill="x", pady=(0, 12))

        self.vB = VectorEntry(self, "Campo magnético  B  [T]", color=ACCENT2)
        self.vB.set([-1, 0.8, -3])
        self.vB.pack(fill="x", pady=(0, 18))

        btn = tk.Button(self, text="  Calcular Fuerza  →",
                        font=FONT_LABEL, bg=ACCENT3, fg=DARK_BG,
                        relief="flat", padx=18, pady=8, cursor="hand2",
                        activebackground="#ffa198", activeforeground=DARK_BG,
                        command=self.calc)
        btn.pack(anchor="w", pady=(0, 18))

        self.result = ResultBox(self)
        self.result.pack(fill="both", expand=True)

    def calc(self):
        try:
            q  = self.q_entry.get()
            v  = tuple(c * 1e3 for c in self.vv.get())   # ×10³
            B  = self.vB.get()
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos.")
            return

        vxB = cross_product(v, B)
        F   = force_charge(q, v, B)
        mag = magnitude(F)

        self.result.clear()
        self.result.write("Datos\n", "title")
        self.result.write(f"  q = {q} μC  =  {q*1e-6:.3e} C\n", "label")
        self.result.write(f"  v = {fmt_vec(v)}  m/s\n", "label")
        self.result.write(f"  B = {fmt_vec(B)}  T\n\n", "label")
        self.result.write("v × B\n", "title")
        self.result.write(f"  {fmt_vec(vxB)}\n\n", "label")
        self.result.write("Fuerza  F = q(v × B)  [N]\n", "title")
        self.result.write(f"  {fmt_vec(F)}\n\n", "result")
        self.result.write(f"  |F| = {mag:.6e} N\n", "label")


class TabEscenario2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL_BG, padx=24, pady=20)
        tk.Label(self, text="Escenario 2 — Conductor Recto",
                 font=FONT_TITLE, fg=ACCENT2, bg=PANEL_BG).pack(anchor="w", pady=(0, 6))
        tk.Label(self, text="F = I (L × B)   ,   L = Q − P",
                 font=("Courier New", 13, "bold"), fg=TEXT_SEC, bg=PANEL_BG).pack(anchor="w", pady=(0, 16))

        # Defaults del enunciado
        self.vP = VectorEntry(self, "Punto  P  [m]", color=ACCENT3)
        self.vP.set([-7, 4, 5])
        self.vP.pack(fill="x", pady=(0, 12))

        self.vQ = VectorEntry(self, "Punto  Q  [m]", color=ACCENT3)
        self.vQ.set([8, 0, -4])
        self.vQ.pack(fill="x", pady=(0, 12))

        self.I_entry = ScalarEntry(self, "Corriente  I", unit="[A]", color=ACCENT)
        self.I_entry.set(20)
        self.I_entry.pack(fill="x", pady=(0, 12))

        self.vB = VectorEntry(self, "Campo magnético  B  [T]", color=ACCENT2)
        self.vB.set([0.8, 4, -2])
        self.vB.pack(fill="x", pady=(0, 18))

        btn = tk.Button(self, text="  Calcular Fuerza  →",
                        font=FONT_LABEL, bg=ACCENT2, fg=DARK_BG,
                        relief="flat", padx=18, pady=8, cursor="hand2",
                        activebackground="#56d364", activeforeground=DARK_BG,
                        command=self.calc)
        btn.pack(anchor="w", pady=(0, 18))

        self.result = ResultBox(self)
        self.result.pack(fill="both", expand=True)

    def calc(self):
        try:
            P = self.vP.get()
            Q = self.vQ.get()
            I = self.I_entry.get()
            B = self.vB.get()
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos.")
            return

        L   = (Q[0]-P[0], Q[1]-P[1], Q[2]-P[2])
        LxB = cross_product(L, B)
        F   = force_conductor(P, Q, I, B)
        mag = magnitude(F)

        self.result.clear()
        self.result.write("Datos\n", "title")
        self.result.write(f"  P = {fmt_vec(P)}  m\n", "label")
        self.result.write(f"  Q = {fmt_vec(Q)}  m\n", "label")
        self.result.write(f"  I = {I} A\n", "label")
        self.result.write(f"  B = {fmt_vec(B)}  T\n\n", "label")
        self.result.write("Vector de longitud  L = Q − P\n", "title")
        self.result.write(f"  {fmt_vec(L)}  m\n\n", "label")
        self.result.write("L × B\n", "title")
        self.result.write(f"  {fmt_vec(LxB)}\n\n", "label")
        self.result.write("Fuerza  F = I(L × B)  [N]\n", "title")
        self.result.write(f"  {fmt_vec(F)}\n\n", "result")
        self.result.write(f"  |F| = {mag:.6e} N\n", "label")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Producto Vectorial & Fuerza Magnética")
        self.configure(bg=DARK_BG)
        self.resizable(True, True)
        self.minsize(620, 580)

        # ── Header ──
        header = tk.Frame(self, bg=DARK_BG, padx=24, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="⟨ Vector Lab ⟩",
                 font=("Courier New", 28, "bold"),
                 fg=ACCENT, bg=DARK_BG).pack(side="left")
        tk.Label(header, text="Producto Vectorial & Fuerzas Magnéticas",
                 font=FONT_SMALL, fg=TEXT_SEC, bg=DARK_BG).pack(side="left", padx=16, pady=6)

        # ── Separador ──
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # ── Notebook (pestañas) ──
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TNotebook",
                         background=DARK_BG, borderwidth=0, tabmargins=0)
        style.configure("TNotebook.Tab",
                         background=INPUT_BG, foreground=TEXT_SEC,
                         font=("Courier New", 10, "bold"),
                         padding=[20, 8], borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", PANEL_BG)],
                  foreground=[("selected", TEXT_PRI)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        nb.add(TabGeneral(nb),    text=" Producto Vectorial  ")
        nb.add(TabEscenario1(nb), text=" Escenario 1 - Particula Cargada  ")
        nb.add(TabEscenario2(nb), text=" Escenario 2 - Conductor Recto  ")

        # ── Footer ──
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
        tk.Label(self, text="F = q(v × B)   |   F = I(L × B)",
                 font=FONT_SMALL, fg=TEXT_SEC, bg=DARK_BG,
                 pady=6).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()