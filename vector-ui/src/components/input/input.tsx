import { Input as HeroInput } from "@heroui/input";
import { FC } from "react";
import { IInput } from "./types";
import "./styles.css";

export const Input:FC<IInput> = (props) => {
    
    const {
        isRequired = false,
        className = "",
        defaultValue = "",
        label,
        type,
        value,
        onChange,
        size="md",
        labelPlacement="inside"
    } = props

    return (
        <HeroInput
            className={`custom-input ${className}`}
            isRequired={isRequired}
            defaultValue={defaultValue}
            label={label}
            type={type}
            value={value}
            color="danger"
            variant='bordered'
            onChange={onChange}
            size={size}
            labelPlacement={labelPlacement}
        />
    )
}