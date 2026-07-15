from structures.cache import Cache
from cli_menu import CLI_Menu
from sys import argv


def main():
    arguments = argv[1:]  # Ignores main.py

    if not arguments:
        exit("Incorrect arguments. No binary file or cache settings found.")

    addresses_file = arguments[-1]
    caches_settings = arguments[:-1]

    caches = []

    # If no cache setting is passed, create the default one.
    if not caches_settings:
        L1 = Cache(
            nsets=2048,
            blocksize_bytes=8,
            associativity=1,
            addressing=32,
            replacement="RANDOM",
        )

        caches.append(L1)

    # Create and store each cache given.
    for settings in caches_settings:
        parts = settings.split(":")
        if len(parts) != 3:
            exit(
                f"Incorrect cache settings format. Expected <nsets>:<bsize>:<assoc>, got: {settings}"
            )
        nsets, bsize, assoc = map(int, parts)

        c = Cache(
            nsets=nsets,
            blocksize_bytes=bsize,
            associativity=assoc,
            replacement="RANDOM",
        )

        caches.append(c)

    # Link caches to form a hierarchy: L1 -> L2 -> L3 -> ... -> None (memory)
    for i in range(len(caches) - 1):
        caches[i].lower_cache = caches[i + 1]
    # The last cache's lower_cache remains None, meaning it accesses main memory on miss

    # Read addresses from the binary file and process them through the L1 cache
    with open(addresses_file, "rb") as f:
        while True:
            bytes_data = f.read(4)
            if not bytes_data or len(bytes_data) < 4:
                break
            address = int.from_bytes(bytes_data, byteorder="big")
            caches[0].read(address)

    # Print statistics for each cache level
    print("\n=== Cache Statistics ===")
    for i, cache in enumerate(caches):
        print(f"\nCache Level {i+1} (L{i+1}):")
        print(
            f"  Configuration: {cache.nsets} sets, {cache.blocksize} B block size, {cache.associativity}-way associativity, {cache.replacement} replacement"
        )
        print(cache.getStats())


main()
