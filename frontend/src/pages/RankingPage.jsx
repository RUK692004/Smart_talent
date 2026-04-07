import { useEffect, useMemo, useState, useCallback } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import PageLayout from "../components/layout/PageLayout";
import FilterBar from "../components/ranking/FilterBar";
import RankingTable from "../components/ranking/RankingTable";
import CandidateDrawer from "../components/ranking/CandidateDrawer";
import { getRankingByJD } from "../services/rankingService";

function RankingPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [jdId, setJdId] = useState("");
  const [minScore, setMinScore] = useState("");
  const [skillFilter, setSkillFilter] = useState("");
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const extractCandidates = (data) => {
    if (Array.isArray(data)) return data;
    if (Array.isArray(data?.rankings)) return data.rankings;
    if (Array.isArray(data?.candidates)) return data.candidates;
    if (Array.isArray(data?.results)) return data.results;
    if (Array.isArray(data?.ranked_candidates)) return data.ranked_candidates;
    if (Array.isArray(data?.data)) return data.data;
    if (Array.isArray(data?.matches)) return data.matches;
    return [];
  };

  const handleLoadRanking = useCallback(
    async (customJdId) => {
      const finalJdId = String(customJdId ?? jdId).trim();

      if (!finalJdId) {
        alert("Please enter a JD ID.");
        return;
      }

      try {
        setLoading(true);
        setError("");
        setCandidates([]);
        setSelectedCandidate(null);

        navigate(`/ranking?jd=${finalJdId}`, { replace: true });

        const data = await getRankingByJD(finalJdId);
        console.log("Ranking API response:", data);

        const extractedCandidates = extractCandidates(data);
        setCandidates(extractedCandidates);
      } catch (err) {
        console.error("Failed to load ranking:", err);
        setError("Failed to load ranking data.");
        setCandidates([]);
      } finally {
        setLoading(false);
      }
    },
    [jdId, navigate]
  );

  useEffect(() => {
    const jdFromUrl = searchParams.get("jd");

    if (jdFromUrl) {
      setJdId(jdFromUrl);
      handleLoadRanking(jdFromUrl);
    }
  }, [searchParams, handleLoadRanking]);

  const filteredCandidates = useMemo(() => {
    return candidates.filter((candidate) => {
      const score =
        candidate.score ??
        candidate.compatibility_score ??
        candidate.match_score ??
        candidate.similarity_score ??
        0;

      const skills =
        candidate.skills ||
        candidate.matched_skills ||
        candidate.top_skills ||
        [];

      const matchesScore =
        minScore === "" || Number(score) >= Number(minScore);

      const matchesSkill =
        skillFilter.trim() === "" ||
        skills.some((skill) =>
          String(skill).toLowerCase().includes(skillFilter.toLowerCase())
        );

      return matchesScore && matchesSkill;
    });
  }, [candidates, minScore, skillFilter]);

  const normalizedCandidates = useMemo(() => {
    return filteredCandidates.map((candidate) => ({
      id:
        candidate.id ||
        candidate.resume_id ||
        candidate.candidate_id ||
        candidate.filename ||
        Math.random().toString(36).slice(2),

      name:
        candidate.name ||
        candidate.candidate_name ||
        candidate.filename ||
        candidate.resume_name ||
        "Unknown Candidate",

      score:
        candidate.score ??
        candidate.compatibility_score ??
        candidate.match_score ??
        candidate.similarity_score ??
        0,

      skills:
        candidate.skills ||
        candidate.matched_skills ||
        candidate.top_skills ||
        [],

      experience:
        candidate.experience ??
        candidate.years_of_experience ??
        candidate.experience_years ??
        0,

      justification:
        candidate.justification ||
        candidate.ai_justification ||
        candidate.summary_of_fit ||
        candidate.reason ||
        "No justification available.",

      summary:
        candidate.summary ||
        candidate.profile_summary ||
        "",

      ranking_reason:
        candidate.ranking_reason ||
        candidate.reasoning ||
        "",

      experience_depth:
        candidate.experience_depth ||
        candidate.experience_details ||
        "",
    }));
  }, [filteredCandidates]);

  return (
    <PageLayout>
      <h1>Ranking Page</h1>
      <p style={{ color: "#475569", marginTop: "8px" }}>
        View ranked candidates, filter results, and inspect AI fit summaries.
      </p>

      <FilterBar
        jdId={jdId}
        setJdId={setJdId}
        onLoadRanking={() => handleLoadRanking()}
        minScore={minScore}
        setMinScore={setMinScore}
        skillFilter={skillFilter}
        setSkillFilter={setSkillFilter}
      />

      {loading && <p style={{ marginTop: "20px" }}>Loading ranking data...</p>}

      {error && (
        <p style={{ marginTop: "20px", color: "red" }}>{error}</p>
      )}

      {!loading && !error && (
        <RankingTable
          candidates={normalizedCandidates}
          onSelectCandidate={setSelectedCandidate}
        />
      )}

      <CandidateDrawer
        candidate={selectedCandidate}
        onClose={() => setSelectedCandidate(null)}
      />
    </PageLayout>
  );
}

export default RankingPage;