import { useEffect, useState } from "react";
import PageLayout from "../components/layout/PageLayout";
import StatCard from "../components/dashboard/StatCard";
import DataIngestionHub from "../components/dashboard/DataIngestionHub";
import DashboardOverview from "../components/dashboard/DashboardOverview";
import CandidateRankingTable from "../components/dashboard/CandidateRankingTable";
import DataOnboarding from "../components/dashboard/DataOnboarding";
import RecentUploadsTimeline from "../components/dashboard/RecentUploadsTimeline";
import IntelligentRanking from "../components/dashboard/IntelligentRanking";

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
  const [statusStats, setStatusStats] = useState({ parsed: 0, failed: 0, pending: 0 });

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
      setTopCandidates(Array.isArray(rankedCandidates) ? rankedCandidates : []);
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

      const resumeList = Array.isArray(resumeData?.resumes) ? resumeData.resumes : [];
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

  return (
    <PageLayout>
      {/* Header */}
      <div style={{ marginBottom: "24px" }}>
        <p style={{ margin: 0, color: "#6b7280", fontSize: "13px", fontWeight: "500" }}>
          Recruiter Dashboard
        </p>
        <h1 style={{
          margin: "4px 0 0 0",
          fontSize: "28px",
          fontWeight: "700",
          color: "#1a1a2e",
          fontFamily: "'Georgia', serif",
        }}>
          Talent Intelligence Hub
        </h1>
      </div>

      {/* Main 60/40 Layout */}
      <div style={{ display: "flex", gap: "24px" }}>
        {/* LEFT SIDE - 60% */}
        <div style={{ flex: "3", minWidth: 0 }}>
          {/* Stats Cards */}
          <div style={{ display: "flex", gap: "16px", flexWrap: "wrap", marginBottom: "24px" }}>
            <StatCard
              title="Total Resumes"
              value={resumeCount}
              accent="#d4a843"
              bgColor="#fffdf8"
            />
            <StatCard
              title="Active Job Roles"
              value={jobCount}
              accent="#7c3aed"
              bgColor="#faf5ff"
            />
            <StatCard
              title="Top Candidates"
              value={topCandidates.length}
              accent="#10b981"
              bgColor="#f0fdf4"
            />
          </div>

          {/* Candidate Ranking Table */}
          <CandidateRankingTable
            candidates={topCandidates}
            jdId={jds[0]?.id}
          />
        </div>

        {/* RIGHT SIDE - 40% */}
        <div style={{ flex: "2", minWidth: "280px" }}>
          <DataOnboarding />
          <RecentUploadsTimeline resumes={resumes} />
          <IntelligentRanking candidates={topCandidates} />
        </div>
      </div>
    </PageLayout>
  );
}

export default Dashboard;