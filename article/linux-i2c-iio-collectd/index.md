---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624125741/https://petermolnar.net/linux-i2c-iio-collectd/
published: '2018-07-13T21:00:00+00:00'
summary: A short story of getting a tiny, cheap USB I²C adapter for a home
    server, learning about the Industrial I/O linux subsystem, and connecting
    it to collectd.
tags:
- linux
title: Using I²C sensors on a linux via a USB and IIO

---

**Notes: no warranties. This is hardware, so it can cause trouble with
your system, especially if you short-circuit something or - as I did
once, many moons ago - solder on the fly why the thing is still
connected to the USB port. Don't do that.**

![Proto-assembly of Digispark ATTiny85, Adafruit BME280, and Adafruit
SI1145](digispark-attiny85-bme280-si1145.jpg)

## USB I²C adapter

A few months ago I wrote about using a Raspberry Pi with some I²C
sensors to collect data for Collectd[^1]. While it worked well, it made
me realise that having the RPi running a full fledged operating system
means I need to apply security patches to yet another machine, and that
is not something I want to deal with. I also have a former laptop,
running as a ZFS based NAS, so why not use that?

After venturing into a fruitless dig to use the I²C port in the VGA
connector[^2] I verified that indeed, as concluded in the tutorial, it
doesn't work with embedded Intel graphics on linux.

Alternative I started looking at USB I²C adapter, but they are
expensive. There is one project though, which looked very promising, and
it didn't require a full-fledged Arduino either: Till Harbaum's
I²C-Tiny-USB[^3].

It uses an ATtiny85 board - as the name suggests, it's tiny, and turned
out to be a perfectly fine USB to I²C adapter. You can buy one here:
<https://amzn.to/2ubPs6I>

*Note: there's an Adafruit FT232H, which, in theory, is capable of the
same thing. I haven't tested it.*

### I2C-Tiny-USB firmware

The git repository already contains a built `hex` file, but in case
there are any modifications needed to be done, this is how it's done:

```bash
sudo -i
apt install gcc-avr avr-libc
cd /usr/src
git clone https://github.com/harbaum/I2C-Tiny-USB
cd I2C-Tiny-USB/digispark
make hex
```

Make sure the `I2C_IS_AN_OPEN_COLLECTOR_BUS` is uncommented; I've tried
with real pull-up resistors, and, for my surprise, the sensors stopped
showing up.

### micronucleus flash utility

To flash the hex file, you'll need `micronucleus`, a tiny flasher
utility.

```bash
sudo -i
apt install libusb-dev
cd /usr/src
git clone https://github.com/micronucleus/micronucleus
cd micronucleus/commandline
make CONFIG=t85_default
make install
```

Run:

```bash
micronucleus --run --dump-progress --type intel-hex main.hex
```

then connect the device through a USB port, and wait for the end of the
flash process.

## I²C on linux

Surprisingly enough, Debian did not show I²C hubs in `/dev` - apparently
the kernel module for this is not loaded, so load it, and make that load
permanent:

```bash
sudo -i
modprobe i2c-dev
echo "i2c-dev" >> /etc/modules
```

### Connect the Attiny85

Normally a PC already has a serious amount of I²C adapters. As a result,
the new device will show up with an extra device number, which number is
rather important. The kernel log can help identify that:

```ḃash
dmesg | grep i2c-tiny-usb
[    3.721200] usb 5-2: Product: i2c-tiny-usb
[    3.725693] i2c-tiny-usb 5-2:1.0: version 2.01 found at bus 005 address 003
[    3.736109] i2c i2c-1: connected i2c-tiny-usb device
[    3.736584] usbcore: registered new interface driver i2c-tiny-usb
```

To read just the device number:

```bash
i2cdev=$(dmesg | grep 'connected i2c-tiny-usb device' | head -n1 | sed -r 's/.*\s+i2c-([0-9]+).*/\1/')
```

**Note: the device number might change after a reboot. For me, it was
`10` when simply plugged in, and `1` if it was connected during a
reboot.**

### Detecting I2C devices

