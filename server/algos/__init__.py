from . import following, discover#, links, secret, mutualaid, unitedkingdom

algos = {
    following.uri: following.handler,
    discover.uri: discover.handler,
    #links.uri: links.handler,
    #secret.uri: secret.handler,
    #mutualaid.uri: mutualaid.handler,
    #unitedkingdom.uri: unitedkingdom.handler,
}
