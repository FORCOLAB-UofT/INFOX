import { atom } from "recoil";

export const userState = atom({
  key: "userState",
  default: { username: "testAdmin", accessToken: "secret-access-token" },
});
