from . import following, discover

algos = {
    #feed.uri: feed.handler
    following.uri: following.handler,
    discover.uri: discover.handler,
}
