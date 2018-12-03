FROM pihole/pihole:latest

# install mosquitto clients to allow dhcp leases to be
# published to mqtt
RUN apt-get update && \
    apt-get install -y mosquitto-clients && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

# Prevent dhcp leases from being passed to the script on reboot.
# This would make it look like all devices with dhcp leases just
# made a dhcp request.
# This may cause the same ip to be issued to multiple devices.
# I could also read the dhcp leases file in my script and check
# the expiration for the given IP.
RUN ln -s /dev/null /etc/pihole/dhcp.leases