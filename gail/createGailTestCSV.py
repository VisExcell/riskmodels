import sys
import numpy as np
import gail
import csv

'''
File to create a CSV file of all possible inputs to the GAIL model.
This can be used to test the python file against the original C# or other GAIL models
'''


def main():
    # TODO: Validate if these valuse are correct From paper?
    raceValues = [1,  # White, other
                  2,  # African American
                  3,  # Hispanic
                  # From BCPTConvert 4, 5 , and 6 are not used?
                  # 4,  # Asian-American
                  # 5,  # American Indian or Alaskan Native
                  # 6,  # Unknown
                  7,  # Chinese
                  8,  # Japanese
                  9,  # Filipino
                  10,  # Hawaiian
                  11,  # Other Pacific Islander
                  12]  # Other Asian-American
    ''' The following hits all the ranges plus 99 for unknown or no births.
        In normal usage, you'd just pass in the age (7 through 39) or 99 for none '''
    # menarchValues = [99,    # Unknown, Empty, zero briths?? from docs
    #                 10,    # 7 to 11
    #                 13,    # 12 to 13
    #                 15]    # > 15
    menarchValues = [2, # 7 to 11
                     1, # 12 to 13
                     0] # >= 14, <= 39 or 99 (unknown)

    ageStart = 35   # GAIL doesn't actually work for under 35
    ageStop = 86   # GAIL stops at 85 (predictions up to 90)
    ageValues = range(ageStart,ageStop)  # could potentially just use the bracketed ages for testing...

    ''' The following hits all the ranges plus 99 for unknown or no births.
        In normal usage, you'd just pass in the age (10 through 55) or 99 for unknown, 0 for none '''
    # liveBirthAgeValues = [99,   # Unknown/empty
    #                     0,    # No Births
    #                      15,   # < 20
    #                      22,   # 20 to 24
    #                      27,   # 25 to 30
    #                      31]   # > 30
    liveBirthAgeValues = [0,    # <20 or unknown
                          1,    # >= 20, < 25
                          2,    # >= 25, < 30 or no birth
                          3]    # >=30 <= 55

    ''' First Deg Relatives coding '''
    numRelativesValues = [0,    # zero or unknown (99)
                          1,    # one
                          2]    # more than one

    ''' Ever had a biopsy? '''
    biopsyVals = [0,    # No or Unknown (99)
                  1]    # Yes

    ''' How many biopsies?'''
    #numBiopsyVals = [0,     # zero of unknown and never had biopsy
    #                 1,     # One or had biopsy but unknown number
    #                 2]     # More than one
    #
    # Since we'retaking care of no biopsies seperatly, these will only have the yes I've had a biopsy values for loops

    numBiopsyVals = [1,  # One or had biopsy but unknown number
                     2]  # More than one

    ''' any of the biopsies with Hyper Plasia?'''
    # These don't actually get used, so I'll just set it to something below.
    #ihyperplasiaVals = [99,  # unknown
    #                   0,   # No
    #                   1]   # yes



    ''' Calculator only uses the 'real value' for hyperplasia... could convert this in the model'''
    rhypValues = [np.float64(1.82),     # hyperplasia = yes
                  np.float64(0.93),     # hyperplasia = no
                  np.float64(1.0)]      # never had biopsy/unknown

    # Set up the model and csv writer
    gailModel = gail.GailRiskCalculator()
    gailModel.Initialize()

    print "Gail Model initalized, begining looping"

    with open('/tmp/gailTestOutput.csv','wb') as outputfile:
        outputwriter = csv.writer(outputfile)
        '''Loop through values'''
        for irace in raceValues:
            for age in ageValues:
                if age > 49 :
                    ageInd = 1
                else:
                    ageInd = 0
                for menarch in menarchValues:
                    for livebirthage in liveBirthAgeValues:
                        for numrelatives in numRelativesValues:
                            # Biopsy values depend on yes/no on ever had biopsy question.
                            currentRowBase = [irace,age,menarch,livebirthage,numrelatives]
                            # No Biopsy (or unknown)
                            currentRow = currentRowBase + [0, 0, 0, np.float64(1.0)]
                            fiveYearRiskAbs = gailModel.CalculateAbsoluteRisk(currentRow[1],
                                                                              currentRow[1] + 5,
                                                                              ageInd,
                                                                              currentRow[5],
                                                                              currentRow[2],
                                                                              currentRow[3],
                                                                              currentRow[6],
                                                                              currentRow[4],
                                                                              currentRow[7],
                                                                              currentRow[8],
                                                                              currentRow[0])
                            fiveYearRiskAve = gailModel.CalculateAeverageRisk(currentRow[1],
                                                                              currentRow[1] + 5,
                                                                              ageInd,
                                                                              currentRow[5],
                                                                              currentRow[2],
                                                                              currentRow[3],
                                                                              currentRow[6],
                                                                              currentRow[4],
                                                                              currentRow[7],
                                                                              currentRow[8],
                                                                              currentRow[0])
                            lifetimeRiskAbs = gailModel.CalculateAbsoluteRisk(currentRow[1],
                                                                              90,
                                                                              ageInd,
                                                                              currentRow[5],
                                                                              currentRow[2],
                                                                              currentRow[3],
                                                                              currentRow[6],
                                                                              currentRow[4],
                                                                              currentRow[7],
                                                                              currentRow[8],
                                                                              currentRow[0])
                            lifetimeRiskAve = gailModel.CalculateAeverageRisk(currentRow[1],
                                                                              90,
                                                                              ageInd,
                                                                              currentRow[5],
                                                                              currentRow[2],
                                                                              currentRow[3],
                                                                              currentRow[6],
                                                                              currentRow[4],
                                                                              currentRow[7],
                                                                              currentRow[8],
                                                                              currentRow[0])
                            currentRow = currentRow + [fiveYearRiskAbs,fiveYearRiskAve,lifetimeRiskAbs,lifetimeRiskAve]
                            outputwriter.writerow(currentRow)
                            for numbiopsy in numBiopsyVals:
                                for rhyp in rhypValues:
                                    currentRow = currentRowBase + [1,1,numbiopsy,rhyp]
                                    fiveYearRiskAbs = gailModel.CalculateAbsoluteRisk(currentRow[1],
                                                                                      currentRow[1] + 5,
                                                                                      ageInd,
                                                                                      currentRow[5],
                                                                                      currentRow[2],
                                                                                      currentRow[3],
                                                                                      currentRow[6],
                                                                                      currentRow[4],
                                                                                      currentRow[7],
                                                                                      currentRow[8],
                                                                                      currentRow[0])
                                    fiveYearRiskAve = gailModel.CalculateAeverageRisk(currentRow[1],
                                                                                      currentRow[1] + 5,
                                                                                      ageInd,
                                                                                      currentRow[5],
                                                                                      currentRow[2],
                                                                                      currentRow[3],
                                                                                      currentRow[6],
                                                                                      currentRow[4],
                                                                                      currentRow[7],
                                                                                      currentRow[8],
                                                                                      currentRow[0])
                                    lifetimeRiskAbs = gailModel.CalculateAbsoluteRisk(currentRow[1],
                                                                                      90,
                                                                                      ageInd,
                                                                                      currentRow[5],
                                                                                      currentRow[2],
                                                                                      currentRow[3],
                                                                                      currentRow[6],
                                                                                      currentRow[4],
                                                                                      currentRow[7],
                                                                                      currentRow[8],
                                                                                      currentRow[0])
                                    lifetimeRiskAve = gailModel.CalculateAeverageRisk(currentRow[1],
                                                                                      90,
                                                                                      ageInd,
                                                                                      currentRow[5],
                                                                                      currentRow[2],
                                                                                      currentRow[3],
                                                                                      currentRow[6],
                                                                                      currentRow[4],
                                                                                      currentRow[7],
                                                                                      currentRow[8],
                                                                                      currentRow[0])
                                    currentRow = currentRow + [fiveYearRiskAbs, fiveYearRiskAve, lifetimeRiskAbs,
                                                               lifetimeRiskAve]
                                    outputwriter.writerow(currentRow)
    print "done?"

if __name__ == "__main__":
    main()