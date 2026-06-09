import React from "react";

export default function MessageBox({ type = "info", children }) {
  if (!children) return null;
  return <div className={`message ${type}`}>{children}</div>;
}
