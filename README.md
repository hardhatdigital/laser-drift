# Laser Drift

![Laser Drift](/dist/images/logo.jpg?raw=true "Laser Drift")

Laser Drift is a collection of tools that allow you to remotely control your [Carrera Digital 132/124](http://www.carrera-toys.com/en/) race track by emulating the infrared wireless controllers for between one and four players simultaneously.

Laser Drift allows you to control the speed and lane change status of your cars in realtime via a simple language sent over TCP. It will also abstract away the messiness involved in tasks like reverse-engineering infrared signals, identifying individual players and syncing with the IR tower. And because each car is accessible over the network, they can be controlled separately from different computers.

This system acts as a low level interface into a Carrera Digital slot car set and is intended to be used to build higher lever applications.  See the [frontends](#Frontends) section for some examples of things you can do with this system. 

I have some additional details and a technical explanation of the reverse engineering process available [at my blog](http://bunts.io/).

## How it works

The main Laser Drift system is comprised of two processes:

  - A game loop that maintains each players state, listens for syncing pulses from the IR tower, and encodes each players data into a data packet the control unit expects. The game loop also consumes commands from the TCP server every ~60ms.
  - A TCP server that accepts commands from the outside world and translates them into a data structures the game loop understands. Those data packets are then added to a queue for consumption by the game loop.

A server and game loop can be spun up using the `race` program. In this case we are starting a server on port 8099 that will send data packets for players 1 and 2:

```
./race --host=127.0.0.1 --port=8099 --p1 --p2 --socket="/usr/local/var/run/lirc/lircd"
```

A full set of options can be seen by passing the help flag: ```./race --help```.

### Commands

Once you have a server running, you can communicate with it via simple commands.

The following definitions should be acknowledged:

  - **P** is the player number (an int between 0 and 3 inclusive)
  - **S** is the speed to travel (an int between 0 and 15 inclusive)
  - **L** is lane change state (0 = off, 1 = on)

The commands are:

  - **start**: Start responding to IR syncs
  - **stop**: Stop responding to IR syncs (cars will instantly stop but retain their state)
  - **pPsS**: Set player *P* to speed *S*
  - **pPlL**: Set player *P*'s lane change status to *L*

Note, the infrared packets are physically sent and received by [lirc](http://www.lirc.org/), which must be running in order for Laser Drift to successfully initialize. The full list of software and hardware dependencies is listed in the [What you need](#Whatyouneed) section below.

## Frontends

This repo provides two simple frontend applications:

  - **repl**: Provides a REPL to send raw commands to a Laser Drift server
    - ```./scripts/repl [host=localhost] [port=8099]```
  - **keyboard**: A simple keyboard-based controller (node.js)
    - ```./scripts/keyboard [player] [host=localhost] [port=8099]```

Other frontends can be built in any programming language that has a networking library (AKA: any language). Some ideas are:

  - Voice-controlled racing
  - Tap racer (the more you press, the faster you drive)
  - Race with hand gestures using a [Leap Motion](https://www.leapmotion.com/)
  - Do a lap every time someone tweets about your favourite topic

## What you need

You will need the following hardware (or equivalent):

  - Carrera Digital 132/124 race track with [Control Unit](http://www.carrera-toys.com/en/products/digital-132/accessories/control-unit-361/) (any modern set will do).
  - [Carrera Wireless Receiver/Tower](http://www.carrera-toys.com/en/products/digital-132/accessories/wireless-empfaengertower-58/).
  - Some [radical](http://www.carrera-toys.com/en/products/digital-132/cars/lamborghini-huracan-lp610-4-3003/years-2015/) [cars](http://www.carrera-toys.com/en/products/go/cars/ferrari-f12-berlinetta-3114/#64055).
  - A USB infrared transceiver. I've successfully tested [USB-UIRT](http://www.usbuirt.com/) and the [irdroid](http://www.irdroid.com/).

Currently, I've only been able to emulate the older infrared controllers with decent accuracy. The more modern 2.4Ghz wireless+ controllers are not supported (yet). Please note, you *do not* actually need any of the old controllers for this system to operate.

## Installation

TODO

  - Lirc (latest - maybe from source)
  - Move dist/aaa.conf to /blah/blah
  - Test with `irw` and `irsend`
  - Run race server
  
  - Light polution
  - Braking setting
  - Speed setting

  - lirc_options.conf
  - Python bindings not working

## FAQ

  - Did you have any help?
    - Yes! The resources available at [SlotBaer](http://www.slotbaer.de) were very important during the reverse engineering process. And Reddit user [byingling](https://www.reddit.com/user/byingling) who helped me with some hardware specifics (and even sent me an old controller!)
  - Why infrared?
        - Because it's much easier to capture and decode signals from devices that emit 38khz IR than devices that operate at 2.4ghz. IR controllers are effectively television remotes. Cheap, off-the-shelf IR transceivers are also much easier to come across. Yes, I suppose I could also have used the wired controllers, but I don't have the depth of knowledge in electrical engineering required to prevent myself from being electrucuted to death.
  - Where is the test suite?
    - Honestly, I don't even think I know how to write tests for an application like this. Literally everything important here relies heavily on the outside world.
  - Who did the logo?
    - [Melanie Huang](http://melaniehuang.com/) with the background by [Freepik](http://freepik.com/)
