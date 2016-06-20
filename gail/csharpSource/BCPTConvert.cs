using System;
using System.Text;
using System.Xml;

namespace NCI.DCEG.BCRA.Engine
{
    /// <summary>
    /// Enumerator for the race/ethnicity
    /// </summary>
    public enum BcptRace
    {
        White = 1, Black = 2, Hispanic = 3, AAChinese = 7, AAJapanese = 8, AAFilipino = 9, AAHawaiian = 10, AAOtherPacificIslander = 11, AAOtherAsianAmerican = 12
    }

    /// <summary>
    /// Has static methods for converting/recoding values passed from ui or test harness 
    /// </summary>
    public class BcptConvert
    {
        private const string _UNKNOWN = "UNKNOWN";
        private const string _UDERSCORE = "__";
        private const string _EMPTY = "";
        private const string _YES = "YES";
        private const string _NO = "NO";
        private const string _NA = "NA";
        private const string _0BIRTHS = "0 BIRTHS";	//appears in menarche 

        /// <summary>
        /// Returns current age
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public static int GetCurrentAge(object o)
        {
            int rval;
            switch (o.ToString().ToUpper())
            {
                case _UNKNOWN:
                case _UDERSCORE:
                case _EMPTY:
                case _NA:
                    rval = 90;
                    break;
                case "< 35":
                case "<35":
                    rval = 34;
                    break;
                default:
                    rval = Convert.ToInt32(o);
                    break;
            }
            return rval;
        }

        /// <summary>
        /// Returns Projection Age
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public static int GetProjectionAge(string o)
        {
            int rval;
            switch (o.Trim().ToUpper())
            {
                case _UNKNOWN:
                case _UDERSCORE:
                case _EMPTY:
                case _NA:
                    rval = 90;
                    break;
                default:
                    rval = Convert.ToInt32(o);
                    break;
            }
            return rval;
        }

        /// <summary>
        /// Returns Menarche Age
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public static int GetMenarcheAge(string o)
        {
            int rval;
            switch (o.Trim().ToUpper())
            {
                case _UNKNOWN:
                case _UDERSCORE:
                case _EMPTY:
                case _NA:
                case _0BIRTHS:
                    rval = 99;
                    break;
                case "7 TO 11":
                    rval = 10;
                    break;
                case "12 TO 13":
                    rval = 13;
                    break;
                case "> 13":
                    rval = 15;
                    break;
                default:
                    rval = Convert.ToInt32(o);
                    break;
            }
            //HACK CHECK AND UNCOMMENT THIS BEFORE BUILDING TO QA/PROD
            //if (rval < 7 || rval > 39 && rval != 99)
            //{
            //    string ERR_MENARCHE_1 = "!!! ERROR CONDITION !!! Menarche age coded as:   {0}. Valid menarche ages are 7 thru 39.";
            //    throw new Exception(string.Format(ERR_MENARCHE_1, rval));
            //}
            return rval;

        }

        /// <summary>
        /// Returns First Live BirthAge
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public static int GetFirstLiveBirthAge(string o)
        {
            int rval;
            switch (o.Trim().ToUpper())
            {
                case _UNKNOWN:
                case _UDERSCORE:
                case _EMPTY:
                case _NA:
                    rval = 99;
                    break;
                case "NO BIRTHS":
                    rval = 0;
                    break;
                case "< 20":
                    rval = 15;
                    break;
                case "20 TO 24":
                    rval = 22;
                    break;
                case "25 TO 30":
                    rval = 27;
                    break;
                case "> 30":
                    rval = 31;
                    break;
                default:
                    rval = Convert.ToInt32(o);
                    break;
            }
            //HACK UNCOMMENT THIS BEFORE BUILDING TO QA/PROD
            //if (rval <= 10)
            //{
            //    string ERR_FLB_1 = "!!! ERROR CONDITION !!! Age of 1st live birth coded as: {0} Outside of valid range of 10 to 55.";
            //    throw new Exception(string.Format(ERR_FLB_1, rval));
            //}

            return rval;
        }

