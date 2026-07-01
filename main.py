from structures.cache import Cache
from cli_menu import CLI_Menu
from sys import argv

def main():
    arguments = argv[1:] # Ignores main.py
    
    if not arguments:
        exit("Incorrect arguments. No binary file or cache settings found.")

    addresses_file = arguments[-1]
    caches_settings = arguments[:-1]

    caches = []
    
    # If no cache setting is passed, create the default one.
    if not caches_settings:
        L1 = Cache(
            nsets=(2048),
            blocksize_bytes=8,
            associativity=1,
            addressing=32,
            replacement="RANDOM"
        )

        caches.append(L1)
    
    # Create and store each cache given.
    for settings in caches_setings:
        nsets, bsize, assoc = sp_set(settings)

        c = Cache(
            nsets=nsets,
            blocksize_bytes=bsize,
            associativity=assoc,
            replacement="RANDOM"
        )

        caches.append(c)

    # TODO: Implement multiple level system
    # TODO: Implement system to track and categorize misses (compulsory and conflict + capacity)
    # TODO: Read each address from addresses_file
    # TODO: Print queries, hits, hit ratio, misses, miss ratio and misses types for each cache level... at the end.

    #cache.read(<address>)      # Reads given address. If it misses, fetches it to the cache.
    #print(cache.getStats())    # Number of queries, misses and hits 
    #print(cache)               # Visualize cache table






# Receives a string like '2048:8:4' and returns (nsets, bsize, assoc), as integers.
def sp_set(settings_string: str) -> tuple:
    settings = tuple(map(int, settings_string.split(":")))
    if len(settings) != 3:
        exit(f"Incorrect cache settings: {settings}")

    return settings

main()
