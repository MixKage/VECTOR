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
    const [filteredList, setFilteredList] = useState<Array<ICardData>>([])
    const [searchQuery, setSearchQuery] = useState("");
    const [statusFilter, setStatusFilter] = useState("all");
    
    useEffect(() => {
        const filteredVacancies = list.filter((vacancy) => {
            const matchesSearch =
            vacancy.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            vacancy.company.toLowerCase().includes(searchQuery.toLowerCase());

            const matchesStatus =
            statusFilter === "all" ||
            (statusFilter === "active" && (vacancy.daysLeft >= 7) && (vacancy.expiryDate >= new Date())) ||
            (statusFilter === "expiring" && vacancy.daysLeft < 7) ||
            (statusFilter === "archived" && vacancy.expiryDate < new Date());

            return matchesSearch && matchesStatus;
        });
        setFilteredList(filteredVacancies)
    }, [searchQuery, statusFilter])

    useEffect(() => {
        const prepareData = prepareDataForCards([{ id: 1, name: "fefef", creation_date: "2025-12-12", expiry_date: "2025-12-13", daysLeft: 2,
    specialization: "efwfwefefefwe",
    candidates: [{id: 1, is_new: true}], company: "fwefwef"}])
        setList(prepareData)
        setFilteredList(prepareData)
    }, [])

    const onChangeSearchQuery = (e: any) => {
        setSearchQuery(e.target.value)
    }

    const onChangeStatusFilter = (e: any) => {
        setStatusFilter(e.target.value)
    }

    return {
        filteredList,
        searchQuery,
        onChangeSearchQuery,
        statusFilter,
        onChangeStatusFilter
    }
}