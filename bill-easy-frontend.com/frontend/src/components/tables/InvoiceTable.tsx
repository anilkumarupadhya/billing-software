import React from "react";

interface Invoice {
  id: number;
  customer: string;
  total: number;
  status: string;
  issuedDate: string;
}

interface Props {
  invoices?: Invoice[];
}

const InvoiceTable: React.FC<Props> = ({ invoices = [] }) => {
  return (
    <table className="min-w-full bg-white shadow-md rounded-md overflow-hidden">
      <thead className="bg-gray-200">
        <tr>
          <th className="p-2 text-left">ID</th>
          <th className="p-2 text-left">Customer</th>
          <th className="p-2 text-left">Total</th>
          <th className="p-2 text-left">Status</th>
          <th className="p-2 text-left">Issued Date</th>
        </tr>
      </thead>
      <tbody>
        {invoices.map((inv) => (
          <tr key={inv.id} className="border-t">
            <td className="p-2">{inv.id}</td>
            <td className="p-2">{inv.customer}</td>
            <td className="p-2">${inv.total}</td>
            <td className="p-2">{inv.status}</td>
            <td className="p-2">{inv.issuedDate}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default InvoiceTable;

