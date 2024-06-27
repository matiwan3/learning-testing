const small = 1;
const medium = 2;
const large = 3;

// PascalCase
const enum Size { Small = 1 , Medium, Large}
// const enum Size { m = 'm' , s = 's', l = 'l'}
let mySize: Size = Size.Medium;
console.log(mySize);
