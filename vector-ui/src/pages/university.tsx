import { DefaultLayout } from "@/layouts/default";
import LogoSvg from '../images/logo.svg';
import "./styles.css";
import { Input } from "@/components/input/input";


export default function UniversityPage() {
  return (
    <DefaultLayout>
      <section>
        <img 
          src={LogoSvg} 
          alt="Логотип компании" 
          className="logo-svg"
        />
      </section>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <Input
           label="ВУЗ/Техникум" 
           value="efef"
        />
      </section>
    </DefaultLayout>
  );
}