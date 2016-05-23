import numpy as np

class GailRiskCalculator:
    NumCovPattInGailModel = 216

    def __init__(self):
        self.bet2 = np.zeros((8,3),dtype=np.float64)
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


