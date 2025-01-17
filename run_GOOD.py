#!/usr/bin/env python
# coding:utf-8

################################################################################
# Import Python modules
import os, sys, pydoc
import platform

__author__ = 'Feng Zhou @ SDUST'
__date__ = '$DatD: 2022-04-06 07:05:20 (Mon, 06 Apr 2022) $'[7:-21]
__version__ = '$Version: run_GOOD.py V2.0 $'[10:-2]


################################################################################
# FUNCTION: write configuration file for GOOD software
################################################################################
def main_run_GOOD(args):

    cfgFile = os.path.join(args.mainDir,'gamp_GOOD.cfg')
    with open(cfgFile,"w") as f_w:
        line = ''
        line += '# GAMP II - GOOD (Gnss Observations and prOducts Downloader) options, vers. 2.0\n'
        line += '\n'

        line += '# The directories of GNSS observations and products  ---------------------------\n'
        # to write the setting of main directory
        line += 'mainDir           = ' + args.mainDir + '                      % The root/main directory of GNSS observations and products\n'
        
        # to write the setting of sub-directories
        line += '  obsDir          = 0  obs                       % The sub-directory of RINEX format observation files\n'
        line += '  navDir          = 0  nav                       % The sub-directory of RINEX format broadcast ephemeris files\n'
        line += '  orbDir          = 0  orb                       % The sub-directory of SP3 format precise ephemeris files\n'
        line += '  clkDir          = 0  clk                       % The sub-directory of RINEX format precise clock files\n'
        line += '  eopDir          = 0  eop                       % The sub-directory of earth rotation/orientation parameter (EOP) files\n'
        line += '  obxDir          = 0  obx                       % The sub-directory of MGEX final/rapid and/or CNES real-time ORBEX (ORBit EXchange format) files\n'
        line += '  biaDir          = 0  bia                       % The sub-directory of CODE/MGEX differential code/signal bias (DCB/DSB), MGEX observable-specific \n'
        line += '                                                 %   signal bias (OSB), and/or CNES real-time OSB files\n'
        line += '  snxDir          = 0  snx                       % The sub-directory of SINEX format IGS weekly solution files\n'
        line += '  ionDir          = 0  ion                       % The sub-directory of CODE/IGS global ionosphere map (GIM) files\n'
        line += '  ztdDir          = 0  ztd                       % The sub-directory of CODE/IGS tropospheric product files\n'
        line += '  tblDir          = 0  tables                    % The sub-directory of table files (i.e., ANTEX, ocean tide loading files, etc.) for processing\n'

        # to write the setting of log file
        line += '\n'
        line += '# The directory of log files ---------------------------------------------------\n'
        line += 'logFile           = 1  ' + os.path.join(args.mainDir,'log','log.txt') + '       % The log file with full path that gives the indications of whether the data downloading is successful or not\n'

        line += '\n'
        line += '# The directory of third-party softwares ---------------------------------------\n'
        line += '3partyDir         = 1  ' + os.path.join(args.mainDir,'thirdParty') + '        % (optional) The directory where third-party softwares (i.e., \'wget\', \'gzip\', \'crx2rnx\' etc) are stored, \n'

        # required time argument
        # ctime = f'{args.time[0]} {args.time[1]} {args.time[2]}' # explicitly construct string
        ctime = ' '.join([str(v) for v in args.time]) # use a loop to build string 
        
        line += '\n'
        line += '# Time settings ----------------------------------------------------------------\n'
        line += 'procTime          = 2  ' + ctime + '               % The setting of start time for processing\n'

        line += '\n'
        line += '# Settings of FTP downloading --------------------------------------------------\n'
        line += 'minusAdd1day      = 1                            % The setting of the day before and after the current day for precise satellite orbit and clock \n'
        line += '                                                 %   products downloading\n'
        line += 'printInfoWget     = 1                            % Printing the information generated by \'wget\'\n'

        # required ftp argument
        line += '\n'
        line += '# Handling of FTP downloading --------------------------------------------------\n'
        line += 'ftpDownloading    = 1  ' + args.ftp + '                     % The setting of the master switch for data downloading\n'

        # optional arguments
        if args.obs:
            cobs = ' '.join([str(v) for v in args.obs])
            line += '  getObs          = 1  ' + cobs + '    % GNSS observation data downloading option\n'
        if args.nav:
            cnav = ' '.join([str(v) for v in args.nav])
            line += '  getNav          = 1  ' + cnav + ' % Various broadcast ephemeris downloading option\n'
        if args.orbclk:
            corb = ' '.join([str(v) for v in args.orbclk])
            line += '  getOrbClk       = 1  ' + corb + '                % Satellite final/rapid/ultra-rapid precise orbit and clock downloading option\n'
        if args.eop:
            ceop = ' '.join([str(v) for v in args.eop])
            line += '  getEop          = 1  ' + ceop + '                % Earth rotation/orientation parameter (ERP/EOP) downloading option\n'
        if args.obx:
            line += '  getObx          = 1  ' + args.obx + '                     % ORBEX (ORBit EXchange format) for satellite attitude information downloading option\n'
        if args.dsb:
            line += '  getDsb          = 1  ' + args.dsb + '                       % Differential code/signal bias (DCB/DSB) downloading option\n'
        if args.snx:
            line += '  getSnx          = 1                                 % IGS weekly SINEX downloading option\n'
        if args.ion:
            line += '  getIon          = 1  ' + args.ion + '                       % Global ionosphere map (GIM) downloading option\n'
        if args.roti:
            line += '  getRoti         = 1                            % Rate of TEC index (ROTI) downloading option\n'
        if args.trop:
            if args.trop[0] == 'all':
                ctrop = ' '.join([str(v) for v in args.trop])
            else:
                ctrop = args.trop[0] + '  ' + os.path.join(args.mainDir,args.trop[1])
            line += '  getTrp          = 1  ' + ctrop + '                  % CODE/IGS tropospheric product downloading option\n'
        if args.atx:
            line += '  getAtx          = 1                            % ANTEX format antenna phase center correction downloading option\n'

        f_w.write(line)

    if 'Windows' in platform.system():
        bin_GOOD = os.path.join(args.mainDir, 'run_GAMP_GOOD.exe')
    elif 'Linux' or 'Mac' in platform.system():
        bin_GOOD = os.path.join(args.mainDir, 'run_GAMP_GOOD')
    cmd = bin_GOOD + ' ' + cfgFile
    os.system(cmd)

