# -*- coding: utf-8 -*-
"""CSCE 605 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Lexical Analysis",
 "subtitle": "Characters to tokens, by a machine you can derive.",
 "question": "How do you split text into the words of a language?",
 "outcomes": [
     "Specify tokens with regular expressions.",
     "Convert a regular expression to an NFA and then to a DFA.",
     "Explain maximal munch and the rule-priority convention.",
     "Handle the practical problems: positions, strings, comments, "
     "Unicode.",
     "Decide between a generator and a hand-written lexer.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Regular expressions to machines",
   "blurb": "A derivation, not a library."},

  {"t": "code", "kicker": "The pipeline", "title": "From specification to table",
   "lang": "text", "code": """
  REGULAR EXPRESSION         [a-zA-Z_][a-zA-Z0-9_]*
      |
      |  THOMPSON'S CONSTRUCTION
      |    each operator becomes a small NFA fragment:
      |      concatenation -> join with an epsilon edge
      |      alternation   -> new start branching to both
      |      Kleene star   -> loop back with epsilons
      |    O(n) states for a pattern of length n
      v
  NFA  (epsilon edges; multiple states active at once)
      |
      |  SUBSET CONSTRUCTION
      |    each DFA state = a SET of NFA states
      |    worst case 2^n states; in practice far fewer
      v
  DFA  (one active state; one transition per character)
      |
      |  HOPCROFT MINIMISATION   O(n log n)
      v
  MINIMAL DFA  ->  a transition table

  Scanning is then: one array lookup per input character.
  Linear time, tiny constant, no backtracking.
""",
   "caption": "<b>This is why lexing is never the bottleneck</b> — the "
              "whole specification collapses into a table indexed by the "
              "current state and character.",
   "note": "The point of the derivation is that it is mechanical; "
           "generators just automate it."},

  {"t": "callout", "title": "The exponential blowup is real and rarely matters",
   "kind": "A bound worth knowing and not fearing",
   "body": ["<b>Subset construction can produce 2ⁿ DFA states</b> from an "
            "n-state NFA, and patterns achieving it exist.",
            "<b>Real token specifications do not.</b> Identifiers, "
            "numbers, and keywords produce DFAs with tens of states, not "
            "thousands.",
            "<b>The blowup appears in <i>general</i> regex engines</b> "
            "with backreferences and lookahead — which are not regular, "
            "and which is where catastrophic backtracking comes from.",
            "<b>A lexer's regular expressions are genuinely regular</b>, "
            "so the DFA approach always works and always runs in linear "
            "time. <b>That is a guarantee a general regex library cannot "
            "offer.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Two conventions",
   "blurb": "What resolves the ambiguities."},

  {"t": "callout", "title": "Maximal munch, and rule priority",
   "kind": "The two rules that make lexing deterministic",
   "body": ["<b>Maximal munch: take the longest match.</b> Given "
            "<code>&lt;=</code>, produce one token, not <code>&lt;</code> "
            "followed by <code>=</code>.",
            "<b>Rule priority: on a tie, the rule listed first wins.</b> "
            "<code>if</code> matches both the keyword rule and the "
            "identifier rule; the keyword is listed first.",
            "<b>Together these make the lexer deterministic</b> with no "
            "lookahead beyond what the DFA already does.",
            "<b>And maximal munch occasionally bites.</b> In old C++, "
            "<code>vector&lt;vector&lt;int&gt;&gt;</code> lexed the "
            "<code>&gt;&gt;</code> as a shift operator — <b>a lexical "
            "rule breaking a syntactic intent</b>, fixed by a special case "
            "in C++11."]},

  {"t": "table", "kicker": "Practice", "title": "What actually causes trouble",
   "header": ["Problem", "Why it is hard", "Handling"],
   "widths": [2.9, 4.3, 4.9],
   "rows": [
     ["<b>Source positions</b>", "<b>Needed by every later phase for diagnostics</b>", "<b>Track line and column from the start</b>"],
     ["<b>Nested comments</b>", "<b>Not regular — needs a counter</b>", "<b>Special-case with a depth count</b>"],
     ["String escapes", "Value differs from the text", "Lexer produces the decoded value"],
     ["<b>Significant indentation</b>", "<b>Needs a stack; not regular</b>", "<b>Emit INDENT/DEDENT tokens</b>"],
     ["Unicode identifiers", "Normalisation; confusables", "Pick a UAX-31 profile and say so"],
     ["<b>Raw strings, interpolation</b>", "<b>Lexer mode changes mid-token</b>", "A mode stack"],
   ],
   "footnote": "<b>Several of these are not regular at all</b>, which is "
               "why real lexers are DFAs plus a small amount of state.",
   "note": "The honest point: pure regularity does not survive contact "
           "with real languages."},

  {"t": "callout", "title": "Carry positions from the first character",
   "kind": "The one that is painful to retrofit",
   "body": ["<b>Every error message in every later phase needs a source "
            "position</b>, and the lexer is the only component that "
            "naturally knows it.",
            "<b>Retrofitting positions is miserable</b> — every AST node, "
            "every IR value, and every diagnostic has to be threaded "
            "through.",
            "<b>So attach a span — start and end offset — to every "
            "token from the beginning</b>, and carry it onto every tree "
            "node.",
            "<b>Byte offsets plus a line table beat storing line and "
            "column</b> per token: cheaper, and the conversion is a binary "
            "search when you need it."]},

  {"t": "section", "label": "Part 3", "title": "Build or generate",
   "blurb": "The practical choice."},

  {"t": "table", "kicker": "Choice", "title": "Generator against hand-written",
   "header": ["", "Generator (lex, flex, re2c)", "Hand-written"],
   "widths": [2.5, 4.6, 5.0],
   "rows": [
     ["<b>Effort</b>", "<b>Specification is short and declarative</b>", "A few hundred lines"],
     ["<b>Speed</b>", "Table-driven; very fast", "<b>Can be faster — better branch prediction</b>"],
     ["<b>Errors</b>", "<b>Generic; hard to customise</b>", "<b>Exactly what you want</b>"],
     ["Modes", "Supported, awkwardly", "<b>Trivial</b>"],
     ["<b>Debugging</b>", "<b>Through generated code</b>", "Ordinary"],
     ["Who uses it", "Many teaching compilers", "<b>GCC, Clang, Rust, Go, V8</b>"],
   ],
   "footnote": "<b>Essentially every production compiler hand-writes its "
               "lexer</b>, for diagnostics and modes rather than for "
               "speed.",
   "note": "The last row is the argument; it surprises people."},

  {"t": "bullets", "kicker": "Recommendation", "title": "What to do in this course",
   "items": [
     "<b>Derive the NFA and DFA by hand once</b>, for a small token set. "
     "The construction is mechanical and worth having done.",
     "",
     "<b>Then hand-write the real lexer.</b> A <code>switch</code> on the "
     "first character, with a helper per token class.",
     "",
     "<b>Keep the token type small and copyable</b> — a kind, a span, "
     "and an index into an interned string table.",
     "",
     "<b>Intern identifiers immediately.</b> Comparison becomes a pointer "
     "comparison, which every later phase benefits from.",
     "",
     "<b>And write the lexer's tests as round-trips</b> — token stream "
     "back to text should match the source.",
   ],
   "footnote": "<b>Interning is the cheap decision with the largest "
               "downstream effect</b> — symbol tables and type "
               "checking both get faster for free."},
 ],
 "takeaways": [
   "Thompson's construction turns a regular expression into an NFA in "
   "linear states, subset construction turns it into a DFA, and "
   "minimisation shrinks it — the whole specification becomes a "
   "table.",
   "Exponential DFA blowup is real but does not arise from realistic token "
   "sets; it is general regex features that cause catastrophic "
   "backtracking.",
   "Maximal munch plus rule priority make lexing deterministic without "
   "lookahead.",
   "Several real lexical problems — nested comments, indentation, "
   "interpolation — are not regular, so real lexers are DFAs plus a "
   "little state.",
   "Attach a source span to every token from the first character; "
   "retrofitting positions is miserable.",
   "Essentially every production compiler hand-writes its lexer, for "
   "diagnostics and modes rather than speed.",
 ],
 "notes": [
  ("h1", "1 &nbsp; From regular expressions to a table"),
  ("code", """REGULAR EXPRESSION      [a-zA-Z_][a-zA-Z0-9_]*
   |  THOMPSON'S CONSTRUCTION    O(n) states
   |    concatenation -> join with epsilon
   |    alternation   -> new start branching to both
   |    Kleene star   -> loop back with epsilons
   v
NFA  (epsilon edges; many states active at once)
   |  SUBSET CONSTRUCTION
   |    each DFA state = a SET of NFA states
   |    worst case 2^n states
   v
DFA  (one active state, one transition per character)
   |  HOPCROFT MINIMISATION       O(n log n)
   v
MINIMAL DFA -> transition table

