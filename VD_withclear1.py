import tkinter as tk
from tkinter import ttk, messagebox

class VoltageDividerCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Voltage Divider Calculator")

        # Variables
        self.volts = tk.StringVar()
        self.ohms1 = tk.StringVar()
        self.ohms2 = tk.StringVar()
        self.volts_out = tk.StringVar()
        self.ohms1_unit = tk.StringVar(value="Ω")
        self.ohms2_unit = tk.StringVar(value="Ω")

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0)

        # Title and Description
        desc_label = ttk.Label(frame, text=(
            "M E C H A T R O N I X\n"
            "Created by: Mahesh Babu Tankashala\n"
            "Contact: +91 9490611972"
            
        ), justify="center", foreground="black", font=("Segoe UI", 10, "bold"))
        desc_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Input fields
        ttk.Label(frame, text="Voltage Source (Vₛ):").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.volts).grid(row=1, column=1)
        ttk.Label(frame, text=("V"),foreground="red",font=("Segoe UI",10,"bold")).grid(row=1, column=2, pady=5)

        ttk.Label(frame, text="Resistance 1 (R₁):").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.ohms1).grid(row=2, column=1)
        ttk.Combobox(frame, textvariable=self.ohms1_unit, values=["Ω", "kΩ", "MΩ"],
                     state="readonly", width=5).grid(row=2, column=2,pady=5)

        ttk.Label(frame, text="Resistance 2 (R₂):").grid(row=3, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.ohms2).grid(row=3, column=1)
        ttk.Combobox(frame, textvariable=self.ohms2_unit, values=["Ω", "kΩ", "MΩ"],
                     state="readonly", width=5).grid(row=3, column=2,pady=5)

        ttk.Label(frame, text="Output Voltage (Vₒᵤₜ):").grid(row=4, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.volts_out).grid(row=4, column=1)
        ttk.Label(frame,text=("V"),foreground="red",font=("Segoe UI",10,"bold")).grid(row=4, column=2,pady=5)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="Calculate", command=self.calculate).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).grid(row=0, column=1, padx=5)

        # Footer
        foot=ttk.Label(frame, text=("Enter any 3 values and select units. Click 'Calculate'."),foreground="blue",font=("Segoe UI", 10, "bold"))
        foot.grid(row=6, column=0, columnspan=3, pady=5)

    def get_multiplier(self, unit):
        return {"Ω": 1.0, "kΩ": 1000.0, "MΩ": 1_000_000.0}.get(unit, 1.0)

    def clear_fields(self):
        self.volts.set("")
        self.ohms1.set("")
        self.ohms2.set("")
        self.volts_out.set("")
        self.ohms1_unit.set("Ω")
        self.ohms2_unit.set("Ω")

    def calculate(self):
        try:
            vs_raw = self.volts.get().strip()
            r1_raw = self.ohms1.get().strip()
            r2_raw = self.ohms2.get().strip()
            vout_raw = self.volts_out.get().strip()

            # Detect which value is missing
            missing_fields = [not vs_raw, not r1_raw, not r2_raw, not vout_raw]
            if missing_fields.count(True) > 1:
                messagebox.showerror("Error", "Please leave only one field blank to calculate.")
                return

            # Convert to float after determining missing
            vs = float(vs_raw) if vs_raw else None
            r1 = float(r1_raw) * self.get_multiplier(self.ohms1_unit.get()) if r1_raw else None
            r2 = float(r2_raw) * self.get_multiplier(self.ohms2_unit.get()) if r2_raw else None
            vout = float(vout_raw) if vout_raw else None

            if vs is None:
                vs = vout * (r1 + r2) / r2
                self.volts.set(f"{round(vs, 2)}")
            elif r1 is None:
                r1 = (vs * r2 / vout) - r2
                self.ohms1.set(f"{round(r1 / self.get_multiplier(self.ohms1_unit.get()), 2)}")
            elif r2 is None:
                r2 = vout * r1 / (vs - vout)
                self.ohms2.set(f"{round(r2 / self.get_multiplier(self.ohms2_unit.get()), 2)}")
            elif vout is None:
                vout = vs * r2 / (r1 + r2)
                self.volts_out.set(f"{round(vout, 2)}")
            else:
                # All values filled – recalculate Vout based on current units
                vout = vs * r2 / (r1 + r2)
                self.volts_out.set(f"{round(vout, 2)}")

        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero. Please check values.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoltageDividerCalculator(root)
    root.mainloop()
