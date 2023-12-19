import { AppBar, Avatar, Box, CssBaseline, Drawer, IconButton, Toolbar, Typography } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import * as React from 'react';
import { Outlet } from "react-router-dom";


export interface AppBarProps {
    avatar: string;
    avatarUrl: string;
    title: string;
}

export interface OutletContext {
    setAppBarProps: (props: AppBarProps) => void;
}


export function Root() {

    const drawerWidth = 240;
    const [mobileOpen, setMobileOpen] = React.useState(false);
    const [appBarProps, setAppBarProps] = React.useState<AppBarProps>({
        avatar: 'Q',
        avatarUrl: 'https://avatars.githubusercontent.com/u/25190563?v=4',
        title: 'Responsive drawer',
    });

    const handleDrawerToggle = () => {
        setMobileOpen(!mobileOpen);
    };

    const drawer = (<div>Side bar</div>);

    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <AppBar position="fixed" color="default"
                sx={{
                    width: { sm: `calc(100% - ${drawerWidth}px)` },
                    ml: { sm: `${drawerWidth}px` },
                }}>
                <Toolbar>
                    <IconButton color="inherit" aria-label="open drawer" edge="start" sx={{ mr: 2, display: { sm: 'None' } }} onClick={handleDrawerToggle}>
                        <MenuIcon></MenuIcon>
                    </IconButton>
                    <Avatar alt={appBarProps.avatar} src={appBarProps.avatarUrl} variant="rounded">{appBarProps.avatar}</Avatar>
                    <Typography variant="h6" noWrap component="div" sx={{ ml: 2 }}>
                        {appBarProps.title}
                    </Typography>
                </Toolbar>
            </AppBar>
            <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }} aria-label="drawer">
                <Drawer variant="temporary" open={mobileOpen} onClose={handleDrawerToggle} ModalProps={{ keepMounted: true }} sx={{
                    display: { xs: 'block', sm: 'none' },
                    '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
                }}>
                    {drawer}
                </Drawer>
                <Drawer variant="permanent" sx={{
                    display: { xs: 'none', sm: 'block' },
                    '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
                }}>
                    {drawer}
                </Drawer>
            </Box>
            <Box component="main" sx={{ flexGrow: 1, p: 0, width: { sm: `calc(100% - ${drawerWidth}px)` }, display: 'flex', height: '100vh', flexDirection: 'column' }}>
                <Toolbar></Toolbar>
                <Outlet context={{ setAppBarProps }}></Outlet>
            </Box>
        </Box>
    );

}
