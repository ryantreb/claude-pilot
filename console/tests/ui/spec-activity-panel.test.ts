/**
 * Tests for Task 7: SpecActivity dashboard panel
 *
 * Validates:
 * - Component renders with specStats prop
 * - Shows completion chart section
 * - Shows recently verified specs list
 * - Shows empty state when no verified specs
 * - Uses Card/CardBody/CardTitle pattern
 */
import { describe, it, expect } from "bun:test";
import { readFileSync } from "fs";
import path from "path";
import React from "react";
import { renderToString } from "react-dom/server";

const COMPONENT_PATH = path.join(
  __dirname,
  "../../src/ui/viewer/views/Dashboard/SpecActivity.tsx",
);
const source = readFileSync(COMPONENT_PATH, "utf-8");

describe("Task 7: SpecActivity source", () => {
  it("should use Card/CardBody/CardTitle components", () => {
    expect(source).toContain("Card");
    expect(source).toContain("CardBody");
    expect(source).toContain("CardTitle");
  });

  it("should import BarChart from recharts", () => {
    expect(source).toContain("BarChart");
    expect(source).toContain("Bar");
    expect(source).toContain("recharts");
  });

  it("should use success color for bars", () => {
    expect(source).toContain("--su");
  });

  it("should show empty state text", () => {
    expect(source).toContain("No specs completed yet");
  });

  it("should render recently verified specs", () => {
    expect(source).toContain("recentlyVerified");
  });
});

describe("Task 7: SpecActivity rendering", () => {
  it("should render with data using renderToString", async () => {
    const { SpecActivity } = await import(
      "../../src/ui/viewer/views/Dashboard/SpecActivity"
    );
    const html = renderToString(
      React.createElement(SpecActivity, {
        specStats: {
          totalSpecs: 14,
          verified: 10,
          inProgress: 2,
          pending: 2,
          avgIterations: 1.2,
          totalTasksCompleted: 45,
          totalTasks: 52,
          completionTimeline: [
            { date: "2026-02-08", count: 2 },
            { date: "2026-02-09", count: 1 },
          ],
          recentlyVerified: [
            { name: "auth-feature", verifiedAt: "2026-02-09T10:00:00Z" },
          ],
        },
      }),
    );
    expect(html).toContain("Spec Activity");
    expect(html).toContain("auth-feature");
  });

  it("should render empty state when no verified specs", async () => {
    const { SpecActivity } = await import(
      "../../src/ui/viewer/views/Dashboard/SpecActivity"
    );
    const html = renderToString(
      React.createElement(SpecActivity, {
        specStats: {
          totalSpecs: 0,
          verified: 0,
          inProgress: 0,
          pending: 0,
          avgIterations: 0,
          totalTasksCompleted: 0,
          totalTasks: 0,
          completionTimeline: [],
          recentlyVerified: [],
        },
      }),
    );
    expect(html).toContain("No specs completed yet");
  });
});
