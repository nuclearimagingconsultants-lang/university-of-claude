# -*- coding: utf-8 -*-
"""CSCE 632 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Semantics and the Accessibility Tree",
 "subtitle": "The mechanism, from which most of the rules follow.",
 "question": "What does the assistive technology actually receive?",
 "outcomes": [
     "Explain the accessibility tree and how it is derived.",
     "Explain the name-role-value-state model.",
     "State the rules of ARIA and why the first one exists.",
     "Explain live regions and announcing change.",
     "Derive a rule from the mechanism rather than recalling it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The tree",
   "blurb": "Which is what is actually exposed."},

  {"t": "callout", "title": "An assistive technology reads a separate tree that your markup generates, not your markup and not your pixels",
   "kind": "The mechanism the whole course depends on",
   "body": ["<b>The platform builds an accessibility tree from your "
            "document</b> — <b>a parallel structure of nodes, each "
            "with a role, a name, a value, and a set of "
            "states</b> — and <b>the assistive technology reads that "
            "tree through a platform API.</b>",
            "<b>Which means your visual design is invisible to it "
            "and your semantics are everything</b> — <b>a "
            "<code>div</code> with a click handler produces a node with "
            "no role and no name</b>, however it looks.",
            "<b>And nodes can be absent</b>: <b>decorative images, "
            "<code>display: none</code> content, and "
            "<code>aria-hidden</code> subtrees are pruned</b>, which is "
            "sometimes what you want and is sometimes the "
            "bug.",
            "<b>So the debugging question is always 'what is in the "
            "tree'</b> — <b>and every browser's inspector will show "
            "you</b>, which turns most accessibility debugging into "
            "reading a data structure."]},

  {"t": "code", "kicker": "Inspect", "title": "What to look at, and in what order",
   "lang": "text", "code": """
  OPEN THE ACCESSIBILITY PANE and for each control
  check the four things:

      ROLE    what kind of thing is this?
              button, link, checkbox, heading...
              missing role => "generic", unusable

      NAME    what is it called?
              from content, label, aria-label,
              aria-labelledby, or alt
              missing name => "button", unidentified

      VALUE   what does it currently hold?
              text entered, option selected,
              slider position

      STATE   checked, expanded, selected, disabled,
              invalid, current, pressed

  THEN THE TREE SHAPE
      is the heading outline right?
      are landmarks present?
      is anything missing that should be there?
      is anything there that should not be?
""",
   "caption": "<b>Role, name, value, state — for every "
              "control</b>, and the accessibility pane in any browser "
              "shows all four.",
   "note": "This four-item check is the mechanical core of the "
           "course."},

  {"t": "section", "label": "Part 2", "title": "Native first",
   "blurb": "Because the native element brings everything with it."},

  {"t": "callout", "title": "A native button is a role, a name, keyboard operability, focus, and state, for free",
   "kind": "Why this is not a style preference",
   "body": ["<b>&lt;button&gt; gives you the button role, the "
            "accessible name from its content, Enter and Space "
            "activation, focusability, a focus ring, and the disabled "
            "state</b> — all of it, in every browser and "
            "platform.",
            "<b>A div with a click handler gives you none of "
            "it</b> — and <b>reproducing all of it correctly takes a "
            "role, a tabindex, two key handlers, a focus style, and "
            "state management</b>, each of which can be wrong.",
            "<b>So the rule is: use the native element</b>, and "
            "<b>the reason is that it is less code and more "
            "correct</b>, which is an engineering argument rather than a "
            "compliance one.",
            "<b>And this extends everywhere:</b> <b>native form "
            "controls, native dialogs, native details, native "
            "tables</b> — <b>each carries a keyboard model and a "
            "semantic contract you would otherwise owe.</b>"]},

  {"t": "section", "label": "Part 3", "title": "ARIA",
   "blurb": "And its first rule, which is the important one."},

  {"t": "bullets", "kicker": "ARIA", "title": "The rules, in order of how often they are broken",
   "items": [
     "<b>1 · Do not use ARIA if a native element will "
     "do</b> — <b>no ARIA is better than bad ARIA</b>, and bad "
     "ARIA is actively worse than none because it asserts something "
     "false.",
     "",
     "<b>2 · Do not change native semantics unless you must</b> "
     "— giving a heading a button role removes it from the "
     "heading outline.",
     "",
     "<b>3 · Every interactive ARIA control must be keyboard "
     "operable</b> — <b>a role does not bring behaviour with "
     "it</b>, which is the commonest misunderstanding.",
     "",
     "<b>4 · Do not use <code>role=\"presentation\"</code> or "
     "<code>aria-hidden</code> on a focusable element</b> — which "
     "produces a control that can be focused and cannot be "
     "identified.",
     "",
     "<b>5 · Every interactive element needs an accessible "
     "name</b> — and the icon-only button is where this is "
     "missed.",
   ],
   "footnote": "<b>ARIA changes what is announced and never what "
               "anything does</b> — so a role without the matching "
               "keyboard behaviour is a lie the user acts "
               "on."},

  {"t": "callout", "title": "Because ARIA is a promise about behaviour that you then have to keep",
   "kind": "The mechanism behind the first rule",
   "body": ["<b>Adding <code>role=\"checkbox\"</code> tells the user "
            "that Space will toggle it and that its checked state will "
            "be announced</b> — <b>and the browser does not implement "
            "either of those for you.</b>",
            "<b>So the user is told what to expect and the "
            "expectation fails</b> — <b>which is worse than an "
            "unlabelled element</b>, because an unidentified control "
            "invites caution and a mislabelled one invites "
            "confidence.",
            "<b>Which is the real content of the first rule:</b> "
            "<b>the native element keeps the promise and your ARIA "
            "makes it</b>, and those are not symmetric "
            "amounts of work.",
            "<b>And it is a general pattern worth "
            "noticing</b> — <b>a declaration you have to keep "
            "manually synchronised with behaviour will drift</b>, which "
            "is CSCE 713 §01's make-the-defect-unexpressible "
            "argument applied here."]},

  {"t": "section", "label": "Part 4", "title": "Change",
   "blurb": "Which is where modern interfaces fail."},

  {"t": "callout", "title": "A serial user does not perceive change unless it is announced",
   "kind": "The characteristic defect of dynamic interfaces",
   "body": ["<b>A search result count updating, a validation error "
            "appearing, a toast notification, an item added to a "
            "cart</b> — <b>all visible, none announced</b>, and the "
            "user continues unaware (Module 03 §2's serial "
            "channel).",
            "<b>So a region that updates must be declared a live "
            "region</b>, with a politeness level: <b>polite waits for a "
            "pause, assertive interrupts</b>, and assertive is almost "
            "always the wrong choice.",
            "<b>And focus management is the other half</b>: "
            "<b>opening a dialog moves focus into it, closing returns "
            "focus where it came from</b>, and route changes in a "
            "single-page application need an explicit announcement and "
            "focus move.",
            "<b>Which is the one area where a framework will not "
            "save you</b> — <b>because the framework does not know "
            "which of its re-renders are meaningful to a user</b>, and "
            "only you do."]},

  {"t": "callout", "title": "And this is why the mechanism is worth the hour it takes",
   "kind": "Closing",
   "body": ["<b>Once you know what the tree contains, most of the "
            "rules become derivable</b> — <b>'why does an icon button "
            "need a label' has an answer rather than a citation</b>, "
            "which is CSCE 671 §05's mechanism-over-rule "
            "argument.",
            "<b>And the four-item check "
            "generalises</b>: <b>role, name, value, state, on every "
            "control</b> — which is a complete audit procedure for "
            "the semantic half of this course.",
            "<b>Plus it is inspectable</b> — <b>the tree is right "
            "there in the browser</b>, which makes this the most "
            "debuggable part of accessibility and the part people "
            "nonetheless guess at.",
            "<b>So the habit to build is: open the accessibility "
            "pane while you build the control</b>, not after — "
            "<b>because the four items are a specification and not a "
            "test.</b>"]},
 ],
 "takeaways": [
   "An assistive technology reads a separate accessibility tree your markup "
   "generates, not your markup and not your pixels.",
   "Check role, name, value, and state for every control, and the browser's "
   "accessibility pane shows all four.",
   "A native button brings a role, a name, keyboard operability, focus, and "
   "state for free; a div with a handler brings none of them.",
   "ARIA changes what is announced and never what anything does, so a role "
   "without the matching keyboard behaviour is a lie the user acts on.",
   "A mislabelled control invites confidence and an unidentified one "
   "invites caution, which is why bad ARIA is worse than none.",
   "A framework cannot manage your live regions, because it does not know "
   "which re-renders are meaningful.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The tree"),
  ("callout", "An assistive technology reads a separate tree that your markup "
              "generates, not your markup and not your pixels",
   ["<b>The platform builds an accessibility tree from your "
    "document</b> — <b>a parallel structure of nodes, each carrying "
    "a role, an accessible name, a value, and a set of states</b> — "
    "and <b>the assistive technology reads that tree through a platform "
    "accessibility API</b>, never the DOM directly and never the "
    "rendered pixels.",
    "<b>Which means your visual design is entirely invisible to it "
    "and your semantics are everything</b> — <b>a <code>div</code> "
    "with a click handler and a background image produces a node with no "
    "role and no name</b>, <b>however convincing it looks</b>, and is "
    "announced as nothing at all.",
    "<b>And nodes can be absent from the tree</b>: <b>images marked "
    "decorative, <code>display: none</code> content, "
    "<code>visibility: hidden</code>, and <code>aria-hidden</code> "
    "subtrees are all pruned</b> — <b>which is sometimes exactly "
    "what you want and is sometimes the bug</b>, and the two cases look "
    "identical in the browser.",
    "<b>So the debugging question is always 'what is in the "
    "tree'</b> — <b>and every major browser's inspector will show "
    "you</b>, which <b>turns most accessibility debugging into reading a "
    "data structure</b> rather than into guessing from a "
    "checklist."]),
  ("code", """OPEN THE ACCESSIBILITY PANE and for each control
check the four things:

    ROLE    what kind of thing is this?
            button, link, checkbox, heading, table...
            missing role => "generic", and unusable

    NAME    what is it called?
            from its content, a label element,
            aria-label, aria-labelledby, or alt
            missing name => "button", unidentified

    VALUE   what does it currently hold?
            the text entered, the option selected,
            the slider position

    STATE   checked, expanded, selected, disabled,
            invalid, current, pressed, busy