Scanning: one array lookup per character. Linear, no backtracking."""),
  ("p", "<b>The value of doing this derivation once is that it is entirely "
        "mechanical.</b> A lexer generator is not doing anything you could "
        "not do by hand; it is automating three well-defined constructions. "
        "<b>And the end state explains why lexing is never the "
        "bottleneck:</b> the whole token specification collapses into a "
        "two-dimensional table indexed by the current state and the next "
        "character, so scanning costs one array lookup per input byte."),
  ("callout", "The exponential blowup is real and rarely matters",
   ["<b>Subset construction can produce 2<super>n</super> DFA states from "
    "an n-state NFA</b>, and patterns that achieve the bound are easy to "
    "construct — something like "
    "<code>(a|b)*a(a|b)<super>k</super></code> does it.",
    "<b>Real token specifications do not come anywhere near it.</b> "
    "Identifiers, integer and float literals, operators, and keywords "
    "produce minimal DFAs with tens of states. The blowup requires "
    "patterns that nobody writes to describe a token.",
    "<b>The pathological behaviour people have actually met comes from "
    "general regex engines</b> with backreferences and lookahead — "
    "<b>features that are not regular at all</b>, which is why those "
    "engines backtrack rather than building a DFA, and why catastrophic "
    "backtracking exists as a denial-of-service vector.",
    "<b>A lexer's regular expressions are genuinely regular</b>, so the "
    "DFA approach always applies and always runs in time linear in the "
    "input with no backtracking whatsoever. <b>That is a guarantee a "
    "general-purpose regex library cannot give you</b>, and it is a good "
    "illustration that restricting a language buys properties."]),

  ("h1", "2 &nbsp; The two conventions"),
  ("callout", "Maximal munch and rule priority",
   ["<b>Maximal munch: always take the longest match.</b> Given the input "
    "<code>&lt;=</code>, the lexer produces a single less-than-or-equal "
    "token rather than <code>&lt;</code> followed by <code>=</code>. "
    "Implemented by running the DFA until it can no longer advance and "
    "backing up to the last accepting state seen.",
    "<b>Rule priority: when two rules match the same longest string, the "
    "one listed first wins.</b> The input <code>if</code> matches both the "
    "keyword rule and the identifier rule at the same length; keywords are "
    "listed first, so <code>if</code> is a keyword.",
    "<b>Together these make lexing fully deterministic</b> with no "
    "lookahead beyond the one-character backup the DFA already performs, "
    "and they are the reason a lexer never needs to consult the parser.",
    "<b>And maximal munch does occasionally bite.</b> In C++ before 2011, "
    "<code>vector&lt;vector&lt;int&gt;&gt;</code> was a syntax error "
    "because <code>&gt;&gt;</code> lexed as the right-shift operator "
    "— <b>a purely lexical rule defeating an obvious syntactic "
    "intent</b>. C++11 fixed it with an explicit special case in the "
    "standard, which is the usual resolution: the convention is right "
    "almost always, and the exceptions get hard-coded."]),
  ("table", ["Problem", "Why it is hard", "How it is handled"],
   [["<b>Source positions</b>",
     "<b>Every later phase needs them for diagnostics</b>, and the lexer is "
     "the only component that naturally knows them.",
     "<b>Track from the first character</b> — see the callout below."],
    ["<b>Nested comments</b>",
     "<b>Not a regular language.</b> Matching <code>/*</code> with "
     "<code>*/</code> to arbitrary depth requires counting.",
     "Special-case it with an explicit depth counter outside the DFA."],
    ["<b>String escapes</b>",
     "The token's <i>value</i> differs from its source text.",
     "The lexer produces the decoded value alongside the original span, so "
     "diagnostics can still quote the source."],
    ["<b>Significant indentation</b>",
     "<b>Requires a stack of indentation levels</b>, which is not regular "
     "either.",
     "<b>Emit synthetic INDENT and DEDENT tokens</b> so the parser sees an "
     "ordinary bracketed structure. Python does exactly this."],
    ["<b>Unicode identifiers</b>",
     "Normalisation forms, and visually confusable characters (a Cyrillic "
     "<i>a</i> in an identifier).",
     "Adopt a published profile — UAX-31 — and state which "
     "normalisation you apply. Do not invent a rule."],
    ["<b>Raw strings and interpolation</b>",
     "<b>The lexer's mode changes mid-construct</b>, and interpolation "
     "nests arbitrarily.",
     "A mode stack. This is the clearest case where a pure DFA is "
     "insufficient."]],
   [0.20, 0.38, 0.42]),
  ("p", "<b>Several of these are not regular languages at all</b>, which is "
        "worth noticing: the clean theory of &sect;1 does not survive "
        "contact with a real language specification. <b>Real lexers are a "
        "DFA plus a small amount of explicit state</b> — a comment "
        "depth, an indentation stack, a mode stack — and that is "
        "normal rather than a compromise."),
  ("callout", "Carry source positions from the first character",
   ["<b>Every error message produced by every later phase needs a source "
    "position</b>, and the lexer is the only part of the compiler that sees "
    "the raw text.",
    "<b>Retrofitting positions is miserable work.</b> Every AST node, every "
    "symbol table entry, every IR value, and every diagnostic has to be "
    "threaded through, and the places that lost the information are "
    "discovered one error message at a time.",
    "<b>So attach a span — a start and end offset — to every "
    "token from the beginning</b>, and propagate it onto every tree node "
    "and, where it is affordable, onto IR values too. Debug information "
    "(Module 10) depends on the same chain.",
    "<b>Store byte offsets plus a line table rather than line and column "
    "per token.</b> It is smaller, it is cheaper to produce, and "
    "converting an offset to a line and column when an error is actually "
    "reported is a binary search over the line table — which happens "
    "rarely and costs nothing."]),

  ("break",),
  ("h1", "3 &nbsp; Generator or hand-written"),
  ("table", ["", "Generator (lex, flex, re2c)", "Hand-written"],
   [["<b>Effort</b>",
     "<b>The specification is short and declarative</b> — a few dozen "
     "lines of patterns and actions.",
     "A few hundred lines of straightforward code."],
    ["<b>Speed</b>", "Table-driven and very fast.",
     "<b>Often faster</b> — a <code>switch</code> on the first "
     "character branch-predicts better than an indirect table lookup, and "
     "the common cases can be special-cased."],
    ["<b>Error messages</b>",
     "<b>Generic and hard to customise.</b> 'Unexpected character' is "
     "about the ceiling.",
     "<b>Exactly what you want</b> — unterminated string literals, "
     "suggestions, and context all become easy."],
    ["<b>Lexer modes</b>",
     "Supported through start conditions, awkwardly.",
     "<b>Trivial</b> — it is just a variable."],
    ["<b>Debugging</b>",
     "<b>Through generated code</b>, which is machine-written and "
     "unpleasant to step through.",
     "Ordinary debugging of ordinary code."],
    ["<b>Who uses it</b>", "Many teaching compilers, and some shipping "
     "ones.",
     "<b>GCC, Clang, Rust, Go, V8, and essentially every production "
     "compiler.</b>"]],
   [0.16, 0.42, 0.42]),
  ("p", "<b>The last row is the argument</b>, and it surprises people who "
        "learned the subject from a textbook where the generator is "
        "presented as the obvious choice. <b>Production compilers "
        "hand-write their lexers for diagnostics and modes, not for "
        "speed</b> — the error-message quality that users actually "
        "experience is largely decided here, and a generator caps it."),
  ("ul", ["<b>Derive the NFA and DFA by hand once</b>, for five or six "
          "token classes. The construction is mechanical and worth having "
          "performed rather than only read.",
          "<b>Then hand-write the real lexer:</b> a <code>switch</code> on "
          "the first character, dispatching to a small helper per token "
          "class.",
          "<b>Keep the token type small and trivially copyable</b> — a "
          "kind tag, a span, and an index into an interned string table. "
          "Tokens are passed around constantly and a fat token type is felt "
          "everywhere.",
          "<b>Intern identifiers immediately.</b> Every identifier becomes "
          "a small integer, so comparison is an integer comparison and "
          "hashing is free. <b>This is the cheap decision with the largest "
          "downstream effect</b> — symbol table lookup (Module 05) and "
          "type checking (Module 06) both get faster and simpler for "
          "nothing.",
          "<b>Write the lexer's tests as round-trips:</b> re-emitting the "
          "token stream as text should reproduce the source, modulo "
          "whitespace. It catches dropped characters and wrong spans "
          "together, with no expected output to maintain."]),
 ],
 "resources": [
   ("Nystrom &mdash; Crafting Interpreters, 'Scanning' (free)",
    "https://craftinginterpreters.com/scanning.html",
    "A complete hand-written lexer, explained line by line. The &sect;3 "
    "recommendation, implemented."),
   ("Stanford CS143 &mdash; lexical analysis lectures (free)",
    "https://web.stanford.edu/class/cs143/",
    "Thompson's construction, subset construction, and minimisation, "
    "derived rather than asserted."),
   ("Russ Cox &mdash; Regular Expression Matching Can Be Simple And Fast "
    "(free)",
    "https://swtch.com/~rsc/regexp/regexp1.html",
    "<b>The &sect;1 blowup discussion, properly explained</b>, including "
    "why general regex engines backtrack and lexers do not."),
   ("Unicode Consortium &mdash; UAX #31, Identifier and Pattern Syntax "
    "(free)",
    "https://unicode.org/reports/tr31/",
    "The identifier profile of &sect;2's table. Short, and it saves "
    "inventing a rule badly."),
 ],
 "exercises": [
   "Convert <code>(a|b)*abb</code> to an NFA by Thompson's construction, "
   "by hand.",
   "Convert that NFA to a DFA by subset construction, and minimise it.",
   "<b>Construct a regular expression whose DFA is exponentially "
   "larger</b> than its NFA, and measure the state count.",
   "Implement the subset construction and run it on your project "
   "language's token set. Report the state count.",
   "Hand-write a lexer for your language, with spans on every token.",
   "<b>Implement maximal munch and demonstrate the C++ "
   "<code>&gt;&gt;</code> problem</b> in a small grammar.",
   "Add nested comment support and explain why the DFA alone cannot do "
   "it.",
   "<b>Implement INDENT/DEDENT tokens</b> for an indentation-sensitive "
   "toy language.",
   "Add string interpolation with a mode stack.",
   "Write round-trip tests and interning, then measure the effect of "
   "interning on a later phase.",
 ],
 "selfcheck": [
   "Describe the three constructions from regex to minimal DFA.",
   "Why does a lexer never backtrack, and why do regex libraries?",
   "State maximal munch and rule priority, and give a case where maximal "
   "munch is wrong.",
   "Name six practical lexing problems and say which are not regular.",
   "Why track byte offsets rather than line and column?",
   "Compare generated and hand-written lexers on six axes.",
   "Why do production compilers hand-write lexers?",
   "What does interning identifiers buy later?",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Parsing I: Top-Down",
 "subtitle": "Grammars, and the parser you write by hand.",
 "question": "How do tokens become a tree?",
 "outcomes": [
     "Write an unambiguous context-free grammar.",
     "Compute FIRST and FOLLOW sets and test for LL(1).",
     "Write a recursive-descent parser.",
     "Handle expression precedence with Pratt parsing.",
     "Produce error messages and recover to parse the rest.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Grammars",
   "blurb": "And the two problems with the obvious one."},

  {"t": "code", "kicker": "Grammars", "title": "Ambiguity, and removing it",
   "lang": "text", "code": """
  THE OBVIOUS GRAMMAR, which is AMBIGUOUS:
      E -> E + E | E * E | ( E ) | num

      "1 + 2 * 3" has TWO parse trees.  Nothing in the grammar
      says which. Ambiguity is a property of the GRAMMAR, not
      of the language -- the language is fine.

  STRATIFY BY PRECEDENCE, one level per nonterminal:
      E -> E + T | T            (+ is lowest, left-associative)
      T -> T * F | F            (* binds tighter)
      F -> ( E ) | num          (atoms)

      Now "1 + 2 * 3" has exactly one tree. Left recursion in
      E -> E + T encodes LEFT associativity, which is what we want.

  BUT left recursion makes a top-down parser loop forever:
      parse_E() calls parse_E() with no input consumed.

  ELIMINATE IT:
      E  -> T E'
      E' -> + T E' | epsilon

      Now LL(1)-parseable -- and the tree it builds is RIGHT
      leaning, so the parser must re-associate while building.
""",
   "caption": "<b>Three separate problems:</b> ambiguity, left recursion, "
              "and associativity — and fixing the first two damages "
              "the third.",
   "note": "The tension here is exactly what motivates Pratt parsing in "
           "Part 3."},

  {"t": "callout", "title": "Ambiguity is a property of the grammar",
   "kind": "The distinction people miss",
   "body": ["<b>A <i>language</i> is a set of strings. A <i>grammar</i> is "
            "one way of describing it.</b>",
            "<b>An ambiguous grammar gives some string two parse "
            "trees</b> — but the same language usually has an "
            "unambiguous grammar too.",
            "<b>So ambiguity is usually fixable by rewriting</b>, as above "
            "with precedence stratification.",
            "<b>Though some languages are <i>inherently</i> ambiguous</b>, "
            "with no unambiguous grammar at all — and whether a given "
            "grammar is ambiguous is <b>undecidable</b>, which is why "
            "parser generators report conflicts rather than proving "
            "absence."]},

  {"t": "section", "label": "Part 2", "title": "LL(1)",
   "blurb": "When one token of lookahead suffices."},

  {"t": "eq", "kicker": "The test", "title": "FIRST, FOLLOW, and the LL(1) condition",
   "eqs": [
     ("FIRST(α) = tokens that can begin a string derived from α",
      "Including ε if α can derive the empty string."),
     ("FOLLOW(A) = tokens that can appear right after A",
      "Needed to decide when to take an ε production."),
     ("LL(1) ⟺ for every pair of productions A → α | β:  "
      "FIRST(α) ∩ FIRST(β) = ∅",
      "And if β ⇒* ε, also FIRST(α) ∩ FOLLOW(A) = ∅."),
   ],
   "caption": "<b>The condition says: one token always determines which "
              "production to take.</b> That is exactly what a recursive-"
              "descent parser needs.",
   "note": "Tie the formal condition directly to the code shape."},

  {"t": "code", "kicker": "Recursive descent", "title": "One function per nonterminal",
   "lang": "cpp", "code": """
// The grammar IS the code. Each nonterminal becomes a function;
// each production becomes a branch; each symbol becomes a call.

Node* parse_statement() {
    switch (peek().kind) {
    case TOK_IF:     return parse_if();
    case TOK_WHILE:  return parse_while();
    case TOK_RETURN: return parse_return();
    case TOK_LBRACE: return parse_block();
    default:         return parse_expr_statement();
    }
}

Node* parse_if() {
    Span s = expect(TOK_IF).span;
    expect(TOK_LPAREN);
    Node* cond = parse_expr();
    expect(TOK_RPAREN);
    Node* then = parse_statement();
    Node* els  = match(TOK_ELSE) ? parse_statement() : nullptr;
    return make_if(cond, then, els, s.to(prev().span));
}

// Readable, debuggable, and the error messages are yours to write.
""",
   "caption": "<b>The call stack is the parse tree</b>, which is why a "
              "stack trace from a recursive-descent parser is actually "
              "informative.",
   "note": "That debugging property is a real and underrated advantage."},

  {"t": "section", "label": "Part 3", "title": "Pratt parsing",
   "blurb": "Expressions, without the grammar gymnastics."},

  {"t": "callout", "title": "Precedence climbing handles expressions directly",
   "kind": "The technique to actually use",
   "body": ["<b>Stratifying a grammar by precedence needs one nonterminal "
            "per level</b> — fifteen levels in C means fifteen functions "
            "that do almost nothing.",
            "<b>Pratt parsing replaces all of them with one function and "
            "a table.</b> Each operator has a binding power; the parser "
            "loops while the next operator binds tighter than the current "
            "minimum.",
            "<b>Associativity falls out of asymmetric binding powers</b> "
            "— left-associative operators recurse with a slightly higher "
            "minimum, right-associative with the same.",
            "<b>And new operators are a table entry</b>, not a new "
            "nonterminal. <b>This is what most hand-written compilers "
            "do.</b>"]},

  {"t": "code", "kicker": "Pratt", "title": "The whole algorithm",
   "lang": "cpp", "code": """
Node* parse_expr(int min_bp) {
    Node* lhs = parse_prefix();           // literal, ident, unary, (expr)

    for (;;) {
        Op op = peek_operator();
        if (!op || left_bp(op) < min_bp) break;

        advance();
        // LEFT-assoc: recurse with left_bp+1 so an equal-precedence
        //             operator stops and is handled by THIS loop.
        // RIGHT-assoc: recurse with left_bp so it keeps going right.
        Node* rhs = parse_expr(right_bp(op));
        lhs = make_binary(op, lhs, rhs);
    }
    return lhs;
}

// Fifteen precedence levels: fifteen table rows, one function.
// Adding an operator does not touch the parser at all.
""",
   "caption": "<b>Twelve lines replace an entire stratified grammar</b>, "
              "and associativity is a <code>+1</code>.",
   "note": "Worth writing out the left/right asymmetry explicitly — it is "
           "the part people get wrong."},

  {"t": "section", "label": "Part 4", "title": "Errors",
   "blurb": "Most of what users experience."},

  {"t": "callout", "title": "Report more than one error per run",
   "kind": "Why recovery matters",
   "body": ["<b>A parser that stops at the first error forces one "
            "edit-compile cycle per mistake</b>, which is a bad experience "
            "and an easy thing to fix.",
            "<b>Panic-mode recovery:</b> on an error, skip tokens until "
            "something in the current construct's FOLLOW set appears "
            "— a semicolon, a closing brace, a statement keyword.",
            "<b>Then resume.</b> The tree has a hole, marked with an error "
            "node, and parsing continues.",
            "<b>Suppress cascades.</b> After an error, suppress further "
            "errors until a token is successfully consumed — otherwise "
            "one mistake produces forty messages and the first is the only "
            "true one."]},

  {"t": "bullets", "kicker": "Diagnostics", "title": "What a good message has",
   "items": [
     "<b>The source location</b>, as a span rather than a point — "
     "underline the whole construct.",
     "",
     "<b>What was expected and what was found</b>, in that order, in the "
     "language's own vocabulary.",
     "",
     "<b>The enclosing context:</b> 'in this function call, opened here' "
     "with a second span.",
     "",
     "<b>A suggestion when one is defensible</b> — a missing semicolon "
     "on the previous line is usually unambiguous.",
     "",
     "<b>And never the parser's internals.</b> 'Expected token 47' is a "
     "bug report about your compiler, not about their program.",
   ],
   "footnote": "<b>Diagnostics are the compiler's entire user "
               "interface.</b> Rust's reputation rests substantially on "
               "having taken this seriously."},
 ],
 "takeaways": [
   "Ambiguity is a property of a grammar, not a language; it is usually "
   "fixable by stratifying for precedence, and deciding it in general is "
   "undecidable.",
   "Left recursion encodes left associativity and makes top-down parsing "
   "loop, so eliminating it damages the tree shape you wanted.",
   "LL(1) holds when one token of lookahead always determines the "
   "production, which is exactly what recursive descent needs.",
   "In recursive descent the grammar is the code and the call stack is the "
   "parse tree, which makes debugging ordinary.",
   "Pratt parsing replaces a stratified grammar with one function and a "
   "binding-power table; associativity is an asymmetry of one.",
   "Panic-mode recovery plus cascade suppression is what lets a parser "
   "report more than one real error per run.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Grammars"),
  ("code", """AMBIGUOUS:   E -> E + E | E * E | ( E ) | num
             "1 + 2 * 3" has TWO parse trees.

STRATIFIED BY PRECEDENCE -- unambiguous:
    E -> E + T | T          (+ lowest, left-associative)
    T -> T * F | F          (* binds tighter)
    F -> ( E ) | num

BUT left recursion loops a top-down parser forever:
    parse_E() calls parse_E() having consumed nothing.

