# YouTube upload details

**Title**
How I Prompted an AI to Upgrade a Wagtail Site (2.7 → 7.4)

**Thumbnail**
`assets/thumb.png` (1280×720)

**Description**

I gave Claude (Claude Code) three prompts. It built a 2019 Wagtail 2.7 site, upgraded it through 2.15 LTS to 7.4 LTS, and recorded every step: 62 commits, 133 command logs, 22 breakages written up, 29 decisions with reasons.

This video is about the prompts, not the code: the eight things in them that did the real work, where the AI stopped and needed me, and the mistakes it made that the method caught.

The eight ideas:
1. Plan first, then wait for approval
2. Put the rules in a file in the repo (CLAUDE.md), not in the chat
3. Record every command
4. Capture each failure before fixing it
5. Define "done" as checks a machine can run, against a baseline
6. Realistic test data with deliberate traps
7. Pin the period, forbid the shortcuts
8. Say how to choose between fixes, and cite versioned docs

Repo (rules file, notes, every log): https://github.com/apequaltowork/wagtail-school
The breakages themselves: "I Upgraded Wagtail 2.7 → 7.4 — Everything That Broke" (companion video)

**Chapters**
0:00 Three prompts, one upgrade
0:51 The prompt method: 1. Plan first, then wait
1:17 2. A rules file in the repo
1:41 3. Record every command
2:05 4. Capture failures before fixing
2:26 5. Define done as machine checks
2:52 6. Realistic data, planted traps
3:13 7. Pin the period
3:30 8. How to choose, versioned sources
3:47 Where it needed me
4:54 The mistakes, and what caught them
5:47 Results and checklist

**Tags**
claude, claude code, ai coding, prompt engineering, wagtail, django, upgrade, ai agent, developer workflow, legacy code

**Captions**
Upload `out/claude-workflow.srt` as English subtitles.