THEN THE TREE SHAPE
    is the heading outline right?
    are the landmarks present?
    is anything missing that should be there?
    is anything there that should not be?"""),
  ("p", "<b>Role, name, value, state — for every control</b>, and "
        "<b>the accessibility pane in any browser shows all four</b> "
        "beside the element. <b>This four-item check is the mechanical "
        "core of the course</b>: it is what a screen reader announces, it "
        "is what voice control matches against, and it is what the "
        "automated checkers are actually inspecting. Doing it while you "
        "build a control rather than afterwards is the habit this module "
        "is trying to install (&sect;4's closing callout)."),

  ("h1", "2 &nbsp; Native first"),
  ("callout", "A native button is a role, a name, keyboard operability, "
              "focus, and state, for free",
   ["<b>A <code>button</code> element gives you the button role, an "
    "accessible name computed from its content, activation on both Enter "
    "and Space, focusability in the right tab position, a platform focus "
    "indicator, and the disabled state</b> — <b>all of it, in every "
    "browser and on every platform</b>, maintained by somebody else.",
    "<b>A <code>div</code> with a click handler gives you none of "
    "it</b> — and <b>reproducing all of it correctly takes a role, "
    "a <code>tabindex</code>, two separate key handlers, a focus style, "
    "and explicit state management</b>, <b>each of which can be wrong "
    "and one of which usually is.</b>",
    "<b>So the rule is: use the native element</b>, and <b>the "
    "reason is that it is less code and more correct</b> — <b>which "
    "is an engineering argument rather than a compliance one</b>, and is "
    "therefore the version to make in a code review.",
    "<b>And this extends everywhere</b>: <b>native form controls, "
    "the native dialog element, <code>details</code>, real "
    "<code>table</code> markup with header cells, "
    "<code>fieldset</code> and <code>legend</code></b> — <b>each "
    "carries a keyboard model and a semantic contract you would "
    "otherwise owe</b> and would have to keep in sync forever."]),

  ("break",),
  ("h1", "3 &nbsp; ARIA"),
  ("ul", ["<b>1 &middot; Do not use ARIA if a native element will "
          "do</b> — <b>no ARIA is better than bad ARIA</b>, and "
          "<b>bad ARIA is actively worse than none</b> because it "
          "asserts something false about the control (see the "
          "callout).",
          "<b>2 &middot; Do not change native semantics unless you "
          "really must</b> — <b>giving a heading a button role "
          "removes it from the heading outline</b>, which removes it "
          "from the navigation (Module 03 &sect;2).",
          "<b>3 &middot; Every interactive ARIA control must be "
          "keyboard operable</b>, with the keyboard model its role "
          "implies — <b>a role does not bring behaviour with "
          "it</b>, <b>which is the commonest misunderstanding of what "
          "ARIA is.</b>",
          "<b>4 &middot; Do not put <code>role=\"presentation\"</code> "
          "or <code>aria-hidden=\"true\"</code> on a focusable "
          "element</b> — <b>which produces a control that can be "
          "focused and cannot be identified</b>, and is a particularly "
          "confusing failure.",
          "<b>5 &middot; Every interactive element needs an accessible "
          "name</b> — <b>and the icon-only button is where this is "
          "missed</b>, universally. <b>ARIA changes what is announced "
          "and never what anything does</b> — <b>so a role without "
          "the matching keyboard behaviour is a lie the user acts "
          "on.</b>"]),
  ("callout", "Because ARIA is a promise about behaviour that you then have "
              "to keep",
   ["<b>Adding <code>role=\"checkbox\"</code> tells the user that "
    "Space will toggle this control and that its checked state will be "
    "announced</b> — <b>and the browser does not implement either "
    "of those for you</b>: the role is a declaration, not an "
    "implementation.",
    "<b>So the user is told what to expect and the expectation "
    "fails</b> — <b>which is worse than an unlabelled "
    "element</b>, <b>because an unidentified control invites caution and "
    "a mislabelled one invites confidence</b>, and acting confidently on "
    "false information is how data gets lost.",
    "<b>Which is the real content of the first rule:</b> <b>the "
    "native element keeps the promise and your ARIA merely makes "
    "it</b> — <b>and those are not symmetric amounts of work</b>, "
    "which is the whole argument in one sentence.",
    "<b>And it is a general pattern worth noticing</b> — <b>a "
    "declaration that has to be kept manually synchronised with "
    "behaviour will drift</b> — <b>which is CSCE 713 Module 01's "
    "make-the-defect-unexpressible argument applied here</b>: the native "
    "element makes the desynchronisation impossible to express."]),

  ("h1", "4 &nbsp; Change"),
  ("callout", "A serial user does not perceive change unless it is announced",
   ["<b>A search result count updating, a validation error appearing "
    "beneath a field, a toast notification, an item added to a cart, a "
    "progress bar advancing</b> — <b>all visible, none "
    "announced</b>, <b>and the user continues entirely unaware</b> "
    "(Module 03 &sect;2's serial channel with a cursor).",
    "<b>So a region that updates must be declared a live "
    "region</b>, with a politeness level: <b><code>polite</code> waits "
    "for a pause in speech, <code>assertive</code> interrupts "
    "immediately</b> — <b>and assertive is almost always the wrong "
    "choice</b>, because interrupting somebody mid-sentence loses their "
    "place.",
    "<b>And focus management is the other half of this</b>: "
    "<b>opening a dialog moves focus into it, closing it returns focus "
    "to the control that opened it</b>, and <b>route changes in a "
    "single-page application need both an explicit announcement and a "
    "deliberate focus move</b>, since no page load happened to do it for "
    "you.",
    "<b>Which is the one area where a framework will not save "
    "you</b> — <b>because the framework does not know which of its "
    "re-renders are meaningful to a user</b> and which are incidental, "
    "<b>and only you do</b>. This is the defect class to look for first "
    "in any application that does not reload pages."]),
  ("callout", "And this is why the mechanism is worth the hour it takes",
   ["<b>Once you know what the accessibility tree contains, most of "
    "the rules become derivable rather than memorised</b> — <b>'why "
    "does an icon-only button need a label' has an answer rather than a "
    "citation</b> — <b>which is CSCE 671 Module 05's "
    "mechanism-over-rule argument</b> and the same payoff.",
    "<b>And the four-item check generalises to everything</b>: "
    "<b>role, name, value, state, on every control</b> — <b>which "
    "is a complete audit procedure for the semantic half of this "
    "course</b> and needs no checklist to remember.",
    "<b>Plus it is directly inspectable</b> — <b>the tree is "
    "right there in the browser's developer tools</b> — <b>which "
    "makes this the most debuggable part of accessibility and the part "
    "people nonetheless guess at</b> most often.",
    "<b>So the habit to build is: open the accessibility pane while "
    "you are building the control</b>, not after it is "
    "finished — <b>because the four items are a specification and "
    "not a test</b>, and treating them as a specification is what makes "
    "the repair work in Project 2 unnecessary next time."]),
 ],
 "resources": [
   ("The ARIA Authoring Practices Guide (free)",
    "https://www.w3.org/WAI/ARIA/apg/",
    "<b>&sect;&sect;2 and 3</b> — patterns with their required "
    "keyboard models, which is the part the role alone does not give "
    "you."),
   ("Using ARIA: the five rules (free)",
    "https://www.w3.org/TR/using-aria/",
    "<b>&sect;3's list in the original</b>, with the reasoning for each "
    "and the first rule stated unambiguously."),
   ("The Accessible Name and Description Computation (free)",
    "https://www.w3.org/TR/accname/",
    "<b>&sect;1's name derivation</b> — the precedence order, which "
    "explains surprising announcements."),
   ("The HTML Accessibility API Mappings (free)",
    "https://www.w3.org/TR/html-aam/",
    "<b>&sect;2's 'for free'</b>, specified — exactly what each "
    "native element contributes to the tree."),
 ],
 "exercises": [
   "<b>Open the accessibility pane</b> on three pages and read the "
   "tree.",
   "<b>Record role, name, value, and state</b> for ten controls in your "
   "own project.",
   "<b>Find a control with a generic role</b> and fix it natively.",
   "<b>Build a button twice</b> — natively, and from a div — "
   "and compare the line counts and the trees.",
   "<b>Find an <code>aria-hidden</code> that hides something "
   "focusable.</b>",
   "<b>Add <code>role=\"checkbox\"</code> to a div</b> and observe what "
   "does and does not happen.",
   "<b>Audit every icon-only button</b> in your project for an "
   "accessible name.",
   "<b>Find three unannounced changes</b> in an application you use "
   "daily.",
   "<b>Add a polite live region</b> to one of them and test it with a "
   "screen reader.",
   "<b>Open and close a dialog</b> and verify focus returns "
   "correctly.",
 ],
 "selfcheck": [
   "What does an assistive technology actually read?",
   "Name the four properties of a node.",
   "When are nodes pruned from the tree, and why is that ambiguous?",
   "List what a native button provides.",
   "Why is 'use the native element' an engineering argument?",
   "State the five rules of ARIA.",
   "Why is bad ARIA worse than none?",
   "What does ARIA change and what does it not?",
   "Why does a serial user miss change, and what are the two fixes?",
   "Why can a framework not handle live regions for you?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Testing",
 "subtitle": "What each method catches, measured.",
 "question": "Your checker says zero errors. What does that mean?",
 "outcomes": [
     "State what automated testing can and cannot detect.",
     "Describe a manual testing procedure.",
     "Give examples of conformant but unusable interfaces.",
     "Explain testing with disabled participants, and pay for it.",
     "Build a testing plan with stated coverage.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Automated coverage",
   "blurb": "The number everybody should know and almost nobody does."},

  {"t": "callout", "title": "Automated tools can detect roughly a third of the success criteria, and that is the optimistic framing",
   "kind": "The measurement this module is built on",
   "body": ["<b>Published estimates put fully automatable criteria "
            "at around 30% or less</b> — <b>and the automatable ones "
            "are the mechanical ones</b>: missing alt attributes, "
            "contrast ratios, missing form labels, invalid "
            "ARIA.",
            "<b>Which are real defects and are worth catching "
            "cheaply</b> — <b>a checker in continuous integration "
            "prevents regressions</b>, and that is a genuine and "
            "worthwhile use.",
            "<b>But a tool cannot judge whether alt text is "
            "<i>correct</i></b>, whether a heading structure is "
            "<i>meaningful</i>, whether a focus order is "
            "<i>sensible</i>, or whether a task is "
            "<i>completable</i>.",
            "<b>So 'zero errors' means 'no detectable errors in "
            "about a third of the criteria'</b> — <b>which is how "
            "false conformance claims happen without anybody "
            "lying</b> (Module 07 §2)."]},

  {"t": "table", "kicker": "Coverage", "title": "What each method finds, and what it costs",
   "header": ["Method", "Finds", "Cost"],
   "widths": [2.9, 4.5, 3.8],
   "rows": [
     ["<b>Automated checker</b>", "<b>Mechanical defects, ~1/3 of criteria</b>", "<b>Seconds; put it in CI</b>"],
     ["<b>Keyboard-only pass</b>", "<b>Operability, focus, traps</b>", "<b>Minutes, high yield</b>"],
     ["<b>Screen reader pass</b>", "<b>Semantics, naming, change</b>", "<b>Longer; needs skill</b>"],
     ["<b>Zoom and reflow pass</b>", "<b>Layout failures at 400%</b>", "<b>Seconds</b>"],
     ["<b>Expert review</b>", "<b>Most of the rest</b>", "<b>Hours; needs expertise</b>"],
     ["<b>Users with disabilities</b>", "<b>What nothing else finds</b>", "<b>Paid, scheduled, worth it</b>"],
   ],
   "footnote": "<b>The methods are complementary and not "
               "substitutable</b> — each row finds a class the rows "
               "above it structurally cannot, which is why a plan names "
               "all six.",
   "note": "The complementary-not-substitutable point is the "
           "module's organising claim."},

  {"t": "section", "label": "Part 2", "title": "The manual pass",
   "blurb": "An order that works."},

  {"t": "code", "kicker": "Procedure", "title": "A manual audit, in order",
   "lang": "text", "code": """
  1  RUN THE CHECKER FIRST
         it is free, and it clears the mechanical
         noise so your attention is spent on the
         rest

  2  KEYBOARD ONLY
         the five properties (Module 05 section 2)
         on the three most important tasks

  3  ZOOM TO 400% AND CHECK REFLOW
         plus magnifier, for distant dependencies

  4  CONTRAST AND GREYSCALE
         numeric, and fast

  5  SCREEN READER
         the same three tasks, eyes closed
         recording what is announced for each step

  6  READ THE TREE
         role, name, value, state (Module 08)
         for every control in those tasks

  7  THEN THE CONTENT
         headings, link text, language, errors
