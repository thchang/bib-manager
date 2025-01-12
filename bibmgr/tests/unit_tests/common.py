from bibmgr.tests.data.soln import soln


def check_results(item):
    bib_key = item.get_key()
    bib_dict = item.to_dict()
    for key in bib_dict:
        assert soln[bib_key][key] == bib_dict[key]
