import http from "k6/http";
import { check, sleep, group } from "k6";

export const options = {
  vus: 1,
  iterations: 1,
};

export default function () {
  group("RESTCountries", () => {
    const url = "https://restcountries.com/v3.1/name/turkey";

    const res = http.get(url);

    // --- 1) HTTP & JSON validation ---
    check(res, {
      "status is 200": (r) => r.status === 200,
      "response is JSON": (r) =>
        r.headers["Content-Type"]?.includes("application/json"),
    });

    let body;
    try {
      body = JSON.parse(res.body);
    } catch {
      body = [];
    }

    // --- 2) Schema / shape checks ---
    check(body, {
      "response is a non-empty array": (b) =>
        Array.isArray(b) && b.length > 0,

      "country has official name": (b) =>
        b[0]?.name?.official !== undefined,

      "capital field exists and is an array": (b) =>
        Array.isArray(b[0]?.capital),

      "region field exists": (b) => b[0]?.region !== undefined,
    });

    // --- 3) Functional assertion ---
    check(body, {
      "country is Turkey": (b) =>
        b[0]?.name?.official === "Republic of Turkey",
    });

    sleep(1);
  });
}