import { DefaultLayout } from "@/layouts/default";
import LogoSvg from "../images/logo.svg";
import "./styles.css";
import { Input } from "@/components/input/input";
import { useState } from "react";
import { Button } from "@/components/button";
import axios from "axios";

export default function UniversityPage() {
  const [universityName, setName] = useState("");
  const [code, setCode] = useState("");
  const [course, setCourse] = useState("");
  const [quantity, setQuantity] = useState("");
  const [dateStart, setDateStart] = useState("");
  const [dateEnd, setDateEnd] = useState("");

  const onClick = () => {
    axios.post("http://localhost:8000/university", {
      "university_name": universityName,
      "direction_of_study_code": code,
      "start_date": (new Date(dateStart)).toISOString(),
      "end_time": (new Date(dateEnd)).toISOString(),
      "count": quantity
    })
    setName("")
    setCode("")
    setCourse("")
    setQuantity("")
    setDateStart("")
    setDateEnd("")
  }


  return (
    <DefaultLayout>
      <section>
        <img src={LogoSvg} alt="Логотип" className="logo-svg" />
      </section>
      <section className="flex flex-col items-left justify-center gap-4 py-8 md:py-10">
        <Input
          label="Вуз/техникум"
          value={universityName}
          onChange={(e) => setName((e.target as HTMLInputElement).value)}
        />
        <Input
          label="Код направления"
          value={code}
          onChange={(e) => setCode((e.target as HTMLInputElement).value)}
        />
        <Input
          label="Курс"
          value={course}
          onChange={(e) => setCourse((e.target as HTMLInputElement).value)}
        />
        <Input
          label="Количество мест"
          value={quantity}
          onChange={(e) => setQuantity((e.target as HTMLInputElement).value)}
        />
        <Input
          label="Дата начала"
          value={dateStart}
          onChange={(e) => setDateStart((e.target as HTMLInputElement).value)}
        />
        <Input
          label="Дата окончания"
          value={dateEnd}
          onChange={(e) => setDateEnd((e.target as HTMLInputElement).value)}
        />
        <Button
          className="w-15" 
          onClick={onClick}>
          Сохранить
        </Button>
      </section>
    </DefaultLayout>
  );
}
