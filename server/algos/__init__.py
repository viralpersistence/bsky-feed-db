from . import following, discover, links, secret

algos = {
    following.uri: following.handler,
    discover.uri: discover.handler,
    links.uri: links.handler,
    secret.uri: secret.handler,
}
