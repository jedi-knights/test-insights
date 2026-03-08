"use client";

import { useAuth } from "@/lib/auth/hooks";

interface HeaderProps {
  title: string;
}

export function Header({ title }: HeaderProps) {
  const { user } = useAuth();
  return (
    <header className="flex h-14 items-center justify-between border-b px-6">
      <h1 className="text-lg font-semibold">{title}</h1>
      {user && (
        <span className="text-sm text-muted-foreground">{user.email}</span>
      )}
    </header>
  );
}
