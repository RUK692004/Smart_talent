import api from "./api";

export const getAllResumes = async () => {
  const response = await api.get("/resumes/");
  return response.data;
};

export const deleteResumeById = async (id) => {
  const response = await api.delete(`/resumes/${id}`);
  return response.data;
};

export const deleteAllResumes = async () => {
  const response = await api.delete("/resumes/clear-all");
  return response.data;
};

export const downloadResume = async (id) => {
  const response = await api.get(`/resumes/${id}/download`, {
    responseType: "blob",
  });
  return response.data;
};
