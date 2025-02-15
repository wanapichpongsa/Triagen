"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts"

const data = [
  { name: "Mon", total: 120 },
  { name: "Tue", total: 132 },
  { name: "Wed", total: 101 },
  { name: "Thu", total: 134 },
  { name: "Fri", total: 90 },
  { name: "Sat", total: 72 },
  { name: "Sun", total: 65 },
]

export function TriageChart() {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data}>
        <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value}`} />
        <Bar dataKey="total" fill="#adfa1d" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}