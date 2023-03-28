import numpy as np
import pandas as pd
from astropy.utils.data import get_pkg_data_filename
from pathlib import Path
from seppy.loader.psp import psp_isois_load
from seppy.loader.soho import soho_load
from seppy.loader.stereo import stereo_load
from seppy.loader.wind import wind3dp_load


def test_psp_load_online():
    df, meta = psp_isois_load(dataset='PSP_ISOIS-EPIHI_L2-HET-RATES60', startdate="2021/05/31",
                              enddate="2021/06/01", path=None, resample="1min")
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (48, 136)
    assert meta['H_ENERGY_LABL'][0][0] == '  6.7 -   8.0 MeV'
    # Check that fillvals are replaced by NaN
    assert np.sum(np.isnan(df['B_H_Uncertainty_14'])) == 48


def test_psp_load_offline():
    fullpath = get_pkg_data_filename('data/test/psp_isois-epihi_l2-het-rates60_20210531_v15.cdf', package='seppy')
    path = Path(fullpath).parent.as_posix()
    df, meta = psp_isois_load(dataset='PSP_ISOIS-EPIHI_L2-HET-RATES60', startdate="2021/05/31",
                              enddate="2021/06/01", path=path, resample="1min")
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (48, 136)
    assert meta['H_ENERGY_LABL'][0][0] == '  6.7 -   8.0 MeV'
    # Check that fillvals are replaced by NaN
    assert np.sum(np.isnan(df['B_H_Uncertainty_14'])) == 48


def test_soho_ephin_load_online():
    df, meta = soho_load(dataset='SOHO_COSTEP-EPHIN_L2-1MIN', startdate="2021/04/16", enddate="2021/04/16",
                           path=None, resample="1min", pos_timestamp=None)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1145, 14)
    assert meta['E1300'] == '0.67 - 10.4 MeV'
    # Check that fillvals are replaced by NaN
    assert np.sum(np.isnan(df['E1300'])) == 444


def test_soho_ephin_load_offline():
    fullpath = get_pkg_data_filename('data/test/epi21106.rl2', package='seppy')
    path = Path(fullpath).parent.as_posix()
    df, meta = soho_load(dataset='SOHO_COSTEP-EPHIN_L2-1MIN', startdate="2021/04/16", enddate="2021/04/16",
                           path=path, resample="1min", pos_timestamp=None)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1145, 14)
    assert meta['E1300'] == '0.67 - 10.4 MeV'
    # Check that fillvals are replaced by NaN
    assert np.sum(np.isnan(df['E1300'])) == 444


def test_stereo_het_load_online():
    df, meta = stereo_load(instrument="HET", startdate="2021/10/28", enddate="2021/10/29",
                           path=None, resample="1min", pos_timestamp=None)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1440, 28)
    assert meta['Proton_Bins_Text'][0][0] == '13.6 - 15.1 MeV '
    assert np.sum(np.isnan(df['Electron_Flux_0'])) == 0


def test_stereo_het_load_offline():
    fullpath = get_pkg_data_filename('data/test/sta_l1_het_20211028_v01.cdf', package='seppy')
    path = Path(fullpath).parent.as_posix()
    df, meta = stereo_load(instrument="HET", startdate="2021/10/28", enddate="2021/10/29",
                           path=path, resample="1min", pos_timestamp=None)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1440, 28)
    assert meta['Proton_Bins_Text'][0][0] == '13.6 - 15.1 MeV '
    assert np.sum(np.isnan(df['Electron_Flux_0'])) == 0


def test_stereo_sept_load_online():
    df, meta = stereo_load(instrument="SEPT", startdate="2006/11/14", enddate="2006/11/14",
                           path=None, resample="1min", pos_timestamp=None)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (371, 30)
    assert meta.ch_strings[meta.index==2].values[0] == '45.0-55.0 keV'
    # Check that fillvals are replaced by NaN
    assert np.sum(np.isnan(df['ch_2'])) == 371


def test_stereo_sept_load_offline():
    fullpath = get_pkg_data_filename('data/test/sept_ahead_ele_sun_2006_318_1min_l2_v03.dat', package='seppy')
    path = Path(fullpath).parent.as_posix()
    df, meta = stereo_load(instrument="SEPT", startdate="2006/11/14", enddate="2006/11/14",
                           path=path, resample="1min", pos_timestamp=None)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (371, 30)
    assert meta.ch_strings[meta.index==2].values[0] == '45.0-55.0 keV'
    # Check that fillvals are replaced by NaN
    assert np.sum(np.isnan(df['ch_2'])) == 371


def test_wind3dp_load_online():
    df, meta = wind3dp_load(dataset="WI_SFPD_3DP",
                            startdate="2021/04/16",
                            enddate="2021/04/18",
                            resample='1min',
                            multi_index=True,
                            path=None)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2880, 76)
    assert meta['FLUX_LABELS'][0][0] == 'ElecNoFlux_Ch1_Often~27keV '
    # Check that fillvals are replaced by NaN
    assert np.sum(np.isnan(df['FLUX_E0', 'FLUX_E0_P0'])) == 169


def test_wind3dp_load_offline():
    fullpath = get_pkg_data_filename('data/test/wi_sfsp_3dp_20200213_v01.cdf', package='seppy')
    path = Path(fullpath).parent.as_posix()
    df, meta = wind3dp_load(dataset="WI_SFSP_3DP",
                            startdate="2020/02/13",
                            enddate="2020/02/14",
                            resample=None,
                            multi_index=False,
                            path=path)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (897, 15)
    assert meta['FLUX_LABELS'][0][0] == 'ElecNoFlux_Ch1_Often~27keV '
    # Check that fillvals are replaced by NaN
    assert np.sum(np.isnan(df['FLUX_0'])) == 352
