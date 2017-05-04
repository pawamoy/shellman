Usage
=====

``shellman [-h01cw] [f {text,man,markdown}] [-i WHITELIST] [-o OUTPUT] FILE``

Options
-------

.. code::

    -h, --help            show this help message and exit
    -0, -n, --nice        be nice: return 0 even if warnings (default to false)
    -1, --failfast        exit 1 at first warning encountered (only useful when not nice) (default to false)
    -c, --check           check if the documentation is correct (default to false)
    -f, --format FORMAT   format to write to: text, man, or markdown (default to text)
    -i, --ignore, --whitelist WHITELIST
                          comma-separated whitelist of tags: TAGNAME[:<OCCURRENCES><LINES>], occurrences and lines being 1 or + (default to none)
    -o, --output OUTPUT   file to write to (default to stdout)
    -w, --warn            actually display the warnings (default to false)
