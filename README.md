# AreTomo_CTF_for_RELION_5

For some Tomography datasets, CTFFIND doesn't give great CTF estimations whereas AreTomo2 performs better. 

However, currently, CTFFIND is the only way of estimating CTF in RELION 5. 

This wrapper runs the CTF estimation from AreTomo2 on .star files generated by RELION 5 and updates the defocus values. 

It does not perform or overwrite tilt series alignment.

# Installation

`pip install AreTomo_CTF_for_RELION_5`

# Use

`aretomo_ctf_4_relion --help`

# Requirements

You have AreTomo2 (only v2) installed. 

Your project was carried out in RELION 5.

Still carry out a CTF estimation job in CTFFIND so RELION can get the astigmatism values.
