// src/components/Toast.tsx
import React, { useEffect, useState } from "react";

interface ToastProps {
  message: string | null; // Message can be null when not visible
}

export const Toast: React.FC<ToastProps> = ({ message }) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (message) {
      setVisible(true);
      const timer = setTimeout(() => {
        setVisible(false);
      }, 3000); // Hide the toast after 3 seconds

      return () => {
        clearTimeout(timer);
      };
    }
  }, [message]);

  if (!visible) return null;

  return (
    <div className="fixed bottom-4 right-4 bg-transparent border border-white rounded-corners shadow-md p-4"> {/* Updated to use rounded-lg */}
      <span className="text-white">{message}</span>
    </div>
  );
};
