# -*- coding: utf-8 -*-
"""CSCE 606 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Version Control and Collaboration",
 "subtitle": "The tool everyone uses and few understand.",
 "question": "What is Git actually doing, and which workflow should you use?",
 "outcomes": [
     "Explain Git's object model and why it explains the commands.",
     "Use rebase, bisect, and reflog with confidence.",
     "Write commit messages that are useful years later.",
     "Compare branching strategies against team size and release cadence.",
     "Recover from the common disasters.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The object model",
   "blurb": "Four object types. Everything else follows."},

  {"t": "code", "kicker": "Objects", "title": "Git is a content-addressed store",
   "lang": "text", "code": """
BLOB    file contents            -- named by SHA of the contents
TREE    a directory listing      -- names -> blobs and trees
COMMIT  a tree + parent(s) + author + message
TAG     a named pointer to a commit

Everything is identified by the HASH OF ITS CONTENT.
Identical content stored twice is stored once.

A BRANCH is a 40-byte file containing a commit hash.
That is all a branch is. Creating one is free; deleting one
loses nothing but the name.

A COMMIT IS A SNAPSHOT, not a diff. Diffs are computed on
demand by comparing two trees.
""",
   "caption": "The snapshot-not-diff fact explains why branching is cheap, "
              "why history rewriting works, and why merges compare trees.",
   "note": "Most Git confusion dissolves once the object model is clear. It "
           "is worth twenty minutes."},

  {"t": "callout", "title": "Commits are immutable; branches move",
   "kind": "The key consequence",
   "body": ["A commit's hash covers its content <i>and its parent</i>. "
            "Change anything and you get a different commit with a different "
            "hash.",
            "So <code>rebase</code>, <code>amend</code>, and "
            "<code>cherry-pick</code> do not modify commits — they "
            "create new ones and move the branch pointer.",
            "<b>The old commits still exist</b>, unreferenced, until garbage "
            "collection runs — typically thirty days.",
            "This is why <code>git reflog</code> can recover almost any "
            "disaster: the commits are still there, and the reflog records "
            "where the branch pointed."]},

  {"t": "section", "label": "Part 2", "title": "The commands that matter",
   "blurb": "Three that people avoid and should not."},

  {"t": "table", "kicker": "Tools", "title": "Underused commands",
   "header": ["Command", "Does", "Use for"],
   "widths": [2.8, 4.4, 4.9],
   "rows": [
     ["<code>bisect</code>", "Binary search over history", "<b>Finding which commit broke it</b>"],
     ["<code>reflog</code>", "Where every branch has pointed", "Recovering from anything"],
     ["<code>rebase -i</code>", "Rewrite your own unpushed history", "Cleaning up before review"],
     ["<code>blame</code>", "Who last changed each line", "Finding the context, not the culprit"],
     ["<code>log -S</code>", "Commits that changed a string", "When was this introduced?"],
   ],
   "note": "bisect is the one with the biggest payoff relative to how rarely "
           "it is used."},

  {"t": "code", "kicker": "bisect", "title": "Finding the breaking commit in log n steps",
   "lang": "bash", "code": """
git bisect start
git bisect bad                 # current commit is broken
git bisect good v1.2.0         # this old tag was fine

# Git checks out the midpoint. Test it, then say which:
git bisect good    # or: git bisect bad

# Repeat. 1000 commits -> 10 steps.

# Or automate it entirely:
git bisect run ./test.sh       # exit 0 = good, non-zero = bad
""",
   "caption": "<code>bisect run</code> with a script that reproduces the bug "
              "will find the commit unattended. It is the highest-value "
              "underused tool in the course.",
   "note": "Emphasise that the test script need not be a real test — any "
           "reproducer with an exit code works."},

  {"t": "section", "label": "Part 3", "title": "Commit messages",
   "blurb": "Written for the person doing archaeology in three years."},

  {"t": "code", "kicker": "Messages", "title": "What makes a message useful later",
   "lang": "text", "code": """
BAD:   "fix bug"           -- which bug? what fix?
       "updates"           -- conveys nothing
       "address PR review" -- meaningless outside the PR

GOOD:
    Reject orders with a delivery date in the past

    The order form allowed any date, so backdated orders reached
    the warehouse queue and were silently skipped by the
    scheduler, which filters on date >= today.

    Validate at the API boundary rather than in the UI, since
    the mobile client posts directly.

    Fixes #1423.

SUBJECT: what changed, imperative, under ~50 chars.
BODY:    WHY. The diff already shows what.
""",
   "caption": "The diff shows what changed. The message must explain why "
              "— that is the information that is otherwise lost "
              "permanently.",
   "note": "The 'why' rule is the single highest-value habit here."},

  {"t": "callout", "title": "Write for the archaeologist",
   "kind": "The test",
   "body": ["In three years someone will run <code>git blame</code> on a "
            "line, find your commit, and need to know whether they can "
            "safely change it.",
            "They can read the diff. What they cannot recover is <b>why</b> "
            "— which constraint, which bug, which decision.",
            "<b>If the message does not tell them, that knowledge is "
            "gone.</b> There is no other record.",
            "This is the one piece of documentation that cannot rot, because "
            "it is attached permanently to the change it describes."]},

  {"t": "section", "label": "Part 4", "title": "Branching",
   "blurb": "The choice depends on how often you release."},

  {"t": "table", "kicker": "Strategies", "title": "Three strategies",
   "header": ["Strategy", "How", "Fits"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Trunk-based", "Everyone to main, many times a day; flags for incomplete work", "<b>Continuous delivery</b>"],
     ["GitHub flow", "Short branch, PR, merge, deploy", "Most teams"],
     ["Git flow", "develop, release, hotfix branches", "Versioned releases; <b>heavy</b>"],
   ],
   "note": "Git flow is widely used and widely wrong for teams shipping "
           "continuously — its author has said so."},

  {"t": "callout", "title": "Long-lived branches are the problem",
   "kind": "What the evidence says",
   "body": ["A branch that lives for weeks diverges. The merge is large, "
            "risky, and conflict-ridden — and the pain scales worse than "
            "linearly with branch lifetime.",
            "<b>DORA's finding:</b> high-performing teams integrate to "
            "trunk at least daily, with branches living less than a day.",
            "The objection is obvious: what about work that takes a week? "
            "<b>Answer: feature flags.</b> Merge incomplete work, disabled, "
            "and integrate continuously.",
            "Which means 'how do I avoid merge hell' and 'how do I deploy "
            "safely' have the same answer. Module 10 develops it."]},

  {"t": "bullets", "kicker": "Recovery", "title": "Getting out of trouble",
   "items": [
     "<b>Committed to the wrong branch:</b> <code>git reset HEAD~</code>, "
     "switch, recommit.",
     "<b>Deleted a branch:</b> <code>git reflog</code>, find the hash, "
     "<code>git branch name hash</code>.",
     "<b>Bad rebase:</b> <code>git reflog</code>, reset to the pre-rebase "
     "state.",
     "<b>Committed a secret:</b> <b>rotate the secret</b>. Rewriting history "
     "does not help — assume it is public.",
     "",
     "<b>Nearly everything is recoverable</b> for thirty days via reflog. "
     "The exception is uncommitted work.",
   ],
   "footnote": "Commit early. Uncommitted work is the only kind Git cannot "
               "recover."},
 ],
 "takeaways": [
   "Git stores blobs, trees, commits, and tags, all content-addressed. A "
   "commit is a snapshot, not a diff.",
   "A branch is a file containing a hash. Commits are immutable; rebase "
   "creates new ones and moves the pointer.",
   "The old commits survive for ~30 days, which is why reflog recovers almost "
   "any disaster.",
   "<code>bisect run</code> finds a breaking commit in log n steps, "
   "unattended. It is the most underused high-value command.",
   "The diff shows what changed; the commit message must explain why. That "
   "knowledge has no other record.",
   "Long-lived branches are the problem, not the merge tool. Integrate daily "
   "and use feature flags for incomplete work.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The object model"),
  ("p", "Most confusion about Git comes from learning commands without the "
        "model underneath. The model is small — four object types "
        "— and understanding it makes the commands follow."),
  ("table", ["Object", "Contains", "Identified by"],
   [["<b>Blob</b>", "File contents. No name, no permissions.",
     "SHA-1 of its contents."],
    ["<b>Tree</b>", "A directory listing: names mapped to blobs and other "
     "trees, with modes.", "SHA-1 of the listing."],
    ["<b>Commit</b>", "A root tree, parent commit(s), author, committer, "
     "timestamp, message.", "SHA-1 of all of that."],
    ["<b>Tag</b>", "A named, annotated pointer to a commit.", "SHA-1."]],
   [0.15, 0.55, 0.30]),
  ("p", "Everything is <b>content-addressed</b>: the name of an object is the "
        "hash of its content. Two identical files anywhere in history are "
        "stored once. Two commits with identical trees share the tree."),
  ("callout", "A commit is a snapshot, not a diff",
   ["This surprises people coming from older systems. A commit references a "
    "complete tree of the project at that moment, not a set of changes.",
    "Diffs are <i>computed</i> on demand by comparing two trees. This is why "
    "Git can show a diff between any two commits instantly without walking "
    "the history between them, and why merging compares trees rather than "
    "replaying patches.",
    "<b>A branch is a file containing a 40-character hash.</b> That is all. "
    "Creating a branch writes 41 bytes; deleting one removes a name and "
    "nothing else. This is why Git branching is cheap when branching in older "
    "systems was an event."]),
  ("callout", "Commits are immutable; branches move",
   ["A commit's hash is computed over its content <i>including its parent "
    "hash</i>. Change anything — the message, a file, the parent "
    "— and the result is a different commit with a different hash.",
    "So <code>rebase</code>, <code>commit --amend</code>, and "
    "<code>cherry-pick</code> never modify a commit. They create new commits "
    "and move a branch pointer to them.",
    "<b>The original commits still exist</b>, now unreferenced, until garbage "
    "collection removes them — by default after about thirty days.",
    "This is precisely why <code>git reflog</code> can rescue you from almost "
    "anything: the commits were never deleted, and the reflog records every "
    "position each branch has held."]),

  ("h1", "2 &nbsp; The commands worth learning properly"),
  ("table", ["Command", "What it does", "When"],
   [["<code>git bisect</code>", "Binary search through history for the "
     "commit that introduced a behaviour.",
     "<b>Any time you know it worked before and does not now.</b>"],
    ["<code>git reflog</code>", "Shows every position every branch and HEAD "
     "has occupied locally.", "Recovering from any mistake."],
    ["<code>git rebase -i</code>", "Rewrite a sequence of your own commits: "
     "reorder, squash, edit, drop.",
     "Cleaning up a messy branch before review. <b>Never on shared "
     "history.</b>"],
    ["<code>git blame</code>", "Last commit to touch each line.",
     "Finding the <i>context</i> for a line — the name is unfortunate, "
     "the purpose is archaeology."],
    ["<code>git log -S'text'</code>", "Commits where the number of "
     "occurrences of a string changed.",
     "'When was this introduced?' and 'where did this constant come from?'"]],
   [0.20, 0.42, 0.38]),
  ("code", """git bisect start
git bisect bad                  # HEAD is broken
git bisect good v1.2.0          # this release was fine
# Git checks out the midpoint; test it and report:
git bisect good                 # or: git bisect bad
# ... repeat. 1000 commits -> ~10 steps.

