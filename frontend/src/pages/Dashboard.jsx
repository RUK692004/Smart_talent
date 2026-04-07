import { useEffect, useState } from "react";
import PageLayout from "../components/layout/PageLayout";
import StatCard from "../components/dashboard/StatCard";
import TopTalentPreview from "../components/dashboard/TopTalentPreview";
import QuickActions from "../components/dashboard/QuickActions";
import SystemStatus from "../components/dashboard/SystemStatus";
import ActiveJDList from "../components/dashboard/ActiveJDList";
import RecentUploads from "../components/dashboard/RecentUploads";

import { getAllResumes } from "../services/resumeService";
import { getAllJDs } from "../services/jdService";
import { getRankingByJD } from "../services/rankingService";

function Dashboard() {
  const [resumeCount, setResumeCount] = useState(0);
  const [jobCount, setJobCount] = useState(0);

  const [resumes, setResumes] = useState([]);
  const [jds, setJds] = useState([]);
  const [topCandidates, setTopCandidates] = useState([]);

  const [topTalentLoading, setTopTalentLoading] = useState(false);

  const [statusStats, setStatusStats] = useState({
    parsed: 0,
    failed: 0,
    pending: 0,
  });

  const normalizeJDs = (data) => {
    if (Array.isArray(data)) return data;
    if (Array.isArray(data?.jds)) return data.jds;
    if (Array.isArray(data?.jd)) return data.jd;
    if (Array.isArray(data?.data)) return data.data;
    if (Array.isArray(data?.job_descriptions)) return data.job_descriptions;
    if (data?.jd && typeof data.jd === "object") return [data.jd];
    return [];
  };

  const normalizeCandidates = (data) => {
    if (Array.isArray(data)) return data;
    if (Array.isArray(data?.rankings)) return data.rankings;
    if (Array.isArray(data?.candidates)) return data.candidates;
    if (Array.isArray(data?.results)) return data.results;
    if (Array.isArray(data?.ranked_candidates)) return data.ranked_candidates;
    if (Array.isArray(data?.matches)) return data.matches;
    if (Array.isArray(data?.data)) return data.data;
    return [];
  };

  const loadTopTalent = async (jdList) => {
    if (!jdList.length) {
      setTopCandidates([]);
      return;
    }

    try {
      setTopTalentLoading(true);

      const firstJDId = jdList[0].id;
      const rankingData = await getRankingByJD(firstJDId);
      const rankedCandidates = normalizeCandidates(rankingData);

      setTopCandidates(
        Array.isArray(rankedCandidates) ? rankedCandidates.slice(0, 3) : []
      );
    } catch (error) {
      console.error("Failed to load top talent:", error);
      setTopCandidates([]);
    } finally {
      setTopTalentLoading(false);
    }
  };

  const loadDashboard = async () => {
    try {
      const [resumeData, jdData] = await Promise.all([
        getAllResumes(),
        getAllJDs(),
      ]);

      const resumeList = Array.isArray(resumeData?.resumes)
        ? resumeData.resumes
        : [];

      const jdList = normalizeJDs(jdData);

      setResumeCount(resumeData?.count || resumeList.length || 0);
      setJobCount(jdData?.count || jdList.length || 0);

      setResumes(resumeList);
      setJds(jdList);

      setStatusStats({
        parsed: resumeList.length,
        failed: 0,
        pending: 0,
      });

      await loadTopTalent(jdList);
    } catch (error) {
      console.error("Failed to load dashboard data:", error);
      setTopCandidates([]);
      setJds([]);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const stats = [
    { title: "Total Resumes", value: resumeCount, accent: "#2563eb" },
    { title: "Active Job Roles", value: jobCount, accent: "#7c3aed" },
    { title: "Top Candidates", value: topCandidates.length, accent: "#16a34a" },
  ];

  return (
    <PageLayout>
      <div style={{ marginBottom: "24px" }}>
        <h1 style={{ marginBottom: "8px" }}>Dashboard</h1>
        <p style={{ color: "#64748b", margin: 0 }}>
          Monitor uploads, job roles, and top-ranked talent from one place.
        </p>
      </div>

      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
        {stats.map((stat, index) => (
          <StatCard
            key={index}
            title={stat.title}
            value={stat.value}
            accent={stat.accent}
          />
        ))}
      </div>

      <div style={{ marginTop: "24px" }}>
        <SystemStatus stats={statusStats} />
      </div>

      <div style={{ marginTop: "24px" }}>
        <QuickActions />
      </div>

      <div style={{ marginTop: "32px" }}>
        <ActiveJDList
          jds={jds}
          onRefresh={loadDashboard}
        />
      </div>

      <div style={{ marginTop: "32px" }}>
        <TopTalentPreview
          candidates={topCandidates}
          jdId={jds[0]?.id}
          loading={topTalentLoading}
        />
      </div>

      <div style={{ marginTop: "32px" }}>
        <RecentUploads
          resumes={resumes.slice(0, 5)}
          onRefresh={loadDashboard}
        />
      </div>
    </PageLayout>
  );
}

export default Dashboard;