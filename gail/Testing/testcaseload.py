import urllib
import sqlite3
import time
import ssl
import codecs
from bs4 import BeautifulSoup
#import logging



# this program loads the test case file, uses the inputs to encode the cancer.gov risk service URL,
# retrieves the risk scores from the cancer.gov site, and inserts the test and corresponding results value into a DB
# todo auto compare the values, which requires working through rounding in python and/or sql


def writeCancerGovScoretoDB():

    # variables below scraped from cancer.gov site through beautiful soup
    cgvfiveyearRiskABS = -1.1
    cgvfiveyearRiskAVE = -1.1
    cgvLifetimeRiskABS = -1.1
    cgvLifetimeRiskAVE = -1.1

    explainer= ""

    url = serviceurl + urllib.urlencode({"genetics":genetics, "current_age":current_age ,"age_at_menarche":wage_at_menarche,
                                         "age_at_first_live_birth":wage_at_first_live_birth,"ever_had_biopsy":wever_had_biopsy,
                                         "previous_biopsies":previous_biopsies,"biopsy_with_hyperplasia":biopsy_with_hyperplasia,
                                         "related_with_breast_cancer":related_with_breast_cancer,
                                         "race":race})


    #logging.debug('Retrieving: %s' ), url
    time.sleep(0.1) #delays for 1 seconds
    myhtml = urllib.urlopen(url,context=scontext).read()

    soup = BeautifulSoup(myhtml, "lxml")

    tags = soup.find_all('p')
    explainer = explainer + str(tags[7])+str(tags[8])


    tags = soup('span', {'id': 'ctl00_cphMain_lbl5YrAbsoluteRisk'})
    for x in tags: cgvfiveyearRiskABS= (float(x.get_text()[:-1])/100)

    tags = soup('span', {'id': 'ctl00_cphMain_lbl5YrAveragRisk'})
    for x in tags: cgvfiveyearRiskAVE= (float(x.get_text()[:-1])/100)

    tags = soup('span', {'id': 'ctl00_cphMain_lblLifetimeAbsoluteRisk90'})
    for x in tags: cgvLifetimeRiskABS= (float(x.get_text()[:-1])/100)

    tags = soup('span', {'id': 'ctl00_cphMain_lblLifeTimeAverageRisk90'})
    for x in tags: cgvLifetimeRiskAVE= (float(x.get_text()[:-1])/100)

    #print 'count ', count, ':',fiveyearRiskABS, ':',cgvfiveyearRiskABS, ':', LifetimeRiskABS, ':',cgvLifetimeRiskABS
    #print url

    cur.execute('''INSERT INTO GailTestCases (csvlinenum,genetics,current_age,age_at_menarche, age_at_first_live_birth, ever_had_biopsy,previous_biopsies,
    biopsy_with_hyperplasia,floatbiopsy_with_hyperplasia,related_with_breast_cancer,race,
    fiveYearRiskABS,fiveYearRiskAVE,LifetimeRiskABS,LifetimeRiskAVE,
    cgvfiveyearRiskABS,cgvfiveyearRiskAVE,cgvLifetimeRiskABS,cgvLifetimeRiskAVE,explainer) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (count,genetics,current_age,age_at_menarche,age_at_first_live_birth, ever_had_biopsy,previous_biopsies,
                 biopsy_with_hyperplasia,floatbiopsy_with_hyperplasia,related_with_breast_cancer,race,
                 fiveyearRiskABS,fiveyearRiskAVE,LifetimeRiskABS,LifetimeRiskAVE,
                 cgvfiveyearRiskABS, cgvfiveyearRiskAVE,cgvLifetimeRiskABS,cgvLifetimeRiskAVE,explainer))

    conn.commit()

#logging.basicConfig(filename='gailtesting.log', level=logging.DEBUG)
#logging.info('Gail Test Case run @ %s'), time.strftime("%H:%M:%S")

# gail service url
serviceurl = "http://www.cancer.gov/bcrisktool/RiskAssessment.aspx?"

# Deal with SSL certificate anomalies Python > 2.7
# scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
scontext = None

conn = sqlite3.connect('GailServiceTestDB.sqlite')
cur = conn.cursor()

#cur.execute('''DROP TABLE IF EXISTS GailTestCases''')

cur.execute('''CREATE TABLE IF NOT EXISTS GailTestCases
(csvlinenum,genetics,current_age,age_at_menarche, age_at_first_live_birth, ever_had_biopsy,
previous_biopsies,biopsy_with_hyperplasia,floatbiopsy_with_hyperplasia,
related_with_breast_cancer,race,fiveYearRiskABS,fiveYearRiskAVE,lifetimeRiskABS,lifetimeRiskAVE,
cgvfiveyearRiskABS, cgvfiveyearRiskAVE,cgvLifetimeRiskABS,cgvLifetimeRiskAVE,explainer )''')

print 'Please check results in the database:  GailServiceTestDB.sqlite'
print 'Starting run at: ', time.strftime("%H:%M:%S")

fh = open("gailTestOutput.csv")

count = 0
for line in fh:
    #Update this to start from Scratch
    if count < 83500 :
        count += 1
        continue

    case = line.strip()
    csvrow = case.split(",")

    genetics = 0 # not set in test data
    current_age = int(csvrow[1])
    age_at_menarche = int(csvrow[2])
    wage_at_menarche = age_at_menarche

    age_at_first_live_birth = int(csvrow[3])
    wage_at_first_live_birth = age_at_first_live_birth

    ever_had_biopsy = int(csvrow[6])
    wever_had_biopsy = ever_had_biopsy

    previous_biopsies = int(csvrow[5])
    biopsy_with_hyperplasia = int(csvrow[7]) #ihyp in the test data csv
    floatbiopsy_with_hyperplasia = float(csvrow[8]) #rhyp in the test data csv
    related_with_breast_cancer = int(csvrow[4])
    race = int(csvrow[0])
    fiveyearRiskABS = float(csvrow[9])
    fiveyearRiskAVE = float(csvrow[10])
    LifetimeRiskABS = float(csvrow[11])
    LifetimeRiskAVE = float(csvrow[12])



    cur.execute("SELECT genetics FROM GailTestCases WHERE genetics=? AND current_age=? AND age_at_menarche=? AND age_at_first_live_birth=? AND ever_had_biopsy=? AND previous_biopsies=? AND biopsy_with_hyperplasia=? AND floatbiopsy_with_hyperplasia=? AND related_with_breast_cancer=? AND race=?",
                (genetics,current_age,age_at_menarche,age_at_first_live_birth,ever_had_biopsy,
                 previous_biopsies,biopsy_with_hyperplasia,floatbiopsy_with_hyperplasia,related_with_breast_cancer,race))

    count = count + 1

    try:
        data = cur.fetchone()[0]
        #print "Duplicate Test Case Found in database ",current_age
        #logging.debug("Duplicate Test Case Found in database %s", current_age)
        continue
    except:
        pass

    # encoding to the URL params for the cancer.gov site for age at menarch, live birth, and ever had a biopsy

    if age_at_menarche == 0:
        wage_at_menarche = 14
    elif age_at_menarche == 1:
        wage_at_menarche = 13
    elif age_at_menarche == 2:
        wage_at_menarche = 10

    if age_at_first_live_birth == 3 :
        wage_at_first_live_birth = 30
    elif age_at_first_live_birth == 1 :
        wage_at_first_live_birth = 22
    elif age_at_first_live_birth == 0 :
        # encode once at 15
        wage_at_first_live_birth = 15
    elif age_at_first_live_birth == 2 :
        # encode once at 27
        wage_at_first_live_birth = 27

    # Write to DB
    writeCancerGovScoretoDB()

    if ever_had_biopsy == 0:
        # encode ever_had_biopsy again at 99
        wever_had_biopsy = 99
        #Write to DB
        writeCancerGovScoretoDB()

    if age_at_first_live_birth == 0:
        # enclode age_at_first_live_birth again at 99
        wage_at_first_live_birth = 99
        #write to DB
        writeCancerGovScoretoDB()


        if ever_had_biopsy == 0:
            # encode ever_had_biopsy again at 99
            wever_had_biopsy = 99
            #write to DB
            writeCancerGovScoretoDB()



    if age_at_first_live_birth == 2:
        # enclode age_at_first_live_birth again at 0
        wage_at_first_live_birth = 0
        #write to DB
        writeCancerGovScoretoDB()

        if ever_had_biopsy == 0:
            # encode ever_had_biopsy again at 99
            wever_had_biopsy = 99
            #write to DB
            writeCancerGovScoretoDB()



    if (count % 500 == 0):
        print 'Processed:', count, 'csv rows at', time.strftime("%H:%M:%S")
        time.sleep(10) #delays for 10 seconds
print 'Processed ', count, 'lines'