LEFT RECURSION ELIMINATED -- now LL(1):
    E  -> T E'
    E' -> + T E' | epsilon
    ...and the tree now leans RIGHT, so the parser must
    re-associate while building it."""),
  ("p", "<b>Three separate problems are tangled here:</b> the grammar is "
        "ambiguous, top-down parsing cannot handle left recursion, and "
        "left recursion is exactly how left associativity is expressed. "
        "<b>Fixing the first two damages the third</b> — the "
        "LL(1)-parseable grammar builds a right-leaning tree for a "
        "left-associative operator, so the parser has to rebuild the "
        "association as it goes. <b>This tension is precisely what Pratt "
        "parsing (&sect;3) sidesteps</b>, which is why it is worth seeing "
        "the problem before the solution."),
  ("callout", "Ambiguity is a property of the grammar, not the language",
   ["<b>A <i>language</i> is a set of strings. A <i>grammar</i> is one "
    "particular way of describing that set</b>, and the same language "
    "generally has many grammars.",
    "<b>An ambiguous grammar assigns some string two or more distinct "
    "parse trees</b> — but it is usually possible to find a different "
    "grammar for the same language that does not, as the precedence "
    "stratification above does.",
    "<b>So ambiguity is usually a fixable defect of your description</b>, "
    "and the fix is normally to encode the disambiguating rule "
    "(precedence, associativity) into the grammar's structure.",
    "<b>Two caveats worth knowing.</b> Some context-free languages are "
    "<i>inherently</i> ambiguous — no unambiguous grammar exists for "
    "them at all. And <b>determining whether an arbitrary context-free "
    "grammar is ambiguous is undecidable</b>, which is why parser "
    "generators report conflicts (a sufficient condition for trouble) "
    "rather than proving your grammar unambiguous. That undecidability "
    "result is CSCE 627 material, and this is where it has practical "
    "consequences."]),

  ("h1", "2 &nbsp; LL(1) and recursive descent"),
  ("eq", "FIRST(&alpha;) &nbsp;=&nbsp; { t : &alpha; &rArr;* t&hellip; } "
         "&nbsp;&nbsp;&nbsp; FOLLOW(A) &nbsp;=&nbsp; { t : S &rArr;* "
         "&hellip;A t&hellip; }"),
  ("p", "<b>FIRST(&alpha;)</b> is the set of tokens that can begin a string "
        "derived from &alpha;, including &epsilon; when &alpha; can derive "
        "the empty string. <b>FOLLOW(A)</b> is the set of tokens that can "
        "immediately follow A in some derivation, which is needed to decide "
        "when to take an &epsilon; production. <b>A grammar is LL(1) when, "
        "for every pair of alternative productions A &rarr; &alpha; | "
        "&beta;, the sets FIRST(&alpha;) and FIRST(&beta;) are disjoint</b> "
        "— and additionally, if &beta; can derive &epsilon;, that "
        "FIRST(&alpha;) and FOLLOW(A) are disjoint. <b>The condition says "
        "exactly this: one token of lookahead always determines which "
        "production to take</b>, which is precisely what lets a "
        "recursive-descent parser decide with a <code>switch</code> on the "
        "next token."),
  ("code", """Node* parse_statement() {
    switch (peek().kind) {
    case TOK_IF:     return parse_if();
    case TOK_WHILE:  return parse_while();
    case TOK_RETURN: return parse_return();
    case TOK_LBRACE: return parse_block();
    default:         return parse_expr_statement();
    }
}

Node* parse_if() {
    Span s = expect(TOK_IF).span;
    expect(TOK_LPAREN);
    Node* cond = parse_expr();
    expect(TOK_RPAREN);
    Node* then = parse_statement();
    Node* els  = match(TOK_ELSE) ? parse_statement() : nullptr;
    return make_if(cond, then, els, s.to(prev().span));
}"""),
  ("p", "<b>The grammar is the code:</b> one function per nonterminal, one "
        "branch per production, one call per symbol. <b>And the call stack "
        "is the parse tree</b>, which means a stack trace from a "
        "recursive-descent parser tells you exactly where in the grammar "
        "you are — an underrated advantage over table-driven parsing "
        "(Module 04), where the equivalent information is a stack of "
        "integers."),

  ("break",),
  ("h1", "3 &nbsp; Pratt parsing"),
  ("callout", "Precedence climbing handles expressions directly",
   ["<b>Stratifying a grammar by precedence requires one nonterminal per "
    "level.</b> C has roughly fifteen precedence levels, which means "
    "fifteen functions each of which does almost nothing except call the "
    "next one — and every expression parse walks all fifteen frames "
    "even to read a single integer.",
    "<b>Pratt parsing replaces all of them with one function and a "
    "table.</b> Each operator is given a binding power; the parser loops "
    "while the next operator binds at least as tightly as the current "
    "minimum, recursing to collect the right operand.",
    "<b>Associativity falls out of making the binding powers "
    "asymmetric.</b> A left-associative operator recurses with a minimum "
    "one higher than its own, so an equal-precedence operator to the right "
    "stops and is handled by the current loop iteration — producing "
    "left nesting. A right-associative operator recurses with the same "
    "minimum, so it keeps going right.",
    "<b>And adding a new operator is a table entry, not a new "
    "nonterminal.</b> <b>This is what most hand-written compilers "
    "actually do for expressions</b>, including Clang and the Go and Rust "
    "front ends, while using ordinary recursive descent for statements and "
    "declarations."]),
  ("code", """Node* parse_expr(int min_bp) {
    Node* lhs = parse_prefix();        // literal, ident, unary, (expr)
    for (;;) {
        Op op = peek_operator();
        if (!op || left_bp(op) < min_bp) break;
        advance();
        // LEFT-assoc  -> recurse with left_bp + 1
        // RIGHT-assoc -> recurse with left_bp
        Node* rhs = parse_expr(right_bp(op));
        lhs = make_binary(op, lhs, rhs);
    }
    return lhs;
}"""),

  ("h1", "4 &nbsp; Errors and recovery"),
  ("callout", "Report more than one error per run",
   ["<b>A parser that stops at the first error forces one "
    "edit-compile-wait cycle per mistake.</b> On a file with eight typos "
    "that is eight round trips, and it is an entirely avoidable "
    "experience.",
    "<b>Panic-mode recovery is the standard technique:</b> on encountering "
    "an error, report it, then skip tokens until reaching one in the "
    "current construct's FOLLOW set — a semicolon, a closing brace, or "
    "a statement-introducing keyword.",
    "<b>Then resume normally.</b> The tree contains a hole marked by an "
    "explicit error node, which later phases must be prepared to see and "
    "skip rather than crash on. <b>Designing the AST with an error node "
    "from the start is much easier than adding one later.</b>",
    "<b>Suppress cascades.</b> After reporting an error, suppress further "
    "error reports until at least one token has been successfully consumed "
    "in the normal way. <b>Without this, one misplaced brace produces "
    "forty messages of which only the first is true</b>, and the user "
    "learns to read only the first line — which defeats the recovery "
    "entirely."]),
  ("ul", ["<b>The source location, as a span rather than a point.</b> "
          "Underline the whole offending construct; a caret under one "
          "character is rarely enough to see what the compiler objected to.",
          "<b>What was expected and what was found, in that order</b>, "
          "phrased in the language's own vocabulary rather than the "
          "grammar's. 'Expected a closing parenthesis' beats 'expected "
          "RPAREN', which beats 'expected token 47'.",
          "<b>The enclosing context, with a second span.</b> 'Unclosed "
          "parenthesis — opened here' pointing at the opening bracket "
          "is frequently more useful than the position of the error itself.",
          "<b>A suggestion, when one is defensible.</b> A missing semicolon "
          "at the end of the previous line is usually unambiguous and "
          "worth stating. <b>A wrong suggestion is worse than none</b>, so "
          "only offer one when the grammar genuinely determines it.",
          "<b>And never the parser's internals.</b> Token numbers, "
          "nonterminal names, and state numbers are bug reports about your "
          "compiler, not about the user's program. <b>Diagnostics are the "
          "compiler's entire user interface</b>, and Rust's reputation for "
          "usability rests substantially on having treated them as a "
          "first-class deliverable rather than an afterthought."]),
 ],
 "resources": [
   ("Nystrom &mdash; Crafting Interpreters, 'Parsing Expressions' and "
    "'Compiling Expressions' (free)",
    "https://craftinginterpreters.com/parsing-expressions.html",
    "Recursive descent and then Pratt parsing, both implemented in full."),
   ("Matklad &mdash; Simple but Powerful Pratt Parsing (free)",
    "https://matklad.github.io/2020/04/13/simple-but-powerful-pratt-parsing.html",
    "<b>The clearest explanation of &sect;3 available</b>, including the "
    "binding-power asymmetry that everyone gets wrong first."),
   ("Stanford CS143 &mdash; top-down parsing lectures (free)",
    "https://web.stanford.edu/class/cs143/",
    "FIRST, FOLLOW, and the LL(1) condition of &sect;2, derived."),
   ("Rust &mdash; the <code>rustc</code> diagnostics guide (free)",
    "https://rustc-dev-guide.rust-lang.org/diagnostics.html",
    "<b>&sect;4 taken seriously by people who made it a priority.</b> "
    "Worth reading for the standards it sets."),
 ],
 "exercises": [
   "Write an ambiguous expression grammar and exhibit two parse trees for "
   "one string.",
   "Stratify it by precedence and show the ambiguity is gone.",
   "<b>Compute FIRST and FOLLOW</b> for your project grammar by hand, then "
   "write code to compute them and compare.",
   "Test your grammar for LL(1) and fix any violations.",
   "Write a recursive-descent parser for statements and declarations.",
   "<b>Implement Pratt parsing</b> for expressions with at least eight "
   "precedence levels.",
   "<b>Demonstrate associativity</b> by parsing <code>a - b - c</code> and "
   "<code>a = b = c</code> and printing both trees.",
   "Add a new operator by adding only a table row, and confirm nothing "
   "else changed.",
   "Implement panic-mode recovery and cascade suppression.",
   "<b>Build a diagnostics gallery</b> of twenty ill-formed programs with "
   "the message each produces, and improve the five worst.",
 ],
 "selfcheck": [
   "Why is ambiguity a property of the grammar, and what is undecidable "
   "about it?",
   "Why does left recursion break top-down parsing, and what does "
   "eliminating it cost?",
   "Define FIRST and FOLLOW and state the LL(1) condition.",
   "Why is the call stack of a recursive-descent parser useful?",
   "What problem does Pratt parsing solve, and how does it encode "
   "associativity?",
   "Describe panic-mode recovery and why cascades must be suppressed.",
   "Name five properties of a good diagnostic.",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Parsing II: Bottom-Up",
 "subtitle": "LR parsing, and what a conflict is telling you.",
 "question": "What can a parser generator do that you cannot by hand?",
 "outcomes": [
     "Explain shift-reduce parsing and the LR item construction.",
     "Distinguish LR(0), SLR, LALR, and LR(1).",
     "Diagnose shift-reduce and reduce-reduce conflicts.",
     "Explain the dangling-else problem and its resolutions.",
     "Choose between LR, LL, and GLR with reasons.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Shift-reduce",
   "blurb": "Building the tree from the leaves."},

  {"t": "code", "kicker": "Shift-reduce", "title": "The mechanism",
   "lang": "text", "code": """
  A stack, an input, and two actions.

      SHIFT   -- move the next input token onto the stack
      REDUCE  -- the top of the stack matches a production's
                 right-hand side; replace it with the left-hand side

  Parsing  1 + 2 * 3  with  E -> E + T | T,  T -> T * F | F,  F -> num

      STACK            INPUT          ACTION
      (empty)          1 + 2 * 3      shift
      1                + 2 * 3        reduce F -> num, T -> F, E -> T
      E                + 2 * 3        shift
      E +              2 * 3          shift
      E + 2            * 3            reduce F -> num, T -> F
      E + T            * 3            SHIFT, not reduce E -> E + T
                                      ^^^ this is the whole decision
      E + T *          3              shift
      E + T * 3        (end)          reduce F -> num, T -> T * F
      E + T            (end)          reduce E -> E + T
      E                (end)          ACCEPT

  Everything hard is in that one choice: shift, or reduce?
""",
   "caption": "<b>The tree is built bottom-up, leaves first</b> — the "
              "reverse of recursive descent, which is why it handles left "
              "recursion naturally.",
   "note": "Walking the trace by hand once is the way this clicks."},

  {"t": "callout", "title": "LR handles left recursion, which is the point",
   "kind": "Why bottom-up at all",
   "body": ["<b>Top-down parsing cannot handle left recursion</b> "
            "(Module 03) — the parser recurses without consuming input.",
            "<b>Bottom-up parsing prefers it.</b> <code>E → E + T</code> "
            "is reduced only after the whole left operand is on the stack, "
            "so left recursion costs nothing.",
            "<b>So the natural, left-associative grammar works "
            "directly</b>, with no rewriting and no re-association.",
            "<b>And LR grammars strictly contain LL grammars.</b> Every "
            "LL(1) grammar is LR(1); the converse is false. <b>LR accepts "
            "more languages with less grammar surgery</b>, which is the "
            "whole argument for it."]},

  {"t": "section", "label": "Part 2", "title": "The item construction",
   "blurb": "How the decision table is built."},

  {"t": "callout", "title": "An item is a production with a position marker",
   "kind": "The construction, in one idea",
   "body": ["<b>An item is a production with a dot: "
            "<code>E → E · + T</code></b> means 'we have seen E and "
            "expect <code>+ T</code>'.",
            "<b>A parser state is a <i>set</i> of items</b> — all the "
            "productions we might currently be in the middle of.",
            "<b>Closure adds items</b>: if the dot precedes a nonterminal, "
            "add that nonterminal's productions with the dot at the "
            "start.",
            "<b>Goto moves the dot</b> across a symbol, producing the next "
            "state. <b>The set of states is a DFA over grammar symbols</b> "
            "— the same subset construction as Module 02, applied to a "
            "grammar."]},

  {"t": "table", "kicker": "The family", "title": "LR(0), SLR, LALR, LR(1)",
   "header": ["Variant", "Lookahead", "States", "Character"],
   "widths": [2.3, 3.3, 2.4, 4.1],
   "rows": [
     ["<b>LR(0)</b>", "None", "Fewest", "<b>Too weak for real languages</b>"],
     ["<b>SLR(1)</b>", "FOLLOW sets", "Same as LR(0)", "Simple; rejects useful grammars"],
     ["<b>LALR(1)</b>", "<b>Merged LR(1) lookaheads</b>", "<b>Same as LR(0)</b>", "<b>yacc, bison, GNU. The practical choice</b>"],
     ["<b>LR(1)</b>", "<b>Exact, per state</b>", "<b>Many more</b>", "<b>Most powerful; large tables</b>"],
     ["GLR", "Forks on conflict", "Varies", "<b>Handles ambiguity; returns a forest</b>"],
   ],
   "footnote": "<b>LALR merges LR(1) states with identical cores</b>, "
               "keeping LR(0)'s state count — and that merge can "
               "introduce reduce-reduce conflicts LR(1) would not have.",
   "note": "The LALR merge artifact is a real source of confusing "
           "conflicts."},

  {"t": "section", "label": "Part 3", "title": "Conflicts",
   "blurb": "What the generator is telling you."},

  {"t": "callout", "title": "A conflict means the grammar is ambiguous here",
   "kind": "How to read the error",
   "body": ["<b>Shift-reduce:</b> in some state, the parser could shift or "
            "reduce and the lookahead does not decide. <b>Usually a real "
            "ambiguity</b>, and usually precedence declarations fix it.",
            "<b>Reduce-reduce:</b> two different productions could be "
            "reduced. <b>Almost always a genuine grammar bug</b> — two "
            "constructs that are indistinguishable.",
            "<b>Generators resolve shift-reduce by shifting</b> by "
            "default, silently, and that default is usually what you "
            "wanted — which is how the dangling-else case gets "
            "accidentally right.",
            "<b>But never ship with unresolved conflicts.</b> The default "
            "is a guess, and the grammar you have is not the grammar you "
            "think you have."]},

  {"t": "code", "kicker": "Dangling else", "title": "The canonical ambiguity",
   "lang": "text", "code": """
  S -> if E then S
     | if E then S else S
     | other

  "if a then if b then x else y"      -- which `if` owns the `else`?

      READING 1:  if a then (if b then x else y)     <- shift
      READING 2:  if a then (if b then x) else y     <- reduce

  The grammar permits both, so the parser has a shift-reduce
  conflict on `else`.

  RESOLUTIONS:
    1. SHIFT (the default) -- binds else to the NEAREST if.
       This is what C, Java, C#, and almost everyone chose.
    2. Rewrite the grammar into "matched" and "unmatched"
       statements. Correct, unambiguous, and much harder to read.
    3. REQUIRE braces. Rust, Go, and Swift do this and the
       ambiguity cannot arise at all.

  Option 3 is a LANGUAGE DESIGN fix for a PARSING problem --
  which is usually the better place to solve it.
