import tkinter as tk
from tkinter import ttk, messagebox

class VoltageDividerCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Voltage Divider Calculator (3 Resistors)")

        self.voltage = tk.StringVar()
        self.r1 = tk.StringVar()
        self.r2 = tk.StringVar()
        self.r3 = tk.StringVar()

        self.unit1 = tk.StringVar(value="Ω")
        self.unit2 = tk.StringVar(value="Ω")
        self.unit3 = tk.StringVar(value="Ω")

        self.v_r1 = tk.StringVar()
        self.v_r2 = tk.StringVar()
        self.v_r3 = tk.StringVar()

        self.create_widgets()

    def get_multiplier(self, unit):
        return {"Ω": 1, "kΩ": 1e3, "MΩ": 1e6}[unit]

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0)

        # Input Voltage
        ttk.Label(frame, text="Input Voltage (V):").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.voltage).grid(row=0, column=1, pady=5)

        # R1
        ttk.Label(frame, text="R1:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.r1).grid(row=1, column=1)
        ttk.Combobox(frame, textvariable=self.unit1, values=["Ω", "kΩ", "MΩ"], state="readonly", width=5).grid(row=1, column=2)

        # R2
        ttk.Label(frame, text="R2:").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.r2).grid(row=2, column=1)
        ttk.Combobox(frame, textvariable=self.unit2, values=["Ω", "kΩ", "MΩ"], state="readonly", width=5).grid(row=2, column=2)

        # R3
        ttk.Label(frame, text="R3:").grid(row=3, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.r3).grid(row=3, column=1)
        ttk.Combobox(frame, textvariable=self.unit3, values=["Ω", "kΩ", "MΩ"], state="readonly", width=5).grid(row=3, column=2)

        # Output Section
        ttk.Label(frame, text="Voltage Across R1 (V):").grid(row=5, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.v_r1, state="readonly").grid(row=5, column=1)

        ttk.Label(frame, text="Voltage Across R2 (V):").grid(row=6, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.v_r2, state="readonly").grid(row=6, column=1)

        ttk.Label(frame, text="Voltage Across R3 (V):").grid(row=7, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.v_r3, state="readonly").grid(row=7, column=1)

        # Buttons
        ttk.Button(frame, text="Calculate", command=self.calculate).grid(row=8, column=0, pady=10)
        ttk.Button(frame, text="Clear", command=self.clear).grid(row=8, column=1, pady=10)

    def calculate(self):
        try:
            vin = float(self.voltage.get())
            r1 = float(self.r1.get()) * self.get_multiplier(self.unit1.get())
            r2 = float(self.r2.get()) * self.get_multiplier(self.unit2.get())
            r3 = float(self.r3.get()) * self.get_multiplier(self.unit3.get())

            total = r1 + r2 + r3
            if total == 0:
                raise ZeroDivisionError

            v1 = vin * r1 / total
            v2 = vin * r2 / total
            v3 = vin * r3 / total

            self.v_r1.set(f"{v1:.6f}")
            self.v_r2.set(f"{v2:.6f}")
            self.v_r3.set(f"{v3:.6f}")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")
        except ZeroDivisionError:
            messagebox.showerror("Error", "Total resistance cannot be zero.")

    def clear(self):
        self.voltage.set("")
        self.r1.set("")
        self.r2.set("")
        self.r3.set("")
        self.v_r1.set("")
        self.v_r2.set("")
        self.v_r3.set("")
        self.unit1.set("Ω")
        self.unit2.set("Ω")
        self.unit3.set("Ω")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoltageDividerCalculator(root)
    root.mainloop()
