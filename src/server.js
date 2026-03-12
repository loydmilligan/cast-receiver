import express from 'express';
import { networkInterfaces } from 'os';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const PORT = 8080;

app.use(express.static(path.join(__dirname, '../public')));
app.use(express.json());

// Get local IP for Chromecast access
function getLocalIP() {
  const nets = networkInterfaces();
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      if (net.family === 'IPv4' && !net.internal) {
        return net.address;
      }
    }
  }
  return 'localhost';
}

app.listen(PORT, '0.0.0.0', () => {
  const ip = getLocalIP();
  console.log(`\n🎬 Cast Test Server Running`);
  console.log(`   Local:   http://localhost:${PORT}`);
  console.log(`   Network: http://${ip}:${PORT}`);
  console.log(`\n   Use the Network URL for Chromecast!\n`);
});
