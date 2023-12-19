import * as React from 'react';
import { useParams, useOutletContext } from 'react-router-dom';
import { OutletContext } from '../layout/Root';
import { Box, Button, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import RestartIcon from '@mui/icons-material/RestartAlt';

export function Chat() {

    let { chatId } = useParams<{ chatId: string }>();
    const { setAppBarProps } = useOutletContext<OutletContext>();

    React.useEffect(() => {
        setAppBarProps({
            avatar: 'Q',
            avatarUrl: 'https://avatars.githubusercontent.com/u/25190563?v=4',
            title: `Chat with ${chatId}`,
        });
    }, [chatId, setAppBarProps]);

    return (
        <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
            <div style={{ flexGrow: 1, flexShrink: 1 }}>
                Chat with {chatId}
            </div>
            <div style={{ flexGrow: 0, flexShrink: 0 }}>
            </div>
            <Box sx={{ flexGrow: 0, flexShrink: 0, display: 'flex', flexDirection: 'row', p: 1 }}>
                <IconButton size="large">
                    <RestartIcon fontSize="inherit" />
                </IconButton>
                <textarea style={{ flexGrow: 1, flexShrink: 1, resize: 'none', height: '52px', margin: '0 8px', fontFamily: 'sans-serif', borderRadius: '8px', padding: '0 8px' }}></textarea>
                <Button variant="contained" endIcon={<SendIcon fontSize='inherit' />} size="large" sx={{ borderRadius: '26px' }}>
                    Send
                </Button>
            </Box>
        </Box>
    );

}
