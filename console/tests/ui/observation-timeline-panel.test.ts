/**
 * Tests for Task 8: ObservationTimeline dashboard panel
 *
 * Validates:
 * - Component renders with data prop
 * - Reuses existing TimelineChart component
 * - Shows empty state when no data
 * - Card header shows title and total count
 */
import { describe, it, expect } from "bun:test";
import { readFileSync } from "fs";
import path from "path";
import React from "react";
import { renderToString } from "react-dom/server";

const COMPONENT_PATH = path.join(
  __dirname,
  "../../src/ui/viewer/views/Dashboard/ObservationTimeline.tsx",
);
const source = readFileSync(COMPONENT_PATH, "utf-8");

describe("Task 8: ObservationTimeline source", () => {
  it("should use Card/CardBody/CardTitle components", () => {
    expect(source).toContain("Card");
    expect(source).toContain("CardBody");
    expect(source).toContain("CardTitle");
  });

  it("should reuse existing TimelineChart component", () => {
    expect(source).toContain("TimelineChart");
    expect(source).toContain("./charts/TimelineChart");
  });

  it("should show Observation Activity title", () => {
    expect(source).toContain("Observation Activity");
  });

  it("should show Last 30 days badge", () => {
    expect(source).toContain("Last 30 days");
  });
});

describe("Task 8: ObservationTimeline rendering", () => {
  it("should render with data using renderToString", async () => {
    const { ObservationTimeline } = await import(
      "../../src/ui/viewer/views/Dashboard/ObservationTimeline"
    );
    const html = renderToString(
      React.createElement(ObservationTimeline, {
        data: [
          { date: "2026-02-08", count: 5 },
          { date: "2026-02-09", count: 12 },
        ],
      }),
    );
    expect(html).toContain("Observation Activity");
    expect(html).toContain("17");
  });

  it("should render empty state when no data", async () => {
    const { ObservationTimeline } = await import(
      "../../src/ui/viewer/views/Dashboard/ObservationTimeline"
    );
    const html = renderToString(
      React.createElement(ObservationTimeline, { data: [] }),
    );
    expect(html).toContain("Observation Activity");
  });
});
