import http from "k6/http";
import { check, sleep, group } from "k6";

export const options = {
  stages: [
    { duration: "5s", target: 1 },  // smoke
    { duration: "10s", target: 3 }, // light load
    { duration: "5s", target: 0 },  // ramp down
  ],
  thresholds: {
    "http_req_duration{group:happy}": ["p(95)<800"],
    "http_req_failed{group:happy}": ["rate<0.01"],
  },
};

const url = "https://rickandmortyapi.com/graphql";

export default function () {
  group("happy", () => {
    const query = `
      query {
        character(id: 1) {
          id
          name
          status
          species
          origin {
            name
          }
        }
      }
    `;

    const payload = JSON.stringify({ query });
    const params = { headers: { "Content-Type": "application/json" } };

    const res = http.post(url, payload, params);

    // --- basic HTTP checks ---
    check(res, {
      "status is 200": (r) => r.status === 200,
      "response is JSON": (r) =>
        r.headers["Content-Type"]?.includes("application/json"),
    });

    // --- safe JSON parse ---
    let body = {};
    try {
      body = JSON.parse(res.body);
    } catch {}

    // --- GraphQL schema checks ---
    check(body, {
      "no GraphQL errors": (b) => !b.errors,
      "character data exists": (b) => b.data?.character,
      "character id is 1": (b) => b.data?.character?.id === "1",
      "name is Rick Sanchez": (b) =>
        b.data?.character?.name === "Rick Sanchez",
      "origin name exists": (b) =>
        b.data?.character?.origin?.name !== undefined,
    });

    sleep(1);
    
    // ***EDGE CASES***
  group("edge-case", () => {
    // 1) Non-existing character
    const invalidQuery = `
      query {
        character(id: 9999999) {
          id
          name
        }
      }
    `;
    const invalidRes = http.post(
      url,
      JSON.stringify({ query: invalidQuery }),
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    check(invalidRes, {
      "invalid id returns 200": (r) => r.status === 200,
    });

    let invalidBody = {};
    try {
      invalidBody = JSON.parse(invalidRes.body);
    } catch {}

    check(invalidBody, {
      "invalid returns null or error": (b) =>
        b.data?.character === null || b.errors,
    });

    sleep(0.5);

    // 2) Invalid field
    const badFieldQuery = `
      query {
        character(id: 1) {
          id
          unknownFieldXYZ
        }
      }
    `;

    const badFieldRes = http.post(
      url,
      JSON.stringify({ query: badFieldQuery }),
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    check(badFieldRes, {
      "invalid field returns 200 or 400": (r) => r.status === 200 || r.status === 400,
    });

    let badFieldBody = {};
    try {
      badFieldBody = JSON.parse(badFieldRes.body);
    } catch {}

    check(badFieldBody, {
      "invalid field produces GraphQL errors": (b) =>
        Array.isArray(b.errors) && b.errors.length > 0,
    });

    sleep(0.5);
  });
});
}