`i2cdetect` is a program that dumps all the devices responding on an I²C
adapter. The Adafruit website has a collection for their sensors[^4].
That `1` after the `i2cdetect -y` is the device number identified in the
previous step, and it says I have 2 devices:

```bash
sudo -i
i2cdev=$(dmesg | grep 'connected i2c-tiny-usb device' | head -n1 | sed -r 's/.*\s+i2c-([0-9]+).*/\1/')
i2cdetect -y ${i2cdev}
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: 60 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- 77   
```

## I²C 0x77: BME280 temperature, pressure, humidity sensor[^5] {#ic-0x77-bme280-temperature-pressure-humidity-sensor1}

This is where things got interesting. Normally, when a `BME280` sensors
comes into play, every tutorial starts pulling out Python for the task,
given that most of the Adafruit libraries are in Python.

Don't get me wrong, those are great libs, and the Python solutions are
decent, but doing a `pip3 search bme280` resulted in this:

    bme280 (0.5)                           - Python Driver for the BME280 Temperature/Pressure/Humidity Sensor from Bosch.
    Adafruit-BME280 (1.0.1)                - Python code to use the BME280 temperature/humidity/pressure sensor with a Raspberry Pi or BeagleBone black.
    adafruit-circuitpython-bme280 (2.0.2)  - CircuitPython library for the Bosch BME280 temperature/humidity/pressure sensor.
    bme280_exporter (0.1.0)                - Prometheus exporter for the Bosh BME280 sensor
    RPi.bme280 (0.2.2)                     - A library to drive a Bosch BME280 temperature, humidity, pressure sensor over I2C

Which one to use? Then there are the dependencies, and the code quality
varies from one to another.

So I started digging into the internet, github, and other sources, and
somehow I realised there's a kernel module, named `bmp280`. The `BMP280`
is a sibling of the `BME280` - it's without the humidity sensor. So the
questions was: what in the world is `drivers/iio/pressure/bmp280-i2c.c`
and how can I use it?

It turned out, that apart from `hwmon`, there's another sensor library
layer in the linux kernel, called Industrial I/O - iio. It was added
with this name somewhere in 2012, around 3.15[^6], and it's purpose is
to offer a subsystem fast speed sensors[^7]. While fast speed is not a
thing for me this time, but I do trust the kernel code quality.

For my greatest surprise, the `BMP280` module is even included in the
Debian Sid kernel as a module, and adding it was a mere:

```bash
sudo -i
modprobe bmp280
echo "bmp280" >> /etc/modules
modprobe bmp280-i2c
echo "bmp280-i2c" >> /etc/modules
```

To actually enable the device, the i2c bus has to be told of the
sensor's existence:

```bash
sudo -i
i2cdev=$(dmesg | grep 'connected i2c-tiny-usb device' | head -n1 | sed -r 's/.*\s+i2c-([0-9]+).*/\1/')
echo "bme280 0x77" > /sys/bus/i2c/devices/i2c-${i2cdev}/new_device
```

The `kernel` log should show something like this:

    kernel: bmp280 1-0077: 1-0077 supply vddd not found, using dummy regulator
    kernel: bmp280 1-0077: 1-0077 supply vdda not found, using dummy regulator
    kernel: i2c i2c-1: new_device: Instantiated device bme280 at 0x77

Verify the device is working:

```bash
tree /sys/bus/iio/devices/iio\:device0
/sys/bus/iio/devices/iio:device0
├── dev
├── in_humidityrelative_input
├── in_humidityrelative_oversampling_ratio
├── in_pressure_input
├── in_pressure_oversampling_ratio
├── in_pressure_oversampling_ratio_available
├── in_temp_input
├── in_temp_oversampling_ratio
├── in_temp_oversampling_ratio_available
├── name
├── power
│   ├── async
│   ├── autosuspend_delay_ms
│   ├── control
│   ├── runtime_active_kids
│   ├── runtime_active_time
│   ├── runtime_enabled
│   ├── runtime_status
│   ├── runtime_suspended_time
│   └── runtime_usage
├── subsystem -> ../../../../../../../../../bus/iio
└── uevent

2 directories, 20 files
```

