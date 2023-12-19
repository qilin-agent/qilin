import './App.css';
import * as React from 'react';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Root } from './layout/Root';
import { ErrorPage } from './layout/ErrorPage';
import { Chat } from './chats/Chat';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root></Root>,
    errorElement: <ErrorPage></ErrorPage>,
    children: [
      {
        path: "/chats/:chatId",
        element: <Chat></Chat>,
      }
    ],
  },
]);

function App() {

  return (
    <RouterProvider router={router} />
  );

}

export default App;
