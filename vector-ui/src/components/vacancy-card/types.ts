export interface ICardData {
    id: string,
    name: string,
    creationDate: Date,
    expiryDate: Date,
    daysLeft: number,
    specialization: string,
    candidatedCount: number,
    hasNew: boolean,
    company: string,
}