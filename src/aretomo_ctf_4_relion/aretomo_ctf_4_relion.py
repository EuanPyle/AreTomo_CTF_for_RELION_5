import starfile
import numpy as np
import typer

from typing import Optional
from pathlib import Path
from .utils import update_defocus, run_aretomo2_ctf, update_global_star

cli = typer.Typer(add_completion=False)
@cli.command(name='aretomo_ctf_4_relion')
def estimate_ctf(
        input_star: Path = typer.Option(...),
        output_star: Path = typer.Option(...),
        tsa_dir: Path = typer.Option(...),
        exe: Optional[str] = typer.Option('AreTomo2'),
        tsa_is_imod: Optional[bool] = typer.Option(False),
):
    """
    Carry out CTF estimation of RELION 5 data using AreTomo2.

    Parameters
    ----------

    input_star: Path
        Path to a global RELION 5 star file. This corresponds to the Tomogram .star file during STA.

    output_star: Path
        Desired output file name. 

    tsa_dir: Path
        Any TiltSeriesAlignment job directory which contains all your tomograms. e.g. AlignTiltSeries/job015/

    exe: Optional[str]
        The command which brings up AreTomo2 on the command line. e.g. AreTomo2, or: /some/path/to/AT2/AreTomo2

    tsa_is_imod: Optional[bool]
        If the TSA was carried out using IMOD, use this flag

    """
    ori_star = starfile.read(input_star)
    ori_star.apply(lambda star_row: run_aretomo2_ctf(star_row, tsa_is_imod, tsa_dir), axis=1)
    ori_star.apply(lambda star_row: update_defocus(star_row, tsa_dir), axis=1)
    ori_star['rlnTomoTiltSeriesStarFile'] = ori_star.apply(lambda star_row: update_global_star(star_row), axis=1)
    starfile.write(ori_star,output_star)
