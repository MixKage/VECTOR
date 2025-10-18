import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react"
import { ICardData } from "@/components/vacancy-card/types";
import { prepareDataForCards } from "@/components/vacancy-card/utils";
import axios from "axios";

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
        axios.get("http://localhost:8000/vacancies/")
            .then(
                (response: any) => {
                    const prepareData = prepareDataForCards(response.data.vacancies)
                    setList(prepareData)
                    setFilteredList(prepareData)
                })
            .catch((error: any) => console.error(error));
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