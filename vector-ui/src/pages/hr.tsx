import { VacancyCard } from "@/components/vacancy-card/vacancy-card";
import { DefaultLayout } from "@/layouts/default";

export default function HRPage() {
  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <VacancyCard
            id={"1"}
            title={"efeff"}
            company="fefwefwe"
            postedDate="2024-12-13"
            daysLeft={3}
            applicants={3}
            hasNewApplicants
            status="active"
        />
      </section>
    </DefaultLayout>
  );
}