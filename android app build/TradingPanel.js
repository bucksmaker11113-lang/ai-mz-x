// components/TradingPanel.js
// MZ/X ANDROID – Natív kereskedési konzol panel (React Native)
// Élő árak + AI döntés + pozíció státusz

import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function TradingPanel() {
  const [eth, setEth] = useState(null);
  const [btc, setBtc] = useState(null);
  const [decision, setDecision] = useState("Nincs adat");
  const [position, setPosition] = useState("Nincs megnyitva");

  useEffect(() => {
    async function loadData() {
      try {
        const res = await fetch('https://your-backend-url/realtime'); // később beállítjuk
        const data = await res.json();

        setEth(data.eth_price || null);
        setBtc(data.btc_price || null);

        // NATÍV AI döntés később innen jön majd
        if (data.ai_decision) setDecision(data.ai_decision);
        if (data.position_status) setPosition(data.position_status);

      } catch (err) {
        console.log('TradingPanel fetch error:', err);
      }
    }

    loadData();
    const interval = setInterval(loadData, 900);
    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.panel}>
      <Text style={styles.title}>Kereskedési Konzol</Text>

      <Text style={styles.row}>ETH ár: {eth ? eth.toFixed(2) + ' USDC' : 'betöltés...'}</Text>
      <Text style={styles.row}>BTC ár: {btc ? btc.toFixed(2) + ' USDC' : 'betöltés...'}</Text>

      <Text style={styles.row}>AI döntés: {decision}</Text>
      <Text style={styles.row}>Pozíció: {position}</Text>

      <Text style={styles.hint}>Binance Futures élő adat</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  panel: {
    backgroundColor: 'rgba(0, 160, 200, 0.25)',
    borderWidth: 1,
    borderColor: 'rgba(0,255,255,0.4)',
    padding: 14,
    borderRadius: 16,
  },
  title: {
    fontSize: 18,
    color: '#ffffff',
    marginBottom: 10,
    fontWeight: 'bold',
  },
  row: {
    fontSize: 15,
    color: '#dfffff',
    marginBottom: 6,
  },
  hint: {
    fontSize: 12,
    color: '#88ffff',
    marginTop: 10,
    opacity: 0.7,
  },
});
