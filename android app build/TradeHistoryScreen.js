// screens/TradeHistoryScreen.js
// MZ/X ANDROID – Kereskedési előzmények + profit / veszteség + equity kalkuláció

import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function TradeHistoryScreen() {
  const [history, setHistory] = useState([]);
  const [equity, setEquity] = useState([]);
  const [startingBalance] = useState(1000); // mobil app induló tőke (USDC)

  // történet betöltése
  async function loadHistory() {
    try {
      const data = await AsyncStorage.getItem('mzx_trade_history');
      if (data) {
        const parsed = JSON.parse(data);
        setHistory(parsed);

        // equity görbe számítása
        let balance = startingBalance;
        const eq = parsed.map((t) => {
          balance += t.profit;
          return balance;
        });
        setEquity(eq);
      }
    } catch (e) {
      console.log('History load error', e);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Kereskedési Előzmények</Text>

      {history.length === 0 && (
        <Text style={styles.empty}>Nincs még kereskedés rögzítve.</Text>
      )}

      {history.map((t, i) => (
        <View key={i} style={styles.tradeBox}>
          <Text style={styles.row}>Pár: {t.pair}</Text>
          <Text style={styles.row}>Akció: {t.side}</Text>
          <Text style={styles.row}>Belépés: {t.entry}</Text>
          <Text style={styles.row}>Kilépés: {t.exit}</Text>
          <Text style={styles.row}>Profit: {t.profit.toFixed(2)} USDC</Text>
          <Text style={styles.time}>{t.time}</Text>
        </View>
      ))}

      {equity.length > 0 && (
        <View style={styles.equityBox}>
          <Text style={styles.section}>Equity alakulása (USDC)</Text>
          {equity.map((v, i) => (
            <Text key={i} style={styles.eqRow}>{i+1}. lépés → {v.toFixed(2)} USDC</Text>
          ))}
        </View>
      )}
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
  empty: {
    fontSize: 16,
    color: '#ccc',
    marginTop: 20,
  },
  tradeBox: {
    borderWidth: 1,
    borderColor: 'rgba(0,255,255,0.4)',
    padding: 12,
    borderRadius: 14,
    marginBottom: 14,
    backgroundColor: 'rgba(0, 180, 255, 0.15)',
  },
  row: {
    fontSize: 15,
    color: '#e8ffff',
    marginBottom: 5,
  },
  time: {
    marginTop: 6,
    fontSize: 12,
    color: '#88ffff',
  },
  equityBox: {
    marginTop: 20,
    padding: 12,
    borderRadius: 14,
    backgroundColor: 'rgba(120,0,200,0.2)',
    borderWidth: 1,
    borderColor: 'rgba(255,0,255,0.3)',
  },
  section: {
    fontSize: 18,
    color: '#ffb7ff',
    marginBottom: 10,
  },
  eqRow: {
    fontSize: 14,
    color: '#f0dfff',
    marginBottom: 4,
  },
});
