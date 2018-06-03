import requests

from utils.json_helper import safe_json


def batch_send_factory(log, config, verify_ssl_certificate=True):

    def batch_func(batched):
        # TODO better error handling needed if / when multiple endpoint subscribers
        for endpoint in config["endpoints"]:
            data = safe_json({ "data": batched })
            log.info("Posting data: \"{}\"".format(data))
            credentials = endpoint["credentials"]
            response = requests.post(endpoint["endpoint_url"],
                data=data,
                auth=(credentials["username"], credentials["password"]),
                timeout=1, # 1 second
                verify=verify_ssl_certificate,
            )
            response.raise_for_status()
            log.info("Posted data succeeded")

    return batch_func
