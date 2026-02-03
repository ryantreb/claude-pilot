# Changelog

All notable changes to Claude Pilot will be documented in this file.

## [6.0.6] - 2026-02-02

### Bug Fixes

- Improved Plan and Spec Verifier Flow

## [6.0.5] - 2026-02-02

### Bug Fixes

- Add demo gif to README
- Make sx vault setup mandatory when sx installed but not configured

## [6.0.4] - 2026-02-02

### Bug Fixes

- Reduce GitHub API calls and simplify installer cleanup

## [6.0.3] - 2026-02-02

### Bug Fixes

- Shorten banner tagline to fit within box width
- Update claude-mem config tests to expect chroma enabled
- Remove claude alias and update branding to Production-Grade Development

## [6.0.2] - 2026-02-02

### Bug Fixes

- Preserve user's .claude/skills folder and clean up empty rules/custom

## [6.0.1] - 2026-02-02

### Bug Fixes

- Remove duplicate sync step in release workflow
- Resolve release pipeline failure and remove codepro fallbacks
- Emphasize running installer in project folder and remove git setup step
- Add backwards compatibility for --restart-ccp argument

### Documentation

- Simplify install command for easier copying

## [6.0.0] - 2026-02-02

Major release introducing Claude Pilot with multi-pass verification and installer improvements.

### Features

- **Renamed project to Claude Pilot** - Full rebrand from claude-codepro
- **Multi-pass plan verification** - plan-verifier agent validates plans match user requirements before approval
- **Multi-pass code verification** - spec-verifier agent verifies implementation matches the plan
- **Installer auto-version** - Auto-fetches latest version from GitHub API when no version specified
- **Changelog generation** - git-cliff integration for automatic CHANGELOG.md updates

### Bug Fixes

- Update documentation to use claude command instead of pilot alias
- Improve installer location and sync workflow
- Make SEO descriptions consistent with new messaging
- Remove Umami analytics
- Update favicon to local file and fix remaining old messaging
- Rebrand messaging to "Claude Code, Done Right"
- Address PR review findings for installer robustness
- Unquote multi-argument variables in install.sh
- Add sx tool and update rules paths
- Improve worker cleanup and installer reliability

### Breaking Changes

- Project renamed from claude-codepro to claude-pilot
- Config location changed from `.claude/` to `~/.pilot/`
- Standard rules now in `~/.claude/rules/`, custom rules in `.claude/rules/`
