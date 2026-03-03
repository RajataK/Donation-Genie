import createClient from "openapi-fetch";

const baseUrl = import.meta.env.VITE_API_URL ?? "/api";

export const apiClient = createClient({ baseUrl });
