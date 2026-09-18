import { Link, Outlet } from 'react-router-dom'

function DashboardLayout() {
  return (
    <div className="min-h-screen bg-slate-100">
      <header className="border-b bg-white p-4">
        <h1 className="text-xl font-bold">ComplianceAI</h1>
      </header>

      <div className="flex">
        <aside className="min-h-[calc(100vh-73px)] w-64 border-r bg-white p-4">
          <nav className="space-y-2">
            <Link
              to="/dashboard"
              className="block rounded-lg p-2 hover:bg-slate-100"
            >
              Dashboard
            </Link>

            <Link
              to="/companies"
              className="block rounded-lg p-2 hover:bg-slate-100"
            >
              Companies
            </Link>

            <Link
              to="/settings"
              className="block rounded-lg p-2 hover:bg-slate-100"
            >
              Settings
            </Link>
          </nav>
        </aside>

        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default DashboardLayout