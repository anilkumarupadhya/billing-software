import React, { useState } from "react";

const Customers: React.FC = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    altPhone: "",
    dob: "",
    gender: "",
    gstNo: "",
    company: "",
    panNo: "",
    businessType: "",
    shippingAddress: "",
    billingAddress: "",
    city: "",
    state: "",
    pinCode: "",
    country: "India",
    eway: "",
    paymentMethod: "",
    notes: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    console.log("Customer Data Submitted:", formData);

    // Reset form after save
    setFormData({
      name: "",
      email: "",
      phone: "",
      altPhone: "",
      dob: "",
      gender: "",
      gstNo: "",
      company: "",
      panNo: "",
      businessType: "",
      shippingAddress: "",
      billingAddress: "",
      city: "",
      state: "",
      pinCode: "",
      country: "India",
      eway: "",
      paymentMethod: "",
      notes: "",
    });
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-center p-8"
      style={{
        backgroundImage: "url('/images/austin-distel-744oGeqpxPQ-unsplash.jpg')",
      }}
    >
      <div className="bg-white bg-opacity-90 rounded-2xl shadow-2xl max-w-6xl w-full p-10">
        <h1 className="text-3xl font-bold text-center mb-8">Customer Registration</h1>

        <form onSubmit={handleSubmit} className="space-y-8">

          {/* SECTION 1: Personal Information */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
            <div className="grid grid-cols-2 gap-6">
              {/* Left Column */}
              <div className="space-y-4">
                <div>
                  <label className="block font-medium mb-1">Name *</label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2"
                    placeholder="Enter customer name"
                    required
                  />
                </div>
                <div>
                  <label className="block font-medium mb-1">Email</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2"
                    placeholder="Enter email"
                  />
                </div>
                <div>
                  <label className="block font-medium mb-1">Phone *</label>
                  <input
                    type="text"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2"
                    placeholder="Enter phone number"
                    required
                  />
                </div>
                <div>
                  <label className="block font-medium mb-1">Alternate Phone</label>
                  <input
                    type="text"
                    name="altPhone"
                    value={formData.altPhone}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2"
                    placeholder="Enter alternate phone number"
                  />
                </div>
              </div>

              {/* Right Column */}
              <div className="space-y-4">
                <div>
                  <label className="block font-medium mb-1">Date of Birth</label>
                  <input
                    type="date"
                    name="dob"
                    value={formData.dob}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2"
                  />
                </div>
                <div>
                  <label className="block font-medium mb-1">Gender</label>
                  <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2"
                  >
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div>
                  <label className="block font-medium mb-1">GST No</label>
                  <input
                    type="text"
                    name="gstNo"
                    value={formData.gstNo}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2"
                    placeholder="Enter GST number"
                  />
                </div>
                <div>
                  <label className="block font-medium mb-1">PAN No</label>
                  <input
                    type="text"
                    name="panNo"
                    value={formData.panNo}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2"
                    placeholder="Enter PAN number"
                  />
                </div>
                <div>
                  <label className="block font-medium mb-1">Company</label>
                  <input
                    type="text"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2"
                    placeholder="Enter company name"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* SECTION 2: Addresses */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Addresses</h2>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block font-medium mb-1">Shipping Address *</label>
                <textarea
                  name="shippingAddress"
                  value={formData.shippingAddress}
                  onChange={handleChange}
                  className="w-full border rounded-lg p-2"
                  rows={4}
                  placeholder="Enter shipping address"
                  required
                ></textarea>
              </div>
              <div>
                <label className="block font-medium mb-1">Billing Address</label>
                <textarea
                  name="billingAddress"
                  value={formData.billingAddress}
                  onChange={handleChange}
                  className="w-full border rounded-lg p-2"
                  rows={4}
                  placeholder="Enter billing address"
                ></textarea>
              </div>
            </div>
          </div>

          {/* SECTION 3: Location */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Location</h2>
            <div className="grid grid-cols-3 gap-6">
              <div>
                <label className="block font-medium mb-1">City</label>
                <input
                  type="text"
                  name="city"
                  value={formData.city}
                  onChange={handleChange}
                  className="w-full border rounded-lg p-2"
                  placeholder="Enter city"
                />
              </div>
              <div>
                <label className="block font-medium mb-1">State</label>
                <input
                  type="text"
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  className="w-full border rounded-lg p-2"
                  placeholder="Enter state"
                />
              </div>
              <div>
                <label className="block font-medium mb-1">Pin Code</label>
                <input
                  type="text"
                  name="pinCode"
                  value={formData.pinCode}
                  onChange={handleChange}
                  className="w-full border rounded-lg p-2"
                  placeholder="Enter pin code"
                />
              </div>
            </div>
          </div>

          {/* SECTION 4: Other Information */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Other Information</h2>
            <div className="space-y-4">
              <div>
                <label className="block font-medium mb-1">Country</label>
                <input
                  type="text"
                  name="country"
                  value={formData.country}
                  readOnly
                  className="w-full border rounded-lg p-2 bg-gray-100"
                />
              </div>
              <div>
                <label className="block font-medium mb-1">E-Way</label>
                <input
                  type="text"
                  name="eway"
                  value={formData.eway}
                  onChange={handleChange}
                  className="w-full border rounded-lg p-2"
                  placeholder="Enter E-Way details"
                />
              </div>
              <div>
                <label className="block font-medium mb-1">Payment Method</label>
                <select
                  name="paymentMethod"
                  value={formData.paymentMethod}
                  onChange={handleChange}
                  className="w-full border rounded-lg p-2"
                >
                  <option value="">Select Payment Method</option>
                  <option value="Cash">Cash</option>
                  <option value="Card">Card</option>
                  <option value="UPI">UPI</option>
                  <option value="Bank Transfer">Bank Transfer</option>
                </select>
              </div>
              <div>
                <label className="block font-medium mb-1">Notes</label>
                <textarea
                  name="notes"
                  value={formData.notes}
                  onChange={handleChange}
                  className="w-full border rounded-lg p-2"
                  rows={3}
                  placeholder="Additional notes about the customer"
                ></textarea>
              </div>
            </div>
          </div>

          {/* Save Button */}
          <div className="text-center">
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg shadow-lg transition-all"
            >
              Save Customer
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Customers;

