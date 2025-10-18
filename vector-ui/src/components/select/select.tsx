import { FC } from "react"
import { Select as HeroSelect, SelectItem} from "@heroui/select";
import { ISelect } from "./types"

export const Select:FC<ISelect> = (props) => {

    const {
        list,
        className = "",
        onChange,
    } = props

    return (
        <HeroSelect 
            className={`max-w-xs ${className}`}
            onChange={onChange}
            defaultSelectedKeys="all"
        >
            {
                list.map((list) => (
                    <SelectItem key={list.key}>{list.label}</SelectItem>
                ))
            }
        </HeroSelect>
    )
}