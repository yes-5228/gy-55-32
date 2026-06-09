import { DoorOpen } from "lucide-react";
import React, { useState } from "react";

import { parcelsApi } from "../api/modules";
import MessageBox from "../components/MessageBox";
import PageHeader from "../components/PageHeader";

export default function PickupPage() {
  const [pickupCode, setPickupCode] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    setResult("");
    setError("");
    try {
      const data = await parcelsApi.open(pickupCode);
      setResult(`${data.message} 运单号 ${data.parcel.tracking_no} 已标记取件。`);
      setPickupCode("");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <PageHeader title="取件码开箱" description="输入用户取件码，系统校验后打开对应柜格并更新快件状态。" />
      <section className="pickup-panel">
        <form className="panel code-form" onSubmit={submit}>
          <label>
            取件码
            <input value={pickupCode} onChange={(event) => setPickupCode(event.target.value)} maxLength={12} required />
          </label>
          <button type="submit"><DoorOpen size={18} />开箱取件</button>
          <MessageBox type="success">{result}</MessageBox>
          <MessageBox type="error">{error}</MessageBox>
        </form>
      </section>
    </>
  );
}
