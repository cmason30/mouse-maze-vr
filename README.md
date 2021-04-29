# mouse-maze-vr
Yorgason Lab statistical analysis of VR mouse simulation project

----------------------------

So far, the files of interest are 

colin_sub_funcs.py
- Functions for colin_funcs to reference. 

colin_funcs.py
- This file contains the necessary functions for vr_mastersheet.py to reference.
- Also compiles everything into a mastersheet.  

mastersheet_mod_funcs.py 
- References colin_funcs.py and has everything needed to create an experiment dataframe and send it to a master_csv. 

vr_vis.py
- Plots mouse movements and other statistics with a variety of visualizations. 

run_experiments.py
- Can loop through experiment files, given a directory. 

----------------------------

The file tree:

colin_sub_funcs.py > colin_funcs.py > mastersheet_mod_funcs.py > run_experiments.py
                                    > vr_vis.py