        /// <summary>
        /// Returns Number First Degree Relatives
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public static int GetFirstDegRelatives(string o)
        {
            int rval;
            switch (o.Trim().ToUpper())
            {
                case _UNKNOWN:
                case _UDERSCORE:
                case _EMPTY:
                case _NA:
                    rval = 99;
                    break;
                case "0":
                    rval = 0;
                    break;
                case "1":
                    rval = 1;
                    break;
                case "> 1":
                    rval = 2;
                    break;
                default:
                    rval = Convert.ToInt32(o);
                    break;
            }
            return rval;
        }

        /// <summary>
        /// Returns whether the person Ever Had Biopsy
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public static int GetEverHadBiopsy(string o)
        {
            int rval = 99;
            switch (o.Trim().ToUpper())
            {
                case _UNKNOWN:
                case _UDERSCORE:
                case _EMPTY:
                case _NA:
                    rval = 99;
                    break;
                case _NO:
                case "0":
                    rval = 0;
                    break;
                case _YES:
                case "1":
                    rval = 1;
                    break;
                //default:
                //    rval = Convert.ToInt32(o);
                //    break;
            }
            return rval;
        }

        /// <summary>
        /// Returns Number of Biopsy
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public static int GetNumberOfBiopsy(string o)
        {
            int rval;
            switch (o.Trim().ToUpper())
            {
                case _UNKNOWN:
                case _UDERSCORE:
                case _EMPTY:
                case _NA:
                    rval = 99;
                    break;
                case "1":
                    rval = 1;
                    break;
                case "> 1":
                    rval = 2;
                    break;
                default:
                    rval = Convert.ToInt32(o);
                    break;
            }
            return rval;
        }

        /// <summary>
        /// Returns whether the person had Hyper Plasia or not
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public static int GetHyperPlasia(string o)
        {
            int rval;
            switch (o.Trim().ToUpper())
            {
                case _UNKNOWN:
                case _UDERSCORE:
                case _EMPTY:
                case _NA:
                    rval = 99;
                    break;
                case _NO:
                    rval = 0;
                    break;
                case _YES:
                    rval = 1;
                    break;
                default:
                    rval = Convert.ToInt32(o);
                    break;
            }
            return rval;
        }

        /// <summary>
        /// Returns race/ethnicity 
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public static int GetRace(string o)
        {
            BcptRace rval;
            switch (o.ToString().Trim().ToUpper())
            {
                case "WHITE":
                case _UNKNOWN:
                case "1":
                case "4":   //! recode other race to white 5/12/00
                    rval = BcptRace.White;
                    break;
                case "BLACK":
                case "2":
                    rval = BcptRace.Black;
                    break;
                case "HISPANIC":
                case "3":
                    rval = BcptRace.Hispanic;
                    break;
                case "7":
                    rval = BcptRace.AAChinese;
                    break;
                case "8":
                    rval = BcptRace.AAJapanese;
                    break;
                case "9":
                    rval = BcptRace.AAFilipino;
                    break;
                case "10":
                    rval = BcptRace.AAHawaiian;
                    break;
                case "11":
                    rval = BcptRace.AAOtherPacificIslander;
                    break;
                case "12":
                    rval = BcptRace.AAOtherAsianAmerican;
                    break;
                default:
                    rval = BcptRace.White;
                    break;
            }
            return (int)rval;
        }
        /// <summary>
        /// Returns Current Age Indicator/Index
        /// </summary>
        /// <param name="currentAge"></param>
        /// <returns></returns>
        public static int CurrentAgeIndicator(int currentAge)
        {
            int rval = 0;
            if (currentAge < 50)
                rval = 0;
            else if (currentAge >= 50)
                rval = 1;
            return rval;
        }

        /// <summary>
        /// gets the menarche age
        /// </summary>
        /// <param name="menarcheAge"></param>
        /// <returns></returns>
        public static int MenarcheAge(int menarcheAge)
        {
            int rval = 0;
            if (menarcheAge >= 7 && menarcheAge < 12)
                rval = 2;
            else if (menarcheAge >= 12 && menarcheAge < 14)
                rval = 1;
            else if (menarcheAge >= 14 && menarcheAge <= 39 || menarcheAge == 99)
                rval = 0;
            return rval;
        }