And that's it. The `BME280` is ready to be used:

```bash
for f in  in_pressure_input in_temp_input in_humidityrelative_input; do echo "$f: $(cat /sys/bus/iio/devices/iio\:device0/$f)"; done
in_pressure_input: 102.112671875
in_temp_input: 26050
in_humidityrelative_input: 49.611328125
```

According to the `BME280` datasheet[^8], under recommended modes of
operation (3.5.1 Weather monitoring), the oversampling for each sensor
should be 1, so:

```bash
sudo -i
echo 1 > /sys/bus/iio/devices/iio\:device0/in_pressure_oversampling_ratio
echo 1 > /sys/bus/iio/devices/iio\:device0/in_temp_oversampling_ratio
echo 1 > /sys/bus/iio/devices/iio\:device0/in_humidityrelative_oversampling_ratio
```

## I²C 0x60: SI1145 UV index, light, IR sensor[^9] {#ic-0x60-si1145-uv-index-light-ir-sensor2}

Unlike the BME280, the SI1145 doesn't have a built-in kernel module in
Debian Sid - but it does exist as a kernel module, it's simply not
included in the Debian Kernel. I've also learnt that this sensor is a
heavyweight player, and that I should have bought something way simpler
for mere light measurements; something that's already included the
out-of-the-box kernel modules, like a TSL2561[^10].

But I wasn't willing to give up the SI1145, being an expensie sensor, so
in order to have it in the kernel, I had to compile the kernel module.
Before getting started make sure:

-   your system is up to date
-   you have rebooted since the last kernel update

Once those two are true, identify the kernel version:

```bash
uname -a
Linux system-hostname 4.17.0-1-amd64 #1 SMP Debian 4.17.3-1 (2018-07-02) x86_64 GNU/Linux
```

The output contains `4.17.3-1` - **that is the actual kernel version**,
not the `4.17.0-1-amd64` which is the Debian name.

Get the kernel; extract it; add the SI1145 to the config; compile the
`drivers/iio/light` modules; add that to the local modules.

```bash
sudo -i
cd /usr/src/
wget https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.17.3.tar.gz
tar xf linux-4.17.3.tar.gz
cd linux-4.17.3
cp /boot/config-4.17.0-1-amd64 .config
cp ../linux-headers-4.17.0-1-amd64/Module.symvers .
echo "CONFIG_SI1145=m" >> .config
make menuconfig
# save it
# exit
make prepare
make modules_prepare
make SUBDIRS=scripts/mod
make M=drivers/iio/light SUBDIRS=drivers/iio/light modules
cp drivers/iio/light/si1145.ko /lib/modules/$(uname -r)/kernel/drivers/iio/light/
depmod
modprobe si1145
echo "si1145" >> /etc/modules
```

Once that is done, and there are no error messages, enable the device:

```bash
sudo -i
i2cdev=$(dmesg | grep 'connected i2c-tiny-usb device' | head -n1 | sed -r 's/.*\s+i2c-([0-9]+).*/\1/')
echo "si1145 0x60" > /sys/bus/i2c/devices/i2c-${i2cdev}/new_device
```

The `kernel` log shoud show something like this:

    kernel: si1145 1-0060: device ID part 0x45 rev 0x0 seq 0x8
    kernel: si1145 1-0060: no irq, using polling
    kernel: i2c i2c-1: new_device: Instantiated device si1145 at 0x60

Verify the device is working:

