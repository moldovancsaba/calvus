
import React, { createContext, useContext, useEffect, useState } from "react";

export type Identity = {
  gametag: string;
  color: string;
};

type IdentityContextType = {
  identity: Identity | null;
  setIdentity: (identity: Identity) => void;
};

const IdentityContext = createContext<IdentityContextType | undefined>(
  undefined
);

export const useIdentity = () => {
  const ctx = useContext(IdentityContext);
  if (!ctx) throw new Error("useIdentity must be used within Provider");
  return ctx;
};

export const IdentityProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [identity, setIdentityState] = useState<Identity | null>(null);

  useEffect(() => {
    const raw = window.localStorage.getItem("identity");
    if (raw) setIdentityState(JSON.parse(raw));
  }, []);

  const setIdentity = (id: Identity) => {
    setIdentityState(id);
    window.localStorage.setItem("identity", JSON.stringify(id));
  };

  return (
    <IdentityContext.Provider value={{ identity, setIdentity }}>
      {children}
    </IdentityContext.Provider>
  );
};
