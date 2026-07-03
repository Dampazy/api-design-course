import { Route, Routes } from 'react-router-dom'
import NavBar from './components/NavBar.jsx'
import Home from './pages/Home.jsx'
import TheoryList from './pages/TheoryList.jsx'
import TheoryDetail from './pages/TheoryDetail.jsx'
import PracticeList from './pages/PracticeList.jsx'
import TaskDetail from './pages/TaskDetail.jsx'
import FinalTest from './pages/FinalTest.jsx'
import ProgressStats from './pages/ProgressStats.jsx'

function App() {
  return (
    <>
      <NavBar />
      <main className="page">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/theory" element={<TheoryList />} />
          <Route path="/theory/:slug" element={<TheoryDetail />} />
          <Route path="/practice" element={<PracticeList />} />
          <Route path="/practice/:taskId" element={<TaskDetail />} />
          <Route path="/final-test" element={<FinalTest />} />
          <Route path="/progress" element={<ProgressStats />} />
        </Routes>
      </main>
    </>
  )
}

export default App
