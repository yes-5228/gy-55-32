import { Bell, Boxes, ClipboardList, LayoutDashboard, PackagePlus, RotateCcw, ScanLine } from "lucide-react";
import React from "react";
import { NavLink, Outlet } from "react-router-dom";

const navItems = [
  { to: "/dashboard", label: "总览", icon: LayoutDashboard },
  { to: "/inbound", label: "快件入库", icon: PackagePlus },
  { to: "/pickup", label: "取件开箱", icon: ScanLine },
  { to: "/lockers", label: "柜格监控", icon: Boxes },
  { to: "/returns", label: "退件处理", icon: RotateCcw },
  { to: "/notifications", label: "通知记录", icon: Bell },
];

export default function AppLayout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <ClipboardList size={24} />
          <span>快递柜管理</span>
        </div>
        <nav>
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink key={item.to} to={item.to}>
                <Icon size={18} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
