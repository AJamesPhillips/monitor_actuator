from time import sleep
import traceback

def retry_main(main_function, log, sleep_on_error_for=10):

    min_sleep_on_error_for = sleep_on_error_for
    max_sleep_on_error_for = sleep_on_error_for * 16

    while True:
        try:
            main_function()
            sleep_on_error_for = min_sleep_on_error_for
        except Exception as e:
            log.error("main function erred.  Sleep for {}, error received: \"{}\"".format(sleep_on_error_for, e))
            log.error("traceback.format_exc():\n{}".format(traceback.format_exc()))
            sleep(sleep_on_error_for)
            sleep_on_error_for = min(sleep_on_error_for * 2, max_sleep_on_error_for)
