// components/NeuralPanel.js
// MZ/X ANDROID – Neurális adatpanel mobilra (ETH/BTC ár + trend + vol)

import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function NeuralPanel() {
  const [eth, setEth] = useState(null);
  const [btc, setBtc] = useState(null);
  const [trend, setTrend] = useState(0.5);
  const [vol, setVol] = useState(0.02);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await fetch('https://your-backend-url/realtime'); // később kitöltjük
        const data = await res.json();
        setEth(data.eth_price || null);
        setBtc(data.btc_price || null);
        setTrend(data.visual_trend || 0.5);
        setVol(data.visual_vol || 0.02);
      } catch (err) {
        console.log('Realtime fetch error:', err);
      }
    }

    loadData();
    const interval = setInterval(loadData, 800);
    return () => clearInterval(interval);
  }, []);

  const trendText =
    trend > 0.55 ? 'Erős emelkedés' : trend < 0.45 ? 'Csökkenő trend' : 'Oldalazás';

  return (
    <View style={styles.panel}>
      <Text style={styles.title}>Neurális Piaci Adatok</Text>

      <Text style={styles.row}>ETH ár: {eth ? eth.toFixed(2) + ' USDC' : 'betöltés...'}</Text>

      <Text style={styles.row}>BTC ár: {btc ? btc.toFixed(2) + ' USDC' : 'betöltés...'}</Text>

      <Text style={styles.row}>Trend: {trendText}</Text>

      <Text style={styles.row}>Volatilitás: {(vol * 100).toFixed(2)}%</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  panel: {
    backgroundColor: 'rgba(120, 0, 200, 0.25)',
    borderWidth: 1,
    borderColor: 'rgba(255, 0, 255, 0.4)',
    padding: 14,
    borderRadius: 16,
    backdropFilter: 'blur(10px)', // csak android 12+ alatt hatásos
  },
  title: {
    fontSize: 18,
    color: '#ffffff',
    marginBottom: 8,
    fontWeight: 'bold',
  },
  row: {
    fontSize: 15,
    color: '#e7dfff',
    marginBottom: 6,
  },
});
