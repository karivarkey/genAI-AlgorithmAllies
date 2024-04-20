import React from "react";

const InventoryList = ({ contents, availableQuantity, expiryDate }) => {
  return (
    <div className="inventory-list grid grid-cols-5 gap-4 py-4">
      {contents.map((content, index) => (
        <div
          key={index}
          className="card bg-white rounded-md shadow-md p-4 hover:scale-x-105 hover:scale-y-105"
        >
          <span className="text-xl font-medium">{content}</span>
          <br />
          <span className="text-l text-gray-500">
            quantity: {availableQuantity[index]}
          </span>
          <br />
          {expiryDate && ( // Only display expiry date if provided
            <span className="text-m text-gray-500">
              Expires: {new Date(expiryDate[index]).toLocaleDateString()}
            </span>
          )}
        </div>
      ))}
    </div>
  );
};

export default InventoryList;
