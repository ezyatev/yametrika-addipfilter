import json

import treq
from twisted.internet.task import react, Cooperator
from twisted.python import log
from twisted.web import client

import helpers


def cb_deletefilters(resp, args):
    counters = json.loads(resp.decode('utf8'))

    urls = []
    for counter in counters['counters']:
        filters = counter.get('filters')
        if not filters:
            continue

        clientip_filters = helpers.get_clientip_filters(filters)
        for filter_id in clientip_filters:
            url = helpers.get_request_url(
                '/management/v1/counter/{}/filter/{}'.format(counter['id'], filter_id),
                {'oauth_token': args.token}
            )
            urls.append(url)

    coop = Cooperator()
    work = (cb_delete(url) for url in urls)

    return coop.coiterate(work)


def cb_addipfilter(resp, args):
    counters = json.loads(resp.decode('utf8'))

    urls = []
    for counter in counters['counters']:
        post = {
            "filter": {
                "attr": "client_ip",
                "type": "equal",
                "value": args.ip,
                "action": args.action,
                "status": args.status
            }
        }
        url = helpers.get_request_url(
            '/management/v1/counter/{}/filters'.format(counter['id']),
            {'oauth_token': args.token}
        )
        urls.append((url, post))

    coop = Cooperator()
    work = (cb_post(url, post) for url, post in urls)

    return coop.coiterate(work)


def print_response(response):
    log.msg(response.code, response.phrase)
    log.msg(response.headers)

    return treq.text_content(response).addCallback(log.msg)


def cb_post(url, post):
    d = treq.post(url, json.dumps(post).encode('utf8'),
                  headers={b'Content-Type': [b'application/json']})
    d.addCallbacks(print_response, log.err)

    return d


def cb_delete(url):
    d = treq.delete(url)
    d.addCallbacks(print_response, log.err)

    return d


def cb_counters(args):
    params = {
        'oauth_token': args.token,
        'status': 'Active',
        'field': 'filters'
    }
    url = helpers.get_request_url('/management/v1/counters', params)

    d = client.getPage(url)
    if args.mode == 'delete':
        d.addCallback(cb_deletefilters, args)
    elif args.mode == 'add':
        d.addCallback(cb_addipfilter, args)

    return d


def main(reactor, *args):
    cli_args = args[0]
    helpers.start_logging_observer(cli_args.logfile)

    return cb_counters(cli_args)


if __name__ == "__main__":
    parser = helpers.create_argparser()
    react(main, [parser.parse_args()])
