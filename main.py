"""
Usage examples:
    python3 main.py "64:4:1" "256:8:2" "1024:16:4" addresses/cacheSimulatorInput2.bin
    python3 main.py "64:4:1" "256:8:2" "1024:16:4" addresses/cacheSimulatorInput2.bin --repl LRU
    python3 main.py "64:4:1" "256:8:2" "1024:16:4" addresses/cacheSimulatorInput2.bin --repl FIFO
    python3 main.py "64:4:1" "128:4:2" "256:8:4" "512:8:8" "1024:16:16" "2048:16:32" "4096:32:64" "8192:32:128" "16384:64:256" "32768:64:512" addresses/cachesimulatorinput2.bin --repl LRU
    ^ RAM EATER xD
"""

import argparse  # part of the Python standard library, no extra install needed
from structures.cache import Cache
from sys import argv, exit


def main() -> None:
    # Parse command‑line arguments
    parser = argparse.ArgumentParser(description="Cache simulator – batch mode")
    parser.add_argument(
        "caches",
        nargs="*",
        help='Cache specifications in the form "nsets:bsize:assoc" '
        "(e.g. 64:4:1). If omitted a default L1 is created.",
    )
    parser.add_argument(
        "addr_file", help="Binary file containing 32‑bit addresses (big‑endian)."
    )
    parser.add_argument(
        "--repl",
        choices=["LRU", "FIFO", "RANDOM"],
        default="RANDOM",
        help="Replacement policy for **all** created caches (default: RANDOM).",
    )

    args = parser.parse_args()

    cache_specs = args.caches  # list like ["64:4:1", "256:8:2", ...]
    addresses_fn = args.addr_file
    repl_policy = args.repl  # default is "RANDOM"

    # Build the cache hierarchy
    caches: list[Cache] = []

    if not cache_specs:  # no spec : use the built‑in default L1
        L1 = Cache(
            nsets=2048,
            blocksize_bytes=8,
            associativity=1,
            addressing=32,
            replacement=repl_policy,
        )
        caches.append(L1)
    else:
        for spec in cache_specs:
            parts = spec.split(":")
            if len(parts) != 3:
                exit(
                    f'Invalid cache specification: "{spec}". '
                    f"Expected <nsets>:<bsize>:<assoc>."
                )

            nsets, bsize, assoc = map(int, parts)

            caches.append(
                Cache(
                    nsets=nsets,
                    blocksize_bytes=bsize,
                    associativity=assoc,
                    addressing=32,  # keep the 32‑bit address width used elsewhere
                    replacement=repl_policy,
                )
            )

    # Link the caches: L1 → L2 → L3 → … → None (main memory)
    for i in range(len(caches) - 1):
        caches[i].lower_cache = caches[i + 1]
    # The last cache's lower_cache stays None → accesses main memory on miss

    # Feed the address trace to the first cache (L1)
    with open(addresses_fn, "rb") as f:
        while True:
            word = f.read(4)  # 4 bytes = 32‑bit address
            if not word or len(word) < 4:
                break
            addr = int.from_bytes(word, byteorder="big")
            caches[0].read(addr)  # always start at L1 (caches[0])

    # Print statistics for every level
    print("\n=== Cache Statistics ===")
    for idx, cache in enumerate(caches, start=1):
        print(f"\nCache Level {idx} (L{idx}):")
        print(
            f"  Configuration: {cache.nsets} sets, {cache.blocksize} B block size, "
            f"{cache.associativity}-way associativity, {cache.replacement} replacement"
        )
        print(cache.getStats())


if __name__ == "__main__":
    main()