""",
   "caption": "<b>Checker first, then keyboard, then screen "
              "reader</b> — the cheap and broad passes before the "
              "slow and deep ones."},

  {"t": "section", "label": "Part 3", "title": "Conformant and unusable",
   "blurb": "Which is the gap, made concrete."},

  {"t": "bullets", "kicker": "The gap", "title": "Interfaces that pass every criterion and fail every user",
   "items": [
     "<b>A form where every field is labelled "
     "<i>correctly</i> and the labels are 'Field 1' through 'Field "
     "14'</b> — conformant, and "
     "unusable.",
     "",
     "<b>Alt text reading 'image'</b> on forty images — "
     "<b>present, accurate, and useless</b>, and no tool can tell the "
     "difference.",
     "",
     "<b>A heading structure that is perfectly nested and "
     "describes the layout rather than the content</b> — 'Header', "
     "'Sidebar', 'Content'.",
     "",
     "<b>A focus order that is complete and runs right-to-left "
     "down the page</b>, visiting the footer between two form "
     "fields.",
     "",
     "<b>And a flow of forty keyboard-accessible steps</b>, each "
     "conformant, that is unusable by switch access "
     "(Module 05 §1).",
   ],
   "footnote": "<b>Each of these passes every automated and most "
               "manual criteria</b> — which is what 'necessary, "
               "checkable, insufficient' means in practice "
               "(Module 07 §3)."},

  {"t": "section", "label": "Part 4", "title": "Testing with people",
   "blurb": "The only method that finds the last class, and how to do "
            "it properly."},

  {"t": "callout", "title": "Test with disabled participants, pay them properly, and recruit for the technology they actually use",
   "kind": "The requirement, with its conditions",
   "body": ["<b>Because expertise with the assistive technology is a "
            "skill</b> — <b>a daily screen reader user navigates "
            "faster than you will ever read</b>, and finds problems your "
            "slow careful pass cannot.",
            "<b>And they are testing your interface, not their "
            "ability</b> — <b>which is CSCE 671 §09's framing</b>, "
            "and it matters more here because the opposite framing is so "
            "readily available.",
            "<b>Pay market rate for the time</b>, as you would for "
            "any specialist consultancy — <b>unpaid accessibility "
            "testing by disabled people is extremely common and is not "
            "defensible.</b>",
            "<b>And recruit for the technology and the configuration, "
            "not for the diagnosis</b> — <b>'a daily NVDA user' and "
            "'a switch access user' are the recruitment "
            "criteria</b>, and five participants finds most of it "
            "(CSCE 671 §09 §3)."]},

  {"t": "callout", "title": "And the honest testing plan",
   "kind": "Closing",
   "body": ["<b>States each method, what it covers, and what it does "
            "not</b> — which converts a plan into a coverage "
            "claim.",
            "<b>Puts the automated check in continuous "
            "integration</b>, because <b>its real value is preventing "
            "regression rather than finding defects</b>, and that value "
            "is high.",
            "<b>Schedules the manual passes at a stated "
            "cadence</b>, since <b>a manual audit is a snapshot and "
            "interfaces change.</b>",
            "<b>And includes disabled participants, "
            "paid</b> — <b>without which the plan has a named gap</b>, "
            "which is better than an unnamed one and is what "
            "Module 13 §2 asks you to write down."]},
 ],
 "takeaways": [
   "Automated tools detect roughly a third of the success criteria, so "
   "'zero errors' means 'no detectable errors in about a third'.",
   "A tool cannot judge whether alt text is correct, whether a heading "
   "structure is meaningful, or whether a task is completable.",
   "The testing methods are complementary and not substitutable: each finds "
   "a class the cheaper ones structurally cannot.",
   "Run the checker first to clear the mechanical noise, then keyboard, "
   "then screen reader.",
   "Alt text reading 'image' on forty images is present, accurate, and "
   "useless — and no tool can tell.",
   "Pay disabled participants market rate; unpaid accessibility testing by "
   "disabled people is common and not defensible.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Automated coverage"),
  ("callout", "Automated tools can detect roughly a third of the success "
              "criteria, and that is the optimistic framing",
   ["<b>Published estimates put the fully automatable criteria at "
    "around 30% or less</b>, depending on how generously you count "
    "partial detection — <b>and the automatable ones are precisely "
    "the mechanical ones</b>: <b>missing <code>alt</code> attributes, "
    "computed contrast ratios, missing form labels, invalid ARIA "
    "attributes, duplicate ids.</b>",
    "<b>Which are real defects and are well worth catching "
    "cheaply</b> — <b>a checker in continuous integration prevents "
    "regressions on everything it can see</b>, <b>and that is a genuine "
    "and worthwhile use</b> that this module is not arguing "
    "against.",
    "<b>But a tool cannot judge whether the alt text is "
    "<i>correct</i></b>, whether a heading structure is "
    "<i>meaningful</i>, whether a focus order is <i>sensible</i>, "
    "whether a live region fires at the <i>right</i> time, or whether a "
    "task is <i>completable at all</i> — and those are where the "
    "real failures are (&sect;3).",
    "<b>So 'zero errors' means 'no detectable errors in about a "
    "third of the criteria'</b> — <b>which is how false conformance "
    "claims happen without anybody intending to lie</b> "
    "(Module 07 &sect;2): a green dashboard is read as a conformance "
    "result, and nothing in the dashboard says otherwise."]),
  ("table", ["Method", "What it finds", "What it costs"],
   [["<b>Automated checker</b>",
     "<b>Mechanical defects; roughly a third of the criteria, "
     "partially.</b>",
     "<b>Seconds. Put it in continuous integration.</b>"],
    ["<b>Keyboard-only pass</b>",
     "<b>Operability, focus visibility, focus order, keyboard "
     "traps.</b>",
     "<b>Minutes, and the highest yield per minute in the "
     "course.</b>"],
    ["<b>Screen reader pass</b>",
     "<b>Semantics, naming, announced change, structure.</b>",
     "<b>Longer, and it needs some skill with the tool.</b>"],
    ["<b>Zoom and reflow pass</b>",
     "<b>Layout failures at 200% and 400%, distant "
     "dependencies.</b>",
     "<b>Seconds.</b>"],
    ["<b>Expert review</b>",
     "<b>Most of the remaining criteria, and the judgement "
     "calls.</b>",
     "<b>Hours, and it needs genuine expertise.</b>"],
    ["<b>Testing with disabled users</b>",
     "<b>The class nothing else finds</b> (&sect;4).",
     "<b>Paid, scheduled, and worth it.</b>"]],
   [0.22, 0.42, 0.36]),
  ("p", "<b>The methods are complementary and not "
        "substitutable</b> — <b>each row finds a class of defect the "
        "rows above it structurally cannot</b>, <b>which is why a "
        "testing plan names all six</b> rather than choosing among them. "
        "<b>The complementary-not-substitutable point is the module's "
        "organising claim</b>, and it is the answer to 'we run axe in "
        "CI'."),

  ("h1", "2 &nbsp; The manual pass"),
  ("code", """1  RUN THE CHECKER FIRST
       it is free, and it clears the mechanical
       noise so that your attention is spent on the
       things only you can assess

2  KEYBOARD ONLY
       the five properties (Module 05 section 2)
       on the three most important tasks

3  ZOOM TO 400% AND CHECK REFLOW
       plus the magnifier, for distant dependencies

4  CONTRAST AND GREYSCALE
       numeric, and fast

5  SCREEN READER
       the same three tasks, eyes closed
       recording what is announced at each step

6  READ THE TREE
       role, name, value, state (Module 08)
       for every control in those tasks

7  THEN THE CONTENT
       headings, link text, language, error
       messages, and alt text quality"""),
  ("p", "<b>Checker first, then keyboard, then screen reader</b> "
        "— <b>the cheap and broad passes before the slow and deep "
        "ones</b>, so that the expensive attention is not spent on "
        "defects a tool would have found. Recording what is announced at "
        "each step of the screen reader pass is the part to be "
        "disciplined about: the transcript is the evidence, and the gap "
        "between it and what you assumed is the finding (Project 1's "
        "requirement)."),

  ("break",),
  ("h1", "3 &nbsp; Conformant and unusable"),
  ("ul", ["<b>A form where every field is labelled, the labels are "
          "programmatically associated, and the labels read 'Field 1' "
          "through 'Field 14'</b> — <b>fully conformant, and "
          "completely unusable</b>, and nothing in the standard says "
          "otherwise.",
          "<b>Alt text reading 'image' on forty images</b> — "
          "<b>present, accurate as a description of what it is, and "
          "entirely useless</b> — <b>and no tool can tell the "
          "difference</b> between that and a good description, because "
          "both are non-empty strings.",
          "<b>A heading structure that is perfectly nested and "
          "describes the layout rather than the content</b> — "
          "'Header', 'Sidebar', 'Content', 'Footer' — which passes "
          "every structural check and <b>provides no table of contents "
          "at all</b> (Module 03 &sect;2).",
          "<b>A focus order that is complete, visible, and runs "
          "right-to-left down the page</b>, visiting the footer between "
          "two fields of the same form — every element reachable, "
          "and the order meaningless.",
          "<b>And a flow of forty keyboard-accessible steps</b>, "
          "each one individually conformant, <b>that is simply not "
          "usable by switch access</b> (Module 05 &sect;1's step "
          "cost). <b>Each of these passes every automated and most "
          "manual criteria</b> — <b>which is what 'necessary, "
          "checkable, insufficient' means in practice</b> "
          "(Module 07 &sect;3)."]),

  ("h1", "4 &nbsp; Testing with people"),
  ("callout", "Test with disabled participants, pay them properly, and "
              "recruit for the technology they actually use",
   ["<b>Because expertise with the assistive technology is a real "
    "skill</b> — <b>a daily screen reader user navigates at speech "
    "rates you cannot follow</b>, uses operations you do not know, and "
    "<b>finds problems your slow careful pass structurally cannot</b>, "
    "as well as routing around ones you would call blockers.",
    "<b>And they are testing your interface, not their "
    "ability</b> — <b>which is CSCE 671 Module 09's "
    "framing</b>, and <b>it matters more here because the opposite "
    "framing is so readily available</b> and so damaging: a participant "
    "who struggles has found a defect, not demonstrated a limitation.",
    "<b>Pay market rate for the time</b>, as you would for any "
    "specialist consultancy, because that is what it is — <b>unpaid "
    "accessibility testing by disabled people is extremely common and is "
    "not defensible</b>, and 'we asked the community' is not a testing "
    "plan.",
    "<b>And recruit for the technology and the configuration rather "
    "than for the diagnosis</b> — <b>'a daily NVDA user on "
    "Windows', 'a switch access user', 'a magnifier user at 400%' are "
    "the recruitment criteria</b> (Module 01 &sect;3's capability "
    "framing) — <b>and five participants finds most of it</b>, for "
    "CSCE 671 Module 09 &sect;3's reasons."]),
  ("callout", "And the honest testing plan",
   ["<b>States each method, what it covers, and what it does "
    "not</b> — <b>which converts a plan into a coverage claim</b> "
    "and makes the remaining gap visible rather than implicit.",
    "<b>Puts the automated check in continuous integration</b>, "
    "because <b>its real value is preventing regression rather than "
    "finding defects</b> — <b>and that value is high</b>, since "
    "accessibility defects are reintroduced constantly by people who "
    "were not thinking about them.",
    "<b>Schedules the manual passes at a stated cadence</b>, since "
    "<b>a manual audit is a snapshot and interfaces change</b> "
    "— which is Module 12 &sect;4's process argument.",
    "<b>And includes disabled participants, paid</b> — "
    "<b>without which the plan has a named gap</b>, <b>which is better "
    "than an unnamed one</b> and <b>is exactly what Module 13 "
    "&sect;2 asks you to write down</b>: the thing you did not test, "
    "stated."]),
 ],
 "resources": [
   ("The WAI evaluation resources and WCAG-EM (free)",
    "https://www.w3.org/WAI/test-evaluate/",
    "<b>&sect;2</b> — a defined evaluation methodology, including "
    "sampling for large sites."),
   ("The WebAIM Million (free)",
    "https://webaim.org/projects/million/",
    "<b>&sect;1 at scale</b> — what automated testing finds across a "
    "million home pages, yearly, and the detectable-defect density is "
    "the headline."),
   ("Easy Checks: a first review of web accessibility (free)",
    "https://www.w3.org/WAI/test-evaluate/easy-checks/",
    "<b>&sect;2's short version</b> — the checks worth running before "
    "anything else, and a good basis for Project 1."),
   ("Deque's and WebAIM's coverage analyses (free)",
    "https://www.deque.com/automated-accessibility-testing-coverage/",
    "<b>&sect;1's number</b> — and read it critically, since the "
    "vendors have an interest in the figure being high."),
 ],
 "exercises": [
   "<b>State the automated coverage figure</b> and what 'zero errors' "
   "therefore means.",
   "<b>Run three different checkers</b> on one page and compare their "
   "findings.",
   "<b>Count the defects you find manually</b> that none of them "
   "reported.",
   "<b>Run §2's seven steps in order</b> on your own project.",
   "<b>Record a screen reader transcript</b> for one task, step by "
   "step.",
   "<b>Build a conformant unusable form</b>, deliberately, and run a "
   "checker on it.",
   "<b>Find a published site with 'image' alt text</b> at scale.",
   "<b>Write a recruitment criterion</b> by technology rather than by "
   "diagnosis.",
   "<b>Price five hours of specialist consultancy</b> in your market, "
   "as a payment baseline.",
   "<b>Write a testing plan</b> with each method's coverage and the "
   "remaining gap named.",
 ],
 "selfcheck": [
   "What fraction of criteria is automatable, and which ones?",
   "What is the real value of a checker in CI?",
   "Name four things a tool cannot judge.",
   "Name the six methods and what each finds.",
   "Why are they not substitutable?",
   "Give the manual pass in order, and say why the checker goes "
   "first.",
   "Give three conformant-but-unusable examples.",
   "Why can no tool detect bad alt text?",
   "Why test with disabled participants, and what is the framing?",
   "What does an honest testing plan contain?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Non-Visual Data",
 "subtitle": "Figures, tables, and the hardest requirement in the "
             "course.",
 "question": "What does a scatterplot sound like?",
 "outcomes": [
     "Explain why a figure is not an image for this purpose.",
     "Write a description that conveys what a figure shows.",
     "Make a data table non-visually navigable.",
     "Explain sonification and tactile alternatives.",
     "Make one of your own figures non-visually available.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "Which is harder than the alt-text rule suggests."},

  {"t": "callout", "title": "A figure's content is a relationship, and alt text for an image does not convey a relationship",
   "kind": "Why this needs its own module",
   "body": ["<b>'Bar chart of sales by region' says what the image "
            "is and nothing about what it shows</b> — <b>which is the "
            "characteristic failure</b> and is extremely "
            "common.",
            "<b>And the figure's point is a comparison, a trend, or "
            "an outlier</b> (CSCE 679 §01 §2's task framing) "
            "— <b>so the alternative has to carry the finding, not "
            "the picture.</b>",
            "<b>Which means it is a writing problem rather than a "
            "markup problem</b>, and is the only requirement in this "
            "course that cannot be met mechanically.",
            "<b>So the question to answer is: what would you say if "
            "you were describing this over the "
            "telephone?</b> — <b>which is the right prompt</b>, and "
            "produces usable descriptions almost "
            "immediately."]},

  {"t": "section", "label": "Part 2", "title": "The three layers",
   "blurb": "Which together do the job."},

  {"t": "code", "kicker": "Structure", "title": "Describe a figure in three layers",
   "lang": "text", "code": """
  1  THE SHORT ALTERNATIVE  (alt, or a caption)
         what kind of figure, what variables, and
         THE FINDING in one sentence
         "Sales rose in all four regions, with the
          north roughly doubling"

  2  THE LONGER DESCRIPTION  (nearby, in text)
         the axes with their units and ranges
         the normalisation (CSCE 679 Module 13)
         the shape: trend, groups, outliers
         anything a reader would ask about

  3  THE DATA ITSELF  (a real table, or a download)
         because the figure is a view of a table
         and the table is navigable, searchable,
         and exact

  AND LAYER 3 IS THE ONE PEOPLE SKIP AND THE ONE
  THAT MOST OFTEN SUFFICES -- it costs a markup
  table, and it makes every value available.
