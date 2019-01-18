Tennis String Recommender

Data obtained from Tennis Warehouse University - String Performance Database
(http://twu.tennis-warehouse.com/learning_center/reporter2.php)


***************************** Original Dataset ****************************

Original Column Name	Formatted Name	Units (if app.)
String	string	N/A
none	string_code	0-4752
Ref. Ten. (lbs)	ref_t	lbs
Swing Speed	swing_speed	fast/med/slow
Material	material	N/A
Gauge Nominal (mm)	gauge_nom	mm
Gauge Acutal (mm)	gauce_ac	mm
Stretch at 40 lbs (%)	stretch_40	lbs (%)
Stretch at 51 lbs (%)	stretch_51	lbs (%)
Stretch at 62 lbs (%)	stretch_62	lbs (%)
Actual Pre-impact Tension (lbs)	pre_t	lbs
Dwell Time (ms)	dwell	ms
Deflection (mm)	deflec	mm
Tension Change (lbs)	change_t	lbs
Peak Tension (lbs)	peak_t	lbs
Peak Perp/trans Force (lbs)	peak_trans_force	lbs
Ave Perp. Force (lbs)	avg_trans_force	lbs
Stiffness (lb/in)	stiffness	lbs/in
Static Loss lbs.	static_loss	lbs
Stabilization Loss (lbs)	stabiliz	lbs
Impact Loss (lbs).	impact_loss	lbs
Total Loss (lbs)	total_loss	lbs
Tension Loss (%)	tension_loss	%
Energy Return (%)	energy_return	%
String/String COF	sts_cof	coef of fric
String/Ball COF	stb_cof	coef of fric
Spin Potential	spin_pot	stb COF / sts COF


*****************************  Data Prep  ******************************

** Edited:
  -swing_speed:
    {'Fast':3,'Medium':2,'Slow':1}
  -material:
    18 missing values, replaced with 'unknown'
  -sts_cof, stb_cof, spin_pot, stretch_40, stretch_51, stretch_62:
    NaNs filled with column mean

** Dropped:
  -avg_trans_force (75% NaN)
  -gauce_ac (25% NaN, impossible to interpolate missing values)
  -string ** stored in look-up dictionary for delivery of recs




******************************** To Do *********************************
  -Investigate missing material type for 18 strings with material NaN

  - Return recs with pertinent info like brand, gauge, material

  - Add gauge to bins (15-19) to "original" dataframe for serving recs

  - Incorrect brands:
    - Mantis
    - Leopard
    - One
    - Poly

  - Narrow strings down to top 100 most similar and allow user to include
  preferences (gauge, spin potential, max_tension, etc. to narrow it down)


********************** Notes from TWU Experiments **********************

Stiffness and Temp:
1. Tension loss is a component of stiffness
2. Stiffness is one of the most important parameter in string performance
3. Cold strings play stiffer, warm strings play softer
