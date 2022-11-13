Mudita harness utility
======================

The aim of [test harness](https://en.wikipedia.org/wiki/Test_harness) is to enable tests automation and facilitate integration testing.

Mudita Pure test harness makes use of USB-CDC serial (on RT1051 target) or pseudo-tty (on Linux) to communicate
with `service-desktop` service in the operating system and get data from the internal database and device status.

This utility is meant to be used as library for MuditaOS testing.
It provides user with a:
- connection to MuditaOS phone
- utility to discover MuditaOS on boot & reboot
- base MuditaOS service-desktop protocol implementation which
    - is able to process any service-desktop transaction
    - is extensible to add any endpoint handling
    - has build in error handling with preferred `api` approach

# FAQ

## My computer doesn't see harness and there is no session -  just timeout, and an error

### Check if Mudita Pure is properly connected

Check the device, it should be either `ls /dev/tty*` or `cat /dev/ttyUSBx`.
If there is no device:
- try connecting and disconnecting the phone with the USB port while verifying with `sudo journalctl -f` if there are any new logs
- check if your USB cable is right (and works)
- check if your USB port on the computer works fine - please check with a direct USB port without any hubs

There are three easy ways to check which USB device is your MuditaOS phone:
- `udevadm info -a -n /dev/ttyACM1` will show device information, it should have `Mudita` in `manufacturer` field
- `sudo lsusb -vvv` -> and check which device has Mudita in description
- see `dmesg` output when connection the MuditaOS - there will be log with new tty added

### Add user access without sudo

First check if you can access device without sudo.
**example**
`cat /dev/ttyACM1`
when your MuditaOS is /dev/ttyACM1 will "hang" if you have access without root. Without - it will end with error

Check what groups MuditaOS phone has:
`ls -la /dev/ttyACM1`

If the device is in any other user group than `root` i.e. `dialout` it should suffice to add user to this group. with:
`sudo usermod -a -G dialout $USER`
**you need to logout and login user so that group will work**

If device is in root - you will have to add udev rule so that it would end up in some group available to user.
1. you will need to add group i.e. `dialout` if not already on PC
2. add udev rule which will add device to `dialout` group. You will need two have two things from USB device description (i.e. from `lsusb -vvv` mentioned previously)
    - idVendor
    - idProduct

**exemplary udev rule**
`ATTRS{idVendor}=="1fc9", ATTRS{idProduct}=="0094", MODE="666", GROUP="dialout"`

Reload the udev rules - **this is super important**!
`sudo udevadm control --reload-rules && sudo udevadm trigger`

## What are the folders?

```
├── README.md                                  : this documentation
├── api                                        : endpoint implementations in Harness
│   ├── developermode.py
│   ├── device_info.py
│   ├── filesystem.py
│   ├── generic.py
│   └── update.py
├── dom_parser_utils.py                        : utility to get GUI DOM
├── harness.py                                 : main harness class used
├── harnesscache.py                            : harness class used for session caching
├── interface                                  : low level physical interface - not API interface, or API look for api folder
│   ├── CDCSerial.py
│   ├── defs.py
│   └── error.py
├── request.py                                 : request - response base harness implementation
├── rt_harness_discovery.py                    : connection discovery for harness and harnesscache
└── utils.py                                   : utilities which didn't fit in other files and catalogs
```

As one can see the catalog layout is not perfect and is a result of constant utility growth.
All `*py` files shuld have

## How does the endpoint work?

Please read the dedicated [endpoints documentation](https://appnroll.atlassian.net/wiki/spaces/MFP/pages/656637953/Protocol+description)

## How to add harness API

Please use existing API, do not modify existing endpoints behavior if it's not needed for Mudita Center
If you need to expand the existing API - please contact solution architects first.

## How do I add a test?

For MuditaOS there is a repository just for that: 
[QAMuditaOS](https://github.com/mudita/QAMuditaOS)

## What's next?

If you managed to read this all, you are ready to use harness! Enjoy! You are welcome :)
