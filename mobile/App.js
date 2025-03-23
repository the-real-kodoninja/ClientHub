// ClientHubMobile/App.js
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import DashboardScreen from './screens/DashboardScreen';
import ClientListScreen from './screens/ClientListScreen';
import LogsScreen from './screens/LogsScreen';
import LoginScreen from './screens/LoginScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Dashboard" component={DashboardScreen} />
        <Stack.Screen name="Clients" component={ClientListScreen} />
        <Stack.Screen name="Logs" component={LogsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}