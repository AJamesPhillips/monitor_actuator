import requests

from utils.json_helper import safe_json


def batch_send_factory(log, config, batch_limit, verify_ssl_certificate=True):

    endpoints = config["endpoints"]
    timeout = 1 # 1 second
    node_name = config["node_name"]

    def batch_func(batched, now):

        if len(batched) >= batch_limit:
            log.info("sending batch of data containing {} entries".format(len(batched)))
            try:
                # TODO better error handling needed if / when multiple endpoint subscribers
                for endpoint in endpoints:
                    url = endpoint["endpoint_url"]
                    data = safe_json({ "data": batched })
                    log.info("Posting data to {}: \"{}\"".format(url, data))
                    credentials = endpoint["credentials"]
                    response = requests.post(url,
                        data=data,
                        auth=(credentials["username"], credentials["password"]),
                        timeout=timeout,
                        verify=verify_ssl_certificate,
                    )
                    response.raise_for_status()
                    log.info("Post data to {} succeeded".format(url))

                log.info("Posting all data succeeded")
                return []

            except requests.exceptions.ConnectTimeout as e:
                log.error("Posting data to endpoint, received ConnectTimeout error \"{}\"".format(e))
                metric_type = "error-batch_send-connection_timeout"
                batched.append({
                    "type": metric_type,
                    "datetime": now,
                    "tags": [node_name + " " + metric_type],
                    "value": timeout,
                })
            except requests.exceptions.HTTPError as e:
                log.error("Posting data to endpoint, received HTTPError \"{}\"".format(e))
                metric_type = "error-batch_send-http_error"
                batched.append({
                    "type": metric_type,
                    "datetime": now,
                    "tags": [node_name + " " + metric_type],
                    "value": e.response.status_code,
                })
            except Exception as e:
                log.exception("Posting data to endpoint, received Exception \"{}\"".format(e))
                metric_type = "error-batch_send-exception"
                batched.append({
                    "type": metric_type,
                    "datetime": now,
                    "tags": [node_name + " " + metric_type],
                    "value": "", # <<< TODO NEXT, can we send a string as a value or only a number?
                })

            # Return unposted data + errors to be retried
            return batched

        else:
            return batched

    return batch_func
