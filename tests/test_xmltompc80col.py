"""
Test the conversion from XML to MPC80 col format
Always use high precision, we are not doing low anymore
"""

# Import global
import os
import subprocess
import shlex
from tempfile import NamedTemporaryFile
import pytest


def test_trksub_submission():
    """Test trksub submission"""
    infile = "input/trksub_sub.xml"
    outfile = "output/trksub_sub.obs"
    # Remove outfile if there
    if os.path.exists(outfile):
        os.remove(outfile)
    subprocess.run(
        "xmltompc80col.py " + infile + " " + outfile,
        shell=True,
        check=False,
    )
    assert os.path.exists(outfile) and os.stat(outfile).st_size != 0


def test_trksub_submission_newregex():
    """After changing the regex in xmltompc80col.py, test trksub submission"""
    infile = "input/gb_trksub.xml"
    outfile = "output/gb_trksub.obs"
    # Remove outfile if there
    if os.path.exists(outfile):
        os.remove(outfile)
    subprocess.run(
        "xmltompc80col.py " + infile + " " + outfile,
        shell=True,
        check=False,
    )
    assert os.path.exists(outfile) and os.stat(outfile).st_size != 0


def test_trksub_8char():
    """Converting the file even if the trksub is 8-char long"""
    infile = "input/trksub_8char.xml"
    outfile = "output/trksub_8char.obs"
    # Remove outfile if there
    if os.path.exists(outfile):
        os.remove(outfile)
    subprocess.run(
        "xmltompc80col.py " + infile + " " + outfile,
        shell=True,
        check=False,
    )
    assert os.path.exists(outfile) and os.stat(outfile).st_size != 0


def test_provid_notrksub():
    """Converting the file even if trksub=provid """
    infile = "input/provid_no_trksub.xml"
    outfile = "output/provid_no_trksub.obs"
    # Remove outfile if there
    if os.path.exists(outfile):
        os.remove(outfile)
    subprocess.run(
        "xmltompc80col.py " + infile + " " + outfile,
        shell=True,
        check=False,
    )
    assert os.path.exists(outfile) and os.stat(outfile).st_size != 0


def test_band_conversions():
    """Testing some edge cases mapping ADES to obs80 band designations"""
    infile = "input/band_conversions.xml"
    expfile = "expected/band_conversions.obs"

    with open(expfile) as f_expected:
        expected = f_expected.read()

    with NamedTemporaryFile(mode="w+t", suffix=".obs") as f_output_temp:
        subprocess.run(
            ["xmltompc80col.py", infile, f_output_temp.name],
            shell=False,
            check=True,
        )
        f_output_temp.seek(0)
        observed = f_output_temp.read()

    assert observed == expected


@pytest.mark.xfail
def test_trksub_9char():
    """ The code should stop with an error for any trksubs longer than 8 chars"""
    infile = "input/trksub_9chars.xml"
    outfile = "output/trksub_chars.obs"
    # Remove outfile if there
    if os.path.exists(outfile):
        os.remove(outfile)
    result = subprocess.run(
        "xmltompc80col.py " + infile + " " + outfile,
        shell=True,
        check=True,
    )

    assert result.returncode == 0
    
def test_net_astcat():
    """ This tests whether NET is added to the header"""
    infile = "input/trksub_withastcat.xml"
    outfile = "output/trksub_withnet.obs"
    pyfile = "xmltompc80col.py"

    # Remove outfile if there
    if os.path.exists(outfile):
        os.remove(outfile)
        
    result1 = subprocess.run(
        pyfile + " " + infile + " " + outfile,
        shell=True,
        check=True,
    )
    
    if result1.returncode == 0:
        command = 'grep "^NET" ' + outfile
        args = shlex.split(command)
        result2 = subprocess.run(
            args,
            text=True, 
            capture_output=True,
        )
    
        if result2.returncode == 0:
            netline = result2.stdout
        
            if len(netline) < 80:
                net_present = True
            
            else:
                net_present = False
        
    assert net_present == True
    
    