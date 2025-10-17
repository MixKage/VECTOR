import BackgroundSvg from '../../images/background.svg';
import LogoSvg from '../images/logo.svg';
import { Button } from "@heroui/button";
import DefaultLayout from "@/layouts/default";

export default function IndexPage() {
  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <img 
          src={LogoSvg} 
          alt="Логотип компании" 
          className="w-32 h-auto"
        />
        <Button>Модератор ОЭЗ</Button>
        <Button>Представитель HR</Button>
        <Button>Университет</Button>
        <Button>Соискатель</Button>
      </section>
    </DefaultLayout>
  );
}
