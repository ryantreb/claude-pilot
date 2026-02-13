/**
 * UsageRoutes
 *
 * API endpoints for Claude Code usage data via ccusage CLI.
 * Caches results for 5 minutes to avoid repeated CLI invocations.
 */

import express, { type Request, type Response } from "express";
import { BaseRouteHandler } from "../BaseRouteHandler.js";

const DATE_REGEX = /^\d{8}$/;
const CACHE_TTL_MS = 5 * 60 * 1000;

interface CacheEntry {
  data: unknown;
  timestamp: number;
}

export class UsageRoutes extends BaseRouteHandler {
  private cache = new Map<string, CacheEntry>();
  private ccusagePath: string | null;
  private pendingExecutions = new Map<string, Promise<unknown>>();

  constructor() {
    super();
    this.ccusagePath = this.resolveCcusage();
  }

  setupRoutes(app: express.Application): void {
    app.get("/api/usage/daily", this.wrapHandler(this.handleDaily.bind(this)));
    app.get("/api/usage/monthly", this.wrapHandler(this.handleMonthly.bind(this)));
    app.get("/api/usage/models", this.wrapHandler(this.handleModels.bind(this)));
  }

  async handleDaily(req: Request, res: Response): Promise<void> {
    if (!this.ccusagePath) {
      res.json({ available: false, error: "ccusage not installed" });
      return;
    }

    const since = req.query.since as string | undefined;
    const until = req.query.until as string | undefined;

    if (since && !DATE_REGEX.test(since)) {
      this.badRequest(res, "Invalid since parameter. Expected YYYYMMDD format.");
      return;
    }
    if (until && !DATE_REGEX.test(until)) {
      this.badRequest(res, "Invalid until parameter. Expected YYYYMMDD format.");
      return;
    }

    const effectiveSince = since || this.defaultSince();
    const cacheKey = `daily-${effectiveSince}-${until || ""}`;

    const data = await this.getCachedOrExecute(cacheKey, () => {
      const args = ["daily", "--json", "--since", effectiveSince];
      if (until) args.push("--until", until);
      return this.runCcusage(args);
    });

    res.json({ available: true, ...data as object });
  }

  async handleMonthly(_req: Request, res: Response): Promise<void> {
    if (!this.ccusagePath) {
      res.json({ available: false, error: "ccusage not installed" });
      return;
    }

    const cacheKey = "monthly";

    const data = await this.getCachedOrExecute(cacheKey, () => {
      return this.runCcusage(["monthly", "--json"]);
    });

    res.json({ available: true, ...data as object });
  }

  async handleModels(_req: Request, res: Response): Promise<void> {
    if (!this.ccusagePath) {
      res.json({ available: false, error: "ccusage not installed" });
      return;
    }

    const cacheKey = "monthly";
    const data = await this.getCachedOrExecute(cacheKey, () => {
      return this.runCcusage(["monthly", "--json"]);
    }) as { monthly?: Array<{ modelBreakdowns?: Array<{ modelName: string; cost: number; inputTokens: number; outputTokens: number; cacheCreationTokens: number; cacheReadTokens: number }> }> };

    const modelMap = new Map<string, { model: string; totalCost: number; inputTokens: number; outputTokens: number; totalTokens: number }>();

    for (const month of data.monthly || []) {
      for (const breakdown of month.modelBreakdowns || []) {
        const totalTokens = (breakdown.inputTokens || 0) + (breakdown.outputTokens || 0) +
          (breakdown.cacheCreationTokens || 0) + (breakdown.cacheReadTokens || 0);
        const existing = modelMap.get(breakdown.modelName);
        if (existing) {
          existing.totalCost += breakdown.cost || 0;
          existing.inputTokens += breakdown.inputTokens || 0;
          existing.outputTokens += breakdown.outputTokens || 0;
          existing.totalTokens += totalTokens;
        } else {
          modelMap.set(breakdown.modelName, {
            model: breakdown.modelName,
            totalCost: breakdown.cost || 0,
            inputTokens: breakdown.inputTokens || 0,
            outputTokens: breakdown.outputTokens || 0,
            totalTokens,
          });
        }
      }
    }

    const models = Array.from(modelMap.values()).sort((a, b) => b.totalCost - a.totalCost);
    res.json({ available: true, models });
  }

  private async getCachedOrExecute(cacheKey: string, execute: () => Promise<unknown>): Promise<unknown> {
    const cached = this.cache.get(cacheKey);
    if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
      return cached.data;
    }

    const pending = this.pendingExecutions.get(cacheKey);
    if (pending) {
      return pending;
    }

    const promise = execute().then((data) => {
      this.cache.set(cacheKey, { data, timestamp: Date.now() });
      return data;
    }).finally(() => {
      this.pendingExecutions.delete(cacheKey);
    });

    this.pendingExecutions.set(cacheKey, promise);
    return promise;
  }

  private async runCcusage(args: string[]): Promise<unknown> {
    const proc = Bun.spawn(["ccusage", ...args], {
      stdout: "pipe",
      stderr: "pipe",
    });

    const timer = setTimeout(() => {
      try { proc.kill("SIGTERM"); } catch {}
    }, 30_000);

    try {
      const [stdout, stderr] = await Promise.all([
        new Response(proc.stdout).text(),
        new Response(proc.stderr).text(),
      ]);
      const exitCode = await proc.exited;

      if (exitCode !== 0) {
        throw new Error(`ccusage command failed: ${stderr.slice(0, 200)}`);
      }

      return JSON.parse(stdout);
    } finally {
      clearTimeout(timer);
    }
  }

  private resolveCcusage(): string | null {
    const found = Bun.which("ccusage");
    return found || null;
  }

  private defaultSince(): string {
    const d = new Date();
    d.setDate(d.getDate() - 30);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${y}${m}${day}`;
  }
}
