import { RefreshCw } from "lucide-react";
import React, { useEffect, useState } from "react";

import { notificationsApi } from "../api/modules";
import DataTable from "../components/DataTable";
import PageHeader from "../components/PageHeader";
import StatusBadge from "../components/StatusBadge";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);
  const load = () => notificationsApi.list().then(setNotifications);

  useEffect(() => {
    load();
  }, []);

  return (
    <>
      <PageHeader
        title="通知记录"
        description="快件入库后生成的取件通知发送记录。"
        action={<button className="ghost" onClick={load}><RefreshCw size={16} />刷新</button>}
      />
      <section className="panel">
        <DataTable
          rows={notifications}
          columns={[
            { key: "tracking_no", title: "运单号" },
            { key: "channel", title: "渠道", render: (row) => row.channel_label },
            { key: "recipient", title: "接收人" },
            { key: "message", title: "内容" },
            { key: "status", title: "状态", render: (row) => <StatusBadge status={row.status} label={row.status_label} /> },
          ]}
        />
      </section>
    </>
  );
}
