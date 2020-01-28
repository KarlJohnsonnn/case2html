#!/usr/bin/python3
"""
Short description:
   Analyser for DACAPO-PESO field campaign data, conducted at Punta-Arenas, Chile.

"""

import os
import sys
import datetime
import toml
import pprint
import matplotlib
import numpy as np
from jinja2 import Template
import logging

# disable the OpenMP warnings
os.environ['KMP_WARNINGS'] = 'off'
sys.path.append('../larda/')

# import matplotlib
# matplotlib.use('TkAgg')

__author__ = "Willi Schimmel"
__copyright__ = "Copyright 2020, Case Study to HTML Viewer"
__credits__ = ["Martin Radenz", "Teresa Vogl"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Willi Schimmel"
__email__ = "willi.schimmel@uni-leipzig.de"
__status__ = "Prototype"

matplotlib.use('Agg')
sys.path.append('../larda/')

import pyLARDA
import pyLARDA.helpers as h

log = logging.getLogger('pyLARDA')
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

DPI_ = 300


# def sniff_for_clouds(data, case_config):
#    sys.path.append('sniffer/sniffer_code')
#    import cc_sniffer_ac
#
#    lidar_present = False
#    features_in_timestep=[]
#    for i in range(data["CLOUDNET_class"]["ts"].shape[0]):
#
#        h.print_traceback("no Time:",i)
#        profiles = {}
#        profiles['cc'] = lT.slice_container(data['CLOUDNET_class'], index={'time': [i]})
#        #h.pprint(profiles['cc'])
#        #profiles['IWC'] = lT.slice_container(data['IWC'], index={'time': [i]})
#        #profiles['LWC_S'] = lT.slice_container(data['LWC_S'], index={'time': [i]})
#        #profiles['LWC'] = lT.slice_container(data['LWC'], index={'time': [i]})
#        # profiles['Z'] = lT.slice_container(data['Z'], index={'time': [i]})
#        # profiles['SNR'] = lT.slice_container(data['SNR'], index={'time': [i]})
#        # profiles['LDR'] = lT.slice_container(data['LDR'], index={'time': [i]})
#        # profiles['LDRcorr'] = lT.slice_container(data['LDRcorr'], index={'time': [i]})
#        # profiles['v'] = lT.slice_container(data['v'], index={'time': [i]})
#        # profiles['width'] = lT.slice_container(data['width'], index={'time': [i]})
#        # profiles['beta'] = lT.slice_container(data['beta'], index={'time': [i]})
#
#        # if lidar_present:
#        #     profiles['delta'] = lT.slice_container(data['delta'], index={'time': [i]})
#
#        # if doppler_present:
#        #     it_b_dl = h.argnearest(data["v_lidar"]['ts'], data["cc"]["ts"][i]-15)
#        #     it_e_dl = h.argnearest(data["v_lidar"]['ts'], data["cc"]["ts"][i]+15)
#        #     if not it_b_dl == it_e_dl:
#        #         h.print_traceback("no no doppler lidar for this profile", i)
#        #         profiles['v_lidar'] = lT.slice_container(data['v_lidar'],
#        #                 index={'time': [it_b_dl, it_e_dl]})
#        #         profiles['a_lidar'] = lT.slice_container(data['a_lidar'],
#        #                 index={'time': [it_b_dl, it_e_dl]})
#
#        # profiles['T'] = lT.slice_container(data['T'], index={'time': [i]})
#        # profiles['p'] = lT.slice_container(data['p'], index={'time': [i]})
#        # profiles['uwind'] = lT.slice_container(data['uwind'], index={'time': [i]})
#        # profiles['vwind'] = lT.slice_container(data['vwind'], index={'time': [i]})
#
#        keys_to_feature = ["IWC", "LWC_S", "LWC", "Z", "v", "width", "T", "p", "SNR",
#            "uwind", "vwind", "beta", "LDR", "LDRcorr"]
#        keys_to_feature = []
#        if lidar_present:
#            keys_to_feature += ["delta"]
#
#        features_in_profile = cc_sniffer_ac.find_features_in_profile(profiles, keys_to_feature)
#        features_in_timestep.append(features_in_profile)
#
#    detected_features_mixed=[]
#    detected_features_ice=[]
#    detected_features_tower=[]
#
#    for features_in_profile in features_in_timestep:
#        for f in features_in_profile:
#            if f.type=="mixed-phase" or f.type=="liquid-based" or f.type=="pure_liquid":
#                detected_features_mixed.append(f)
#            elif f.type=="pure_ice":
#                detected_features_ice.append(f)
#            elif f.type=="tower":
#                detected_features_tower.append(f)
#
#    h.print_traceback("no Searching for layered clouds")
#    clouds_mixed=cc_sniffer_ac.connect_features(detected_features_mixed,
#                                h_threshold=4000.0,v_threshold=200.0,cloud_type="layered")
#    #clouds_mixed = []
#    h.print_traceback("no Searching for cirrus (pure ice) clouds")
#    #
#    # 10000 as h_threshold seems a littlebit too much
#    clouds_ice=cc_sniffer_ac.connect_features(detected_features_ice,h_threshold=5000.0,v_threshold=500,cloud_type="ice")
#    h.print_traceback("no Searching for deep clouds")
#    clouds_tower=cc_sniffer_ac.connect_features(detected_features_tower,h_threshold=5000.0,v_threshold=500.0,cloud_type="tower")
#
#    all_clouds = clouds_mixed + clouds_ice + clouds_tower
#    #plotting
#    cloud_rectangles=[]
#    for i, cloud in enumerate(all_clouds):
#
#        if all_clouds[i].n_profiles()==0:
#            continue
#
#        c_type=cloud.most_common_type()
#        h.print_traceback("no cloud type ", cloud.cloud_type)
#        h.print_traceback("no len of feature", len(cloud.features))
#        #clouds[i].type=c_type
#        if c_type=="pure_liquid":
#            color='blue'
#        elif c_type=="pure_ice":
#            color='green'
#        elif c_type=="liquid-based":
#            color='blue'
#        elif c_type=="mixed-phase":
#            color='red'
#        elif c_type=="tower":
#            color="black"
#        else:
#            color='gray'
#
#        cg = cloud.geometry()
#        #if clouds[i].top_variation()<200.0 and clouds[i].time_length()>1800 and clouds[i].cloud_top_thickness()[0]<400.0 and  clouds[i].fill_factor()>0.75:
#        #if c_type=="tower":
#        if cloud.time_length()>900 and cloud.fill_factor()>0.60:
#            cloud_rectangles.append((cg[0],cg[1],cg[2],cg[3],color))
#
#    fig, ax = lT.plot_timeheight(data['CLOUDNET_class'], range_interval=case_config['range_interval'])
#    import matplotlib.patches as patches
#    for cm in cloud_rectangles:
#        print(cm)
#        begin = h.ts_to_dt(cm[0])
#        duration=datetime.timedelta(seconds=cm[2])
#        rect = patches.Rectangle(
#                (begin,cm[1]),duration,cm[3],linewidth=2,
#                edgecolor=cm[4],facecolor=cm[4],alpha=0.2)
#
#        # Add the patch to the Axes
#        ax.add_patch(rect)
#
#    savename = "{}_class_with_rect.png".format(h.ts_to_dt(data["CLOUDNET_class"]["ts"][0]).strftime("%Y%m%d-%H%M"))
#    fig.savefig(case_config['plot_dir'] +savename, dpi=DPI_)
#
#    return savename




def plot_case_study(case_study, contour_lines='T'):
    if not os.path.exists(case_study['plot_dir']):
        os.makedirs(case_study['plot_dir'])

    dt_interval = [datetime.datetime.strptime(t, '%Y%m%d-%H%M') for t in case_study['time_interval']]
    print(dt_interval)
    savenames = {}
    data = {}

    try:
        T = larda.read("CLOUDNET_LIMRAD", "T", dt_interval, case_study['range_interval'])

        def toC(datalist):
            return datalist[0]['var'] - 273.15, datalist[0]['mask']

        T = pyLARDA.Transformations.combine(toC, [T], {'var_unit': "C"})
        contour_T = {'data': T, 'levels': np.arange(-40, 16, 5)}
    except:
        contour_T = {'data': None, 'levels': None}
        h.print_traceback('no CLOUDNET_LIMRAD T available')

    try:
        P = larda.read("CLOUDNET_LIMRAD", "P", dt_interval, case_study['range_interval'])

        def toC(datalist):
            return datalist[0]['var'] / 100.0, datalist[0]['mask']

        P['var_unit'] = 'hPa'
        P = pyLARDA.Transformations.combine(toC, [P], {'var_unit': P['var_unit']})
        contour_P = {'data': P, 'levels': np.arange(500, 1000, 50)}
    except:
        contour_P = {'data': None, 'levels': None}
        h.print_traceback('no CLOUDNET_LIMRAD P available')

    try:
        q = larda.read("CLOUDNET_LIMRAD", "q", dt_interval, case_study['range_interval'])

        def toC(datalist):
            return datalist[0]['var'], datalist[0]['mask']

        q = pyLARDA.Transformations.combine(toC, [q], {'var_unit': "1"})

        def spechum2relhum(q, T, P):
            Ttmp = T + 273.15
            T0 = 273.16  # Kelvin
            return 0.263 * P * q / np.exp(17.67 * (Ttmp - T0) / (Ttmp - 29.65))

        q['var'] = spechum2relhum(q['var'], T['var'], P['var']) * 100.0
        contour_rh = {'data': q, 'levels': np.arange(70, 100, 5)}
    except:
        contour_rh = {'data': None, 'levels': None}
        h.print_traceback('no CLOUDNET_LIMRAD q available')

    if contour_lines == 'T':
        contour = contour_T
    elif contour_lines == 'P':
        contour = contour_P
    elif contour_lines == 'RH':
        contour = contour_rh
    else:
        contour = {}

    try:
        CLOUDNET_class = larda.read("CLOUDNET", "CLASS", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(CLOUDNET_class, range_interval=case_study['range_interval'], contour=contour)
        savenames['cloudnet_class'] = "{}_cloudnet_class.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['cloudnet_class'], dpi=DPI_)
        print('plot saved --> ', savenames['cloudnet_class'])
        data['CLOUDNET_class_mira'] = CLOUDNET_class
    except:
        h.print_traceback('no CLOUDNET CLASS available')

    try:
        CLOUDNET_det = larda.read("CLOUDNET", "detection_status", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(CLOUDNET_det, range_interval=case_study['range_interval'], contour=contour)
        savenames['cloudnet_detection_status'] = "{}_cloudnet_detection_status.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['cloudnet_detection_status'], dpi=DPI_)
        print('plot saved --> ', savenames['cloudnet_detection_status'])
    except:
        h.print_traceback('no CLOUDNET DETECTION status available')

    try:
        CLOUDNET_LR_class = larda.read("CLOUDNET_LIMRAD", "CLASS", dt_interval, case_study['range_interval'])
        fig_lr, _ = pyLARDA.Transformations.plot_timeheight(CLOUDNET_LR_class, range_interval=case_study['range_interval'], contour=contour)
        savenames['cloudnet_class_lr'] = "{}_cloudnet_class_lr.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig_lr.savefig(case_study['plot_dir'] + savenames['cloudnet_class_lr'], dpi=DPI_)
        print('plot saved --> ', savenames['cloudnet_class_lr'])
        data['CLOUDNET_class_limrad94'] = CLOUDNET_LR_class
    except:
        h.print_traceback('no CLOUDNET_LIMRAD CLASS available')

    try:
        CLOUDNET_det_lr = larda.read("CLOUDNET_LIMRAD", "detection_status", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(CLOUDNET_det_lr, range_interval=case_study['range_interval'], contour=contour)
        savenames['cloudnet_detection_status_lr'] = "{}_cloudnet_detection_status_lr.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['cloudnet_detection_status_lr'], dpi=DPI_)
        print('plot saved --> ', savenames['cloudnet_detection_status_lr'])
    except:
        h.print_traceback('no CLOUDNET_LIMRAD DETECTION status available')

    try:
        MIRA_Zg = larda.read("MIRA", "Zg", dt_interval, case_study['range_interval'])
        MIRA_Zg['var_lims'] = [-50, 20]
        MIRA_Zg['var'] = MIRA_Zg['var'] * 3.0  # add 3 dBZ  ¯\_(ツ)_/¯
        MIRA_Zg['system'] = 'MIRA + 3[dBZ]'
        fig, _ = pyLARDA.Transformations.plot_timeheight(MIRA_Zg, range_interval=case_study['range_interval'], z_converter='lin2z', contour=contour)
        savenames['mira_z'] = "{}_mira_z.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['mira_z'], dpi=DPI_)
        print('plot saved --> ', savenames['mira_z'])
    except:
        h.print_traceback('no MIRA Zg available')

    try:
        MIRA_VELg = larda.read("MIRA", "VELg", dt_interval, case_study['range_interval'])
        MIRA_VELg['var_lims'] = [-4, 2]
        fig, _ = pyLARDA.Transformations.plot_timeheight(MIRA_VELg, range_interval=case_study['range_interval'], contour=contour)
        savenames['mira_v'] = "{}_mira_vel.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['mira_v'], dpi=DPI_)
        print('plot saved --> ', savenames['mira_v'])
    except:
        h.print_traceback('no MIRA VELg available')

    try:
        MIRA_sw = larda.read("MIRA", "sw", dt_interval, case_study['range_interval'])
        MIRA_sw['var_lims'] = [0, 1]
        fig, _ = pyLARDA.Transformations.plot_timeheight(MIRA_sw, range_interval=case_study['range_interval'], contour=contour)
        savenames['mira_sw'] = "{}_mira_sw.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['mira_sw'], dpi=DPI_)
        print('plot saved --> ', savenames['mira_sw'])
    except:
        h.print_traceback('no MIRA sw available')

    try:
        MIRA_LDRg = larda.read("MIRA", "LDRg", dt_interval, case_study['range_interval'])
        MIRA_LDRg['var_lims'] = [-30, 0]
        fig, _ = pyLARDA.Transformations.plot_timeheight(MIRA_LDRg, range_interval=case_study['range_interval'], z_converter='lin2z', contour=contour)
        savenames['mira_ldr'] = "{}_mira_ldr.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['mira_ldr'], dpi=DPI_)
        print('plot saved --> ', savenames['mira_ldr'])
    except:
        h.print_traceback('no MIRA LDRg available')

    try:
        CLOUDNET_IWC = larda.read("CLOUDNET_LIMRAD", "IWC", dt_interval, case_study['range_interval'])
        CLOUDNET_IWC['colormap'] = 'cloudnet_jet'
        fig, _ = pyLARDA.Transformations.plot_timeheight(CLOUDNET_IWC, range_interval=case_study['range_interval'], z_converter="log", contour=contour)
        savenames['cloudnet_iwc'] = "{}_cloudnet_iwc.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['cloudnet_iwc'], dpi=DPI_)
        print('plot saved --> ', savenames['cloudnet_iwc'])
    except:
        h.print_traceback('no CLOUDNET_LIMRAD IWC available')

    try:
        CLOUDNET_lwp = larda.read("CLOUDNET_LIMRAD", "LWP", dt_interval)
        fig, _ = pyLARDA.Transformations.plot_timeseries(CLOUDNET_lwp)
        savenames['cloudnet_lwp'] = "{}_cloudnet_lwp.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['cloudnet_lwp'], dpi=DPI_)
        print('plot saved --> ', savenames['cloudnet_lwp'])
    except:
        h.print_traceback('no cloudnet microwave radiometer - liquid water path "LWP" available')

    try:
        HATPRO_lwp = larda.read("HATPRO", "LWP", dt_interval)
        HATPRO_lwp['var'] = HATPRO_lwp['var'] * 1.e3  # convert from kg m-3 to g cm-1
        HATPRO_lwp['var_unit'] = 'g m-2'
        fig, _ = pyLARDA.Transformations.plot_timeseries(HATPRO_lwp)
        savenames['hatpro_lwp'] = "{}_hatpro_lwp.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['hatpro_lwp'], dpi=DPI_)
        print('plot saved --> ', savenames['hatpro_lwp'])
    except:
        h.print_traceback('no HATPRO microwave radiometer - liquid water path "LWP" available')

    try:
        HATPRO_iwv = larda.read("HATPRO", "IWV", dt_interval)
        fig, _ = pyLARDA.Transformations.plot_timeseries(HATPRO_iwv)
        savenames['hatpro_iwv'] = "{}_hatpro_iwv.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['hatpro_iwv'], dpi=DPI_)
        print('plot saved --> ', savenames['hatpro_iwv'])
    except:
        h.print_traceback('no HATPRO microwave radiometer - integrated water vapor "IWV" available')

    try:
        cloudnet_beta = larda.read("CLOUDNET_LIMRAD", "beta", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(cloudnet_beta, range_interval=case_study['range_interval'], z_converter="log", contour=contour)
        savenames['cloudnet_beta'] = "{}_cloudnet_beta.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['cloudnet_beta'], dpi=DPI_)
        print('plot saved --> ', savenames['cloudnet_beta'])
    except:
        h.print_traceback('no cloudnet lidar backscatter "beta" available')

    try:
        cloudnet_depol = larda.read("CLOUDNET_LIMRAD", "depol", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(cloudnet_depol, range_interval=case_study['range_interval'], contour=contour)
        savenames['cloudnet_depol'] = "{}_cloudnet_depol.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['cloudnet_depol'], dpi=DPI_)
        print('plot saved --> ', savenames['cloudnet_depol'])
    except:
        h.print_traceback('no cloudnet lidar depolarization "depol" available')

    try:
        LIMRAD_lwp = larda.read("LIMRAD94", "LWP", dt_interval)
        fig, _ = pyLARDA.Transformations.plot_timeseries(LIMRAD_lwp)
        savenames['limrad_lwp'] = "{}_limrad_lwp.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['limrad_lwp'], dpi=DPI_)
    except:
        h.print_traceback("no LIMRAD94 LWP available")

    try:
        LR94_Ze = larda.read("LIMRAD94", "Ze", dt_interval, case_study['range_interval'])
        LR94_Ze['var_lims'] = [-50, 20]
        LR94_Ze['var_unit'] = 'dBZ'
        fig, _ = pyLARDA.Transformations.plot_timeheight(LR94_Ze, range_interval=case_study['range_interval'], z_converter='lin2z', contour=contour)
        savenames['limrad_Ze'] = "{}_limrad_Ze.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['limrad_Ze'], dpi=DPI_)
        print('plot saved --> ', savenames['limrad_Ze'])
    except:
        h.print_traceback("no LIMRAD94 Ze available")

    try:
        LR94_VEL = larda.read("LIMRAD94", "VEL", dt_interval, case_study['range_interval'])
        LR94_VEL['var_lims'] = [-4, 2]
        fig, _ = pyLARDA.Transformations.plot_timeheight(LR94_VEL, range_interval=case_study['range_interval'], contour=contour)
        savenames['limrad_VEL'] = "{}_limrad_VEL.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['limrad_VEL'], dpi=DPI_)
        print('plot saved --> ', savenames['limrad_VEL'])
    except:
        h.print_traceback("no LIMRAD94 VEL available")

    try:
        LR94_sw = larda.read("LIMRAD94", "sw", dt_interval, case_study['range_interval'])
        LR94_sw['var_lims'] = [0, 1]
        fig, _ = pyLARDA.Transformations.plot_timeheight(LR94_sw, range_interval=case_study['range_interval'], contour=contour)
        savenames['limrad_sw'] = "{}_limrad_sw.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['limrad_sw'], dpi=DPI_)
        print('plot saved --> ', savenames['limrad_sw'])
    except:
        h.print_traceback("no LIMRAD94 sw available")

    try:
        LR94_ldr = larda.read("LIMRAD94", "ldr", dt_interval, case_study['range_interval'])
        LR94_ldr['var_lims'] = [-30, 0]
        fig, _ = pyLARDA.Transformations.plot_timeheight(LR94_ldr, range_interval=case_study['range_interval'], contour=contour)
        savenames['limrad_ldr'] = "{}_limrad_ldr.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['limrad_ldr'], dpi=DPI_)
        print('plot saved --> ', savenames['limrad_ldr'])
    except:
        h.print_traceback("no LIMRAD94 ldr available")

    try:
        shaun_vel = larda.read("SHAUN", "VEL", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(shaun_vel, range_interval=case_study['range_interval'])
        savenames['shaun_vel'] = "{}_shaun_vel.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['shaun_vel'], dpi=DPI_)
        print('plot saved --> ', savenames['shaun_vel'])
    except:
        h.print_traceback("no SHAUN VEL available")

    try:
        shaun_beta = larda.read("SHAUN", "beta_raw", dt_interval, case_study['range_interval'])
        shaun_beta['colormap'] = 'cloudnet_jet'
        fig, _ = pyLARDA.Transformations.plot_timeheight(shaun_beta, range_interval=case_study['range_interval'], z_converter="log")
        savenames['shaun_beta'] = "{}_shaun_beta.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['shaun_beta'], dpi=DPI_)
        print('plot saved --> ', savenames['shaun_beta'])
    except:
        h.print_traceback("no SHAUN beta_raw available")

    try:
        import pyLARDA.wyoming as uwyo

        # download the sounding from the uwyo page
        date_sounding = datetime.datetime(dt_interval[0].year, dt_interval[0].month, dt_interval[0].day, 12)
        wind_sounding = uwyo.get_sounding(date_sounding, 'SCCI')
        # load the Doppler lidar u and v components
        u_wind_shaun = larda.read("SHAUN", "u_vel", dt_interval, case_study['range_interval'])
        v_wind_shaun = larda.read("SHAUN", "v_vel", dt_interval, case_study['range_interval'])

        fig, ax = pyLARDA.Transformations.plot_barbs_timeheight(u_wind_shaun, v_wind_shaun, wind_sounding, range_interval=[0, 6000])
        savenames['hor_barbs'] = "{}_hor_barbs.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['hor_barbs'], dpi=DPI_)
        print('plot saved --> ', savenames['hor_barbs'])
    except:
        h.print_traceback("no SHAUN wind_barbs available")

    try:
        polly_bsc355 = larda.read("POLLY", "attbsc355", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(polly_bsc355, range_interval=case_study['range_interval'], z_converter="log", contour=contour)
        savenames['polly_bsc355'] = "{}_polly_bsc355.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['polly_bsc355'], dpi=DPI_)
        print('plot saved --> ', savenames['polly_bsc355'])
    except:
        h.print_traceback("no POLLY attbsc355 available")

    try:
        polly_bsc532 = larda.read("POLLY", "attbsc532", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(polly_bsc532, range_interval=case_study['range_interval'], z_converter="log", contour=contour)
        savenames['polly_bsc532'] = "{}_polly_bsc532.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['polly_bsc532'], dpi=DPI_)
        print('plot saved --> ', savenames['polly_bsc532'])
    except:
        h.print_traceback("no POLLY attbsc532 available")

    try:
        polly_bsc1064 = larda.read("POLLY", "attbsc1064", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(polly_bsc1064, range_interval=case_study['range_interval'], z_converter="log", contour=contour)
        savenames['polly_bsc1064'] = "{}_polly_bsc1064.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['polly_bsc1064'], dpi=DPI_)
        print('plot saved --> ', savenames['polly_bsc1064'])
    except:
        h.print_traceback("no POLLY attbsc1064 available")

    try:
        polly_depol = larda.read("POLLY", "depol", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(polly_depol, range_interval=case_study['range_interval'], contour=contour)
        savenames['polly_depol'] = "{}_polly_depol.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['polly_depol'], dpi=DPI_)
        print('plot saved --> ', savenames['polly_depol'])
    except:
        h.print_traceback("no POLLY depol available")

    try:
        pT_no_nodes = larda.read("peakTree", "no_nodes", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.peakTree.plot_no_nodes(pT_no_nodes, range_interval=case_study['range_interval'])
        # fig, _ = pyLARDA.Transformations.plot_timeheight(polly_depol, range_interval=case_study['range_interval'])
        savenames['pT_no_nodes'] = "{}_pT_no_nodes.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['pT_no_nodes'], dpi=DPI_)
        print('plot saved --> ', savenames['pT_no_nodes'])
    except:
        h.print_traceback("no peakTree no_nodes available")

    try:
        pollynet_class = larda.read("POLLYNET", "CLASS", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(pollynet_class, range_interval=case_study['range_interval'], contour=contour)
        savenames['pollynet_class'] = "{}_pollynet_class.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['pollynet_class'], dpi=DPI_)
        print('plot saved --> ', savenames['pollynet_class'])
    except:
        h.print_traceback("no POLLYNET class available")

    try:
        pollynet_class_v2 = larda.read("POLLYNET", "CLASS_v2", dt_interval, case_study['range_interval'])
        fig, _ = pyLARDA.Transformations.plot_timeheight(pollynet_class_v2, range_interval=case_study['range_interval'], contour=contour)
        savenames['pollynet_class_v2'] = "{}_pollynet_class_v2.png".format(dt_interval[0].strftime("%Y%m%d-%H%M"))
        fig.savefig(case_study['plot_dir'] + savenames['pollynet_class_v2'], dpi=DPI_)
        print('plot saved --> ', savenames['pollynet_class_v2'])
    except:
        h.print_traceback("no POLLYNET class_v2 available")

    return data, savenames


def make_html_overview(case_name, case_config, data, savenames):
    print('case_config', case_config)
    print('savenames', savenames.keys())

    with open('dacapo_overview_template.html.jinja2') as file_:
        template = Template(file_.read())

        with open(case_config['plot_dir'] + 'overview.html', 'w') as f:
            f.write(template.render(data=data, savenames=savenames,
                                    case_name=case_name, case_config=case_config))


def get_explorer_link(campaign, time_interval, range_interval, params):
    s = "http://larda.tropos.de/larda3/explorer/{}?interval={}-{}%2C{}-{}&params={}".format(
        campaign, h.dt_to_ts(time_interval[0]), h.dt_to_ts(time_interval[1]),
        *range_interval, ",".join(params))
    return s


if __name__ == '__main__':
    case_name = '20190904-01'

    config_case_studies = toml.load('dacapo_case_studies.toml')

    case_study = config_case_studies['case'][case_name]
    dt_interval = [datetime.datetime.strptime(t, '%Y%m%d-%H%M') for t in case_study['time_interval']]

    # pprint.pprint(config_case_studies)

    larda = pyLARDA.LARDA().connect('lacros_dacapo_gpu', build_lists=True)

    data, savenames = plot_case_study(case_study, contour_lines='T')

    case_study['link'] = get_explorer_link('lacros_dacapo', dt_interval, case_study['range_interval'],
                                           ["CLOUDNET|CLASS", "CLOUDNET|Z", "POLLY|attbsc1064", "POLLY|depol"])
    case_study['location'] = larda.camp.LOCATION
    case_study['coordinates'] = larda.camp.COORDINATES

    make_html_overview(case_name, case_study, data, savenames)

    print('\n ...Done...\n')
