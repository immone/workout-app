import React from 'react';

export const Typography: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className }) => {
  return (
    <p className={`text-white ${className}`}>
      {children}
    </p>
  );
};
