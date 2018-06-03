from time import sleep
import datetime


def intervaled_ma(log, action_func, batch_func, batch_limit, min_seconds_between_actions):

    batched = []
    last_sample_datatime = None

    while True:
        now = datetime.datetime.now()

        if last_sample_datatime:
            diff = max((now - last_sample_datatime).total_seconds(), 0)
            if diff < min_seconds_between_actions:
                sleep_for = min_seconds_between_actions - diff
                log.info("time elapsed: {}, sleeping for {}".format(diff, sleep_for))
                sleep(sleep_for)

        batched = batched + action_func(now=now)

        if len(batched) >= batch_limit:
            log.info("sending batch of data containing {} entries".format(len(batched)))
            try:
                batch_func(batched)
                batched = []
            except Exception as e:
                log.error("Posting data to endpoint, received error \"{}\"".format(e))

        last_sample_datatime = now
