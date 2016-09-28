import sqlite3
import csv
import datetime

'''
This python file creates a csv file of inputs and expected outputs for use when doing full end to end testing
'''


def choose_iter(elements, length):
    for i in xrange(len(elements)):
        if length == 1:
            yield (elements[i],)
        else:
            for next in choose_iter(elements[i + 1:len(elements)], length - 1):
                yield (elements[i],) + next


def choose(l, k):
    return list(choose_iter(l, k))


dt_fmt = "%m/%d/%Y"
today = datetime.date.today()

birthdates = {}

birthdates[today.replace(year=today.year - 30).strftime(dt_fmt)] = 30  # age is less than 35
birthdates[
    today.replace(year=today.year - 37).strftime(dt_fmt)] = 37  # age is greater than 35, but age+5 is less than 50
birthdates[
    today.replace(year=today.year - 49).strftime(dt_fmt)] = 49  # age is greater than 35, age+5 is greater than 50
birthdates[today.replace(year=today.year - 63).strftime(dt_fmt)] = 63  # age is greater than 50 but less than 85
birthdates[today.replace(year=today.year - 88).strftime(dt_fmt)] = 88  # age is greater than 85

ethnicities = {"White": 1,
               "African American / Black": 2,
               "Hispanic": 3,
               "Chinese": 7,
               "Japanese": 8,
               "Filipino": 9,
               "Other Asian American": 12,
               "American Indian or Alaskan Native": 1,
               "Hawaiian": 10,
               "Other Pacific Islander": 11,
               "Unknown": 1}

age_at_first_born = {"Unknown": 0,
                     "None": 2,
                     "15": 0,
                     "23": 1,
                     "28": 2,
                     "36": 3}

menstral_cycle_start = {"Not Sure": 0,
                        "7-11": 2,
                        "12-13": 1,
                        "14-older": 0}

biopsy_options = {"Unknown": {"ever_had": 1, "biopsy_count": 1, "hyp": 99},
                  "No": {"ever_had": 0, "biopsy_count": 0, "hyp": 0},
                  "Yes - 1 - No Hyp": {"ever_had": 1, "biopsy_count": 1, "hyp": 0},
                  "Yes - 1 - Hyp": {"ever_had": 1, "biopsy_count": 1, "hyp": 1},
                  "Yes - 1 - Unknown Hyp": {"ever_had": 1, "biopsy_count": 1, "hyp": 99},
                  "Yes - 2 - No Hyp": {"ever_had": 1, "biopsy_count": 2, "hyp": 0},
                  "Yes - 2 - Hyp": {"ever_had": 1, "biopsy_count": 2, "hyp": 1},
                  "Yes - 2 - Unknown Hyp": {"ever_had": 1, "biopsy_count": 2, "hyp": 99}
                  }

'''Radiation Therapy is a blocker so should divert to "Not Applicable"'''
chest_rad_therapy = {"Yes": True,
                     "No": False,
                     "Not Sure": False}

'''These options don't affect GAIL calc'''
syndromes_options = {"options": ["Li-Fraumeni Syndrom",
                                 "Cowden Syndrome",
                                 "Bannayan-Riley-Ruvalcaba Syndrome"],
                     "No": False,
                     "Not Sure": False}

'''Braca should divert to "Not Applicable"'''
brca_options = {"options": ["Me", "Parent", "Sibling", "Child"],
                "Nobody": False,
                "Not Sure": False}


def create_multi_options(options_dict):
    options = []
    for op in options_dict.keys():
        if op == "options":
            orig_options_list = options_dict[op]
            options.append(orig_options_list)
            for i in range(1, len(orig_options_list)):
                newlist = choose(orig_options_list, i)
                for tuple in newlist:
                    options.append(list(tuple))
        else:
            options.append([op])
    # print str(options)
    return options


family_bc_options = {"family": {"Mother": 58, "Sister": 40, "Daughter": 36},
                     "Not Sure": 0,
                     "No": 0}

''' yes to the following are blockers to GAIL'''
self_bc_options = {"Yes": True,
                   "No": False,
                   "Not Sure": False}

dcis_options = {"Yes": True,
                "No": False,
                "Not Sure": False}

lcis_options = {"Yes": True,
                "No": False,
                "Not Sure": False}

