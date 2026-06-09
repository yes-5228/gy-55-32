import { Bell, Boxes, PackageCheck, RotateCcw } from "lucide-react";
import React, { useEffect, useState } from "react";

import { lockersApi, notificationsApi, parcelsApi, returnsApi } from "../api/modules";
import DataTable from "../components/DataTable";
import MetricCard from "../components/MetricCard";
import PageHeader from "../components/PageHeader";
import StatusBadge from "../components/StatusBadge";

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [parcels, setParcels] = useState([]);
  const [returns, setReturns] = useState([]);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    Promise.all([lockersApi.summary(), parcelsApi.list(), returnsApi.list(), notificationsApi.list()]).then(
      ([summaryData, parcelData, returnData, notificationData]) => {
        setSummary(summaryData);
        setParcels(parcelData);
        setReturns(returnData);
        setNotifications(notificationData);
      },
    );
  }, []);

  const storedCount = parcels.filter((parcel) => parcel.status === "stored").length;
  const pendingReturns = returns.filter((item) => item.status === "pending").length;

  return (
    <>
      <PageHeader title="运营总览" description="快件流转、柜格占用、通知发送和退件处理集中看板。" />
      <div className="metric-grid">
        <MetricCard title="柜格总数" value={summary?.total ?? "-"} hint={`空闲 ${summary?.empty ?? 0}`} icon={Boxes} />
        <MetricCard title="在柜快件" value={storedCount} hint="等待用户取件" icon={PackageCheck} />
        <MetricCard title="待处理退件" value={pendingReturns} hint="需操作员确认" icon={RotateCcw} />
        <MetricCard title="通知记录" value={notifications.length} hint="入库通知已发送" icon={Bell} />
      </div>
      <section className="panel">
        <h2>最近入库</h2>
        <DataTable
          rows={parcels.slice(0, 6)}
          columns={[
            { key: "tracking_no", title: "运单号" },
            { key: "receiver_name", title: "收件人" },
            { key: "carrier", title: "承运商" },
            { key: "cell", title: "柜格", render: (row) => row.locker_cell_detail?.code },
            { key: "status", title: "状态", render: (row) => <StatusBadge status={row.status} label={row.status_label} /> },
          ]}
        />
      </section>
    </>
  );
}
