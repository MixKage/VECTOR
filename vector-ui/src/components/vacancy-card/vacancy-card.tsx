import { Calendar, Clock, User } from "lucide-react";
import { Button } from "./atoms";
import { Badge } from "./atoms";

interface VacancyCardProps {
  id: string;
  title: string;
  company: string;
  postedDate: string;
  daysLeft: number;
  applicants: number;
  hasNewApplicants: boolean;
  status: "active" | "expiring" | "archived";
}

export function VacancyCard({
  title,
  company,
  postedDate,
  daysLeft,
  applicants,
  hasNewApplicants,
  status,
}: VacancyCardProps) {
  const getStatusBadge = () => {
    if (status === "archived") {
      return (
        <Badge
          className="rounded-full px-3 py-1"
          style={{ backgroundColor: "#CECECE", color: "#4E4E50" }}
        >
          Архив
        </Badge>
      );
    }
    if (status === "expiring" || daysLeft < 7) {
      return (
        <Badge
          className="rounded-full px-3 py-1"
          style={{ backgroundColor: "#D00E46", color: "white" }}
        >
          Истекает
        </Badge>
      );
    }
    return (
      <Badge
        className="rounded-full px-3 py-1"
        style={{ backgroundColor: "#C49A6C", color: "white" }}
      >
        Активно
      </Badge>
    );
  };

  const getDaysLeftColor = () => {
    if (daysLeft > 21) return "#4E4E50";
    if (daysLeft >= 7) return "#C49A6C";
    return "#D00E46";
  };

  const getDaysLeftText = () => {
    return `Осталось: ${daysLeft} ${daysLeft === 1 ? "день" : daysLeft < 5 ? "дня" : "дней"}${daysLeft < 7 ? "!" : ""}`;
  };

  return (
    <div
      className="bg-white rounded-xl border border-[#CECECE] p-6 transition-all duration-200 hover:shadow-lg hover:border-[#C49A6C] cursor-pointer"
      style={{ boxShadow: "0px 2px 8px rgba(0, 0, 0, 0.08)" }}
    >
      <div className="flex items-start justify-between mb-4">
        {/* <div className="w-12 h-12 rounded-lg overflow-hidden bg-gray-100 flex-shrink-0">
          <ImageWithFallback
            src={logoUrl}
            alt={company}
            className="w-full h-full object-cover"
          />
        </div> */}
        {getStatusBadge()}
      </div>

      <h3 className="mb-1" style={{ color: "#393649" }}>
        {title}
      </h3>
      <p className="mb-4" style={{ color: "#4E4E50" }}>
        {company}
      </p>

      <div
        className="border-t border-dashed mb-4"
        style={{ borderColor: "#CECECE" }}
      />

      <div className="space-y-2 mb-4">
        <div className="flex items-center gap-2" style={{ color: "#4E4E50" }}>
          <Calendar className="w-4 h-4" />
          <span>Размещена: {postedDate}</span>
        </div>
        <div
          className="flex items-center gap-2"
          style={{
            color: getDaysLeftColor(),
            fontWeight: daysLeft < 7 ? 600 : 400,
          }}
        >
          <Clock className="w-4 h-4" />
          <span>{getDaysLeftText()}</span>
        </div>
      </div>

      <div
        className="border-t border-dashed mb-4"
        style={{ borderColor: "#CECECE" }}
      />

      <div className="flex items-center gap-2 mb-4">
        <User className="w-5 h-5" style={{ color: "#393649" }} />
        <span className="relative" style={{ color: "#393649" }}>
          {applicants}
          {hasNewApplicants && (
            <span
              className="absolute -top-1 -right-3 w-2 h-2 rounded-full"
              style={{ backgroundColor: "#D00E46" }}
            />
          )}
        </span>
        <span style={{ color: "#4E4E50" }}>
          {applicants === 1 ? "отклик" : applicants < 5 ? "отклика" : "откликов"}
        </span>
      </div>

      <div className="flex flex-col gap-2">
        <div className="flex gap-2">
          {daysLeft < 7 && status !== "archived" && (
            <Button
              variant="outline"
              className="flex-1 transition-all hover:text-white"
              style={{
                borderColor: "#D00E46",
                color: "#D00E46",
              }}
              onMouseEnter={(e: any) => {
                e.currentTarget.style.backgroundColor = "#D00E46";
                e.currentTarget.style.color = "white";
              }}
              onMouseLeave={(e: any) => {
                e.currentTarget.style.backgroundColor = "transparent";
                e.currentTarget.style.color = "#D00E46";
              }}
            >
              Продлить
            </Button>
          )}
          <Button
            variant="outline"
            className={`transition-all hover:text-white ${daysLeft >= 7 || status === "archived" ? "flex-1" : "flex-1"}`}
            style={{
              borderColor: "#4E4E50",
              color: "#4E4E50",
            }}
            onMouseEnter={(e: any) => {
              e.currentTarget.style.backgroundColor = "#4E4E50";
              e.currentTarget.style.color = "white";
            }}
            onMouseLeave={(e: any) => {
              e.currentTarget.style.backgroundColor = "transparent";
              e.currentTarget.style.color = "#4E4E50";
            }}
          >
            Скрыть
          </Button>
        </div>
        <button
          className="text-center transition-colors"
          style={{ color: "#393649" }}
          onMouseEnter={(e) => {
            e.currentTarget.style.color = "#D00E46";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.color = "#393649";
          }}
        >
          Управление
        </button>
      </div>
    </div>
  );
}
