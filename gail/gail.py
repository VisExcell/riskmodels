import numpy as np

class GailRiskCalculator:
    NumCovPattInGailModel = 216

    def __init__(self):
        self.bet2 = np.zeros((8,12),dtype=np.float64)
        self.bet = np.zeros(8,dtype=np.float64)

        self.rf = np.zeros(2,dtype=np.float64)
        self.abs = np.zeros(self.NumCovPattInGailModel,dtype=np.float64)

        self.rlan = np.zeros(14,dtype=np.float64)
        self.rmu = np.zeros(14,dtype=np.float64)
        self.sumb = np.zeros(self.NumCovPattInGailModel,dtype=np.float64)
        self.sumbb = np.zeros(self.NumCovPattInGailModel,dtype=np.float64)
        self.t = np.zeros(15,dtype=np.float64)

        self.rmu2 = np.zeros((14,12),dtype=np.float64)
        self.rlan2 = np.zeros((14,12),dtype=np.float64)

        self.rf2 = np.zeros((2,13),dtype=np.float64)

    def Initialize(self):
        # age categories boundaries * /
        self.t[0] = 20.0
        self.t[1] = 25.0
        self.t[2] = 30.0
        self.t[3] = 35.0
        self.t[4] = 40.0
        self.t[5] = 45.0
        self.t[6] = 50.0
        self.t[7] = 55.0
        self.t[8] = 60.0
        self.t[9] = 65.0
        self.t[10] = 70.0
        self.t[11] = 75.0
        self.t[12] = 80.0
        self.t[13] = 85.0
        self.t[14] = 90.0

        '''
            age specific competing hazards (h2) - BCPT model or STAR model
            SEER mortality 1985:87, excluding death from breast cancer - white, African American)
            US   mortality 1990:96, excluding death from breast cancer -     hispanic)
            ages [20:25), [25:30), [30:35) .... [70:74), [75:80), [80:85), [85:90)
        '''
        self.rmu2[0, 0] = 49.3 * 0.00001      # // [20:25) race = white, other 1 / 12
        self.rmu2[1, 0] = 53.1 * 0.00001      # // [25:30) race = white, other  BCPT
        self.rmu2[2, 0] = 62.5 * 0.00001      # // [30:35) race = white, other
        self.rmu2[3, 0] = 82.5 * 0.00001      # // [35:40) race = white, other
        self.rmu2[4, 0] = 130.7 * 0.00001     # // [40:45) race = white, other
        self.rmu2[5, 0] = 218.1 * 0.00001     # // [45:50) race = white, other
        self.rmu2[6, 0] = 365.5 * 0.00001     # // [50:55) race = white, other
        self.rmu2[7, 0] = 585.2 * 0.00001     # // [55:60) race = white, other
        self.rmu2[8, 0] = 943.9 * 0.00001     # // [60:65) race = white, other
        self.rmu2[9, 0] = 1502.8 * 0.00001    # // [65:70) race = white, other
        self.rmu2[10, 0] = 2383.9 * 0.00001   # // [70:75) race  = white, other
        self.rmu2[11, 0] = 3883.2 * 0.00001   # // [75:80) race = white, other
        self.rmu2[12, 0] = 6682.8 * 0.00001   # // [80:85) race = white, other
        self.rmu2[13, 0] = 14490.8 * 0.00001  # // [85:90) race = white, other

        '''
        11/29/2007 SRamaiah - updated age specific competing hazards (h2)
        with new values from NCHS 1996-00 data for African American Women
        Updated array  rmu2[*, 1] with following new values for African American Women
        '''

        self.rmu2[0, 1] = 0.00074354   # //  [20, 25) race = African American
        self.rmu2[1, 1] = 0.00101698   # //  [24, 30) race = African American
        self.rmu2[2, 1] = 0.00145937   # //  [30, 35) race = African American
        self.rmu2[3, 1] = 0.00215933   # //  [34, 40) race = African American
        self.rmu2[4, 1] = 0.00315077   # //  [40, 45) race = African American
        self.rmu2[5, 1] = 0.00448779   # //  [44, 50) race = African American
        self.rmu2[6, 1] = 0.00632281   # //  [50, 55) race = African American
        self.rmu2[7, 1] = 0.00963037   # //  [54, 60) race = African American
        self.rmu2[8, 1] = 0.01471818   # //  [60, 65) race = African American
        self.rmu2[9, 1] = 0.02116304   # //  [64, 70) race = African American
        self.rmu2[10, 1] = 0.03266035  # //  [70, 75) race = African American
        self.rmu2[11, 1] = 0.04564087  # //  [74, 80) race = African American
        self.rmu2[12, 1] = 0.06835185  # //  [80, 84) race = African American
        self.rmu2[13, 1] = 0.13271262  # //  [84, 90) race = African American

        self.rmu2[0, 2] = 43.7 * 0.00001     # // [20:25) race = hispanic     5 / 12 / 00
        self.rmu2[1, 2] = 53.3 * 0.00001     # // [25:30) race = hispanic     STAR
        self.rmu2[2, 2] = 70.0 * 0.00001     # // [30:35) race = hispanic
        self.rmu2[3, 2] = 89.7 * 0.00001     # // [35:40) race = hispanic
        self.rmu2[4, 2] = 116.3 * 0.00001    # // [40:45) race = hispanic
        self.rmu2[5, 2] = 170.2 * 0.00001    # // [45:50) race = hispanic
        self.rmu2[6, 2] = 264.6 * 0.00001    # // [50:55) race = hispanic
        self.rmu2[7, 2] = 421.6 * 0.00001    # // [55:60) race = hispanic
        self.rmu2[8, 2] = 696.0 * 0.00001    # // [60:65) race = hispanic
        self.rmu2[9, 2] = 1086.7 * 0.00001   # // [65:70) race = hispanic
        self.rmu2[10, 2] = 1685.8 * 0.00001  # // [70:75) race = hispanic
        self.rmu2[11, 2] = 2515.6 * 0.00001  # // [75:80) race = hispanic
        self.rmu2[12, 2] = 4186.6 * 0.00001  # // [80:85) race = hispanic
        self.rmu2[13, 2] = 8947.6 * 0.00001  # // [85:90) race = hispanic

        '''
        age specific competing hazards (h2) for "average woman"
        (NCHS mortality 1992:95, excluding death from breast cancer - white, African American)
        (US   mortality 1990:95, excluding death from breast cancer -     hispanic)
        ages [20:25), [25:30), [30:35) .... [70:74), [75:80), [80:85), [85:90)
        '''
        self.rmu2[0, 3] = 44.12 * 0.00001       # // [20,25) race=white,other 11/21
        self.rmu2[1, 3] = 52.54 * 0.00001       # // [24,30) race=white,other
        self.rmu2[2, 3] = 67.46 * 0.00001       # // [30,35) race=white,other
        self.rmu2[3, 3] = 90.92 * 0.00001       # // [34,40) race=white,other
        self.rmu2[4, 3] = 125.34 * 0.00001      # // [40,45) race=white,other
        self.rmu2[5, 3] = 195.70 * 0.00001      # // [44,50) race=white,other
        self.rmu2[6, 3] = 329.84 * 0.00001      # // [50,55) race=white,other
        self.rmu2[7, 3] = 546.22 * 0.00001      # // [54,60) race=white,other
        self.rmu2[8, 3] = 910.35 * 0.00001      # // [60,65) race=white,other
        self.rmu2[9, 3] = 1418.54 * 0.00001     # // [64,70) race=white,other
        self.rmu2[10, 3] = 2259.35 * 0.00001    # // [70,75) race=white,other
        self.rmu2[11, 3] = 3611.46 * 0.00001    # // [74,80) race=white,other
        self.rmu2[12, 3] = 6136.26 * 0.00001    # // [80,84) race=white,other
        self.rmu2[13, 3] = 14206.63 * 0.00001   # // [84,90) race=white,other

        '''
        11/29/2007 SRamaiah - updated age specific competing hazards (h2)
                with new values from NCHS 1996-00 data for African American Women
                Updated array rmu2[*, 4] with following new values for African American Women
        '''

        self.rmu2[0, 4] = 0.00074354   # // [20, 25) race = African American        11 / 28 / 07
        self.rmu2[1, 4] = 0.00101698   # // [24, 30) race = African American
        self.rmu2[2, 4] = 0.00145937   # // [30, 35) race = African American
        self.rmu2[3, 4] = 0.00215933   # // [34, 40) race = African American
        self.rmu2[4, 4] = 0.00315077   # // [40, 45) race = African American
        self.rmu2[5, 4] = 0.00448779   # // [44, 50) race = African American
        self.rmu2[6, 4] = 0.00632281   # // [50, 55) race = African American
        self.rmu2[7, 4] = 0.00963037   # // [54, 60) race = African American
        self.rmu2[8, 4] = 0.01471818   # // [60, 65) race = African American
        self.rmu2[9, 4] = 0.02116304   # // [64, 70) race = African American
        self.rmu2[10, 4] = 0.03266035  # // [70, 75) race = African American
        self.rmu2[11, 4] = 0.04564087  # // [74, 80) race = African American
        self.rmu2[12, 4] = 0.06835185  # // [80, 84) race = African American
        self.rmu2[13, 4] = 0.13271262  # // [84, 90) race = African American

        self.rmu2[0, 5] = 43.7 * 0.00001     # // [20:25) race = hispanic        5 / 12 / 00
        self.rmu2[1, 5] = 53.3 * 0.00001     # // [25:30) race = hispanic
        self.rmu2[2, 5] = 70.0 * 0.00001     # // [30:35) race = hispanic
        self.rmu2[3, 5] = 89.7 * 0.00001     # // [35:40) race = hispanic
        self.rmu2[4, 5] = 116.3 * 0.00001    # // [40:45) race = hispanic
        self.rmu2[5, 5] = 170.2 * 0.00001    # // [45:50) race = hispanic
        self.rmu2[6, 5] = 264.6 * 0.00001    # // [50:55) race = hispanic
        self.rmu2[7, 5] = 421.6 * 0.00001    # // [55:60) race = hispanic
        self.rmu2[8, 5] = 696.0 * 0.00001    # // [60:65) race = hispanic
        self.rmu2[9, 5] = 1086.7 * 0.00001   # // [65:70) race = hispanic
        self.rmu2[10, 5] = 1685.8 * 0.00001  # // [70:75) race = hispanic
        self.rmu2[11, 5] = 2515.6 * 0.00001  # // [75:80) race = hispanic
        self.rmu2[12, 5] = 4186.6 * 0.00001  # // [80:85) race = hispanic
        self.rmu2[13, 5] = 8947.6 * 0.00001  # // [85:90) race = hispanic

        '''
        age specific breast cancer composite incidence (h1*)
        (SEER incidence 1983:87 - white)                                      BCPT
        (SEER incidence 1994-98 - African American)                                      SEER11
        (SEER incidence 1990:96 -     hispanic)                               STAR
        ages [20:25), [25:30), [30:35) .... [70:74), [75:80), [80:85), [85:90)
        '''

        self.rlan2[0, 0] = 1.0 * 0.00001        # // [20:25) race = white, other        1 / 12
        self.rlan2[1, 0] = 7.6 * 0.00001        # // [25:30) race = white, other        BCPT
        self.rlan2[2, 0] = 26.6 * 0.00001       # // [30:35) race = white, other
        self.rlan2[3, 0] = 66.1 * 0.00001       # // [35:40) race = white, other
        self.rlan2[4, 0] = 126.5 * 0.00001      # // [40:45) race = white, other
        self.rlan2[5, 0] = 186.6 * 0.00001      # // [45:50) race = white, other
        self.rlan2[6, 0] = 221.1 * 0.00001      # // [50:55) race = white, other
        self.rlan2[7, 0] = 272.1 * 0.00001      # // [55:60) race = white, other
        self.rlan2[8, 0] = 334.8 * 0.00001      # // [60:65) race = white, other
        self.rlan2[9, 0] = 392.3 * 0.00001      # // [65:70) race = white, other
        self.rlan2[10, 0] = 417.8 * 0.00001     # // [70:75) race = white, other
        self.rlan2[11, 0] = 443.9 * 0.00001     # // [75:80) race = white, other
        self.rlan2[12, 0] = 442.1 * 0.00001     # // [80:85) race = white, other
        self.rlan2[13, 0] = 410.9 * 0.00001     # // [85:90) race = white, other

        '''
        11/29/2007 SRamaiah - updated age specific breast cancer composite incidence (h1*)
        with new values from 1994-98SEER11 data for African American Women
        Updated array rlan2[*, 1] with following new values for African American Women
        '''

        self.rlan2[0, 1] = 0.00002696    # // [20:25) race=African American    11/29/2007
        self.rlan2[1, 1] = 0.00011295    # // [25:30) race=African American
        self.rlan2[2, 1] = 0.00031094    # // [30:35) race=African American
        self.rlan2[3, 1] = 0.00067639    # // [35:40) race=African American
        self.rlan2[4, 1] = 0.00119444    # // [40:45) race=African American
        self.rlan2[5, 1] = 0.00187394    # // [45:50) race=African American
        self.rlan2[6, 1] = 0.00241504    # // [50:55) race=African American
        self.rlan2[7, 1] = 0.00291112    # // [55:60) race=African American
        self.rlan2[8, 1] = 0.00310127    # // [60:65) race=African American
        self.rlan2[9, 1] = 0.00366560    # // [65:70) race=African American
        self.rlan2[10, 1] = 0.00393132   # // [70:75) race=African American
        self.rlan2[11, 1] = 0.00408951   # // [75:80) race=African American
        self.rlan2[12, 1] = 0.00396793   # // [80:85) race=African American
        self.rlan2[13, 1] = 0.00363712   # // [85:90) race=African American

        self.rlan2[0, 2] = 2.00 * 0.00001      # [20:25) race = hispanic        5 / 12 / 00
        self.rlan2[1, 2] = 7.10 * 0.00001      # [25:30) race = hispanic        STAR
        self.rlan2[2, 2] = 19.70 * 0.00001     # [30:35) race = hispanic
        self.rlan2[3, 2] = 43.80 * 0.00001     # [35:40) race = hispanic
        self.rlan2[4, 2] = 81.10 * 0.00001     # [40:45) race = hispanic
        self.rlan2[5, 2] = 130.70 * 0.00001    # [45:50) race = hispanic
        self.rlan2[6, 2] = 157.40 * 0.00001    # [50:55) race = hispanic
        self.rlan2[7, 2] = 185.70 * 0.00001    # [55:60) race = hispanic
        self.rlan2[8, 2] = 215.10 * 0.00001    # [60:65) race = hispanic
        self.rlan2[9, 2] = 251.20 * 0.00001    # [65:70) race = hispanic
        self.rlan2[10, 2] = 284.60 * 0.00001       # [70:75) race = hispanic
        self.rlan2[11, 2] = 275.70 * 0.00001       # [75:80) race = hispanic
        self.rlan2[12, 2] = 252.30 * 0.00001       # [80:85) race = hispanic
        self.rlan2[13, 2] = 203.90 * 0.00001       # [85:90) race = hispanic

        '''
        age specific breast cancer composite incidence (h1*)-"average woman"
        (SEER incidence 1992:96 - white, African American)
        (SEER incidence 1990:96 -     hispanic)
        ages [20:25), [25:30), [30:35) .... [70:74), [75:80), [80:85), [85:90)
        '''

        self.rlan2[0, 3] = 1.22 * 0.00001    # [20:25) race = white, other        11 / 21
        self.rlan2[1, 3] = 7.41 * 0.00001    # [25:30) race = white, other
        self.rlan2[2, 3] = 22.97 * 0.00001   # [30:35) race = white, other
        self.rlan2[3, 3] = 56.49 * 0.00001   # [35:40) race = white, other
        self.rlan2[4, 3] = 116.45 * 0.00001  # [40:45) race = white, other
        self.rlan2[5, 3] = 195.25 * 0.00001  # [45:50) race = white, other
        self.rlan2[6, 3] = 261.54 * 0.00001  # [50:55) race = white, other
        self.rlan2[7, 3] = 302.79 * 0.00001  # [55:60) race = white, other
        self.rlan2[8, 3] = 367.57 * 0.00001  # [60:65) race = white, other
        self.rlan2[9, 3] = 420.29 * 0.00001  # [65:70) race = white, other
        self.rlan2[10, 3] = 473.08 * 0.00001     # [70:75) race = white, other
        self.rlan2[11, 3] = 494.25 * 0.00001     # [75:80) race = white, other
        self.rlan2[12, 3] = 479.76 * 0.00001     # [80:85) race = white, other
        self.rlan2[13, 3] = 401.06 * 0.00001     # [85:90) race = white, other

        '''
        11/29/2007 SRamaiah - updated age specific breast cancer composite incidence (h1*)
        with new values from 1994-98SEER11 data for African American Women

        Updated array rlan2[*, 4] with following new values for African American Women
        '''

        self.rlan2[0, 4] = 0.00002696    # [20:25) race = African American    11 / 29 / 2007
        self.rlan2[1, 4] = 0.00011295    # [25:30) race = African    American
        self.rlan2[2, 4] = 0.00031094    # [30:35) race = African    American
        self.rlan2[3, 4] = 0.00067639    # [35:40) race = African    American
        self.rlan2[4, 4] = 0.00119444    # [40:45) race = African    American
        self.rlan2[5, 4] = 0.00187394    # [45:50) race = African    American
        self.rlan2[6, 4] = 0.00241504    # [50:55) race = African    American
        self.rlan2[7, 4] = 0.00291112    # [55:60) race = African    American
        self.rlan2[8, 4] = 0.00310127    # [60:65) race = African    American
        self.rlan2[9, 4] = 0.00366560    # [65:70) race = African    American
        self.rlan2[10, 4] = 0.00393132   # [70:75) race = African    American
        self.rlan2[11, 4] = 0.00408951   # [75:80) race = African    American
        self.rlan2[12, 4] = 0.00396793   # [80:85) race = African    American
        self.rlan2[13, 4] = 0.00363712   # [85:90) race = African    American

        self.rlan2[0, 5] = 2.00 * 0.00001    # [20:25) race = hispanic        5 / 12 / 00
        self.rlan2[1, 5] = 7.10 * 0.00001    # [25:30) race = hispanic
        self.rlan2[2, 5] = 19.70 * 0.00001   # [30:35) race = hispanic
        self.rlan2[3, 5] = 43.80 * 0.00001   # [35:40) race = hispanic
        self.rlan2[4, 5] = 81.10 * 0.00001   # [40:45) race = hispanic
        self.rlan2[5, 5] = 130.70 * 0.00001  # [45:50) race = hispanic
        self.rlan2[6, 5] = 157.40 * 0.00001  # [50:55) race = hispanic
        self.rlan2[7, 5] = 185.70 * 0.00001  # [55:60) race = hispanic
        self.rlan2[8, 5] = 215.10 * 0.00001  # [60:65) race = hispanic
        self.rlan2[9, 5] = 251.20 * 0.00001  # [65:70) race = hispanic
        self.rlan2[10, 5] = 284.60 * 0.00001     # [70:75) race = hispanic
        self.rlan2[11, 5] = 275.70 * 0.00001     # [75:80) race = hispanic
        self.rlan2[12, 5] = 252.30 * 0.00001     # [80:85) race = hispanic
        self.rlan2[13, 5] = 203.90 * 0.00001     # [85:90) race = hispanic

        ''' White & Other women logistic regression coefficients - GAIL model (BCDDP) '''

        self.bet2[0, 0] = -0.7494824600  # intercept        1 / 12 / 99 & 11 / 13 / 07
        self.bet2[1, 0] = 0.0108080720   # age >= 50 indicator
        self.bet2[2, 0] = 0.0940103059   # age  menarchy
        self.bet2[3, 0] = 0.5292641686   #  # of breast biopsy
        self.bet2[4, 0] = 0.2186262218   # age 1st live birth
        self.bet2[5, 0] = 0.9583027845   #  # 1st degree relatives with breast ca
        self.bet2[6, 0] = -0.2880424830  #  # breast biopsy * age >=50 indicator
        self.bet2[7, 0] = -0.1908113865  # age 1st live birth *  # 1st degree rel

        '''African American women  logistic regression coefficients - CARE model'''

        self.bet2[0, 1] = -0.3457169653  # intercept        11 / 13 / 07
        self.bet2[1, 1] = 0.0334703319   # age >= 50 indicator set ? to 0 in PGM
        self.bet2[2, 1] = 0.2672530336   # age menarchy
        self.bet2[3, 1] = 0.1822121131   #  # of breast biopsy
        self.bet2[4, 1] = 0.0000000000   # age 1st live birth
        self.bet2[5, 1] = 0.4757242578   #  # 1st degree relatives with breast ca
        self.bet2[6, 1] = -0.1119411682  #  # breast biopsy * age >=50 indicator
        self.bet2[7, 1] = 0.0000000000   # age 1st live birth *  # 1st degree rel

        '''Hispanic women   logistic regression coefficients - GAIL model (BCDDP)'''

        self.bet2[0, 2] = -0.7494824600  # intercept        1 / 12 / 99 & 11 / 13 / 07
        self.bet2[1, 2] = 0.0108080720   # age >= 50 indicator
        self.bet2[2, 2] = 0.0940103059   # age menarchy
        self.bet2[3, 2] = 0.5292641686   #  # of breast biopsy
        self.bet2[4, 2] = 0.2186262218   # age 1st live birth
        self.bet2[5, 2] = 0.9583027845   #  # 1st degree relatives with breast ca
        self.bet2[6, 2] = -0.2880424830  #  # breast biopsy * age >=50 indicator
        self.bet2[7, 2] = -0.1908113865  # age 1st live birth *  # 1st degree rel

        '''American-Asian Beta

            VisExcell SRMOORE: This was originally c# code:

            int i = 6;
            for (i = 6; i <= 11; i++)
            {
                bet2[0, i] = 0.00000000000000; //  intercept
                bet2[1, i] = 0.00000000000000; //  age >= 50 indicator
                bet2[2, i] = 0.07499257592975; //age menarchy
                bet2[3, i] = 0.55263612260619; //   # of breast biopsy
                bet2[4, i] = 0.27638268294593; //  age 1st live birth
                bet2[5, i] = 0.79185633720481; //   # 1st degree relatives with breast ca
                bet2[6, i] = 0.00000000000000; //  # breast biopsy * age >=50 indicator
                bet2[7, i] = 0.00000000000000; //   age 1st live birth * # 1st degree rel
            }
        '''
        for i in range(6,12):
            self.bet2[0, i] = 0.00000000000000   # intercept
            self.bet2[1, i] = 0.00000000000000   # age >= 50 indicator
            self.bet2[2, i] = 0.07499257592975   # age menarchy
            self.bet2[3, i] = 0.55263612260619   #  # of breast biopsy
            self.bet2[4, i] = 0.27638268294593   # age 1st live birth
            self.bet2[5, i] = 0.79185633720481   #  # 1st degree relatives with breast ca
            self.bet2[6, i] = 0.00000000000000   #  # breast biopsy * age >=50 indicator
            self.bet2[7, i] = 0.00000000000000   # age 1st live birth *  # 1st degree rel

        ''' LINE 432 BCPT.cs
         age 1st live birth * # 1st degree rel

         conversion factors (1-attributable risk) used in BCPT model
        '''

        self.rf2[0, 0] = 0.5788413   # age < 50, race = white, other        1 / 12 / 99
        self.rf2[1, 0] = 0.5788413   # age >= 50, race = white, other

        '''
        /* 11/27/2007 SRamaiah.
         * Based on Journal(JNCI djm223 LM) published on Dec 05, 2007 by Gail and other scientists,
         * The new values are being used for african american woman
         * as there were some major descrenpancies between CARE model and GAIL Model
         */
        '''

        self.rf2[0, 1] = 0.72949880  # age < 50, race = African American    12 / 19 / 2007 based on david pee's input
        self.rf2[1, 1] = 0.74397137  # age >= 50, race = African American
        self.rf2[0, 2] = 0.5788413   # age < 50, race = hispanic             5 / 12 / 2000
        self.rf2[1, 2] = 0.5788413   # age >= 50, race = hispanic

        '''
        conversion factors (1-attributable risk) used for "average woman"
        '''

        self.rf2[0, 3] = 1.0     # age < 50, race = white avg woman                11 / 21
        self.rf2[1, 3] = 1.0     # age >= 50, race = white avg woman
        self.rf2[0, 4] = 1.0     # age < 50, race = AfricanAmerican avg woman              11 / 21
        self.rf2[1, 4] = 1.0     # age >= 50, race = AfricanAmerican avg woman
        self.rf2[0, 5] = 1.0     # age < 50, race = hispanic avg woman             5 / 12
        self.rf2[1, 5] = 1.0     # age >= 50, race = hispanic avg woman

        ''' LINE 470 BCPT.cs
        American-Asian conversion factor

        VisExcell SRMOORE: Originally the following C# code:

        i = 6;
        for (i = 6; i <= 11; i++)
        {
            rf2[0, i] = 0.47519806426735;                // age < 50, avg woman
            rf2[1, i] = 0.50316401683903;                // age >=50, avg woman
        }
        '''

        for i in range(6,12):
            self.rf2[0, i] = 0.47519806426735    # age < 50, avg woman
            self.rf2[1, i] = 0.50316401683903    # age >= 50, avg woman

        self.rf2[0, 12] = 1.0    # age < 50, race = hispanic avg woman        5 / 12
        self.rf2[1, 12] = 1.0    # age >= 50, race = hispanic avg woman

        '''LINE 481 BCPT.cs

        SEER18 incidence 1998:02 - chinese  Jan052010'''

        self.rlan2[0, 6] = 0.000004059636
        self.rlan2[1, 6] = 0.000045944465
        self.rlan2[2, 6] = 0.000188279352
        self.rlan2[3, 6] = 0.000492930493
        self.rlan2[4, 6] = 0.000913603501
        self.rlan2[5, 6] = 0.001471537353
        self.rlan2[6, 6] = 0.001421275482
        self.rlan2[7, 6] = 0.001970946494
        self.rlan2[8, 6] = 0.001674745804
        self.rlan2[9, 6] = 0.001821581075
        self.rlan2[10, 6] = 0.001834477198
        self.rlan2[11, 6] = 0.001919911972
        self.rlan2[12, 6] = 0.002233371071
        self.rlan2[13, 6] = 0.002247315779

        '''
        NCHS mortality 1998:02,    chinese  Jan052010
        '''

        self.rmu2[0, 6] = 0.000210649076
        self.rmu2[1, 6] = 0.000192644865
        self.rmu2[2, 6] = 0.000244435215
        self.rmu2[3, 6] = 0.000317895949
        self.rmu2[4, 6] = 0.000473261994
        self.rmu2[5, 6] = 0.000800271380
        self.rmu2[6, 6] = 0.001217480226
        self.rmu2[7, 6] = 0.002099836508
        self.rmu2[8, 6] = 0.003436889186
        self.rmu2[9, 6] = 0.006097405623
        self.rmu2[10, 6] = 0.010664526765
        self.rmu2[11, 6] = 0.020148678452
        self.rmu2[12, 6] = 0.037990796590
        self.rmu2[13, 6] = 0.098333900733

        '''// ** *SEER18
        incidence
        1998:02 - japanese
        Jan052010;'''

        self.rlan2[0, 7] = 0.000000000001
        self.rlan2[1, 7] = 0.000099483924
        self.rlan2[2, 7] = 0.000287041681
        self.rlan2[3, 7] = 0.000545285759
        self.rlan2[4, 7] = 0.001152211095
        self.rlan2[5, 7] = 0.001859245108
        self.rlan2[6, 7] = 0.002606291272
        self.rlan2[7, 7] = 0.003221751682
        self.rlan2[8, 7] = 0.004006961859
        self.rlan2[9, 7] = 0.003521715275
        self.rlan2[10, 7] = 0.003593038294
        self.rlan2[11, 7] = 0.003589303081
        self.rlan2[12, 7] = 0.003538507159
        self.rlan2[13, 7] = 0.002051572909

        '''// ** *NCHS
        mortality
        1998:02, japanese
        Jan052010;'''

        self.rmu2[0, 7] = 0.000173593803
        self.rmu2[1, 7] = 0.000295805882
        self.rmu2[2, 7] = 0.000228322534
        self.rmu2[3, 7] = 0.000363242389
        self.rmu2[4, 7] = 0.000590633044
        self.rmu2[5, 7] = 0.001086079485
        self.rmu2[6, 7] = 0.001859999966
        self.rmu2[7, 7] = 0.003216600974
        self.rmu2[8, 7] = 0.004719402141
        self.rmu2[9, 7] = 0.008535331402
        self.rmu2[10, 7] = 0.012433511681
        self.rmu2[11, 7] = 0.020230197885
        self.rmu2[12, 7] = 0.037725498348
        self.rmu2[13, 7] = 0.106149118663

        '''// ** *SEER18
        incidence
        1998:02 - filipino
        Jan052010;'''

        self.rlan2[0, 8] = 0.000007500161
        self.rlan2[1, 8] = 0.000081073945
        self.rlan2[2, 8] = 0.000227492565
        self.rlan2[3, 8] = 0.000549786433
        self.rlan2[4, 8] = 0.001129400541
        self.rlan2[5, 8] = 0.001813873795
        self.rlan2[6, 8] = 0.002223665639
        self.rlan2[7, 8] = 0.002680309266
        self.rlan2[8, 8] = 0.002891219230
        self.rlan2[9, 8] = 0.002534421279
        self.rlan2[10, 8] = 0.002457159409
        self.rlan2[11, 8] = 0.002286616920
        self.rlan2[12, 8] = 0.001814802825
        self.rlan2[13, 8] = 0.001750879130

        '''// ** *NCHS
        mortality
        1998:02, filipino
        Jan052010;'''

        self.rmu2[0, 8] = 0.000229120979
        self.rmu2[1, 8] = 0.000262988494
        self.rmu2[2, 8] = 0.000314844090
        self.rmu2[3, 8] = 0.000394471908
        self.rmu2[4, 8] = 0.000647622610
        self.rmu2[5, 8] = 0.001170202327
        self.rmu2[6, 8] = 0.001809380379
        self.rmu2[7, 8] = 0.002614170568
        self.rmu2[8, 8] = 0.004483330681
        self.rmu2[9, 8] = 0.007393665092
        self.rmu2[10, 8] = 0.012233059675
        self.rmu2[11, 8] = 0.021127058106
        self.rmu2[12, 8] = 0.037936954809
        self.rmu2[13, 8] = 0.085138518334

        '''// ** *SEER18
        incidence
        1998:02 - hawaiian
        Jan052010;'''

        self.rlan2[0, 9] = 0.000045080582
        self.rlan2[1, 9] = 0.000098570724
        self.rlan2[2, 9] = 0.000339970860
        self.rlan2[3, 9] = 0.000852591429
        self.rlan2[4, 9] = 0.001668562761
        self.rlan2[5, 9] = 0.002552703284
        self.rlan2[6, 9] = 0.003321774046
        self.rlan2[7, 9] = 0.005373001776
        self.rlan2[8, 9] = 0.005237808549
        self.rlan2[9, 9] = 0.005581732512
        self.rlan2[10, 9] = 0.005677419355
        self.rlan2[11, 9] = 0.006513409962
        self.rlan2[12, 9] = 0.003889457523
        self.rlan2[13, 9] = 0.002949061662

        '''// ** *NCHS
        mortality
        1998:02, hawaiian
        Jan052010;'''

        self.rmu2[0, 9] = 0.000563507269
        self.rmu2[1, 9] = 0.000369640217
        self.rmu2[2, 9] = 0.001019912579
        self.rmu2[3, 9] = 0.001234013911
        self.rmu2[4, 9] = 0.002098344078
        self.rmu2[5, 9] = 0.002982934175
        self.rmu2[6, 9] = 0.005402445702
        self.rmu2[7, 9] = 0.009591474245
        self.rmu2[8, 9] = 0.016315472607
        self.rmu2[9, 9] = 0.020152229069
        self.rmu2[10, 9] = 0.027354838710
        self.rmu2[11, 9] = 0.050446998723
        self.rmu2[12, 9] = 0.072262026612
        self.rmu2[13, 9] = 0.145844504021

        '''// ** *SEER18
        incidence
        1998:02 - other
        pacific
        islander
        Jan052010;'''

        self.rlan2[0, 10] = 0.000000000001
        self.rlan2[1, 10] = 0.000071525212
        self.rlan2[2, 10] = 0.000288799028
        self.rlan2[3, 10] = 0.000602250698
        self.rlan2[4, 10] = 0.000755579402
        self.rlan2[5, 10] = 0.000766406354
        self.rlan2[6, 10] = 0.001893124938
        self.rlan2[7, 10] = 0.002365580107
        self.rlan2[8, 10] = 0.002843933070
        self.rlan2[9, 10] = 0.002920921732
        self.rlan2[10, 10] = 0.002330395655
        self.rlan2[11, 10] = 0.002036291235
        self.rlan2[12, 10] = 0.001482683983
        self.rlan2[13, 10] = 0.001012248203

        '''// ** *NCHS
        mortality
        1998:02, other
        pacific
        islander
        Jan052010;'''

        self.rmu2[0, 10] = 0.000465500812
        self.rmu2[1, 10] = 0.000600466920
        self.rmu2[2, 10] = 0.000851057138
        self.rmu2[3, 10] = 0.001478265376
        self.rmu2[4, 10] = 0.001931486788
        self.rmu2[5, 10] = 0.003866623959
        self.rmu2[6, 10] = 0.004924932309
        self.rmu2[7, 10] = 0.008177071806
        self.rmu2[8, 10] = 0.008638202890
        self.rmu2[9, 10] = 0.018974658371
        self.rmu2[10, 10] = 0.029257567105
        self.rmu2[11, 10] = 0.038408980974
        self.rmu2[12, 10] = 0.052869579345
        self.rmu2[13, 10] = 0.074745721133

        '''// ** *SEER18
        incidence
        1998:02 - other
        asian
        Jan052010;'''

        self.rlan2[0, 11] = 0.000012355409
        self.rlan2[1, 11] = 0.000059526456
        self.rlan2[2, 11] = 0.000184320831
        self.rlan2[3, 11] = 0.000454677273
        self.rlan2[4, 11] = 0.000791265338
        self.rlan2[5, 11] = 0.001048462801
        self.rlan2[6, 11] = 0.001372467817
        self.rlan2[7, 11] = 0.001495473711
        self.rlan2[8, 11] = 0.001646746198
        self.rlan2[9, 11] = 0.001478363563
        self.rlan2[10, 11] = 0.001216010125
        self.rlan2[11, 11] = 0.001067663700
        self.rlan2[12, 11] = 0.001376104012
        self.rlan2[13, 11] = 0.000661576644

        '''NCHS
        mortality
        1998:02, other
        asian
        Jan052010'''

        self.rmu2[0, 11] = 0.000212632332
        self.rmu2[1, 11] = 0.000242170741
        self.rmu2[2, 11] = 0.000301552711
        self.rmu2[3, 11] = 0.000369053354
        self.rmu2[4, 11] = 0.000543002943
        self.rmu2[5, 11] = 0.000893862331
        self.rmu2[6, 11] = 0.001515172239
        self.rmu2[7, 11] = 0.002574669551
        self.rmu2[8, 11] = 0.004324370426
        self.rmu2[9, 11] = 0.007419621918
        self.rmu2[10, 11] = 0.013251765130
        self.rmu2[11, 11] = 0.022291427490
        self.rmu2[12, 11] = 0.041746550635
        self.rmu2[13, 11] = 0.087485802065

        ### END Initialize(self)

    '''
    Line 699 BCPT.cs
    private double CalculateAbosluteRisk(...)
    '''
    def CalculateAbsoluteRisk(self,
                      CurrentAge,           # int    [t1]
                      ProjectionAge,        # int    [t2]
                      AgeIndicator,         # int    [i0]
                      NumberOfBiopsy,       # int    [i2]
                      MenarcheAge,          # int    [i1]
                      FirstLiveBirthAge,    # int    [i3]
                      EverHadBiopsy,        # int    [iever]
                      FirstDegRelatives,    # int    [i4]
                      ihyp,                 # int    [ihyp]  HyperPlasia
                      rhyp,                 # double [rhyp]  RHyperPlasia
                      irace                 # int    [race]
                    ):
        # return self.CalculateRisk(1, CurrentAge, ProjectionAge, AgeIndicator,
        #                          NumberOfBiopsy, MenarcheAge, FirstLiveBirthAge, EverHadBiopsy,
        #                          FirstDegRelatives, ihyp, rhyp, irace)
        return self.CalculateRiskAPI(1, CurrentAge, ProjectionAge, MenarcheAge, FirstLiveBirthAge, FirstDegRelatives,
                                     EverHadBiopsy, NumberOfBiopsy, ihyp, irace)

    '''
    Line 727 BCPT.cs
    private double calculateAeverageRisk(...)
    NOTE: Mis-spelled in original.
    '''
    def CalculateAeverageRisk(self,
                      CurrentAge,           # int    [t1]
                      ProjectionAge,        # int    [t2]
                      AgeIndicator,         # int    [i0]
                      NumberOfBiopsy,       # int    [i2]
                      MenarcheAge,          # int    [i1]
                      FirstLiveBirthAge,    # int    [i3]
                      EverHadBiopsy,        # int    [iever]
                      FirstDegRelatives,    # int    [i4]
                      ihyp,                 # int    [ihyp]  HyperPlasia
                      rhyp,                 # double [rhyp]  RHyperPlasia
                      irace                 # int    [race]
                    ):
        # return self.CalculateRisk(2, CurrentAge, ProjectionAge, AgeIndicator,
        #                          NumberOfBiopsy, MenarcheAge, FirstLiveBirthAge, EverHadBiopsy,
        #                          FirstDegRelatives, ihyp, rhyp, irace)
        return self.CalculateRiskAPI(2, CurrentAge, ProjectionAge, MenarcheAge, FirstLiveBirthAge, FirstDegRelatives,
                                     EverHadBiopsy,NumberOfBiopsy,ihyp,irace)

    ''' New API calculate risk entry point '''
    def CalculateRiskAPI(self,
                         riskindex,
                         CurrentAge,
                         ProjectionAge,
                         MenarcheAge,
                         FirstLiveBirthAge,
                         FirstDegRelatives,
                         everhadbiopsy=99,    # 99: unknown, 1: yes, 0: no
                         NumberOfBiopsy=99,    # 0: no, 1: One, or unknown buy have had biopsy, 2: more than one
                         hyperplasia=99,  # [ 1: yes, 0: no, 99: Unknown or never had biopsy
                         race=1):

        # 50 and over?
        ageindicator = 0
        if CurrentAge >= 50:
            ageindicator = 1

        # Clean up biopsy inputs

        if everhadbiopsy == 0:
            NumberOfBiopsy = 0
            hyperplasia = 99

        if everhadbiopsy == 99:
            NumberOfBiopsy = 99
        elif NumberOfBiopsy == 0 or (everhadbiopsy == 99 and NumberOfBiopsy == 99):
            NumberOfBiopsy = 0
        elif NumberOfBiopsy == 1 or (everhadbiopsy == 1 and NumberOfBiopsy == 99):
            NumberOfBiopsy = 1
        elif 1 < NumberOfBiopsy <= 30:
            NumberOfBiopsy = 2
        else:
            NumberOfBiopsy = 0  # Inputs are out of bounds... or everhadbiopsy == 0


        realHyp = np.float64(1.0)   # Zero Biopsy or Unknown
        if hyperplasia == 1:
            realHyp = np.float64(1.82)  # Yes to hyperplasia
        elif hyperplasia == 0:
            realHyp = np.float64(0.93)  # No to hyperplasia but yes to biopsy

        # level set everhadbiopsy (99 -> 0)
        if everhadbiopsy == 99:
            everhadbiopsy = 0

        # Clean up first deg relatives for race values
        if FirstDegRelatives == 0 or FirstDegRelatives == 99:
           FirstDegRelatives = 0
        elif 2 <= FirstDegRelatives <= 31 and race < 7:
            FirstDegRelatives = 2
        elif FirstDegRelatives >= 2 and race >= 7:
            FirstDegRelatives = 1

        # clean up First Live Birth age

        #newlivebirth = 0
        #if FirstLiveBirthAge == 0:
        #    newlivebirth = 2
        #elif FirstLiveBirthAge > 0
        #    if FirstLiveBirthAge < 20 or FirstLiveBirthAge == 99:
        #        newlivebirth = 0
        #    elif 20 <= FirstLiveBirthAge < 25:

        return self.CalculateRisk(riskindex,CurrentAge,ProjectionAge, ageindicator, NumberOfBiopsy,
                                  MenarcheAge, FirstLiveBirthAge, everhadbiopsy, FirstDegRelatives, hyperplasia,
                                  realHyp, race)




    '''
    Line 755 BCPT.cs
    private double CalculateRisk(...)
    '''
    def CalculateRisk(self,
                      riskindex,            # int    [1 = Abs, 2 = Ave]
                      CurrentAge,           # int    [t1]
                      ProjectionAge,        # int    [t2]
                      AgeIndicator,         # int    [i0]
                      NumberOfBiopsy,       # int    [i2]
                      MenarcheAge,          # int    [i1]
                      FirstLiveBirthAge,    # int    [i3]
                      EverHadBiopsy,        # int    [iever]
                      FirstDegRelatives,    # int    [i4]
                      ihyp,                 # int    [ihyp]  HyperPlasia
                      rhyp,                 # double [rhyp]  RHyperPlasia
                      irace                 # int    [race]
                    ):

        # print "CalculateRisk: riskindex: %d" % riskindex
        # print "CalculateRisk: CurrentAge: %d" % CurrentAge
        # print "CalculateRisk: ProjectionAge: %d" % ProjectionAge
        # print "CalculateRisk: AgeIndicator: %d" % AgeIndicator
        # print "CalculateRisk: NumberOfBiopsy: %d" % NumberOfBiopsy
        # print "CalculateRisk: MenarcheAge: %d" % MenarcheAge
        # print "CalculateRisk: FirstLiveBirthAge: %d" % FirstLiveBirthAge
        # print "CalculateRisk: EverHadBiopsy: %d" % EverHadBiopsy
        # print "CalculateRisk: FirstDegRelatives: %d" % FirstDegRelatives
        # print "CalculateRisk: ihyp: %d" % ihyp
        # print "CalculateRisk: rhyp: %f" % rhyp
        # print "CalculateRisk: irace: %d" % irace

        # Local Variables
        retval = np.float64(0.0)

        i = 0  # SRMOORE: no initalizer needed as we use in for loops and such.
        j = 0
        k = 0
        n = 0
        r = np.float64(0.0)
        ni = 0
        ti = np.float64(0.0)
        ns = 0
        ts = np.float64(0.0)
        abss = np.float64(0.0)
        incr = 0
        ilev = 0
        r8iTox2 = np.zeros((self.NumCovPattInGailModel,9),dtype=np.float64)
        n = self.NumCovPattInGailModel
        r = np.float64(0.0)

        # // HACK (According to BCPT.cs line 795)
        # setting ni and ns to 0
        # TODO: SRMOORE: Move these to the variable initaliziers up above. Leaving here for parity with original
        ti = np.float64(CurrentAge)
        ts = np.float64(ProjectionAge)

        '''
        /*11/29/2007 SR: setting BETA to race specific lnRR*/
        '''
        for i in range(8):
            self.bet[i] = self.bet2[i, irace - 1]   # //index starts from 0 hence irace-1

        '''
        /*11/29/2007 SR: recode agemen for African American women*/
        '''
        if irace == 2:
            if MenarcheAge == 2:
                MenarcheAge = 1         # // recode agemen=2 (age<12) to agmen=1 [12,13]
                FirstLiveBirthAge = 0   # // set age 1st live birth to 0

        ''' Line 821 BCPT.cs '''
        for i in range(1,16):   # for (i = 1; i <= 15, i++)
            # /* i-1=14 ==> current age=85, max for curre */
            if ti < self.t[i - 1]:
                # //TODO CHECK THE INDEX (From original)
                ni = i - 1  # /* ni holds the index for current */
                break       # //goto L70    (This is from the original. figure out where this is supposed to go

        for i in range(1,16):
            if ts <= self.t[i - 1]:
                # //!!!TODO CHECK THE INDEX (From original)
                ns = i - 1
                break
        incr = 0
        if riskindex == 2 and irace < 7:
            # //HACK CHECK THIS  (From original Line 843 )
            incr = 3

        '''
        /* for race specific "avg women" */
        /* otherwise use cols 1,2,3 depen */
        /* on users race                5 */
        /* use cols 4,5,6 from rmu, rla */

        //TODO Check this
        /* select race specific */
        '''
        # cindx = 0   # //column index  TODO SRMOORE: optimize this, get rid of the initialization here
        cindx = incr + irace - 1

        for i in range(14):
            self.rmu[i] = self.rmu2[i, cindx]       # /* competeing baseline h */
            self.rlan[i] = self.rlan2[i, cindx]     # /* br ca composite incid */

        # Line 868 BCPT.cs
        self.rf[0] = self.rf2[0, incr + irace - 1]  # /* selecting correct fac */
        self.rf[1] = self.rf2[1, incr + irace - 1]  # /* based on race */

        if riskindex == 2 and irace >= 7:
            self.rf[0] = self.rf2[0, 12] # /* selecting correct fac */
            self.rf[1] = self.rf2[1, 12] # /* based on race */

        # Line 877 BCPT.cs
        if riskindex >= 2:  # //&& irace < 7)  (From original)
            # /* set risk factors to */
            MenarcheAge = 0         # // baseline age menarchy
            NumberOfBiopsy = 0      # //  # of previous biop
            FirstLiveBirthAge = 0   # // age 1st live birth
            FirstDegRelatives = 0   # //  # 1st degree relat
            rhyp = np.float64(1.0)  # // set hyperplasia to 1.0

        ilev = AgeIndicator * 108 + MenarcheAge * 36 + NumberOfBiopsy * 12 + FirstLiveBirthAge * 3 \
               + FirstDegRelatives + 1  # /* matrix of */

        ''' Line 889 of BCPT.cs
         /* covariate */
        /* range of 1 */
        /* AgeIndicator: age ge 50 ind  0=[20, 50) */
        /*                    1=[50, 85) */
        /* MenarcheAge: age menarchy   0=[14, 39] U 99 (unknown) */
        /*                    1=[12, 14) */
        /*                    2=[ 7, 12) */
        /* NumberOfBiopsy: # biopsy       0=0 or (99 and ever had biopsy=99 */
        /*                    1=1 or (99 and ever had biopsy=1 y */
        /*                    2=[ 2, 30] */
        /* FirstLiveBirthAge: age 1st live   0=<20, 99 (unknown) */
        /*                    1=[20, 25) */
        /*                    2=[25, 30) U 0 */
        /*                    3=[30, 55] */
        /* FirstDegRelatives: 1st degree rel 0=0, 99 (unknown) */
        /*                    1=1 */
        /*                    2=[2, 31] */
        /* **  Correspondence between exposure level and covariate factors X */
        /* **  in the logistic model */
        /* **  i-to-X correspondence */
        /* index in r8i */
        '''
        for k in range(self.NumCovPattInGailModel):  # Note: I've been using NumCovPattInGailModel when I see 216
            # /* col1: intercept o */
            r8iTox2[k, 0] = np.float64(1.0)

        for k in range(108):    # really is NumCovPattInGailModel / 2
            # /* col2: indicator for age */
            r8iTox2[k, 1] = np.float64(0.0)
            r8iTox2[108 + k, 1] = np.float(1.0)

        for j in range(1, 3):       # note, since we always subtract 1 from j and k, we could zero base these
            # /* col3: age menarchy cate */
            for k in range(1, 37):
                r8iTox2[(j - 1) * 108 + k - 1, 2] = np.float64(0.0)
                r8iTox2[(j - 1) * 108 + 36 + k - 1, 2] = np.float64(1.0)
                r8iTox2[(j - 1) * 108 + 72 + k - 1, 2] = np.float64(2.0)

        for j in range(1,7):
            # /* col4: # biopsy cate */
            for k in range(1,13):
                r8iTox2[(j - 1) * 36 + k - 1, 3] = np.float64(0.0)
                r8iTox2[(j - 1) * 36 + 12 + k - 1, 3] = np.float64(1.0)
                r8iTox2[(j - 1) * 36 + 24 + k - 1, 3] = np.float64(2.0)

        for j in range(1,19):
            # /* col5: age ist live birt */
            for k in range(1,4):
                r8iTox2[(j - 1) * 12 + k - 1, 4] = np.float64(0.0)
                r8iTox2[(j - 1) * 12 + 3 + k - 1, 4] = np.float64(1.0)
                r8iTox2[(j - 1) * 12 + 6 + k - 1, 4] = np.float64(2.0)
                r8iTox2[(j - 1) * 12 + 9 + k - 1, 4] = np.float64(3.0)

        for j in range(1,73):
            # /* col6: # 1st degree re */
            r8iTox2[(j - 1) * 3 + 1 - 1, 5] = np.float64(0.0)
            r8iTox2[(j - 1) * 3 + 2 - 1, 5] = np.float64(1.0)
            r8iTox2[(j - 1) * 3 + 3 - 1, 5] = np.float64(2.0)

        for i in range(216):
            '''
            /* col8: age 1st live*# r */
            /* col7: age*#biop intera */
            '''
            r8iTox2[i, 6] = r8iTox2[i, 1] * r8iTox2[i, 3]
            r8iTox2[i, 7] = r8iTox2[i, 4] * r8iTox2[i, 5]

            # Consolidating for loop at Line 967 BCPT.cs
            # //HACK r8iTox2[i + 1727] = 1.0;
            r8iTox2[i, 8] = np.float64(1.0)

        ''' Line 974 BCPT.cs
        /* **  Computation of breast cancer risk */
        /* **  sum(bi*Xi) for all covariate patterns */
        '''
        for i in range(self.NumCovPattInGailModel):
            self.sumb[i] = np.float64(0)
            for j in range(8):
                self.sumb[i] += self.bet[j] * r8iTox2[i, j]
        # Line 985 BCPT.cs
        for i in range(1,109):
            # /* eliminate int */
            self.sumbb[i - 1] = self.sumb[i - 1] - self.bet[0]
        for i in range(109,self.NumCovPattInGailModel+1):
            # /* eliminate intercept */
            self.sumbb[i - 1] = self.sumb[i - 1] - self.bet[0] - self.bet[1]
        # Line 995 BCPT.cs
        for j in range(1,7):
            # /* age specific baseline hazard */
            self.rlan[j - 1] *= self.rf[0]
        for j in range(7,15):
            # /* age specific baseline hazard */
            self.rlan[j - 1] *= self.rf[1]

        i = ilev  # Local Variable for function
        ''' /* index ilev of range 1- */
        /* setting i to covariate p */
        // HACK CHECK LOG VALUE
        Original: Line 1008
        sumbb[i - 1] += Math.Log(rhyp);'''
        self.sumbb[i - 1] += np.log(rhyp)
        if i <= 108:
            self.sumbb[i + 107] += np.log(rhyp)

        if ts <= self.t[ni]:
            '''
            /* same 5 year age risk in */
            /* age & projection age wi */
            '''
            self.abs[i - 1] = np.float64(1) - np.exp(-(self.rlan[ni - 1] * np.exp(self.sumbb[i - 1]) +
                                                       self.rmu[ni - 1]) * (ts - ti))

            self.abs[i - 1] = self.abs[i - 1] * self.rlan[ni - 1] \
                              * np.exp(self.sumbb[i - 1]) / (self.rlan[ni - 1] * np.exp(self.sumbb[i - 1])
                                                             + self.rmu[ni - 1])  # /* breast cance */

        else:  # Line 1025 BCPT.cs
            '''
            /* 5 year age risk interval */
            /* calculate risk from */
            /* 1st age interval */
            /* age & projection age not i */
            '''
            self.abs[i - 1] = 1.0 - np.exp(-(self.rlan[ni - 1] * np.exp(self.sumbb[i - 1])
                                             + self.rmu[ni - 1]) * (self.t[ni] - ti))
            self.abs[i - 1] = self.abs[i - 1] * self.rlan[ni - 1] * np.exp(self.sumbb[i - 1]) \
                             / (self.rlan[ni - 1] * np.exp(self.sumbb[i - 1]) + self.rmu[ni - 1])  # /* age in */
            ''' /* risk f */'''
            if ns - ni > 0:
                if np.float64(ProjectionAge) > np.float64(50.0) and np.float64(CurrentAge) < np.float64(50.0):
                    ''' Line 1041 BCPT.cs
                    /* a */
                    /* s */
                    /* a */
                    /* calculate ris */
                    /* last age inte */
                    '''
                    r = np.float64(1.0) - np.exp(-(self.rlan[ns - 1] * np.exp(self.sumbb[i + 107]) + self.rmu[ns - 1])
                                                 * (ts - self.t[ns - 1]))
                    r = r * self.rlan[ns - 1] * np.exp(self.sumbb[i + 107]) / (self.rlan[ns - 1]
                                                                               * np.exp(self.sumbb[i + 107])
                                                                               + self.rmu[ns - 1])
                    r *= np.exp(-(self.rlan[ni - 1] * np.exp(self.sumbb[i - 1])
                                  + self.rmu[ni - 1]) * (self.t[ni] - ti))

                    if ns - ni > 1:  # Line 1060 BCPT.cs
                        MenarcheAge = ns - 1
                        for j in range(ni + 1, MenarcheAge + 1):
                            if self.t[j -1] >= np.float64(50.0):
                                r *= np.exp(-(self.rlan[j - 1] * np.exp(self.sumbb[i + 107]) + self.rmu[j - 1])
                                            * (self.t[j] - self.t[j - 1]))
                            else:
                                r *= np.exp(-(self.rlan[j - 1] * np.exp(self.sumbb[i - 1]) + self.rmu[j - 1])
                                            * (self.t[j] - self.t[j - 1]))
                    self.abs[i - 1] += r
                # Line 1081 BCPT.cs
                else:  # close: if np.float64(ProjectionAge) > np.float64(50.0) and np.float64(CurrentAge) < 50
                    '''
                    /* calculate risk from */
                    /* last age interval */
                    /* ages do not stradle */
                    '''
                    r = np.float64(1.0) - np.exp(-(self.rlan[ns - 1] * np.exp(self.sumbb[i - 1])
                                                   + self.rmu[ns - 1]) * (ts - self.t[ns - 1]))
                    r = r * self.rlan[ns - 1] * np.exp(self.sumbb[i - 1]) / (self.rlan[ns - 1]
                                                                             * np.exp(self.sumbb[i - 1])
                                                                             + self.rmu[ns - 1])
                    r *= np.exp(-(self.rlan[ni - 1] * np.exp(self.sumbb[i - 1]) + self.rmu[ni - 1])
                                * (self.t[ni] - ti))
                    if ns - ni > 1:
                        MenarcheAge = ns - 1
                        for j in range(ni + 1, MenarcheAge + 1):
                            r *= np.exp(-(self.rlan[j - 1] * np.exp(self.sumbb[i -1]) + self.rmu[j - 1])
                                        * (self.t[j] - self.t[j - 1]))
                    self.abs[i - 1] += r

            if ns - ni > 1: # Line 1106 BCPT.cs
                if np.float64(ProjectionAge) > np.float64(50.0) and np.float64(CurrentAge) < np.float64(50.0):
                    '''
                    /* calculate risk from */
                    /* intervening age int */
                    '''
                    MenarcheAge = ns -1
                    for k in range(ni + 1, MenarcheAge + 1):
                        if self.t[k - 1] >= np.float64(50.0):   # Line 1115 BCPT.cs
                            r = 1.0 - np.exp(-(self.rlan[k - 1] * np.exp(self.sumbb[i + 107]) + self.rmu[k - 1])
                                             * (self.t[k] - self.t[k - 1]))
                            r = r * self.rlan[k - 1] * np.exp(self.sumbb[i + 107]) / (self.rlan[k - 1]
                                                                                      * np.exp(self.sumbb[i + 107])
                                                                                      + self.rmu[k - 1])
                        else:   # Line 1124 BCPT.cs
                            r = 1.0 - np.exp(-(self.rlan[k - 1] * np.exp(self.sumbb[i - 1]) + self.rmu[k - 1])
                                             * (self.t[k] - self.t[k - 1]))
                            r = r * self.rlan[k - 1] * np.exp(self.sumbb[i - 1]) / (self.rlan[k - 1]
                                                                                    * np.exp(self.sumbb[i - 1])
                                                                                    + self.rmu[k - 1])

                        r *= np.exp(-(self.rlan[ni - 1] * np.exp(self.sumbb[i - 1])
                                      + self.rmu[ni - 1]) * (self.t[ni] - ti))
                        NumberOfBiopsy = k - 1
                        for j in range(ni + 1, NumberOfBiopsy + 1): # Line 1136 BCPT.cs
                            if self.t[j - 1] >= np.float64(50.0):
                                r *= np.exp(-(self.rlan[j - 1] * np.exp(self.sumbb[i + 107])
                                              + self.rmu[j - 1]) * (self.t[j] - self.t[j - 1]))
                            else:
                                r *= np.exp(-(self.rlan[j - 1] * np.exp(self.sumbb[i - 1])
                                              + self.rmu[j - 1]) * (self.t[j] - self.t[j - 1]))
                        # End for j in range...
                        self.abs[i - 1] += r
                else:   # Line 1154 BCPT.cs
                    '''
                    /* calculate risk from */
                    /* intervening age int */
                    '''
                    MenarcheAge = ns - 1
                    for k in range(ni + 1, MenarcheAge + 1):
                        r = 1.0 - np.exp(-(self.rlan[k - 1] * np.exp(self.sumbb[i - 1])
                                           + self.rmu[k - 1]) * (self.t[k] - self.t[k - 1]))
                        r = r * self.rlan[k - 1] * np.exp(self.sumbb[i - 1]) / \
                            (self.rlan[k - 1] * np.exp(self.sumbb[i - 1]) + self.rmu[k - 1])
                        r *= np.exp(-(self.rlan[ni - 1] * np.exp(self.sumbb[i - 1]) + self.rmu[ni - 1])
                                    * (self.t[ni] - ti))
                        NumberOfBiopsy = k - 1
                        for j in range(ni + 1, NumberOfBiopsy + 1):
                            r *= np.exp(-(self.rlan[j - 1] * np.exp(self.sumbb[i - 1]) + self.rmu[j - 1])
                                        * (self.t[j] - self.t[j - 1]))
                        self.abs[i - 1] += r
        # End of if ts <= self.t[ni]: else
        ''' Line 1185 BCPT.cs
        Leaving the following code out as 'abss' is only used for rounding the number to print to console
        in the original code. TODO: SRMOORE should we put this back in?
        abss = self.abs[i - 1] * np.float64(1000.0)
        //HACK CHECK THIS (From original):
        if (abss - (int)(abss) >= .5f)
        {
            //abss = d_int(abss) + 1.0 ;
            abss = (int)(abss) + 1.0;
        }
        else
        {
            abss = (int)(abss);
        }
        abss /= 10.0;

        It seems they are trying to round the number using .5 to decide if it should go up or down,
            then deviding it by 10
        '''
        return self.abs[i - 1]  # End def CalculateRisk(...)

    ''' The folowing code isn't needed unless we want to mimic BCPT.cs's printing to console:

        public static void PrintArray(double[] o, string Name)
        {
            Console.WriteLine("------------------Contents of {0}", Name);
            foreach (double d in o)
            {
                Console.WriteLine(string.Format("{0}", d.ToString("F5")));
            }
        }

        public static void PrintArray2(double[,] o, string Name)
        {
            Console.WriteLine("------------------Contents of {0}", Name);
            for (int i = 0; i <= o.GetUpperBound(0); ++i)
            {
                for (int j = 0; j <= o.GetUpperBound(1); ++j)
                {
                    Console.Write(string.Format("{0} ", o[i, j].ToString("F2")));
                }
                Console.WriteLine();
            }
        }
    '''

if __name__ == '__main__':
    gailMod = GailRiskCalculator()
    gailMod.Initialize()
    print gailMod.CalculateRisk(1,  # riskIndex int    [1 = Abs, 2 = Ave]
                  35,  # CurrentAge int    [t1]
                  40,  # ProjectionAge int    [t2]
                  0,  # AgeIndicator int    [i0]
                  1,  # NumberOfBiopsy int    [i2]
                  2,  # MenarcheAge int    [i1]
                  0,  # FirstLiveBirthAge int    [i3]
                  1,  # EverHaveBiopsy int    [iever]
                  0,  # FirstDegRelatives int    [i4]
                  1,  # int    [ihyp]  HyperPlasia
                  np.float64(1.82),  # double [rhyp]  RHyperPlasia
                  1  # irace int    [race]
                  )
