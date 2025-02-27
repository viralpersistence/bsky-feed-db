from . import following, discover, links

algos = {
    #feed.uri: feed.handler
    following.uri: following.handler,
    discover.uri: discover.handler,
    links.uri: links.handler,
}