```bash
tree /sys/bus/iio/devices/iio\:device1
/sys/bus/iio/devices/iio:device1                                     
├── buffer
│   ├── data_available
│   ├── enable
│   ├── length
│   └── watermark
├── current_timestamp_clock
├── dev
├── in_intensity_ir_offset
├── in_intensity_ir_raw
├── in_intensity_ir_scale
├── in_intensity_ir_scale_available
├── in_intensity_offset
├── in_intensity_raw
├── in_intensity_scale
├── in_intensity_scale_available
├── in_proximity0_raw
├── in_proximity_offset
├── in_proximity_scale
├── in_proximity_scale_available
├── in_temp_offset
├── in_temp_raw
├── in_temp_scale
├── in_uvindex_raw
├── in_uvindex_scale
├── in_voltage_raw
├── name
├── out_current0_raw
├── power
│   ├── async
│   ├── autosuspend_delay_ms
│   ├── control
│   ├── runtime_active_kids
│   ├── runtime_active_time
│   ├── runtime_enabled
│   ├── runtime_status
│   ├── runtime_suspended_time
│   └── runtime_usage
├── sampling_frequency
├── scan_elements
│   ├── in_intensity_en
│   ├── in_intensity_index
│   ├── in_intensity_ir_en
│   ├── in_intensity_ir_index
│   ├── in_intensity_ir_type
│   ├── in_intensity_type
│   ├── in_proximity0_en
│   ├── in_proximity0_index
│   ├── in_proximity0_type
│   ├── in_temp_en
│   ├── in_temp_index
│   ├── in_temp_type
│   ├── in_timestamp_en
│   ├── in_timestamp_index
│   ├── in_timestamp_type
│   ├── in_uvindex_en
│   ├── in_uvindex_index
│   ├── in_uvindex_type
│   ├── in_voltage_en
│   ├── in_voltage_index
│   └── in_voltage_type
├── subsystem -> ../../../../../../../../../bus/iio
├── trigger
│   └── current_trigger
└── uevent

5 directories, 59 files
```

**Note: I tried, others tried, but even though in theory, there's a
temperature sensor on the SI1145, it doesn't work. It seems like it
reads the value on startup, and that's it.**

## CLI script

In order to have a quick view, without collectd, or other dependencies,
a script like this is more, than sufficient:

```bash
#!/usr/bin/env bash

d="$(date)"
temperature=$(echo "scale=2;$(cat /sys/bus/iio/devices/iio\:device0/in_temp_input)/1000" | bc)
pressure=$(echo "scale=2;$(cat /sys/bus/iio/devices/iio\:device0/in_pressure_input)*10/1" | bc) 
humidity=$(echo "scale=2;$(cat /sys/bus/iio/devices/iio\:device0/in_humidityrelative_input)/1" | bc) 
light_vis=$(cat /sys/bus/iio/devices/iio\:device1/in_intensity_raw) 
light_ir=$(cat /sys/bus/iio/devices/iio\:device1/in_intensity_ir_raw) 
light_uv=$(cat /sys/bus/iio/devices/iio\:device1/in_uvindex_raw) 

echo "$(hostname -f) $d

Temperature: $temperature °C
Pressure: $pressure mBar
Humidity: $humidity %
Visible light: $light_vis lm
IR light: $light_ir lm
UV light: $light_uv lm"
```

The output:

    your.hostname Thu Jul 12 08:48:40 BST 2018

    Temperature: 25.59 °C
    Pressure: 1021.65 mBar
    Humidity: 49.28 %
    Visible light: 287 lm
    IR light: 334 lm
    UV light: 12 lm

*Note: I'm not completely certain that the light unit is actually in
lumens; the documentation is a bit fuzzy about that, so I assumed it
is.*

## Collectd

The next step is to actually collect the sensor readouts from the
sensors. I'm still using `collectd`[^11], a small, ancient, yet stable
and very good little metrics collection system, because it's enough. It
writes ordinary `rrd` files, which can be plotted into graphs with tools
like Collectd Graph Panel[^12]

Unfortunately there's not yet an iio plugin for collectd (or I couldn't
find it yet, and if you did, please let me know), so I had to add an
extremely simple shell script as an exec plugin to collectd.

`/usr/local/lib/collectd/iio.sh`