""",
   "caption": "<b>The best fix was to change the language</b>, and the "
              "languages designed after this was well understood all did.",
   "note": "Good illustration that parser difficulty is a design signal."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "What to actually use."},

  {"t": "table", "kicker": "Decision", "title": "LR, LL, or something else",
   "header": ["Use", "When", "Examples"],
   "widths": [2.7, 4.5, 4.9],
   "rows": [
     ["<b>Hand-written recursive descent + Pratt</b>", "<b>You control the language; diagnostics matter</b>", "<b>GCC, Clang, Rust, Go, V8</b>"],
     ["<b>LALR generator</b>", "<b>Grammar is given and large; speed of development</b>", "<b>Many DSLs; older compilers</b>"],
     ["LR(1) generator", "LALR conflicts you cannot resolve", "Menhir; some research work"],
     ["<b>GLR</b>", "<b>Genuinely ambiguous language</b>", "<b>C++ in some tools; NLP</b>"],
     ["PEG / packrat", "Want to write the grammar as code", "<b>Ordered choice hides ambiguity</b>"],
   ],
   "footnote": "<b>The industry moved to hand-written recursive descent</b> "
               "once diagnostics and IDE integration became the priority.",
   "note": "Worth being explicit that the textbook default lost."},

  {"t": "callout", "title": "Why production compilers abandoned generators",
   "kind": "The honest history",
   "body": ["<b>GCC used bison until 2004. Clang never did. Both now "
            "hand-write.</b>",
            "<b>Diagnostics were the main reason.</b> A generated parser "
            "knows it is in state 247; it does not know you forgot a "
            "semicolon.",
            "<b>Error recovery is the second.</b> Panic-mode recovery "
            "(Module 03) is natural in recursive descent and awkward in a "
            "table-driven parser.",
            "<b>And IDEs need incremental, error-tolerant parsing</b> of "
            "code that is <i>always</i> briefly invalid as it is typed. "
            "<b>That requirement did not exist when yacc was designed</b>, "
            "and it is now the dominant one."]},
 ],
 "takeaways": [
   "Shift-reduce parsing builds the tree from the leaves, and every "
   "difficulty lives in the single shift-or-reduce decision.",
   "LR handles left recursion naturally, so the natural left-associative "
   "grammar works with no rewriting — and LR grammars strictly "
   "contain LL grammars.",
   "A parser state is a set of items, and the state machine is built by the "
   "same subset construction as a lexer's DFA.",
   "LALR merges LR(1) states with identical cores to keep LR(0)'s state "
   "count, and that merge can introduce reduce-reduce conflicts.",
   "Shift-reduce conflicts are usually real ambiguities fixable by "
   "precedence; reduce-reduce conflicts are almost always grammar bugs.",
   "Production compilers abandoned generators for diagnostics, error "
   "recovery, and incremental IDE parsing.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Shift-reduce parsing"),
  ("code", """Two actions on a stack:
    SHIFT  -- push the next input token
    REDUCE -- the stack top matches a production's RHS; replace
              it with the LHS

Parsing  1 + 2 * 3   with  E -> E+T | T,  T -> T*F | F,  F -> num

  STACK        INPUT      ACTION
  (empty)      1 + 2*3    shift
  1            + 2*3      reduce F->num, T->F, E->T
  E            + 2*3      shift
  E +          2*3        shift
  E + 2        *3         reduce F->num, T->F
  E + T        *3         SHIFT  <-- not reduce E->E+T.
                                     THIS is the whole decision.
  E + T *      3          shift
  E + T * 3    (end)      reduce F->num, T->T*F
  E + T        (end)      reduce E->E+T
  E            (end)      ACCEPT"""),
  ("p", "<b>The tree is built bottom-up, leaves first</b> — the "
        "reverse of recursive descent — and <b>everything difficult "
        "about LR parsing is contained in that one choice: shift, or "
        "reduce?</b> The item construction of &sect;2 exists entirely to "
        "answer it mechanically. Walking this trace by hand once is the "
        "thing that makes the rest of the module make sense."),
  ("callout", "LR handles left recursion, which is the point",
   ["<b>Top-down parsing cannot handle left recursion at all</b> "
    "(Module 03 &sect;1) — <code>parse_E</code> calls "
    "<code>parse_E</code> having consumed nothing, and the parser loops "
    "forever.",
    "<b>Bottom-up parsing actively prefers it.</b> The production "
    "<code>E &rarr; E + T</code> is reduced only once the entire left "
    "operand is already on the stack, so left recursion costs nothing and "
    "requires no transformation.",
    "<b>So the natural, directly left-associative grammar works as "
    "written</b>, with no rewriting, no auxiliary nonterminals, and no "
    "re-association while building the tree.",
    "<b>And the LR grammars strictly contain the LL grammars.</b> Every "
    "LL(1) grammar is LR(1), and the converse fails — there are "
    "grammars no amount of left-factoring makes LL. <b>LR accepts more "
    "languages with less grammar surgery</b>, which is the whole technical "
    "argument for it, and it is a good one. &sect;4 explains why the "
    "industry nevertheless went the other way."]),

  ("h1", "2 &nbsp; The item construction"),
  ("callout", "An item is a production with a position marker",
   ["<b>An item is a production with a dot marking how far through it we "
    "are.</b> <code>E &rarr; E &middot; + T</code> means 'we have "
    "recognised an E and we expect to see <code>+ T</code> next'.",
    "<b>A parser state is a <i>set</i> of items</b> — all the "
    "productions we might currently be partway through, since the parser "
    "does not yet know which one it is in.",
    "<b>Closure completes a state:</b> whenever the dot immediately "
    "precedes a nonterminal, add every production for that nonterminal with "
    "the dot at the beginning, repeating until nothing new appears. This is "
    "the same idea as epsilon-closure in Module 02.",
    "<b>Goto moves the dot across a grammar symbol</b>, producing the "
    "successor state. <b>The resulting collection of states is a DFA over "
    "grammar symbols</b> — constructed by exactly the subset "
    "construction of Module 02, applied to items rather than to characters. "
    "<b>That the same construction appears twice is not a coincidence</b>; "
    "both are determinising a nondeterministic recognition process."]),
  ("table", ["Variant", "Lookahead used", "State count", "Character"],
   [["<b>LR(0)</b>", "None at all.", "Fewest.",
     "<b>Too weak for any realistic language</b> — it cannot even "
     "handle a grammar where a nonterminal is sometimes followed by "
     "different tokens. Pedagogically useful as the base construction."],
    ["<b>SLR(1)</b>",
     "The global FOLLOW set of the nonterminal being reduced.",
     "Same as LR(0).",
     "Simple, and <b>rejects many useful grammars</b> because the global "
     "FOLLOW set is coarser than the context actually permits."],
    ["<b>LALR(1)</b>",
     "<b>LR(1) lookaheads, merged across states with identical cores.</b>",
     "<b>Same as LR(0)</b> — which is the entire point.",
     "<b>What yacc, bison, and most generators produce, and the practical "
     "choice.</b> The merge is what keeps the tables small enough to have "
     "been shippable in 1975."],
    ["<b>LR(1)</b>",
     "<b>Exact lookahead, computed per state.</b>",
     "<b>Many more</b> — often an order of magnitude.",
     "<b>The most powerful of the deterministic family</b>, with tables "
     "that were impractical historically and are fine now. Menhir produces "
     "these."],
    ["<b>GLR</b>",
     "Forks the parse on every conflict and runs all possibilities.",
     "Varies dynamically.",
     "<b>Handles genuinely ambiguous grammars</b> and returns a parse "
     "<i>forest</i> rather than a tree, leaving disambiguation to a later "
     "phase."]],
   [0.14, 0.24, 0.17, 0.45]),
  ("p", "<b>LALR's merge is worth understanding, because it causes "
        "confusing conflicts.</b> Two LR(1) states with the same items but "
        "different lookaheads are merged into one, which keeps the table "
        "small — but the merged lookahead sets are unions, and "
        "<b>that union can create a reduce-reduce conflict that neither "
        "original state had</b>. The resulting bison error describes a "
        "problem that does not exist in your grammar as LR(1), which is "
        "deeply unhelpful if you do not know the merge is happening."),

  ("break",),
  ("h1", "3 &nbsp; Conflicts"),
  ("callout", "A conflict means the grammar is ambiguous at that point",
   ["<b>A shift-reduce conflict</b> means that in some state, with some "
    "lookahead, the parser could legitimately either shift or reduce and "
    "the lookahead does not settle it. <b>This is usually a real ambiguity "
    "in the grammar</b>, and precedence and associativity declarations "
    "normally resolve it cleanly.",
    "<b>A reduce-reduce conflict</b> means two different productions could "
    "both be reduced at the same point. <b>This is almost always a genuine "
    "grammar bug</b> — two constructs that the grammar has made "
    "indistinguishable — and precedence declarations will not help.",
    "<b>Generators resolve shift-reduce conflicts by shifting, by "
    "default, and usually silently.</b> That default happens to be what "
    "you want surprisingly often, which is how the dangling-else case "
    "below gets accidentally right in a great many grammars.",
    "<b>But never ship with unresolved conflicts.</b> The default is a "
    "guess made by the tool, and <b>the grammar you have is then not the "
    "grammar you think you have</b> — the language your parser accepts "
    "has been decided by a conflict-resolution rule rather than by you. "
    "Treat conflict count as a build error, not a warning."]),
  ("code", """S -> if E then S
   | if E then S else S
   | other

"if a then if b then x else y"   -- which `if` owns the `else`?

  SHIFT  -> if a then (if b then x else y)
  REDUCE -> if a then (if b then x) else y