defaults = {"birthdate": today.replace(year=today.year - 49).strftime(dt_fmt),
            "ethnicity": "White",
            "age_at_first_born": "None",
            "menstral_cycle_start": "12-13",
            "chest_rad_therapy": "No",
            "syndromes_options": ["No"],
            "brca_options": ["Nobody"],
            "family_bc_options": "No",
            "self_bc_options": "No",
            "dcis_options": "No",
            "lcis_options": "No",
            "biopsy_options": "No"}


def create_test_row(changeop, value):
    testrow = defaults.copy()
    testrow[changeop] = value
    return testrow


def create_test_rows():
    testrows = []
    # Birthdates
    for bdate in birthdates.keys():
        testrows.append(create_test_row("birthdate", bdate))

    # Ethnicity
    for eth in ethnicities.keys():
        testrows.append(create_test_row("ethnicity", eth))

    # Age at first born
    for aafb in age_at_first_born.keys():
        testrows.append(create_test_row("age_at_first_born", aafb))

    # menstral cycle start
    for mcs in menstral_cycle_start.keys():
        testrows.append(create_test_row("menstral_cycle_start", mcs))

    # family bc
    for fbc in family_bc_options.keys():
        if fbc == "family":
            # family looks like: {"Mother": 58, "Sister": 40, "Daughter": 36}
            fbc = {"Mother": family_bc_options["family"]["Mother"]}
            testrows.append(create_test_row("family_bc_options", fbc))

            fbc = {"Sister": family_bc_options["family"]["Sister"]}
            testrows.append(create_test_row("family_bc_options", fbc))

            fbc = {"Daughter": family_bc_options["family"]["Daughter"]}
            testrows.append(create_test_row("family_bc_options", fbc))

            fbc = {"Mother": family_bc_options["family"]["Mother"],
                   "Sister": family_bc_options["family"]["Sister"]}
            testrows.append(create_test_row("family_bc_options", fbc))

            fbc = {"Mother": family_bc_options["family"]["Mother"],
                   "Daughter": family_bc_options["family"]["Daughter"]}
            testrows.append(create_test_row("family_bc_options", fbc))

            fbc = {"Sister": family_bc_options["family"]["Sister"],
                   "Daughter": family_bc_options["family"]["Daughter"]}
            testrows.append(create_test_row("family_bc_options", fbc))

            fbc = {"Mother": family_bc_options["family"]["Mother"],
                   "Sister": family_bc_options["family"]["Sister"],
                   "Daughter": family_bc_options["family"]["Daughter"]}
            testrows.append(create_test_row("family_bc_options", fbc))

        else:
            testrows.append(create_test_row("family_bc_options", fbc))
    # Biopsy
    for hyp in biopsy_options.keys():
        testrows.append(create_test_row("biopsy_options", hyp))

    ''' These are blockers to GAIL if Yes'''
    # BRCA
    for brca_op in create_multi_options(brca_options):
        testrows.append(create_test_row("brca_options", brca_op))

    # self bc
    for sbc in self_bc_options.keys():
        testrows.append(create_test_row("self_bc_options", sbc))

    # dcis
    for dcis in dcis_options.keys():
        testrows.append(create_test_row("dcis_options", dcis))

    # lcis
    for lcis in lcis_options.keys():
        testrows.append(create_test_row("lcis_options", lcis))

    # chest rad therapy
    for crt in chest_rad_therapy.keys():
        testrows.append(create_test_row("chest_rad_therapy", crt))

    # Syndromes
    for synd_op in create_multi_options(syndromes_options):
        testrows.append(create_test_row("syndromes_options", synd_op))

    return testrows


def check_multi_op(option_set, option_val):
    # print "check_multi option_val: " + str(option_val)
    if len(option_val) > 1:
        # print "check_multi: Len > 1"
        return True
    elif option_val[0] in option_set and not option_set[option_val[0]]:
        return False
    else:
        # print "check_multi: else"
        return True


