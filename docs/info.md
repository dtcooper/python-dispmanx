---
title: More Info
---

# Additional Information

## OS and Device Support

Bullseye 32- and 64- bit Raspberry Pi OS

## Notes On Using [ctypes][ctypes]

## [Docker][docker] and [Compose][compose]

## Acknowledgements

Several projects were used as reference in development of Python DispmanX. Some
of the main ones are described below.

### [PyDispmanx][pydispmanx]

First and foremost, let me acknowledge the work [Tim Clark][tim-clark] put into
[PyDispmanx][pydispmanx].

[PyDispmanx][pydispmanx] is another Python library _is_ available that functions
somewhat similarly. Honestly, it's great and I would recommend it! I owe a debt
of gratitude to its author, for two reasons,

1. First and foremost, showing me that interfacing with the Pi's DispmanX API
   via Python is possible; and
2. Being available to peep into his source code.

Some reasons I've chosen to re-write from scratch are:

 * To provide a [ctypes][ctypes] pure Python interface;
 * To provide a more complete interface to DispmanX;
 * To provide documentation on how to use the thing with popular Python
   graphics libraries;
 * To publish regular, stable, and tested releases to [PyPI][pypi];
 * [PyDispmanx][pydispmanx] appears to be an unstable work in progress. For
   example, by its own author's admission in the project README, he says
   _"\[he\] probably wouldn't install this system wide yet";_ and
 * Oh, _writing code is fun!_

### [raspidmx][raspidmx]

The Broadcom hardware interface library which provides the DispmanX APIs is very
poorly documented. One of the first usable set of open source C programming
language example programs were by a developer named
[Andrew Duncan][andrew-duncan]. He calls the suite [raspidmx][raspidmx]. Andrew
provided a set of "programs [that could] be used as a starting point for anyone
wanting to make use of DispmanX."

Some of the common code from [raspidmx][raspidmx] is the underlying code that
drives [PyDispmanx][pydispmanx]. I owe a debt of gratitude to its author, since
peeing into [raspidmx][raspidmx]'s source tree is what helped figure out how to
call the DispmanX APIs from this Python package.

### [picamera][picamera]

TODO

[andrew-duncan]: https://github.com/AndrewFromMelbourne
[compose]: https://docs.docker.com/compose/
[docker]: https://www.docker.com/
[picamera]: https://picamera.readthedocs.io/
[pydispmanx]: https://github.com/eclispe/pyDispmanx
[pypi]: https://pypi.org/
[raspidmx]: https://github.com/AndrewFromMelbourne/raspidmx
[tim-clark]: https://twitter.com/eclispe