""",
   "caption": "<b>Layer 3 is the one people skip and the one that "
              "most often suffices</b> — the underlying table makes "
              "every value available exactly.",
   "note": "The three-layer structure is this module's main "
           "deliverable."},

  {"t": "callout", "title": "And a real data table is navigable in a way a figure never is",
   "kind": "Why the table deserves its own requirement",
   "body": ["<b>A screen reader navigates a properly marked table "
            "cell by cell, announcing the row and column headers for "
            "each</b> — <b>which is a genuinely good interface for "
            "exact values</b>, and better than a figure for lookup "
            "(CSCE 679 §01 §3).",
            "<b>But it requires the markup</b>: <b>header cells "
            "declared as headers, scope stated, a caption, and no "
            "layout tables</b> — and a table built from divs is "
            "announced as nothing.",
            "<b>And multi-level or merged headers need explicit "
            "association</b>, which is where table markup gets "
            "genuinely difficult — <b>so prefer a flat "
            "table.</b>",
            "<b>Which gives a useful default:</b> <b>publish the "
            "figure and the table together</b> — <b>sighted readers "
            "use the figure for shape and everybody uses the table for "
            "values</b>, which is a curb cut."]},

  {"t": "section", "label": "Part 3", "title": "Other channels",
   "blurb": "Sound and touch, honestly assessed."},

  {"t": "bullets", "kicker": "Alternatives", "title": "What the other channels can and cannot do",
   "items": [
     "<b>Sonification maps a value to pitch</b>, which conveys "
     "<b>trend and shape well and exact values badly</b> — so it "
     "complements a table rather than replacing "
     "it.",
     "",
     "<b>And it has the same channel-ranking problem as "
     "colour</b> — <b>pitch is a magnitude channel with poor "
     "accuracy</b>, so CSCE 679 §02's argument applies to it "
     "directly.",
     "",
     "<b>Tactile graphics and refreshable braille displays work "
     "well</b> and <b>require equipment most readers do not have</b>, "
     "which limits them to contexts where it is "
     "provided.",
     "",
     "<b>And structured exploration beats both</b> — "
     "<b>letting a user query the data (highest, lowest, this "
     "category) is frequently more useful than any "
     "rendering.</b>",
     "",
     "<b>So the honest ordering is: table, description, "
     "exploration, sonification</b>, in decreasing "
     "generality.",
   ],
   "footnote": "<b>Structured exploration beats sonification</b> "
               "— a user who can ask 'which is highest' has a "
               "better interface than one listening to a "
               "tune."},

  {"t": "section", "label": "Part 4", "title": "Practice",
   "blurb": "What to actually do, for every figure."},

  {"t": "callout", "title": "Every figure gets a one-sentence finding and a table, and that covers most of it",
   "kind": "Closing",
   "body": ["<b>The one-sentence finding is the alternative that "
            "matters</b> — <b>and writing it improves the figure's "
            "own caption</b>, because it forces you to say what the "
            "figure is for (CSCE 679 §13 §2).",
            "<b>And the table makes every value "
            "available</b> — <b>which is exact, navigable, and "
            "cheaper than any other option</b>, and is what you already "
            "have.",
            "<b>Which is the curb cut again:</b> <b>a figure with a "
            "stated finding and a published table is a better figure for "
            "everybody</b> — searchable, quotable, and "
            "checkable.",
            "<b>So this module's requirement is also "
            "CSCE 679's advice</b> — <b>state what the figure "
            "shows and publish what it was made from</b> — which is "
            "the most satisfying convergence in the "
            "semester."]},
 ],
 "takeaways": [
   "'Bar chart of sales by region' says what the image is and nothing about "
   "what it shows, which is the characteristic failure.",
   "A figure's content is a relationship, so the alternative has to carry "
   "the finding rather than the picture.",
   "Describe a figure in three layers: the finding, the longer description, "
   "and the data itself.",
   "The underlying table is the layer people skip and the one that most "
   "often suffices.",
   "Pitch is a magnitude channel with poor accuracy, so the channel-ranking "
   "argument applies to sonification too.",
   "A figure with a stated finding and a published table is a better figure "
   "for everybody.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The problem"),
  ("callout", "A figure's content is a relationship, and alt text for an "
              "image does not convey a relationship",
   ["<b>'Bar chart of sales by region' says what the image is and "
    "nothing whatever about what it shows</b> — <b>which is the "
    "characteristic failure of figure alternatives</b> and <b>is "
    "extremely common</b>, including in otherwise careful "
    "publications.",
    "<b>And the figure's actual point is a comparison, a trend, or "
    "an outlier</b> (CSCE 679 Module 01 &sect;2's task framing: the "
    "figure exists to support a specific judgement) — <b>so the "
    "alternative has to carry the finding, not the picture.</b>",
    "<b>Which means this is a writing problem rather than a markup "
    "problem</b>, and <b>is the only requirement in this course that "
    "cannot be met mechanically</b>: no tool can generate it, and no "
    "tool can check it (Module 09 &sect;3's alt-text example).",
    "<b>So the question to answer is: what would you say if you were "
    "describing this figure to somebody over the "
    "telephone?</b> — <b>which is the right prompt</b>, and "
    "<b>produces usable descriptions almost immediately</b> because it "
    "forces you to lead with the point rather than the "
    "apparatus."]),

  ("h1", "2 &nbsp; The three layers"),
  ("code", """1  THE SHORT ALTERNATIVE  (alt, or a caption)
       what kind of figure, what variables, and
       THE FINDING in one sentence
       "Sales rose in all four regions, with the
        north roughly doubling"

2  THE LONGER DESCRIPTION  (nearby, in real text)
       the axes with their units and their ranges
       the normalisation (CSCE 679 Module 13)
       the shape: trend, groups, outliers
       anything a reader would ask about

3  THE DATA ITSELF  (a real table, or a download)
       because the figure is a view of a table
       and the table is navigable, searchable, and
       exact

AND LAYER 3 IS THE ONE PEOPLE SKIP AND THE ONE THAT
MOST OFTEN SUFFICES -- it costs a markup table, and
it makes every single value available."""),
  ("callout", "And a real data table is navigable in a way a figure never is",
   ["<b>A screen reader navigates a properly marked table cell by "
    "cell, announcing the relevant row and column headers for each "
    "cell</b> — <b>which is a genuinely good interface for exact "
    "values</b>, <b>and better than a figure for lookup</b> "
    "(CSCE 679 Module 01 &sect;3's division of labour: tables for "
    "values, figures for shape).",
    "<b>But it requires the markup</b>: <b>header cells declared as "
    "<code>th</code>, <code>scope</code> stated, a "
    "<code>caption</code>, and no tables used for layout</b> — and "
    "<b>a 'table' built from <code>div</code> elements is announced as "
    "nothing at all</b> (Module 08 &sect;1).",
    "<b>And multi-level or merged headers need explicit "
    "association</b> via <code>headers</code> and <code>id</code>, "
    "<b>which is where table markup gets genuinely difficult and is "
    "frequently got wrong</b> — <b>so prefer a flat table</b>, "
    "repeated if necessary, over a clever nested one.",
    "<b>Which gives a useful default:</b> <b>publish the figure and "
    "the table together</b> — <b>sighted readers use the figure for "
    "shape and everybody uses the table for values</b>, <b>which is a "
    "curb cut</b> (Module 01 &sect;2) and costs almost nothing since "
    "you already have the data."]),

  ("break",),
  ("h1", "3 &nbsp; Other channels"),
  ("ul", ["<b>Sonification maps a data value to pitch</b>, playing a "
          "series as a tune — which <b>conveys trend and overall "
          "shape well and exact values badly</b> — <b>so it "
          "complements a table rather than replacing one.</b>",
          "<b>And it has exactly the same channel-ranking problem as "
          "colour does</b> — <b>pitch is a magnitude channel with "
          "poor accuracy</b> — <b>so CSCE 679 Module 02's "
          "argument applies to it directly</b>, which is a pleasing and "
          "slightly deflating result: the auditory channels have a "
          "ranking too, and pitch is not near the top of it.",
          "<b>Tactile graphics and refreshable braille displays work "
          "well for the people who have them</b> and <b>require "
          "equipment most readers do not have</b> — <b>which limits "
          "them to contexts where the equipment is provided</b>, such as "
          "education, and makes them a poor general answer for published "
          "material.",
          "<b>And structured exploration beats both</b> — "
          "<b>letting a user query the data ('which is highest', 'what "
          "is the value for this category', 'move to the next peak') is "
          "frequently more useful than any rendering of it</b>, and is "
          "what the better accessible-chart libraries now do.",
          "<b>So the honest ordering is: table, description, "
          "structured exploration, sonification</b>, in decreasing "
          "generality. <b>Structured exploration beats "
          "sonification</b> — <b>a user who can ask 'which is "
          "highest' has a better interface than one listening to a "
          "tune</b>, and it is also easier to build."]),

  ("h1", "4 &nbsp; Practice"),
  ("callout", "Every figure gets a one-sentence finding and a table, and that "
              "covers most of it",
   ["<b>The one-sentence finding is the alternative that "
    "matters</b> — <b>and writing it improves the figure's own "
    "caption</b>, <b>because it forces you to say what the figure is "
    "for</b> (CSCE 679 Module 13 &sect;2's five-clause caption, of "
    "which this is the first clause).",
    "<b>And the table makes every value available</b> — "
    "<b>which is exact, navigable, searchable, and cheaper than any "
    "other option</b>, <b>and is what you already have</b> since the "
    "figure was rendered from it.",
    "<b>Which is the curb cut argument again:</b> <b>a figure with a "
    "stated finding and a published table is a better figure for "
    "everybody</b> — searchable, quotable, re-analysable, and "
    "checkable — which is why this requirement is easy to "
    "defend.",
    "<b>So this module's access requirement is also CSCE 679's "
    "advice</b> — <b>state what the figure shows and publish what "
    "it was made from</b> — <b>which is the most satisfying "
    "convergence in the semester</b> and the clearest case of the "
    "design-for-the-constraint claim being literally true."]),
 ],
 "resources": [
   ("The WAI complex images tutorial (free)",
    "https://www.w3.org/WAI/tutorials/images/complex/",
    "<b>&sect;&sect;1 and 2</b> — the short-plus-long structure, with "
    "worked examples of good and bad descriptions."),
   ("The WAI tables tutorial (free)",
    "https://www.w3.org/WAI/tutorials/tables/",
    "<b>&sect;2's callout</b> — header association, scope, and the "
    "multi-level cases, which are the difficult part."),
   ("The Diagram Center image description guidelines (free)",
    "http://diagramcenter.org/table-of-contents-2.html",
    "<b>&sect;1 and &sect;2 in depth</b> — by figure type, from people "
    "who do this professionally for educational material."),
   ("Highcharts and the accessible-charts literature (free docs)",
    "https://www.highcharts.com/docs/accessibility/accessibility-module",
    "<b>&sect;3's structured exploration</b> — a working "
    "implementation of querying a chart rather than rendering it."),
 ],
 "exercises": [
   "<b>Find five published figures</b> with alt text that describes the "
   "image rather than the finding.",
   "<b>Describe one figure over the telephone</b>, and transcribe what "
   "you said.",
   "<b>Write all three layers</b> for one of your own figures.",
   "<b>Publish the underlying table</b> for one figure you have "
   "made.",
   "<b>Navigate a well-marked table with a screen reader</b>, cell by "
   "cell.",
   "<b>Build a table from divs</b> and listen to what is "
   "announced.",
   "<b>Find a merged-header table</b> and check its "
   "associations.",
   "<b>Sonify one series</b> and try to read an exact value from "
   "it.",
   "<b>Build a query interface</b> for one dataset: highest, lowest, "
   "by category.",
   "<b>Compare all four alternatives</b> on the same data, and rank "
   "them for one task.",
 ],
 "selfcheck": [
   "Why is alt text insufficient for a figure?",
   "What must the alternative carry?",
   "Why is this a writing problem, and what prompt helps?",
   "Give the three layers and what each contains.",
   "Which layer is skipped, and why does it often suffice?",
   "What does a table require in markup, and what breaks it?",
   "What does sonification convey well and badly?",
   "Why does the channel-ranking argument apply to pitch?",
   "State the honest ordering of the alternatives.",
   "Why is this requirement also good visualisation advice?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Games and Real-Time Systems",
 "subtitle": "Where this track's work meets this course's "
             "requirements.",
 "question": "Can your game be finished by somebody who cannot do the "
             "hard part?",
 "outcomes": [
     "Explain why games are a distinct accessibility problem.",
     "State the input, difficulty, and presentation options.",
     "State the photosensitivity and vestibular requirements.",
     "Explain accessibility in a rendering and engine context.",
     "Specify accessibility options for a real-time system.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why games differ",
   "blurb": "Which is about where the challenge is supposed to be."},

  {"t": "callout", "title": "A game's difficulty is deliberate, which makes separating intended from accidental difficulty the whole problem",
   "kind": "The distinction the subject turns on",
   "body": ["<b>An application that is hard to operate is "
            "defective</b> — <b>a game that is hard to play may be "
            "working exactly as designed</b>, which no other interface "
            "has to reason about.",
            "<b>So the question is whether the difficulty is the "
            "intended challenge or an incidental barrier</b> — <b>a "
            "timing puzzle may be the point, and a menu that needs a "
            "timing input is never the point.</b>",
            "<b>Which gives a usable rule:</b> <b>everything outside "
            "the intended challenge should be as easy as "
            "possible</b> — menus, navigation, text, inventory, and "
            "saving.",
            "<b>And inside the challenge, offer options rather than "
            "removing it</b> — <b>which preserves the design for "
            "players who want it and makes the game finishable for "
            "those who cannot meet one particular "
            "demand.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The options",
   "blurb": "Which are well established and cheap if planned."},

  {"t": "code", "kicker": "Options", "title": "What a real-time system should offer",
   "lang": "text", "code": """
  INPUT
      full remapping, including modifiers
      no required simultaneous inputs
      toggle instead of hold, everywhere
      no required rapid repeated presses
      adjustable sensitivity and dead zones

  DIFFICULTY
      separable: combat, timing, puzzle, resource
      not one slider for all of them
      and adjustable mid-game, without penalty

  PRESENTATION
      text size, independently of UI scale
      subtitles with speaker names (Module 04)
      high-contrast and colourblind modes
      audio cues duplicated visually, and
          visual cues duplicated audibly

  CAMERA AND MOTION
      field of view, shake, motion blur, head bob
      all adjustable or disableable (Part 3)
