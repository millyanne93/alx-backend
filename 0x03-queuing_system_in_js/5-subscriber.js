import { createClient } from 'redis';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
  
  client.subscribe('holberton school channel', (err) => {
    if (err) {
      console.error('Error subscribing to channel:', err.message);
    } else {
      console.log('Subscribed to holberton school channel');
    }
  });
});

client.on('error', (err) => {
  console.error('Redis client not connected to the server:', err.message);
});

client.on('message', (channel, message) => {
  console.log(message);
  
  if (message === 'KILL_SERVER') {
    client.unsubscribe('holberton school channel');
    client.quit();
  }
});
