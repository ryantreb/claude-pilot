import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { Card, CardBody, CardTitle, Badge } from '../../components/ui';
import { ChartTooltip } from './charts/ChartTooltip';

interface SpecStats {
  totalSpecs: number;
  verified: number;
  inProgress: number;
  pending: number;
  avgIterations: number;
  totalTasksCompleted: number;
  totalTasks: number;
  completionTimeline: Array<{ date: string; count: number }>;
  recentlyVerified: Array<{ name: string; verifiedAt: string }>;
}

interface SpecActivityProps {
  specStats: SpecStats;
}

export function SpecActivity({ specStats }: SpecActivityProps) {
  const hasVerified = specStats.verified > 0;

  if (!hasVerified && specStats.completionTimeline.length === 0) {
    return (
      <Card>
        <CardBody>
          <CardTitle>Spec Activity</CardTitle>
          <div className="flex items-center justify-center h-48 text-base-content/50">
            No specs completed yet
          </div>
        </CardBody>
      </Card>
    );
  }

  const formattedData = specStats.completionTimeline.map((item) => ({
    ...item,
    displayDate: new Date(item.date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    }),
  }));

  return (
    <Card>
      <CardBody>
        <div className="flex items-center justify-between mb-4">
          <CardTitle>Spec Activity</CardTitle>
          <div className="flex gap-2">
            <Badge variant="success">{specStats.verified} verified</Badge>
            {specStats.avgIterations > 0 && (
              <Badge variant="info">avg {specStats.avgIterations.toFixed(1)} iterations</Badge>
            )}
          </div>
        </div>

        {formattedData.length > 0 && (
          <div className="h-48 w-full mb-4">
            <ResponsiveContainer width="100%" height="100%" debounce={50}>
              <BarChart data={formattedData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-base-content/10" />
                <XAxis
                  dataKey="displayDate"
                  tick={{ fontSize: 12 }}
                  className="text-base-content/60"
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  tick={{ fontSize: 12 }}
                  className="text-base-content/60"
                  tickLine={false}
                  axisLine={false}
                  allowDecimals={false}
                />
                <Tooltip
                  content={
                    <ChartTooltip
                      labelFormatter={(label) => `Date: ${label}`}
                      valueFormatter={(value) => [value, 'Specs Verified']}
                    />
                  }
                />
                <Bar
                  dataKey="count"
                  fill="oklch(var(--su))"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {specStats.recentlyVerified.length > 0 && (
          <div>
            <div className="text-sm font-medium text-base-content/70 mb-2">Recently Verified</div>
            <div className="space-y-1">
              {specStats.recentlyVerified.map((spec) => (
                <div key={spec.name} className="flex justify-between items-center text-sm">
                  <span className="font-mono text-base-content/80">{spec.name}</span>
                  <span className="text-base-content/50">
                    {new Date(spec.verifiedAt).toLocaleDateString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardBody>
    </Card>
  );
}
