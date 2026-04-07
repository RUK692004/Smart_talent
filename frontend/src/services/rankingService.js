import api from "./api";

export const getRankingByJD = async (jdId) => {
  const response = await api.get(`/ranking/jd/${jdId}`);
  return response.data;
};

export const getTopCandidatesByJD = async (jdId) => {
  const response = await api.get(`/ranking/jd/${jdId}/top`);
  return response.data;
};