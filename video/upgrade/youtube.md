# YouTube upload details

**Title**
I Upgraded Wagtail 2.7 → 7.4 — Everything That Broke

**Thumbnail**
`assets/thumb.png` (1280×720)

**Description**

I took a 2019 Wagtail 2.7 site (Django 2.2, Python 3.8) and upgraded it to Wagtail 7.4 LTS on Django 5.2, going through 2.15 LTS on the way. 22 things broke. Most were loud ImportErrors. Four broke silently, and those are what this video is about:

• the 2.10 form-builder change that made every enquiry form lose its data
• StreamField columns that stayed as text, because the 3.0–5.x migration is never generated when you skip versions
• logged search queries deleted by migrate (the copy migration is a no-op since Wagtail 6.0)
• static-file hashing silently switched off by Django 5.1

Every step is a commit, with tags for each stage (v2.7-baseline · v2.15 · v7.4). Every log, screenshot and the full breakage list are in the repo:
https://github.com/apequaltowork/wagtail-school

Blog post (same story, in writing):
https://github.com/apequaltowork/wagtail-school/blob/main/blog/wagtail-2.7-to-7.4-everything-that-broke.md

The demo school, Kestrel Ridge College, is fictional. All people, numbers and images were made up for this project.

**Chapters**
0:00 Twenty-two things broke
0:21 The test site (Wagtail 2.7, 2019)
1:17 The baseline: how to prove nothing was lost
2:08 Hop 1: 2.7 → 2.15
3:07 Every enquiry form loses its data (clean_name)
5:48 Hop 2: 2.15 → 7.4
7:14 The migration that never came (StreamField)
8:27 Search logs deleted by migrate
9:10 Silent settings and the one visible break
10:33 The result
11:08 Checklist before you upgrade

**Tags**
wagtail, wagtail cms, wagtail upgrade, django, django upgrade, python, streamfield, wagtail 7, django 5, cms upgrade, legacy code, web development

**Captions**
Upload `out/upgrade.srt` as English subtitles.
