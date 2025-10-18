import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import axios from "axios";
import { useEffect, useState } from 'react';

export function TopSpecialties() {
  
  const [data, setData] = useState()

  useEffect(() => {
    axios.get("http://localhost:8000/metrics/summary")
      .then(
          (response: any) => {
              const rawData = response.data.top_specializations.map((spec: any) => {
                return (
                  { 
                    name: spec.specialization, 
                    count: spec.applications 
                  }
                )
              })
              setData(rawData)
      });
    }, [])

  return (
    <div className="bg-white border border-[#CECECE] rounded-xl p-6 shadow-sm">
      <h3 className="text-[#393649] mb-4">Топ-10 востребованных специальностей</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="#F5F5F5" />
          <XAxis 
            type="number"
            tick={{ fill: '#4E4E50', fontSize: 13 }}
          />
          <YAxis 
            type="category"
            dataKey="name" 
            tick={{ fill: '#4E4E50', fontSize: 13 }}
            width={150}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'white', 
              border: '1px solid #CECECE',
              borderRadius: '8px'
            }}
            cursor={{ fill: '#F5F5F5' }}
          />
          <Bar 
            dataKey="count" 
            fill="#393649"
            radius={[0, 4, 4, 0]}
            name="Количество вакансий"
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