""",
   "caption": "<b>Toggle instead of hold, everywhere</b> — the "
              "cheapest single option on this list and one of the most "
              "widely needed.",
   "note": "Separable difficulty is the option most often requested "
           "and least often provided."},

  {"t": "callout", "title": "And the cost is almost entirely in retrofitting, which is an architecture argument",
   "kind": "Why this belongs in the design phase",
   "body": ["<b>Remappable input is cheap if the input layer is "
            "abstracted and expensive if key codes are scattered through "
            "the gameplay code</b> — which is a decision made in the "
            "first week.",
            "<b>Separable difficulty is cheap if the difficulty "
            "parameters are data and expensive if they are "
            "constants</b> — likewise.",
            "<b>And text scaling is cheap if the UI layout is "
            "responsive and nearly impossible if it is "
            "pixel-positioned</b> — which is the same "
            "argument.",
            "<b>So the accessibility cost of a real-time system is "
            "set by its architecture</b>, which is "
            "Module 12 §3's retrofit argument in the form this track "
            "will actually meet it."]},

  {"t": "section", "label": "Part 3", "title": "Photosensitivity and motion",
   "blurb": "Two requirements where the failure mode is physical "
            "harm."},

  {"t": "callout", "title": "Flashing can induce a seizure and large-field motion can induce sickness, and both are design-controllable",
   "kind": "The requirement with the most serious failure mode",
   "body": ["<b>The general flash threshold limits how much of the "
            "screen may flash, how fast, and at what "
            "contrast</b> — <b>roughly, no more than three flashes "
            "per second over a large area</b>, with red flashes treated "
            "more strictly.",
            "<b>And it is testable</b> — <b>analysis tools exist "
            "for exactly this</b> — which makes it one of the few "
            "requirements in this module with a numeric "
            "check.",
            "<b>Vestibular symptoms come from large-field motion the "
            "body did not cause</b> — <b>camera shake, head bob, "
            "motion blur, forced camera movement, and a narrow field of "
            "view</b> — and the response is to make each "
            "adjustable.",
            "<b>Plus respect the system's reduced-motion "
            "preference</b> — <b>which the platform already exposes "
            "and almost nothing reads</b>, and which is a one-line "
            "check with a real effect."]},

  {"t": "section", "label": "Part 4", "title": "Engines and rendering",
   "blurb": "Where this course meets the graphics track."},

  {"t": "bullets", "kicker": "Engine", "title": "What the rendering and engine work owes",
   "items": [
     "<b>The UI layer needs the accessibility tree</b> "
     "(Module 08) — <b>and a game engine's custom UI usually "
     "does not have one</b>, which is the largest gap in this "
     "area.",
     "",
     "<b>Which means menus, settings, and text are frequently "
     "unreachable by a screen reader</b> even where the gameplay is "
     "playable — and <b>the menu is where the accessibility options "
     "live</b>, which is a particular "
     "irony.",
     "",
     "<b>Contrast and colour requirements apply to the HUD</b> "
     "(Module 03 §3) — and a HUD over arbitrary rendered "
     "content has no fixed background, so it needs its own "
     "backing.",
     "",
     "<b>And the render settings are accessibility "
     "settings</b> — <b>motion blur, depth of field, bloom, and "
     "film grain all reduce legibility</b>, so each needs to be "
     "separately disableable.",
     "",
     "<b>Which is CSCE 647's rendering features meeting this "
     "course</b>: <b>physically correct is not the same as "
     "legible</b> (CSCE 679 §12 §4).",
   ],
   "footnote": "<b>A game engine's custom UI usually has no "
               "accessibility tree</b> — so the menus holding the "
               "accessibility options are themselves frequently "
               "unreachable."},

  {"t": "callout", "title": "And the closing position",
   "kind": "Closing",
   "body": ["<b>Games are where the accessibility argument is "
            "hardest and the results are most visible</b> — "
            "<b>because a finishable game is an unambiguous "
            "outcome</b>, unlike 'conformant'.",
            "<b>And the field has improved faster here than "
            "anywhere</b>, driven by players rather than by "
            "regulation — <b>which is Module 12 §4's point about "
            "what actually causes change.</b>",
            "<b>So the practical requirement for this track "
            "is:</b> <b>abstract the input, parameterise the "
            "difficulty, make the UI scale, expose the render settings, "
            "and respect reduced motion</b> — five architectural "
            "decisions.",
            "<b>All five of which are cheap in week one and expensive "
            "in year two</b> — <b>which is the only accessibility "
            "argument that reliably lands with an engineering "
            "lead.</b>"]},
 ],
 "takeaways": [
   "A game's difficulty is deliberate, so separating intended challenge "
   "from incidental barrier is the whole problem.",
   "Everything outside the intended challenge should be as easy as "
   "possible, and inside it offer options rather than removing it.",
   "Toggle instead of hold is the cheapest single option available and one "
   "of the most widely needed.",
   "The accessibility cost of a real-time system is set by its "
   "architecture: cheap in week one, expensive in year two.",
   "Flashing can induce a seizure and is numerically testable; large-field "
   "motion induces sickness and needs per-effect controls.",
   "A game engine's custom UI usually has no accessibility tree, so the "
   "menus holding the accessibility options are unreachable.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why games differ"),
  ("callout", "A game's difficulty is deliberate, which makes separating "
              "intended from accidental difficulty the whole problem",
   ["<b>An application that is hard to operate is simply "
    "defective</b> — <b>a game that is hard to play may be working "
    "exactly as designed</b> — <b>which is a distinction no other "
    "interface in this course has to reason about</b> and is why this "
    "module exists separately.",
    "<b>So the question for every barrier is whether the difficulty "
    "is the intended challenge or an incidental obstacle</b> — "
    "<b>a precise timing puzzle may be entirely the point, and a menu "
    "that requires a timed input is never the point</b> and is a plain "
    "defect.",
    "<b>Which gives a usable rule:</b> <b>everything outside the "
    "intended challenge should be as easy as possible</b> — menus, "
    "navigation, text, inventory management, saving, and settings "
    "— and it is remarkable how much of a typical game's difficulty "
    "lives there accidentally.",
    "<b>And inside the challenge, offer options rather than removing "
    "it</b> — <b>which preserves the design for the players who "
    "want it and makes the game finishable for those who cannot meet one "
    "particular demand</b>, which is the settled position in the field "
    "and resolves the 'but difficulty is the art' objection."]),

  ("h1", "2 &nbsp; The options"),
  ("code", """INPUT
    full remapping, including modifier keys
    no required simultaneous inputs
    toggle instead of hold, everywhere
    no required rapid repeated presses
    adjustable sensitivity and dead zones

DIFFICULTY
    separable: combat, timing, puzzle, resource
    not one slider governing all of them
    and adjustable mid-game, without penalty

PRESENTATION
    text size, independently of overall UI scale
    subtitles with speaker names (Module 04)
    high-contrast and colour-blind modes
    audio cues duplicated visually, and visual cues
        duplicated audibly

