import React from 'react';
import { Card, CardBody, CardTitle, Badge } from '../../components/ui';
import { TimelineChart } from './charts/TimelineChart';

interface ObservationTimelineProps {
  data: Array<{ date: string; count: number }>;
}

export function ObservationTimeline({ data }: ObservationTimelineProps) {
  const totalCount = data.reduce((sum, item) => sum + item.count, 0);

  return (
    <Card>
      <CardBody>
        <div className="flex items-center justify-between mb-4">
          <CardTitle>Observation Activity</CardTitle>
          <div className="flex gap-2">
            <Badge variant="info">Last 30 days</Badge>
            {totalCount > 0 && (
              <Badge variant="ghost">{totalCount} total</Badge>
            )}
          </div>
        </div>
        <TimelineChart data={data} />
      </CardBody>
    </Card>
  );
}
