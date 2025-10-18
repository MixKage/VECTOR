import { useEffect, useState } from "react";
import { ROLE_OPTIONS } from "../api";

export default function RoleModal({
  visible,
  multiple = false,
  initialSelected = [],
  title,
  description,
  onCancel,
  onSubmit,
}) {
  const [localSelection, setLocalSelection] = useState(new Set(initialSelected));

  useEffect(() => {
    setLocalSelection(new Set(initialSelected));
  }, [initialSelected]);

  if (!visible) {
    return null;
  }

  const toggle = (code) => {
    setLocalSelection((prev) => {
      const next = new Set(prev);
      if (multiple) {
        if (next.has(code)) {
          next.delete(code);
        } else {
          next.add(code);
        }
      } else {
        next.clear();
        next.add(code);
      }
      return next;
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(Array.from(localSelection));
  };

  return (
    <div className="modal-backdrop" role="dialog" aria-modal="true">
      <div className="modal">
        <h3>{title}</h3>
        {description && <p className="modal-description">{description}</p>}
        <form className="modal-form" onSubmit={handleSubmit}>
          <div className="modal-options">
            {ROLE_OPTIONS.map((role) => {
              const checked = localSelection.has(role.code);
              return (
                <label key={role.code} className="modal-option">
                  <input
                    type={multiple ? "checkbox" : "radio"}
                    name="role"
                    value={role.code}
                    checked={checked}
                    onChange={() => toggle(role.code)}
                  />
                  <span>{role.label}</span>
                </label>
              );
            })}
          </div>
          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={onCancel}>
              Отмена
            </button>
            <button type="submit" className="btn-primary" disabled={localSelection.size === 0}>
              Подтвердить
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
