// AppNavigator.js
// MZ/X ANDROID – Képernyő navigáció + AI/Realtime összekötése
// Ez a modul az egész natív app vezérlőközpontja

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import HomeScreen from './screens/HomeScreen';
import AIDetailsScreen from './screens/AIDetailsScreen';
import TradeHistoryScreen from './screens/TradeHistoryScreen';

const Stack = createStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerShown: false,
          animation: 'fade',
        }}
      >
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="AI" component={AIDetailsScreen} />
        <Stack.Screen name="History" component={TradeHistoryScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
