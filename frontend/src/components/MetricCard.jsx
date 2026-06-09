import React from "react";

export default function MetricCard({ title, value, hint, icon: Icon }) {
  return (
    <section className="metric-card">
      <div className="metric-icon">{Icon ? <Icon size={20} /> : null}</div>
      <div>
        <p>{title}</p>
        <strong>{value}</strong>
        {hint ? <span>{hint}</span> : null}
      </div>
    </section>
  );
}
