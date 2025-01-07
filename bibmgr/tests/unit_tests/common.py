from bibmgr.tests.data.soln import soln


def check_results(tester):
    for item in tester.info:
        for key in tester.info[item]:
            assert soln[item][key] == tester.info[item][key]
