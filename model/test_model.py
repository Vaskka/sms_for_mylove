# for test

# test schedule
import schedule as sc


def do_job():
    print("ok")
    pass


def test_schedule():
    sc.every().day.at("17:32").do(do_job)
    pass