RESOLUTIONS:
  1. SHIFT (the default): else binds to the NEAREST if.
     C, Java, C# -- and it is what everyone expects.
  2. Rewrite into "matched" and "unmatched" statements.
     Unambiguous, and much harder to read.
  3. REQUIRE braces. Rust, Go, Swift: the ambiguity cannot arise."""),
  ("p", "<b>Option 3 is a language-design fix for a parsing problem, and it "
        "is the better place to solve it.</b> Every language designed after "
        "this ambiguity was thoroughly understood chose to require braces "
        "— which eliminates not only the parsing difficulty but also "
        "the whole class of reader confusion and the "
        "<code>goto fail</code> family of bugs. <b>A construct that is hard "
        "to parse is frequently also hard for a human to read</b>, so "
        "parser difficulty is worth treating as a design signal rather than "
        "purely as an implementation obstacle."),

  ("h1", "4 &nbsp; Choosing a parsing technology"),
  ("table", ["Use", "When", "Who does"],
   [["<b>Hand-written recursive descent plus Pratt</b>",
     "<b>You control the language, and diagnostics and IDE support "
     "matter.</b>",
     "<b>GCC (since 2004), Clang, Rust, Go, V8, TypeScript.</b>"],
    ["<b>LALR generator (bison, yacc)</b>",
     "The grammar is given, large, and stable, and development speed "
     "matters more than error messages.",
     "<b>Many DSLs and configuration languages; most older compilers.</b>"],
    ["<b>LR(1) generator (Menhir)</b>",
     "You hit LALR merge conflicts you cannot resolve, and want the "
     "stronger guarantee.",
     "OCaml tooling; research compilers."],
    ["<b>GLR</b>",
     "<b>The language is genuinely ambiguous</b> and disambiguation needs "
     "semantic information.",
     "<b>C++ in some analysis tools</b>; natural language parsing."],
    ["<b>PEG / packrat</b>",
     "You want to write the grammar directly as composable code.",
     "<b>Ordered choice silently hides ambiguity</b> rather than reporting "
     "it, which is a genuine drawback — you get a parse, not a "
     "warning."]],
   [0.26, 0.37, 0.37]),
  ("callout", "Why production compilers abandoned generators",
   ["<b>GCC used bison until 2004 and then replaced it with a hand-written "
    "recursive-descent parser. Clang never used one.</b> The textbook "
    "default lost, and it is worth knowing why.",
    "<b>Diagnostics were the main reason.</b> A generated parser knows it "
    "is in state 247 with a particular lookahead; <b>it does not know that "
    "you forgot a semicolon on the previous line</b>, and recovering that "
    "intent from the automaton's state is extremely awkward. Recursive "
    "descent knows it is in <code>parse_if</code> and can say so.",
    "<b>Error recovery is the second.</b> Panic-mode recovery (Module 03 "
    "&sect;4) is natural when the parser is a call stack of functions that "
    "each know their own FOLLOW set, and clumsy when it is a table-driven "
    "automaton whose stack holds integers.",
    "<b>And modern IDEs need incremental, error-tolerant parsing</b> of "
    "code that is <i>almost always</i> briefly invalid while it is being "
    "typed, re-parsed on every keystroke, with a usable tree produced "
    "anyway. <b>That requirement simply did not exist when yacc was "
    "designed in the 1970s</b>, and it is now the dominant one — which "
    "is the real story here: the technology did not get worse, the "
    "requirements changed underneath it."]),
 ],
 "resources": [
   ("Stanford CS143 &mdash; bottom-up parsing lectures (free)",
    "https://web.stanford.edu/class/cs143/",
    "The item construction and the LR family of &sect;2, worked through "
    "carefully."),
   ("Aho, Lam, Sethi & Ullman &mdash; Compilers (the Dragon Book), "
    "chapter 4",
    "https://www.pearson.com/en-us/subject-catalog/p/compilers-principles-techniques-and-tools/P200000003389",
    "The definitive treatment of LR parsing. Library copy; this chapter is "
    "the book's strongest."),
   ("Bison manual &mdash; conflict reporting and resolution (free)",
    "https://www.gnu.org/software/bison/manual/",
    "<b>How to read a conflict report</b>, which is the practically "
    "important skill of &sect;3."),
   ("Tree-sitter &mdash; documentation and design (free)",
    "https://tree-sitter.github.io/tree-sitter/",
    "<b>Incremental, error-tolerant GLR parsing for editors</b> — the "
    "&sect;4 requirement, taken seriously and generated rather than "
    "hand-written."),
 ],
 "exercises": [
   "<b>Trace a shift-reduce parse by hand</b> for an expression with both "
   "operators, writing out the stack at every step.",
   "Build the LR(0) item sets for a small grammar.",
   "Compute SLR lookaheads and find a grammar SLR rejects but LALR "
   "accepts.",
   "Run bison on an ambiguous grammar and read the conflict report.",
   "<b>Resolve a shift-reduce conflict with precedence declarations</b> "
   "and confirm the conflict count reaches zero.",
   "<b>Construct a reduce-reduce conflict</b> deliberately and explain the "
   "grammar bug behind it.",
   "Implement the dangling-else grammar both ways and compare the parse "
   "trees.",
   "<b>Find an LALR conflict caused by state merging</b> that LR(1) does "
   "not have.",
   "Generate a parser for your project grammar and compare it against your "
   "hand-written one on error quality.",
   "Parse a file with a deliberate error in both and compare the "
   "messages.",
 ],
 "selfcheck": [
   "Describe shift-reduce parsing and name the one hard decision.",
   "Why does LR handle left recursion when LL cannot?",
   "What is an item, a state, closure, and goto?",
   "Compare LR(0), SLR, LALR, LR(1), and GLR.",
   "What does LALR's merge buy and what does it cost?",
   "Distinguish shift-reduce from reduce-reduce conflicts.",
   "State the dangling-else problem and three resolutions.",
   "Give three reasons production compilers hand-write parsers.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Names, Scopes, and Symbol Tables",
 "subtitle": "Connecting every use to its definition.",
 "question": "What does this name refer to, here?",
 "outcomes": [
     "Implement lexical scoping with a scope stack.",
     "Handle shadowing, forward references, and recursion.",
     "Explain the difference between declaration, definition, and use.",
     "Implement overload resolution and namespacing.",
     "Produce useful name-resolution diagnostics.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Scoping",
   "blurb": "Which definition a name reaches."},

  {"t": "callout", "title": "Lexical scoping is determined by the text",
   "kind": "The rule nearly every language uses",
   "body": ["<b>A name refers to the nearest enclosing declaration in the "
            "<i>source text</i></b>, and that can be decided at compile "
            "time.",
            "<b>Dynamic scoping instead uses the nearest declaration on "
            "the <i>call stack</i></b> at runtime — which makes a "
            "function's meaning depend on its caller.",
            "<b>Dynamic scoping lost decisively.</b> It prevents local "
            "reasoning, defeats most optimisation, and makes refactoring "
            "unsafe.",
            "<b>It survives in narrow places</b> — shell variables, "
            "Emacs Lisp's defaults, exception handlers, and thread-local "
            "context — where the caller-dependence is the point."]},

  {"t": "code", "kicker": "Scope stack", "title": "The resolution algorithm",
   "lang": "cpp", "code": """
// A stack of scopes. Enter pushes, leave pops, lookup walks outward.

struct Scope { std::unordered_map<Symbol, Decl*> names; Scope* parent; };

Decl* lookup(Scope* s, Symbol name) {
    for (; s; s = s->parent)
        if (auto it = s->names.find(name); it != s->names.end())
            return it->second;
    return nullptr;                     // undefined: report it
}

void declare(Scope* s, Symbol name, Decl* d) {
    auto [it, inserted] = s->names.emplace(name, d);
    if (!inserted)
        error(d->span, "redefinition of '%s'", name)
            .note(it->second->span, "previous definition here");
    //  ^^ TWO spans. The second is what makes the message useful.
}

// Shadowing an OUTER scope is legal and is not an error.
// Redefining in the SAME scope is an error. The distinction is
// exactly whether `emplace` found it in THIS map or a parent's.
""",
   "caption": "<b>Thirty lines</b>, and the shadow-versus-redefine "
              "distinction falls directly out of the structure.",
   "note": "The two-span diagnostic is the detail worth copying."},

  {"t": "section", "label": "Part 2", "title": "What makes it harder",
   "blurb": "The cases the simple version does not cover."},

  {"t": "table", "kicker": "Complications", "title": "What a real resolver must handle",
   "header": ["Case", "Problem", "Handling"],
   "widths": [2.9, 4.3, 4.9],
   "rows": [
     ["<b>Forward references</b>", "<b>Used before declared at top level</b>", "<b>Two passes: collect, then resolve</b>"],
     ["<b>Mutual recursion</b>", "Each needs the other", "<b>Falls out of the two-pass structure</b>"],
     ["<b>Closures</b>", "<b>Captured variable outlives its frame</b>", "<b>Mark captures; box or copy them</b>"],
     ["Overloading", "One name, several definitions", "Resolve by argument types (Module 06)"],
     ["<b>Imports and namespaces</b>", "<b>Scope is not purely lexical</b>", "Explicit import resolution pass"],
     ["Generics / templates", "<b>Meaning depends on instantiation</b>", "<b>Two-phase lookup, and it is subtle</b>"],
   ],
   "footnote": "<b>The two-pass structure solves forward references and "
               "mutual recursion together</b>, which is why nearly every "
               "resolver has it.",
   "note": "Two-phase template lookup is where C++ gets genuinely hard; "
           "flag but don't dwell."},

  {"t": "callout", "title": "Two passes, and why both are needed",
   "kind": "The standard structure",
   "body": ["<b>Pass 1 collects declarations</b> into each scope, without "
            "resolving anything. After it, every scope knows every name it "
            "contains.",
            "<b>Pass 2 resolves uses</b> against the now-complete scopes.",
            "<b>Forward references work</b> because the declaration was "
            "collected before any use was resolved.",
            "<b>And mutual recursion works for free</b> — neither "
            "function needs the other to exist first. <b>Inside a function "
            "body, though, scoping is usually sequential</b>, so a local "
            "used before its declaration is still an error. <b>Those are "
            "different rules and both are intentional.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Closures",
   "blurb": "When a variable outlives its scope."},

  {"t": "callout", "title": "Capture is the hard part of scoping",
   "kind": "Why closures complicate everything",
   "body": ["<b>A nested function that references an enclosing local "
            "<i>captures</i> it</b>, and may outlive the frame that local "
            "lived in.",
            "<b>Capture by value copies at creation time.</b> Simple, and "
            "later mutations are not seen.",
            "<b>Capture by reference shares</b> — so the variable must be "
            "heap-allocated (boxed) once anything captures it by "
            "reference.",
            "<b>The classic bug is capturing a loop variable by "
            "reference:</b> every closure sees the final value. <b>JavaScript "
            "changed <code>var</code> to <code>let</code> semantics "
            "specifically to fix this</b>, and C++ lambdas make you choose "
            "explicitly."]},

  {"t": "bullets", "kicker": "Implementation", "title": "What the resolver must record",
   "items": [
     "<b>For each name use: the declaration it resolves to.</b> A pointer, "
     "resolved once, used by every later phase.",
     "",
     "<b>For each local: whether it is captured</b>, and by value or by "
     "reference. Determines stack or heap.",
     "",
     "<b>For each function: its captured set</b> — which becomes the "
     "closure environment's layout.",
     "",
     "<b>For each scope: its depth and its frame slot assignment</b>, if "
     "you resolve to slots rather than names.",
     "",
     "<b>Resolving to slot indices rather than names</b> is the single "
     "biggest interpreter speedup available.",
   ],
   "footnote": "<b>Crafting Interpreters measures this</b> — "
               "replacing hash lookups with array indices is a large win."},

  {"t": "section", "label": "Part 4", "title": "Diagnostics",
   "blurb": "The messages this phase owes."},

  {"t": "callout", "title": "'Undefined name' should suggest",
   "kind": "The one place suggestions clearly pay",
   "body": ["<b>Most undefined-name errors are typos</b>, so compute the "
            "edit distance to names in scope and suggest the closest.",
            "<b>Suggest only within a small distance</b> — one or two "
            "edits — and only one candidate. A list of five is noise.",
            "<b>Also check other scopes:</b> 'no local named <code>x</code>; "
            "there is a field <code>this.x</code>' is frequently exactly "
            "right.",
            "<b>And report the declaration site on a shadow warning.</b> "
            "Two spans, as in Part 1 — the second is what turns a "
            "complaint into an explanation."]},
 ],
 "takeaways": [
   "Lexical scoping is decided by the source text at compile time; dynamic "
   "scoping depends on the call stack and lost because it prevents local "
   "reasoning.",
   "A scope stack with outward lookup is about thirty lines, and the "
   "shadow-versus-redefine distinction falls out of which map held the "
   "name.",
   "Two passes — collect declarations, then resolve uses — solve "
   "forward references and mutual recursion together.",
   "Inside a function body scoping is usually sequential, so a local used "
   "before declaration is still an error; the two rules are deliberately "
   "different.",
   "Capture by reference forces a variable onto the heap, and capturing a "
   "loop variable by reference is the classic bug.",
   "Resolving names to frame slot indices rather than strings is the "
   "largest single interpreter speedup available.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Lexical scoping"),
  ("callout", "Lexical scoping is determined by the text",
   ["<b>A name refers to the nearest enclosing declaration in the source "
    "text</b>, and because the source text is available at compile time, "
    "the resolution can be computed once and recorded.",
    "<b>Dynamic scoping instead resolves to the nearest declaration on the "
    "call stack at runtime</b>, which means a function's meaning depends on "
    "who called it — the same function body can refer to different "
    "variables on different calls.",
    "<b>Dynamic scoping lost decisively, and for good reasons.</b> It "
    "prevents local reasoning (you cannot understand a function without "
    "knowing its callers), defeats most optimisation (the compiler cannot "
    "know what a name refers to), and makes refactoring unsafe (renaming a "
    "local in one function can change another's behaviour).",
    "<b>It survives in narrow places where caller-dependence is exactly "
    "the point:</b> shell environment variables, Emacs Lisp's dynamic "
    "defaults, exception handler lookup, and thread-local or "
    "task-local context. <b>Each of those is a case where you genuinely "
    "want the caller to be able to influence the callee</b>, which is worth "
    "noticing — the feature is not bad, it is just a bad default."]),
  ("code", """struct Scope { unordered_map<Symbol, Decl*> names; Scope* parent; };

Decl* lookup(Scope* s, Symbol name) {
    for (; s; s = s->parent)
        if (auto it = s->names.find(name); it != s->names.end())
            return it->second;
    return nullptr;                 // undefined -- report it
}

void declare(Scope* s, Symbol name, Decl* d) {
    auto [it, inserted] = s->names.emplace(name, d);
    if (!inserted)
        error(d->span, "redefinition of '%s'", name)
            .note(it->second->span, "previous definition here");
}

