import { atom } from "recoil";

export const userState = atom({
  key: "userState",
  default: null,
});

export const repoState = atom({
  key: "repoState",
  default: null,
});
