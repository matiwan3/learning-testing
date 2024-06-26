type Customer = {
    birthday?: Date
};

function getCustomer(id: number): Customer | null | undefined {
    return id === 0 ? null : { birthday: new Date() };

}

let customer = getCustomer(1);
if (customer !== null && customer !== undefined)
    // Optional property access
    console.log(customer?.birthday?.getFullYear());

// Optional element access operator
// if (customers !== null)
// customers?.[0]

// Optional call
// let log: any = (message: strirng) 
let log: any = null;
log?.('a');