CAMERA AND MOTION
    field of view, shake, motion blur, head bob
    all adjustable or disableable (section 3)"""),
  ("p", "<b>Toggle instead of hold, everywhere</b> — <b>the "
        "cheapest single option on this list and one of the most widely "
        "needed</b>, since sustained pressure is exactly what many motor "
        "conditions cannot provide (Module 05 &sect;1). <b>Separable "
        "difficulty is the option most often requested and least often "
        "provided</b>: a player who wants the full combat challenge and "
        "cannot solve a timing puzzle is served by one slider per axis "
        "and not at all by a single easy-normal-hard choice."),
  ("callout", "And the cost is almost entirely in retrofitting, which is an "
              "architecture argument",
   ["<b>Remappable input is cheap if the input layer is abstracted "
    "behind named actions and expensive if raw key codes are scattered "
    "through the gameplay code</b> — <b>which is a decision made in "
    "the first week of a project</b> and is very hard to reverse "
    "later.",
    "<b>Separable difficulty is cheap if the difficulty parameters "
    "are data and expensive if they are constants compiled into the "
    "behaviour</b> — likewise a week-one decision, and likewise one "
    "nobody frames as an accessibility decision at the time.",
    "<b>And text scaling is cheap if the UI layout is responsive and "
    "very nearly impossible if it is pixel-positioned</b> against a "
    "fixed design resolution — which is the same argument a third "
    "time.",
    "<b>So the accessibility cost of a real-time system is set by "
    "its architecture</b> rather than by its accessibility work, "
    "<b>which is Module 12 &sect;3's retrofit argument in the form "
    "this track will actually meet it</b> — and is the version to "
    "make to an engine programmer."]),

  ("break",),
  ("h1", "3 &nbsp; Photosensitivity and motion"),
  ("callout", "Flashing can induce a seizure and large-field motion can "
              "induce sickness, and both are design-controllable",
   ["<b>The general flash threshold limits how much of the screen may "
    "flash, how rapidly, and at what contrast</b> — <b>roughly, no "
    "more than three flashes per second over a large central "
    "area</b>, <b>with saturated red flashes treated more "
    "strictly</b>, because red is specifically implicated.",
    "<b>And it is testable</b> — <b>analysis tools exist for "
    "exactly this purpose</b> and are used in broadcast "
    "compliance — <b>which makes it one of the very few "
    "requirements in this module with a numeric check</b> rather than a "
    "judgement (Module 07 &sect;4's testability point).",
    "<b>Vestibular symptoms come from large-field visual motion the "
    "body did not cause</b> — <b>camera shake, head bob, motion "
    "blur, forced camera movement, rapid field-of-view changes, and a "
    "narrow field of view</b> — <b>and the response is to make each "
    "of them individually adjustable</b>, because which one triggers "
    "symptoms varies.",
    "<b>Plus respect the operating system's reduced-motion "
    "preference</b> — <b>which the platform already exposes and "
    "almost nothing reads</b> — <b>and which is a one-line check "
    "with a real effect</b>, in web interfaces as much as in games "
    "(and is the single easiest item in this module)."]),

  ("h1", "4 &nbsp; Engines and rendering"),
  ("ul", ["<b>The UI layer needs an accessibility tree</b> "
          "(Module 08) — <b>and a game engine's custom-rendered "
          "UI usually does not have one at all</b>, since it draws "
          "textured quads rather than declaring semantic elements "
          "— <b>which is the largest single gap in this area.</b>",
          "<b>Which means menus, settings screens, and in-game text "
          "are frequently unreachable by a screen reader</b> even where "
          "the gameplay itself is playable — and <b>the menu is "
          "exactly where the accessibility options live</b>, <b>which is "
          "a particular irony</b> and a real barrier.",
          "<b>Contrast and colour requirements apply to the "
          "HUD</b> (Module 03 &sect;3) — and <b>a HUD drawn over "
          "arbitrary rendered content has no fixed background</b>, so "
          "<b>it needs its own backing plate or outline</b> rather than "
          "a contrast ratio computed against one screenshot.",
          "<b>And the render settings are accessibility "
          "settings</b> — <b>motion blur, depth of field, bloom, "
          "chromatic aberration, and film grain all reduce "
          "legibility</b>, sometimes severely — <b>so each needs to "
          "be separately disableable</b> rather than bundled into a "
          "quality preset.",
          "<b>Which is CSCE 647's rendering features meeting this "
          "course directly</b>: <b>physically correct is not the same as "
          "legible</b> — the same observation CSCE 679 "
          "Module 12 &sect;4 makes about scientific volume rendering, "
          "arriving from the other side."]),
  ("callout", "And the closing position",
   ["<b>Games are where the accessibility argument is hardest to make "
    "and where the results are most visible</b> — <b>because a "
    "finishable game is an unambiguous outcome</b>, unlike 'conformant', "
    "and players report it directly.",
    "<b>And the field has improved faster here than anywhere else in "
    "this course, driven by players and developers rather than by "
    "regulation</b> — <b>which is Module 12 &sect;4's point about "
    "what actually causes change</b>, and a genuinely encouraging "
    "counterexample to that module's general pessimism.",
    "<b>So the practical requirement for this track is five "
    "architectural decisions:</b> <b>abstract the input behind named "
    "actions, parameterise the difficulty as data, make the UI layout "
    "scale, expose the render settings individually, and respect reduced "
    "motion.</b>",
    "<b>All five of which are cheap in week one and expensive in "
    "year two</b> — <b>which is the only accessibility argument "
    "that reliably lands with an engineering lead</b>, and is therefore "
    "the one to make first (Module 12 &sect;3)."]),
 ],
 "resources": [
   ("The Game Accessibility Guidelines (free)",
    "https://gameaccessibilityguidelines.com/",
    "<b>&sect;2</b> — organised by implementation effort, which makes "
    "it usable mid-project rather than only at the start."),
   ("The AbleGamers APX player experience resources (free)",
    "https://accessible.games/accessible-player-experiences/",
    "<b>&sect;1's intended-versus-incidental distinction</b>, developed "
    "into design patterns."),
   ("Understanding WCAG 2.3.1 and 2.3.3 on flashes and motion (free)",
    "https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold",
    "<b>&sect;3's thresholds</b>, with the derivation and the red-flash "
    "exception."),
   ("The Xbox and PlayStation accessibility guidelines (free)",
    "https://learn.microsoft.com/en-us/gaming/accessibility/",
    "<b>&sect;&sect;2 and 4 as platform requirements</b> — and these "
    "are what a publisher will actually be held to."),
 ],
 "exercises": [
   "<b>Take one game you know</b> and classify five difficulties as "
   "intended or incidental.",
   "<b>Find a menu that requires a timed input.</b>",
   "<b>Audit one of your own projects against §2's option "
   "list.</b>",
   "<b>Replace every hold with a toggle option</b> in something you "
   "built.",
   "<b>Separate one difficulty slider</b> into its component axes.",
   "<b>Check whether your input layer is abstracted</b>, and estimate "
   "the remapping cost.",
   "<b>Run a flash analysis</b> on any sequence you have built.",
   "<b>Read the reduced-motion preference</b> and act on it, in one "
   "project.",
   "<b>Try to reach your own menus with a screen reader.</b>",
   "<b>Disable each render effect individually</b> and compare HUD "
   "legibility.",
 ],
 "selfcheck": [
   "Why do games need separate treatment?",
   "State the intended-versus-incidental rule and its consequence.",
   "What should happen inside the intended challenge?",
   "Give five input options and five presentation options.",
   "Which single option is cheapest and most needed?",
   "Why is separable difficulty requested and rarely provided?",
   "State the three architecture arguments.",
   "Give the flash threshold and the red exception.",
   "Name five sources of vestibular symptoms.",
   "Why is a game engine's UI usually inaccessible, and why is that "
   "ironic?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Why It Fails",
 "subtitle": "The organisational causes, which are the real ones.",
 "question": "Everybody agrees it matters. Why is almost nothing "
             "accessible?",
 "outcomes": [
     "Explain why accessibility fails organisationally.",
     "Make the cost argument correctly.",
     "Explain the retrofit cost and its cause.",
     "Explain what actually produces change.",
     "Specify a process that holds accessibility.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The failure pattern",
   "blurb": "Which is remarkably consistent."},

  {"t": "callout", "title": "Accessibility fails as a late-stage check against work that was already finished",
   "kind": "The pattern, which is almost universal",
   "body": ["<b>The design is approved, the implementation is built, "
            "and then an audit arrives</b> — <b>at which point every "
            "finding is a change request against finished "
            "work</b>, competing with features.",
            "<b>So the findings are triaged, the serious ones are "
            "deferred, and the cheap ones are "
            "fixed</b> — <b>producing an interface with correct alt "
            "text and an unusable focus order</b>, which is the "
            "characteristic outcome.",
            "<b>And nobody involved made a bad decision</b>: "
            "<b>each triage call was locally reasonable</b>, which is "
            "why exhortation does not fix this and process "
            "does.",
            "<b>Which means the cause is the position in the "
            "schedule, not the priority</b> — <b>the same findings "
            "arriving as design feedback would simply have been "
            "built</b>, at no additional cost."]},

  {"t": "section", "label": "Part 2", "title": "The cost argument",
   "blurb": "How to make it, and how not to."},

  {"t": "bullets", "kicker": "Arguments", "title": "What works and what does not, in practice",
   "items": [
     "<b>The quality argument works</b> — <b>'this is a "
     "defect that excludes users' is a bug report</b>, and bug "
     "reports have an existing process "
     "(Module 01 §1).",
     "",
     "<b>The architecture argument works</b> — <b>'this is "
     "cheap now and expensive later' is a technical-debt claim</b>, "
     "which engineering leads already act "
     "on.",
     "",
     "<b>The legal argument works and poorly</b> — <b>it "
     "produces conformance rather than access</b>, which is "
     "Module 07 §3's gap turned into a strategy.",
     "",
     "<b>The market-size argument backfires</b> — <b>it "
     "invites arguing about the number</b> "
     "(Module 02 §4), and the number is "
     "contestable.",
     "",
     "<b>And the moral argument is true and does not "
     "allocate</b> — <b>everybody already agrees, and agreement "
     "is not what is missing.</b>",
   ],
   "footnote": "<b>Everybody already agrees it matters</b> — so an "
               "argument that produces agreement produces nothing; what "
               "is missing is a position in the "
               "process."},

  {"t": "section", "label": "Part 3", "title": "The retrofit cost",
   "blurb": "Which is real and is worth quantifying honestly."},

  {"t": "callout", "title": "Accessibility is nearly free in design and expensive in repair, and the ratio is architectural",
   "kind": "Why the timing argument is the strongest one",
   "body": ["<b>Choosing a native element costs nothing; replacing a "
            "custom component library with accessible ones costs "
            "quarters</b> — and <b>the second is the same decision made "
            "later</b> (Module 08 §2).",
            "<b>Abstracting the input layer costs a day in week one "
            "and a rewrite in year two</b> "
            "(Module 11 §2) — which is the same "
            "shape.",
            "<b>And a design that assumed fixed pixel positions "
            "cannot be made to reflow</b> without redoing the "
            "layout — <b>so the 400% criterion is decided by a "
            "design decision nobody labelled.</b>",
            "<b>Which is the argument to make and the one that is "
            "true:</b> <b>the cost is not the accessibility, it is the "
            "lateness</b> — and that reframes the request from "
            "'additional work' to 'avoided rework'."]},

  {"t": "section", "label": "Part 4", "title": "What changes things",
   "blurb": "Observed, not hoped."},

  {"t": "code", "kicker": "Causes", "title": "What actually moves an organisation",
   "lang": "text", "code": """
  PROCUREMENT
      a buyer that requires conformance moves
      suppliers, which is why public-sector
      procurement rules have had more effect than
      any guideline

  LITIGATION AND REGULATION
      effective, slow, and it produces the
      conformance-not-access outcome (Module 07)

  A DEFECT PROCESS THAT ACCEPTS THESE AS DEFECTS
      the single most effective internal change,
      because it routes the work through the
      machinery that already works

  CI GATES
      cheap, narrow (Module 09 section 1), and
      they prevent regression, which is most of
      the long-run value

  DISABLED STAFF, AND USERS WITH A ROUTE IN
      which is what changes design rather than
      only fixing defects -- and is why the
      games field moved (Module 11 section 4)
""",
   "caption": "<b>Routing accessibility through the existing defect "
              "process is the single most effective internal "
              "change</b> — because that machinery already "
              "works.",
   "note": "The defect-process point is the module's practical "
           "recommendation."},

  {"t": "callout", "title": "And the honest summary of this module",
   "kind": "Closing",
   "body": ["<b>The technical problems in this course are "
            "solved</b> — <b>every requirement in Modules 03 to 11 "
            "has a known implementation</b> — and <b>the subject's "
            "actual failure is organisational.</b>",
            "<b>Which is why this module exists in an engineering "
            "course</b>: <b>knowing the fix is not sufficient if the "
            "fix arrives after the decision that made it "
            "expensive.</b>",
            "<b>And the leverage is in the schedule and the "
            "process</b> — <b>design review, the defect process, the "
            "CI gate, and a route for users to report</b> — rather "
            "than in anybody's conviction.",
            "<b>So the thing to carry out of here is a "
            "sequence:</b> <b>argue from quality and architecture, get "
            "it into the defect process, gate the regressions, and ask "
            "in design review</b> — which is four moves and none of "
            "them require authority."]},
 ],
 "takeaways": [
   "Accessibility fails as a late-stage check against finished work, where "
   "every finding is a change request competing with features.",
   "Nobody involved made a bad decision, which is why exhortation does not "
   "fix this and process does.",
   "The quality and architecture arguments work; the market-size argument "
   "backfires by inviting a debate about the number.",
   "Everybody already agrees it matters, so an argument that produces "
   "agreement produces nothing.",
   "The cost is not the accessibility, it is the lateness — which "
   "reframes the request from additional work to avoided rework.",
   "Routing accessibility through the existing defect process is the single "
   "most effective internal change.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The failure pattern"),
  ("callout", "Accessibility fails as a late-stage check against work that "
              "was already finished",
   ["<b>The design is approved, the implementation is built, the "
    "release date is set, and then an accessibility audit "
    "arrives</b> — <b>at which point every single finding is a "
    "change request against finished work</b>, <b>competing directly "
    "with features for the remaining time.</b>",
    "<b>So the findings are triaged, the structurally serious ones "
    "are deferred because they are expensive, and the cheap ones are "
    "fixed</b> — <b>producing an interface with correct alt text and "
    "an unusable focus order</b>, <b>which is the characteristic "
    "outcome</b> and is recognisable in a great deal of shipped "
    "software.",
    "<b>And nobody involved made a bad decision</b>: <b>each triage "
    "call was locally reasonable</b> given the schedule and the "
    "alternatives — <b>which is precisely why exhortation does not "
    "fix this and process does</b>, and is the same structure as "
    "CSCE 713 Module 11's incident analysis.",
    "<b>Which means the cause is the position in the schedule rather "
    "than the priority</b> — <b>the same findings arriving as "
    "design feedback would simply have been built that way</b>, <b>at no "
    "additional cost whatsoever</b> (&sect;3)."]),

  ("h1", "2 &nbsp; The cost argument"),
  ("ul", ["<b>The quality argument works</b> — <b>'this is a "
          "defect that excludes users' is a bug report</b>, and <b>bug "
          "reports have an existing process with an owner and a "
          "queue</b> (Module 01 &sect;1's social-model "
          "consequence).",
          "<b>The architecture argument works</b> — <b>'this is "
          "cheap now and expensive later' is a technical-debt claim</b>, "
          "<b>which engineering leads already understand and already act "
          "on</b> for other reasons (&sect;3).",
          "<b>The legal argument works, and works poorly</b> — "
          "<b>it produces conformance rather than access</b>, <b>which "
          "is Module 07 &sect;3's gap turned into a deliberate "
          "strategy</b>: meet the criteria, claim the level, change "
          "nothing a user would notice.",
          "<b>The market-size argument backfires</b> — <b>it "
          "invites arguing about the number</b> (Module 02 "
          "&sect;4's warning), <b>and the number is genuinely "
          "contestable</b>, so the discussion moves from a requirement "
          "to an estimate.",
          "<b>And the moral argument is true and does not "
          "allocate</b> — <b>everybody already agrees, and "
          "agreement is not what is missing</b>. <b>So an argument that "
          "produces agreement produces nothing</b>; <b>what is missing "
          "is a position in the process</b>, which is &sect;4's "
          "subject."]),

  ("break",),
  ("h1", "3 &nbsp; The retrofit cost"),
  ("callout", "Accessibility is nearly free in design and expensive in "
              "repair, and the ratio is architectural",
   ["<b>Choosing a native element costs nothing; replacing an "
    "established custom component library with accessible equivalents "
    "costs quarters of engineering time</b> — and <b>the second is "
    "the same decision made later</b> (Module 08 &sect;2), which is "
    "the clearest instance of the pattern.",
    "<b>Abstracting the input layer behind named actions costs a day "
    "in week one and a rewrite in year two</b> (Module 11 "
    "&sect;2) — <b>which is the same shape</b>, in a different "
    "domain, and with the same cause.",
    "<b>And a design that assumed fixed pixel positions cannot be "
    "made to reflow</b> without redoing the layout entirely — <b>so "
    "the 400% reflow criterion is effectively decided by a visual design "
    "decision nobody labelled as an accessibility decision</b> "
    "(Module 03 &sect;4).",
    "<b>Which is the argument to make and is also the one that "
    "happens to be true:</b> <b>the cost is not the accessibility, it is "
    "the lateness</b> — and <b>that reframes the request from "
    "'additional work' to 'avoided rework'</b>, which is a category "
    "engineering organisations have a budget for."]),

  ("h1", "4 &nbsp; What changes things"),
  ("code", """PROCUREMENT
    a buyer that requires conformance moves
    suppliers, which is why public-sector
    procurement rules have had more effect than any
    guideline ever published

