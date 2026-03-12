# Cast Receiver - Chromecast Custom Receiver Service

## Purpose
This service hosts a custom Chromecast receiver that displays arbitrary web content (URLs) on Chromecast devices. It serves as the receiver component for the lyric-scroll Home Assistant addon, allowing lyrics to be cast automatically to Chromecast displays.

## How It Works
1. **Receiver HTML** (`public/receiver.html`) runs directly ON the Chromecast
2. The receiver contains an iframe that can load any URL sent to it
3. **PyChromecast** (from the addon) connects to Chromecast and sends URLs to display
4. No browser or manual interaction needed after initial setup

## Project Structure
```
├── src/
│   ├── server.js           # Express server (serves receiver + sender)
│   ├── chromecast_caster.py # Python module for automatic casting
│   └── auto_cast.py        # Test script for PyChromecast
├── public/
│   ├── receiver.html       # Runs ON Chromecast (iframe-based URL loader)
│   └── sender.html         # Manual browser-based sender (backup/testing)
├── Dockerfile
├── docker-compose.yml
└── package.json
```

## Deployment

### Production (Docker on Pi)
Deployed on piUSBcam (192.168.4.158) running on port 9123.

**Receiver URL:** `http://192.168.4.158:9123/receiver.html`

**Deploy changes:**
```bash
ssh pi "cd ~/cast-receiver && git pull && docker compose up -d --build"
```

**Check status:**
```bash
ssh pi "docker ps --filter name=cast-receiver"
ssh pi "docker logs cast-receiver"
```

**Restart:**
```bash
ssh pi "cd ~/cast-receiver && docker compose restart"
```

**Full redeploy:**
```bash
ssh pi "cd ~/cast-receiver && docker compose down && docker compose up -d --build"
```

### Local Development
```bash
npm install
npm run dev
# Access at http://localhost:8080
```

## Configuration

### Cast App ID
- **App ID:** `857B94F0`
- **Console:** https://cast.google.com/publish
- **Receiver URL in Console:** `http://192.168.4.158:9123/receiver.html`

### Registered Chromecast Devices
Devices must be registered in Cast Console for unpublished apps:
| Serial | Name | IP |
|--------|------|-----|
| 6920103PYB5A | Old Chromecast | 192.168.5.187 |

**To add new devices:**
1. Get serial from Google Home app (Device → Settings → scroll down)
2. Add in Cast Console → App → Devices → Add Cast Receiver Device
3. Reboot the Chromecast

## Message Protocol
The receiver listens for JSON messages on namespace `urn:x-cast:com.casttest.custom`:

| Message | Description |
|---------|-------------|
| `{"loadUrl": "http://..."}` | Load URL in iframe |
| `{"clearUrl": true}` | Clear iframe, show standby |
| `{"message": "text"}` | Display text message |
| `{"background": "css"}` | Change background CSS |

## Manual Testing (Browser-based Sender)
For debugging or testing without PyChromecast:
1. Open `http://localhost:8080/sender.html` (must be localhost for Cast SDK)
2. Enter App ID: `857B94F0`
3. Click Initialize Cast
4. Click Start Casting
5. Enter URL and click Cast URL

## GitHub Repository
- **Repo:** https://github.com/loydmilligan/cast-receiver
- **Visibility:** Public (for easy cloning on Pi)
