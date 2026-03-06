import { useEffect } from "react";
import { useFoodBanks } from "../../hooks/useFoodBanks";

export default function FoodBankLogger() {
  const { data, error, isSuccess, isError } = useFoodBanks();

  useEffect(() => {
    if (isSuccess) {
      console.log("Food banks loaded:", data);
    }
  }, [isSuccess, data]);

  useEffect(() => {
    if (isError) {
      console.error("Failed to fetch food banks:", error);
    }
  }, [isError, error]);

  return null;
}
