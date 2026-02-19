import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import CaseList from "./components/CaseList";
import CaseDetail from "./components/CaseDetail";

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/cases" replace />} />
        <Route path="/cases" element={<CaseList />} />
        <Route path="/cases/:caseId" element={<CaseDetail />} />
      </Routes>
    </Layout>
  );
}

export default App;

