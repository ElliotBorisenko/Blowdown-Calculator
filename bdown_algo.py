# Blowdown time calculator
# Elliot Borisenko (2023)

import math

from datetime import datetime

import matplotlib.pyplot as plt

# Required variables

def bdown_calc(sys_vol, bpress, p_atm, cv, xt, mol_wt, initial_p, initial_t, initial_z, initial_k,
	final_p, final_t, final_z, final_k, notes):

	"""Blowdown calculation algo based on initial and final conditions."""

	# Interval factors

	p_int_factor = ((final_p + p_atm)/(initial_p + p_atm))**(1/40)
	t_int_factor = ((final_t)/(initial_t))**(1/40)
	z_int_factor = (final_z/initial_z)**(1/40)
	k_int_factor = (final_k/initial_k)**(1/40)

	# Backpressure for calculations

	pb = bpress + p_atm

	# Source volume properties

	p = []
	p_g = []
	t = []
	z = []
	vd = []
	m = []
	dm = []
	k = []

	# Initialization of source volume properties based on input

	p.append(initial_p + p_atm)
	p_g.append(initial_p)
	t.append(initial_t)
	z.append(initial_z)
	vd.append((p[0])*(mol_wt)/(z[0]*10.7316*(t[0]+460)))
	m.append(sys_vol * vd[0])
	dm.append(float(0))
	k.append(initial_k)

	# Fisher variables

	cg = 40*cv*(xt**0.5)
	c1 = cg/cv

	angle = []
	sin_func = []
	flow_type = []
	fish_m = []
	fish_sq = []
	fish_dt = []
	fish_tt = []

	# Initial Fisher Calcs

	angle.append((59.64/c1)*((p[0]-pb)/p[0])**0.5)
	if angle[0] >= math.sin(math.pi/2):
		sin_func.append(1.0)
	else:
		sin_func.append(math.sin((59.64/c1)*((p[0]-pb)/p[0]))**0.5)

	if sin_func[0] == 1:
		flow_type.append("Critical")
	else:
		flow_type.append("Sub-critical")

	if flow_type[0] == "Critical":
		fish_m.append(1.06*((vd[0]*p[0])**0.5)*cg)
	else:
		fish_m.append(1.06*((vd[0]*p[0])**0.5)*cg*sin_func[0])

	fish_sq.append(379.32*(fish_m[0]/mol_wt)*24/1e6)
	fish_dt.append(float(0))
	fish_tt.append(float(0))

	# ISA variables

	fk = []
	x = []
	y = []
	isa_type = []
	isa_m = []
	isa_sq = []
	isa_dt = []
	isa_tt = []

	# Initial ISA calculations (Fp = 1)

	fk.append(1/k[0])
	x.append((p[0]-pb)/p[0])
	y.append(1-(x[0]/(3*fk[0]*xt)))

	if y[0] <= (2/3):
		isa_type.append("Critical")
	else:
		isa_type.append("Sub-critical")

	if isa_type[0] == "Critical":
		isa_m.append(19.3*cv*p[0]*(2/3)*((x[0]*mol_wt)/((t[0]+460)*z[0]))**0.5)

	else:
		isa_m.append(19.3*cv*p[0]*y[0]*((x[0]*mol_wt)/((t[0]+460)*z[0]))**0.5)

	isa_sq.append(379.32*(isa_m[0]/mol_wt)*24/1e6)
	isa_dt.append(float(0))
	isa_tt.append(float(0))

	# Loop for 40 interval calculations

	count = 1

	while count <= 40:

		# Volume interval calculations

		j = count
		p.append(p_int_factor*p[j-1])
		p_g.append(p[j]-p_atm)
		t.append(t_int_factor*t[j-1])
		z.append(z_int_factor*z[j-1])
		k.append(k_int_factor*k[j-1])
		vd.append((p[j])*(mol_wt)/(z[j]*10.7316*(t[j]+460)))
		m.append(sys_vol*vd[j])
		dm.append(m[j-1]-m[j])

		# Fisher interval calculations

		angle.append((59.64/c1)*((p[j]-pb)/p[j])**0.5)
		if angle[j] >= math.sin(math.pi/2):
			sin_func.append(1.0)
		else:
			sin_func.append(math.sin((59.64/c1)*((p[j]-pb)/p[j])**0.5))

		if sin_func[j] == 1:
			flow_type.append("Critical")
		else:
			flow_type.append("Sub-critical")

		if flow_type[j] == "Critical":
			fish_m.append(1.06*((vd[j]*p[j])**0.5)*cg)
		else:
			fish_m.append(1.06*((vd[j]*p[j])**0.5)*cg*sin_func[j])
			
		fish_sq.append(379.32*(fish_m[j]/mol_wt)*24/1e6)
		fish_dt.append((dm[j]/fish_m[j-1])*60)
		fish_tt.append(fish_tt[j-1]+fish_dt[j])

		# ISA interval calculations

		fk.append(1/k[j])
		x.append((p[j]-pb)/p[j])
		y.append(1-(x[j]/(3*fk[j]*xt)))

		if y[j] <= (2/3):
			isa_type.append("Critical")
		else:
			isa_type.append("Sub-critical")

		if isa_type[j] == "Critical":
			isa_m.append(19.3*cv*p[j]*(2/3)*((x[j]*mol_wt)/((t[j]+460)
				*z[j]))**0.5)

		else:
			isa_m.append(19.3*cv*p[j]*y[j]*((x[j]*mol_wt)/((t[j]+460)
				*z[j]))**0.5)

		isa_sq.append(379.32*(isa_m[j]/mol_wt)*24/1e6)
		isa_dt.append((dm[j]/isa_m[j-1])*60)
		isa_tt.append(isa_tt[j-1]+isa_dt[j])

		count += 1

	# Date for output file

	current_date = datetime.now()

	# Calculation results for output file

	fish_max_q = round(max(fish_sq),2)
	isa_max_q = round(max(isa_sq), 2)
	total_dm = round(m[0]-m[-1],2)
	fish_time = round(fish_tt[-1],2)
	isa_time = round(isa_tt[-1], 2)
	fish_avg_q = round(379.32*(((total_dm)/(fish_time/60))/mol_wt)*24/1e6, 2)
	isa_avg_q = round(379.32*(((total_dm)/(isa_time/60))/mol_wt)*24/1e6, 2)

	# Output file

	filename = 'blowdown_output.txt'

	# Population of output file

	with open(filename, 'w') as f:
		f.write("Blowdown time calculator by Elliot Borisenko (2023).\n")
		f.write(f"Date: {current_date}\n\n")	
		f.write(f"System volume (ft³): {sys_vol}\n")
		f.write(f"System backpressure (psig): {bpress}\n")
		f.write(f"Atmospheric pressure (psia): {p_atm}\n")
		f.write(f"Valve Cv @ 100% travel: {cv}\n")
		f.write(f"Valve xT @ 100% travel: {xt}\n")
		f.write(f"Molecular weight: {mol_wt}\n\n")
		f.write(f"Initial pressure (psig): {initial_p}\n")
		f.write(f"Initial temperature (°F): {initial_t}\n")
		f.write(f"Initial compressibility, z: {initial_z}\n")
		f.write(f"Initial heat capacity ratio, k: {initial_k}\n\n")
		f.write(f"Final pressure (psig): {final_p}\n")
		f.write(f"Final temperature (°F): {final_t}\n")
		f.write(f"Final compressibility, z: {final_z}\n")
		f.write(f"Final heat capacity ratio, k: {final_k}\n\n")
		f.write(f"RESULTS: \n\n")
		f.write(f"ISA (Fp=1) blowdown time (min): {isa_time}\n")
		f.write(f"ISA (Fp=1) maximum flow rate (MMscfd): {isa_max_q}\n")
		f.write(f"ISA (Fp=1) average flow rate (MMscfd): {isa_avg_q}\n\n")	
		f.write(f"Fisher blowdown time (min): {fish_time}\n")
		f.write(f"Fisher maximum flow rate (MMscfd): {fish_max_q}\n")
		f.write(f"Fisher average flow rate (MMscfd): {fish_avg_q}\n\n")
		f.write(f"Total mass change (lb): {total_dm}\n\n")
		f.write(f"Notes:\n\n")
		f.write(f"{notes}")

	# Final Fisher time, ISA time, gauge pressure, Fisher time series, ISA time series

	calc_output = [fish_time, isa_time, p_g, fish_tt, isa_tt]

	return calc_output