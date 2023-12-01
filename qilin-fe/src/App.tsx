import './App.css';
import * as React from 'react';
import Grid from '@mui/joy/Grid';
import MessagesPane from './components/MessagesPane';
import Sidebar from './components/Sidebar';
import { ChatProps } from './shared/types';

const currentChat: ChatProps = {
  id: '1',
  sender: {
    name: 'John Doe',
    username: '@johndoe',
    avatar: 'https://i.pravatar.cc/100?img=1',
  },
  messages: [],
};

function App() {

  return (
    <Grid container spacing={0} sx={{ flexGrow: 1 }}>
      <Grid xs={5} sm={4} md={3} lg={2}>
        <Sidebar />
      </Grid>
      <Grid xs={7} sm={8} md={9} lg={10}>
        <MessagesPane chat={currentChat} />
      </Grid>
    </Grid>
  );

}

export default App;
