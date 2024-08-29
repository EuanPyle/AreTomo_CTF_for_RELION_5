import starfile
from pathlib import Path
import os
import numpy as np

tsa_star = "AlignTiltSeries/job008/aligned_tilt_series.star" #.star from AlignTiltSeries job in RELION 5
is_imod = False #Was the alignment done in IMOD, true or false?
output_star = "AlignTiltSeries/job008/aligned_tilt_series_ctf.star" #desired output name
exe = 'AreTomo2' #Command which brings up AreTomo2 on cmd line

#######

ori_star = starfile.read(tsa_star)

def run_aretomo2_ctf(star_row):
    ts_name = star_row.rlnTomoName
    voltage = star_row.rlnVoltage
    cs = star_row.rlnSphericalAberration
    ac = star_row.rlnAmplitudeContrast
    pix_size = star_row.rlnTomoTiltSeriesPixelSize
    tsa_path = Path(star_row.rlnTomoTiltSeriesStarFile).parent.parent
    ts_path = tsa_path / 'external' / ts_name 

    command = f'{exe} -InMrc {str(ts_path)}/{ts_name}.mrc -OutMrc {str(ts_path)}/delete_me.mrc -Align 0 -PixSize {pix_size} -Kv {voltage} -Cs {cs} -AmpContrast {ac} -VolZ 0 -DarkTol 0.0000000001'

    if is_imod is True:
        command += f' -AngFile {str(ts_path)}/{ts_name}.tlt '
    else:
        command += f' -AlnFile {str(ts_path)}/{ts_name}.aln '

    os.system(command)
    os.system(f'rm {str(ts_path)}/delete_me.mrc')

def update_defocus(star_row):
    tilt_series_star_path = Path(star_row.rlnTomoTiltSeriesStarFile)
    ts_star = starfile.read(tilt_series_star_path)
    tsa_path = Path(star_row.rlnTomoTiltSeriesStarFile).parent.parent
    ts_root = str(tsa_path / 'external' / star_row.rlnTomoName)
    defocus_file = f'{ts_root}/{star_row.rlnTomoName}_ctf.txt'
    defocus = np.loadtxt(defocus_file)[:,1:7]
    ts_star['rlnDefocusU'] = defocus[:,0]
    ts_star['rlnDefocusV'] = defocus[:,1]
    ts_star['rlnDefocusAngle'] = defocus[:,2]
    ts_star['rlnCtfFigureOfMerit'] = defocus[:,4]
    ts_star['rlnCtfMaxResolution'] = defocus[:,5]
    ts_star['rlnCtfImage'] = f'{ts_root}/{star_row.rlnTomoName}_ctf.mrc'
    output_name = Path(tilt_series_star_path)
    output_name = f'{str(output_name.parent)}/{str(output_name.stem)}_ctf.star'
    starfile.write(ts_star,output_name)

def update_global_star(star_row):
    return star_row['rlnTomoTiltSeriesStarFile'].replace('.star','_ctf.star')

ori_star.apply(lambda star_row: run_aretomo2_ctf(star_row), axis=1)
ori_star.apply(lambda star_row: update_defocus(star_row), axis=1)

ori_star['rlnTomoTiltSeriesStarFile'] = ori_star.apply(lambda star_row: update_global_star(star_row), axis=1)
starfile.write(ori_star,output_star)
               
