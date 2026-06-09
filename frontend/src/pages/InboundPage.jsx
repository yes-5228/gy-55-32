import { PackagePlus, RefreshCw } from "lucide-react";
import React, { useEffect, useState } from "react";

import { parcelsApi } from "../api/modules";
import DataTable from "../components/DataTable";
import MessageBox from "../components/MessageBox";
import PageHeader from "../components/PageHeader";
import StatusBadge from "../components/StatusBadge";

const initialForm = {
  tracking_no: "",
  sender_name: "",
  receiver_name: "",
  receiver_phone: "",
  carrier: "顺丰",
  size: "medium",
  note: "",
};

export default function InboundPage() {
  const [form, setForm] = useState(initialForm);
  const [parcels, setParcels] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadParcels = () => parcelsApi.list().then(setParcels);

  useEffect(() => {
    loadParcels();
  }, []);

  const updateField = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const submit = async (event) => {
    event.preventDefault();
    setMessage("");
    setError("");
    try {
      const created = await parcelsApi.inbound(form);
      setMessage(`入库成功，柜格 ${created.locker_cell_detail.code}，取件码 ${created.pickup_code}。`);
      setForm(initialForm);
      loadParcels();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <PageHeader title="快件入库" description="登记快件后自动分配空柜格，并生成取件码与通知记录。" />
      <section className="work-grid">
        <form className="panel form-panel" onSubmit={submit}>
          <h2>入库登记</h2>
          <label>运单号<input name="tracking_no" value={form.tracking_no} onChange={updateField} required /></label>
          <label>寄件方<input name="sender_name" value={form.sender_name} onChange={updateField} required /></label>
          <label>收件人<input name="receiver_name" value={form.receiver_name} onChange={updateField} required /></label>
          <label>手机号<input name="receiver_phone" value={form.receiver_phone} onChange={updateField} required /></label>
          <label>承运商<input name="carrier" value={form.carrier} onChange={updateField} required /></label>
          <label>
            柜格尺寸
            <select name="size" value={form.size} onChange={updateField}>
              <option value="small">小</option>
              <option value="medium">中</option>
              <option value="large">大</option>
            </select>
          </label>
          <label>备注<input name="note" value={form.note} onChange={updateField} /></label>
          <button type="submit"><PackagePlus size={18} />确认入库</button>
          <MessageBox type="success">{message}</MessageBox>
          <MessageBox type="error">{error}</MessageBox>
        </form>
        <section className="panel">
          <div className="panel-title">
            <h2>快件列表</h2>
            <button className="ghost" onClick={loadParcels}><RefreshCw size={16} />刷新</button>
          </div>
          <DataTable
            rows={parcels}
            columns={[
              { key: "tracking_no", title: "运单号" },
              { key: "receiver_name", title: "收件人" },
              { key: "cell", title: "柜格", render: (row) => row.locker_cell_detail?.code },
              { key: "pickup_code", title: "取件码" },
              { key: "status", title: "状态", render: (row) => <StatusBadge status={row.status} label={row.status_label} /> },
            ]}
          />
        </section>
      </section>
    </>
  );
}
