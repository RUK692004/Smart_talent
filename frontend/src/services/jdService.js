import api from "./api";

export const getAllJDs = async () => {
  const res = await api.get("/jd/");
  return res.data;
};

export const uploadJD = async (jdData) => {
  const res = await api.post("/jd/upload", jdData);
  return res.data;
};

export const deleteJD = async (id) => {
  const res = await api.delete(`/jd/${id}`);
  return res.data;
};

export const deleteAllJDs = async () => {
  const res = await api.delete("/jd/delete/all");
  return res.data;
};
