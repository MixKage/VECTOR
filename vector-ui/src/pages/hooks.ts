import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react"
import { ICardData } from "@/components/vacancy-card/types";
import { prepareDataForCards } from "@/components/vacancy-card/utils";

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
        setList(prepareDataForCards([{ id: 1, name: "fefef", creation_date: "2025-12-12", expiry_date: "2025-12-13", daysLeft: 2,
    specialization: "efwfwefefefwe",
    candidates: [{id: 1, is_new: true}], company: "fwefwef"}]))
    }, [])
    
    return {
        list,
    }
}