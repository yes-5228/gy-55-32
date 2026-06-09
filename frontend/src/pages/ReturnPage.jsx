import { CheckCircle2, RefreshCw, RotateCcw } from "lucide-react";
import React, { useEffect, useMemo, useState } from "react";

import { parcelsApi, returnsApi } from "../api/modules";
import DataTable from "../components/DataTable";
import MessageBox from "../components/MessageBox";
import PageHeader from "../components/PageHeader";
import StatusBadge from "../components/StatusBadge";

export default function ReturnPage() {
  const [parcels, setParcels] = useState([]);
  const [orders, setOrders] = useState([]);
  const [form, setForm] = useState({ parcel_id: "", reason: "timeout", operator: "管理员", remark: "" });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const load = async () => {
    const [parcelData, orderData] = await Promise.all([parcelsApi.list(), returnsApi.list()]);
    setParcels(parcelData);
    setOrders(orderData);
  };

  useEffect(() => {
    load();
  }, []);

  const storedParcels = useMemo(() => parcels.filter((parcel) => parcel.status === "stored"), [parcels]);

  const submit = async (event) => {
    event.preventDefault();
    setMessage("");
    setError("");
    try {
      await returnsApi.create({ ...form, parcel_id: Number(form.parcel_id) });
      setForm({ parcel_id: "", reason: "timeout", operator: "管理员", remark: "" });
      setMessage("退件单已创建。");
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  const complete = async (id) => {
    setMessage("");
    setError("");
    try {
      await returnsApi.complete(id);
      setMessage("退件已完成，柜格已释放。");
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <PageHeader title="退件处理" description="对逾期未取、拒收或异常快件创建退件单，并完成退回释放柜格。" />
      <section className="work-grid">
        <form className="panel form-panel" onSubmit={submit}>
          <h2>创建退件单</h2>
          <label>
            快件
            <select name="parcel_id" value={form.parcel_id} onChange={(event) => setForm({ ...form, parcel_id: event.target.value })} required>
              <option value="">选择在柜快件</option>
              {storedParcels.map((parcel) => (
                <option key={parcel.id} value={parcel.id}>
                  {parcel.tracking_no} / {parcel.receiver_name} / {parcel.locker_cell_detail?.code}
                </option>
              ))}
            </select>
          </label>
          <label>
            原因
            <select name="reason" value={form.reason} onChange={(event) => setForm({ ...form, reason: event.target.value })}>
              <option value="timeout">逾期未取</option>
              <option value="rejected">用户拒收</option>
              <option value="damaged">快件破损</option>
              <option value="other">其他</option>
            </select>
          </label>
          <label>操作员<input value={form.operator} onChange={(event) => setForm({ ...form, operator: event.target.value })} required /></label>
          <label>备注<input value={form.remark} onChange={(event) => setForm({ ...form, remark: event.target.value })} /></label>
          <button type="submit"><RotateCcw size={18} />创建退件</button>
          <MessageBox type="success">{message}</MessageBox>
          <MessageBox type="error">{error}</MessageBox>
        </form>
        <section className="panel">
          <div className="panel-title">
            <h2>退件单</h2>
            <button className="ghost" onClick={load}><RefreshCw size={16} />刷新</button>
          </div>
          <DataTable
            rows={orders}
            columns={[
              { key: "tracking_no", title: "运单号", render: (row) => row.parcel_detail?.tracking_no },
              { key: "reason", title: "原因", render: (row) => row.reason_label },
              { key: "operator", title: "操作员" },
              { key: "status", title: "状态", render: (row) => <StatusBadge status={row.status} label={row.status_label} /> },
              {
                key: "actions",
                title: "操作",
                render: (row) =>
                  row.status === "pending" ? (
                    <button className="ghost" onClick={() => complete(row.id)}><CheckCircle2 size={15} />完成</button>
                  ) : (
                    "-"
                  ),
              },
            ]}
          />
        </section>
      </section>
    </>
  );
}
