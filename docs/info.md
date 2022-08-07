---
title: More Info
---

# Additional Information

## Python, OS and Device Version Support

OS Support:
:   The latest versions of 32- and 64- bit Raspberry Pi OS are supports. As of
    the time of this writing, that's based on [Debian Bullseye (11.x)][debian-bullseye].

Python Version
:   The minimum version of Python supported is 3.9. That's the default version
    installed on [Raspberry Pi OS][pi-os].

Raspberry Pi Versions
:   This library should work on any versions of the Pi, but I've specifically
    tested,

    1. Raspberry Pi 4 B
    2. Raspberry Pi 3 B+
    3. Raspberry Pi 3 B
    4. Raspberry Pi 2
    5. Raspberry Pi B

If you're using an older version Python, Raspberry Pi OS, and/or a different OS
entirely, you can always use [Docker][] you can use any version of the Pi. See
the section on [Docker and Compose][docker-and-compose] just below.

## [Docker][] and [Compose][]

## [ctypes][] and `bcm_host.so`

While Python DispmanX is written completely in Python, it uses Python's included
[ctypes][] library to perform "foreign function calls" to `bcm_host.so`. In
short it calls the C library included with Raspberry Pi OS to interface with the
DispmanX layer directly.

The library `bcm_host.so` is available through the `libraspberrypi0` Debian
package, which should have come installed on your Pi if you used Raspberry Pi
OS. If that's not available, you can always use [Docker][] following the
instructions in the [Docker and Compose][docker-and-compose] section above.

## Acknowledgements

Several projects were used as reference in development of Python DispmanX. Some
of the main ones are described below.

### [PyDispmanx][]

First and foremost, let me acknowledge the work [Tim Clark][] put into
[PyDispmanx][].

[PyDispmanx][] is another Python library _is_ available that functions
somewhat similarly. Honestly, it's great and I would recommend it! I owe a debt
of gratitude to its author, for two reasons,

1. First and foremost, showing me that interfacing with the Pi's DispmanX API
   via Python is possible; and
2. Being available to peep into his source code.

Some reasons I've chosen to re-write from scratch are:

 * To provide a [ctypes][] pure Python interface;
 * To provide a more complete interface to DispmanX;
 * To provide documentation on how to use the thing with popular Python
   graphics libraries;
 * To publish regular, stable, and tested releases to [PyPI][];
 * [PyDispmanx][] appears to be an unstable work in progress. For
   example, by its own author's admission in the project README, he says
   _"\[he\] probably wouldn't install this system wide yet";_ and
 * Oh, _writing code is fun!_

### [raspidmx][]

The Broadcom hardware interface library which provides the DispmanX APIs is very
poorly documented. One of the first usable set of open source C programming
language example programs were by a developer named
[Andrew Duncan][]. He calls the suite [raspidmx][]. Andrew
provided a set of "programs [that could] be used as a starting point for anyone
wanting to make use of DispmanX."

Some of the common code from [raspidmx][] is the underlying code that
drives [PyDispmanx][]. I owe a debt of gratitude to its author, since
peeing into [raspidmx][]'s source tree is what helped figure out how to
call the DispmanX APIs from this Python package.

### [picamera][]

TODO

[andrew duncan]: https://github.com/andrewfrommelbourne
[debian-bullseye]: https://www.debian.org/releases/bullseye/
[compose]: https://docs.docker.com/compose/
[docker]: https://www.docker.com/
[pi-os]: https://www.raspberrypi.com/software/
[picamera]: https://picamera.readthedocs.io/
[pydispmanx]: https://github.com/eclispe/pydispmanx
[pypi]: https://pypi.org/
[raspidmx]: https://github.com/andrewfrommelbourne/raspidmx
[tim clark]: https://twitter.com/eclispe