```bash
#!/usr/bin/env bash

HOSTNAME="${COLLECTD_HOSTNAME:-$(hostname -f)}"
INTERVAL="${COLLECTD_INTERVAL:-60}"

# this will run only on collectd load, and once it's loaded, 
# even though it throws and error, additional runs don't make any
# problems
i2cdev=$(dmesg | grep 'connected i2c-tiny-usb device' | head -n1 | sed -r 's/.*\s+i2c-([0-9]+).*/\1/')
echo "bme280 0x77" > /sys/bus/i2c/devices/i2c-${i2cdev}/new_device
echo "si1145 0x60" > /sys/bus/i2c/devices/i2c-${i2cdev}/new_device


while true; do
    for sensor in /sys/bus/iio/devices/iio\:device*; do 
        name=$(cat "${sensor}/name")
        if [ "$name" == "bme280" ]; then

            # unit: °C
            temp=$(echo "scale=2;$(cat ${sensor}/in_temp_input)/1000" | bc )
            echo "PUTVAL $HOSTNAME/sensors-$name/temperature-temperature interval=$INTERVAL N:${temp}"

            # unit: mBar
            pressure=$(echo "scale=2;$(cat ${sensor}/in_pressure_input)*10/1" | bc)
            echo "PUTVAL $HOSTNAME/sensors-$name/pressure-pressure interval=$INTERVAL N:${pressure}"

            # unit: %
            humidity=$(echo "scale=2;$(cat ${sensor}/in_humidityrelative_input)/1" | bc)
            echo "PUTVAL $HOSTNAME/sensors-$name/percent-humidity interval=$INTERVAL N:${humidity}"

        elif [ "$name" == "si1145" ]; then

            # unit: lumen?
            ir=$(cat ${sensor}/in_intensity_ir_raw)
            echo "PUTVAL $HOSTNAME/sensors-$name/gauge-ir interval=$INTERVAL N:${ir}"

            light=$(cat ${sensor}/in_intensity_raw)
            echo "PUTVAL $HOSTNAME/sensors-$name/gauge-light interval=$INTERVAL N:${light}"

            uv=$(cat ${sensor}/in_uvindex_raw)
            echo "PUTVAL $HOSTNAME/sensors-$name/gauge-uv interval=$INTERVAL N:${uv}"

        fi
    done
    sleep "$INTERVAL"
done
```

`/etc/collectd/collectd.conf`

    [...]
    LoadPlugin "exec"
    <Plugin exec>
      Exec "nobody" "/usr/local/lib/collectd/iio.sh"
    </Plugin>
    [...]

The results are:

![BME280 temperature graph in Collectd Graph
Panel](iio_bme280_temperature.png)

![SI1145 raw light measurement in Collectd Graph
Panel](iio_si1145_light.png)

## Conclusions

The Industrial I/O layer is something I've heard for the first time, but
it's extremely promising: the code is clean, it already has support for
a lot of sensors, and it seems to be possible to extend at a relative
easy.

Unfortunately it's documentation it brief and I'm yet to find any
metrics collector that supports it out of the box, but that doesn't mean
there won't be any very soon.

Currently I'm very happy with my budget I2C USB solution - not having to
run a Raspberry Pi for simple metrics collection is certainly in win,
and utilising the sensors directly from the kernel also looks very
decent.

[^1]: <https://petermolnar.net/raspberry-pi-bme280-si1145-collectd-mosquitto/>

[^2]: <https://web.archive.org/web/20160506154718/http://www.paintyourdragon.com/?p=43>

[^3]: <https://github.com/harbaum/I2C-Tiny-USB/tree/master/digispark>

[^4]: <https://learn.adafruit.com/i2c-addresses>

[^5]: <https://www.adafruit.com/product/2652>

[^6]: <https://github.com/torvalds/linux/tree/a980e046098b0a40eaff5e4e7fcde6cf035b7c06>

[^7]: <https://wiki.analog.com/software/linux/docs/iio/iio>

[^8]: <https://cdn-shop.adafruit.com/datasheets/BST-BME280_DS001-10.pdf>

[^9]: <https://www.adafruit.com/product/1777>

[^10]: <https://www.adafruit.com/product/439>

[^11]: <http://collectd.org/>

[^12]: <https://github.com/pommi/CGP>