// Shadowing an OUTER scope: legal. Redefining in the SAME scope:
// an error. The distinction is just which map held the name."""),
  ("p", "<b>Note the two spans in the diagnostic.</b> 'Redefinition of x' "
        "tells the user something they can already see; <b>'previous "
        "definition here' tells them the thing they could not find</b>, "
        "and it is the difference between a complaint and an explanation "
        "(Module 03 &sect;4)."),

  ("h1", "2 &nbsp; What makes it harder"),
  ("table", ["Case", "The problem", "The handling"],
   [["<b>Forward references</b>",
     "<b>A top-level function is called before it is declared</b>, which is "
     "normal and expected in most languages.",
     "<b>Two passes</b> — see the callout below."],
    ["<b>Mutual recursion</b>",
     "Each of two functions refers to the other, so neither can be resolved "
     "first.",
     "<b>Falls out of the two-pass structure for free</b>, which is part of "
     "why that structure is universal."],
    ["<b>Closures</b>",
     "<b>A captured variable can outlive the stack frame it was declared "
     "in.</b>",
     "The resolver must mark which locals are captured and how, so that "
     "code generation can box them (&sect;3)."],
    ["<b>Overloading</b>",
     "One name has several definitions, distinguished by argument types.",
     "Name resolution produces a candidate <i>set</i>, and type checking "
     "selects from it (Module 06). The two phases must be interleaved."],
    ["<b>Imports and namespaces</b>",
     "<b>Scope is no longer purely lexical</b> — names enter from "
     "elsewhere, possibly cyclically.",
     "An explicit import-resolution pass before name resolution, with cycle "
     "detection."],
    ["<b>Generics and templates</b>",
     "<b>What a name means can depend on the instantiation.</b>",
     "<b>Two-phase lookup</b>: resolve what you can at definition, defer "
     "dependent names to instantiation. <b>This is where C++ becomes "
     "genuinely hard</b>, and it is the source of the "
     "<code>typename</code> keyword."]],
   [0.20, 0.38, 0.42]),
  ("callout", "Two passes, and why both are needed",
   ["<b>Pass 1 collects declarations</b> into their scopes without "
    "resolving anything. When it finishes, every scope knows every name "
    "declared directly within it, though no use has been connected to "
    "anything.",
    "<b>Pass 2 resolves uses</b> against the now-complete scopes, "
    "recording for each use a pointer to the declaration it refers to.",
    "<b>Forward references work</b> because the declaration was collected "
    "in pass 1, before any use was examined in pass 2. <b>And mutual "
    "recursion works for free</b> — neither function needs the other "
    "to have been processed first, because neither is resolved until both "
    "are collected.",
    "<b>Inside a function body, though, scoping is usually sequential</b>: "
    "a local variable used above its declaration is an error, even though a "
    "top-level function used above its declaration is fine. <b>Those are "
    "deliberately different rules</b> — sequential scoping inside a "
    "body is what makes a reader able to follow the code top to bottom, "
    "while top-level order-independence is what makes a file's layout a "
    "matter of style. Implement them as two different behaviours, not one "
    "with exceptions."]),

  ("break",),
  ("h1", "3 &nbsp; Closures and capture"),
  ("callout", "Capture is the hard part of scoping",
   ["<b>A nested function that references a local of an enclosing function "
    "<i>captures</i> it</b>, and the resulting closure may outlive the "
    "stack frame that local was allocated in — which means the "
    "variable cannot simply live on the stack.",
    "<b>Capture by value copies the variable at closure-creation time.</b> "
    "Simple, safe, and later mutations by either side are invisible to the "
    "other. This is C++'s <code>[=]</code> and the default in several "
    "languages.",
    "<b>Capture by reference shares the variable</b>, so mutations are "
    "mutually visible — which means <b>the variable must be "
    "heap-allocated (boxed) as soon as anything captures it by "
    "reference</b>, and the resolver is what determines that, long before "
    "code generation.",
    "<b>The classic bug is capturing a loop variable by reference:</b> "
    "every closure created in the loop shares one variable, so after the "
    "loop they all observe the final value, and a loop that created ten "
    "callbacks produces ten identical ones. <b>JavaScript introduced "
    "<code>let</code> with per-iteration binding specifically to fix "
    "this</b>, and C++ requires you to state the capture mode explicitly "
    "rather than guessing — two different language-level answers to "
    "the same resolver-level problem."]),
  ("ul", ["<b>For each name use, the declaration it resolves to.</b> A "
          "pointer, computed once, consulted by type checking, IR "
          "generation, and every later phase. <b>Nothing should ever "
          "re-resolve a name.</b>",
          "<b>For each local, whether it is captured and how.</b> This "
          "decides stack versus heap allocation, and it must be known "
          "before code generation lays out the frame.",
          "<b>For each function, its captured set</b> — which becomes "
          "the layout of the closure environment object.",
          "<b>For each scope, its depth and its frame-slot assignment</b>, "
          "if you resolve names to slots rather than to strings.",
          "<b>Resolving to slot indices rather than to names is the single "
          "largest interpreter speedup available.</b> A variable access "
          "becomes an array index instead of a hash table lookup, and the "
          "hash lookup was happening on every access in the inner loop. "
          "Crafting Interpreters measures this and the difference is "
          "substantial."]),

  ("h1", "4 &nbsp; Diagnostics this phase owes"),
  ("callout", "'Undefined name' should suggest",
   ["<b>The overwhelming majority of undefined-name errors are typos</b>, "
    "so compute the edit distance from the unknown name to every name in "
    "scope and suggest the closest one.",
    "<b>Suggest only within a small distance</b> — one or two edits on "
    "a name of reasonable length — <b>and suggest only one "
    "candidate.</b> A list of five possibilities is noise that the user has "
    "to filter, and a confident single suggestion that is right 90% of the "
    "time is far more valuable.",
    "<b>Also check scopes the name is <i>not</i> in.</b> 'There is no local "
    "named <code>count</code>, but there is a field "
    "<code>this.count</code>' or 'did you mean the module-level "
    "<code>count</code>?' is frequently exactly the right answer, and it "
    "costs one extra lookup.",
    "<b>And report the original declaration site on a shadowing "
    "warning</b> — two spans, as in &sect;1. <b>The second span is "
    "what turns a complaint into an explanation</b>, and it is the single "
    "most reusable idea in compiler diagnostics."]),
 ],
 "resources": [
   ("Nystrom &mdash; Crafting Interpreters, 'Resolving and Binding' and "
    "'Closures' (free)",
    "https://craftinginterpreters.com/resolving-and-binding.html",
    "<b>The two-pass resolver and closure capture, implemented and "
    "measured.</b> The slot-index optimisation of &sect;3 is here with "
    "numbers."),
   ("Stanford CS143 &mdash; semantic analysis lectures (free)",
    "https://web.stanford.edu/class/cs143/",
    "Symbol tables, scoping, and the structure of &sect;2."),
   ("Cooper & Torczon &mdash; Engineering a Compiler, chapter 5",
    "https://www.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-815412-0",
    "Symbol table implementation choices and their costs."),
   ("rustc dev guide &mdash; name resolution (free)",
    "https://rustc-dev-guide.rust-lang.org/name-resolution.html",
    "A production resolver handling modules, imports, macros, and cycles "
    "— the &sect;2 complications at full scale."),
 ],
 "exercises": [
   "Implement a scope stack with enter, leave, declare, and lookup.",
   "<b>Produce a redefinition error with two spans</b>, and a shadowing "
   "warning with two spans.",
   "Implement the two-pass structure and verify forward references and "
   "mutual recursion both work.",
   "<b>Verify that sequential scoping inside a body still rejects</b> a "
   "local used before declaration.",
   "Implement closures with capture by value, then by reference.",
   "<b>Reproduce the loop-variable capture bug</b> and then fix it with "
   "per-iteration binding.",
   "Determine which locals are captured and box only those. Measure the "
   "allocation count before and after.",
   "<b>Resolve names to slot indices</b> and measure your interpreter "
   "before and after.",
   "Implement edit-distance suggestions for undefined names and test them "
   "on real typos.",
   "Add a check for 'there is a field with this name' and report it.",
 ],
 "selfcheck": [
   "Contrast lexical and dynamic scoping, and say why one won.",
   "Where does dynamic scoping still make sense?",
   "How does the scope stack distinguish shadowing from redefinition?",
   "Why are two passes needed, and what do they solve together?",
   "Why is scoping inside a body sequential when top level is not?",
   "Contrast capture by value and by reference, and say what boxing is "
   "for.",
   "Describe the loop-variable capture bug and two language-level fixes.",
   "What should the resolver record for later phases?",
   "What makes a good undefined-name diagnostic?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Type Checking",
 "subtitle": "Proving, before it runs, that the operations make sense.",
 "question": "What can a type system establish, and what does it cost?",
 "outcomes": [
     "Implement a type checker for a small language.",
     "Explain soundness and completeness, and why both are impossible.",
     "Implement Hindley–Milner inference and state its limits.",
     "Explain subtyping and variance.",
     "Explain how shader languages differ and why.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a type system is for",
   "blurb": "A proof system with a deadline."},

  {"t": "callout", "title": "A type system is an automated proof of a weak theorem",
   "kind": "The framing",
   "body": ["<b>It proves, before execution, that certain errors cannot "
            "occur</b> — typically that no operation is applied to a "
            "value it cannot handle.",
            "<b>The theorem is deliberately weak</b> so that the proof can "
            "be found automatically, for every program, quickly.",
            "<b>Rice's theorem is the reason.</b> Any non-trivial semantic "
            "property of programs is undecidable, so <b>a checker must be "
            "incomplete, or unsound, or non-terminating.</b>",
            "<b>Nearly all choose incomplete:</b> they reject some "
            "programs that would in fact have run fine. <b>That rejection "
            "is the price, and the whole design question is what you buy "
            "with it.</b>"]},

  {"t": "table", "kicker": "The trade", "title": "Soundness, completeness, and what gets given up",
   "header": ["Property", "Meaning", "Who gives it up"],
   "widths": [2.7, 4.6, 4.8],
   "rows": [
     ["<b>Sound</b>", "<b>Accepted ⇒ no type error at runtime</b>", "<b>C, C++, Java (arrays), TypeScript</b>"],
     ["<b>Complete</b>", "<b>Would not error ⇒ accepted</b>", "<b>Essentially everyone</b>"],
     ["Decidable", "The checker always terminates", "C++ templates; some dependent types"],
     ["<b>Inferring</b>", "Annotations are optional", "C, Java (partly); Go (partly)"],
   ],
   "footnote": "<b>'Unsound by design' is a legitimate choice</b> — "
               "TypeScript is deliberately unsound to stay usable with "
               "JavaScript idioms, and says so.",
   "note": "That soundness is sometimes deliberately traded away "
           "surprises people."},

  {"t": "section", "label": "Part 2", "title": "Checking",
   "blurb": "The rules, and the code that implements them."},

  {"t": "code", "kicker": "Typing rules 1/2", "title": "The notation",
   "lang": "text", "code": """
  A typing rule: premises above the line, conclusion below.

      G |- e1 : int      G |- e2 : int
      --------------------------------          (T-ADD)
            G |- e1 + e2 : int

      G |- c : bool    G |- a : T    G |- b : T
      -----------------------------------------  (T-IF)
            G |- if c then a else b : T

  "G |- e : T" reads: in environment G, expression e has type T.

  Note that T-IF requires BOTH branches to have the SAME type.
  That is a LANGUAGE DESIGN decision, not a necessity -- relaxing
  it to "some common supertype" is exactly what requires the
  subtyping machinery of Part 3.
""",
   "caption": "<b>Premises are the recursive calls; the conclusion is the "
              "return value.</b>",
   "note": "Read the rules bottom-up and they are already the code."},

  {"t": "code", "kicker": "Typing rules 2/2", "title": "…and the function they become",
   "lang": "cpp", "code": """
// Each rule becomes one case of one recursive function.

Type check(Env& G, Expr* e) {
    switch (e->kind) {

    case ADD: {                                   // T-ADD
        Type l = check(G, e->lhs);                // premise 1
        Type r = check(G, e->rhs);                // premise 2
        if (l != INT || r != INT)
            error(e->span, "operands of + must be int");
        return INT;                               // conclusion
    }

    case IF: {                                    // T-IF
        if (check(G, e->cond) != BOOL)
            error(e->cond->span, "condition must be bool");
        Type a = check(G, e->then_), b = check(G, e->else_);
        if (a != b)
            error(e->span, "branches have different types");
        return a;
    }
    ...
    }
}
""",
   "caption": "<b>Inference rules are not decoration</b> — they "
              "translate directly into the checker, one case per rule.",
   "note": "Showing the correspondence makes the notation feel useful "
           "rather than academic."},

  {"t": "section", "label": "Part 3", "title": "Inference",
   "blurb": "Working out the types you did not write."},

  {"t": "callout", "title": "Hindley–Milner: unification over type variables",
   "kind": "How inference works",
   "body": ["<b>Give every unknown a fresh type variable.</b> Then walk "
            "the program generating <i>constraints</i>: this must equal "
            "that.",
            "<b>Solve the constraints by unification</b> — the same "
            "algorithm as in logic programming, with an occurs check to "
            "reject infinite types.",
            "<b>Generalise at <code>let</code> bindings</b>, which is what "
            "gives polymorphism: a function used at two types gets two "
            "instantiations.",
            "<b>It infers principal types with no annotations at "
            "all</b> — which is remarkable, and it is why ML and Haskell "
            "feel the way they do. <b>Adding subtyping or higher-rank "
            "polymorphism breaks it</b>, which is why most languages ask "
            "for some annotations."]},

  {"t": "callout", "title": "Variance is where subtyping gets subtle",
   "kind": "The rule people get wrong",
   "body": ["<b>If Cat is a subtype of Animal, is List&lt;Cat&gt; a "
            "subtype of List&lt;Animal&gt;?</b>",
            "<b>Only if the list is read-only.</b> A mutable "
            "List&lt;Animal&gt; accepts a Dog, so treating a "
            "List&lt;Cat&gt; as one would let you insert a Dog into it.",
            "<b>Covariant in output positions, contravariant in input "
            "positions.</b> A function returning Cat is usable where one "
            "returning Animal is wanted; a function <i>taking</i> Animal "
            "is usable where one taking Cat is wanted.",
            "<b>Java's arrays are covariant and therefore unsound</b> — "
            "which is why every array store carries a runtime check. <b>A "
            "type system hole paid for on every write, forever.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Shader type systems",
   "blurb": "Where the rules are different, and why."},

  {"t": "table", "kicker": "Shaders", "title": "How shading languages differ",
   "header": ["Feature", "Shader languages", "Why"],
   "widths": [3.0, 4.2, 4.9],
   "rows": [
     ["<b>No pointers</b>", "<b>Absent or heavily restricted</b>", "<b>No aliasing ⇒ far better optimisation</b>"],
     ["<b>No recursion</b>", "<b>Forbidden (mostly)</b>", "<b>No call stack; bounded registers</b>"],
     ["<b>Vector types first-class</b>", "<code>float4</code>, swizzles, component ops", "<b>The hardware is SIMD</b>"],
     ["<b>Precision qualifiers</b>", "<code>half</code>, <code>lowp</code>", "<b>Mobile power and bandwidth</b>"],
     ["Uniform vs varying", "<b>In the type system</b>", "<b>Decides where a value lives</b>"],
     ["<b>No dynamic allocation</b>", "<b>None at all</b>", "Thousands of threads; no allocator"],
   ],
   "footnote": "<b>These restrictions exist to make compilation "
               "tractable</b>, and they are why shader compilers optimise "
               "far more aggressively than C compilers can.",
   "note": "Reframing restrictions as enabling optimisation is the "
           "insight here."},

  {"t": "callout", "title": "The restrictions are what make the optimisation possible",
   "kind": "The point of Part 4",
   "body": ["<b>A C compiler cannot prove two pointers do not alias</b>, so "
            "it must assume they might — which blocks reordering, "
            "vectorisation, and register promotion constantly.",
            "<b>A shader has no pointers</b>, so every value's provenance "
            "is known exactly, and aggressive transformation is always "
            "legal.",
            "<b>No recursion means no call stack</b>, so everything inlines "
            "and register pressure is statically bounded (Module 11).",
            "<b>So shader compilers routinely achieve what C compilers "
            "cannot</b> — not because they are better, but because the "
            "language gave them a stronger guarantee. <b>Restricting the "
            "language is how you buy optimisation.</b>"]},
 ],
 "takeaways": [
   "A type system is an automated proof of a deliberately weak theorem; "
   "Rice's theorem forces it to be incomplete, unsound, or "
   "non-terminating.",
   "Almost every type system chooses incomplete — rejecting some "
   "programs that would have run — and some choose unsoundness "
   "deliberately.",
   "Inference rules translate directly into the checker, one case per rule, "
   "read bottom-up.",
   "Hindley–Milner infers principal types with no annotations by "
   "unification plus generalisation at let bindings, and subtyping breaks "
   "it.",
   "Variance is covariant in output positions and contravariant in input "
   "positions; Java's covariant arrays are unsound and pay a runtime check "
   "on every store.",
   "Shader languages forbid pointers, recursion, and allocation — and "
   "those restrictions are precisely what let their compilers optimise so "
   "aggressively.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a type system is for"),
  ("callout", "An automated proof of a deliberately weak theorem",
   ["<b>A type system proves, before execution, that a certain class of "
    "error cannot occur</b> — typically that no operation is ever "
    "applied to a value it cannot handle. That is a real theorem about the "
    "program, mechanically established.",
    "<b>The theorem is deliberately weak</b>, because the proof must be "
    "found automatically, for every program, fast enough to run on every "
    "compile. Stronger theorems exist and cost more — which is the "
    "entire design space, from dynamic typing through to dependent types "
    "and full verification.",
    "<b>Rice's theorem is the fundamental constraint.</b> Every non-trivial "
    "semantic property of programs is undecidable (CSCE 627), so <b>a type "
    "checker must be incomplete, or unsound, or non-terminating</b> — "
    "there is no fourth option, and no amount of cleverness produces one.",
    "<b>Nearly every system chooses incomplete:</b> it rejects some "
    "programs that would in fact have run without error. <b>That rejection "
    "is the price, and the whole design question is what you buy with "
    "it</b> — how many real errors are caught per correct program "
    "wrongly rejected, and how annoying the rejections are to work "
    "around."]),
  ("table", ["Property", "What it means", "Who gives it up, and why"],
   [["<b>Sound</b>",
     "<b>If the checker accepts it, no type error occurs at runtime.</b>",
     "<b>C and C++</b> (casts, unions, undefined behaviour); <b>Java</b> "
     "(array covariance, &sect;3); <b>TypeScript</b> deliberately, to stay "
     "usable with existing JavaScript idioms — and it documents the "
     "unsoundness rather than hiding it."],
    ["<b>Complete</b>",
     "<b>If no type error would occur, the checker accepts it.</b>",
     "<b>Essentially every type system.</b> This is the one that Rice's "
     "theorem takes, and giving it up is the standard choice."],
    ["<b>Decidable</b>", "The checker always terminates.",
     "C++ template instantiation (Turing-complete, and the standard only "
     "suggests a recursion limit); full dependent types without "
     "restrictions."],
    ["<b>Inferring</b>",
     "Type annotations are optional and are reconstructed.",
     "C and older Java require annotations nearly everywhere; Go and modern "
     "Java infer locally but not across function boundaries — a "
     "deliberate choice, since full inference makes error messages much "
     "worse."]],
   [0.15, 0.32, 0.53]),

  ("h1", "2 &nbsp; Checking"),
  ("code", """    G |- e1 : int      G |- e2 : int
    --------------------------------            (T-ADD)
          G |- e1 + e2 : int

    G |- c : bool    G |- a : T    G |- b : T
    -----------------------------------------   (T-IF)
          G |- if c then a else b : T

"G |- e : T"  reads: in environment G, expression e has type T.

Type check(Env& G, Expr* e) {
    switch (e->kind) {
    case ADD: {
        Type l = check(G, e->lhs), r = check(G, e->rhs);
        if (l != INT || r != INT)
            error(e->span, "operands of + must be int");
        return INT;
    }
    ...
    }
}"""),
  ("p", "<b>Inference rules are not decoration.</b> Each rule becomes one "
        "case of one recursive function: the premises are the recursive "
        "calls, the side conditions are the checks, and the conclusion is "
        "the return value. <b>Reading a rule bottom-up gives you the "
        "code.</b> Note also that T-IF requires both branches to have the "
        "<i>same</i> type — <b>that is a language design decision, not "
        "a necessity</b>, and relaxing it to 'some common supertype' is "
        "exactly what requires the subtyping machinery of &sect;3."),

  ("break",),
  ("h1", "3 &nbsp; Inference and subtyping"),
  ("callout", "Hindley–Milner: unification over type variables",
   ["<b>Assign every unknown type a fresh type variable.</b> Then walk the "
    "program generating <i>constraints</i> — 'the type of this "
    "argument must equal the type of that parameter', 'the condition must "
    "be bool'.",
    "<b>Solve the constraint set by unification</b>, the same algorithm "
    "used in logic programming: repeatedly match structures and bind "
    "variables, <b>with an occurs check</b> to reject constraints like "
    "&alpha; = &alpha; &rarr; &alpha; that would require an infinite type.",
    "<b>Generalise at <code>let</code> bindings</b>, quantifying over the "
    "type variables not free in the environment. <b>This is what produces "
    "polymorphism:</b> a function bound by <code>let</code> and used at two "
    "different types gets two instantiations of one general scheme.",
    "<b>The result infers <i>principal</i> types — the most general "
    "type each expression can have — with no annotations "
    "whatsoever</b>, which is a genuinely remarkable result and is why ML "
    "and Haskell feel the way they do. <b>Adding subtyping, or "
    "higher-rank polymorphism, breaks it</b>: principal types stop "
    "existing, and inference becomes undecidable. That is why most "
    "mainstream languages infer locally and require annotations at function "
    "boundaries — a deliberate retreat that also makes the error "
    "messages dramatically better."]),
  ("callout", "Variance is where subtyping gets subtle",
   ["<b>If <code>Cat</code> is a subtype of <code>Animal</code>, is "
    "<code>List&lt;Cat&gt;</code> a subtype of "
    "<code>List&lt;Animal&gt;</code>?</b> The intuitive answer is yes and "
    "the intuitive answer is wrong.",
    "<b>It is sound only if the list is read-only.</b> A mutable "
    "<code>List&lt;Animal&gt;</code> accepts a <code>Dog</code>; so if a "
    "<code>List&lt;Cat&gt;</code> could be used as one, you could insert a "
    "Dog into a list of Cats and the next read would return a Dog where a "
    "Cat was guaranteed.",
    "<b>The general rule: covariant in output positions, contravariant in "
    "input positions.</b> A function returning <code>Cat</code> is usable "
    "wherever one returning <code>Animal</code> is wanted (outputs are "
    "covariant); a function <i>taking</i> <code>Animal</code> is usable "
    "wherever one taking <code>Cat</code> is wanted (inputs are "
    "contravariant — it accepts more, so it is more general). "
    "<b>Mutable containers are both, so they must be invariant.</b>",
    "<b>Java made arrays covariant and they are therefore unsound.</b> The "
    "language compensates with a runtime check on <i>every</i> array store "
    "— an <code>ArrayStoreException</code> that exists purely to patch "
    "a type system hole. <b>A design decision from 1995 that every Java "
    "program has paid for on every array write ever since</b>, and the "
    "clearest illustration available that soundness is worth getting right "
    "the first time."]),

  ("h1", "4 &nbsp; Shader type systems"),
  ("table", ["Feature", "In shading languages", "Why"],
   [["<b>Pointers</b>",
     "<b>Absent, or heavily restricted to specific storage classes.</b>",
     "<b>No aliasing means far better optimisation</b> — see the "
     "callout."],
    ["<b>Recursion</b>", "<b>Forbidden in most shader stages.</b>",
     "<b>There is no call stack.</b> Register allocation must be statically "
     "bounded across thousands of simultaneous invocations."],
    ["<b>Vector types</b>",
     "First-class: <code>float4</code>, swizzles like <code>.xyzw</code> "
     "and <code>.rgba</code>, component-wise operators.",
     "<b>The hardware is SIMD</b> and the natural data is 2-to-4 component, "
     "so the type system matches the machine directly rather than relying "
     "on auto-vectorisation (CSCE 735 Module 02)."],
    ["<b>Precision qualifiers</b>",
     "<code>half</code>, <code>lowp</code>, <code>mediump</code>, "
     "<code>highp</code> as part of the type.",
     "<b>Mobile power and bandwidth.</b> Half precision halves the register "
     "pressure and the memory traffic, and for colour it is usually "
     "sufficient."],
    ["<b>Uniform versus varying</b>",
     "<b>Encoded in the type system</b> (or in the storage class).",
     "<b>It decides where a value physically lives</b> — a constant "
     "buffer, an interpolated attribute, or a register — which the "
     "compiler must know statically."],
    ["<b>Dynamic allocation</b>", "<b>None at all.</b>",
     "Thousands of concurrent invocations and no allocator. All storage is "
     "statically sized."]],
   [0.18, 0.40, 0.42]),
  ("callout", "The restrictions are what make the optimisation possible",
   ["<b>A C compiler usually cannot prove that two pointers do not "
    "alias</b>, so it must assume they might — which blocks "
    "reordering, blocks keeping a value in a register across a store, and "
    "blocks vectorisation, constantly and invisibly. <code>restrict</code> "
    "exists because this is the dominant obstacle to optimising C.",
    "<b>A shader has no pointers</b>, so the provenance of every value is "
    "known exactly and aggressive transformation is always legal. The "
    "compiler never has to be conservative about memory.",
    "<b>No recursion means no call stack</b>, so every call can be inlined, "
    "and register pressure is a statically computable quantity rather than "
    "a dynamic one (Module 11). <b>No allocation means no garbage "
    "collector and no allocation-related side effects</b> to order around.",
    "<b>So shader compilers routinely achieve transformations that C "
    "compilers cannot</b> — not because they are better engineered, "
    "but because <b>the language handed them a far stronger "
    "guarantee</b>. <b>Restricting the language is how you buy "
    "optimisation</b>, and that trade is visible everywhere: Fortran beats "
    "C on numerics for the aliasing reason, Rust's borrow checker enables "
    "<code>noalias</code> by construction, and pure functional languages "
    "can reorder almost anything."]),
 ],
 "resources": [
   ("Pierce &mdash; Types and Programming Languages",
    "https://www.cis.upenn.edu/~bcpierce/tapl/",
    "<b>The standard reference.</b> Chapters on simple types, subtyping, "
    "and variance cover &sect;1 through &sect;3. Library copy; the "
    "author's slides are free."),
   ("Stanford CS143 &mdash; type checking lectures (free)",
    "https://web.stanford.edu/class/cs143/",
    "The rule-to-code correspondence of &sect;2, worked through."),
   ("Damas & Milner; and 'Write You a Haskell' (free)",
    "http://dev.stephendiehl.com/fun/",
    "<b>Hindley&ndash;Milner implemented</b>, with unification and "
    "generalisation in readable code."),
   ("Microsoft &mdash; HLSL reference; Khronos &mdash; GLSL specification "
    "(free)",
    "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html",
    "The &sect;4 restrictions, stated normatively. The storage-class and "
    "precision sections are the interesting ones."),
 ],
 "exercises": [
   "Write the typing rules for your project language on one page.",
   "Implement the checker directly from those rules, one case each.",
   "<b>Produce a type error message with both spans</b> — where the "
   "expected type came from and where the actual one did.",
   "Find a program your checker rejects that would have run correctly. "
   "<b>That is incompleteness; describe it precisely.</b>",
   "Implement unification with an occurs check.",
   "<b>Implement Hindley–Milner</b> for a small functional language "
   "and verify it infers principal types.",
   "Construct a program where HM infers a type you did not expect, and "
   "explain it.",
   "<b>Demonstrate Java's array covariance hole</b> and the runtime "
   "exception it produces.",
   "Implement variance checking for a generic container.",
   "Write a shader, then write the equivalent C, and compare the generated "
   "code. <b>Explain the difference using aliasing.</b>",
 ],
 "selfcheck": [
   "What theorem does a type system prove, and why is it weak?",
   "State Rice's theorem's consequence for type checking.",
   "Define sound and complete, and say who gives up which.",
   "How does an inference rule become code?",
   "Describe Hindley–Milner and say what breaks it.",
   "State the variance rule and explain Java's array hole.",
   "Name six ways shader type systems differ from C.",
   "Why do those restrictions enable better optimisation?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Intermediate Representation and SSA",
 "subtitle": "The decision everything downstream depends on.",
 "question": "What shape should the program have for optimisation?",
 "outcomes": [
     "Build a control flow graph from an AST.",
     "Compute dominators and dominance frontiers.",
     "Place φ functions and rename to construct SSA.",
     "Explain why SSA makes optimisation practical.",
     "Destruct SSA correctly, including the swap problem.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The control flow graph",
   "blurb": "Making control explicit."},

  {"t": "callout", "title": "Basic blocks and the graph over them",
   "kind": "The structure",
   "body": ["<b>A basic block is a maximal straight-line run of "
            "instructions</b> — entered only at the top, left only at the "
            "bottom.",
            "<b>So control flow within a block is trivial</b>, and all the "
            "interesting structure is in the edges between blocks.",
            "<b>Leaders start blocks:</b> the first instruction, any "
            "branch target, and anything following a branch.",
            "<b>The CFG makes implicit control explicit</b>, which is the "
            "precondition for every dataflow analysis in Module 08 — you "
            "cannot compute what reaches a point without knowing what "
            "precedes it."]},

  {"t": "section", "label": "Part 2", "title": "SSA",
   "blurb": "One definition per value."},

  {"t": "code", "kicker": "SSA", "title": "What the form is, and what phi does",
   "lang": "text", "code": """
  BEFORE                         AFTER (SSA)
    x = 1                          x1 = 1
    if (c)                         if (c)
        x = 2                          x2 = 2
    y = x + 1                      x3 = phi(x1, x2)
                                   y1 = x3 + 1

  EVERY VARIABLE IS ASSIGNED EXACTLY ONCE.

  phi is not a real instruction. It says: "this value is x1 if we
  arrived from the first predecessor, x2 if from the second."
  It must sit at the TOP of a block, and all phis in a block are
  conceptually SIMULTANEOUS -- not sequential.

  WHAT THIS BUYS:
    * "where is this value defined?" -> ONE answer, always
    * def-use chains are explicit, no analysis needed
    * constant propagation becomes local
    * dead code elimination becomes "no uses -> delete"
    * every value has a single, unambiguous meaning
""",
   "caption": "<b>The whole payoff is that the definition is unique</b>, "
              "which turns a search into a pointer dereference.",
   "note": "The simultaneity of phis matters for Part 4's swap problem."},

  {"t": "callout", "title": "SSA is why modern optimisation is practical",
   "kind": "The central claim, restated",
   "body": ["<b>Without SSA, 'what is the value of x here?' requires a "
            "dataflow analysis</b> over the whole function, redone "
            "whenever anything changes.",
            "<b>With SSA it is a pointer.</b> The use names its unique "
            "definition directly.",
            "<b>So analyses that were quadratic become linear</b>, and "
            "optimisations that were too expensive to run become cheap "
            "enough to run on every function at every level.",
            "<b>LLVM, GCC, HotSpot, V8, and SPIR-V are all SSA.</b> "
            "<b>SPIR-V is SSA in its file format</b>, which means every "
            "shader you have ever written was compiled through it "
            "(Module 13)."]},

  {"t": "section", "label": "Part 3", "title": "Constructing it",
   "blurb": "Dominance, frontiers, and renaming."},

  {"t": "eq", "kicker": "Dominance", "title": "The relation that drives construction",
   "eqs": [
     ("A dominates B  ⟺  every path from entry to B passes through A",
      "A strictly dominates B if additionally A ≠ B."),
     ("idom(B) = the immediate dominator",
      "The closest strict dominator. These form the dominator tree."),
     ("DF(A) = { B : A dominates a predecessor of B, but not B itself }",
      "The dominance frontier — exactly where A's definitions stop being "
      "the only ones that reach."),
   ],
   "caption": "<b>Place a φ for a variable at the dominance frontier of "
              "every block defining it</b>, iterating to a fixpoint.",
   "note": "Defining DF as 'where dominance runs out' is the intuition "
           "that makes placement obvious."},

  {"t": "code", "kicker": "Construction", "title": "The two phases",
   "lang": "text", "code": """
  PHASE 1 -- PLACE PHI FUNCTIONS
      compute the dominator tree         (Lengauer-Tarjan, or the
                                          simple iterative algorithm --
                                          the simple one is fast enough)
      compute dominance frontiers        (one pass up the dom tree)

      for each variable v:
          W = { blocks that assign v }
          while W not empty:
              b = W.pop()
              for each d in DF(b):
                  if d has no phi for v yet:
                      insert phi for v at the top of d
                      W.add(d)           # the phi is itself a DEF

  PHASE 2 -- RENAME
      walk the dominator tree in preorder, keeping a stack of the
      current name for each variable:
          on a DEF:  push a fresh name
          on a USE:  replace with the stack top
          on a phi operand in a SUCCESSOR: use the stack top for
              the edge we arrived on
          on leaving a block: pop everything pushed in it

  Both phases are near-linear in practice.
""",
   "caption": "<b>The worklist in phase 1 must re-add d</b>, because "
              "inserting a φ creates a new definition that may itself "
              "need φs downstream.",
   "note": "That iteration is the step people omit and then get wrong "
           "answers from."},

  {"t": "section", "label": "Part 4", "title": "Destruction",
   "blurb": "Getting back to a machine."},

  {"t": "callout", "title": "φ is not an instruction, so it must be removed",
   "kind": "The destruction problem",
   "body": ["<b>No machine has a φ.</b> Before code generation, each φ "
            "becomes copies placed at the end of each predecessor block.",
            "<b>The naive translation is wrong.</b> Because φs in a block "
            "execute <i>simultaneously</i>, a group of them can describe a "
            "permutation — and sequential copies destroy it.",
            "<b>The swap problem:</b> "
            "<code>a2 = φ(b1,…), b2 = φ(a1,…)</code> means swap. "
            "Emitting <code>a = b; b = a</code> loses a.",
            "<b>So the copies form a parallel copy that must be "
            "sequentialised correctly</b> — find cycles, break each with "
            "one temporary. <b>This is a real bug in real compilers, and "
            "it is why destruction is its own phase.</b>"]},

  {"t": "bullets", "kicker": "Also", "title": "The other destruction concerns",
   "items": [
     "<b>Critical edges must be split</b> — an edge from a block with "
     "several successors to one with several predecessors has nowhere to "
     "put the copy.",
     "",
     "<b>Coalescing removes most of the copies</b> by assigning the "
     "related values the same register (Module 11).",
     "",
     "<b>Lost-copy and swap problems</b> both arise from naive "
     "translation after aggressive copy propagation.",
     "",
     "<b>Some compilers stay in SSA through register allocation</b> — "
     "SSA interference graphs are chordal, which makes colouring "
     "polynomial (Module 11).",
   ],
   "footnote": "<b>Critical edge splitting is cheap insurance</b> and most "
               "compilers simply do it before destruction unconditionally."},
 ],
 "takeaways": [
   "A basic block is a maximal straight-line run; the CFG over blocks makes "
   "control explicit, which is the precondition for dataflow analysis.",
   "In SSA every variable is assigned exactly once, so 'where is this "
   "defined?' has one answer and def-use chains are explicit.",
   "φ is not a real instruction — it selects by incoming edge, "
   "sits at the top of a block, and all φs in a block are "
   "simultaneous.",
   "Place φ for a variable at the dominance frontier of every block "
   "defining it, iterating because each inserted φ is itself a "
   "definition.",
   "Renaming walks the dominator tree with a stack of current names per "
   "variable.",
   "Destruction must sequentialise parallel copies correctly — the "
   "swap problem is a real bug in real compilers.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The control flow graph"),
  ("callout", "Basic blocks, and the graph over them",
   ["<b>A basic block is a maximal straight-line sequence of "
    "instructions</b> — control enters only at the first instruction "
    "and leaves only after the last. No branches in, no branches out, "
    "except at the ends.",
    "<b>So control flow <i>within</i> a block is entirely trivial</b>, and "
    "all the interesting structure lives in the edges between blocks. That "
    "separation is the whole reason for the construct.",
    "<b>Blocks are found by identifying <i>leaders</i>:</b> the first "
    "instruction of the function, any instruction that is a branch target, "
    "and any instruction immediately following a branch. Each leader begins "
    "a block that runs until the next leader.",
    "<b>The CFG makes implicit control flow explicit</b>, which is the "
    "precondition for every dataflow analysis in Module 08 — you "
    "cannot compute what reaches a program point without first knowing what "
    "can precede it. <b>This is the same move as Module 01 &sect;2's "
    "argument about representations:</b> the AST had the control flow too, "
    "but only implicitly, and implicit is the same as absent for the "
    "purposes of analysis."]),

  ("h1", "2 &nbsp; Static single assignment"),
  ("code", """BEFORE                     AFTER (SSA)
  x = 1                      x1 = 1
  if (c)                     if (c)
      x = 2                      x2 = 2
  y = x + 1                  x3 = phi(x1, x2)
                             y1 = x3 + 1

EVERY VARIABLE ASSIGNED EXACTLY ONCE.

phi is NOT a real instruction. It selects by which predecessor
we arrived from. It sits at the TOP of a block, and all phis in
a block are SIMULTANEOUS, not sequential (see section 4).

WHAT IT BUYS:
  "where is this defined?"  -> exactly one answer, always
  def-use chains            -> explicit, no analysis
  constant propagation      -> becomes local
  dead code elimination     -> "no uses" means delete"""),
  ("callout", "SSA is why modern optimisation is practical",
   ["<b>Without SSA, answering 'what is the value of x at this point?' "
    "requires a dataflow analysis over the whole function</b> (Module 08) "
    "— and that analysis must be redone, or carefully invalidated, "
    "every time any transformation changes anything.",
    "<b>With SSA it is a pointer dereference.</b> The use names its unique "
    "definition directly, and transformations maintain that property "
    "incrementally as they go.",
    "<b>So analyses that were quadratic become linear, and optimisations "
    "that were too expensive to run become cheap enough to run on every "
    "function at every optimisation level.</b> That is the difference "
    "between an optimisation existing in the literature and existing in "
    "your compiler.",
    "<b>LLVM, GCC, HotSpot, V8, and SPIR-V are all SSA-based.</b> <b>SPIR-V "
    "is SSA in its on-disk format</b>, not merely internally — which "
    "means <b>every shader you have ever written was compiled through an "
    "SSA representation you can disassemble and read</b> (Module 13). That "
    "is an unusually direct connection between a compiler-theory idea and "
    "something already on your machine."]),

  ("break",),
  ("h1", "3 &nbsp; Constructing SSA"),
  ("eq", "DF(A) = { B : A dominates a predecessor of B, and A does not "
         "strictly dominate B }"),
  ("p", "<b>A dominates B</b> when every path from the entry block to B "
        "passes through A. The <b>immediate dominator</b> idom(B) is the "
        "closest strict dominator, and these form the <b>dominator "
        "tree</b>. <b>The dominance frontier DF(A) is where A's dominance "
        "runs out</b> — the first blocks reachable from A that A does "
        "not itself dominate, which is precisely where a definition in A "
        "stops being the only one that can reach. <b>So that is exactly "
        "where a &phi; is needed</b>, and stating the frontier that way "
        "makes the placement rule obvious rather than magical."),
  ("code", """PHASE 1 -- PLACE PHIS
  compute the dominator tree, then dominance frontiers
  for each variable v:
      W = { blocks assigning v }
      while W not empty:
          b = W.pop()
          for each d in DF(b):
              if d has no phi for v:
                  insert phi for v at top of d
                  W.add(d)        # the phi is ITSELF a definition

PHASE 2 -- RENAME
  walk the dominator tree in preorder with a stack per variable:
      DEF  -> push a fresh name
      USE  -> replace with stack top
      phi operand in a successor -> stack top for THIS edge
      leaving a block -> pop everything pushed in it"""),
  ("p", "<b>The <code>W.add(d)</code> is the step people omit.</b> "
        "Inserting a &phi; creates a new definition of v in block d, and "
        "that definition may itself require &phi;s at d's dominance "
        "frontier. Without the iteration the construction terminates with "
        "missing &phi;s, the IR verifier passes if it is not checking "
        "dominance, and the wrong values are used at merge points — a "
        "miscompile of exactly the kind Module 01 &sect;4 described."),

  ("h1", "4 &nbsp; Destructing SSA"),
  ("callout", "&phi; is not an instruction, so it must be removed",
   ["<b>No machine has a &phi; instruction.</b> Before code generation, "
    "each &phi; must be replaced by ordinary copies placed at the end of "
    "each predecessor block — the copy on edge <i>i</i> assigns the "
    "&phi;'s <i>i</i>-th operand to its result.",
    "<b>The naive translation is wrong.</b> Because all the &phi;s at the "
    "top of a block execute <i>simultaneously</i>, a group of them can "
    "collectively describe a permutation of values — and emitting the "
    "copies sequentially destroys it.",
    "<b>The swap problem is the canonical case:</b> "
    "<code>a2 = &phi;(b1, &hellip;)</code> together with "
    "<code>b2 = &phi;(a1, &hellip;)</code> means 'swap a and b on this "
    "edge'. Emitting <code>a = b</code> then <code>b = a</code> loses the "
    "original a entirely and assigns b to both.",
    "<b>So the copies form a <i>parallel copy</i> that must be "
    "sequentialised correctly:</b> build the dependency graph, emit the "
    "copies that are not part of a cycle in topological order, and break "
    "each remaining cycle with one temporary. <b>This is a real bug that "
    "has shipped in real compilers</b>, it only manifests after copy "
    "propagation has made the permutation possible, and it is why SSA "
    "destruction is treated as its own carefully-tested phase rather than a "
    "mechanical rewrite."]),
  ("ul", ["<b>Critical edges must be split.</b> An edge from a block with "
          "multiple successors to a block with multiple predecessors has "
          "nowhere to put the copy — putting it in the source block "
          "executes it on the wrong paths, and putting it in the "
          "destination executes it for the wrong predecessors. <b>Insert an "
          "empty block on the edge.</b> It is cheap insurance and most "
          "compilers do it unconditionally before destruction.",
          "<b>Coalescing removes most of the inserted copies</b> by "
          "assigning the &phi;'s operands and result the same register, "
          "which is a register allocation concern (Module 11). A naive "
          "destruction followed by good coalescing is usually better than a "
          "clever destruction.",
          "<b>The lost-copy problem</b> is the swap problem's sibling: "
          "aggressive copy propagation can extend a value's live range "
          "across the point where the copy was to be inserted, so the "
          "inserted copy overwrites a value still needed.",
          "<b>Some compilers remain in SSA through register "
          "allocation.</b> <b>SSA interference graphs are chordal</b>, "
          "which makes optimal colouring polynomial rather than NP-hard "
          "— a genuinely surprising result that Module 11 returns "
          "to."]),
 ],
 "resources": [
   ("Cytron, Ferrante, Rosen, Wegman & Zadeck &mdash; Efficiently Computing "
    "SSA Form (free)",
    "https://dl.acm.org/doi/10.1145/115372.115320",
    "<b>The original construction of &sect;3</b>, including dominance "
    "frontiers. Still the clearest statement of the placement argument."),
   ("Cooper, Harvey & Kennedy &mdash; A Simple, Fast Dominance Algorithm "
    "(free)",
    "https://web.archive.org/web/20230131180704/https://www.cs.rice.edu/~keith/Embed/dom.pdf",
    "<b>The iterative dominator algorithm</b> — simpler than "
    "Lengauer&ndash;Tarjan and faster on real CFGs. Four pages; implement "
    "this one."),
   ("Briggs, Cooper, Harvey & Simpson &mdash; Practical Improvements to "
    "the Construction and Destruction of SSA Form (free)",
    "https://www.cs.princeton.edu/courses/archive/spr04/cos598C/papers/SSADestruction.pdf",
    "<b>The &sect;4 swap and lost-copy problems</b>, named and solved by "
    "the people who found them."),
   ("LLVM Language Reference, and SSA Book (free)",
    "https://pfalcon.github.io/ssabook/latest/book-full.pdf",
    "A full free book on SSA, and the IR specification to read alongside "
    "it."),
 ],
 "exercises": [
   "Build a CFG from your AST and render it with Graphviz.",
   "<b>Implement the Cooper–Harvey–Kennedy dominator "
   "algorithm</b> and verify it against a brute-force definition.",
   "Compute dominance frontiers and check them by hand on a small CFG.",
   "<b>Implement φ placement with the worklist</b>, then remove the "
   "<code>W.add(d)</code> line and find a program that now gets wrong "
   "answers.",
   "Implement renaming over the dominator tree.",
   "<b>Write an IR verifier that checks dominance</b> — every use is "
   "dominated by its definition.",
   "Compare your SSA against <code>clang -S -emit-llvm -O1</code> on the "
   "same source.",
   "<b>Implement naive φ destruction and construct the swap "
   "problem.</b> Then fix it with cycle breaking.",
   "Implement critical edge splitting and show a case that needs it.",
   "<b>Disassemble a SPIR-V shader</b> and identify its φ "
   "instructions and basic blocks.",
 ],
 "selfcheck": [
   "Define a basic block and say how leaders are found.",
   "What is SSA and what does the single-assignment property buy?",
   "What does φ mean, where does it sit, and why are φs "
   "simultaneous?",
   "Define dominance, immediate dominance, and the dominance frontier.",
   "Why is the dominance frontier the right place for a φ?",
   "Why must φ placement iterate?",
   "Describe the renaming walk.",
   "State the swap problem and its fix.",
   "What is a critical edge and why split it?",
 ],
},

]
