# Cast Test - Chromecast Dynamic Content PoC

## Purpose
Proof of concept for casting a website with dynamic content to Chromecast devices.

## Project Structure
- `src/server.js` - Express server hosting the castable content
- `public/` - Static files and receiver app
- `public/receiver.html` - Custom receiver app for Chromecast
- `public/sender.html` - Web sender interface to initiate cast

## Key Concepts
- **Sender**: The web page/app that initiates the cast session
- **Receiver**: The app that runs ON the Chromecast device
- **Default Media Receiver**: Google's built-in receiver for simple media
- **Custom Receiver**: Our own HTML/JS that runs on the Chromecast

## Testing
1. Start server: `npm run dev`
2. Access sender page from browser with Cast-enabled extension
3. Cast to device on local network

## Network Requirements
- Server must be accessible from Chromecast (same network)
- Use machine's LAN IP, not localhost
- Chromecast device: 192.168.5.187

## Cast App ID
- Required for custom receiver
- Register at: https://cast.google.com/publish
- Once registered, update APP_ID in sender.html