# Or fully automated:
git bisect run ./reproduce.sh   # exit 0 = good, non-zero = bad"""),
  ("p", "<code>bisect run</code> is the highest-value underused tool in "
        "everyday practice. The script does not need to be a real test "
        "— anything that reproduces the problem and exits with a status "
        "will do. Set it going and it will identify the commit while you do "
        "something else."),

  ("break",),
  ("h1", "3 &nbsp; Commit messages"),
  ("code", """Reject orders with a delivery date in the past

The order form accepted any date, so backdated orders reached the
warehouse queue and were silently dropped by the scheduler, which
filters on date >= today. Users saw "order placed" and nothing
arrived.

Validation is at the API boundary rather than in the form,
because the mobile client posts directly to the API.

Fixes #1423."""),
  ("table", ["Part", "Rule"],
   [["Subject", "What changed, in the imperative mood, under about 50 "
     "characters. 'Reject orders&hellip;' not 'Rejected' or 'Rejects'. It "
     "completes the sentence 'If applied, this commit will&hellip;'"],
    ["Blank line", "Required. Tooling treats the first line specially."],
    ["Body", "<b>Why.</b> The diff already shows what. Explain the problem, "
     "the constraint, the rejected alternative."],
    ["Footer", "Issue references, co-authors, breaking-change notes."]],
   [0.17, 0.83]),
  ("callout", "Write for the archaeologist",
   ["In three years, someone will run <code>git blame</code> on a line of "
    "code, land on your commit, and need to decide whether the line can "
    "safely be changed.",
    "They can read the diff perfectly well. What they cannot reconstruct is "
    "<b>why</b> — which bug prompted it, which constraint forced the "
    "odd approach, which obvious alternative was tried and failed.",
    "<b>If your message does not record that, the knowledge is gone.</b> "
    "There is no other durable record: the ticket may be in a system that has "
    "been replaced, the discussion was in a chat that has been purged, and "
    "the people have left.",
    "This is the only documentation that cannot rot, because it is attached "
    "permanently and immutably to the change it describes. 'Address PR "
    "feedback' as a message throws that away."]),

  ("h1", "4 &nbsp; Branching strategies"),
  ("table", ["Strategy", "Mechanics", "Suits"],
   [["<b>Trunk-based</b>", "Everyone commits to main, multiple times daily. "
     "Incomplete work is hidden behind feature flags. Releases are tags or "
     "short-lived release branches.",
     "<b>Continuous delivery.</b> The practice DORA associates with the "
     "highest-performing teams."],
    ["<b>GitHub flow</b>", "Branch from main, open a pull request, review, "
     "merge, deploy. Branches live hours to days.",
     "Most teams, most of the time. Simple and adequate."],
    ["<b>Git flow</b>", "Permanent <code>develop</code> and "
     "<code>main</code>, plus feature, release, and hotfix branch types with "
     "prescribed merge directions.",
     "Software with versioned releases supported in parallel — "
     "installed products, libraries with long-term support branches. "
     "<b>Substantial ceremony</b>, and its author has since written that it "
     "is poorly suited to continuously delivered web applications."]],
   [0.17, 0.44, 0.39]),
  ("callout", "The problem is branch lifetime, not the merge tool",
   ["A branch that lives three weeks diverges from main for three weeks. The "
    "resulting merge is large, unfamiliar, and conflict-ridden — and the "
    "difficulty grows worse than linearly with the branch's age, because "
    "conflicts interact.",
    "<b>DORA's consistent finding is that high-performing teams integrate to "
    "trunk at least daily</b>, with branches typically living less than a "
    "day. This correlates with both faster delivery and greater stability "
    "— which is not the trade-off people expect.",
    "The obvious objection is work that takes a week to complete. <b>The "
    "answer is feature flags:</b> merge the incomplete work in a disabled "
    "state, integrate continuously, and enable it when it is ready.",
    "So 'how do I avoid merge hell' and 'how do I deploy safely' turn out to "
    "have the same answer. Module 10 develops it."]),

  ("h1", "5 &nbsp; Recovery"),
  ("table", ["Situation", "Recovery"],
   [["Committed to the wrong branch.",
     "<code>git reset HEAD~</code> (keeps the changes), switch branch, "
     "commit again."],
    ["Deleted a branch you needed.",
     "<code>git reflog</code>, find the last commit hash, "
     "<code>git branch &lt;name&gt; &lt;hash&gt;</code>."],
    ["A rebase went wrong.",
     "<code>git reflog</code>, find the pre-rebase position, "
     "<code>git reset --hard &lt;hash&gt;</code>."],
    ["Committed a large file by accident.",
     "If unpushed, amend or rebase it out. If pushed, "
     "<code>git filter-repo</code> and a coordinated force-push."],
    ["<b>Committed a secret.</b>",
     "<b>Rotate the secret.</b> Immediately. Rewriting history does not "
     "help: it was pushed, it may be cloned, forked, cached by the host, or "
     "indexed. Treat it as public, because it is."]],
   [0.34, 0.66]),
  ("p", "Almost everything is recoverable for about thirty days through the "
        "reflog. The exception is work that was never committed, which Git "
        "has no record of. <b>Commit early and often</b>; a messy history can "
        "be cleaned up with interactive rebase before review, and lost work "
        "cannot be cleaned up at all."),
 ],
 "resources": [
   ("Pro Git (free book)",
    "https://git-scm.com/book/en/v2",
    "Chapter 10 ('Git Internals') is the one that makes everything else make "
    "sense. Read it before the command chapters."),
   ("Git from the Bottom Up (free)",
    "https://jwiegley.github.io/git-from-the-bottom-up/",
    "Builds the model from the object store upward. Short, and the best "
    "explanation of why rebase works the way it does."),
   ("Conventional Commits",
    "https://www.conventionalcommits.org/",
    "A structured message format that enables automated changelogs and "
    "version bumping. Useful when adopted consistently."),
   ("DORA — trunk-based development",
    "https://dora.dev/capabilities/trunk-based-development/",
    "The evidence behind &sect;4's claim about branch lifetime."),
 ],
 "exercises": [
   "Explore the object store directly: commit a file, then use "
   "<code>git cat-file -p</code> to walk from the commit to its tree to the "
   "blob. Confirm the blob's hash is the hash of the contents.",
   "Create a branch, make commits, delete the branch, then recover it using "
   "<code>git reflog</code>.",
   "Introduce a bug ten commits back in a test repository, then find it with "
   "<code>git bisect</code>. Then automate it with <code>bisect run</code>.",
   "Take a branch with five messy commits and clean it with "
   "<code>git rebase -i</code>: squash, reorder, and rewrite the messages.",
   "Find a commit in a real open-source project whose message explains "
   "<i>why</i>. Find one that does not. Assess how much harder the second "
   "makes a hypothetical change.",
   "Measure branch lifetime in a project you can see: for twenty merged pull "
   "requests, record the time between first commit and merge, and plot it "
   "against the number of conflicts.",
   "Deliberately create a merge conflict, resolve it, and then examine what "
   "Git recorded about the resolution.",
 ],
 "selfcheck": [
   "Name Git's four object types and say what identifies each.",
   "Why is a commit a snapshot rather than a diff, and what two things does "
   "that explain?",
   "Why does rebase not modify commits, and why does reflog work?",
   "What does <code>git bisect run</code> do, and why is it underused?",
   "What must a commit message contain that the diff cannot provide?",
   "Why are long-lived branches the problem, and what makes short ones "
   "possible for week-long work?",
   "What is the one thing Git cannot recover, and what should you do about a "
   "committed secret?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Code Review",
 "subtitle": "The highest-leverage practice, done badly almost everywhere.",
 "question": "What is review for, and how do you do it without damage?",
 "outcomes": [
     "State what review is actually for, in priority order.",
     "Review effectively: what to look for and what to ignore.",
     "Give feedback that improves code without damaging people.",
     "Size changes so review is possible.",
     "Explain what the evidence says about review effectiveness.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What review is for",
   "blurb": "Finding bugs is on the list and is not first."},

  {"t": "table", "kicker": "Purposes", "title": "In order of actual value",
   "header": ["Purpose", "Why it matters"],
   "widths": [4.0, 8.1],
   "rows": [
     ["<b>Knowledge sharing</b>", "No code known by only one person. Survives departures"],
     ["<b>Maintainability</b>", "A second reader proves it is comprehensible"],
     ["<b>Design feedback</b>", "The cheapest point to change an approach"],
     ["Correctness", "Found, but tests find more"],
     ["Consistency", "<b>Automate this</b> — do not spend review on it"],
     ["Mentoring", "Both directions"],
   ],
   "note": "Putting knowledge sharing first reframes review from gatekeeping "
           "to teaching, which changes how people do it."},

  {"t": "callout", "title": "If a human is checking formatting, you have failed",
   "kind": "Automate the mechanical",
   "body": ["Formatting, import order, naming conventions, lint rules, "
            "obvious bugs — all machine-checkable.",
            "Every comment a human writes about these is attention not spent "
            "on design, correctness, or clarity — which only a human can "
            "assess.",
            "<b>Run the formatter and the linter in CI and make them "
            "blocking.</b> Then the argument is settled once, in "
            "configuration, rather than per pull request forever.",
            "The style debate is not worth having repeatedly. Pick something "
            "defensible, automate it, and never discuss it again."]},

  {"t": "section", "label": "Part 2", "title": "Reviewing well",
   "blurb": "In order, because order matters."},

  {"t": "bullets", "kicker": "Order", "title": "What to look at, in sequence",
   "items": [
     "<b>1. Should this exist?</b> Does it solve the right problem? Cheapest "
     "to catch here.",
     "<b>2. Is the approach right?</b> Design, boundaries, whether it fits "
     "the system.",
     "<b>3. Is it correct?</b> Edge cases, error paths, concurrency.",
     "<b>4. Is it tested?</b> Do the tests test behaviour (Module 05)?",
     "<b>5. Is it readable?</b> Will someone understand this in two years?",
     "<b>6. Mechanical.</b> <b>The machine does this.</b>",
     "",
     "Reviewing bottom-up wastes effort on code that should not exist.",
   ],
   "note": "The ordering is the actionable content — people naturally "
           "start at 6 because it is easiest."},

  {"t": "callout", "title": "Review size determines review quality",
   "kind": "The best-supported finding",
   "body": ["Defect detection falls sharply with change size. Beyond roughly "
            "400 lines, reviewers stop finding problems — the review "
            "becomes a skim and an approval.",
            "<b>A 2,000-line pull request does not get four times the "
            "scrutiny of a 500-line one. It gets less in total.</b>",
            "<b>Under 200 lines</b> is where review is genuinely effective.",
            "So the author's responsibility is to make review possible: split "
            "the change, separate refactoring from behaviour (Module 07), and "
            "land groundwork separately."]},

  {"t": "bullets", "kicker": "Author", "title": "The author's obligations",
   "items": [
     "<b>Keep it small.</b> Several small pull requests beat one large one, "
     "every time.",
     "",
     "<b>Separate refactoring from behavioural change.</b> Mixed diffs are "
     "unreviewable.",
     "",
     "<b>Write the description</b>: what, why, how to verify, what you are "
     "unsure about.",
     "",
     "<b>Review your own diff first.</b> You will find things, and it is "
     "cheaper when you do.",
     "",
     "<b>Say where you want scrutiny.</b> 'The locking in handler.rs is the "
     "risky part' directs attention usefully.",
   ],
   "footnote": "Self-review before requesting review catches a surprising "
               "share of comments."},

  {"t": "section", "label": "Part 3", "title": "Feedback",
   "blurb": "The part that determines whether review is sustainable."},

  {"t": "table", "kicker": "Feedback", "title": "Phrasing that works",
   "header": ["Instead of", "Write"],
   "widths": [5.4, 6.7],
   "rows": [
     ["'This is wrong.'", "'What happens if items is empty here?'"],
     ["'Why would you do it this way?'", "'Have you considered X? It would avoid Y.'"],
     ["'Bad naming.'", "'I read <i>count</i> as a total — is it a limit?'"],
     ["'Needs tests.'", "'Could we add a test for the timeout path?'"],
     ["'nit: spacing'", "<b>Nothing — the formatter handles it</b>"],
   ],
   "note": "Questions outperform assertions because they are often answered "
           "— the author knows something you do not."},

  {"t": "callout", "title": "Ask questions rather than issue verdicts",
   "kind": "Why it works",
   "body": ["A question invites an explanation. Frequently the answer is "
            "good, and you have learned something — the author had "
            "context you lacked.",
            "A verdict invites defence. Now it is a contest, and the "
            "code does not improve.",
            "<b>And questions are honest:</b> a reviewer reading a diff "
            "genuinely has less context than the author who has been in it "
            "for days.",
            "<b>Review the code, never the person.</b> 'This function does "
            "X' not 'you did X'. The difference is small in text and large in "
            "effect."]},

  {"t": "bullets", "kicker": "Calibration", "title": "Three levels of comment",
   "items": [
     "<b>Blocking:</b> correctness, security, data loss, a design problem "
     "that will be expensive later. Say so explicitly.",
     "",
     "<b>Suggestion:</b> an improvement the author may take or not. Mark it "
     "<code>nit:</code> or <code>optional:</code>.",
     "",
     "<b>Question:</b> you do not understand something. Often the most "
     "valuable — if you cannot follow it, nor will the next reader.",
     "",
     "<b>Label them.</b> An unlabelled suggestion reads as a demand, and "
     "authors rewrite things they did not need to.",
   ],
   "footnote": "Unlabelled comments are the main cause of review friction."},

  {"t": "callout", "title": "Perfect is not the bar",
   "kind": "The standard",
   "body": ["Google's rule: <b>approve when the change definitely improves "
            "the codebase</b>, even if it is not perfect.",
            "Holding out for perfection blocks progress, exhausts authors, "
            "and — crucially — encourages larger changes, since "
            "each round trip is expensive.",
            "<b>Approve with comments</b> for non-blocking suggestions. The "
            "author decides.",
            "A review culture where approval is rare produces fewer, larger, "
            "worse-reviewed changes. The incentives have to point the right "
            "way."]},

  {"t": "bullets", "kicker": "Evidence", "title": "What is actually known",
   "items": [
     "<b>Review finds defects</b> — well supported, though estimates "
     "vary widely.",
     "",
     "<b>Size dominates everything</b> — the strongest and most "
     "consistent finding.",
     "",
     "<b>Knowledge transfer is real</b> and is probably the larger benefit.",
     "",
     "<b>Two reviewers add little</b> over one in most studies.",
     "",
     "<b>Review is not a substitute for testing.</b> They find different "
     "things.",
   ],
   "footnote": "The size finding is the one to act on."},
 ],
 "takeaways": [
   "Review's biggest value is knowledge sharing and maintainability. Finding "
   "bugs is real and secondary.",
   "Automate everything mechanical. A human commenting on formatting is "
   "attention wasted on something a machine does better.",
   "Review in order: should it exist, is the approach right, is it correct, "
   "is it tested, is it readable. Bottom-up wastes effort.",
   "Defect detection collapses above ~400 lines. Keeping changes small is the "
   "author's job and the best-supported finding in the field.",
   "Ask questions rather than issue verdicts — the author usually has "
   "context you lack, and a question invites explanation.",
   "Approve when the change improves the codebase. A culture of rare approval "
   "produces larger, worse changes.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What review is for"),
  ("table", ["Purpose", "Value"],
   [["<b>Knowledge sharing</b>",
     "After review, at least two people understand the change. This is how a "
     "team avoids code that only one person can maintain, and it is what "
     "makes departures survivable. Probably the largest benefit."],
    ["<b>Maintainability</b>",
     "A second reader is empirical evidence that the code can be understood "
     "by someone who did not write it — which is the condition Module 01 "
     "identified as determining lifetime cost."],
    ["<b>Design feedback</b>",
     "The cheapest moment to change an approach is before it has been built "
     "on. After merge the cost rises steeply."],
    ["<b>Correctness</b>",
     "Review does find defects. Tests find more, and find them repeatedly and "
     "automatically."],
    ["<b>Consistency</b>",
     "Real, and almost entirely automatable. See below."],
    ["<b>Mentoring</b>",
     "In both directions. A junior reviewing senior code learns the codebase "
     "faster than by reading it alone."]],
   [0.22, 0.78]),
  ("callout", "Automate everything mechanical",
   ["Formatting, import ordering, naming conventions, lint rules, unused "
    "variables, obvious null dereferences — a machine checks all of "
    "these faster, more consistently, and without anyone's feelings being "
    "involved.",
    "Every human comment spent on them is attention not spent on design, "
    "correctness, or clarity, which are the things only a human can assess.",
    "<b>Run the formatter and the linter in CI and make them blocking.</b> "
    "Then the style question is settled once, in a configuration file, rather "
    "than renegotiated in every pull request forever.",
    "Which formatter does not matter. Pick a defensible default, commit the "
    "configuration, and decline to discuss it again. The time saved by not "
    "having that argument repeatedly exceeds any benefit from winning it."]),

  ("h1", "2 &nbsp; Reviewing well"),
  ("p", "Review in this order. The ordering matters because effort spent at "
        "the bottom is wasted if something at the top is wrong."),
  ("ol", ["<b>Should this change exist?</b> Does it solve the right problem? "
          "Is the problem worth solving? Is there a simpler approach that "
          "makes it unnecessary? This is the cheapest possible place to catch "
          "a misdirected effort, and the most expensive place to miss one.",
          "<b>Is the approach right?</b> Does it fit the system's existing "
          "structure? Does it put responsibility in the right place "
          "(Module 03)? Does it introduce coupling that will be expensive?",
          "<b>Is it correct?</b> Edge cases, boundary values, error paths, "
          "concurrency, resource cleanup. Use Module 06's partitioning as a "
          "checklist.",
          "<b>Is it adequately tested?</b> Not 'are there tests' but do the "
          "tests test <i>behaviour</i> (Module 05), and do they cover the "
          "cases that worry you?",
          "<b>Is it readable?</b> Will someone encountering this in two years "
          "understand it? If you had to reread a section three times, say so "
          "— that is data.",
          "<b>Mechanical issues.</b> <b>The machine does this.</b> If you are "
          "here, something is misconfigured."]),
  ("callout", "Change size is the dominant variable",
   ["This is the best-supported empirical finding about code review, and it "
    "is consistently ignored.",
    "Defect detection rates fall sharply as change size grows. Beyond roughly "
    "400 lines, reviewers find very little — the review becomes a skim "
    "followed by an approval, because sustained careful attention does not "
    "extend that far.",
    "<b>A 2,000-line pull request does not receive four times the scrutiny of "
    "a 500-line one. It receives less scrutiny in total</b>, because the "
    "reviewer disengages.",
    "Under 200 lines is where review is genuinely effective. This makes "
    "keeping changes small primarily the <b>author's</b> responsibility, and "
    "it is the single most useful thing an author can do for review quality."]),
  ("h2", "2.1 &nbsp; What the author owes the reviewer"),
  ("ul", ["<b>Keep it small.</b> Several small pull requests reviewed "
          "properly beat one large one approved without reading.",
          "<b>Separate refactoring from behavioural change</b> (Module 07). A "
          "diff mixing a rename across forty files with a logic change is "
          "unreviewable: the logic change is invisible in the noise.",
          "<b>Write the description.</b> What changed, why, how to verify it, "
          "and what you are uncertain about. The reviewer has a fraction of "
          "your context.",
          "<b>Review your own diff first.</b> Reading your change as a diff "
          "rather than as an edit surfaces a surprising number of problems, "
          "and finding them yourself is cheaper than a round trip.",
          "<b>Direct attention.</b> 'The locking in <code>handler.rs</code> is "
          "the part I am least sure about' is worth more than any amount of "
          "general politeness."]),

  ("break",),
  ("h1", "3 &nbsp; Giving feedback"),
  ("p", "This determines whether a review culture is sustainable. Reviews "
        "that feel like attacks produce defensive authors, larger batches to "
        "reduce exposure, and eventually rubber-stamping."),
  ("table", ["Instead of", "Write", "Because"],
   [["'This is wrong.'", "'What happens if <code>items</code> is empty?'",
     "The specific question is actionable, and may have an answer."],
    ["'Why would you do it this way?'",
     "'Have you considered X? It would avoid Y.'",
     "The first reads as an accusation; the second as a contribution."],
    ["'Bad variable name.'",
     "'I read <code>count</code> as a running total — is it actually a "
     "limit?'",
     "Reports the confusion, which is the evidence, rather than issuing a "
     "verdict."],
    ["'Needs tests.'", "'Could we add a case for the timeout path?'",
     "Specific and immediately actionable."],
    ["'nit: inconsistent spacing'", "<b>Nothing.</b>",
     "The formatter handles it. If it is not handled, fix the configuration, "
     "not the pull request."]],
   [0.24, 0.40, 0.36]),
  ("callout", "Questions outperform verdicts, and are more honest",
   ["A question invites an explanation. Often the explanation is good, and "
    "the reviewer has learned something: the author spent days in this code "
    "and has context the reviewer does not.",
    "A verdict invites defence. The exchange becomes about who is right, and "
    "the code does not improve while that is being settled.",
    "The honesty point matters independently. A reviewer reading a diff for "
    "ten minutes genuinely knows less than the author. Phrasing as a question "
    "reflects the actual epistemic position rather than performing "
    "politeness.",
    "<b>Review the code, never the person.</b> 'This function allocates on "
    "every call' rather than 'you allocate on every call'. The difference is "
    "trivial in text and substantial in how it is received — and it "
    "costs nothing."]),
  ("h2", "3.1 &nbsp; Calibrate every comment"),
  ("table", ["Level", "Meaning", "How to mark it"],
   [["<b>Blocking</b>", "Correctness, security, data loss, or a design "
     "problem that will be expensive to undo.",
     "State it plainly: 'This needs to change before merge, because&hellip;'"],
    ["<b>Suggestion</b>", "An improvement the author may take or leave.",
     "Prefix <code>nit:</code> or <code>optional:</code>. Mean it — if "
     "it is not optional, do not label it so."],
    ["<b>Question</b>", "You do not understand something.",
     "Ask. These are often the most valuable comments: if you cannot follow "
     "it after ten minutes, the next reader will not either."]],
   [0.17, 0.43, 0.40]),
  ("p", "<b>Label every comment.</b> An unlabelled suggestion reads as a "
        "requirement, and authors rewrite perfectly good code to satisfy a "
        "preference nobody intended to impose. This single habit removes most "
        "review friction."),
  ("callout", "The approval standard",
   ["Google's documented rule: <b>approve when the change definitely improves "
    "the overall health of the codebase, even if it is not perfect.</b>",
    "Holding out for perfection blocks progress, exhausts authors, and — "
    "most damagingly — incentivises larger changes. If each review round "
    "trip costs two days, authors batch work to reduce the number of round "
    "trips, which makes review less effective, which makes reviewers more "
    "anxious, which makes them stricter.",
    "<b>Approve with comments</b> for anything non-blocking and let the "
    "author decide. A culture where approval is rare and hard-won produces "
    "fewer, larger, more poorly reviewed changes — the opposite of what "
    "the strictness was for."]),

  ("h1", "4 &nbsp; What the evidence supports"),
  ("table", ["Claim", "Status"],
   [["Code review finds defects.",
     "<b>Well supported</b>, though estimates of how many vary enormously "
     "across studies and contexts."],
    ["Review effectiveness falls sharply with change size.",
     "<b>The strongest and most consistent finding.</b> Act on this one."],
    ["Knowledge transfer is a major benefit, possibly the largest.",
     "Well supported by practitioner studies and consistent with how teams "
     "report using it."],
    ["A second reviewer adds substantial value over the first.",
     "<b>Weakly supported.</b> Most studies find sharply diminishing returns "
     "after one careful reviewer."],
    ["Review substitutes for testing.",
     "<b>No.</b> They detect different categories of problem, and review does "
     "not repeat itself automatically on every future change."]],
   [0.42, 0.58]),
 ],
 "resources": [
   ("Google's Code Review Developer Guide (free)",
    "https://google.github.io/eng-practices/review/",
    "The best free material on this, from both the reviewer's and the "
    "author's side. The 'approve when it improves things' standard comes from "
    "here."),
   ("Software Engineering at Google — Chapter 9 (Code Review)",
    "https://abseil.io/resources/swe-book",
    "Why they review, what they found it actually buys, and the data behind "
    "it."),
   ("SmartBear — Best Kept Secrets of Peer Code Review (free summary)",
    "https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/",
    "The source of the frequently cited size and duration findings."),
   ("Conventional Comments",
    "https://conventionalcomments.org/",
    "A light convention for labelling comments by type and severity. Adopting "
    "it removes most review friction for free."),
 ],
 "exercises": [
   "Review an open pull request in a project you do not maintain. Write the "
   "review privately first, then compare against the actual reviewers' "
   "comments. What did you miss, and what did they miss?",
   "Take one of your own changes larger than 500 lines and split it into "
   "pull requests of under 200 lines each, in a sensible order. Record how "
   "long it took and whether the split revealed anything.",
   "Review your own last five commits as diffs rather than as remembered "
   "edits. Record what you find.",
   "Take five review comments you have written or received and reclassify "
   "each as blocking, suggestion, or question. Rewrite any that were "
   "miscalibrated.",
   "Configure a formatter and linter for a project and make them blocking in "
   "CI. Count the review comments they would have made unnecessary over the "
   "last twenty pull requests.",
   "Find a review conversation in an open-source project that went badly. "
   "Identify the specific comment that escalated it and rewrite it.",
   "Measure review latency in a project you can observe: time from pull "
   "request opened to first substantive comment, plotted against change size.",
 ],
 "selfcheck": [
   "What is code review's largest benefit, and where does defect-finding "
   "rank?",
   "Why should mechanical issues never appear in human review comments?",
   "List the six things to look at in review, in order, and say why the order "
   "matters.",
   "What happens to defect detection above 400 lines, and whose "
   "responsibility is change size?",
   "Give two reasons questions work better than verdicts in review.",
   "What are the three comment levels, and what goes wrong if they are "
   "unlabelled?",
   "What is the approval standard, and what does a culture of rare approval "
   "produce?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Continuous Integration and Delivery",
 "subtitle": "Making release boring.",
 "question": "How do you deploy frequently without breaking things?",
 "outcomes": [
     "Explain what CI actually requires beyond running tests.",
     "Design a pipeline with the right stages in the right order.",
     "Explain feature flags and why they enable trunk-based development.",
     "Compare deployment strategies and their rollback properties.",
     "Explain the DORA metrics and what they measure.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What CI actually is",
   "blurb": "Not a server that runs tests."},

  {"t": "callout", "title": "CI is a practice, not a tool",
   "kind": "The common misunderstanding",
   "body": ["'We have CI' usually means 'we have a server that runs tests on "
            "pull requests'. That is useful and it is not continuous "
            "integration.",
            "<b>Continuous integration means everyone integrates their work "
            "into the mainline at least daily.</b>",
            "A team with a build server and three-week branches does not have "
            "CI. They have a test runner and deferred integration pain.",
            "The point is that integration problems are found when they are "
            "small and attributable to one small change — which requires "
            "integrating often, not owning a server."]},

  {"t": "bullets", "kicker": "Requirements", "title": "What CI requires",
   "items": [
     "<b>A single mainline</b> everyone integrates into.",
     "<b>Integrate at least daily.</b> This is the actual practice.",
     "<b>Every integration triggers an automated build and test.</b>",
     "<b>A broken build is fixed immediately</b> — it is the highest "
     "priority for whoever broke it.",
     "<b>The build is fast</b> — under ten minutes, or people stop "
     "waiting for it.",
     "",
     "The culture item — fix the build now — is the one teams skip, "
     "and it is the one that matters.",
   ],
   "note": "A tolerated broken build destroys the whole practice: if it is "
           "normally red, nobody looks."},

  {"t": "callout", "title": "A permanently red build is worse than none",
   "kind": "Why the discipline matters",
   "body": ["If the build is usually broken, nobody checks it. A genuine "
            "failure is indistinguishable from the ambient noise.",
            "Worse, people learn to merge on red, so the signal is not just "
            "ignored — it is actively worked around.",
            "This is the flaky test problem of Module 05, at the level of the "
            "whole pipeline, and the fix is the same: <b>a red build stops "
            "other work until it is green</b>.",
            "Teams that find this intolerable usually have a build that is "
            "too slow or too flaky. Fix that; do not relax the rule."]},

  {"t": "section", "label": "Part 2", "title": "The pipeline",
   "blurb": "Fast and cheap first."},

  {"t": "table", "kicker": "Stages", "title": "Order by speed, fail early",
   "header": ["Stage", "Time", "Catches"],
   "widths": [3.4, 2.6, 6.1],
   "rows": [
     ["Lint, format, types", "Seconds", "Mechanical problems"],
     ["Small tests", "<b>Under a minute</b>", "Logic errors"],
     ["Build artefacts", "Minutes", "Compilation, packaging"],
     ["Medium tests", "Minutes", "Component integration"],
     ["Large tests", "Minutes", "<b>Whether it works</b>"],
     ["Deploy to staging", "Minutes", "Deployment mechanics"],
     ["Smoke tests", "Seconds", "Did it come up?"],
   ],
   "footnote": "Each stage is cheaper than the next. Fail at the earliest "
               "possible point.",
   "note": "The ordering is an economics argument: fail cheap before failing "
           "expensive."},

  {"t": "bullets", "kicker": "Speed", "title": "Keeping the pipeline fast",
   "items": [
     "<b>Ten minutes is the threshold.</b> Beyond it, people context-switch "
     "and stop treating failures as urgent.",
     "",
     "<b>Parallelise.</b> Test suites usually shard trivially.",
     "<b>Cache dependencies.</b> Resolving them every run is pure waste.",
     "<b>Run only what changed</b> where the build system supports it.",
     "<b>Move slow tests off the critical path</b> — run nightly, not "
     "per commit.",
     "",
     "A slow pipeline is not an inconvenience; it changes behaviour, and all "
     "the changes are bad.",
   ]},

  {"t": "section", "label": "Part 3", "title": "Feature flags",
   "blurb": "Separating deploy from release."},

  {"t": "callout", "title": "Deploy and release become different events",
   "kind": "The key idea",
   "body": ["Without flags, deploying code means releasing the feature. So "
            "incomplete work cannot be merged, so branches live for weeks "
            "(Module 08).",
            "<b>With flags, you deploy code that is disabled.</b> The feature "
            "is released later by changing a configuration value, with no "
            "deployment.",
            "This unlocks trunk-based development, canary releases, A/B "
            "tests, and instant rollback — turning off a flag is faster "
            "and safer than deploying a revert.",
            "<b>The cost is real:</b> every flag is a branch in the code and "
            "doubles the state space. Flags must be removed once the decision "
            "is made."]},

  {"t": "table", "kicker": "Flags", "title": "Four kinds, with different lifetimes",
   "header": ["Kind", "Purpose", "Lifetime"],
   "widths": [2.6, 5.0, 4.5],
   "rows": [
     ["Release", "Hide incomplete work", "<b>Days — then delete</b>"],
     ["Experiment", "A/B test", "Weeks — then delete"],
     ["Ops", "Kill switch; degrade under load", "Permanent, deliberately"],
     ["Permission", "Entitlement by plan or role", "Permanent — arguably not a flag"],
   ],
   "note": "Release flags that are not deleted are the main source of flag "
           "debt."},

  {"t": "section", "label": "Part 4", "title": "Deployment",
   "blurb": "Strategies, judged by how fast you can undo them."},

  {"t": "table", "kicker": "Strategies", "title": "Four ways to deploy",
   "header": ["Strategy", "How", "Rollback"],
   "widths": [2.6, 5.0, 4.5],
   "rows": [
     ["Big bang", "Stop, replace, start", "Redeploy the old version — slow"],
     ["Rolling", "Replace instances gradually", "Roll forward or back gradually"],
     ["Blue/green", "Two environments; switch traffic", "<b>Switch back — instant</b>"],
     ["Canary", "Small share first, watch, expand", "<b>Stop and revert — small blast radius</b>"],
   ],
   "note": "Canary plus flags is the combination that makes deployment "
           "genuinely low-risk."},

  {"t": "callout", "title": "Rollback speed is the thing that matters",
   "kind": "The design criterion",
   "body": ["You cannot prevent all bad deployments. You can make them cheap "
            "to undo.",
            "A system you can roll back in thirty seconds tolerates a much "
            "higher deployment rate than one that takes an hour — and "
            "higher deployment rate means smaller changes, which means fewer "
            "failures.",
            "<b>Database migrations are the hard part</b>, because they are "
            "often not reversible. The discipline is "
            "<b>expand/contract</b>: add the new column, write both, migrate, "
            "read new, then remove the old — each step independently "
            "reversible.",
            "Never deploy a migration and the code depending on it in the "
            "same release."]},

  {"t": "bullets", "kicker": "DORA", "title": "The four metrics worth tracking",
   "items": [
     "<b>Deployment frequency</b> — how often you release.",
     "<b>Lead time for changes</b> — commit to production.",
     "<b>Change failure rate</b> — share of deployments causing "
     "problems.",
     "<b>Time to restore</b> — how long recovery takes.",
     "",
     "<b>The finding that surprised people:</b> speed and stability are "
     "<i>positively</i> correlated.",
     ("Teams that deploy more often also fail less and recover faster.", 1),
     ("Because small changes are safer and frequent practice makes recovery "
      "routine.", 1),
   ],
   "footnote": "The speed/stability trade-off people assume does not appear "
               "in the data."},
 ],
 "takeaways": [
   "CI is a practice — everyone integrates daily — not a server "
   "that runs tests on branches.",
   "A permanently red build is worse than no build, because it trains people "
   "to ignore the signal.",
   "Order pipeline stages by cost: lint, small tests, build, medium, large. "
   "Fail at the earliest point.",
   "Ten minutes is the threshold. A slower pipeline changes behaviour, and "
   "every change is for the worse.",
   "Feature flags separate deploy from release, which is what makes "
   "trunk-based development possible. Delete release flags promptly.",
   "Speed and stability are positively correlated in the DORA data. Smaller "
   "changes are safer, and frequent practice makes recovery routine.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What continuous integration actually is"),
  ("callout", "A practice, not a product",
   ["'We have CI' almost always means 'we have a server that runs tests when "
    "a pull request opens'. That is a useful thing to have and it is not "
    "continuous integration.",
    "<b>Continuous integration is the practice of every developer "
    "integrating their work into a shared mainline at least daily.</b> The "
    "automation supports it; it is not the thing itself.",
    "A team with an excellent build server and three-week feature branches "
    "does not practise CI. They have automated testing and deferred "
    "integration pain — and the pain is deferred, not avoided.",
    "The purpose is to discover integration problems while they are small and "
    "attributable to one small change. That requires integrating frequently; "
    "no amount of tooling substitutes."]),
  ("table", ["Requirement", "Why"],
   [["<b>A single mainline.</b>",
     "Multiple long-lived integration branches reproduce the problem CI "
     "exists to solve."],
    ["<b>Everyone integrates at least daily.</b>",
     "This is the practice. Everything else is support."],
    ["<b>Every integration triggers an automated build and test.</b>",
     "Otherwise integration problems are found later, by someone else."],
    ["<b>A broken build is fixed immediately.</b>",
     "The highest priority for whoever broke it. See below."],
    ["<b>The build is fast.</b>",
     "Under ten minutes. Beyond that, people stop waiting and start working "
     "around it."]],
   [0.34, 0.66]),
  ("callout", "A tolerated red build destroys the practice",
   ["If the build is frequently broken, people stop looking at it. A genuine "
    "failure becomes indistinguishable from the usual noise, which means the "
    "signal has zero value — not reduced value, zero.",
    "Worse, teams develop the habit of merging onto a red build 'because it "
    "was already broken', at which point failures compound and nobody can "
    "tell which change caused what.",
    "This is Module 05's flaky test problem at the scale of the whole "
    "pipeline, and the remedy is the same: <b>a red build stops other work "
    "until it is green.</b> Not 'should be looked at soon' — stops.",
    "Teams that find this rule intolerable almost always have a build that is "
    "too slow or too flaky to sustain it. The correct response is to fix the "
    "build, not to relax the rule."]),

  ("h1", "2 &nbsp; Pipeline design"),
  ("table", ["Stage", "Typical duration", "What it catches"],
   [["Lint, format, type check", "Seconds",
     "Mechanical problems. First, because it is cheapest."],
    ["Small tests (Module 05)", "<b>Under a minute</b>", "Logic errors."],
    ["Build artefacts", "Minutes", "Compilation and packaging failures."],
    ["Medium tests", "Minutes", "Component integration."],
    ["Large / end-to-end tests", "Minutes",
     "<b>Whether the system actually works.</b>"],
    ["Deploy to staging", "Minutes", "Deployment mechanics and configuration."],
    ["Smoke tests", "Seconds", "Did it start and answer?"]],
   [0.27, 0.22, 0.51]),
  ("p", "The ordering is an economic argument: each stage costs more than the "
        "one before, so fail at the earliest point possible. A type error "
        "should never consume twenty minutes of end-to-end test time before "
        "being reported."),
  ("callout", "Ten minutes is a behavioural threshold, not a preference",
   ["Below about ten minutes, a developer waits for the result and treats a "
    "failure as part of the current task.",
    "Above it, they context-switch to something else. The failure now arrives "
    "when their attention is elsewhere, so it is deprioritised, so it sits "
    "broken longer, so others build on top of it.",
    "<b>A slow pipeline is not an inconvenience; it changes behaviour</b>, "
    "and every behavioural change it causes is bad.",
    "<b>What to do:</b> parallelise and shard the test suite; cache "
    "dependencies rather than resolving them each run; use build-system "
    "support for testing only what changed; move genuinely slow suites off "
    "the per-commit path to a nightly run."]),

  ("break",),
  ("h1", "3 &nbsp; Feature flags"),
  ("callout", "Separating deployment from release",
   ["Without flags, deploying code means releasing the feature in it. So "
    "incomplete work cannot be merged, so it lives on a branch, so branches "
    "live for weeks — which Module 08 identified as the source of merge "
    "difficulty.",
    "<b>With flags, you deploy code in a disabled state.</b> The feature is "
    "released later by changing a configuration value, with no deployment at "
    "all. The two events are decoupled.",
    "This single change unlocks a great deal: trunk-based development becomes "
    "possible for long-running work; features can be enabled for 1% of users "
    "and expanded; A/B experiments become configuration; and <b>rollback "
    "becomes turning a flag off</b>, which is faster and far safer than "
    "deploying a revert.",
    "<b>The cost is genuine.</b> Each flag is a branch in the code, and n "
    "independent flags give 2&#8319; configurations, only a few of which are "
    "ever tested. Flags must be removed once their decision is made."]),
  ("table", ["Kind", "Purpose", "Intended lifetime"],
   [["<b>Release flag</b>", "Hide incomplete work so it can be merged.",
     "<b>Days to weeks, then deleted.</b> These are the ones that accumulate "
     "and cause trouble."],
    ["<b>Experiment flag</b>", "A/B testing.",
     "The duration of the experiment, then deleted along with the losing "
     "branch."],
    ["<b>Operational flag</b>", "Kill switch; shed load; disable an expensive "
     "feature under pressure.",
     "Permanent, deliberately. These are infrastructure."],
    ["<b>Permission flag</b>", "Entitlement by subscription tier or role.",
     "Permanent. Arguably not a feature flag at all but part of the domain "
     "model, and better represented as such."]],
   [0.20, 0.38, 0.42]),
  ("p", "The practical discipline is to give every release flag an owner and "
        "an expiry date at creation, and to treat an expired flag as a "
        "build failure. Codebases where this is not enforced accumulate "
        "hundreds of flags, nobody knows which combinations are tested, and "
        "the flag system becomes the largest source of accidental complexity "
        "in the product."),

  ("h1", "4 &nbsp; Deployment strategies"),
  ("table", ["Strategy", "Mechanism", "Rollback", "Risk"],
   [["<b>Big bang</b>", "Stop the old version, deploy the new, start it.",
     "Redeploy the previous version — minutes at best.",
     "Downtime, and full exposure immediately."],
    ["<b>Rolling</b>", "Replace instances in batches.",
     "Roll the previous version back out, gradually.",
     "Both versions run simultaneously, so they must be compatible."],
    ["<b>Blue/green</b>", "Two complete environments; switch the load "
     "balancer.", "<b>Switch back. Seconds.</b>",
     "Twice the infrastructure; database compatibility across both."],
    ["<b>Canary</b>", "Route a small percentage to the new version, watch "
     "metrics, expand gradually.",
     "<b>Stop and revert. Small blast radius throughout.</b>",
     "Requires good metrics and automated analysis to be worth it."]],
   [0.15, 0.32, 0.27, 0.26]),
  ("callout", "Optimise for rollback speed",
   ["You cannot prevent every bad deployment. You can make undoing one cheap, "
    "and that is the more tractable problem.",
    "A system that rolls back in thirty seconds tolerates a far higher "
    "deployment rate than one requiring an hour — and a higher "
    "deployment rate means smaller individual changes, which means fewer "
    "failures in the first place. The two reinforce each other.",
    "<b>Database migrations are the genuinely hard part</b>, because many are "
    "not reversible: once a column is dropped, the data is gone. The "
    "discipline is <b>expand/contract</b>: add the new column; write to both "
    "old and new; backfill; switch reads to the new; and only then, in a "
    "later release, drop the old. Every step is independently deployable and "
    "independently reversible.",
    "<b>Never deploy a schema migration and the code that depends on it in "
    "the same release.</b> That combination is what makes rollback "
    "impossible, and it is the usual cause of an incident becoming an "
    "outage."]),

  ("h1", "5 &nbsp; Measuring delivery"),
  ("table", ["Metric", "Measures", "Elite performance"],
   [["<b>Deployment frequency</b>", "How often code reaches production.",
     "On demand — multiple times per day."],
    ["<b>Lead time for changes</b>", "Commit to running in production.",
     "Under one hour."],
    ["<b>Change failure rate</b>", "Share of deployments causing degraded "
     "service.", "Under 15%."],
    ["<b>Time to restore service</b>", "How long recovery from an incident "
     "takes.", "Under one hour."]],
   [0.26, 0.42, 0.32]),
  ("callout", "Speed and stability are positively correlated",
   ["The intuition is that deploying more often must mean breaking things "
    "more often, and that stability requires slowing down and adding review "
    "gates.",
    "<b>The DORA data consistently shows the opposite.</b> Teams that deploy "
    "most frequently also have the lowest change failure rates and the "
    "fastest recovery. The two sets of metrics move together.",
    "The mechanism is not mysterious. Frequent deployment forces small "
    "changes, and small changes are easier to review, easier to test, easier "
    "to diagnose when they fail, and easier to revert. Frequent deployment "
    "also means the deployment and rollback paths are exercised constantly, "
    "so they work when needed — Module 06's point about untested error "
    "paths, applied to operations.",
    "<b>A heavyweight change-approval process predicts worse outcomes on both "
    "axes</b>, which is one of the more uncomfortable findings in the data "
    "and one of the most consistently ignored."]),
 ],
 "resources": [
   ("Martin Fowler — Continuous Integration",
    "https://martinfowler.com/articles/continuousIntegration.html",
    "The article that defined the practice, and still the clearest statement "
    "that it is a practice rather than a tool."),
   ("Fowler — Feature Toggles",
    "https://martinfowler.com/articles/feature-toggles.html",
    "The taxonomy of &sect;3 and the management discipline that keeps flags "
    "from becoming debt."),
   ("DORA — research and the four key metrics",
    "https://dora.dev/",
    "The evidence base. Read the capability pages, not just the metric "
    "definitions."),
   ("Humble & Farley — Continuous Delivery",
    "https://continuousdelivery.com/",
    "The standard reference for pipelines, deployment strategies, and "
    "database migration under continuous delivery."),
 ],
 "exercises": [
   "Set up a CI pipeline for your Project 1 repository with the stages of "
   "&sect;2, ordered by cost. Measure the total duration and the duration of "
   "each stage.",
   "Make the pipeline faster. Parallelise the test suite, cache dependencies, "
   "and report before-and-after timings.",
   "Implement a feature flag system, even a simple one. Deploy a disabled "
   "feature, then enable it by configuration without deploying.",
   "Implement an expand/contract database migration: add a column, dual-write, "
   "backfill, switch reads, drop the old. Verify that you can roll back after "
   "each step.",
   "Measure your own DORA metrics on a project: deployment frequency, lead "
   "time from commit to deploy, and how long a revert takes.",
   "Deliberately break the build and measure how long it takes to notice and "
   "fix. Then make the pipeline report failures more visibly and repeat.",
   "Find an open-source project with public CI. Examine its pipeline "
   "configuration and assess it against &sect;2 — ordering, duration, "
   "and what runs per commit against nightly.",
 ],
 "selfcheck": [
   "What does continuous integration actually require, and why is a build "
   "server insufficient?",
   "Why is a permanently red build worse than no CI at all?",
   "What principle orders the pipeline stages?",
   "Why is ten minutes a threshold rather than a preference?",
   "What do feature flags decouple, and what does that make possible?",
   "Name the four flag types and say which causes debt if not removed.",
   "Why is rollback speed the right design criterion, and what makes database "
   "migrations hard?",
   "What is the relationship between speed and stability in the DORA data, "
   "and why?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Observability",
 "subtitle": "Knowing what your system is doing in production.",
 "question": "Something is wrong in production. How do you find out what?",
 "outcomes": [
     "Distinguish monitoring from observability.",
     "Use logs, metrics, and traces for their respective purposes.",
     "Design alerts that are worth waking someone for.",
     "Explain why percentiles matter and averages mislead.",
     "Explain SLOs and error budgets.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The distinction",
   "blurb": "Known unknowns against unknown unknowns."},

  {"t": "two", "kicker": "Two things", "title": "Monitoring and observability",
   "lh": "Monitoring",
   "l": ["Watching things you <b>knew to watch</b>.",
         "Dashboards, thresholds, alerts.",
         "Answers questions you anticipated.",
         ("'Is CPU above 80%?'", 1),
         "Necessary, and insufficient."],
   "rh": "Observability",
   "r": ["Answering questions you <b>did not anticipate</b>.",
         "Rich, high-cardinality data you can query freely.",
         "Answers new questions without deploying.",
         ("'Why are requests from one customer on one build slow?'", 1),
         "What you need during an incident."],
   "note": "The high-cardinality point is the technical crux — it is what "
           "most metrics systems cannot do."},

  {"t": "callout", "title": "You cannot dashboard your way out of a novel failure",
   "kind": "Why observability matters",
   "body": ["Dashboards show what someone previously thought to display. "
            "Novel failures are, by construction, not on them.",
            "The useful question during an incident is almost always a new "
            "one: 'is this specific to one region, one version, one customer, "
            "one code path?'",
            "<b>Answering that requires querying rich data, not reading "
            "pre-built charts.</b>",
            "So the test of an observability setup is: <i>can I ask a "
            "question nobody anticipated, right now, without deploying "
            "anything?</i>"]},

  {"t": "section", "label": "Part 2", "title": "Three signals",
   "blurb": "Different costs, different purposes."},

  {"t": "table", "kicker": "Signals", "title": "Logs, metrics, traces",
   "header": ["Signal", "Is", "Best for", "Cost"],
   "widths": [2.2, 3.4, 3.4, 3.1],
   "rows": [
     ["Logs", "Discrete events with context", "<b>What happened to this request</b>", "High volume"],
     ["Metrics", "Aggregated numbers over time", "<b>Trends and alerting</b>", "Cheap"],
     ["Traces", "One request across services", "<b>Where the time went</b>", "Sampled"],
   ],
   "note": "The three are complementary, not alternatives — each answers "
           "a question the others cannot."},

  {"t": "code", "kicker": "Logs", "title": "Structured logging",
   "lang": "python", "code": """
# UNSTRUCTURED -- a human can read it; a machine cannot query it
log.info(f"Order {order.id} failed for user {user.id}: {err}")

# STRUCTURED -- queryable
log.info("order_failed", extra={
    "order_id":    order.id,
    "user_id":     user.id,
    "error_code":  err.code,
    "amount":      order.total,
    "trace_id":    current_trace_id(),   # <-- ties to the trace
})

# Now: "all order_failed events for amount > 1000 in the last hour,
#       grouped by error_code" is a query, not a grep.
""",
   "caption": "The <code>trace_id</code> is what connects the three signals. "
              "Without it, correlating a log line to a trace is manual "
              "archaeology.",
   "note": "Trace ID propagation is the single highest-value piece of "
           "plumbing in observability."},

  {"t": "callout", "title": "Averages hide exactly what matters",
   "kind": "Use percentiles",
   "body": ["A mean response time of 100 ms is consistent with everyone "
            "getting 100 ms, and with 99% getting 50 ms while 1% get 5 "
            "seconds.",
            "<b>The second is a serious problem and the average cannot see "
            "it.</b>",
            "Track p50, p95, p99, and p99.9. The tail is where real user pain "
            "lives — and your heaviest users hit it most, because they "
            "make the most requests.",
            "<b>Never average percentiles across instances.</b> The average "
            "of two p99s is not a p99 and has no meaningful "
            "interpretation."]},

  {"t": "section", "label": "Part 3", "title": "Alerting",
   "blurb": "Every alert is an interruption. Spend them carefully."},

  {"t": "bullets", "kicker": "Alerts", "title": "Alert on symptoms, not causes",
   "items": [
     "<b>Bad:</b> 'CPU above 80%.' Maybe fine. Maybe the system is working "
     "hard and users are happy.",
     "",
     "<b>Good:</b> 'p99 latency above 2 s for five minutes.' Users are "
     "suffering.",
     "",
     "<b>Alert on what users experience</b>: availability, latency, error "
     "rate, throughput.",
     "",
     "Causes belong on dashboards for diagnosis — not in the pager.",
     "",
     "<b>Test:</b> if this fires and nobody needs to act, it should not "
     "exist.",
   ],
   "note": "The symptom/cause distinction eliminates most alert noise by "
           "itself."},

  {"t": "callout", "title": "Alert fatigue is a reliability problem",
   "kind": "The failure mode",
   "body": ["An on-call engineer paged six times a night learns to "
            "acknowledge without reading.",
            "<b>Then the real alert is missed too.</b> Noisy alerts do not "
            "merely waste time — they actively destroy the response "
            "capability they were meant to provide.",
            "Same structure as flaky tests (Module 05) and red builds "
            "(Module 10): a signal that is usually noise is ignored "
            "entirely.",
            "<b>Rule:</b> every page must be actionable and urgent. If it can "
            "wait until morning, it is a ticket. If nothing can be done, it "
            "is a dashboard."]},

  {"t": "section", "label": "Part 4", "title": "SLOs",
   "blurb": "Deciding how reliable is reliable enough."},

  {"t": "bullets", "kicker": "SLOs", "title": "Service level objectives and error budgets",
   "items": [
     "<b>SLI</b> — the measurement. 'Proportion of requests under 300 "
     "ms.'",
     "<b>SLO</b> — the target. '99.9% over 30 days.'",
     "<b>Error budget</b> — what the target permits: 0.1%, about 43 "
     "minutes a month.",
     "",
     "<b>The budget is the useful part.</b> It converts reliability into a "
     "resource you spend deliberately.",
     ("Budget remaining → ship features.", 1),
     ("Budget exhausted → stop feature work, fix reliability.", 1),
     "",
     "It turns an argument into arithmetic.",
   ],
   "note": "The error budget as a conflict-resolution mechanism is the "
           "genuinely clever part of SRE."},

  {"t": "callout", "title": "100% is the wrong target",
   "kind": "Why error budgets work",
   "body": ["Each additional nine costs roughly ten times more than the last, "
            "and users cannot detect the difference above a certain point "
            "— their own network is less reliable than your service.",
            "<b>So perfect reliability is both unachievable and "
            "wasteful.</b>",
            "Choosing 99.9% explicitly means accepting 43 minutes of monthly "
            "unavailability as a <i>budget</i> — and an unspent budget "
            "means you were too conservative and shipped too slowly.",
            "This resolves the usual developers-versus-operations conflict "
            "with a number both sides agreed to in advance."]},
 ],
 "takeaways": [
   "Monitoring answers questions you anticipated; observability answers ones "
   "you did not. Novel failures are never on the dashboard.",
   "Logs say what happened to one request, metrics show trends cheaply, "
   "traces show where the time went. Use all three.",
   "Structured logging makes logs queryable; a propagated trace ID is what "
   "ties the three signals together.",
   "Averages hide the tail. Track p50, p95, p99, p99.9 — and never "
   "average percentiles.",
   "Alert on symptoms users feel, not on causes. Every page must be "
   "actionable and urgent, or it destroys the signal.",
   "Error budgets turn reliability into a spendable resource and convert an "
   "argument into arithmetic.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Monitoring and observability"),
  ("table", ["", "Monitoring", "Observability"],
   [["Answers", "Questions you knew to ask.",
     "Questions you did not anticipate."],
    ["Mechanism", "Pre-defined dashboards, thresholds, alerts.",
     "Rich, high-cardinality event data that can be queried freely after the "
     "fact."],
    ["Typical question", "'Is CPU above 80%?'",
     "'Why are requests from customer 4471, on build 1.8.3, in eu-west, "
     "slow — but only for POSTs?'"],
    ["Sufficient?", "Necessary, and not sufficient.",
     "What you need during an incident you have not seen before."]],
   [0.14, 0.38, 0.48]),
  ("callout", "Dashboards cannot answer novel questions",
   ["A dashboard displays what someone previously decided was worth "
    "displaying. A genuinely novel failure — which is what incidents "
    "mostly are — is by construction not on it.",
    "The question that actually resolves an incident is nearly always new and "
    "specific: is this confined to one region, one version, one customer, one "
    "endpoint, one combination of all four?",
    "Answering that requires <b>querying rich data</b> rather than reading "
    "pre-aggregated charts, and in particular it requires "
    "<b>high-cardinality</b> fields — user IDs, request IDs, build "
    "hashes — which most traditional metrics systems explicitly cannot "
    "store, because each distinct value creates a new time series.",
    "<b>The test of an observability setup:</b> can you ask a question nobody "
    "anticipated, right now, without shipping code? If answering requires a "
    "deploy, you have monitoring."]),

  ("h1", "2 &nbsp; The three signals"),
  ("table", ["Signal", "What it is", "Answers", "Cost profile"],
   [["<b>Logs</b>", "Discrete timestamped events with context.",
     "'What happened to <i>this</i> request?'",
     "High volume; expensive to store and index at scale."],
    ["<b>Metrics</b>", "Numeric aggregates over time windows.",
     "'Is the error rate rising? Is latency up this week?'",
     "Very cheap — fixed cost regardless of request volume. The right "
     "basis for alerting."],
    ["<b>Traces</b>", "The path of one request across every service it "
     "touched, with timing per hop.",
     "'Where did the 3 seconds go?'",
     "Expensive per trace, so usually sampled."]],
   [0.14, 0.31, 0.28, 0.27]),
  ("p", "The three are complementary rather than alternatives. Metrics tell "
        "you something is wrong and are cheap enough to evaluate "
        "continuously. Traces tell you which component is responsible. Logs "
        "tell you what that component was actually doing."),
  ("h2", "2.1 &nbsp; Structured logging"),
  ("code", """# Unstructured: readable by a human, not queryable
log.info(f"Order {order.id} failed for user {user.id}: {err}")

# Structured: queryable
log.info("order_failed", extra={
    "order_id":   order.id,
    "user_id":    user.id,
    "error_code": err.code,
    "amount":     order.total,
    "trace_id":   current_trace_id(),
})"""),
  ("p", "With structured events, 'all <code>order_failed</code> events with "
        "amount over 1000 in the last hour, grouped by error code' is a query "
        "rather than an exercise in regular expressions. The fields are "
        "available for aggregation, filtering, and grouping without anyone "
        "having anticipated the question."),
  ("callout", "The trace ID is the connective tissue",
   ["Generate a unique identifier at the system's edge and propagate it "
    "through every service call, every queue message, and every log line.",
    "Then a single identifier connects all three signals: a metric anomaly "
    "leads to a trace, the trace identifies the slow service, and the trace "
    "ID retrieves exactly the log lines from that request.",
    "<b>Without propagated trace IDs, correlating signals is manual "
    "archaeology</b> — matching timestamps across systems with "
    "differently-skewed clocks, which is as unpleasant as it sounds.",
    "This is the single highest-value piece of plumbing in observability, and "
    "it is far cheaper to add before you need it than during an incident."]),
  ("callout", "Averages conceal precisely what you need to see",
   ["A mean response time of 100 ms is consistent with every user "
    "experiencing 100 ms, and equally consistent with 99% of users "
    "experiencing 50 ms while 1% wait five seconds.",
    "The second situation is a serious problem, and the average is incapable "
    "of distinguishing it from the first.",
    "<b>Track percentiles: p50, p95, p99, and p99.9.</b> The tail is where "
    "real user pain lives — and your most engaged users encounter it "
    "most often, simply because they make the most requests. A 1% failure "
    "rate means a user making a hundred requests per session almost certainly "
    "hits it.",
    "<b>Never average percentiles across instances or time windows.</b> The "
    "mean of two p99 values is not a p99 of anything and has no valid "
    "interpretation. Percentiles must be computed from the underlying "
    "distribution, which is why histogram-based metrics exist."]),

  ("break",),
  ("h1", "3 &nbsp; Alerting"),
  ("p", "Every alert is an interruption of someone's attention, and "
        "frequently of their sleep. The budget is small and should be spent "
        "deliberately."),
  ("callout", "Alert on symptoms, not causes",
   ["<b>'CPU above 80%'</b> is a cause. It might indicate a problem, or it "
    "might indicate the system working hard and serving users perfectly well. "
    "Waking someone to tell them the computer is being used is not a good "
    "use of a person.",
    "<b>'p99 latency above 2 seconds for five minutes'</b> is a symptom. "
    "Users are experiencing it now.",
    "Alert on the four things users actually experience: <b>availability, "
    "latency, error rate, and throughput</b>. Causes belong on dashboards, "
    "where they are consulted during diagnosis after a symptom alert has "
    "fired.",
    "<b>The test:</b> if this alert fires and nobody needs to take action, it "
    "should not be an alert."]),
  ("callout", "Alert fatigue is a reliability failure",
   ["An engineer paged six times in a night learns, correctly, to acknowledge "
    "without reading. The sixth alert and the first receive identical "
    "attention: none.",
    "<b>Then the genuine alert is missed too.</b> Noisy alerting does not "
    "merely waste time; it destroys the response capability it exists to "
    "provide, and it does so invisibly — the alerts are all being "
    "acknowledged.",
    "This is structurally identical to the flaky test of Module 05 and the "
    "red build of Module 10. A signal that is usually noise is treated as "
    "always noise, and the system that depended on it quietly stops working.",
    "<b>The rule: every page must be both actionable and urgent.</b> If "
    "action can wait until morning, it is a ticket. If no action is possible, "
    "it is a dashboard. If it fires regularly and is always ignored, delete "
    "it — deleting it loses nothing and recovers attention."]),

  ("h1", "4 &nbsp; Service level objectives"),
  ("table", ["Term", "Definition", "Example"],
   [["<b>SLI</b> — indicator", "The thing you measure.",
     "Proportion of HTTP requests completing successfully in under 300 ms."],
    ["<b>SLO</b> — objective", "The target for that measurement.",
     "99.9% over a rolling 30-day window."],
    ["<b>Error budget</b>", "What the objective permits you to fail.",
     "0.1% of requests — about 43 minutes of full unavailability per "
     "month, or a larger amount of partial degradation."],
    ["<b>SLA</b> — agreement", "A contractual commitment, with "
     "penalties.", "Set well below the SLO, so that missing the SLO is a "
     "warning rather than a breach."]],
   [0.20, 0.33, 0.47]),
  ("callout", "The error budget is the genuinely useful idea",
   ["An SLO on its own is a target. The <b>error budget</b> turns reliability "
    "into a resource that is spent deliberately.",
    "<b>Budget remaining:</b> ship features, take risks, deploy more often. "
    "You have room.",
    "<b>Budget exhausted:</b> feature work stops and reliability work starts, "
    "until the budget recovers.",
    "This resolves the standard conflict between development, which wants to "
    "ship, and operations, which wants stability — not by argument but "
    "by a number both sides agreed to in advance. It converts a recurring "
    "political dispute into arithmetic, which is a remarkable thing for a "
    "metric to accomplish."]),
  ("callout", "100% is the wrong target",
   ["Each additional nine of availability costs roughly an order of magnitude "
    "more than the last, and above a certain point users cannot perceive the "
    "difference — their own network connection is less reliable than "
    "your service, so your additional nines are invisible beneath their noise "
    "floor.",
    "So perfect reliability is simultaneously unachievable and, past some "
    "point, worthless.",
    "Choosing 99.9% <i>explicitly</i> means deciding that 43 minutes of "
    "unavailability per month is acceptable, and treating it as a budget to "
    "be spent rather than a failure to be avoided.",
    "<b>An unspent error budget means you were too conservative</b> — "
    "you could have shipped faster and taken more risk. That reframing, that "
    "excess reliability is itself a cost, is the most counterintuitive and "
    "most useful idea in site reliability engineering."]),
 ],
 "resources": [
   ("Google — Site Reliability Engineering (free online)",
    "https://sre.google/books/",
    "SLOs, error budgets, alerting philosophy, and incident response. The "
    "standard reference, and free."),
   ("Charity Majors et al. — Observability Engineering (sample chapters "
    "free)",
    "https://www.honeycomb.io/resources",
    "The monitoring-versus-observability distinction and the argument for "
    "high-cardinality data."),
   ("OpenTelemetry documentation",
    "https://opentelemetry.io/docs/",
    "The vendor-neutral standard for traces, metrics, and logs. Instrument "
    "with this rather than a proprietary agent."),
   ("Gil Tene — How NOT to Measure Latency (free video)",
    "https://www.youtube.com/watch?v=lJ8ydIuPFeU",
    "Why averages mislead, why percentile averaging is invalid, and what "
    "coordinated omission does to your measurements. Essential and "
    "entertaining."),
 ],
 "exercises": [
   "Convert an application's logging from string formatting to structured "
   "events. Then answer a question with a query that would previously have "
   "required grep and manual counting.",
   "Implement trace ID generation and propagation across at least two "
   "services. Demonstrate retrieving all log lines for one request.",
   "Instrument a service with a latency histogram. Plot mean alongside p50, "
   "p95, and p99 under load, and construct a situation where the mean looks "
   "healthy and p99 does not.",
   "Audit an existing alert configuration. Classify each alert as symptom or "
   "cause, and as actionable or not. Delete the ones that fail both tests.",
   "Define an SLI and SLO for a service you run. Compute the error budget in "
   "minutes and compare against actual downtime over the last month.",
   "Run a load test and use traces to find where the time goes in a slow "
   "request. Report the breakdown by service.",
   "Deliberately introduce latency into one dependency and verify that your "
   "alerting notices it before you do.",
 ],
 "selfcheck": [
   "Distinguish monitoring from observability, and say why dashboards cannot "
   "resolve novel incidents.",
   "What question does each of logs, metrics, and traces answer best, and how "
   "do their costs differ?",
   "Why does structured logging matter, and what role does the trace ID "
   "play?",
   "Why do averages mislead, and why can percentiles not be averaged?",
   "What is the difference between a symptom alert and a cause alert, and why "
   "does it matter?",
   "Why is alert fatigue a reliability problem rather than merely an "
   "annoyance?",
   "What is an error budget, and why is an unspent one a problem?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Process",
 "subtitle": "How teams organise work, and what the evidence says.",
 "question": "Does the process matter, and which parts of it?",
 "outcomes": [
     "Explain why waterfall persisted and what it got right.",
     "Explain what the Agile Manifesto actually said.",
     "Distinguish agile principles from Agile ceremony.",
     "Estimate honestly, and explain why estimates are unreliable.",
     "Judge a process by what it optimises.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Waterfall",
   "blurb": "Maligned, and the original paper said the opposite of what "
            "people think."},

  {"t": "callout", "title": "Royce's 1970 paper argued against the model it is credited with",
   "kind": "The historical correction",
   "body": ["Royce presented the sequential model — requirements, "
            "design, implementation, verification — and then wrote that "
            "it 'is risky and invites failure'.",
            "His recommendation was to <b>do it twice</b>, and to feed "
            "testing back into design. Essentially an iterative process.",
            "The sequential diagram was adopted and the argument against it "
            "was not, which is among the more consequential misreadings in "
            "the field.",
            "<b>What it got right:</b> thinking before building; writing "
            "things down; that late changes cost more than early ones. Those "
            "remain true."]},

  {"t": "bullets", "kicker": "Why it fails", "title": "Where sequential development breaks",
   "items": [
     "<b>Requirements are not knowable up front</b> (Module 02). People learn "
     "what they want by using something.",
     "",
     "<b>No feedback until the end.</b> A misunderstanding in week two "
     "surfaces in month nine.",
     "",
     "<b>No working software for a long time</b>, so progress cannot be "
     "verified — only reported.",
     "",
     "<b>Change is treated as failure</b>, so it is resisted rather than "
     "planned for.",
     "",
     "The core problem is feedback latency.",
   ],
   "note": "Framing it as a feedback-latency problem makes the agile response "
           "feel like engineering rather than ideology."},

  {"t": "section", "label": "Part 2", "title": "What Agile said",
   "blurb": "Four sentences, and most of what followed is not in them."},

  {"t": "table", "kicker": "The manifesto", "title": "Four preferences, 2001",
   "header": ["Over", "Value more"],
   "widths": [5.8, 6.3],
   "rows": [
     ["Processes and tools", "<b>Individuals and interactions</b>"],
     ["Comprehensive documentation", "<b>Working software</b>"],
     ["Contract negotiation", "<b>Customer collaboration</b>"],
     ["Following a plan", "<b>Responding to change</b>"],
   ],
   "footnote": "'While there is value in the items on the left, we value the "
               "items on the right more.' The caveat is routinely dropped.",
   "note": "The dropped caveat is why 'agile means no documentation' became a "
           "widespread misreading."},

  {"t": "callout", "title": "Agile principles and Agile ceremony are different things",
   "kind": "The distinction that matters",
   "body": ["<b>The principles are modest and well supported:</b> deliver "
            "frequently, get feedback, respond to change, keep it simple, "
            "reflect and adjust.",
            "<b>The ceremony is what was sold:</b> two-week sprints, story "
            "points, velocity, stand-ups, retrospectives, certifications, "
            "consultants.",
            "Much of the ceremony has no evidence behind it, and some of it "
            "contradicts the principles — a two-week sprint commitment "
            "is a plan you are not supposed to change.",
            "<b>Evaluate any practice by whether it shortens the feedback "
            "loop.</b> If it does not, it is overhead regardless of what it "
            "is called."]},

  {"t": "section", "label": "Part 3", "title": "Estimation",
   "blurb": "Unreliable for structural reasons."},

  {"t": "bullets", "kicker": "Estimation", "title": "Why estimates are wrong",
   "items": [
     "<b>The planning fallacy.</b> People systematically underestimate, even "
     "knowing they do.",
     "",
     "<b>Unknown unknowns.</b> The work you did not know existed is, by "
     "definition, not in the estimate.",
     "",
     "<b>Estimates become commitments</b> the moment someone writes them "
     "down, so they get padded, so they become less informative.",
     "",
     "<b>Estimating requires understanding</b>, and understanding usually "
     "arrives by doing the work.",
     "",
     "<b>Historical data beats judgement</b> — and almost nobody keeps "
     "it.",
   ],
   "note": "The estimate-becomes-commitment dynamic explains most "
           "dysfunction around planning."},

  {"t": "table", "kicker": "Better", "title": "Approaches that work better",
   "header": ["Approach", "Idea"],
   "widths": [3.6, 8.5],
   "rows": [
     ["Historical throughput", "Measure how long similar items actually took"],
     ["Ranges, not points", "'Two to six weeks, most likely three'"],
     ["Reference class", "Compare against similar past projects, not from scratch"],
     ["Slice smaller", "Small items estimate better; errors cancel"],
     ["<b>#NoEstimates</b>", "Slice to similar size, count throughput, skip estimating"],
   ],
   "note": "The #NoEstimates position is stronger than it sounds once you "
           "have uniform small items."},

  {"t": "callout", "title": "Measure cycle time instead",
   "kind": "The practical alternative",
   "body": ["<b>Cycle time</b> — from starting an item to delivering it "
            "— is measured, not guessed.",
            "Plot the distribution. 'Items like this take 3–10 days, "
            "85% within 8' is a forecast with evidence, derived from your "
            "team on your codebase.",
            "<b>It improves automatically</b> as you gather data, and it "
            "cannot be padded or negotiated.",
            "And it directs attention usefully: reducing cycle time means "
            "removing waiting, which is where most of the time goes — "
            "not typing."]},

  {"t": "section", "label": "Part 4", "title": "What the evidence supports",
   "blurb": "Less than the industry's confidence suggests."},

  {"t": "table", "kicker": "Evidence", "title": "Practices by support",
   "header": ["Practice", "Evidence"],
   "widths": [5.6, 6.5],
   "rows": [
     ["Small batches, frequent delivery", "<b>Strong</b> — DORA"],
     ["Version control, CI, automated deploy", "<b>Strong</b>"],
     ["Loosely coupled architecture", "<b>Strong</b>"],
     ["Psychological safety", "<b>Strong</b> — the best predictor found"],
     ["Heavyweight change approval", "<b>Negative</b> — worse on both axes"],
     ["Specific ceremonies, story points", "Weak to none"],
   ],
   "note": "The change-approval finding is the most uncomfortable and the "
           "most ignored."},

  {"t": "callout", "title": "The best predictor is whether people can speak up",
   "kind": "The finding nobody expected",
   "body": ["Google's Project Aristotle set out to find what makes teams "
            "effective. The strongest factor was not skill, seniority, or "
            "process.",
            "It was <b>psychological safety</b>: whether members believe they "
            "can admit a mistake, ask an obvious question, or disagree "
            "without being punished.",
            "<b>Mechanism:</b> problems surface early. Bad news travels fast. "
            "People ask instead of guessing. Bugs get reported rather than "
            "hidden.",
            "Which makes a blameless culture an <i>engineering</i> practice "
            "— it determines how quickly you learn about problems, which "
            "is the whole subject of this course."]},

  {"t": "bullets", "kicker": "Judging", "title": "How to evaluate any process",
   "items": [
     "<b>Does it shorten the feedback loop?</b> The single best question.",
     "<b>Does it surface problems early</b> or hide them until a deadline?",
     "<b>Does it reduce batch size?</b>",
     "<b>Does it make work visible?</b>",
     "<b>Is anyone deciding to continue it</b>, or is it just what we do?",
     "",
     "A practice nobody can justify is ceremony. Stop it and see what "
     "breaks.",
   ],
   "footnote": "Most process dysfunction is practices retained after their "
               "reason expired."},
 ],
 "takeaways": [
   "Royce's 1970 paper argued <i>against</i> pure sequential development. The "
   "diagram was adopted and the argument was not.",
   "Waterfall's core problem is feedback latency, not documentation or "
   "planning — both of which remain valuable.",
   "The Agile Manifesto is four preferences with an explicit caveat that both "
   "sides have value. The caveat is routinely dropped.",
   "Agile principles are modest and supported; Agile ceremony largely is not. "
   "Judge any practice by whether it shortens feedback.",
   "Estimates are unreliable for structural reasons, and become commitments "
   "the moment they are written down. Measure cycle time instead.",
   "Psychological safety is the strongest predictor of team effectiveness "
   "found, because it determines how fast problems surface.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Waterfall, and what it actually said"),
  ("callout", "Royce argued against the model he is credited with",
   ["Winston Royce's 1970 paper is universally cited as the origin of the "
    "waterfall model. He presented the sequential diagram — "
    "requirements, design, implementation, verification, operations — "
    "and then wrote that implementing it this way 'is risky and invites "
    "failure'.",
    "His actual recommendation was to <b>build it twice</b> — a pilot "
    "version to learn from — and to feed testing results back into "
    "design. That is an iterative process with feedback loops.",
    "The diagram was adopted and the argument accompanying it was not. It is "
    "among the more consequential misreadings in the field's history, and it "
    "shaped a generation of government procurement.",
    "<b>What the sequential model got right remains right:</b> thinking "
    "before building is better than not; writing decisions down preserves "
    "them; and a change costs more the later it is made. None of this is in "
    "dispute."]),
  ("p", "The genuine failure is <b>feedback latency</b>. Requirements cannot "
        "be fully known in advance (Module 02); a misunderstanding in week "
        "two surfaces in month nine; there is no working software to inspect, "
        "so progress can only be reported rather than verified; and change is "
        "framed as a failure of planning, so it is resisted rather than "
        "accommodated."),

  ("h1", "2 &nbsp; What the Agile Manifesto said"),
  ("p", "Seventeen people, 2001, four sentences. Worth reading in the "
        "original, because most of what is done in its name is not in it."),
  ("table", ["We value", "over"],
   [["<b>Individuals and interactions</b>", "processes and tools"],
    ["<b>Working software</b>", "comprehensive documentation"],
    ["<b>Customer collaboration</b>", "contract negotiation"],
    ["<b>Responding to change</b>", "following a plan"]],
   [0.5, 0.5]),
  ("p", "The document then states explicitly: '<i>That is, while there is "
        "value in the items on the right, we value the items on the left "
        "more.</i>' That caveat is almost always omitted in practice, which "
        "is how 'agile means we do not write documentation' became a "
        "widespread and entirely unsupported reading."),
  ("callout", "Principles and ceremony are not the same thing",
   ["<b>The principles are modest and largely well supported:</b> deliver "
    "working software frequently; welcome changing requirements; get feedback "
    "from real users; keep the design simple; have the team reflect and "
    "adjust at intervals.",
    "<b>The ceremony is what was subsequently sold:</b> two-week sprints, "
    "story points, velocity tracking, daily stand-ups, sprint planning poker, "
    "retrospectives with sticky notes, certification programmes, and "
    "consultants to install all of it.",
    "Much of the ceremony has no evidential support, and some of it "
    "contradicts the principles it claims to implement — a sprint "
    "commitment is a plan you have agreed not to change for two weeks, which "
    "is the fourth value inverted.",
    "<b>The useful test for any practice: does it shorten the feedback "
    "loop?</b> Daily stand-ups can, if they surface blockers. They do not, if "
    "they are status reports to a manager. The same ritual, opposite "
    "effects — which is why arguing about the ritual rather than its "
    "function is unproductive."]),

  ("break",),
  ("h1", "3 &nbsp; Estimation"),
  ("p", "Software estimates are unreliable, and the reasons are structural "
        "rather than a matter of insufficient discipline."),
  ("ol", ["<b>The planning fallacy.</b> People systematically underestimate "
          "task duration, and continue to do so after being shown evidence "
          "that they do. This is a robust finding well outside software.",
          "<b>Unknown unknowns.</b> The work you did not know would be "
          "necessary is by definition absent from the estimate, and on novel "
          "work it is frequently the majority.",
          "<b>Estimates become commitments.</b> The moment a number is "
          "written down it is treated as a promise, so estimators pad, so the "
          "numbers carry less information, so trust declines, so more padding "
          "is required. The feedback loop is self-defeating.",
          "<b>Estimating requires understanding the work</b>, and "
          "understanding the work generally arrives by doing it. The estimate "
          "is required at the moment of minimum information."]),
  ("table", ["Approach", "What it does"],
   [["<b>Historical throughput</b>",
     "Measure how long comparable items have actually taken on this team, "
     "with this codebase. Beats expert judgement consistently, and almost "
     "nobody collects the data."],
    ["<b>Ranges rather than points</b>",
     "'Two to six weeks, most likely three.' Honest about uncertainty, and "
     "harder to convert into a commitment."],
    ["<b>Reference class forecasting</b>",
     "Compare against the distribution of similar completed projects rather "
     "than reasoning from the inside. Corrects the planning fallacy more "
     "effectively than trying harder."],
    ["<b>Slice smaller</b>",
     "Small items estimate better, and errors on many small items partially "
     "cancel rather than compounding."],
    ["<b>#NoEstimates</b>",
     "Slice work into items of roughly uniform size, count how many are "
     "completed per week, and forecast from the count. Stronger than it "
     "sounds once items are genuinely uniform."]],
   [0.26, 0.74]),
  ("callout", "Measure cycle time",
   ["<b>Cycle time</b> is the elapsed time from starting work on an item to "
    "delivering it. It is measured rather than predicted.",
    "Plot the distribution and you have a forecast with evidence behind it: "
    "'items of this type take three to ten days, with 85% completing within "
    "eight.' That is derived from this team working on this codebase, which "
    "is exactly the population the question is about.",
    "<b>It improves automatically</b> as data accumulates, requires no "
    "estimation meetings, and cannot be padded or negotiated — it is a "
    "record of what happened.",
    "It also directs attention usefully. Reducing cycle time means removing "
    "<i>waiting</i> — for review, for CI, for deployment, for a "
    "decision — and in most teams waiting dominates. Almost none of "
    "cycle time is typing, which is the activity estimation focuses on."]),

  ("h1", "4 &nbsp; What the evidence supports"),
  ("table", ["Practice", "Evidence", "Source"],
   [["Small batch sizes and frequent delivery.", "<b>Strong</b>",
     "DORA, consistently across years and organisation types."],
    ["Version control, CI, automated deployment, test automation.",
     "<b>Strong</b>", "DORA."],
    ["Loosely coupled architecture allowing independent deployment.",
     "<b>Strong</b>", "DORA. Module 03's argument, measured."],
    ["<b>Psychological safety.</b>", "<b>Strong</b>",
     "Google's Project Aristotle; DORA's culture findings. The strongest "
     "single predictor identified."],
    ["Heavyweight change approval boards.", "<b>Negatively correlated</b>",
     "DORA. Associated with worse outcomes on both speed and stability, "
     "which is the opposite of their purpose."],
    ["Specific ceremonies: sprint length, story points, planning poker.",
     "Weak to none", "Little rigorous study; what exists is inconclusive."]],
   [0.34, 0.22, 0.44]),
  ("callout", "The strongest predictor is whether people can speak up",
   ["Google's Project Aristotle studied 180 teams looking for the "
    "determinants of effectiveness. The strongest factor was not individual "
    "skill, seniority, team size, or process.",
    "It was <b>psychological safety</b>: whether team members believe they "
    "can admit a mistake, ask a question that might sound ignorant, challenge "
    "a decision, or report bad news without being penalised.",
    "<b>The mechanism is directly relevant to engineering.</b> In a safe "
    "team, problems surface early, bad news travels fast, people ask rather "
    "than guess, bugs are reported rather than concealed, and bad estimates "
    "are corrected rather than defended.",
    "Every one of those is a <i>feedback loop</i>, which this module has "
    "identified as the thing that matters. That makes blameless culture an "
    "engineering practice rather than a management nicety: it determines how "
    "quickly you find out that something is wrong."]),

  ("h1", "5 &nbsp; Judging a process"),
  ("ol", ["<b>Does it shorten the feedback loop?</b> The single most useful "
          "question, and most practices can be assessed against it directly.",
          "<b>Does it surface problems early,</b> or does it defer their "
          "discovery to a deadline?",
          "<b>Does it reduce batch size?</b> Smaller batches are the "
          "best-supported finding in the field.",
          "<b>Does it make work visible?</b> Invisible work cannot be "
          "prioritised, balanced, or improved.",
          "<b>Is anyone actively deciding to continue it?</b> Or is it simply "
          "what has always been done?"]),
  ("p", "That last question identifies most process dysfunction. Practices "
        "accumulate, the reasons for them expire, and nobody removes them "
        "because nobody is responsible for the question. A practice that "
        "nobody can justify is ceremony. <b>Stop it for a month and observe "
        "what breaks</b> — frequently nothing does, and when something "
        "does, you have learned what the practice was actually for, which is "
        "more than anyone knew before."),
 ],
 "resources": [
   ("Royce — Managing the Development of Large Software Systems (1970, "
    "free)",
    "https://www.praxisframework.org/files/royce1970.pdf",
    "The waterfall paper. Read sections 3 onward, where he argues against the "
    "model he had just drawn."),
   ("The Agile Manifesto and its twelve principles",
    "https://agilemanifesto.org/",
    "Four sentences and twelve principles. Takes five minutes and corrects a "
    "great deal."),
   ("Forsgren, Humble & Kim — Accelerate / DORA",
    "https://dora.dev/",
    "The empirical research. Read the capability pages rather than only the "
    "four metrics."),
   ("Google re:Work — Project Aristotle",
    "https://rework.withgoogle.com/print/guides/5721312655835136/",
    "The psychological safety finding, with the methodology."),
 ],
 "exercises": [
   "Read Royce's paper and identify the passage where he recommends against "
   "the sequential model. Write a paragraph on how the misreading happened.",
   "Read the twelve Agile principles and identify which practices in a team "
   "you know follow from them and which do not.",
   "Measure cycle time for the last twenty items in a project you can "
   "observe. Plot the distribution and produce an 85th-percentile forecast.",
   "Compare that forecast against the original estimates for the same items. "
   "Quantify the estimation error and its direction.",
   "List every recurring process practice in a team you know. For each, state "
   "what feedback loop it shortens. Identify the ones with no answer.",
   "Break down cycle time into working time and waiting time for five items. "
   "Report the ratio.",
   "Find a team practice that has been retained past its original purpose. "
   "Propose stopping it and predict what will break.",
 ],
 "selfcheck": [
   "What did Royce actually recommend, and what did waterfall get right?",
   "What is the core problem with sequential development?",
   "State the four values of the Agile Manifesto and the caveat that "
   "accompanies them.",
   "Distinguish agile principles from Agile ceremony, and give the test for "
   "any practice.",
   "Give four structural reasons software estimates are unreliable.",
   "What is cycle time, and why is it better than estimation?",
   "What is the strongest predictor of team effectiveness found, and why does "
   "it matter for engineering specifically?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Maintenance and the Long Life of Code",
 "subtitle": "What happens after the project ends.",
 "question": "How do you hand a system to someone who was not there?",
 "outcomes": [
     "Explain why software decays without being modified.",
     "Write documentation that stays true.",
     "Manage dependencies as an ongoing liability.",
     "Plan for deprecation and migration.",
     "Judge your own work by what it costs its next owner.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Software rot",
   "blurb": "Code decays even when nobody edits it."},

  {"t": "callout", "title": "Nothing changed, and it stopped working",
   "kind": "Why it happens",
   "body": ["Code does not wear out. Its <b>environment</b> changes "
            "underneath it.",
            "A dependency releases a breaking version. An OS removes an API. "
            "A certificate expires. A protocol is deprecated. A third-party "
            "service changes a response format.",
            "<b>Hyrum's law:</b> with enough users, every observable "
            "behaviour of your system is depended on by someone — "
            "including behaviours you never documented and did not intend.",
            "<b>Consequence:</b> 'we will not touch it' is not a maintenance "
            "strategy. Unmaintained code becomes unbuildable, then "
            "unrunnable, then unreplaceable."]},

  {"t": "bullets", "kicker": "Lehman", "title": "Lehman's laws, the two that matter",
   "items": [
     "<b>Continuing change:</b> a system used in a real environment must be "
     "continually adapted, or it becomes progressively less useful.",
     "",
     "<b>Increasing complexity:</b> as a system evolves, its complexity "
     "increases <i>unless work is done to reduce it</i>.",
     "",
     "That second clause is the engineering content: complexity growth is the "
     "default, and reversing it requires deliberate effort.",
     "",
     "Refactoring (Module 07) is not optional tidying — it is what "
     "offsets a law.",
   ],
   "note": "'Unless work is done to reduce it' reframes refactoring as "
           "resisting entropy rather than as polish."},

  {"t": "section", "label": "Part 2", "title": "Documentation",
   "blurb": "The kind that stays true."},

  {"t": "table", "kicker": "Documentation", "title": "Four kinds, four purposes",
   "header": ["Kind", "Answers", "Rots?"],
   "widths": [2.8, 5.4, 3.9],
   "rows": [
     ["Tutorial", "How do I get started?", "Slowly"],
     ["How-to guide", "How do I do X?", "Moderately"],
     ["Reference", "What are the parameters?", "<b>Fast — generate it</b>"],
     ["Explanation", "<b>Why is it like this?</b>", "<b>Barely — most valuable</b>"],
   ],
   "footnote": "Diátaxis. Most projects write only reference and wonder "
               "why nobody can get started.",
   "note": "The rot column is the practical insight: write what does not rot, "
           "generate what does."},

  {"t": "callout", "title": "Write what cannot be recovered from the code",
   "kind": "The principle",
   "body": ["<b>What the code does</b> can be read from the code. "
            "Documentation that restates it duplicates knowledge, so it rots "
            "and then actively misleads.",
            "<b>Why it does that</b> cannot be recovered. Which alternative "
            "was tried and failed, which constraint forced the odd approach, "
            "which bug this guards against.",
            "<b>So: document decisions, constraints, and rejected "
            "alternatives.</b> ADRs (Module 04), commit messages (Module "
            "08), and comments explaining why.",
            "<b>Wrong documentation is worse than none</b>, because it is "
            "trusted."]},

  {"t": "bullets", "kicker": "Executable", "title": "Documentation that cannot lie",
   "items": [
     "<b>Types</b> — checked by the compiler. Cannot be wrong.",
     "<b>Tests</b> — executable examples. Fail if they become false.",
     "<b>Doctests</b> — examples in the docs, run by CI.",
     "<b>Generated reference</b> — derived from source.",
     "<b>Assertions</b> — invariants, checked at runtime.",
     "",
     "<b>Prefer these wherever possible.</b> Prose is for the things that "
     "cannot be expressed in code — which is mainly <i>why</i>.",
   ],
   "note": "'Documentation that cannot lie' is the useful framing for why "
           "types and tests count as docs."},

  {"t": "section", "label": "Part 3", "title": "Dependencies",
   "blurb": "Every one is a liability you took on."},

  {"t": "table", "kicker": "Dependencies", "title": "What a dependency costs",
   "header": ["Cost", "Detail"],
   "widths": [3.4, 8.7],
   "rows": [
     ["Security", "Their vulnerabilities become yours"],
     ["Upgrades", "Breaking changes on their schedule, not yours"],
     ["Abandonment", "<b>Maintainer stops; you inherit it</b>"],
     ["Transitive", "You get their dependencies too, unexamined"],
     ["Supply chain", "A compromised package runs with your privileges"],
     ["Build time", "Every one slows your pipeline"],
   ],
   "note": "Transitive dependencies are the under-appreciated cost — one "
           "direct dep can pull in hundreds."},

  {"t": "callout", "title": "The decision is not free either way",
   "kind": "Judgement",
   "body": ["<b>Taking a dependency</b> costs the items above, forever.",
            "<b>Writing it yourself</b> costs the implementation plus "
            "maintenance, and your version will have bugs the mature library "
            "fixed years ago.",
            "<b>Reasonable heuristics:</b> prefer dependencies that are "
            "small, that you could replace in a week, that are widely used "
            "and actively maintained, and whose licence you have actually "
            "read.",
            "<b>Be most cautious about trivial dependencies</b> — a "
            "ten-line package is all cost and no benefit, and the "
            "<code>left-pad</code> incident demonstrated the failure mode "
            "publicly."]},

  {"t": "section", "label": "Part 4", "title": "Deprecation and handover",
   "blurb": "Removing things, and leaving."},

  {"t": "bullets", "kicker": "Deprecation", "title": "Removing something people use",
   "items": [
     "<b>1. Announce,</b> with a date and a migration path. Not just a "
     "warning.",
     "<b>2. Provide the replacement</b> and make migration mechanical where "
     "possible.",
     "<b>3. Warn at use</b> — deprecation warnings in logs and build "
     "output.",
     "<b>4. Measure usage.</b> You cannot remove what you cannot see.",
     "<b>5. Remove</b>, on the announced date.",
     "",
     "<b>Skip step 4 and you will never remove anything</b>, because nobody "
     "can prove it is safe.",
   ],
   "note": "Usage telemetry is the step that makes deprecation possible at "
           "all."},

  {"t": "callout", "title": "The handover test",
   "kind": "The standard for this course",
   "body": ["<b>Could someone who has never seen this codebase become "
            "productive in a week?</b>",
            "Can they build it from a clean machine using only the README? "
            "Run the tests? Make a small change with confidence? Find out why "
            "a decision was made? Deploy it? Know what to do when it breaks?",
            "If the answer is no, the knowledge lives in your head, and that "
            "is a single point of failure — for the project and for "
            "you.",
            "<b>This is the test for Project 2</b>, and it is the test "
            "worth applying to everything you build afterwards."]},

  {"t": "bullets", "kicker": "End", "title": "Where this course leaves you",
   "items": [
     "You can judge a practice by whether it reduces the cost of the next "
     "change.",
     "You can design modules, test them meaningfully, review code without "
     "damage, and ship continuously.",
     "You can be sceptical about confident advice — including the advice "
     "here.",
     "",
     "<b>CSCE 641, 645, 647, 649</b> are where you build things worth "
     "maintaining.",
     "<b>CSCE 611, 614</b> are the machine underneath.",
     "<b>CSCE 713</b> takes security seriously.",
     "",
     "And the capstone is where all of it has to hold together at once.",
   ]},
 ],
 "takeaways": [
   "Code decays without being edited, because its environment changes. "
   "'We will not touch it' is not a maintenance strategy.",
   "Lehman: complexity increases as a system evolves <i>unless work is done "
   "to reduce it</i>. Refactoring offsets a law.",
   "Document what cannot be recovered from the code — decisions, "
   "constraints, rejected alternatives. Wrong documentation is worse than "
   "none.",
   "Prefer documentation that cannot lie: types, tests, doctests, generated "
   "reference, assertions.",
   "Every dependency is a permanent liability. Be most suspicious of trivial "
   "ones — all cost, no benefit.",
   "The handover test: could someone new be productive in a week? If not, the "
   "knowledge is a single point of failure.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why software decays"),
  ("callout", "The environment moves even when the code does not",
   ["Software does not wear out. What changes is everything around it: a "
    "dependency ships a breaking major version; an operating system removes a "
    "system call; a TLS certificate expires; a protocol version is disabled "
    "for security reasons; a third-party API alters a response format; the "
    "language runtime drops support for the version you pinned.",
    "So a system that nobody has edited for three years may not build, may "
    "not run, and may not be deployable — and the people who understood "
    "it have moved on.",
    "<b>Hyrum's law</b> compounds this: <i>with a sufficient number of users, "
    "every observable behaviour of your system will be depended upon by "
    "somebody</i> — including behaviours you never documented, never "
    "intended, and would describe as bugs. The implicit interface is "
    "everything the system does, not everything you promised.",
    "<b>The consequence is that 'we will not touch it' is not a maintenance "
    "strategy.</b> Untouched code becomes unbuildable, then unrunnable, then "
    "unreplaceable, and the cost of each stage is higher than the "
    "maintenance that was avoided."]),
  ("h2", "1.1 &nbsp; Lehman's laws"),
  ("p", "Meir Lehman studied how real systems evolve over decades. Two of his "
        "laws carry the engineering content."),
  ("table", ["Law", "Statement", "Implication"],
   [["<b>Continuing change</b>",
     "A system used in a real-world environment must be continually adapted, "
     "or it becomes progressively less satisfactory.",
     "Maintenance is not a failure of the original design. It is the "
     "condition of being useful."],
    ["<b>Increasing complexity</b>",
     "As a system evolves, its complexity increases <i>unless work is done to "
     "maintain or reduce it</i>.",
     "<b>This is the actionable one.</b> Complexity growth is the default "
     "state; reversing it requires deliberate, budgeted effort."]],
   [0.20, 0.42, 0.38]),
  ("p", "That conditional clause reframes Module 07 entirely. Refactoring is "
        "not tidying or polish or professional pride. It is the work that "
        "offsets a documented tendency, and a project that does none is not "
        "staying still — it is losing ground."),

  ("h1", "2 &nbsp; Documentation"),
  ("p", "The Di&aacute;taxis framework distinguishes four kinds of "
        "documentation serving four different needs. Most projects write only "
        "one of them and are puzzled that nobody can use the system."),
  ("table", ["Kind", "Serves", "Question it answers", "Rate of rot"],
   [["<b>Tutorial</b>", "A newcomer learning.", "How do I get started?",
     "Slow — but when it breaks, it blocks everyone new."],
    ["<b>How-to guide</b>", "A competent user with a task.",
     "How do I accomplish X?", "Moderate."],
    ["<b>Reference</b>", "Someone who knows what they want.",
     "What are the parameters and return values?",
     "<b>Fast. Generate it from source</b> so it cannot diverge."],
    ["<b>Explanation</b>", "Someone trying to understand.",
     "<b>Why is it built this way?</b>",
     "<b>Very slow</b>, because the reasons do not change. The most valuable "
     "and the least written."]],
   [0.16, 0.22, 0.32, 0.30]),
  ("callout", "Document what cannot be recovered from the code",
   ["<b>What the code does</b> is recoverable by reading it. Prose restating "
    "it duplicates knowledge (Module 03's DRY), so it drifts out of date and "
    "then actively misleads — and because it is documentation, it is "
    "trusted.",
    "<b>Why the code does it</b> is not recoverable. Which approach was tried "
    "and abandoned, which external constraint forced the awkward structure, "
    "which production incident this guard clause commemorates, which "
    "obvious-looking simplification is wrong.",
    "<b>So document decisions, constraints, and rejected alternatives</b> "
    "— architecture decision records (Module 04), commit message bodies "
    "(Module 08), and comments that explain reasoning rather than mechanism.",
    "<b>Wrong documentation is worse than no documentation</b>, because a "
    "reader with none knows to read the code, and a reader with wrong "
    "documentation does not."]),
  ("callout", "Prefer documentation that cannot lie",
   ["<b>Types</b> are checked by the compiler and cannot be stale.",
    "<b>Tests</b> are executable examples that fail the build if they stop "
    "being true (Module 05).",
    "<b>Doctests</b> put examples in the documentation and execute them in "
    "CI, so the examples in your README are verified.",
    "<b>Generated reference</b> is derived from the source and cannot "
    "diverge from it.",
    "<b>Assertions</b> state invariants and check them at runtime "
    "(Module 02).",
    "Each of these is documentation that the build system maintains for you. "
    "Reserve prose for what genuinely cannot be expressed in code — "
    "which, as above, is mostly <i>why</i>."]),

  ("break",),
  ("h1", "3 &nbsp; Dependencies"),
  ("table", ["Cost", "Detail"],
   [["<b>Security</b>", "Their vulnerabilities become yours, on their "
     "disclosure timeline, and you must respond."],
    ["<b>Upgrade burden</b>", "Breaking changes arrive on their schedule. "
     "Falling behind makes catching up harder, and the gap compounds."],
    ["<b>Abandonment</b>", "The maintainer loses interest or moves on. You "
     "now own a codebase you did not write and did not choose."],
    ["<b>Transitive closure</b>", "You acquire their dependencies too, "
     "unexamined. One direct dependency can bring hundreds of indirect ones, "
     "each with all of these costs."],
    ["<b>Supply chain risk</b>", "A compromised package executes with your "
     "application's privileges, in your build system, with your secrets in "
     "the environment."],
    ["<b>Build time</b>", "Every dependency slows the pipeline, which "
     "Module 10 showed changes behaviour."],
    ["<b>Licence obligations</b>", "Which someone must have actually read."]],
   [0.22, 0.78]),
  ("callout", "Both options cost something",
   ["<b>Taking a dependency</b> incurs everything above, permanently.",
    "<b>Writing it yourself</b> costs implementation and ongoing maintenance, "
    "and your version will contain bugs that the mature library fixed years "
    "ago — date handling, Unicode, timezone edge cases, and character "
    "encoding are the classic examples, and reimplementing any of them is "
    "almost always a mistake.",
    "<b>Useful heuristics:</b> prefer dependencies that are small in scope, "
    "that you could replace in a week if abandoned, that are widely used and "
    "actively maintained, whose source you could read if you had to, and "
    "whose licence is compatible with your use.",
    "<b>Be most suspicious of trivial dependencies.</b> A package of ten "
    "lines carries every cost above and saves ten lines. The "
    "<code>left-pad</code> incident — where the removal of an "
    "eleven-line package broke a substantial share of the JavaScript "
    "ecosystem — demonstrated the failure mode publicly and at scale."]),

  ("h1", "4 &nbsp; Deprecation"),
  ("p", "Removing something that people depend on is a process, not an event, "
        "and skipping steps is how systems accumulate functionality nobody "
        "dares delete."),
  ("ol", ["<b>Announce</b>, with a specific removal date and a documented "
          "migration path. A warning with no date and no alternative is "
          "noise that users correctly ignore.",
          "<b>Provide the replacement</b> before deprecating, and make "
          "migration mechanical where possible — a codemod, a shim, or "
          "a compatibility layer. Every manual step reduces the proportion of "
          "users who migrate.",
          "<b>Warn at the point of use.</b> Deprecation warnings in logs, "
          "build output, and IDE hints reach people who never read "
          "announcements.",
          "<b>Measure usage.</b> Instrument the deprecated path so you know "
          "who is still calling it and how often.",
          "<b>Remove</b>, on the announced date."]),
  ("p", "<b>Step 4 is the one that is skipped, and it is the one that makes "
        "the process work.</b> Without usage data, nobody can demonstrate "
        "that removal is safe, so removal is deferred indefinitely, so the "
        "deprecated path is maintained forever alongside its replacement "
        "— which is strictly worse than never having deprecated it."),

  ("h1", "5 &nbsp; The handover test"),
  ("callout", "Could someone new be productive in a week?",
   ["This is the standard this course has been building toward, and it is "
    "concrete enough to check.",
    "<b>Can they build it</b> from a clean machine, following only the "
    "README, without asking anyone? <b>Can they run the tests</b> and "
    "understand what failure means? <b>Can they make a small change</b> and "
    "be confident they have not broken anything? <b>Can they find out why</b> "
    "a surprising decision was made? <b>Can they deploy it</b>? <b>Do they "
    "know what to do</b> when it breaks at two in the morning?",
    "If the answer to any of these is no, the missing knowledge is in "
    "somebody's head, and that is a single point of failure — for the "
    "project, and for the person, who can now never leave the project "
    "cleanly.",
    "<b>This is the test for Project 2</b>, and it is worth applying to "
    "everything you build afterwards. It is also the most direct expression "
    "of Module 01's framing: software engineering is programming integrated "
    "over time, and the integral includes the people who come after you."]),
  ("p", "Where this course leaves you: able to judge a practice by whether it "
        "reduces the cost of the next change; able to design modules that "
        "absorb change, test them meaningfully, review code without damaging "
        "people, and ship continuously; and appropriately sceptical of "
        "confident claims in a field with more opinion than evidence "
        "— including the claims made here."),
  ("p", "The other courses in this program are where you build things worth "
        "maintaining. <b>CSCE 641, 645, 647, and 649</b> produce codebases "
        "large enough that these practices matter. <b>CSCE 611 and 614</b> "
        "are the machine underneath. <b>CSCE 713</b> takes security "
        "seriously. And the capstone is where all of it has to hold together "
        "at the same time, which is the only real test."),
 ],
 "resources": [
   ("Software Engineering at Google — Chapters 1, 10, 21, 22 (time, "
    "documentation, dependencies, large-scale change)",
    "https://abseil.io/resources/swe-book",
    "Hyrum's law, dependency management at scale, and how to make a change "
    "across millions of lines. The deprecation material is particularly "
    "good."),
   ("Diátaxis documentation framework",
    "https://diataxis.fr/",
    "The four-kind taxonomy of &sect;2. Short, practical, and it immediately "
    "explains why most project documentation fails."),
   ("Lehman — Programs, Life Cycles, and Laws of Software Evolution "
    "(free summaries)",
    "https://en.wikipedia.org/wiki/Lehman%27s_laws_of_software_evolution",
    "The laws, with the empirical work behind them."),
   ("Michael Feathers — Working Effectively with Legacy Code",
    "https://www.oreilly.com/library/view/working-effectively-with/0131177052/",
    "What to do when you inherit a system that fails the handover test."),
 ],
 "exercises": [
   "Take a project of yours from more than a year ago and try to build it on "
   "a clean machine. Record every step that fails, and fix the README until "
   "it does not.",
   "Apply the handover test to your Project 1 repository. Have someone else "
   "attempt each item and record where they get stuck.",
   "Audit the dependencies of a project: count direct and transitive, check "
   "each direct one's last release date and open issue count, and identify "
   "any that look abandoned.",
   "Find a trivial dependency — under fifty lines — and inline it. "
   "Assess whether the project is better off.",
   "Write an architecture decision record for a decision in your code that "
   "would surprise a newcomer.",
   "Classify an existing project's documentation using Di&aacute;taxis. "
   "Identify which of the four kinds is missing and write a page of it.",
   "Find a deprecated API in a library you use. Assess the deprecation "
   "against &sect;4's five steps and report which were done.",
   "<b>Project 2 is now due.</b> Submit your merged open-source contribution "
   "with the full review conversation and your written reflection.",
 ],
 "selfcheck": [
   "Why does code decay without being modified? Give three concrete causes.",
   "State Hyrum's law and say what follows for maintaining a public "
   "interface.",
   "Which of Lehman's laws contains the engineering content, and what clause "
   "carries it?",
   "What should documentation record, and why is wrong documentation worse "
   "than none?",
   "Name four forms of documentation that cannot become stale.",
   "List four costs of taking a dependency, and say which kind to be most "
   "suspicious of.",
   "Give the five steps of deprecation and say which is usually skipped and "
   "why that matters.",
   "State the handover test and explain why failing it is a risk to you "
   "personally.",
 ],
},

]
