#!/usr/bin/env python3
"""
Automatic Chromecast casting using PyChromecast.
No browser, no user interaction required.
"""

import pychromecast
import pychromecast.controllers
import time
import sys

# Configuration
APP_ID = "857B94F0"
NAMESPACE = "urn:x-cast:com.casttest.custom"
CHROMECAST_NAME = "Old Chromecast"  # Friendly name from Google Home

def discover_chromecasts():
    """Find all Chromecasts on the network."""
    print("Discovering Chromecasts...")
    services, browser = pychromecast.discovery.discover_chromecasts()
    pychromecast.discovery.stop_discovery(browser)

    print(f"Found {len(services)} device(s):")
    for service in services:
        print(f"  - {service.friendly_name} ({service.host})")

    return services

def connect_to_chromecast(name=None, ip=None):
    """Connect to a specific Chromecast by name or IP."""
    if ip:
        print(f"Connecting to Chromecast at {ip}...")
        chromecasts, browser = pychromecast.get_chromecasts(
            known_hosts=[ip]
        )
        pychromecast.discovery.stop_discovery(browser)
        if not chromecasts:
            print(f"No Chromecast found at {ip}")
            return None
        cast = chromecasts[0]
    else:
        print(f"Looking for Chromecast: {name}...")
        chromecasts, browser = pychromecast.get_listed_chromecasts(
            friendly_names=[name]
        )
        pychromecast.discovery.stop_discovery(browser)

        if not chromecasts:
            print(f"Could not find Chromecast: {name}")
            return None

        cast = chromecasts[0]

    cast.wait()
    print(f"Connected to: {cast.name}")
    print(f"  Model: {cast.model_name}")
    print(f"  Cast Type: {cast.cast_type}")
    print(f"  UUID: {cast.uuid}")
    return cast

def launch_receiver(cast, app_id):
    """Launch the custom receiver app."""
    print(f"Launching app {app_id}...")
    cast.start_app(app_id)

    # Wait for app to launch
    time.sleep(3)

    if cast.app_id == app_id:
        print("Custom receiver launched successfully!")
        return True
    else:
        print(f"App launch may have failed. Current app: {cast.app_id}")
        return False

class CustomController(pychromecast.controllers.BaseController):
    """Controller for custom receiver messages."""

    def __init__(self, namespace):
        super().__init__(namespace, "CC")
        self.namespace = namespace

    def receive_message(self, _message, data):
        print(f"Received: {data}")
        return True

    def send(self, data):
        self.send_message(data)

def send_message(cast, namespace, data):
    """Send a message to the receiver."""
    print(f"Sending message: {data}")

    # Create and register controller
    controller = CustomController(namespace)
    cast.register_handler(controller)

    # Send the message
    controller.send(data)
    print("Message sent!")

def cast_url(cast, url):
    """Cast a URL to the receiver."""
    send_message(cast, NAMESPACE, {"loadUrl": url})

def clear_content(cast):
    """Clear content on receiver."""
    send_message(cast, NAMESPACE, {"clearUrl": True})

def main():
    # Connect directly by IP (works better in WSL/Docker)
    cast = connect_to_chromecast(ip="192.168.5.187")

    if not cast:
        print("Failed to connect")
        sys.exit(1)

    print()

    # Launch the custom receiver
    if not launch_receiver(cast, APP_ID):
        print("Warning: App may not have launched correctly")

    print()

    # Cast a URL
    test_url = "http://192.168.4.217:8080/receiver.html"
    print(f"Casting URL: {test_url}")
    cast_url(cast, test_url)

    print()
    print("Done! Check your Chromecast.")
    print()
    print("The cast session will remain active.")
    print("You can send more URLs programmatically without re-launching.")

if __name__ == "__main__":
    main()
