import { Button as HeroButton } from "@heroui/button";
import { FC } from "react";
import { IButton } from "./types";
import "./styles.css";

export const Button:FC<IButton> = (props) => {
    return (
        <HeroButton 
            onPress={props.onClick}
            className="button"
        >
            {props.children}
        </HeroButton>
    )
}