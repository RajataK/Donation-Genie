import createClient from "openapi-fetch";
import type { paths } from "../types/generated/api";

const baseUrl = import.meta.env.VITE_API_URL ?? "";

export const apiClient = createClient<paths>({ baseUrl });
