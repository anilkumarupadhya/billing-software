// utils/dateUtils.ts

// Format a date to human-readable string
export const formatDate = (date: string | Date): string => {
    const d = typeof date === "string" ? new Date(date) : date;
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };
  
  // Get today's date (YYYY-MM-DD)
  export const today = (): string => {
    return new Date().toISOString().split("T")[0];
  };
  