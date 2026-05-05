async function getData() {
  const res = await fetch("http://localhost:8000/api/v1/opportunities", { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export default async function Home() {
  const rows = await getData();
  return (
    <main style={{ padding: 24 }}>
      <h1>NZ Product Opportunity Scanner</h1>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            {[
              "Product",
              "Image",
              "Supplier URL",
              "Supplier Price",
              "Shipping",
              "Sell Price",
              "Gross Margin",
              "Demand",
              "Competition",
              "Risk",
              "Score",
              "AI Recommendation"
            ].map((h) => <th key={h} style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>{h}</th>)}
          </tr>
        </thead>
        <tbody>
          {rows.map((r: any) => (
            <tr key={r.id}>
              <td>{r.product_name}</td>
              <td><img src={r.image_url} alt={r.product_name} width="48" /></td>
              <td><a href={r.supplier_url} target="_blank">Link</a></td>
              <td>{r.supplier_price_nzd}</td>
              <td>{r.shipping_cost_nzd} / {r.shipping_days_estimate}d</td>
              <td>{r.estimated_sell_price_nzd}</td>
              <td>{r.estimated_gross_margin_nzd}</td>
              <td>{r.demand_score}</td>
              <td>{r.competition_score}</td>
              <td>{r.risk_score}</td>
              <td>{r.final_opportunity_score}</td>
              <td>{r.ai_recommendation}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <a href="http://localhost:8000/api/v1/opportunities/export">Export CSV</a>
    </main>
  );
}
