import React, { useState } from 'react';
import { View, Text, TextInput, Button } from 'react-native';

const App = () => {
  const [roomName, setRoomName] = useState('');
  const [joinRoomName, setJoinRoomName] = useState('');

  const createRoom = () => {
    console.log('Creating room:', roomName);

    // Call the API to create a room
    fetch('http://localhost:8000/create_room/{roomName}', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        '_Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        name: roomName,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Room created:', data);
      })
      .catch((error) => {
        console.error('Error creating room:', error);
      });

    setRoomName('');
  };

  const joinRoom = () => {
    console.log('Joining room:', joinRoomName);

    // Call the API to join a room
    fetch('http://localhost:8000/join_room/{roomName}', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        '_Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        name: roomName,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Room joined:', data);
      })
      .catch((error) => {
        console.error('Error joining room:', error);
      });

    setJoinRoomName('');
  };

  return (
    <View>
      <Text>Create a Room:</Text>
      <TextInput
        placeholder="Enter new room name"
        value={roomName}
        onChangeText={(text) => setRoomName(text)}
      />
      <Button title="Create" onPress={createRoom} />

      <Text>or join room</Text>
      <TextInput
        placeholder="Enter existing room name"
        value={joinRoomName}
        onChangeText={(text) => setJoinRoomName(text)}
      />
      <Button title="Join" onPress={joinRoom} />
    </View>
  );
};

export default App;