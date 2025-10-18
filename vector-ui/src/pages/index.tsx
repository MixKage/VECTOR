import LogoSvg from '../images/logo.svg';
import { Button } from "../components/button";
import { DefaultLayout } from "@/layouts/default";
import "./styles.css";
import { useIndexPage } from './hooks';

export default function IndexPage() {

  const {
    handleClickModerator,
    handleClickHr,
    handleClickCandidate,
    handleClickUniversity,
  } = useIndexPage()

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
        <Button
          className='menu-btn'
          onClick={handleClickModerator}
        >Модератор ОЭЗ</Button>
        <Button
          className='menu-btn'
          onClick={handleClickHr}
        >Представитель HR</Button>
        <Button
          className='menu-btn'
          onClick={handleClickUniversity}
        >Университет</Button>
        <Button
          className='menu-btn'
          onClick={handleClickCandidate}
        >Соискатель</Button>
      </section>
    </DefaultLayout>
  );
}
