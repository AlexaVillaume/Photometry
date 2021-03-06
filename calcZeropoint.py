import sys
import os
from subprocess import call

import numpy as np
import matplotlib.pyplot as plt
from astroquery.vizier import Vizier
import astropy.units as u

import makeRegionFile
import Quadtree as Q
import Sources as S
import phot_utils
import geom_utils

def associate(table, tree2):
    dist = 0.000014
    matches = []
    for entry in table:
        match = tree2.match(entry['RAJ2000'], entry['DEJ2000'])
        if match != None and geom_utils.equnorm(entry['RAJ2000'], entry['DEJ2000'], \
                                       match.ra, match.dec) <= dist:
            match.match2 = entry
            matches.append(match)
    return matches

def getSDSS(galaxy):
    """
    Query SDSS through Vizier, pick out only the stellar sources,
    and put the SDSS magnitudes into AB
    """
    Vizier.ROW_LIMIT = -1 # Removes row limit on output table
    result = Vizier.query_region(galaxy, width=1.0*u.deg,
                                 height=1.0*u.deg, catalog='SDSS')
    # Only select stellar sources
    index = []
    for i, entry in enumerate(result[1]):
        if entry['cl'] != 6:
            index.append(i)
    # Get the most recent SDSS catalog
    result[len(result) - 1].remove_rows(index)

    # SDSS magnitudes are not exactly in AB so need to correct (not doing this yet).
    return result[len(result)-1]

def calcZP(galaxy, scam, band):
    """
    To calculate the zeropoint of the Subaru image match the Subaru catalog
    and the table returned from Vizier.
    """
    sdss = getSDSS(galaxy)
    column = str(band + 'mag')
    print "Column: ", column

    # Get only the brightest sources of both SDSS and Subaru.
    mag = map(lambda source: source[column], sdss)
    max_mag = np.mean(mag) + 0.25*np.mean(np.std(mag))
    sdss = filter(lambda s: phot_utils.mag_cut(s[column], 18, max_mag), sdss)

    with open(scam, 'r') as f:
        catalog = [S.SCAMSource(line) for line in f if phot_utils.no_head(line)]

    mag = map(lambda s: s.mag_best, catalog)
    max_mag = np.mean(mag) + 0.25*np.mean(np.std(mag))
    sources = filter(lambda s: phot_utils.mag_cut(s.mag_best, 18, max_mag), catalog)

    ra = [source.ra for source in catalog]
    dec = [source.dec for source in catalog]
    scam_sources = Q.ScamEquatorialQuadtree(min(ra), min(dec),
                                            max(ra), max(dec))
    map(lambda sources: scam_sources.insert(sources), sources)
    matches = associate(sdss, scam_sources)

    m_scam_sources = map(lambda source: source.mag_aper, matches)
    m_sdss_sources = map(lambda source: source.match2[column], matches)

    # Clip outliers of (m_sdss - m_scam)
    difference = []
    for m_sdss, m_scam in zip(m_sdss_sources, m_scam_sources):
        difference.append(m_sdss - m_scam)
    std =  np.std(difference)

    # Make a region file to check the matching
    makeRegionFile.fromList(matches, band + "_scam_match_source.reg", 0.1, "red")
    makeRegionFile.fromList(matches, band + "_sdss_match_source.reg", 0.1, "green")

    clipped = []
    for entry in matches:
        if entry.match2[column] - entry.mag_aper < std*3:
            clipped.append(entry)

    difference = []
    for entry in clipped:
        difference.append(entry.match2[column] - entry.mag_aper)
    m_scam = map(lambda source: source.mag_aper, clipped)

    # Look at offsets
    plt.plot(difference, m_scam, linestyle='none', marker='o')
    plt.xlabel(r'$m_{SDSS}$ - $m_{SCAM}$', fontsize=20)
    plt.ylabel(r'$m_{SCAM}$', fontsize=20, labelpad=30)
    path = os.getcwd()
    phot_utils.save(path, band + '_zp.png')

    # Take median of offset
    return  np.median(difference)

def main():
    galaxy, scam_catalog, band = sys.argv[1], sys.argv[2], sys.argv[3]
    print "Zeropoint is: ", calcZP(galaxy, scam_catalog, band)

if __name__ == '__main__':
    #calcZP(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit(main())
