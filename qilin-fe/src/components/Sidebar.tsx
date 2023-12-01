import * as React from 'react';
import Box from '@mui/joy/Box';
import Sheet from '@mui/joy/Sheet';
import List from '@mui/joy/List';
import ListItemButton from '@mui/joy/ListItemButton';
import ModalClose from '@mui/joy/ModalClose';

export default function Sidebar() {
  return (
    <Sheet>
      <List
        size="lg"
        component="nav"
        sx={{
          flex: 'none',
          fontSize: 'xl',
          '& > div': { justifyContent: 'left' },
        }}
      >
        <ListItemButton sx={{ fontWeight: 'lg' }}>Home</ListItemButton>
        <ListItemButton>All Chats</ListItemButton>
        <ListItemButton>My Bots</ListItemButton>
        <ListItemButton>My Profile</ListItemButton>
        <ListItemButton>Settings</ListItemButton>
      </List>
    </Sheet>
  );
}
