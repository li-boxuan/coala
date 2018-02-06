class Cache(dict):
    pass

# Bears analysis results shall be:
# - Time independent
#   (means: consecutive runs on the same setup shall yield same results)
# - Argument only dependent
#   (means: Only the arguments passed have influence on the result, nothing
#    else)
# Otherwise: caching has to be disabled!

# Possibility to disable cache inside a bear regardless if passed or not? For
# things that are considered to be uncachable/don't make sense to be cached?
# Like an analysis that needs current system time? Current workaround:
# override __init__ and initialize cache manually with None:
# super(..., cache=None)

# TODO: Implement hash/comparison operators to support quick cache lookup.

# TODO: Storing caches in different files?
# TODO: Cache controls:
# --cache-storage-protocol ?
# --cache-protocol / --cache-strategy (I vote for --cache-strategy)
#     0: none (no cache used), maybe synonym to `--no-cache`
#     1: primitive (no automatic cache clearing, cache grows infinitely)
#            effective when many recurrent changes happen in coafile and settings.
#            fastest in storing.
#     2: lri / last-recently-used (only cached items persist that were actually used)
#             TODO: Maybe it's possible to implement a "count" param that allows to
#                   provide a count after that cached items are removed. Default should be 3 for it.
#        This is default.
#   This functionality should base on "cache-filtering". Bears just cache more and more, but
#   coala is itself responsible to clean up the cache with the specified cache strategy.
# --clear-cache
# --export-cache <dir>/<filename> / --import-cache <dir>/<filename>
#     TODO: No priority right now, but super useful for distributed stuff or to cache things
#           across CI builds!
# compression?
# What about using pickletools.optimize? I guess this can be an additional flag too.
