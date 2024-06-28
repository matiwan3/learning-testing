// type aliases
// unions and intersections
// type narrowing
// nullable types
// the unknown type
// the never type


type Employee = {
    readonly id: number,
    name: string,
    retire: (date: Date) => void
}

let employee: Employee=  {
    id: 1, 
    name: 'Mosh', 
    retire: (date: Date) => {
        console.log(date);
    }
};
