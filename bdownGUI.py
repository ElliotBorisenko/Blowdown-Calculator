# Blowdown time calculator
# Elliot Borisenko (2023)

import tkinter as tk

from tkinter import messagebox

from bdown_algo import bdown_calc

from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

def plot(x, y, z):

	"""Plot of system pressure vs. time for ISA and Fisher calculations."""
	
	bd_plot.clear()
	bd_plot.plot(z, x, linewidth=3, c='red', label="ISA")
	bd_plot.plot(y, x, linewidth=3, c='blue', label="Fisher")
	bd_plot.legend()
	bd_plot.grid()
	bd_plot.set_title("Pressure vs. Time", fontsize=10)
	bd_plot.set_xlabel("Time (min)", fontsize=8)
	bd_plot.set_ylabel("Pressure (psig)", fontsize=8)
	canvas.draw()
	canvas.get_tk_widget().pack()
	toolbar.update()

def calculate():

	"""Pulls widget values and executes blowdown algo when "Calculate" button is pressed.
	Populates output text file."""

	# Check for input value errors

	try:
		sys_vol = float(vol_entry.get())
		backpress = float(bp_entry.get())
		atmpress = float(patm_entry.get())
		mol_weight = float(molwt_entry.get())
		valve_cv = float(cv_entry.get())
		valve_xt = float(xt_entry.get())
		ipressure = float(ipress_entry.get())
		itemperature = float(itemp_entry.get())
		icompress = float(icomp_entry.get())
		iheatcap = float(iheat_entry.get())
		fpressure = float(fpress_entry.get())
		ftemperature = float(ftemp_entry.get())
		fcompress = float(fcomp_entry.get())
		fheatcap = float(fheat_entry.get())
		notes_output = (notes_text.get("1.0", tk.END))

	except ValueError:
		tk.messagebox.showerror("Invalid Input", "Scenario values must be numbers.")

	else:
		bd_output = bdown_calc(sys_vol, backpress, atmpress, valve_cv, valve_xt, mol_weight, ipressure,
			itemperature, icompress, iheatcap, fpressure, ftemperature, fcompress, fheatcap, notes_output)
	
	# Blowdown algo output

	fish_time_output.set(bd_output[0])
	isa_time_output.set(bd_output[1])
	p_series = bd_output[2]
	fish_tt_series = bd_output[3]
	isa_tt_series = bd_output[4]

	# Create plot of Fisher and ISA time series' against pressure

	plot(p_series, fish_tt_series, isa_tt_series)

window = tk.Tk()
window.title("Blowdown Time (Elliot Borisenko, 2023)")

menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Close", command=exit)
menubar.add_cascade(menu=filemenu, label="File")
window.config(menu=menubar)

frame1 = tk.Frame(window)
frame1.pack()

frame2 = tk.Frame(window)
frame2.pack()

frame3 = tk.Frame(window)
frame3.pack()

fig = Figure(figsize=(6,4))
bd_plot = fig.add_subplot()
canvas = FigureCanvasTkAgg(fig, master = window)
toolbar = NavigationToolbar2Tk(canvas, window)

header = tk.Label(frame1, text="Enter scenario values, add notes, and then press Calculate button.\n" 
	"Results in blowdown_output.txt", anchor="w", justify="left")
header.grid(row=0, column=0, padx=5, pady=5, sticky="w")
header.config(font=("TKDefaultFont", 11))

cond_input = tk.LabelFrame(frame2, text="Initial Conditions")
cond_input.grid(row=0, column=0, padx=5, pady=0)
cond_input.config(font=("TKDefaultFont", 12))

cond_input2 = tk.LabelFrame(frame2, text="Final Conditions")
cond_input2.grid(row=1, column=0, padx=5, pady=10)
cond_input2.config(font=("TKDefaultFont", 12))

cond_input3 = tk.LabelFrame(frame2, text="System Conditions")
cond_input3.grid(row=0, column=1, padx=5, pady=0)
cond_input3.config(font=("TKDefaultFont", 12))

cond_input4 = tk.LabelFrame(frame2, text="Valve Details")
cond_input4.grid(row=1, column=1, padx=5, pady=5)
cond_input4.config(font=("TKDefaultFont", 12))

output = tk.LabelFrame(frame2, text="Results")
output.grid(row=2, column=1, padx=5, pady=5)
output.config(font=("TKDefaultFont", 12))

button = tk.Button(frame2, text="Calculate", command=calculate)
button.grid(row=2, column=0, sticky="news", padx=5, pady=5)
button.config(font=("TKDefaultFont", 12))

notes = tk.LabelFrame(frame3, text="Notes")
notes.grid(row=0, column=0, padx=0, pady=0)
notes.config(font=("TKDefaultFont", 12))

notes_text = tk.Text(notes, height=2, font=("TKDefaultFont", 10))
notes_text.grid(row=1, column=1, padx=10, pady=10)

