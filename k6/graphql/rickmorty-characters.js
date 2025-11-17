import http from "k6/http";
import { check, sleep, group } from "k6";

export const options = {
  vus: 1,
  iterations: 1,
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
  });
}
