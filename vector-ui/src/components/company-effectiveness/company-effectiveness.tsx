import { useEffect, useState } from 'react';
import axios from "axios";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../table/table';
import { ICompany } from './types';

export function CompanyEffectiveness() {
    const [companies, setCompanies] = useState<Array<ICompany>>([])
    useEffect(() => {
        axios.get("http://localhost:8000/metrics/summary")
                    .then(
                        (response: any) => {
                            const rawData = response.data.top_companies.map((comp: any) => {
                                return (
                                { 
                                    name: comp.company, 
                                    vacancies: comp.vacancies,
                                    responses: comp.total_applications,
                                    employed: comp.approved_applications
                                }
                                )
                            })
                            setCompanies(rawData)
                    });
    }, [])

  return (
    <div className="bg-white border border-[#CECECE] rounded-xl p-6 shadow-sm">
      <h3 className="text-[#393649] mb-4">Эффективность трудоустройства по компаниям</h3>
      <Table>
        <TableHeader>
          <TableRow className="border-[#CECECE]">
            <TableHead className="text-[#4E4E50]">Компания</TableHead>
            <TableHead className="text-[#4E4E50] text-right">Вакансий</TableHead>
            <TableHead className="text-[#4E4E50] text-right">Откликов</TableHead>
            <TableHead className="text-[#4E4E50] text-right">Трудоустроено</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {companies.map((company, index) => (
            <TableRow 
              key={index} 
              className="border-[#CECECE] hover:bg-[#F5F5F5] cursor-pointer transition-colors"
            >
              <TableCell className="text-[#393649]">{company.name}</TableCell>
              <TableCell className="text-[#4E4E50] text-right">{company.vacancies}</TableCell>
              <TableCell className="text-[#4E4E50] text-right">{company.responses}</TableCell>
              <TableCell className="text-[#4E4E50] text-right">{company.employed}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}