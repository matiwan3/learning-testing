"use strict";
function getCustomer(id) {
    return id === 0 ? null : { birthday: new Date() };
}
let customer = getCustomer(1);
if (customer !== null && customer !== undefined)
    console.log(customer.birthday);
//# sourceMappingURL=index11.js.map