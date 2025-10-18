import { VacancyCard } from "@/components/vacancy-card/vacancy-card";
import { DefaultLayout } from "@/layouts/default";
import { useHr } from "./hooks";
import { Button } from "@/components/button";
import { Search, Plus, ChevronDown } from "lucide-react";
import { Input } from "@/components/input/input";
import { Select } from "@/components/select/select";

export default function HRPage() {
  
    const {
      filteredList,
      searchQuery,
      onChangeSearchQuery,
      statusFilter,
      onChangeStatusFilter,
    } = useHr()

    return (
    <DefaultLayout>
      <div className="max-w-7xl mx-auto">
        <h1 className="mb-8" style={{ color: "#393649", fontWeight: "bolder" }}>
          Мои вакансии
        </h1>
        <div className="bg-white rounded-xl border border-[#CECECE] p-6 mb-8" style={{ boxShadow: "0px 2px 8px rgba(0, 0, 0, 0.08)" }}>
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1 relative">
              <Search
                className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5"
                style={{ color: "#4E4E50" }}
              />
              <Input
                label="Поиск по вакансиям..."
                type="text"
                value={searchQuery}
                onChange={onChangeSearchQuery}
                className="pl-10 border-[#CECECE]"
                size="sm"
                labelPlacement="inside"
              />
            </div>
            <Select
              list={[
                {key: "all", label: "Все статусы"},
                {key: "active", label: "Активные"},
                {key: "expiring", label: "Истекающие"},
                {key: "archived", label: "Архив"},
              ]}
              value={statusFilter}
              onChange={onChangeStatusFilter}
              className="h-12"
            />
            <Button
              className="transition-all header-hr h-12"
              onClick={() => {
                window.location.href = 'https://technomoscow.ru/tech-work/anketa/';
              }}
            >
              <Plus className="w-5 h-5 mr-2" />
              Создать вакансию
            </Button>
          </div>
        </div>
      </div>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        {
            filteredList.map(value => 
                <VacancyCard
                    id={value.id}
                    title={value.name}
                    company={value.company}
                    postedDate={value.creationDate.toISOString()}
                    daysLeft={value.daysLeft}
                    applicants={value.candidatedCount}
                    hasNewApplicants={value.hasNew}
                    status={value.expiryDate > new Date() ? "active" : "archived"}
                />
            )
        }

      </section>
    </DefaultLayout>
  );
}

// export default function App() {

//   return (
//     <div className="min-h-screen bg-[#F5F5F5] p-6 md:p-8 lg:p-12">
//       <div className="max-w-7xl mx-auto">
//         {/* Header */}
//         <h1 className="mb-8" style={{ color: "#393649" }}>
//           Мои вакансии
//         </h1>

//         {/* Control Panel */}
//         <div className="bg-white rounded-xl border border-[#CECECE] p-6 mb-8" style={{ boxShadow: "0px 2px 8px rgba(0, 0, 0, 0.08)" }}>
//           <div className="flex flex-col lg:flex-row gap-4">
//             {/* Search */}
//             <div className="flex-1 relative">
//               <Search
//                 className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5"
//                 style={{ color: "#4E4E50" }}
//               />
//               <Input
//                 type="text"
//                 placeholder="Поиск по вакансиям..."
//                 value={searchQuery}
//                 onChange={(e) => setSearchQuery(e.target.value)}
//                 className="pl-10 border-[#CECECE]"
//                 style={{ color: "#393649" }}
//               />
//             </div>

//             {/* Status Filter */}
//             <Select value={statusFilter} onValueChange={setStatusFilter}>
//               <SelectTrigger className="w-full lg:w-48 border-[#CECECE]">
//                 <SelectValue placeholder="Все статусы" />
//               </SelectTrigger>
//               <SelectContent>
//                 <SelectItem value="all">Все статусы</SelectItem>
//                 <SelectItem value="active">Активные</SelectItem>
//                 <SelectItem value="expiring">Истекающие</SelectItem>
//                 <SelectItem value="archived">Архив</SelectItem>
//               </SelectContent>
//             </Select>

//             {/* Sort Filter */}
//             <Select value={sortBy} onValueChange={setSortBy}>
//               <SelectTrigger className="w-full lg:w-48 border-[#CECECE]">
//                 <SelectValue placeholder="Сортировка" />
//               </SelectTrigger>
//               <SelectContent>
//                 <SelectItem value="date">По дате</SelectItem>
//                 <SelectItem value="applicants">По откликам</SelectItem>
//                 <SelectItem value="expiring">По сроку</SelectItem>
//               </SelectContent>
//             </Select>

//             {/* Create Button */}
//             <Button
//               className="transition-all"
//               style={{
//                 backgroundColor: "#D00E46",
//                 color: "white",
//               }}
//               onMouseEnter={(e) => {
//                 e.currentTarget.style.backgroundColor = "#740827";
//               }}
//               onMouseLeave={(e) => {
//                 e.currentTarget.style.backgroundColor = "#D00E46";
//               }}
//             >
//               <Plus className="w-5 h-5 mr-2" />
//               Создать вакансию
//             </Button>
//           </div>
//         </div>

//         {/* Vacancies Grid */}
//         {filteredVacancies.length > 0 ? (
//           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
//             {filteredVacancies.map((vacancy) => (
//               <VacancyCard key={vacancy.id} {...vacancy} />
//             ))}
//           </div>
//         ) : (
//           <div className="flex flex-col items-center justify-center py-20">
//             <div
//               className="w-24 h-24 rounded-full flex items-center justify-center mb-6"
//               style={{ backgroundColor: "#CECECE" }}
//             >
//               <Search className="w-12 h-12" style={{ color: "#4E4E50" }} />
//             </div>
//             <h2 className="mb-2" style={{ color: "#393649" }}>
//               Вакансии не найдены
//             </h2>
//             <p className="mb-6" style={{ color: "#4E4E50" }}>
//               Попробуйте изменить параметры поиска
//             </p>
//             <Button
//               className="transition-all"
//               style={{
//                 backgroundColor: "#D00E46",
//                 color: "white",
//               }}
//               onMouseEnter={(e) => {
//                 e.currentTarget.style.backgroundColor = "#740827";
//               }}
//               onMouseLeave={(e) => {
//                 e.currentTarget.style.backgroundColor = "#D00E46";
//               }}
//             >
//               <Plus className="w-5 h-5 mr-2" />
//               Создать первую вакансию
//             </Button>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }
