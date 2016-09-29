import sqlite3
import time


conn = sqlite3.connect('GailServiceTestDB.sqlite')
cur = conn.cursor()

fh = open("/tmp/gailTestOutput.csv")


cur.execute('''CREATE TABLE IF NOT EXISTS UpdatedGailTestCases
    (csvlinenum,genetics,current_age,age_at_menarche, age_at_first_live_birth, ever_had_biopsy,
    previous_biopsies,biopsy_with_hyperplasia,floatbiopsy_with_hyperplasia,
    related_with_breast_cancer,race,fiveYearRiskABS,fiveYearRiskAVE,lifetimeRiskABS,lifetimeRiskAVE )''')

count = 1
for line in fh:

    case = line.strip()
    csvrow = case.split(",")

    genetics = 0 # not set in test data
    current_age = int(csvrow[1])
    age_at_menarche = int(csvrow[2])
    age_at_first_live_birth = int(csvrow[3])
    ever_had_biopsy = int(csvrow[6])
    previous_biopsies = int(csvrow[5])
    biopsy_with_hyperplasia = int(csvrow[7]) #ihyp in the test data csv
    floatbiopsy_with_hyperplasia = float(csvrow[8]) #rhyp in the test data csv
    related_with_breast_cancer = int(csvrow[4])
    race = int(csvrow[0])
    fiveyearRiskABS = float(csvrow[9])
    fiveyearRiskAVE = float(csvrow[10])
    LifetimeRiskABS = float(csvrow[11])
    LifetimeRiskAVE = float(csvrow[12])


    cur.execute('''INSERT INTO UpdatedGailTestCases (csvlinenum,genetics, fiveyearRiskABS,fiveyearRiskAVE,LifetimeRiskABS,LifetimeRiskAVE,current_age,age_at_menarche,age_at_first_live_birth,
               ever_had_biopsy,previous_biopsies,biopsy_with_hyperplasia,floatbiopsy_with_hyperplasia,related_with_breast_cancer,race) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (count, genetics, fiveyearRiskABS,fiveyearRiskAVE,LifetimeRiskABS,LifetimeRiskAVE,current_age,age_at_menarche,age_at_first_live_birth,
               ever_had_biopsy,previous_biopsies,biopsy_with_hyperplasia,floatbiopsy_with_hyperplasia,related_with_breast_cancer,race))


    count = count + 1

    conn.commit()

    if (count % 5000 == 0):
        print 'Processed:', count, 'csv rows at', time.strftime("%H:%M:%S")
        time.sleep(1) #delays for 10 seconds
print 'Processed ', count, 'lines'

