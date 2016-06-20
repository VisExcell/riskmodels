using System;
using System.Collections.Generic;
using System.Text;
using NCI.DCEG.BCRA.Engine;

namespace NCI.DCEG.BCRA.ConsoleSample
{
    internal static class Helper
    {
        internal static void RiskCalc(
    int riskIndex,
    int currentAge,
    int projectionAge,
    int menarcheAge,
    int firstLiveBirthAge,
    int everHadBiopsy,
    int numberOfBiopsy,
    int hyperPlasia,
    int firstDegRelatives,
    int race,
    out double absoluteRisk,
    out double averageRisk)
        {
            int ageIndicator;
            double rHyperPlasia;

            currentAge = BcptConvert.GetCurrentAge(currentAge);
            menarcheAge = BcptConvert.MenarcheAge(menarcheAge);
            firstLiveBirthAge = BcptConvert.FirstLiveBirthAge(firstLiveBirthAge);
            everHadBiopsy = BcptConvert.EverHadBiopsy(everHadBiopsy);
            numberOfBiopsy = BcptConvert.NumberOfBiopsy(numberOfBiopsy, everHadBiopsy);
            hyperPlasia = BcptConvert.Hyperplasia(hyperPlasia, everHadBiopsy);
            //firstDegRelatives = BcptConvert.FirstDegRelatives(firstDegRelatives);
            race = BcptConvert.GetRace(race.ToString());

            if (race < 7)
                firstDegRelatives = BcptConvert.FirstDegRelatives(firstDegRelatives);
            else
                firstDegRelatives = BcptConvert.FirstDegRelatives(firstDegRelatives, race);

            ageIndicator = BcptConvert.CurrentAgeIndicator(currentAge);
            rHyperPlasia = BcptConvert.RHyperplasia(hyperPlasia, everHadBiopsy);

            riskIndex = 1;  //get absolute risk
            RiskCalculator oBcpt = new RiskCalculator();
            absoluteRisk = oBcpt.CalculateAbsoluteRisk(
                 currentAge		    //[t1]
                , projectionAge		//[t2]
                , ageIndicator		//[i0]
                , numberOfBiopsy	//[i2]
                , menarcheAge		//[i1]
                , firstLiveBirthAge	//[i3]
                , firstDegRelatives	//[i4]
                , everHadBiopsy		//[iever]
                , hyperPlasia		//[ihyp]
                , rHyperPlasia		//[rhyp]
                , race				//[race]
                );
            riskIndex = 2;  //get average risk also
            averageRisk = oBcpt.CalculateAeverageRisk(
                  currentAge		//[t1]
                , projectionAge		//[t2]
                , ageIndicator		//[i0]
                , numberOfBiopsy	//[i2]
                , menarcheAge		//[i1]
                , firstLiveBirthAge	//[i3]
                , firstDegRelatives	//[i4]
                , everHadBiopsy		//[iever]
                , hyperPlasia		//[ihyp]
                , rHyperPlasia		//[rhyp]
                , race				//[race]
                );
        }

        internal static void CalcPercentage(double absoluteRisk, double averageRisk,
                            out double absoluteRiskPctg, out double averageRiskPctg)
        {
            absoluteRisk = Math.Round(absoluteRisk, 6);
            averageRisk = Math.Round(averageRisk, 6);
            absoluteRiskPctg = Math.Round(absoluteRisk * 100, 1);
            averageRiskPctg = Math.Round(averageRisk * 100, 1);
        }
    }
}
