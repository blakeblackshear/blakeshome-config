## Overview
This is the my configuration for my home server. It serves the following functions:
- nginx proxy
- oauth2_proxy for authentication across all applications
- homeassistant
- appdaemon
- mqtt (mosquitto)
- ffmpeg based ip camera recording
- motion detection for ip cameras
- (future) tensorflow based object detection for cameras
- pihole for adblocking and dhcp server
- unifi controller for network gear
- postgres (db for homeassistant)

## HomeAssistant
My config isn't very organized. Still trying to decide what works best for me.
### Components
- **Switches**: Homeseer Z-Wave dimmers + Cooper 5-button Scene Controller
- **Bulbs**: Hue zigbee bulbs
- **Sensors**: Xiaomi zigbee sensors
- **Thermostats**: Ecobee 3 lite
- **Smart Plugs**: Sonoff S31 flashed with Tasmota
- **Led Strips**: H801 flashed with Tasmota
- **Smart Locks**: Schlage Connect Z-Wave
- **Whole Home Audio**: Google Chromecast
- **Voice Control**: Google Home
- **Media Control**: Harmony Hub
- **Vacuum**: Xiaomi Mi Vacuum Gen1 (rooted)
- **Lawn Mower**: Worx Landroid M
- **Cameras**: Dahua IPC-HDW5231R-Z
- **Presence Detection**: Google Location Sharing + DHCP Leases + Unifi Controller
- **Notifications**: Twilio + HTML5
- **Custom ESP8266 Devices**:
  - Fireplace
  - Smoke/CO Detector (Kidde SM120X/CO120X)
  - Garage Doors

### Automations

- Turn on the outside lights when the garage opens after sunset for 5 minutes or until the back door is locked
- Notify me if the garage is left open while we are not home and give me the option to close it
- Sync the cabinet lighting with the kitchen lights, taking into consideration daytime vs nighttime
- Make sure the fireplace is off if we are not home
- Integrate the Harmony Hub with the status of the Chromecast audio to automatically switch inputs when music starts, and stopping playback when switching to another activity
- Unlock the back door when someone arrives home
- Turn on closets, bathrooms, pantry, and laundry with motion
- When it is hot in the media room, prompt to turn on the media room a/c if we are near home at 7pm
- Standard lighting scenes for when we are not home and when we arrive, taking into account day vs night
- Arm the alarm system when we are not home
- Set off the alarm if the garage opens
- Disarm the alarm when we arrive or when a valid code is entered on the smart locks
- Ensure the doors are locked if we are away, and notify me if they cant be locked automatically
- Baby monitor mode to send alerts if motion is detected inside the house if we are grabbing a drink at the neighbors after the kids go to bed
- Notify me by text if the smoke or co alarms go off
- Alert me if any battery devices drop below 25%
- Dog sitter mode to notify if any motion sensors go off upstairs while we are on vacation even if the alarm is disarmed
- Start the vacuum after the dog sitters lock the door if it hasnt already run in the past 24 hours
- Guest mode to prevent some of the automations based on presence detection, automatically enabled when certain devices are present
- Upstairs hall lamps turn on after sunrise, dim before sunset, and turn on with motion after 10pm
- Notify Ali to switch over the laundry 5 minutes after it finishes if no motion has been detected. If she isn't home, wait until she gets home and then notify her
- Turn on the porch light at sunset and off at sunrise
- Vacation mode to randomly turn lights on and off while we are gone
- Enable/disable vacation mode when we are both more than 50km away
- Set the thermostats to away/home when vacation mode is turned on/off
- Start the vacuum when Ali leaves to take the kids to school in the mornings
- Start the vacuum when Ali arrives at the gym
- Ask about starting the vacuum when we are not home on the weekends, and the vacuum hasnt run in the past 24 hours
- Notify me if any of the water leak detectors detect water

## Other Stuff
### Mount data drive in CoreOS
```
sudo parted /dev/sdc mklabel gpt
sudo parted -a opt /dev/sdc mkpart primary ext4 0% 100%
lsblk
sudo mkfs.xfs -L data /dev/sdc1
sudo mkdir -p /mnt/data
UUID=8200b18e-7943-4924-b458-81be1887602a /mnt/data xfs defaults 0 2
sudo mount -a
```

