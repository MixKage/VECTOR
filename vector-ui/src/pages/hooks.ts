import { useNavigate } from "react-router-dom";

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