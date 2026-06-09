import React from "react";
import ReactDOM from "react-dom/client";
import { Navigate, RouterProvider, createBrowserRouter } from "react-router-dom";

import AppLayout from "./layouts/AppLayout.jsx";
import DashboardPage from "./pages/DashboardPage.jsx";
import InboundPage from "./pages/InboundPage.jsx";
import PickupPage from "./pages/PickupPage.jsx";
import LockerMonitorPage from "./pages/LockerMonitorPage.jsx";
import ReturnPage from "./pages/ReturnPage.jsx";
import NotificationsPage from "./pages/NotificationsPage.jsx";
import "./styles/global.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: "dashboard", element: <DashboardPage /> },
      { path: "inbound", element: <InboundPage /> },
      { path: "pickup", element: <PickupPage /> },
      { path: "lockers", element: <LockerMonitorPage /> },
      { path: "returns", element: <ReturnPage /> },
      { path: "notifications", element: <NotificationsPage /> },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);
