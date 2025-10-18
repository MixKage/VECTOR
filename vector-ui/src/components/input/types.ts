import { ChangeEventHandler } from "react";

export interface IInput {
    isRequired?: boolean;
    className?: string;
    defaultValue?: string;
    label: string;
    type?: string;
    value: string;
    onChange: ChangeEventHandler;
    size?: "md" | "sm" | "lg" | undefined;
    labelPlacement?: "inside" | "outside" | "outside-left" | "outside-top";
}