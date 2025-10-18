import { DefaultLayout } from "@/layouts/default";
import LogoSvg from '../images/logo.svg';
import "./styles.css";
import { Input } from "@/components/input/input";
import {Children, useState} from "react";
import { Button } from "@/components/button";

export default function UniversityPage() {

  const[universityName, setName] = useState('');
  const[code, setCode] = useState('');
  const[course, setCourse] = useState('');
  const[quantity, setQuantity] = useState('');
  const[dateStart, setDateStart] = useState('');
  const[dateEnd, setDateEnd] = useState('');

  return (
    <DefaultLayout>
      <section>
        <img 
          src={LogoSvg} 
          alt="Логотип компании" 
          className="logo-svg"
        />
      </section>
      <section className="flex flex-col items-left justify-center gap-4 py-8 md:py-10">
        <Input
          label="ВУЗ/Техникум" 
          value={universityName}
          onChange={e => setName((e.target as HTMLInputElement).value)}
        />
        <Input
          label="Код направления обучения"
          value={code}
          onChange={e => setCode((e.target as HTMLInputElement).value)}
        />
        <Input
          label="Курс"
          value={course}
          onChange={e => setCourse((e.target as HTMLInputElement).value)}
        />
        <Input
          label="Количество студентов"
          value={quantity}
          onChange={e => setQuantity((e.target as HTMLInputElement).value)}
        />
        <Input
          label="Дата начала прохождения практики"
          value={dateStart}
          onChange={e => setDateStart((e.target as HTMLInputElement).value)}
        />
        <Input
          label="Дата конца прохождения практики"
          value={dateEnd}
          onChange={e => setDateEnd((e.target as HTMLInputElement).value)}
        />
        <Button
          onClick={() => {return}}
          children="Отправить"
        />
      </section>
    </DefaultLayout>
  );
}