################################################################################
# Main program
################################################################################
if __name__ == '__main__':
    import argparse
    import textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description='write configuration for GOOD and execute',
        epilog=textwrap.dedent('''\
            Additional detail for arguments:

                -obs DATA_TYPE SOURCE SITE_LIST START_HOUR NHOURS
                    DATA_TYPE: daily, hourly, highrate, 30s, 5s, 1s
                    SOURCE: igs, mgex, igm, cut, ga, hk, ngs, epn, pbo2, pbo3, pbo5
                    SITE_LIST: all (observation files downloaded in the whole remote directory), or the full path of 
                        site list (observation files downloaded site-by-site according to the site list file)
                    START_HOUR: Start hour (00, 01, 02, ...)
                    NHOURS: the consecutive hours, i.e., '01  3' denotes 01, 02, and 03

                -nav DATA_TYPE NAV_TYPE SOURCE START_HOUR NHOURS
                    DATA_TYPE: daily, hourly
                    NAV_TYPE: gps, glo, bds, gal, qzs, irn, mixed3, mixed4, all
                    SOURCE: igs, dlr, ign, gop, wrd
                    START_HOUR: Start hour (00, 01, 02, ...)
                    NHOURS: the consecutive hours, i.e., '01  3' denotes 01, 02, and 03
            
            NEED TO ADD TO ADDITIONAL DETAILED HELP:
            -orbclk, -eop, -ion, -trop

            EXAMPLES:

            download 3 consecutive days of IGS station observations from CDDIS,
            starting day-of-year 32, year 2022
                python run_GOOD.py -dir_main D:\data -time 2022 32 3 -ftp cddis -obs daily igs site_igs.list 0 24

            download SINEX, ROTI, and ANTEX from Wuhan
                python run_GOOD.py -dir_main D:\data -time 2022 32 3 -ftp whu -snx -roti -atx
        '''
        ))

    parser.add_argument('-mainDir',required=True,
        help='The root/main directory of GNSS observations and products storage')
    parser.add_argument('-time',required=True,
        type=int, nargs=3, metavar=('YYYY','DOY','NUM_DAYS'),
        help='time setting, see examples')
    parser.add_argument('-ftp',required=True,
        choices=('cddis','whu','ign'),
        help='FTP archive')
    parser.add_argument('-obs', nargs=5, 
        metavar=('DATA_TYPE','SOURCE','SITE_LIST','START_HOUR','NHOURS'),
        help='GNSS observation data downloading')
    parser.add_argument('-nav', nargs=5,
        metavar=('DATA_TYPE','NAV_TYPE', 'SOURCE','START_HOUR','NHOURS'),
        help='various broadcast ephemeris downloading')
    parser.add_argument('-orbclk', nargs=3,
        metavar=('SOURCE','START_HOUR','NHOURS'),
        help='satellite final/rapid/ultra-rapid precise orbit and clock downloading')
    parser.add_argument('-eop', nargs=3,
        metavar=('SOURCE','START_HOUR','NHOURS'),
        help='Earth rotation/orientation parameter (ERP/EOP) downloading')
    parser.add_argument('-obx',
        help='ORBEX (ORBit EXchange format) for satellite attitude information downloading: ' +
        'final/rapid = cod_m, gfz_m, grg_m, whu_m, all_m; real-time = cnt')
    parser.add_argument('-dsb',
        help='Differential code/signal bias (DCB/DSB) downloading',
        choices=('cod','cas','all'))
    parser.add_argument('-snx', action='store_true',
        help='IGS weekly SINEX downloading option')
    parser.add_argument('-ion',
        help='Global ionosphere map (GIM) downloading')
    parser.add_argument('-roti', action='store_true',
        help='Rate of TEC index (ROTI) downloading')
    parser.add_argument('-trop', nargs=2,
        metavar=('SOURCE','SITE_LIST'),
        help='CODE/IGS tropospheric product downloading')
    parser.add_argument('-atx', action='store_true',
        help='ANTEX format antenna phase center correction downloading')

    args = parser.parse_args()
    #print(args.__dict__)

    main_run_GOOD(args)