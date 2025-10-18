export interface ISelectElement {
    key: string;
    label: string;
}

export interface ISelect {
    list: Array<ISelectElement>;
    value: string;
    className?: string;
    onChange: (e: any) => void
}