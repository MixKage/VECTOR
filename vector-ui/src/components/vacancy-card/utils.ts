import { ICardData } from "./types"


function getDifferenceInDays(date1: Date, date2: Date): number {
  const timeDifference = date2.getTime() - date1.getTime();
  const daysDifference = timeDifference / (1000 * 60 * 60 * 24);
  return Math.floor(daysDifference); // Округляем до целых дней
}

export const prepareDataForCards = (data: any): Array<ICardData> => {
    return data.map((value: any) => {
        return {
            id: value.id.toString(),
            name: value.name,
            creationDate: new Date(value.creation_date),
            expiryDate: new Date(value.expiry_date),
            daysLeft: getDifferenceInDays(new Date(value.expiry_date), new Date(value.creation_date)),
            specialization: value.specialization,
            candidatedCount: value.candidates.length,
            hasNew: value.candidates.some((x: any) => x.is_new),
            company: value.company,
        }
    })
}