def lookup_gail_score(options):
    con = None
    results = {"five_year_abs": "Not Applicable",
               "five_year_ave": "Not Applicable",
               "lifetime_abs": "Not Applicable",
               "lifetime_ave": "Not Applicable"}
    try:
        con = sqlite3.connect('/Users/srmoore/Downloads/GailServiceTestDB.sqlite')
        cur = con.cursor()
        cur.execute(
            'SELECT cgvfiveyearRiskABS, cgvfiveyearRiskAVE, cgvLifetimeRiskABS, cgvLifetimeRiskAVE FROM GailTestCases WHERE current_age=? AND age_at_menarche=? AND age_at_first_live_birth=? AND related_with_breast_cancer=? AND race=? AND ever_had_biopsy=? AND previous_biopsies=? AND biopsy_with_hyperplasia=?',
            (birthdates[options["birthdate"]],
             menstral_cycle_start[options["menstral_cycle_start"]],
             age_at_first_born[options["age_at_first_born"]],
             options["fam_bc_count"],
             ethnicities[options["ethnicity"]],
             biopsy_options[options["biopsy_options"]]["ever_had"],
             biopsy_options[options["biopsy_options"]]["biopsy_count"],
             biopsy_options[options["biopsy_options"]]["hyp"]))
        data = cur.fetchone()
        results["five_year_abs"] = data[0]  # data["cgvfiveyearRiskABS"]
        results["five_year_ave"] = data[1]  # data["cgvfiveyearRiskAVE"]
        results["lifetime_abs"] = data[2]  # data["cgvLifetimeRiskABS"]
        results["lifetime_ave"] = data[3]  # data["cgvLifetimeRiskAVE"]
        print data
    except sqlite3.Error, e:
        print "Error %s" % e.args[0]
    finally:
        if con:
            con.close()
    return results


def get_results(options):
    na_results = {"five_year_abs": "Not Applicable",
                  "five_year_ave": "Not Applicable",
                  "lifetime_abs": "Not Applicable",
                  "lifetime_ave": "Not Applicable"}

    # Test for Not Applicable first
    if check_multi_op(brca_options, options["brca_options"]) or check_multi_op(syndromes_options,
                                                                               options["syndromes_options"]) or \
            self_bc_options[options["self_bc_options"]] or dcis_options[
        options["dcis_options"]] or lcis_options[options["lcis_options"]] or chest_rad_therapy[
        options["chest_rad_therapy"]] or birthdates[options["birthdate"]] < 35 or birthdates[options["birthdate"]] > 85:
        print "Not available results!"
        options["results"] = na_results
        return options
    fam_bc_count = 0
    if type(options["family_bc_options"]) == type("STRING"):
        fam_bc_count = family_bc_options[options["family_bc_options"]]
    else:
        if len(options["family_bc_options"]) > 1:
            fam_bc_count = 2
        elif len(options["family_bc_options"]) == 1:
            fam_bc_count = 1
    options["fam_bc_count"] = fam_bc_count
    print "Looking up gail score"
    options["results"] = lookup_gail_score(options)
    return options


finalrows = create_test_rows()
print finalrows[1]
with open('end_to_end_test.csv', 'wb') as csvfile:
    testwriter = csv.writer(csvfile)
    testwriter.writerow(["birthdate", "ethnicity", "age_at_first_born", "menstral_cycle_start", "chest_rad_therapy",
                         "syndromes_options", "brca_options", "family_bc_options", "self_bc_options", "dcis_options",
                         "lcis_options", "biopsy_options", "five_year_abs", "five_year_ave","lifetime_abs","lifetime_ave"])
    for row in finalrows:
        rowobj = get_results(row)
        if type(rowobj["family_bc_options"]) == type("STRING"):
            fambcstring = rowobj["family_bc_options"]
        else:
            fambcdict = rowobj["family_bc_options"]
            fambclist = []
            for key in fambcdict.keys():
                fambclist.append(key + " @ " + str(fambcdict[key]))
            fambcstring = ", ".join(fambclist)
        rowoutput = [rowobj["birthdate"],
                     rowobj["ethnicity"],
                     rowobj["age_at_first_born"],
                     rowobj["menstral_cycle_start"],
                     rowobj["chest_rad_therapy"],
                     ", ".join(rowobj["syndromes_options"]),
                     ", ".join(rowobj["brca_options"]),
                     fambcstring,
                     rowobj["self_bc_options"],
                     rowobj["dcis_options"],
                     rowobj["lcis_options"],
                     rowobj["biopsy_options"],
                     rowobj["results"]["five_year_abs"],
                     rowobj["results"]["five_year_ave"],
                     rowobj["results"]["lifetime_abs"],
                     rowobj["results"]["lifetime_ave"],]
        testwriter.writerow(rowoutput)
