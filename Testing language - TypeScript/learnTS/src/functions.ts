
function calculateTax(income: number, taxYear = 10_000): number {
// function calculateTax(income: number, taxYear?: number): number {
    // if ((taxYear || 2022) < 2022)
    if ((taxYear || 2022) < 2022)
        return income * 1.2;
    return income * 1.3;
}

calculateTax(100_000, 2022);