LITIGATION AND REGULATION
    effective, slow, and it produces the
    conformance-not-access outcome (Module 07)

A DEFECT PROCESS THAT ACCEPTS THESE AS DEFECTS
    the single most effective internal change,
    because it routes the work through machinery
    that already works

CI GATES
    cheap, narrow (Module 09 section 1), and they
    prevent regression, which is most of the
    long-run value

DISABLED STAFF, AND USERS WITH A ROUTE IN
    which is what changes design rather than only
    fixing defects -- and is why the games field
    moved (Module 11 section 4)"""),
  ("p", "<b>Routing accessibility through the existing defect process "
        "is the single most effective internal change</b> — "
        "<b>because that machinery already works</b>: it has owners, "
        "severities, queues, and a culture of not shipping with known "
        "serious bugs. An accessibility finding filed as an "
        "accessibility finding goes into a separate list that nobody owns; "
        "the same finding filed as a defect competes on equal terms and "
        "usually wins. <b>The defect-process point is the module's "
        "practical recommendation</b>, and it is available to an "
        "individual engineer without any authority."),
  ("callout", "And the honest summary of this module",
   ["<b>The technical problems in this course are solved</b> — "
    "<b>every requirement in Modules 03 through 11 has a known, "
    "documented, implemented solution</b> — and <b>the subject's "
    "actual failure is organisational</b> rather than technical, which "
    "is unusual and worth sitting with.",
    "<b>Which is exactly why this module exists in an engineering "
    "course</b>: <b>knowing the fix is not sufficient if the fix arrives "
    "after the decision that made it expensive</b> (&sect;3), and most "
    "of this course's content arrives at that point by default.",
    "<b>And the leverage is in the schedule and the process</b> "
    "— <b>design review, the defect process, the CI gate, and a "
    "route for users to report problems</b> — <b>rather than in "
    "anybody's conviction</b>, which is already sufficient "
    "(&sect;2).",
    "<b>So the thing to carry out of here is a sequence:</b> "
    "<b>argue from quality and architecture, get it into the defect "
    "process, gate the regressions in CI, and ask the question in design "
    "review</b> — <b>which is four moves and none of them require "
    "authority</b>, which is what makes them worth knowing as an "
    "individual contributor."]),
 ],
 "resources": [
   ("Lazar, Goldstein & Taylor &mdash; Ensuring Digital Accessibility "
    "through Process and Policy",
    "https://www.elsevier.com/books/ensuring-digital-accessibility-through-process-and-policy/lazar/978-0-12-800646-7",
    "<b>The whole module</b> — the organisational and policy causes, "
    "with case studies. Library copy."),
   ("The W3C's planning and managing accessibility resources (free)",
    "https://www.w3.org/WAI/planning-and-managing/",
    "<b>&sect;4</b> — a process model, including the design-review "
    "placement this module argues for."),
   ("EN 301 549, the European accessibility procurement standard "
    "(free)",
    "https://www.etsi.org/deliver/etsi_en/301500_301599/301549/",
    "<b>&sect;4's procurement lever</b>, in the form a supplier actually "
    "encounters it."),
   ("The WebAIM Million trend data (free)",
    "https://webaim.org/projects/million/",
    "<b>&sect;1's outcome, measured over years</b> — and the slow "
    "improvement is the evidence that this module's pessimism is "
    "warranted."),
 ],
 "exercises": [
   "<b>Describe the failure pattern</b> from a project you have "
   "seen.",
   "<b>Find an interface with good alt text and a bad focus "
   "order</b>, and infer its history.",
   "<b>Write the same finding five ways</b>, one per argument in "
   "§2.",
   "<b>File one accessibility finding as an ordinary defect</b> and "
   "note what happens.",
   "<b>Estimate the retrofit cost</b> of making one existing component "
   "library accessible.",
   "<b>Estimate what it would have cost in week one.</b>",
   "<b>Find a pixel-positioned layout</b> and estimate the reflow "
   "cost.",
   "<b>Read one procurement accessibility requirement</b> in full.",
   "<b>Add an automated accessibility gate</b> to one CI pipeline.",
   "<b>Write the design-review question</b> you would add, in one "
   "sentence.",
 ],
 "selfcheck": [
   "State the failure pattern and its characteristic outcome.",
   "Why does blaming the participants not help?",
   "What is the actual cause?",
   "Rank the five arguments, with reasons.",
   "Why does the market-size argument backfire?",
   "Why is the moral argument insufficient despite being true?",
   "Give three instances of the retrofit ratio.",
   "State the reframing that the timing argument allows.",
   "Name five things that change organisations.",
   "Which internal change is most effective, and why?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming Something Is Accessible",
 "subtitle": "What you tested, and what you did not.",
 "question": "'It's accessible.' Tested with whom, against what?",
 "outcomes": [
     "State what an accessibility claim establishes.",
     "Identify the standard overclaims.",
     "Write an honest accessibility statement.",
     "Place this course in the semester and the program.",
     "State a proportionate practice you will actually keep.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a claim establishes",
   "blurb": "Which has four parts, and three are usually missing."},

  {"t": "callout", "title": "An accessibility claim establishes that these criteria, tested this way, by these people, at this time, passed",
   "kind": "The honest reading",
   "body": ["<b>Which criteria</b> — <b>the level, and whether "
            "every criterion at and below it was actually "
            "checked</b> (Module 07 §2's "
            "all-or-nothing rule).",
            "<b>Tested how</b> — <b>automated only, which covers "
            "about a third; or manually; or with assistive "
            "technology</b> (Module 09 §1), which are "
            "wildly different claims.",
            "<b>By whom</b> — <b>and whether anybody who uses "
            "assistive technology daily was involved</b> "
            "(Module 09 §4), which nothing requires and which "
            "determines the claim's value.",
            "<b>And when</b> — <b>because an audit is a snapshot "
            "and the interface has shipped eleven times "
            "since</b>. <b>'It's accessible' asserts all four and "
            "specifies none.</b>"]},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["Claim", "Correction"],
   "widths": [4.3, 6.7],
   "rows": [
     ["<b>'It's accessible'</b>", "<b>Which criteria, tested how, by whom, when? (§1)</b>"],
     ["<b>'Our checker reports zero errors'</b>", "<b>That covers about a third of the criteria (M09 §1)</b>"],
     ["<b>'We're AA conformant'</b>", "<b>Every page? Every complete process? (M07 §2)</b>"],
     ["<b>'We tested it with a screen reader'</b>", "<b>You did, or a daily user did? Not the same test (M09 §4)</b>"],
     ["<b>'No users have complained'</b>", "<b>The excluded are absent from your data (M02 §2)</b>"],
     ["<b>'It's accessible but not WCAG compliant'</b>", "<b>Possible, and it needs the evidence the claim skipped</b>"],
   ],
   "footnote": "<b>'No users have complained' is the one to refuse "
               "hardest</b> — the people excluded by the interface "
               "are structurally absent from the channel through which "
               "complaints arrive.",
   "note": "The no-complaints claim is the commonest and the "
           "emptiest."},

  {"t": "section", "label": "Part 2", "title": "The statement",
   "blurb": "What an honest one contains."},

  {"t": "code", "kicker": "Statement", "title": "An accessibility statement that is worth reading",
   "lang": "text", "code": """
  THE TARGET
      which standard, which level, and whether the
      whole product or named parts

  THE STATUS
      conformant, partially conformant, or
      non-conformant -- and partially is the honest
      answer almost always

  THE KNOWN EXCEPTIONS, NAMED
      "the data export dialog is not keyboard
       accessible; fix planned for Q3"
      which is the clause that makes the rest
      credible

  HOW IT WAS TESTED
      the methods, and who ran them, and whether
      disabled participants were involved
      (Module 09 section 4)

  WHEN
      the date of the assessment, and the cadence

  AND A ROUTE IN
      a contact who answers, which is the part that
      changes outcomes
