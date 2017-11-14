class Cache(dict):
    pass

# Bears analysis results shall be:
# - Time independent
#   (means: consecutive runs on the same setup shall yield same results)
# - Argument only dependent
#   (means: Only the arguments passed have influence on the result, nothing
#    else)

# Possibility to disable cache inside a bear regardless if passed or not? For
# things that are considered to be uncachable/don't make sense to be cached?
# Like an analysis that needs current system time? Current workaround:
# override __init__ and initialize cache manually with None:
# super(..., cache=None)

# TODO: Implement hash/comparison operators to support quick cache lookup.
