import { RefreshCw, RotateCcw, Wrench } from "lucide-react";
import React, { useEffect, useState } from "react";

import { lockersApi } from "../api/modules";
import DataTable from "../components/DataTable";
import MessageBox from "../components/MessageBox";
import MetricCard from "../components/MetricCard";
import PageHeader from "../components/PageHeader";
import StatusBadge from "../components/StatusBadge";

export default function LockerMonitorPage() {
  const [cells, setCells] = useState([]);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");

  const load = async () => {
    setError("");
    try {
      const [cellData, summaryData] = await Promise.all([lockersApi.list(), lockersApi.summary()]);
      setCells(cellData);
      setSummary(summaryData);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const operate = async (fn) => {
    setError("");
    try {
      await fn();
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <PageHeader
        title="柜格状态监控"
        description="查看柜格占用、开门、维护状态，支持释放柜格和标记维护。"
        action={<button className="ghost" onClick={load}><RefreshCw size={16} />刷新</button>}
      />
      <div className="metric-grid compact">
        <MetricCard title="空闲" value={summary?.empty ?? 0} />
        <MetricCard title="已占用" value={summary?.occupied ?? 0} />
        <MetricCard title="已开门" value={summary?.open ?? 0} />
        <MetricCard title="维护中" value={summary?.maintenance ?? 0} />
      </div>
      <MessageBox type="error">{error}</MessageBox>
      <section className="panel">
        <DataTable
          rows={cells}
          columns={[
            { key: "code", title: "柜格" },
            { key: "zone", title: "区域" },
            { key: "size", title: "尺寸", render: (row) => row.size_label },
            { key: "temperature", title: "温度", render: (row) => `${row.temperature}°C` },
            { key: "status", title: "状态", render: (row) => <StatusBadge status={row.status} label={row.status_label} /> },
            {
              key: "actions",
              title: "操作",
              render: (row) => (
                <div className="row-actions">
                  <button className="ghost" onClick={() => operate(() => lockersApi.reset(row.id))}><RotateCcw size={15} />释放</button>
                  <button className="ghost danger" onClick={() => operate(() => lockersApi.markMaintenance(row.id))}><Wrench size={15} />维护</button>
                </div>
              ),
            },
          ]}
        />
      </section>
    </>
  );
}