        /// <summary>
        /// Returns First Live Birth Age
        /// </summary>
        /// <param name="firstLiveBirthAge"></param>
        /// <returns></returns>
        public static int FirstLiveBirthAge(int firstLiveBirthAge)
        {
            int rval = 0;
            if (firstLiveBirthAge == 0)
            {
                // no live birth
                rval = 2;
            }
            else if (firstLiveBirthAge > 0)
            {
                if (firstLiveBirthAge < 20 || firstLiveBirthAge == 99)       // includes unknown
                    rval = 0;
                else if (firstLiveBirthAge >= 20 && firstLiveBirthAge < 25)
                    rval = 1;
                else if (firstLiveBirthAge >= 25 && firstLiveBirthAge < 30)
                    rval = 2;
                else if (firstLiveBirthAge >= 30 && firstLiveBirthAge <= 55)
                    rval = 3;
            }
            return rval;
        }

        /// <summary>
        /// Returns Number of first degree relatives
        /// </summary>
        /// <param name="firstDegRelatives"></param>
        /// <returns></returns>
        public static int FirstDegRelatives(int firstDegRelatives)
        {
            int rval = 0;
            if (firstDegRelatives == 0 || firstDegRelatives == 99)
                rval = 0;
            else if (firstDegRelatives == 1)
                rval = 1;
            else if (firstDegRelatives >= 2 && firstDegRelatives <= 31)
                rval = 2;
            return rval;
        }

        /// <summary>
        /// Returns Number of first degree relatives based on race
        /// </summary>
        /// <param name="firstDegRelatives"></param>
        /// <returns></returns>
        public static int FirstDegRelatives(int firstDegRelatives, int race)
        {
            int rval = 0;
            if (firstDegRelatives == 0 || firstDegRelatives == 99)
                rval = 0;
            else if (firstDegRelatives == 1)
                rval = 1;
            else if (firstDegRelatives >= 2 && firstDegRelatives <= 31 && race < 7)
                rval = 2;
            else if (firstDegRelatives >= 2 && race >= 7)
                rval = 1;
            return rval;
        }
        /// <summary>
        /// Returns whether a woman ever had biopsy or not
        /// </summary>
        /// <param name="everHadBiopsy"></param>
        /// <returns></returns>
        public static int EverHadBiopsy(int everHadBiopsy)
        {
            int rval = 0;
            switch (everHadBiopsy)
            {
                case 99:
                    //case 0:
                    rval = 0;
                    break;
                default:
                    rval = everHadBiopsy;
                    break;
            }
            return rval;
        }

        /// <summary>
        /// Returns Number Of Biopsies
        /// </summary>
        /// <param name="numberOfPreviousBiopsy"></param>
        /// <param name="everHadBiopsy"></param>
        /// <returns></returns>
        public static int NumberOfBiopsy(int numberOfPreviousBiopsy, int everHadBiopsy)
        {
            int rval = 0;
            if (everHadBiopsy == 99)
                rval = 99;
            else if (numberOfPreviousBiopsy == 0 || (numberOfPreviousBiopsy == 99 && everHadBiopsy == 99))
                rval = 0;
            else if (numberOfPreviousBiopsy == 1 || (numberOfPreviousBiopsy == 99 && everHadBiopsy == 1))
                rval = 1;
            else if (numberOfPreviousBiopsy > 1 && numberOfPreviousBiopsy <= 30)
                rval = 2;
            return rval;
        }

        /// <summary>
        /// Returns Hyperlasia value
        /// </summary>
        /// <param name="hyperplasia"></param>
        /// <param name="everHadBiopsy"></param>
        /// <returns></returns>
        public static int Hyperplasia(int hyperplasia, int everHadBiopsy)
        {
            int rval;
            if (everHadBiopsy == 0)
                rval = 99;
            else
            {
                switch (hyperplasia)
                {
                    default:
                        rval = hyperplasia;
                        break;
                }
            }
            return rval;
        }

        /// <summary>
        /// Returns RHyperplasia value
        /// </summary>
        /// <param name="hyperplasia"></param>
        /// <param name="everHadBiopsy"></param>
        /// <returns></returns>
        public static double RHyperplasia(int hyperplasia, int everHadBiopsy)
        {
            double rval;
            //if (everHadBiopsy == 0) hyperplasia = 0;
            switch (hyperplasia)
            {
                case 1:			// hyperplasia=yes
                    rval = 1.82;
                    break;
                case 0:			// hyperplasia=no
                    rval = 0.93;
                    break;
                default:		// hyperplasia=never had biopsy
                    rval = 1.0;
                    break;
            }
            return rval;
        }

    }

}
