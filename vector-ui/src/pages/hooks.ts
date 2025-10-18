import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react"
import { ICardData } from "@/components/vacancy-card/types";

export const useIndexPage = () => {
    const navigate = useNavigate();

    const handleClickModerator = () => {
        navigate('/moderator'); // Переход на страницу about
    };

    const handleClickHr = () => {
        navigate('/hr'); // Переход на страницу about
    };

    const handleClickCandidate = () => {
        navigate('/candidate'); // Переход на страницу about
    };

    const handleClickUniversity = () => {
        navigate('/university'); // Переход на страницу about
    };

    return {
        handleClickModerator,
        handleClickHr,
        handleClickCandidate,
        handleClickUniversity,
    }
}

export const useHr = () => {
    
    const [list, setList] = useState<Array<ICardData>>([])

    useEffect(() => {

    }, [])
    
    return {
        list,
    }
}