import { VacancyCard } from "@/components/vacancy-card/vacancy-card";
import { DefaultLayout } from "@/layouts/default";
import { useHr } from "./hooks";

export default function HRPage() {
  
    const {
        list,
    } = useHr()

    return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        {
            list.map(value => 
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