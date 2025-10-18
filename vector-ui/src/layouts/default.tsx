import { FC } from "react";
import "./styles.css"
import { IDefaultLayout } from "./types";

export const DefaultLayout:FC<IDefaultLayout> = ({ className = "", children}) => {
  return (
    <div className={`min-h-screen flex flex-col layout ${className}`}>
      <main className="flex-1">
        <div className="container mx-auto p-4">
          <div className="content">
            {children}
          </div>
        </div>
      </main>
      <footer className="mt-auto">
        <div className="mb-[30px] mr-8 text-right">
          <p>© 2025 ВЕКТОР. Все права защищены. </p>
        </div>
      </footer>
    </div>
  );
}