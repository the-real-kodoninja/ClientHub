// ClientHubMobile/screens/DashboardScreen.js
import React from 'react';
import { View, Text, Button } from 'react-native';

export default function DashboardScreen({ navigation }) {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#f5f5f0' }}>
      <Text style={{ color: '#4a7048', fontSize: 24 }}>ClientHub Mobile</Text>
      <Button title="View Clients" onPress={() => navigation.navigate('Clients')} color="#8b6f47" />
    </View>
  );
}