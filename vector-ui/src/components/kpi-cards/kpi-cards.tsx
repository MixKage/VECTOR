import axios from "axios";
import { FC, useEffect, useState } from 'react';
import { IKPICard } from './types';

export const KPICard:FC<IKPICard> = (props) => {
    return (
        <div className="bg-white border border-[#CECECE] rounded-xl p-6 shadow-sm">
        <div className="space-y-2">
            <p className="text-[#4E4E50]">{props.title}</p>
            <div className="flex items-baseline gap-3">
            <span className="text-[#393649]">{props.value}</span>
            </div>
        </div>
        </div>
    );
}

export const KPICards = () => {

  const [kpis, setList] = useState<Array<IKPICard>>([])
  useEffect(() => {
    axios.get("http://localhost:8000/metrics/summary")
                .then(
                    (response: any) => {
                        console.log(response)
                          const kpisData = [
                                {
                                    title: 'Всего вакансий',
                                    value: response.data.total_vacancies,
                                },
                                {
                                    title: 'Активные вакансии',
                                    value: response.data.active_vacancies,
                                },
                                {
                                    title: 'Всего откликов',
                                    value: response.data.total_applications,
                                },
                                {
                                    title: 'Уровень трудоустройства',
                                    value: response.data.employment_rate
                                }
                            ];
                        setList(kpisData)
                });
  }, [])

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {kpis.map((kpi, index) => (
        <KPICard key={index} {...kpi} />
      ))}
    </div>
  );

}