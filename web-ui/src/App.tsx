import { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// ⚡ Bolt Performance Optimization: Code Splitting
// Lazy load route components to reduce initial bundle size and improve time-to-interactive.
const ChatPage = lazy(() => import('./pages/ChatPage').then(module => ({ default: module.ChatPage })));
const CodeWikiPage = lazy(() => import('./pages/CodeWikiPage').then(module => ({ default: module.CodeWikiPage })));
const TraceAnalysisPage = lazy(() => import('./pages/TraceAnalysisPage').then(module => ({ default: module.TraceAnalysisPage })));
const RepositoryDetailPage = lazy(() => import('./components/CodeWiki/RepositoryDetailPage').then(module => ({ default: module.RepositoryDetailPage })));

function App() {
  return (
    <Router>
      <Suspense fallback={<div className="flex h-screen items-center justify-center bg-bg-100 text-text-200 font-mono text-sm">Loading...</div>}>
        <Routes>
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/codewiki" element={<CodeWikiPage />} />
          <Route path="/codewiki/:repoName" element={<RepositoryDetailPage />} />
          <Route path="/traces" element={<TraceAnalysisPage />} />
          <Route path="/" element={<Navigate to="/chat" replace />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

export default App;
