import { Activity, BarChart3, FileText, Settings, Users } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

import { Header } from "@/components/header"
import { RecentCases } from "@/components/recent-cases"
import { Sidebar } from "@/components/sidebar"
import { TriageChart } from "@/components/week-chart"

export default function Home() {
  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 dark:bg-gray-900">
          <div className="container mx-auto px-6 py-8">
            <h1 className="text-3xl font-semibold text-gray-800 dark:text-white mb-6">Dashboard</h1>
            <div className="grid gap-6 mb-8 md:grid-cols-2 xl:grid-cols-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Cases Processed</CardTitle>
                  <FileText className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">1,234</div>
                  <p className="text-xs text-muted-foreground">+20.1% from last month</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Average Processing Time</CardTitle>
                  <Activity className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">2.4 minutes</div>
                  <p className="text-xs text-muted-foreground">-0.3 minutes from last week</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Accuracy Rate</CardTitle>
                  <BarChart3 className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">98.7%</div>
                  <p className="text-xs text-muted-foreground">+0.5% from last quarter</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Patients</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">573</div>
                  <p className="text-xs text-muted-foreground">+201 since last week</p>
                </CardContent>
              </Card>
            </div>
            <div className="grid gap-6 mb-8 md:grid-cols-2">
              <Card className="col-span-2">
                <CardHeader>
                  <CardTitle>Triage Processing Statistics</CardTitle>
                </CardHeader>
                <CardContent className="pl-2">
                  <TriageChart />
                </CardContent>
              </Card>
            </div>
            <div className="grid gap-6 mb-8 md:grid-cols-2">
              <Card className="col-span-2">
                <CardHeader>
                  <CardTitle>Recent Triage Cases</CardTitle>
                </CardHeader>
                <CardContent>
                  <RecentCases />
                </CardContent>
              </Card>
            </div>
            <div className="mb-8">
              <Card>
                <CardHeader>
                  <CardTitle>System Status</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center space-x-4">
                    <div className="flex-1">
                      <div className="flex justify-between mb-2">
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">System Load</span>
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">65%</span>
                      </div>
                      <Progress value={65} className="w-full" />
                    </div>
                    <Button variant="outline">
                      <Settings className="mr-2 h-4 w-4" />
                      Manage
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}