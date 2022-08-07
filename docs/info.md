---
title: Additional Info
---

# Additional Information

Below is more information about the DispmanX for Python library, including
what's supported, how to install the necessary library on your Pi, and some
acknowledgements.

## Python, OS and Device Version Support

OS Support:
:   The latest versions of 32- and 64- bit Raspberry Pi OS are supported. As of
    the time of this writing, that's based on
    [Debian Bullseye (11.x)][debian-bullseye].

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
entirely, you can always use [Docker] you can use any version of the Pi. See the
section on [Docker and Compose][docker-and-compose] below.


## [ctypes][] and `bcm_host.so`

While Python DispmanX is written completely in Python, it uses Python's included
[ctypes] library to perform "foreign function calls" to `bcm_host.so`. In short
it calls the C library included with Raspberry Pi OS to interface with the
DispmanX layer directly.

The library `bcm_host.so` is available through the `libraspberrypi0` Debian
package, which should have come installed on your Pi if you used Raspberry Pi
OS. If that's not available, you can always use [Docker] following the
instructions in the [Docker and Compose][docker-and-compose] section below.


## [Docker] and [Compose]

Both [Docker] and [Docker Compose][Compose] work great. There actually how I run
the library. Details below.

### Using [Docker]

If the version of [Raspberry Pi OS][pi-os] that you're using isn't supported by
this library or you're using a different operating system altogether, you can
always use [Docker]. Docker is supported on both 32- and 64-bit architectures.

The base container for Debian Bullseye doesn't by default contain the necessary
`libraspberrypi0` package as described above. So, you'll need to either add the
["Raspbian Repository"][raspbian-repo], or use my
[minimal Raspberry Pi OS base containers][pi-base-containers]. Three variants
are provided.

The device `/dev/vchiq` needs to be exposed to container. For the Debian image,
you'll need to install pip yourself. Three images are provided.

| Description       | Image Name                                   |
|------------------:|:---------------------------------------------|
| Python 3.9        | `ghcr.io/dtcooper/raspberrypi-os:python3.9`  |
| Python 3.10       | `ghcr.io/dtcooper/raspberrypi-os:python3.10` |
| Debian (Bullseye) | `ghcr.io/dtcooper/raspberrypi-os:bullseye`   |

### Using [Compose]

Similarly, using [Docker Compose][compose] works great. You'll similarly need to
expose the `/dev/vchiq` device, however. Here's a sample `docker-compose.yml`
file,

```yaml title="docker-compose.yml"
services:
  dispmanx:
    #image: <Your image based on ghcr.io/dtcooper/raspberrypi-os:python3.9>
    devices:
      - /dev/vchiq:/dev/vchiq
```


## Acknowledgements

Several projects were used as reference in development of Python DispmanX. Some
of the main ones are described below.

### [PyDispmanx]

First and foremost, let me acknowledge the work [Tim Clark] put into
[PyDispmanx].

[PyDispmanx] is another Python library _is_ available that functions somewhat
similarly. Honestly, it's great and I would recommend it! I owe a debt of
gratitude to its author, for two reasons,

1. First and foremost, showing me that interfacing with the Pi's DispmanX API
   via Python is possible; and
2. Being available to peep into his source code.

Some reasons I've chosen to re-write from scratch are:

 * To provide a [ctypes][] pure Python interface;
 * To provide a more complete interface to DispmanX;
 * To provide documentation on how to use the thing with popular Python
   graphics libraries;
 * To publish regular, stable, and tested releases to [PyPI];
 * [PyDispmanx] appears to be an unstable work in progress. For
   example, by its own author's admission in the project README, he says
   _"\[he\] probably wouldn't install this system wide yet";_ and
 * Oh, _writing code is fun!_

### [raspidmx]

The Broadcom hardware interface library which provides the DispmanX APIs is very
poorly documented. One of the first usable set of open source C programming
language example programs were by a developer named
[Andrew Duncan]. He calls the suite [raspidmx]. Andrew
provided a set of "programs [that could] be used as a starting point for anyone
wanting to make use of DispmanX."

Some of the common code from [raspidmx] is the underlying code that
drives [PyDispmanx]. I owe a debt of gratitude to its author, since
peeing into [raspidmx]'s source tree is what helped figure out how to
call the DispmanX APIs from this Python package.

### [picamera]

The [picamera] Python library interfaces with the
[Pi's Camera Module][pi-camera-module]. Its source code contains several parts
that interface with the Pi's APIs including the DispmanX layer contained in the
`bcm_host.so` shared library. In particular [picamera]'s source in its source
file [`bcm_host.py`][bcm-host-py] were used as inspiration for how to interact
with DispmanX via [ctypes][].

[andrew duncan]: https://github.com/andrewfrommelbourne
[bcm-host-py]: https://github.com/waveform80/picamera/blob/master/picamera/bcm_host.py
[compose]: https://docs.docker.com/compose/
[debian-bullseye]: https://www.debian.org/releases/bullseye/
[docker]: https://www.docker.com/
[pi-base-containers]: https://github.com/dtcooper/raspberrypi-os-docker
[pi-camera-module]: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera
[pi-os]: https://www.raspberrypi.com/software/
[picamera]: https://picamera.readthedocs.io/
[pydispmanx]: https://github.com/eclispe/pydispmanx
[pypi]: https://pypi.org/
[raspbian-repo]: https://www.raspbian.org/RaspbianRepository
[raspidmx]: https://github.com/andrewfrommelbourne/raspidmx
[tim clark]: https://twitter.com/eclispe
