// screens/HomeScreen.js
// MZ/X ANDROID – Főképernyő: 3D AI Core + Panels + Binance stream + Q-learning döntések

import React from 'react';
import { View, ScrollView, StyleSheet } from 'react-native';

import AICore3D from '../components/AICore3D';
import NeuralPanel from '../components/NeuralPanel';
import TradingPanel from '../components/TradingPanel';
import { useBinanceRealtime } from '../binance/realtime';
import { aiDecision } from '../ai/qlearning';

export default function HomeScreen() {
  const { eth, btc, trend, vol } = useBinanceRealtime();

  // AI döntés automatikusan minden árfrissítésnél
  let aiAction = "NOP";
  if (eth) {
    aiAction = aiDecision(eth - vol, eth, trend, vol);
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.coreWrapper}>
        <AICore3D />
      </View>

      <View style={styles.panelsWrapper}>
        <NeuralPanel />
        <TradingPanel aiAction={aiAction} />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#080014',
  },
  coreWrapper: {
    height: 360,
    width: '100%',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  panelsWrapper: {
    padding: 12,
    gap: 14,
  },
});
