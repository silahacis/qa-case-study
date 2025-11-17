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

    // ***EDGE CASES***

    // 1) Non-existing country
    const invalid = http.get(
      "https://restcountries.com/v3.1/name/thisCountryDoesNotExist123456"
    );
    check(invalid, {
      "invalid country returns 404 or 200": (r) =>
        r.status === 404 || r.status === 200,
    });

    if (invalid.status === 200) {
      const invalidBody = JSON.parse(invalid.body || "[]");
      check(invalidBody, {
        "empty array for invalid country": (b) =>
          Array.isArray(b) && b.length === 0,
      });
    }

    sleep(0.5);

    // 2) Partial match (should return multiple countries)
    const partial = http.get("https://restcountries.com/v3.1/name/tur");
    check(partial, {
      "partial search returns 200": (r) => r.status === 200,
      "partial search returns multiple results": (r) => {
        try {
          const data = JSON.parse(r.body);
          return Array.isArray(data) && data.length >= 2;
        } catch {
          return false;
        }
      },
    });

    sleep(0.5);

    // 3) Invalid numeric input
    const numeric = http.get("https://restcountries.com/v3.1/name/12345");
    check(numeric, {
      "numeric query handled gracefully": (r) =>
        r.status === 404 || r.status === 200,
    });

    sleep(0.5);

    // 4) Special characters
    const specialInput = encodeURIComponent("%$#@!");
    const special = http.get(
    `https://restcountries.com/v3.1/name/${specialInput}`
    );

    check(special, {
    "special chars do not crash API": (r) =>
        r.status === 404 || r.status === 200,
    });

    sleep(0.5);

    // 5) Empty string
    const emptyQuery = http.get("https://restcountries.com/v3.1/name/");
    check(emptyQuery, {
      "empty query returns valid status (400|404|200)": (r) =>
        r.status === 400 || r.status === 404 || r.status === 200,
    });
    sleep(0.5);
  });
}