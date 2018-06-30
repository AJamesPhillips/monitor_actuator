from time import sleep
import datetime


def intervaled_ma(log, action_func, batch_func, min_seconds_between_actions):

    batched = []
    last_sample_datetime = None

    while True:

        if last_sample_datetime:
            diff = max((datetime.datetime.now() - last_sample_datetime).total_seconds(), 0)
            if diff < min_seconds_between_actions:
                sleep_for = min_seconds_between_actions - diff
                log.info("time elapsed: {}, sleeping for {}".format(diff, sleep_for))
                sleep(sleep_for)

        now = datetime.datetime.now()
        batched = batched + action_func(now=now)
        batched = batch_func(batched=batched, now=now)

        last_sample_datetime = now