ipress = tk.Label(cond_input, text="Pressure (psig)")
ipress.grid(row=0, column=0)
ipress.config(font=("TKDefaultFont", 10))
itemp = tk.Label(cond_input, text="Temperature (°F)")
itemp.grid(row=1, column=0)
itemp.config(font=("TKDefaultFont", 10))
icomp = tk.Label(cond_input, text="Compressiblity, z")
icomp.grid(row=2, column=0)
icomp.config(font=("TKDefaultFont", 10))
iheat = tk.Label(cond_input, text="Heat Capacity Ratio, k")
iheat.grid(row=3, column=0)
iheat.config(font=("TKDefaultFont", 10))

fpress = tk.Label(cond_input2, text="Pressure (psig)")
fpress.grid(row=0, column=0)
fpress.config(font=("TKDefaultFont", 10))
ftemp = tk.Label(cond_input2, text="Temperature (°F)")
ftemp.grid(row=1, column=0)
ftemp.config(font=("TKDefaultFont", 10))
fcomp = tk.Label(cond_input2, text="Compressiblity, z")
fcomp.grid(row=2, column=0)
fcomp.config(font=("TKDefaultFont", 10))
fheat = tk.Label(cond_input2, text="Heat Capacity Ratio, k")
fheat.grid(row=3, column=0)
fheat.config(font=("TKDefaultFont", 10))

vol = tk.Label(cond_input3, text="System Volume (ft³)")
vol.grid(row=0, column=0)
vol.config(font=("TKDefaultFont", 10))
bp = tk.Label(cond_input3, text="Backpressure (psig)")
bp.grid(row=1, column=0)
bp.config(font=("TKDefaultFont", 10))
patm = tk.Label(cond_input3, text="Atmos. Pressure (psia)")
patm.grid(row=2, column=0)
patm.config(font=("TKDefaultFont", 10))
molwt = tk.Label(cond_input3, text="Molecular Weight")
molwt.grid(row=3, column=0)
molwt.config(font=("TKDefaultFont", 10))

cv = tk.Label(cond_input4, text="Cv @ 100% travel")
cv.grid(row=0, column=0)
cv.config(font=("TKDefaultFont", 10))
xt = tk.Label(cond_input4, text="xT @ 100% travel")
xt.grid(row=1, column=0)
xt.config(font=("TKDefaultFont", 10))

isa_time = tk.Label(output, text="ISA time (min)")
isa_time.grid(row=0, column=0)
isa_time.config(font=("TKDefaultFont", 10))
fish_time = tk.Label(output, text="Fisher time (min)")
fish_time.grid(row=1, column=0)
fish_time.config(font=("TKDefaultFont", 10))

ipress_entry = tk.Entry(cond_input)
itemp_entry = tk.Entry(cond_input)
icomp_entry = tk.Entry(cond_input)
iheat_entry = tk.Entry(cond_input)

fpress_entry = tk.Entry(cond_input2)
ftemp_entry = tk.Entry(cond_input2)
fcomp_entry = tk.Entry(cond_input2)
fheat_entry = tk.Entry(cond_input2)

vol_entry = tk.Entry(cond_input3)
bp_entry = tk.Entry(cond_input3)
patm_entry = tk.Entry(cond_input3)
molwt_entry = tk.Entry(cond_input3)

cv_entry = tk.Entry(cond_input4)
xt_entry = tk.Entry(cond_input4)

ipress_entry.grid(row=0, column=1)
ipress_entry.config(font=("TKDefaultFont", 10))
itemp_entry.grid(row=1, column=1)
itemp_entry.config(font=("TKDefaultFont", 10))
icomp_entry.grid(row=2, column=1)
icomp_entry.config(font=("TKDefaultFont", 10))
iheat_entry.grid(row=3, column=1)
iheat_entry.config(font=("TKDefaultFont", 10))

fpress_entry.grid(row=0, column=1)
fpress_entry.config(font=("TKDefaultFont", 10))
ftemp_entry.grid(row=1, column=1)
ftemp_entry.config(font=("TKDefaultFont", 10))
fcomp_entry.grid(row=2, column=1)
fcomp_entry.config(font=("TKDefaultFont", 10))
fheat_entry.grid(row=3, column=1)
fheat_entry.config(font=("TKDefaultFont", 10))

vol_entry.grid(row=0, column=1)
vol_entry.config(font=("TKDefaultFont", 10))
bp_entry.grid(row=1, column=1)
bp_entry.config(font=("TKDefaultFont", 10))
patm_entry.grid(row=2, column=1)
patm_entry.config(font=("TKDefaultFont", 10))
molwt_entry.grid(row=3, column=1)
molwt_entry.config(font=("TKDefaultFont", 10))

cv_entry.grid(row=0, column=1)
cv_entry.config(font=("TKDefaultFont", 10))
xt_entry.grid(row=1, column=1)
xt_entry.config(font=("TKDefaultFont", 10))

isa_time_output = tk.StringVar()
tk.Label(output, textvariable=isa_time_output, font=("TKDefaultFont", 10)).grid(row=0, column=1)
fish_time_output = tk.StringVar()
tk.Label(output, textvariable=fish_time_output, font=("TKDefaultFont", 10)).grid(row=1, column=1)

window.mainloop()