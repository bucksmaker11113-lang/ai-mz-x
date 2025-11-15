// screens/AIDetailsScreen.js
// MZ/X ANDROID – AI Részletes képernyő: Q-mátrix, döntések, reward vizualizáció

import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';
import { Q } from '../ai/qlearning';
import { useBinanceRealtime } from '../binance/realtime';
import { aiDecision } from '../ai/qlearning';

export default function AIDetailsScreen() {
  const { eth, trend, vol } = useBinanceRealtime();
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!eth) return;

    const newDecision = aiDecision(eth - vol, eth, trend, vol);

    setHistory((prev) => [
      {
        price: eth,
        trend,
        vol,
        decision: newDecision,
        time: new Date().toLocaleTimeString(),
      },
      ...prev,
    ].slice(0, 40));
  }, [eth]);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>AI Diagnosztikai Képernyő</Text>

      <Text style={styles.section}>Q-mátrix (9 állapot × 3 akció)</Text>
      {Q.map((row, i) => (
        <Text key={i} style={styles.row}>Állapot {i}: {JSON.stringify(row)}</Text>
      ))}

      <Text style={styles.section}>Legutóbbi AI döntések</Text>
      {history.map((h, i) => (
        <View key={i} style={styles.historyItem}>
          <Text style={styles.label}>{h.time}</Text>
          <Text style={styles.item}>Ár: {h.price.toFixed(2)}</Text>
          <Text style={styles.item}>Trend: {h.trend.toFixed(2)}</Text>
          <Text style={styles.item}>Vol: {(h.vol * 100).toFixed(2)}%</Text>
          <Text style={styles.item}>Döntés: {h.decision}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#080014',
    padding: 12,
  },
  title: {
    fontSize: 22,
    color: '#fff',
    fontWeight: 'bold',
    marginBottom: 16,
  },
  section: {
    fontSize: 18,
    color: '#cc99ff',
    marginTop: 12,
    marginBottom: 8,
  },
  row: {
    fontSize: 14,
    color: '#eee',
    marginVertical: 2,
  },
  historyItem: {
    borderWidth: 1,
    borderColor: 'rgba(255,0,255,0.3)',
    padding: 10,
    borderRadius: 12,
    marginBottom: 10,
    backgroundColor: 'rgba(120,0,200,0.15)',
  },
  item: {
    fontSize: 14,
    color: '#f0dfff',
  },
  label: {
    color: '#ffb7ff',
    fontWeight: 'bold',
    marginBottom: 4,
  },
});
