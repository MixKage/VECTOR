import { CompanyEffectiveness } from "@/components/company-effectiveness/company-effectiveness";
import { KPICards } from "@/components/kpi-cards/kpi-cards";
import { TopSpecialties } from "@/components/top-specialities/top-specialities";
import { DefaultLayout } from "@/layouts/default";

export default function ModeratorPage() {
  return (
    <DefaultLayout>
      <div className="min-h-screen bg-[#F5F5F5] p-6">
        <div className="max-w-[1600px] mx-auto">
          <h1 className="text-[#393649] mb-6">
            Статистика платформы трудоустройства ОЭЗ
          </h1>
          <KPICards />
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <TopSpecialties />
              <CompanyEffectiveness />
            </div>
          </div>
        </div>
      </div>
    </DefaultLayout>
  );
}