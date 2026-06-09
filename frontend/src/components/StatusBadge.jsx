import React from "react";

const statusMap = {
  empty: "green",
  occupied: "amber",
  open: "blue",
  maintenance: "red",
  stored: "amber",
  picked_up: "green",
  return_pending: "red",
  returned: "gray",
  pending: "amber",
  completed: "green",
  sent: "green",
  failed: "red",
};

export default function StatusBadge({ status, label }) {
  return <span className={`badge ${statusMap[status] || "gray"}`}>{label || status}</span>;
}
