// App.js
// MZ/X ANDROID – React Native prémium mobil verzió
// 3D AI Core + Binance Realtime + AI Panels (mobilra optimalizált)

import React from 'react';
import { StatusBar, SafeAreaView, View, StyleSheet } from 'react-native';
import AICore3D from './components/AICore3D';
import NeuralPanel from './components/NeuralPanel';
import TradingPanel from './components/TradingPanel';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <View style={styles.coreWrapper}>
        <AICore3D />
      </View>
      <View style={styles.panelsWrapper}>
        <NeuralPanel />
        <TradingPanel />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#080014',
  },
  coreWrapper: {
    flex: 3,
    justifyContent: 'center',
    alignItems: 'center',
  },
  panelsWrapper: {
    flex: 2,
    padding: 12,
    gap: 12,
  },
});
