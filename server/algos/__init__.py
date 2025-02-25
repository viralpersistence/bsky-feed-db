from . import following, discovery

algos = {
    #feed.uri: feed.handler
    following.uri: following.handler,
    discovery.uri: discovery.handler,
}