""",
   "caption": "<b>The named exceptions are what make the rest of the "
              "statement credible</b> — a statement with no "
              "exceptions is a statement nobody checked."},

  {"t": "callout", "title": "Because the gap between conformance and usability has to be stated, not implied",
   "kind": "Why the exceptions clause carries the weight",
   "body": ["<b>A conformant interface may be unusable</b> "
            "(Module 09 §3) and <b>a non-conformant one may be "
            "perfectly usable</b> — <b>so the conformance level alone "
            "is a weak signal</b> about the thing anybody "
            "cares about.",
            "<b>Which means the useful statement is about tasks, not "
            "criteria:</b> <b>'these tasks have been completed by "
            "assistive technology users' is a far stronger claim than "
            "any level.</b>",
            "<b>And the route in is what actually fixes "
            "things</b> — <b>a contact who answers converts an "
            "excluded user into a defect report</b>, which is "
            "Module 12 §4's most effective lever.",
            "<b>So the statement's job is to be honest and "
            "actionable rather than reassuring</b> — and <b>a "
            "statement with no named exceptions is a statement nobody "
            "checked.</b>"]},

  {"t": "section", "label": "Part 3", "title": "The semester and the program",
   "blurb": "Where this course sits."},

  {"t": "table", "kicker": "Semester 11", "title": "Three courses, one correction",
   "header": ["Course", "Its measurement", "Replacing"],
   "widths": [2.3, 4.4, 4.6],
   "rows": [
     ["<b>CSCE 671</b>", "<b>Five participants and a real task</b>", "<b>'This feels intuitive'</b>"],
     ["<b>CSCE 679</b>", "<b>The measured channel ranking</b>", "<b>'This chart looks good'</b>"],
     ["<b>CSCE 632</b>", "<b>The technology, and the standard</b>", "<b>'This seems accessible'</b>"],
   ],
   "footnote": "<b>All three correct the same error:</b> designing for "
               "an imagined user who resembles the designer — and "
               "all three correct it with an observation rather than an "
               "argument.",
   "note": "This is the semester's result, stated from the third "
           "course."},

  {"t": "section", "label": "Part 4", "title": "A practice you will keep",
   "blurb": "Which is the only kind worth specifying."},

  {"t": "bullets", "kicker": "Practice", "title": "In order of return per minute",
   "items": [
     "<b>1 · Unplug the mouse before you commit</b> "
     "(Module 05 §2) — <b>the highest-yield thirty seconds in "
     "the course.</b>",
     "",
     "<b>2 · Open the accessibility pane while building each "
     "control</b> (Module 08 §1) — role, name, value, "
     "state.",
     "",
     "<b>3 · Use the native element</b> "
     "(Module 08 §2) — which is less code and more "
     "correct.",
     "",
     "<b>4 · Put a checker in CI</b> "
     "(Module 09 §1) — for the regressions, which is its "
     "real value.",
     "",
     "<b>5 · And ask the question in design review</b> "
     "(Module 12 §1) — <b>because that is the only point at "
     "which it is free.</b>",
   ],
   "footnote": "<b>Only step 5 changes the cost</b> — the other "
               "four find defects, and the fifth prevents the decisions "
               "that make them expensive."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can state a requirement from a capability and "
            "test it in minutes</b> — <b>which is what makes this "
            "engineering rather than advocacy</b>, and is the whole "
            "structure of Modules 03 through 06.",
            "<b>You know the mechanism</b> — <b>the accessibility "
            "tree, and name-role-value-state</b> — <b>so most of the "
            "rules are derivable rather than recalled</b> "
            "(Module 08).",
            "<b>And you know what a conformance claim is worth, and "
            "why the failure is organisational rather than "
            "technical</b> (Modules 07, 09, 12) — which is the part "
            "most courses omit.",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it is the accessibility "
            "statement with its exceptions named</b> — because "
            "<b>'it's accessible' claims everything and establishes "
            "nothing.</b>"]},
 ],
 "takeaways": [
   "An accessibility claim establishes which criteria, tested how, by whom, "
   "and when — and 'it's accessible' asserts all four and specifies "
   "none.",
   "'No users have complained' is the claim to refuse hardest, because the "
   "excluded are structurally absent from the complaint channel.",
   "The named exceptions are what make an accessibility statement credible; "
   "one with no exceptions is one nobody checked.",
   "A useful statement is about tasks rather than criteria, because "
   "conformance and usability come apart in both directions.",
   "A contact who answers converts an excluded user into a defect report, "
   "which is the most effective lever available.",
   "Only asking in design review changes the cost; the other practices find "
   "defects after the expensive decision was made.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a claim establishes"),
  ("callout", "An accessibility claim establishes that these criteria, tested "
              "this way, by these people, at this time, passed",
   ["<b>Which criteria</b> — <b>the level claimed, and whether "
    "every criterion at and below that level was actually checked</b>, "
    "since <b>conformance is all-or-nothing per page and per complete "
    "process</b> (Module 07 &sect;2).",
    "<b>Tested how</b> — <b>automated only, which covers about "
    "a third of the criteria; or manually by somebody competent; or with "
    "the actual assistive technology</b> (Module 09 &sect;1) — "
    "<b>which are wildly different claims routinely expressed in the "
    "same words.</b>",
    "<b>By whom</b> — <b>and in particular whether anybody who "
    "uses assistive technology daily was involved</b> (Module 09 "
    "&sect;4) — <b>which no conformance level requires and which "
    "largely determines the claim's value.</b>",
    "<b>And when</b> — <b>because an audit is a snapshot and "
    "the interface has shipped eleven times since</b> "
    "(Module 09 &sect;4's cadence point). <b>'It's accessible' "
    "asserts all four of these and specifies none of them</b>, which is "
    "why it is not a claim so much as a sentiment."]),
  ("table", ["The claim", "The correction"],
   [["<b>'It's accessible.'</b>",
     "<b>Which criteria, tested how, by whom, and when?</b> "
     "(&sect;1.)"],
    ["<b>'Our checker reports zero errors.'</b>",
     "<b>Which covers roughly a third of the criteria, and none of the "
     "judgement calls</b> (Module 09 &sect;1)."],
    ["<b>'We're AA conformant.'</b>",
     "<b>Every page? Every complete process, end to end?</b> "
     "(Module 07 &sect;2.)"],
    ["<b>'We tested it with a screen reader.'</b>",
     "<b>You did, or a daily user did?</b> <b>Those are not the same "
     "test</b> (Module 09 &sect;4)."],
    ["<b>'No users have complained.'</b>",
     "<b>The excluded are absent from your data by construction</b> "
     "(Module 02 &sect;2) — see the note."],
    ["<b>'It's accessible but not WCAG compliant.'</b>",
     "<b>Entirely possible</b> (Module 09 &sect;3 runs the other "
     "way too) — <b>and it needs exactly the evidence the claim "
     "skipped.</b>"]],
   [0.33, 0.67]),
  ("p", "<b>'No users have complained' is the one to refuse "
        "hardest</b> — <b>the people excluded by the interface are "
        "structurally absent from the channel through which complaints "
        "arrive</b>, because the complaint form is part of the interface. "
        "<b>The no-complaints claim is the commonest and the "
        "emptiest</b>, and <b>Module 02 &sect;2's survivorship "
        "argument is the complete answer to it</b>, delivered as a "
        "technical objection rather than a reproach."),

  ("h1", "2 &nbsp; The statement"),
  ("code", """THE TARGET
    which standard, which level, and whether the
    whole product or named parts of it

THE STATUS
    conformant, partially conformant, or
    non-conformant -- and "partially" is the honest
    answer almost always

THE KNOWN EXCEPTIONS, NAMED
    "the data export dialog is not keyboard
     accessible; a fix is planned for Q3"
    which is the clause that makes the rest of the
    statement credible

HOW IT WAS TESTED
    the methods, who ran them, and whether disabled
    participants were involved
    (Module 09 section 4)

WHEN
    the date of the assessment, and the cadence of
    reassessment

AND A ROUTE IN
    a contact who answers, which is the part that
    actually changes outcomes"""),
  ("callout", "Because the gap between conformance and usability has to be "
              "stated, not implied",
   ["<b>A fully conformant interface may be unusable</b> "
    "(Module 09 &sect;3's five examples) <b>and a non-conformant one "
    "may be perfectly usable for every real task</b> — <b>so the "
    "conformance level alone is a weak signal</b> about the thing anybody "
    "actually cares about.",
    "<b>Which means the useful statement is about tasks rather than "
    "criteria:</b> <b>'these five tasks have been completed "
    "independently by assistive technology users' is a far stronger and "
    "more informative claim than any conformance level</b>, and is also "
    "harder to fake.",
    "<b>And the route in is what actually fixes things over "
    "time</b> — <b>a contact who answers converts an excluded user "
    "into a defect report</b>, <b>which is Module 12 &sect;4's most "
    "effective lever</b> and costs a mailbox somebody reads.",
    "<b>So the statement's job is to be honest and actionable rather "
    "than reassuring</b> — and <b>a statement with no named "
    "exceptions is a statement nobody checked</b>, which is how a "
    "careful reader should treat one."]),

  ("break",),
  ("h1", "3 &nbsp; The semester and the program"),
  ("table", ["Course", "The measurement it introduces",
             "What it replaces"],
   [["<b>CSCE 671</b>", "<b>Five participants attempting a real "
     "task, observed.</b>", "<b>'This feels intuitive.'</b>"],
    ["<b>CSCE 679</b>", "<b>The measured ranking of the visual "
     "channels.</b>", "<b>'This chart looks good.'</b>"],
    ["<b>CSCE 632 (this one)</b>", "<b>The actual assistive "
     "technology, and a published standard.</b>",
     "<b>'This seems accessible.'</b>"]],
   [0.22, 0.42, 0.36]),
  ("p", "<b>All three courses correct the same error:</b> <b>designing "
        "for an imagined user who resembles the designer</b> — and "
        "<b>all three correct it with an observation rather than an "
        "argument</b>, which is why the semester's three closing modules "
        "arrive at the same shape. <b>This is the semester's result, "
        "stated from the third course</b>: the common structure is cheap "
        "measurement in place of confident intuition, and in each case "
        "the measurement takes minutes and the intuition was wrong."),

  ("h1", "4 &nbsp; A practice you will keep"),
  ("ul", ["<b>1 &middot; Unplug the mouse before you commit</b> "
          "(Module 05 &sect;2) — <b>the highest-yield thirty "
          "seconds in the course</b>, and the one that will survive "
          "being busy.",
          "<b>2 &middot; Open the accessibility pane while you are "
          "building each control</b> (Module 08 &sect;1) — "
          "<b>role, name, value, state</b> — which is a "
          "specification rather than a test.",
          "<b>3 &middot; Use the native element</b> (Module 08 "
          "&sect;2) — <b>which is less code and more correct</b>, "
          "and is therefore the easiest habit on this list to keep.",
          "<b>4 &middot; Put an automated checker in continuous "
          "integration</b> (Module 09 &sect;1) — <b>for the "
          "regressions, which is its real value</b> rather than for the "
          "initial findings.",
          "<b>5 &middot; And ask the question in design review</b> "
          "(Module 12 &sect;1) — <b>because that is the only "
          "point at which it is free.</b> <b>Only step 5 changes the "
          "cost</b>: <b>the other four find defects, and the fifth "
          "prevents the decisions that make them expensive</b> "
          "(Module 12 &sect;3)."]),
  ("callout", "Where this course leaves you",
   ["<b>You can state a requirement from a capability and test it in "
    "minutes</b> — <b>which is what makes this engineering rather "
    "than advocacy</b>, and <b>is the whole structure of Modules 03 "
    "through 06</b>: a constraint, a requirement, and a test you can run "
    "today.",
    "<b>You know the mechanism</b> — <b>the accessibility tree, "
    "and name-role-value-state</b> — <b>so most of the rules are "
    "derivable rather than recalled</b> (Module 08 &sect;4), which is "
    "the difference between knowing this subject and having read about "
    "it.",
    "<b>And you know what a conformance claim is worth, and why this "
    "subject's failure is organisational rather than technical</b> "
    "(Modules 07, 09, and 12) — <b>which is the part most "
    "accessibility courses omit</b> and the part that determines whether "
    "any of the rest happens.",
    "<b>The closing rule is the program's, unchanged across "
    "thirty-three courses:</b> <b>state what you measured, state what "
    "you assumed, and never claim more than you established.</b> <b>In "
    "this subject it is the accessibility statement with its exceptions "
    "named</b> — because <b>'it's accessible' claims everything and "
    "establishes nothing</b>, and the named exception is the only part of "
    "such a statement a reader can rely on."]),
 ],
 "resources": [
   ("The W3C accessibility statement generator (free)",
    "https://www.w3.org/WAI/planning/statements/",
    "<b>&sect;2</b> — a template that asks for all six parts, "
    "including the exceptions and the contact route."),
   ("WCAG conformance claims and the understanding documents (free)",
    "https://www.w3.org/TR/WCAG22/#conformance-claims",
    "<b>&sect;1</b> — what a conformance claim must contain to be one "
    "at all, which is more than most claims contain."),
   ("The WebAIM Million, read as a claims audit (free)",
    "https://webaim.org/projects/million/",
    "<b>&sect;1's overclaims at scale</b> — compare stated "
    "accessibility policies against measured detectable "
    "defects."),
   ("Lazar et al. &mdash; Research Methods in Human-Computer "
    "Interaction, the accessibility chapters",
    "https://www.elsevier.com/books/research-methods-in-human-computer-interaction/lazar/978-0-12-805390-4",
    "<b>&sect;1's 'by whom'</b>, done properly — including recruitment "
    "and compensation. Library copy."),
 ],
 "exercises": [
   "<b>State the four parts of a claim</b> for something you have "
   "built.",
   "<b>Find three published accessibility claims</b> and assess each "
   "against §1.",
   "<b>Correct six overclaims</b> you have personally heard or "
   "made.",
   "<b>Answer 'no users have complained'</b> in four sentences.",
   "<b>Write a full accessibility statement</b> with all six parts, for "
   "your Project 2 work.",
   "<b>Make the exceptions list specific</b>, with dates.",
   "<b>Rewrite one criteria-based claim</b> as a task-based one.",
   "<b>Set up a contact route</b> and decide who answers it.",
   "<b>State each Semester 11 course's measurement</b> and what it "
   "replaces.",
   "<b>Project 2 is now due.</b> Submit the repairs with their "
   "mechanism justifications, the before-and-after assistive technology "
   "transcripts, the 400% reflow case, the non-visual representation, the "
   "remaining-defects list, and the one repair that improved the "
   "interface for everybody.",
 ],
 "selfcheck": [
   "Give the four parts of an accessibility claim.",
   "Why is 'it's accessible' not a claim?",
   "Correct six standard overclaims.",
   "Why is the no-complaints claim empty, and what answers it?",
   "Give the six parts of an honest statement.",
   "Why do the named exceptions carry the credibility?",
   "Why is a task-based claim stronger than a criteria-based one?",
   "What does a route in actually accomplish?",
   "State each Semester 11 course's measurement and what it replaces.",
   "Give the five practices, and say which one changes the cost.",
 ],
},

]
