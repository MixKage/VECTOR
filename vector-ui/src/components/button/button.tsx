import { Button as HeroButton } from "@heroui/button";
import { FC } from "react";
import { IButton } from "./types";
import "./styles.css";

export const Button:FC<IButton> = (props) => {
    
    const {
        className = "",
    } = props

    return (
        <HeroButton 
            onPress={props.onClick}
            className={`button ${className}`}
        >
            {props.children}
        </HeroButton>
    )
}