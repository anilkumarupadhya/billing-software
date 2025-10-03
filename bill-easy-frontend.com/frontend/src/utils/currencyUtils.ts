// utils/currencyUtils.ts

// Format a number into USD currency
export const formatCurrency = (amount: number, currency = "USD"): string => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency,
    }).format(amount);
  };
  
  // Parse formatted currency back into number
  export const parseCurrency = (value: string): number => {
    return Number(value.replace(/[^0-9.-]+/g, ""));
  };
  