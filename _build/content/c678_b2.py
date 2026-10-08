# -*- coding: utf-8 -*-
"""CSCE 678 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "The Network Underneath",
 "subtitle": "What the wire actually gives you, and what it charges.",
 "question": "What should you build on — and what does it cost?",
 "outcomes": [
     "Compare TCP and UDP on the properties that matter.",
     "Explain head-of-line blocking and when it is fatal.",
     "Reason about bandwidth-delay product and congestion control.",
     "Explain NAT traversal and why peer-to-peer is hard.",
     "Choose a transport and justify it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "TCP and UDP",
   "blurb": "Two answers to the same unreliable network."},

  {"t": "table", "kicker": "Transports", "title": "What each gives and withholds",
   "header": ["Property", "TCP", "UDP"],
   "widths": [3.0, 4.3, 4.8],
   "rows": [
     ["<b>Delivery</b>", "<b>Reliable, retransmitted</b>", "<b>Best effort; you retry or you do not</b>"],
     ["<b>Ordering</b>", "<b>In order — and that is the problem</b>", "<b>Any order; you sequence yourself</b>"],
     ["Framing", "A byte stream; you frame it", "Datagrams, preserved whole"],
     ["<b>Congestion control</b>", "<b>Built in, and mandatory</b>", "<b>Yours to implement, and you must</b>"],
     ["<b>Head-of-line blocking</b>", "<b>Yes. One lost packet stalls all</b>", "<b>None</b>"],
     ["Connection", "Handshake; stateful", "<b>Stateless; NAT hates it</b>"],
   ],
   "footnote": "<b>The decisive row is head-of-line blocking</b>, and the "
               "reason is on the next slide.",
   "note": "Resist the 'TCP is reliable so use TCP' reflex here."},

  {"t": "callout", "title": "TCP's ordering guarantee is what makes it wrong for games",
   "kind": "The key insight of the module",
   "body": ["<b>TCP delivers bytes in order.</b> So if packet 7 is lost, "
            "packets 8, 9, and 10 <i>arrive</i> but are held in the kernel "
            "buffer until 7 is retransmitted and arrives.",
            "<b>That is one extra round trip of delay on data you "
            "already have.</b>",
            "<b>For a file transfer this is exactly right</b> — you need "
            "all the bytes and the order is the point.",
            "<b>For a game it is exactly wrong.</b> Position update 7 is "
            "<i>obsolete</i> the moment update 8 exists. <b>Waiting for "
            "stale data before showing fresh data is the worst possible "
            "trade</b>, and it is TCP's central promise."]},

  {"t": "callout", "title": "So real games send UDP and rebuild what they need",
   "kind": "The consequence",
   "body": ["<b>Unreliable-unordered for state</b> — positions, "
            "orientations. A dropped one is replaced by the next anyway.",
            "<b>Reliable-ordered for events</b> — a chat message, a "
            "weapon pickup, a death. Implemented over UDP with sequence "
            "numbers and acknowledgements.",
            "<b>So you rebuild a subset of TCP, per channel, with the "
            "semantics each channel actually needs.</b>",
            "<b>That is what ENet, QUIC, and every game networking library "
            "do</b> — and <b>QUIC is the acknowledgement that this was "
            "right</b>, since HTTP/3 abandoned TCP for exactly the "
            "head-of-line reason."]},

  {"t": "section", "label": "Part 2", "title": "Capacity",
   "blurb": "Bandwidth, delay, and the product of the two."},

  {"t": "eq", "kicker": "BDP", "title": "Bandwidth-delay product",
   "eqs": [
     ("BDP = bandwidth × round-trip time",
      "The number of bytes 'in flight' on the wire at full utilisation."),
     ("100 Mb/s × 100 ms = 1.25 MB",
      "So you must have 1.25 MB unacknowledged to saturate that link."),
     ("Window < BDP ⟹ you cannot fill the pipe",
      "Throughput becomes window / RTT, no matter how fast the link is."),
   ],
   "caption": "<b>This is why a fast link to a distant server is slow</b> "
              "until the window scales — and why TCP slow start hurts "
              "short connections.",
   "note": "BDP explains a lot of otherwise-mysterious throughput "
           "problems."},

  {"t": "callout", "title": "Bufferbloat: latency from too much buffer",
   "kind": "The counterintuitive one",
   "body": ["<b>Loss-based congestion control (Reno, CUBIC) speeds up "
            "until packets drop.</b> Loss is its only congestion signal.",
            "<b>So it fills every buffer between the endpoints</b> before "
            "it backs off — and consumer routers have very large "
            "buffers.",
            "<b>Full buffers mean queueing delay.</b> A saturated link can "
            "show RTTs of seconds, with no packet loss at all.",
            "<b>This is why a download ruins a game on the same "
            "connection</b>, and why BBR, CoDel, and fq_codel exist "
            "— they target delay rather than loss. <b>More buffer made "
            "latency worse</b>, which is worth remembering generally."]},

  {"t": "section", "label": "Part 3", "title": "NAT",
   "blurb": "Why peer-to-peer is harder than it should be."},

  {"t": "code", "kicker": "NAT", "title": "Why two clients cannot just connect",
   "lang": "text", "code": """
  Both peers are behind NAT. Neither has a public address.
  Neither can accept an inbound connection. There is no
  address for either to dial.

  THE TECHNIQUES, in order of preference:

    STUN  -- ask a public server "what address do you appear
             to come from?"  Learn your own mapped endpoint.

    HOLE PUNCHING -- both peers send to each other's mapped
             endpoint simultaneously. Each outbound packet
             creates a NAT mapping that lets the other's
             inbound packet through. Works for CONE NATs.

    TURN  -- relay everything through a public server.
             ALWAYS works. Costs you bandwidth and adds a hop
             of latency. This is the fallback, not the plan.

    ICE   -- try all of the above, in parallel, pick what works.
             WebRTC does this and you should too.

  SYMMETRIC NAT assigns a DIFFERENT external port per
  destination, so the address STUN taught you is wrong for
  any other peer. Hole punching fails. ~8-20% of users.
  You need TURN, and you will pay for it.
""",
   "caption": "<b>Symmetric NAT is why every P2P system needs relay "
              "servers</b> — so 'peer-to-peer saves server costs' is "
              "only partly true.",
   "note": "The cost argument is the one that decides architectures."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "The decision, with reasons."},

  {"t": "table", "kicker": "Decision", "title": "What to build on",
   "header": ["Need", "Use", "Why"],
   "widths": [3.1, 3.6, 5.4],
   "rows": [
     ["<b>Real-time state</b>", "<b>UDP, unreliable</b>", "<b>Stale data is worthless; no HOL blocking</b>"],
     ["<b>Real-time + events</b>", "<b>UDP + reliability layer</b>", "<b>ENet, GameNetworkingSockets, QUIC</b>"],
     ["RPC between services", "<b>gRPC over HTTP/2</b>", "Streams, deadlines, tooling"],
     ["<b>Web-facing</b>", "HTTP/3 (QUIC)", "<b>Solves HOL; 0-RTT resumption</b>"],
     ["Bulk transfer", "TCP", "Ordering is what you want"],
     ["<b>Browser real-time</b>", "<b>WebRTC data channels</b>", "<b>The only UDP a browser gets</b>"],
   ],
   "footnote": "<b>Do not write your own reliability layer</b> unless you "
               "have a reason. The libraries above already got the "
               "congestion control right.",
   "note": "The 'don't roll your own' advice matters most for congestion "
           "control, which is subtle."},

  {"t": "callout", "title": "Measure on a bad network or you have not measured",
   "kind": "The discipline",
   "body": ["<b>Localhost has 0.05 ms latency, no loss, no jitter, and "
            "infinite bandwidth.</b> Nothing you learn there transfers.",
            "<b>Test at 50, 150, and 300 ms RTT</b>, with 1%, 5%, and 10% "
            "loss, and with jitter — because mobile networks deliver all "
            "of these.",
            "<b>And test asymmetry and reordering</b>, both of which are "
            "common and both of which break naive implementations.",
            "<b>This is the same rule as CSCE 735's 'measure the real "
            "thing'</b> and CSCE 620's 'random input proves nothing'. "
            "<b>The clean case is not the informative one.</b>"]},
 ],
 "takeaways": [
   "TCP's in-order delivery means one lost packet stalls everything behind "
   "it — right for files, wrong for games where stale data is "
   "worthless.",
   "Real games send UDP and rebuild per-channel reliability, which is what "
   "ENet and QUIC do; HTTP/3 abandoning TCP is the acknowledgement that "
   "this was right.",
   "Bandwidth-delay product is how many bytes must be in flight to "
   "saturate a link; a window below it caps throughput at window/RTT.",
   "Bufferbloat makes latency worse by adding buffer — loss-based "
   "congestion control fills every queue before backing off.",
   "Symmetric NAT defeats hole punching for 8–20% of users, so every "
   "P2P system needs paid relay servers.",
   "Localhost has no latency, loss, or jitter, so anything measured there "
   "has not been measured.",
 ],
 "notes": [
  ("h1", "1 &nbsp; TCP and UDP"),
  ("table", ["Property", "TCP", "UDP"],
   [["<b>Delivery</b>",
     "<b>Reliable</b> — lost segments are retransmitted until "
     "acknowledged.",
     "<b>Best effort.</b> A lost datagram is simply gone; retrying is "
     "your decision and your code."],
    ["<b>Ordering</b>",
     "<b>Strictly in order — and that is the problem</b>, per the "
     "callout below.",
     "Any order, or none. You attach sequence numbers if you need them."],
    ["<b>Framing</b>",
     "A byte stream with no message boundaries; you must frame it "
     "yourself, and forgetting to is a classic bug.",
     "Datagrams, preserved whole. One send is one receive."],
    ["<b>Congestion control</b>",
     "<b>Built in and mandatory</b>, and generally well tuned.",
     "<b>Entirely yours, and you must implement it.</b> UDP traffic with "
     "no congestion control is antisocial and will be throttled."],
    ["<b>Head-of-line blocking</b>",
     "<b>Yes.</b> One lost segment delays every byte behind it.",
     "<b>None.</b> Each datagram is independent."],
    ["<b>Connection</b>",
     "A handshake and per-connection state at both ends.",
     "<b>Stateless</b>, which is why NAT and firewalls treat it badly "
     "(&sect;3)."]],
   [0.17, 0.39, 0.44]),
  ("callout", "TCP's ordering guarantee is what makes it wrong for games",
   ["<b>TCP delivers bytes to the application in order.</b> So if segment "
    "7 is lost, segments 8, 9, and 10 may have <i>arrived</i> at the "
    "machine and be sitting in the kernel's receive buffer — but the "
    "application cannot have them until 7 is retransmitted and arrives.",
    "<b>That is one extra round trip of delay, minimum, on data you "
    "already physically have.</b> At 150 ms RTT it is 150 ms of added "
    "latency applied to everything behind the loss.",
    "<b>For a file transfer this is exactly the right behaviour.</b> You "
    "need every byte and you need them in order; there is no sense in which "
    "byte 8 is useful without byte 7.",
    "<b>For a real-time game it is exactly wrong.</b> Position update 7 is "
    "<i>obsolete</i> the moment update 8 exists — nobody wants to know "
    "where the player was two frames ago. <b>Waiting for stale data before "
    "delivering fresh data is the worst available trade</b>, and it is "
    "precisely TCP's central promise. <b>The guarantee is not too weak; it "
    "is too strong</b>, which is an unusual and important shape of "
    "problem."]),
  ("callout", "So real games send UDP and rebuild what they need",
   ["<b>Unreliable and unordered for state</b> — positions, "
    "orientations, velocities. A dropped update is simply superseded by the "
    "next one, so retransmitting it would deliver something already "
    "worthless.",
    "<b>Reliable and ordered for events</b> — a chat message, a weapon "
    "pickup, a death, a score change. These must arrive, and they must "
    "arrive once. <b>Implemented over UDP with sequence numbers, "
    "acknowledgements, and retransmission.</b>",
    "<b>So you end up rebuilding a subset of TCP, per channel, with the "
    "semantics each channel actually requires.</b> The important word is "
    "<i>per channel</i>: a loss on the chat channel must not delay the "
    "position channel, which is precisely what TCP cannot offer.",
    "<b>That is what ENet, Valve's GameNetworkingSockets, and QUIC all "
    "do.</b> <b>QUIC is the mainstream acknowledgement that this analysis "
    "was right</b> — HTTP/3 abandoned TCP in favour of independent "
    "streams over UDP for exactly the head-of-line-blocking reason, after "
    "the game industry had been doing it for twenty years."]),

  ("h1", "2 &nbsp; Capacity"),
  ("eq", "BDP = bandwidth &times; round-trip time"),
  ("p", "The bandwidth-delay product is the number of bytes that must be "
        "'in flight' — sent but not yet acknowledged — to keep a "
        "link fully utilised. <b>A 100 Mb/s link with a 100 ms RTT has a "
        "BDP of 1.25 MB</b>, so you must have that much unacknowledged data "
        "outstanding at all times or the link idles. <b>If the window is "
        "smaller than the BDP, throughput is capped at window / RTT</b> "
        "regardless of the link's capacity — which is why a fast "
        "connection to a distant server can be slow until window scaling "
        "takes effect, and why TCP slow start is so costly for short "
        "connections. It is also why QUIC's 0-RTT connection resumption "
        "matters."),
  ("callout", "Bufferbloat: latency caused by too much buffer",
   ["<b>Loss-based congestion control — Reno, CUBIC — increases "
    "its sending rate until packets are dropped.</b> Loss is its only "
    "signal that the path is congested.",
    "<b>So it fills every buffer between the two endpoints before it backs "
    "off</b>, and consumer routers and modems were built with very large "
    "buffers on the theory that dropping packets is bad.",
    "<b>Full buffers mean queueing delay.</b> A saturated link can show "
    "round-trip times of one or two <i>seconds</i>, with no packet loss "
    "whatsoever — every packet arrives, having waited in a queue.",
    "<b>This is why a large download ruins a game on the same "
    "connection</b>, and why BBR, CoDel, and fq_codel were developed "
    "— they treat delay, or queue occupancy, as the congestion signal "
    "rather than loss. <b>Adding buffer made latency dramatically "
    "worse</b>, which is worth carrying as a general lesson: <b>a buffer "
    "trades latency for throughput, and that trade is not always the one "
    "you want</b> (CSCE 650 Module 06 made the same point about render "
    "queues)."]),

  ("break",),
  ("h1", "3 &nbsp; NAT and peer-to-peer"),
  ("code", """Both peers are behind NAT. Neither has a public address.
Neither can accept an inbound connection. There is no address
for either one to dial.

  STUN   ask a public server "what address do I appear to
         come from?" -- learn your own mapped endpoint.

  HOLE PUNCHING
         both peers send to each other's mapped endpoint at
         the same time. Each OUTBOUND packet creates a NAT
         mapping that admits the other's INBOUND packet.
         Works for cone NATs.

  TURN   relay everything through a public server. ALWAYS
         works. Costs bandwidth and adds a latency hop.
         The fallback, not the plan.

  ICE    try all of the above in parallel and use whatever
         works. WebRTC does this; so should you.

SYMMETRIC NAT uses a DIFFERENT external port per destination,
so the address STUN taught you is wrong for any other peer.
Hole punching fails. Roughly 8-20% of users. You need TURN."""),
  ("p", "<b>Symmetric NAT is why every peer-to-peer system needs relay "
        "servers anyway</b>, which substantially undercuts the usual "
        "argument that P2P saves on server costs. <b>You still run "
        "infrastructure, you still pay for bandwidth, and you now have two "
        "code paths to test instead of one</b> — and the relayed path "
        "is the one your least-well-connected users will be on. The honest "
        "framing is that P2P reduces bandwidth cost for the majority and "
        "adds complexity for everyone."),

  ("h1", "4 &nbsp; Choosing a transport"),
  ("table", ["If you need", "Use", "Because"],
   [["<b>Real-time state updates</b>", "<b>UDP, unreliable, unordered.</b>",
     "<b>Stale data is worthless and head-of-line blocking is fatal</b> "
     "(&sect;1)."],
    ["<b>Real-time state <i>and</i> reliable events</b>",
     "<b>UDP with a per-channel reliability layer</b> — ENet, "
     "GameNetworkingSockets, or QUIC.",
     "<b>Do not write your own.</b> These libraries already got the "
     "congestion control right, and congestion control is subtle enough "
     "that getting it wrong makes you a bad network citizen."],
    ["<b>RPC between internal services</b>", "gRPC over HTTP/2.",
     "Streaming, deadlines, cancellation, and mature tooling. Worth the "
     "dependency."],
    ["<b>Anything web-facing</b>", "<b>HTTP/3, which is QUIC.</b>",
     "<b>Solves head-of-line blocking per stream</b>, and 0-RTT resumption "
     "removes a round trip from reconnections."],
    ["<b>Bulk transfer</b>", "TCP.",
     "Ordering is exactly what you want, and the congestion control is "
     "well tuned for it."],
    ["<b>Real-time from a browser</b>",
     "<b>WebRTC data channels.</b>",
     "<b>The only way to get UDP semantics in a browser</b>, and it brings "
     "ICE (&sect;3) with it."]],
   [0.22, 0.30, 0.48]),
  ("callout", "Measure on a bad network, or you have not measured",
   ["<b>Localhost has about 0.05 ms of latency, no loss, no jitter, no "
    "reordering, and effectively infinite bandwidth.</b> It is not a "
    "network; it is a memory copy with a socket API.",
    "<b>Test at 50, 150, and 300 ms RTT, with 1%, 5%, and 10% loss, and "
    "with jitter</b> — because mobile networks routinely deliver all "
    "of these simultaneously, and your users are on them.",
    "<b>And test asymmetry and reordering.</b> Consumer uplinks are a "
    "fraction of downlinks, and packets genuinely arrive out of order on "
    "multipath routes. <b>Both break naive implementations</b> in ways "
    "that are hard to diagnose after the fact.",
    "<b>This is the same rule as CSCE 735's insistence on measuring the "
    "real workload and CSCE 620's observation that random input proves "
    "nothing.</b> <b>The clean case is not the informative one</b> "
    "— three courses, three domains, one conclusion, which suggests "
    "it is a fact about testing rather than about networks."]),
 ],
 "resources": [
   ("Glenn Fiedler &mdash; UDP vs TCP, and Reliability over UDP (free)",
    "https://gafferongames.com/post/udp_vs_tcp/",
    "<b>The &sect;1 argument</b>, made concretely and with code. The whole "
    "series is worth reading."),
   ("Ilya Grigorik &mdash; High Performance Browser Networking (free "
    "book)",
    "https://hpbn.co/",
    "<b>Free in full.</b> The best treatment of &sect;2 — BDP, "
    "congestion control, and why latency dominates — and strong on "
    "WebRTC for &sect;3."),
   ("Gettys & Nichols &mdash; Bufferbloat: Dark Buffers in the Internet "
    "(free)",
    "https://queue.acm.org/detail.cfm?id=2071893",
    "The &sect;2 callout, from the people who identified and named the "
    "problem."),
   ("RFC 8445 (ICE), and Valve's GameNetworkingSockets (free)",
    "https://github.com/ValveSoftware/GameNetworkingSockets",
    "The &sect;3 traversal machinery, and a production implementation of "
    "the &sect;4 recommendation with readable source."),
 ],
 "exercises": [
   "<b>Demonstrate head-of-line blocking:</b> send numbered messages over "
   "TCP with 5% loss and plot delivery time against sequence number.",
   "Send the same over UDP and compare the plots.",
   "Implement sequence numbers and acknowledgements over UDP for a "
   "reliable channel.",
   "<b>Add a second, unreliable channel</b> and show that loss on one does "
   "not delay the other.",
   "<b>Compute the BDP</b> for three real links you have access to, and "
   "measure whether you achieve full throughput.",
   "<b>Reproduce bufferbloat:</b> saturate your uplink and measure RTT "
   "during the transfer. Report the before and after.",
   "Enable fq_codel if you can and measure again.",
   "Implement STUN and determine your own NAT type.",
   "<b>Attempt hole punching</b> between two machines on different "
   "networks and report whether it worked.",
   "Measure a protocol of yours at 50, 150, and 300 ms RTT with jitter, "
   "and plot the degradation.",
 ],
 "selfcheck": [
   "Compare TCP and UDP on six properties.",
   "Explain head-of-line blocking and why TCP's guarantee is too strong "
   "for games.",
   "What two channel types does a game need, and why?",
   "Define bandwidth-delay product and say what happens when the window "
   "is smaller.",
   "Explain bufferbloat and why more buffer made latency worse.",
   "Describe STUN, hole punching, TURN, and ICE.",
   "Why does symmetric NAT undercut the P2P cost argument?",
   "Give six transport choices with reasons.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Time, Clocks, and Ordering",
 "subtitle": "There is no now.",
 "question": "What does it mean for one event to happen before another?",
 "outcomes": [
     "Explain why physical clocks cannot be trusted.",
     "Define the happens-before relation.",
     "Implement Lamport and vector clocks and state what each "
     "captures.",
     "Explain hybrid logical clocks and TrueTime.",
     "Explain why timestamps are the wrong conflict resolution.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Physical time lies",
   "blurb": "Every assumption you have about clocks is wrong."},

  {"t": "bullets", "kicker": "Clocks", "title": "Ways the wall clock betrays you",
   "items": [
     "<b>Clocks drift</b> — a cheap crystal is off by seconds per day, "
     "and temperature changes the rate.",
     "",
     "<b>NTP steps them backwards.</b> Two readings can decrease, so a "
     "measured duration can be negative.",
     "",
     "<b>Leap seconds</b> — repeated or smeared, differently by "
     "different vendors on the same day.",
     "",
     "<b>Virtual machines pause.</b> A VM can lose seconds to migration "
     "or to a host under pressure.",
     "",
     "<b>And garbage collection pauses</b> (CSCE 605 M12) — the process "
     "stops, the clock does not, and it wakes up in the future.",
   ],
   "footnote": "<b>Use a monotonic clock for durations and the wall clock "
               "only for displaying times to humans.</b> Mixing them is a "
               "very common bug."},

  {"t": "callout", "title": "A clock reading is a range, not a point",
   "kind": "The right mental model",
   "body": ["<b>Even perfectly synchronised, a reading has uncertainty.</b> "
            "NTP over the internet gives tens of milliseconds; inside a "
            "datacentre, perhaps one.",
            "<b>So 'this happened at 10:00:00.000' means 'somewhere in a "
            "window around then'</b>, and comparing two such readings from "
            "different machines may be meaningless.",
            "<b>Most systems ignore the uncertainty</b> and compare "
            "timestamps as if they were exact — which silently produces "
            "wrong answers when the gap is smaller than the error.",
            "<b>Spanner's TrueTime does the opposite:</b> it returns an "
            "explicit interval and <b>waits out the uncertainty</b> before "
            "committing. <b>Correctness bought with latency</b>, which is "
            "an honest trade and a rare one."]},

  {"t": "section", "label": "Part 2", "title": "Logical time",
   "blurb": "Ordering without clocks."},

  {"t": "eq", "kicker": "Happens-before", "title": "Lamport's relation",
   "eqs": [
     ("a → b  if a and b are in the same process and a comes first",
      "Program order within a process."),
     ("a → b  if a is a send and b is the matching receive",
      "Causality across processes."),
     ("a → b  if a → c and c → b    (transitive)",
      "And if neither a → b nor b → a, the events are CONCURRENT."),
   ],
   "caption": "<b>Concurrent does not mean simultaneous.</b> It means "
              "neither could have influenced the other, which is the only "
              "thing you can actually determine.",
   "note": "That reframing — concurrency as 'no possible influence' — is "
           "the whole idea."},

  {"t": "code", "kicker": "Clocks", "title": "Lamport and vector clocks",
   "lang": "text", "code": """
  LAMPORT CLOCK -- one integer per process.
      on a local event:   c = c + 1
      on send:            c = c + 1; attach c
      on receive(t):      c = max(c, t) + 1

      GUARANTEE:   a -> b  implies  C(a) < C(b)
      NOT:         C(a) < C(b) implies a -> b     <-- the catch
      So it gives a total order, and CANNOT detect concurrency.

  VECTOR CLOCK -- one integer PER PROCESS, at every process.
      on a local event:   V[self] += 1
      on send:            V[self] += 1; attach the whole V
      on receive(W):      V = elementwise max(V, W); V[self] += 1

      V(a) < V(b) elementwise, strictly somewhere  <=>  a -> b
      neither <= the other                         <=>  CONCURRENT

      So vector clocks DETECT concurrency exactly. The cost is
      O(n) space and bandwidth per message, for n processes.
""",
   "caption": "<b>Lamport clocks order; vector clocks detect "
              "concurrency.</b> That difference decides which you need.",
   "note": "The 'NOT' line is the one students miss and then misuse "
           "Lamport clocks."},

  {"t": "section", "label": "Part 3", "title": "Hybrids",
   "blurb": "Wanting both properties at once."},

  {"t": "table", "kicker": "Options", "title": "The clock choices",
   "header": ["Clock", "Captures", "Cost"],
   "widths": [2.8, 4.3, 5.0],
   "rows": [
     ["<b>Physical (NTP)</b>", "<b>Roughly real time; no causality</b>", "<b>Free, and wrong at fine grain</b>"],
     ["<b>Lamport</b>", "A consistent total order", "<b>One integer; no concurrency detection</b>"],
     ["<b>Vector</b>", "<b>Causality exactly</b>", "<b>O(n) per message</b>"],
     ["<b>Hybrid logical (HLC)</b>", "<b>Causality + close to real time</b>", "<b>Small. Widely used now</b>"],
     ["<b>TrueTime</b>", "<b>Real time with bounded error</b>", "<b>GPS and atomic clocks; commit wait</b>"],
     ["Version vectors", "Causality over replicas", "O(replicas); used by Dynamo-likes"],
   ],
   "footnote": "<b>HLC is the practical default</b> — it respects "
               "causality, stays close to wall-clock time, and fits in a "
               "fixed number of bytes.",
   "note": "HLC is underused relative to how well it solves the actual "
           "problem."},

  {"t": "section", "label": "Part 4", "title": "Last write wins",
   "blurb": "The conflict resolution that silently loses data."},

  {"t": "callout", "title": "'Last write wins' decides by a clock that is wrong",
   "kind": "The practical warning of this module",
   "body": ["<b>Two replicas accept concurrent writes; on merge, keep the "
            "one with the later timestamp.</b> Simple, and it is "
            "everywhere.",
            "<b>But the timestamps came from different machines with "
            "unsynchronised clocks.</b> If one is 200 ms fast, its write "
            "always wins — including when it was genuinely first.",
            "<b>So data is discarded silently.</b> There is no error, no "
            "log line, and no way to recover the lost write afterwards.",
            "<b>The alternatives: detect the conflict with version "
            "vectors and surface it; use a CRDT that merges without "
            "choosing</b> (Module 08); <b>or serialise through consensus</b> "
            "(Module 06). <b>LWW is acceptable only when losing a write is "
            "genuinely acceptable</b>, and that should be a stated "
            "decision."]},

  {"t": "callout", "title": "Where this matters in a game",
   "kind": "The netcode connection",
   "body": ["<b>Clients disagree about <i>when</i> everything "
            "happened</b>, because each sees the world at a different "
            "delay.",
            "<b>So the server defines time.</b> A single authoritative "
            "tick number replaces wall-clock time entirely — it is a "
            "Lamport clock with a designated owner.",
            "<b>Clients estimate their offset from server time</b> and "
            "timestamp inputs with the server tick they believe they are "
            "acting on.",
            "<b>And lag compensation rewinds the world to the tick the "
            "shooter saw</b> (Module 11) — which is only possible "
            "because there is one authoritative timeline to rewind."]},
 ],
 "takeaways": [
   "Clocks drift, step backwards, smear leap seconds, and jump after VM "
   "or GC pauses — use a monotonic clock for durations.",
   "A clock reading is a range, not a point; TrueTime makes the "
   "uncertainty explicit and waits it out, buying correctness with latency.",
   "Happens-before captures possible influence, and 'concurrent' means "
   "neither event could have affected the other.",
   "Lamport clocks give a total order but cannot detect concurrency; "
   "vector clocks detect it exactly at O(n) cost per message.",
   "Hybrid logical clocks are the practical default — causality plus "
   "near-real time in a few bytes.",
   "Last-write-wins discards data silently using clocks that disagree; use "
   "it only when losing a write is an accepted decision.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Physical time lies"),
  ("ul", ["<b>Clocks drift.</b> An ordinary quartz crystal is off by "
          "seconds per day, and its rate changes with temperature — so "
          "two machines in the same rack drift apart at different speeds.",
          "<b>NTP steps them backwards.</b> When a correction is applied, "
          "two successive readings of the wall clock can <i>decrease</i>, "
          "<b>so a measured duration can come out negative</b>. Code that "
          "subtracts two wall-clock readings has a latent bug.",
          "<b>Leap seconds.</b> A second is repeated or 'smeared' across a "
          "day, and <b>different vendors smear differently on the same "
          "day</b> — so two correctly configured machines genuinely "
          "disagree about what time it is.",
          "<b>Virtual machines pause.</b> A VM can lose seconds to live "
          "migration or to a host under memory pressure, and resumes with "
          "the wall clock having moved on without it.",
          "<b>And garbage collection pauses</b> (CSCE 605 Module 12). The "
          "process stops; the clock does not. <b>Code resumes believing "
          "very little time has passed and finds itself in the "
          "future</b> — which has caused real outages where a node "
          "held a lease it had already lost. <b>Use a monotonic clock for "
          "durations and the wall clock only for displaying times to "
          "humans</b>; mixing them is among the most common bugs in this "
          "subject."]),
  ("callout", "A clock reading is a range, not a point",
   ["<b>Even when well synchronised, a clock reading carries "
    "uncertainty.</b> NTP over the public internet gives tens of "
    "milliseconds of error; within a datacentre with good peering, perhaps "
    "one; PTP with hardware support, microseconds.",
    "<b>So 'this happened at 10:00:00.000' really means 'somewhere in a "
    "window around then'</b>, and comparing two such readings taken on "
    "different machines is meaningless whenever the difference between them "
    "is smaller than the combined uncertainty.",
    "<b>Most systems ignore this entirely</b> and compare timestamps as "
    "though they were exact — which silently produces wrong orderings "
    "exactly in the close cases, which are the cases where the ordering "
    "mattered.",
    "<b>Google's Spanner does the opposite.</b> Its TrueTime API returns "
    "an explicit interval rather than a point, and <b>a transaction waits "
    "out the uncertainty before committing</b> so that its timestamp is "
    "guaranteed to be in the past for every other node. <b>Correctness "
    "bought with latency</b> — typically a few milliseconds of commit "
    "wait — which is an honest and unusually explicit trade, and it "
    "requires GPS receivers and atomic clocks in every datacentre to keep "
    "the interval small."]),

  ("h1", "2 &nbsp; Logical time"),
  ("eq", "a &rarr; b &nbsp;(happens-before)"),
  ("p", "defined by three rules: <b>a and b are in the same process and a "
        "comes first</b>; <b>a is a send and b is the matching receive</b>; "
        "or <b>transitivity</b> through some intermediate c. <b>If neither "
        "a &rarr; b nor b &rarr; a, the two events are "
        "<i>concurrent</i>.</b> <b>Concurrent does not mean "
        "simultaneous</b> — it means <i>neither could possibly have "
        "influenced the other</i>, which is the only thing a distributed "
        "system can actually determine. That reframing is the whole idea: "
        "give up on knowing what time it was, and settle for knowing what "
        "could have caused what."),
  ("code", """LAMPORT CLOCK -- one integer per process
    local event:  c = c + 1
    send:         c = c + 1; attach c
    receive(t):   c = max(c, t) + 1

  GUARANTEE:  a -> b  implies  C(a) < C(b)
  NOT TRUE:   C(a) < C(b) implies a -> b     <-- the catch
  Gives a total order; CANNOT detect concurrency.

VECTOR CLOCK -- one integer per process, kept at every process
    local event:  V[self] += 1
    send:         V[self] += 1; attach all of V
    receive(W):   V = elementwise max(V, W);  V[self] += 1

  V(a) <= V(b) and strictly less somewhere  <=>  a -> b
  neither <= the other                      <=>  CONCURRENT

  Detects concurrency EXACTLY. Costs O(n) per message."""),
  ("p", "<b>The 'NOT TRUE' line is the one that gets missed</b>, and "
        "missing it leads directly to misusing Lamport clocks for conflict "
        "detection. A Lamport clock tells you that if a caused b then a's "
        "timestamp is smaller — it does not tell you that a smaller "
        "timestamp implies causation, so two unrelated events get ordered "
        "arbitrarily and you cannot tell that from the numbers."),

  ("break",),
  ("h1", "3 &nbsp; The clock choices"),
  ("table", ["Clock", "What it captures", "What it costs"],
   [["<b>Physical (NTP)</b>",
     "<b>Approximately real time, and no causality at all.</b>",
     "<b>Free, and wrong at fine granularity</b> — &sect;1."],
    ["<b>Lamport</b>", "A consistent total order over all events.",
     "<b>One integer.</b> Cannot distinguish concurrent from ordered."],
    ["<b>Vector</b>", "<b>Causality, exactly.</b>",
     "<b>O(n) space and bandwidth per message</b>, which becomes "
     "prohibitive with many participants and requires handling membership "
     "changes."],
    ["<b>Hybrid logical clock (HLC)</b>",
     "<b>Causality, and stays within a bounded distance of real time.</b>",
     "<b>A physical component plus a small logical counter.</b> <b>The "
     "practical default</b> — it respects happens-before, is "
     "meaningful to humans, and fits in a fixed number of bytes. Used by "
     "CockroachDB, MongoDB, and others."],
    ["<b>TrueTime</b>",
     "<b>Real time with an explicit, bounded error interval.</b>",
     "<b>GPS receivers and atomic clocks in every datacentre, plus commit "
     "wait.</b> Spanner. Correct, and only available if you own the "
     "hardware."],
    ["<b>Version vectors</b>",
     "Causality over <i>replicas</i> rather than processes.",
     "O(replicas), which is far smaller than O(clients). Used by Dynamo-"
     "style stores and by CRDTs (Module 08)."]],
   [0.20, 0.35, 0.45]),

  ("h1", "4 &nbsp; Last write wins"),
  ("callout", "'Last write wins' decides by a clock that is wrong",
   ["<b>Two replicas accept concurrent writes to the same key; when they "
    "reconcile, keep whichever carries the later timestamp.</b> It is "
    "simple, it is stateless, and it is extremely widespread — "
    "Cassandra's default, among many others.",
    "<b>But the two timestamps came from different machines with "
    "unsynchronised clocks</b> (&sect;1). If one node's clock is 200 ms "
    "fast, <b>its writes always win</b> — including the ones that "
    "genuinely happened first.",
    "<b>So data is discarded silently.</b> There is no error returned, no "
    "log entry, no metric, and <b>no way to recover the lost write "
    "afterwards</b>, because the losing value was never stored anywhere. "
    "The failure is invisible by construction.",
    "<b>The alternatives, in increasing order of cost:</b> detect the "
    "conflict with version vectors and surface it to the application or the "
    "user (Dynamo's sibling values); <b>use a CRDT that merges without "
    "having to choose</b> (Module 08 &sect;3); or <b>serialise the writes "
    "through consensus</b> so concurrency never arises (Module 06). "
    "<b>Last-write-wins is acceptable only when silently losing a write is "
    "genuinely acceptable</b> — for a cache or a presence indicator it "
    "may well be — <b>and that should be a stated decision rather "
    "than a default inherited from a configuration file.</b>"]),
  ("callout", "Where this matters in a game",
   ["<b>Clients fundamentally disagree about when things happened</b>, "
    "because each one observes the world through a different and varying "
    "delay. There is no shared present moment to appeal to.",
    "<b>So the server defines time.</b> A single authoritative <i>tick "
    "number</i>, incremented at a fixed rate, replaces wall-clock time "
    "entirely — which is to say <b>it is a Lamport clock with a "
    "designated owner</b>, and the designation is what removes the "
    "ambiguity that a general Lamport clock leaves.",
    "<b>Clients estimate their offset from server time</b> — by "
    "measuring round-trip time and smoothing it — and stamp each input "
    "with the server tick they believe they are acting on. The server then "
    "knows not just what the client did but <i>when the client thought it "
    "was doing it</i>.",
    "<b>And lag compensation rewinds the world to the tick the shooter "
    "actually saw</b> (Module 11 &sect;2) before testing the hit. <b>That "
    "is only possible because there is one authoritative timeline to rewind "
    "along</b> — which is a good illustration that choosing a clock "
    "model is an architectural decision, not an implementation detail."]),
 ],
 "resources": [
   ("Lamport &mdash; Time, Clocks, and the Ordering of Events in a "
    "Distributed System (free)",
    "https://lamport.azurewebsites.net/pubs/time-clocks.pdf",
    "<b>The paper that created &sect;2.</b> Short, readable, and one of "
    "the most cited papers in computing for good reason."),
   ("Kleppmann &mdash; Designing Data-Intensive Applications, chapter 8 "
    "('Unreliable Clocks')",
    "https://dataintensive.net/",
    "<b>The &sect;1 catalogue and the &sect;4 warning</b>, with real "
    "incident examples."),
   ("Kulkarni et al. &mdash; Logical Physical Clocks (HLC) (free)",
    "https://cse.buffalo.edu/tech-reports/2014-04.pdf",
    "The &sect;3 default, from the paper that introduced it."),
   ("Corbett et al. &mdash; Spanner: Google's Globally-Distributed "
    "Database (free)",
    "https://research.google/pubs/pub39966/",
    "<b>TrueTime and commit wait</b> — the &sect;1 callout, as "
    "shipped."),
 ],
 "exercises": [
   "<b>Measure clock drift</b> between two machines over an hour, with NTP "
   "disabled.",
   "Write code that subtracts two wall-clock readings and <b>make it "
   "produce a negative duration</b> by stepping the clock.",
   "Implement Lamport clocks and verify the guarantee empirically.",
   "<b>Find two concurrent events whose Lamport timestamps are ordered</b> "
   "and explain why that is not a bug.",
   "Implement vector clocks and build a tool that reports, for any two "
   "events, whether one happened before the other or they are concurrent.",
   "Measure the bandwidth cost of vector clocks as the node count rises "
   "from 3 to 100.",
   "<b>Implement a hybrid logical clock</b> and verify it respects "
   "causality while tracking wall time.",
   "<b>Build a last-write-wins store, skew one node's clock by 200 ms, and "
   "demonstrate silent data loss.</b>",
   "Replace LWW with version vectors and surface the conflict instead.",
   "Implement client-to-server tick offset estimation and measure its "
   "stability under jitter.",
 ],
 "selfcheck": [
   "Give five ways a physical clock betrays you.",
   "Why should durations use a monotonic clock?",
   "Why is a clock reading a range, and what does TrueTime do about it?",
   "Define happens-before and say what 'concurrent' actually means.",
   "State what a Lamport clock guarantees and what it does not.",
   "How do vector clocks detect concurrency, and what do they cost?",
   "Compare six clock schemes.",
   "Why is last-write-wins dangerous, and what are the alternatives?",
   "How does a game define time, and why does that enable lag "
   "compensation?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Replication and Consistency",
 "subtitle": "Several copies, and what you promise about them.",
 "question": "What does a read return when there are many copies?",
 "outcomes": [
     "Compare replication strategies on their failure behaviour.",
     "Define linearizability and distinguish it from serialisability.",
     "Place the consistency models in order of strength.",
     "Explain the session guarantees and why they are enough.",
     "Choose a consistency model deliberately.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Replication strategies",
   "blurb": "Where writes go."},

  {"t": "table", "kicker": "Strategies", "title": "Three ways to replicate",
   "header": ["Strategy", "How", "Failure behaviour"],
   "widths": [2.7, 4.3, 5.1],
   "rows": [
     ["<b>Single leader</b>", "<b>All writes to one node, replicated out</b>", "<b>Simple; the leader is a bottleneck and a SPOF</b>"],
     ["<b>Multi-leader</b>", "Several accept writes; reconcile", "<b>Write conflicts are now your problem</b>"],
     ["<b>Leaderless (quorum)</b>", "<b>Write to w, read from r nodes</b>", "<b>No failover; needs repair</b>"],
   ],
   "footnote": "<b>Single leader is the right default</b> — it "
               "eliminates write conflicts entirely, which is the "
               "expensive problem.",
   "note": "Most teams reach for multi-leader before they need it."},

  {"t": "eq", "kicker": "Quorum", "title": "The quorum condition",
   "eqs": [
     ("w + r > n",
      "Write to w replicas, read from r, out of n. Then any read set "
      "overlaps any write set."),
     ("n=3, w=2, r=2",
      "Tolerates one failure for both reads and writes. The usual "
      "choice."),
     ("w=n, r=1  /  w=1, r=n",
      "Fast reads with slow fragile writes, or the reverse. Pick by "
      "workload."),
   ],
   "caption": "<b>Overlap is the whole mechanism</b> — a read set "
              "that intersects every write set must see the latest write.",
   "note": "The overlap argument is one line and makes quorums obvious."},

  {"t": "callout", "title": "Quorums are weaker than they look",
   "kind": "The caveat that matters",
   "body": ["<b>w + r > n guarantees overlap, not "
            "linearizability.</b> Concurrent writes can still be applied in "
            "different orders at different replicas.",
            "<b>A read can see a newer value and then an older one</b> if "
            "it contacts different replicas on successive attempts.",
            "<b>And a failed write may have reached some replicas</b>, so "
            "it is neither applied nor not applied.",
            "<b>Read repair and anti-entropy converge things "
            "eventually</b>, and 'eventually' is doing real work in that "
            "sentence. <b>If you need linearizability, you need consensus</b> "
            "(Module 06), not a quorum."]},

  {"t": "section", "label": "Part 2", "title": "The models",
   "blurb": "What a read is allowed to return."},

  {"t": "table", "kicker": "Hierarchy", "title": "Consistency models, strongest first",
   "header": ["Model", "Guarantee", "Cost"],
   "widths": [3.0, 4.4, 4.7],
   "rows": [
     ["<b>Linearizable</b>", "<b>Behaves like one copy, in real time</b>", "<b>Consensus; a round trip minimum</b>"],
     ["<b>Sequential</b>", "One order, agreed; not necessarily real time", "Cheaper; surprising to users"],
     ["<b>Causal</b>", "<b>Causally related ops are ordered</b>", "<b>Available under partition. The sweet spot</b>"],
     ["<b>Eventual</b>", "<b>Replicas converge if writes stop</b>", "<b>Cheapest; says almost nothing</b>"],
     ["Read-your-writes", "You see your own writes", "<b>A session guarantee, not a global one</b>"],
     ["<b>Monotonic reads</b>", "Time never goes backwards for you", "Session-level; cheap and valuable"],
   ],
   "footnote": "<b>Causal consistency is the strongest model available "
               "during a partition</b> (Module 05), which is why it is "
               "where the research went.",
   "note": "The causal-is-the-ceiling result is the one worth "
           "remembering."},

  {"t": "callout", "title": "Linearizability: the system behaves like one copy",
   "kind": "The definition worth getting right",
   "body": ["<b>Every operation appears to take effect at a single instant "
            "between its invocation and its response</b>, and that order "
            "respects real time.",
            "<b>So if A's write completes before B's read begins, B sees "
            "it.</b> Even on a different client, even on a different "
            "replica.",
            "<b>It is a <i>recency</i> guarantee about single "
            "objects.</b> Serialisability is an <i>isolation</i> guarantee "
            "about multi-object transactions (CSCE 608). <b>They are "
            "different and orthogonal</b>, and combining both is strict "
            "serialisability.",
            "<b>The cost is at least one round trip to a quorum</b>, which "
            "is why it is unavailable during a partition."]},

  {"t": "section", "label": "Part 3", "title": "Session guarantees",
   "blurb": "Weak globally, consistent enough locally."},

  {"t": "callout", "title": "Most user-visible anomalies are session anomalies",
   "kind": "The practical insight",
   "body": ["<b>'I posted a comment and it vanished' is a "
            "read-your-writes violation.</b> The user hit a replica that "
            "had not received their write.",
            "<b>'The count went 5, 7, 5' is a monotonic reads "
            "violation</b> — two reads landed on replicas at different "
            "stages.",
            "<b>Both are fixable cheaply</b>: route a user's reads to the "
            "replica that took their write, or pass a version token the "
            "replica must have reached.",
            "<b>So you can leave the system eventually consistent and "
            "still eliminate the anomalies people actually notice.</b> "
            "<b>That is usually a much better trade than global strong "
            "consistency.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "Deliberately, and per operation."},

  {"t": "table", "kicker": "Decision", "title": "What needs what",
   "header": ["Operation", "Needs", "Why"],
   "widths": [3.3, 3.5, 5.3],
   "rows": [
     ["<b>Account balance, inventory</b>", "<b>Linearizable</b>", "<b>Double-spend is unacceptable</b>"],
     ["<b>Unique username</b>", "<b>Linearizable</b>", "Uniqueness is a global invariant"],
     ["Social feed", "<b>Causal</b>", "<b>A reply must not precede its parent</b>"],
     ["<b>Like / view counters</b>", "Eventual", "<b>Nobody can tell, and nobody cares</b>"],
     ["Session state", "<b>Read-your-writes</b>", "Only that user observes it"],
     ["<b>Game world state</b>", "<b>Single authority</b>", "<b>Not a consistency model — a referee</b>"],
   ],
   "footnote": "<b>Consistency is per operation, not per system.</b> "
               "Treating one setting as covering everything is the usual "
               "mistake.",
   "note": "The last row sets up Modules 09-11."},

  {"t": "callout", "title": "A game server sidesteps the whole problem",
   "kind": "Why netcode looks different",
   "body": ["<b>There is exactly one authoritative copy of the world: the "
            "server's.</b> Clients hold predictions, not replicas.",
            "<b>So there is no consistency model to choose</b> — no "
            "quorum, no conflict resolution, no convergence. There is an "
            "authority and there are guesses.",
            "<b>Clients are allowed to be wrong, and are corrected</b> "
            "(Module 10). That is a completely different bargain from "
            "replication.",
            "<b>It works because a game has a natural trusted party and a "
            "bounded world</b>. <b>It stops working the moment you need two "
            "authoritative servers</b> — which is why sharding a game "
            "world is genuinely hard."]},
 ],
 "takeaways": [
   "Single-leader replication is the right default because it eliminates "
   "write conflicts, which are the expensive problem.",
   "w + r > n guarantees that read and write sets overlap, but overlap is "
   "not linearizability — quorums still permit reordering and "
   "non-monotonic reads.",
   "Linearizability is a recency guarantee about single objects; "
   "serialisability is an isolation guarantee about transactions. They are "
   "orthogonal.",
   "Causal consistency is the strongest model available during a partition, "
   "which is why the research concentrated there.",
   "Most anomalies users actually notice are session anomalies, and those "
   "are cheap to fix without global strong consistency.",
   "Consistency is chosen per operation, not per system — and a game "
   "server sidesteps it entirely by having one authority and no replicas.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Replication strategies"),
  ("table", ["Strategy", "How it works", "Failure behaviour"],
   [["<b>Single leader</b>",
     "<b>All writes go to one designated node</b>, which replicates them to "
     "followers synchronously or asynchronously.",
     "<b>Simple, and it eliminates write conflicts entirely</b> — "
     "there is one order because there is one writer. <b>The leader is a "
     "throughput bottleneck and a single point of failure</b>, so failover "
     "is required, and failover is where the bugs are (Module 06)."],
    ["<b>Multi-leader</b>",
     "Several nodes accept writes and replicate to each other, reconciling "
     "afterwards.",
     "<b>Write conflicts are now your problem</b> (Module 03 &sect;4), and "
     "they are the expensive problem. Justified across datacentres or for "
     "offline-capable clients, and rarely otherwise."],
    ["<b>Leaderless (quorum)</b>",
     "<b>The client writes to w replicas and reads from r</b>, with no "
     "designated leader at all. Dynamo-style.",
     "<b>No failover to get wrong</b>, since there is nothing to fail over. "
     "Requires read repair and anti-entropy to converge, and gives weaker "
     "guarantees than it appears to — see below."]],
   [0.18, 0.36, 0.46]),
  ("eq", "w + r &gt; n"),
  ("p", "Write to w replicas and read from r, out of n total. <b>The "
        "condition guarantees that any read set intersects any write "
        "set</b>, so a read is guaranteed to contact at least one replica "
        "that has the latest completed write. <b>Overlap is the entire "
        "mechanism.</b> With n = 3, w = 2, r = 2 the system tolerates one "
        "failure for both reads and writes, which is the usual choice; "
        "w = n with r = 1 gives very fast reads and fragile writes, and the "
        "reverse gives the opposite."),
  ("callout", "Quorums are weaker than they look",
   ["<b>w + r &gt; n guarantees overlap, not linearizability.</b> The read "
    "will see <i>a</i> replica holding the latest completed write, but "
    "there is no mechanism forcing all replicas to apply concurrent writes "
    "in the same order.",
    "<b>So a read can return a newer value and a subsequent read an older "
    "one</b>, if the two reads happen to contact different subsets of "
    "replicas — a monotonic-reads violation (&sect;3) arising directly "
    "from the quorum mechanism.",
    "<b>And a write that failed may have reached some replicas before "
    "failing.</b> It is then neither applied nor not applied: it will "
    "persist if those replicas win a future read repair, and vanish "
    "otherwise. <b>The caller was told the write failed.</b>",
    "<b>Read repair and anti-entropy converge things eventually</b>, and "
    "'eventually' is carrying real weight in that sentence — it means "
    "'if writes stop, which they do not'. <b>If you need linearizability, "
    "you need consensus</b> (Module 06), not a quorum. Dynamo-style stores "
    "are frequently deployed on the assumption that w + r &gt; n provides "
    "strong consistency, and it does not."]),

  ("h1", "2 &nbsp; The consistency models"),
  ("table", ["Model", "What it guarantees", "What it costs"],
   [["<b>Linearizable</b>",
     "<b>The system behaves as though there were one copy</b>, and the "
     "order respects real time.",
     "<b>Consensus, and at least one round trip to a quorum.</b> "
     "Unavailable during a partition (Module 05)."],
    ["<b>Sequential</b>",
     "All nodes see operations in the same order, but that order need not "
     "match real time.",
     "Cheaper than linearizable, and <b>surprising to users</b> — your "
     "own write can appear to happen after someone else's later one."],
    ["<b>Causal</b>",
     "<b>Causally related operations are seen in order by everyone; "
     "concurrent ones may differ.</b>",
     "<b>Available during a partition</b>, and it is <b>the strongest "
     "model of which that is true</b> — which is why so much research "
     "went into it."],
    ["<b>Eventual</b>",
     "<b>If writes stop, replicas converge.</b> Nothing is promised while "
     "they do not.",
     "<b>The cheapest, and it says almost nothing</b> — 'returns the "
     "value 42 always' satisfies eventual consistency until a write "
     "arrives."],
    ["<b>Read-your-writes</b>", "You observe your own writes.",
     "<b>A session guarantee</b>, scoped to one client, not a global "
     "property. Cheap (&sect;3)."],
    ["<b>Monotonic reads</b>",
     "Successive reads by one client never go backwards in time.",
     "Also session-scoped, also cheap, and <b>it removes one of the two "
     "anomalies users actually report</b>."]],
   [0.18, 0.40, 0.42]),
  ("callout", "Linearizability: the system behaves like one copy",
   ["<b>Every operation appears to take effect at a single instant between "
    "its invocation and its response</b>, and the resulting total order is "
    "consistent with real time.",
    "<b>So if client A's write completes before client B's read begins, B "
    "sees it</b> — even on a different machine, even hitting a "
    "different replica, with no coordination between A and B. That real-"
    "time requirement is what makes it the strongest practical model and "
    "what makes it expensive.",
    "<b>It is a <i>recency</i> guarantee about single objects.</b> "
    "<b>Serialisability is an <i>isolation</i> guarantee about multi-object "
    "transactions</b> (CSCE 608 Module 08) — that some serial order of "
    "transactions produces the same result. <b>They are different and "
    "orthogonal properties</b>, routinely confused because both are "
    "informally called 'strong consistency'. A system can be serialisable "
    "and not linearizable (transactions may be ordered in a way that "
    "contradicts real time), and combining both is called strict "
    "serialisability.",
    "<b>The cost is at least one round trip to a quorum on every "
    "operation</b> — you cannot answer from a local replica, because "
    "you cannot know whether a newer write exists elsewhere. <b>Which is "
    "exactly why it becomes unavailable during a partition</b> "
    "(Module 05)."]),

  ("break",),
  ("h1", "3 &nbsp; Session guarantees"),
  ("callout", "Most user-visible anomalies are session anomalies",
   ["<b>'I posted a comment and then it vanished' is a read-your-writes "
    "violation.</b> The write went to one replica; the subsequent page load "
    "was served by another that had not yet received it. The data is not "
    "lost and the user has no way to know that.",
    "<b>'The count showed 5, then 7, then 5 again' is a monotonic-reads "
    "violation.</b> Two successive reads landed on replicas at different "
    "stages of replication, so time appeared to run backwards.",
    "<b>Both are fixable cheaply and locally.</b> Route a user's reads to "
    "the replica that accepted their write for some interval; or have the "
    "client carry a version token and require the serving replica to have "
    "caught up to it before answering. Neither requires consensus or a "
    "quorum read.",
    "<b>So the system can remain eventually consistent globally while "
    "eliminating the anomalies people actually notice and complain "
    "about.</b> <b>That is usually a far better trade than global strong "
    "consistency</b>, which costs a round trip on every operation to "
    "prevent anomalies that, in most applications, no single observer is "
    "positioned to detect. <b>Ask what an individual user can actually "
    "see</b>, rather than what the system as a whole guarantees."]),

  ("h1", "4 &nbsp; Choosing"),
  ("table", ["Operation", "Needs", "Why"],
   [["<b>Account balance, inventory decrement, seat booking</b>",
     "<b>Linearizable.</b>",
     "<b>Double-spending or double-booking is unacceptable</b>, and the "
     "invariant is global."],
    ["<b>Unique username registration</b>", "<b>Linearizable.</b>",
     "Uniqueness is a global invariant — two replicas cannot both "
     "accept the same name."],
    ["<b>Social feed, comment threads</b>", "<b>Causal.</b>",
     "<b>A reply must never appear before the comment it replies to</b>, "
     "which is exactly a causal guarantee. Strong consistency would be "
     "overkill."],
    ["<b>Like counts, view counts, metrics</b>", "Eventual.",
     "<b>Nobody can tell, and nobody cares.</b> Approximate counters are "
     "frequently used deliberately."],
    ["<b>Session and preference state</b>", "<b>Read-your-writes.</b>",
     "Only that one user observes it, so a session guarantee is exactly "
     "the right scope (&sect;3)."],
    ["<b>Game world state</b>", "<b>A single authority.</b>",
     "<b>Not a consistency model at all</b> — see below."]],
   [0.26, 0.21, 0.53]),
  ("p", "<b>Consistency is chosen per operation, not per system.</b> "
        "Treating one database setting as covering an entire application is "
        "the usual mistake, and it leads either to paying for "
        "linearizability on like counters or to losing inventory."),
  ("callout", "A game server sidesteps the whole problem",
   ["<b>There is exactly one authoritative copy of the world: the "
    "server's.</b> Clients do not hold replicas — they hold "
    "<i>predictions</i>, which is a different thing with a different "
    "contract.",
    "<b>So there is no consistency model to choose.</b> No quorum, no "
    "conflict resolution, no convergence criterion, no reconciliation "
    "between equals. <b>There is an authority, and there are guesses about "
    "what the authority will say.</b>",
    "<b>Clients are permitted to be wrong and are corrected</b> "
    "(Module 10). That is a completely different bargain from replication, "
    "and it is why the netcode modules look so unlike the first half of "
    "this course despite solving a superficially similar problem.",
    "<b>It works because a game has a natural trusted party and a bounded "
    "world.</b> <b>And it stops working the moment you need two "
    "authoritative servers</b> — at which point you are back to "
    "Module 06 with a hard real-time deadline attached, which is why "
    "sharding a seamless game world across servers is genuinely difficult "
    "and why most games do not."]),
 ],
 "resources": [
   ("Kleppmann &mdash; Designing Data-Intensive Applications, chapters 5, "
    "6 and 9",
    "https://dataintensive.net/",
    "<b>The best treatment of this entire module</b>, particularly the "
    "linearizability-versus-serialisability distinction of &sect;2."),
   ("Herlihy & Wing &mdash; Linearizability: A Correctness Condition for "
    "Concurrent Objects (free)",
    "https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf",
    "The original definition. Worth reading for how carefully it is "
    "stated."),
   ("Terry et al. &mdash; Session Guarantees for Weakly Consistent "
    "Replicated Data (free)",
    "https://dl.acm.org/doi/10.5555/645792.668302",
    "<b>The &sect;3 result</b>, and the paper that named read-your-writes "
    "and monotonic reads."),
   ("DeCandia et al. &mdash; Dynamo: Amazon's Highly Available Key-value "
    "Store (free)",
    "https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf",
    "The quorum system of &sect;1, with the sibling-value conflict "
    "handling that LWW replaced in many later systems."),
 ],
 "exercises": [
   "Implement single-leader replication with asynchronous followers.",
   "<b>Kill the leader mid-write</b> and report what the followers "
   "contain.",
   "Implement quorum reads and writes with configurable n, w, and r.",
   "<b>Demonstrate a non-monotonic read</b> under w + r &gt; n by "
   "contacting different replica subsets.",
   "<b>Demonstrate a partially-applied failed write</b> and explain why "
   "the caller cannot know.",
   "Run a linearizability checker (Porcupine or Knossos) over a history "
   "from your quorum store. Report the result.",
   "Implement read-your-writes with a version token and verify the "
   "anomaly is gone.",
   "Implement monotonic reads and verify the same.",
   "<b>Take an application you know and classify each operation</b> by the "
   "consistency it actually needs.",
   "<b>Measure the latency cost</b> of linearizable reads against local "
   "reads at several RTTs.",
 ],
 "selfcheck": [
   "Compare three replication strategies on failure behaviour.",
   "State the quorum condition and explain the overlap argument.",
   "Give three ways quorums are weaker than they look.",
   "Define linearizability, and distinguish it from serialisability.",
   "Order six consistency models by strength.",
   "Why is causal consistency significant?",
   "Name two session anomalies and the cheap fix for each.",
   "Why is consistency per operation rather than per system?",
   "Why does a game server not need a consistency model?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "The Impossibility Results",
 "subtitle": "What they actually say, and what they are quoted as "
             "saying.",
 "question": "What is provably impossible, and under what assumptions?",
 "outcomes": [
     "State CAP precisely and say what it does not claim.",
     "State FLP precisely and explain why consensus still works.",
     "Explain PACELC and why it is the more useful framing.",
     "Explain the two generals and the coordinated attack problem.",
     "Recognise these results being misused.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "CAP",
   "blurb": "The most misquoted theorem in computing."},

  {"t": "callout", "title": "CAP does not say 'pick two'",
   "kind": "What the theorem actually states",
   "body": ["<b>The claim is narrower: a system that is partitioned cannot "
            "be both consistent and available.</b> That is all.",
            "<b>'Consistent' means linearizable</b> (Module 04) — not "
            "'correct', not ACID, not any weaker model.",
            "<b>'Available' means every non-failing node answers every "
            "request</b> — which is far stronger than 'mostly up'.",
            "<b>And partitions are not optional.</b> You do not choose "
            "whether to tolerate them; the network chooses. <b>So the "
            "choice is only what to do <i>during</i> one</b>, and 'CA' is "
            "not a category you can select."]},

  {"t": "table", "kicker": "Misreadings", "title": "What people say, and what is true",
   "header": ["Claimed", "Actually"],
   "widths": [4.3, 7.8],
   "rows": [
     ["<b>'Pick two of three'</b>", "<b>P is not optional. You pick C or A during a partition</b>"],
     ["<b>'NoSQL is AP, SQL is CA'</b>", "<b>Both are configurable; most are neither purely</b>"],
     ["<b>'We chose availability'</b>", "Usually means 'we did not think about it'"],
     ["'CAP forbids strong consistency'", "<b>Only during a partition. Spanner is linearizable</b>"],
     ["<b>'Eventual consistency is required'</b>", "<b>Causal is stronger and also partition-available</b>"],
   ],
   "footnote": "<b>Brewer himself wrote '12 Years Later: How the Rules "
               "Have Changed'</b> largely to correct the folklore version.",
   "note": "That the author had to publish a correction is the most "
           "persuasive evidence here."},

  {"t": "section", "label": "Part 2", "title": "FLP",
   "blurb": "A deeper result, and a narrower one."},

  {"t": "callout", "title": "FLP: no deterministic consensus in an asynchronous system",
   "kind": "The statement",
   "body": ["<b>In a fully asynchronous system with even one possible "
            "crash failure, no deterministic algorithm guarantees "
            "consensus.</b>",
            "<b>'Asynchronous' means no bound on message delay or "
            "processing time</b> — so a slow node is indistinguishable "
            "from a dead one (Module 01 §1).",
            "<b>The proof constructs an infinite execution</b> in which "
            "the algorithm never decides. It does not say it decides "
            "wrongly — it says it may never decide.",
            "<b>So the impossibility is about <i>termination</i>, not "
            "safety.</b> That distinction is what leaves room for every "
            "practical algorithm."]},

  {"t": "callout", "title": "Why Raft and Paxos work anyway",
   "kind": "How the result is escaped",
   "body": ["<b>They never violate safety.</b> Two conflicting values are "
            "never decided, under any delays whatsoever. That part is "
            "unconditional.",
            "<b>They sacrifice guaranteed liveness.</b> Under "
            "pathological timing they can fail to make progress — which "
            "is exactly what FLP says must be possible.",
            "<b>And they add randomness.</b> Randomised election timeouts "
            "break symmetry, so progress occurs with probability 1 even "
            "though it is not guaranteed.",
            "<b>Real networks are partially synchronous</b> — usually "
            "timely, occasionally not. <b>Algorithms are designed to be "
            "safe always and live during the good periods</b>, which is the "
            "correct engineering response to an impossibility result."]},

  {"t": "section", "label": "Part 3", "title": "PACELC",
   "blurb": "The framing that is actually useful."},

  {"t": "eq", "kicker": "PACELC", "title": "The more complete statement",
   "eqs": [
     ("if Partition: choose Availability or Consistency",
      "This is CAP, and it is the rare case."),
     ("Else: choose Latency or Consistency",
      "This is the common case, and CAP says nothing about it."),
     ("Spanner: PC/EC.  Dynamo: PA/EL.  MongoDB: PA/EC (tunable).",
      "Two decisions, not one — and the second one is made every day."),
   ],
   "caption": "<b>The 'else' branch is where you live.</b> Partitions are "
              "rare; the latency–consistency trade is continuous.",
   "note": "PACELC is the better tool and is much less widely known."},

  {"t": "section", "label": "Part 4", "title": "Two generals",
   "blurb": "The oldest result, and the most directly useful."},

  {"t": "code", "kicker": "Two generals", "title": "Why no agreement is certain",
   "lang": "text", "code": """
  Two generals must attack simultaneously. They communicate by
  messengers who may be captured. Can they agree on a time?

      A sends "attack at dawn"
      -- but A does not know it arrived, so A cannot commit.
      B acknowledges
      -- but B does not know the ACK arrived, so B cannot commit.
      A acknowledges the acknowledgement
      -- but A does not know THAT arrived...

  NO FINITE PROTOCOL ACHIEVES CERTAINTY. The last message is
  always unacknowledged, and whoever sent it cannot know it
  landed. This is provable, and it holds for any number of
  messages.

  WHAT YOU DO INSTEAD:
    * accept at-least-once + idempotence (Module 01)
    * use a third party both trust (a transaction coordinator,
      or in a game, THE SERVER -- Module 11)
    * accept a probability of disagreement and bound it
    * restructure so agreement is not needed

  The last one is usually the best and is usually not tried.
""",
   "caption": "<b>This is Module 01's timeout ambiguity, proved.</b> It is "
              "the oldest result here and the one that bites most often.",
   "note": "Connecting it back to M01 closes the loop on the course's "
           "organising fact."},

  {"t": "callout", "title": "How to recognise these being misused",
   "kind": "The practical skill",
   "body": ["<b>'CAP means we cannot have transactions'</b> — no, it "
            "means not during a partition, and only for linearizability.",
            "<b>'FLP means consensus is impossible'</b> — no, it means "
            "guaranteed termination is impossible in a fully asynchronous "
            "model.",
            "<b>'We are AP so consistency is not our problem'</b> — "
            "availability during partitions says nothing about what you do "
            "the other 99.9% of the time.",
            "<b>Ask three questions: which consistency model, under what "
            "timing assumptions, and during a partition or otherwise?</b> "
            "<b>Most invocations of these theorems do not survive them.</b>"]},
 ],
 "takeaways": [
   "CAP says a partitioned system cannot be both linearizable and fully "
   "available; P is not optional, so 'pick two' is wrong.",
   "FLP says no deterministic algorithm guarantees consensus in a fully "
   "asynchronous system — the impossibility is about termination, not "
   "safety.",
   "Raft and Paxos are always safe, sacrifice guaranteed liveness, and use "
   "randomness to make progress with probability 1.",
   "PACELC adds the else-branch — latency versus consistency when "
   "there is no partition — which is the trade you make every day.",
   "Two generals proves no finite protocol gives certain agreement, because "
   "the last message is always unacknowledged.",
   "Ask which consistency model, under what timing assumptions, and during "
   "a partition or not — most invocations of these theorems fail those "
   "questions.",
 ],
 "notes": [
  ("h1", "1 &nbsp; CAP"),
  ("callout", "CAP does not say 'pick two'",
   ["<b>The theorem's actual claim is narrow: a system that is experiencing "
    "a network partition cannot be both consistent and available.</b> That "
    "is the whole statement.",
    "<b>'Consistent' means linearizable</b> (Module 04 &sect;2) — not "
    "'correct', not ACID, not any of the weaker models. A causally "
    "consistent system is not 'inconsistent' in CAP's sense of giving "
    "something up; it is simply not linearizable.",
    "<b>'Available' means every non-failing node returns a response to "
    "every request.</b> This is far stronger than the operational sense of "
    "'available' — a system with 99.99% uptime is not CAP-available if "
    "any node ever refuses a request.",
    "<b>And partitions are not optional.</b> You do not get to choose "
    "whether your network partitions; the network chooses, and it will. "
    "<b>So the only choice is what to do <i>during</i> one</b>, and 'CA' is "
    "not a selectable category — a system claiming it is simply one "
    "that has not decided what it does when the partition arrives, which "
    "means it will do something arbitrary."]),
  ("table", ["What is said", "What is true"],
   [["<b>'Pick two of the three.'</b>",
     "<b>P is not a choice. You pick C or A, and only during a "
     "partition.</b> The 'pick two' formulation is the single most "
     "damaging piece of folklore in this subject."],
    ["<b>'NoSQL is AP; SQL is CA.'</b>",
     "<b>Both are configurable, and most real systems are neither "
     "purely.</b> Cassandra can be configured for quorum reads and writes; "
     "PostgreSQL with synchronous replication makes a CP-ish choice."],
    ["<b>'We chose availability.'</b>",
     "Frequently means 'we did not think about it and the default was "
     "eventual consistency'."],
    ["<b>'CAP forbids strong consistency at scale.'</b>",
     "<b>Only during a partition.</b> Spanner is linearizable across "
     "continents and simply becomes unavailable in the minority partition, "
     "which is a deliberate and documented choice."],
    ["<b>'So we must use eventual consistency.'</b>",
     "<b>Causal consistency is strictly stronger and is also available "
     "under partition</b> (Module 04 &sect;2). Eventual is not the only "
     "partition-tolerant option and is rarely the best one."]],
   [0.33, 0.67]),
  ("p", "<b>Brewer published 'CAP Twelve Years Later: How the Rules Have "
        "Changed' largely to correct the folklore version of his own "
        "conjecture</b>, which is about as strong a signal as one can get "
        "that the popular reading is wrong."),

  ("h1", "2 &nbsp; FLP"),
  ("callout", "No deterministic consensus in an asynchronous system",
   ["<b>Fischer, Lynch and Paterson proved that in a fully asynchronous "
    "system with even one possible crash failure, no deterministic "
    "algorithm guarantees consensus.</b>",
    "<b>'Asynchronous' is doing heavy lifting:</b> it means no bound "
    "whatsoever on message delay or on processing speed. In that model <b>a "
    "slow node is formally indistinguishable from a dead one</b> — "
    "which is Module 01 &sect;1's timeout ambiguity elevated into a "
    "theorem.",
    "<b>The proof constructs an infinite execution in which the algorithm "
    "never decides</b>, by repeatedly delaying whichever message would "
    "resolve the ambiguity. <b>It does not show the algorithm decides "
    "wrongly</b> — it shows it may never decide at all.",
    "<b>So the impossibility is about <i>termination</i>, not safety.</b> "
    "<b>That distinction is the entire reason practical consensus exists</b>, "
    "and it is the part the folklore version ('consensus is impossible') "
    "drops."]),
  ("callout", "Why Raft and Paxos work anyway",
   ["<b>They never violate safety.</b> Two conflicting values are never "
    "decided, under any pattern of delays, losses, and crashes whatsoever. "
    "That guarantee is unconditional and is what you actually need.",
    "<b>They sacrifice guaranteed liveness.</b> Under sufficiently "
    "adversarial timing — an election that repeatedly splits, messages "
    "delayed exactly enough to trigger timeouts — they can fail to "
    "make progress indefinitely. <b>Which is precisely what FLP says must "
    "be possible.</b>",
    "<b>And they add randomness.</b> Raft's randomised election timeouts "
    "break the symmetry that the FLP adversary depends on, so progress "
    "occurs with probability 1 even though it is not guaranteed in the "
    "worst case. <b>Randomisation does not contradict FLP</b>, which is a "
    "statement about deterministic algorithms.",
    "<b>And real networks are <i>partially</i> synchronous</b> — "
    "usually timely, occasionally not, with no bound you can state in "
    "advance but with long periods of good behaviour. <b>So the algorithms "
    "are designed to be safe always and live during the good periods</b>, "
    "which is exactly the right engineering response to an impossibility "
    "result: <b>find the assumption that makes it bite, and note that "
    "reality mostly does not satisfy it.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; PACELC"),
  ("eq", "if (P) then (A or C) else (L or C)"),
  ("p", "<b>If there is a Partition, choose Availability or Consistency</b> "
        "— that is CAP, and it covers the rare case. "
        "<b>Else, choose Latency or Consistency</b> — and that is the "
        "common case, about which CAP says nothing at all. Spanner is "
        "PC/EC: it gives up availability under partition and gives up "
        "latency otherwise (the commit wait of Module 03). Dynamo is "
        "PA/EL: available under partition, and fast rather than consistent "
        "the rest of the time. <b>Two decisions, not one — and the "
        "second is made on every single request</b>, while the first "
        "applies during incidents measured in minutes per year. <b>PACELC "
        "is the more useful framing and is far less widely known</b>, which "
        "is a reasonable thing to fix in your own team's vocabulary."),

  ("h1", "4 &nbsp; Two generals"),
  ("code", """Two generals must attack simultaneously. Messengers may be
captured. Can they agree on a time?

    A sends "attack at dawn"
       -- A does not know it arrived, so A cannot commit.
    B acknowledges
       -- B does not know the ACK arrived, so B cannot commit.
    A acknowledges the acknowledgement
       -- A does not know THAT arrived...

NO FINITE PROTOCOL ACHIEVES CERTAINTY. The last message sent is
always unacknowledged, and its sender cannot know it landed.
Provable, for any number of messages.

WHAT YOU DO INSTEAD:
  * at-least-once delivery + idempotence       (Module 01)
  * a third party both sides trust -- a coordinator, or in
    a game, THE SERVER                         (Module 11)
  * accept a bounded probability of disagreement
  * RESTRUCTURE so agreement is not required   <- usually best,
                                                  usually untried"""),
  ("p", "<b>This is Module 01's timeout ambiguity, proved rather than "
        "observed.</b> It is the oldest result in this module and the one "
        "that bites most often in ordinary engineering — every time "
        "two services must both do something or neither, every distributed "
        "transaction, every 'did the payment go through' question. <b>And "
        "the fourth response is usually the right one</b>: a design in "
        "which one side can proceed unilaterally and the other reconciles "
        "afterwards avoids the problem rather than paying for it."),
  ("callout", "How to recognise these being misused",
   ["<b>'CAP means we cannot have transactions.'</b> No — it means not "
    "during a partition, and only for linearizability. Transactions within "
    "a partition, or serialisable transactions that are not linearizable, "
    "are unaffected.",
    "<b>'FLP means consensus is impossible.'</b> No — it means "
    "guaranteed termination is impossible for a deterministic algorithm in "
    "a fully asynchronous model. Raft is running in production on a great "
    "many systems.",
    "<b>'We're AP, so consistency isn't our problem.'</b> No — "
    "availability during partitions says nothing whatsoever about what "
    "happens the other 99.9% of the time, which is the PACELC else-branch "
    "and is where your users actually live.",
    "<b>Ask three questions of any invocation of these results: which "
    "consistency model is meant, under what timing assumptions, and during "
    "a partition or outside one?</b> <b>Most invocations do not survive "
    "those questions</b> — and being able to ask them calmly is the "
    "practical skill this module is for."]),
 ],
 "resources": [
   ("Gilbert & Lynch &mdash; Brewer's Conjecture and the Feasibility of "
    "Consistent, Available, Partition-Tolerant Web Services (free)",
    "https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf",
    "<b>The actual proof</b>, with the actual definitions. Read the "
    "definitions section at minimum."),
   ("Brewer &mdash; CAP Twelve Years Later: How the Rules Have Changed "
    "(free)",
    "https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/",
    "<b>The author correcting the folklore</b>, which is the most "
    "persuasive item in &sect;1."),
   ("Fischer, Lynch & Paterson &mdash; Impossibility of Distributed "
    "Consensus with One Faulty Process (free)",
    "https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf",
    "FLP itself. Short, and the proof idea is followable."),
   ("Abadi &mdash; Consistency Tradeoffs in Modern Distributed Database "
    "System Design (PACELC) (free)",
    "https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf",
    "<b>The &sect;3 framing</b>, with real systems classified."),
 ],
 "exercises": [
   "<b>State CAP precisely</b> in your own words, with both definitions, "
   "and then state three things it does not say.",
   "Find a vendor's marketing page invoking CAP and assess whether it uses "
   "the terms correctly.",
   "<b>Partition a three-node cluster</b> and observe what the minority "
   "side does. Classify the system.",
   "Reconfigure it for the other choice and observe again.",
   "<b>Construct the FLP scenario informally:</b> delay messages so a "
   "leader election repeatedly splits. How long can you prevent progress?",
   "Add randomised timeouts and measure how that changes.",
   "<b>Classify five systems you use by PACELC.</b>",
   "Implement the two generals exchange and <b>instrument it to show that "
   "the final message is always unacknowledged</b>.",
   "Take a two-service agreement problem from your own work and "
   "<b>restructure it so agreement is not required</b>.",
   "Write one paragraph explaining to a colleague why 'we chose AP' is "
   "not a complete answer.",
 ],
 "selfcheck": [
   "State CAP precisely, including what C and A mean.",
   "Why is P not a choice?",
   "Give five common misreadings of CAP.",
   "State FLP and say what kind of impossibility it is.",
   "How do Raft and Paxos escape it?",
   "State PACELC and say why the else-branch matters more.",
   "Explain the two generals problem and four responses to it.",
   "What three questions should you ask when someone cites these "
   "results?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Consensus",
 "subtitle": "Getting a group of machines to agree on one thing.",
 "question": "How do several machines agree, despite failures?",
 "outcomes": [
     "Explain the replicated state machine approach.",
     "Explain Raft leader election and log replication.",
     "State the safety properties and why each is needed.",
     "Explain quorum intersection as the underlying mechanism.",
     "Explain membership change and the split-brain hazard.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The reduction",
   "blurb": "Agree on a log, and everything else follows."},

  {"t": "callout", "title": "Replicated state machines: agree on the log, not the state",
   "kind": "The idea that makes consensus useful",
   "body": ["<b>If every replica starts in the same state and applies the "
            "same deterministic operations in the same order, they end in "
            "the same state.</b>",
            "<b>So replicating a service reduces to agreeing on an ordered "
            "log of operations</b> — which is one problem instead of a "
            "different one per service.",
            "<b>Determinism is required and is easy to lose:</b> a map "
            "iteration order, a wall-clock read, a random number, or a "
            "floating-point difference (CSCE 735 M13) all break it.",
            "<b>This is also how lockstep netcode works</b> "
            "(Module 09) — same inputs, same simulation, same result. "
            "<b>The same idea in two very different settings.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Raft",
   "blurb": "Leader election and log replication."},

  {"t": "code", "kicker": "Raft", "title": "The algorithm, in outline",
   "lang": "text", "code": """
  THREE ROLES: follower, candidate, leader. One leader per TERM.
  A term is a logical clock -- an integer that only increases.

  ELECTION
      a follower hearing nothing for its randomised timeout
      becomes a CANDIDATE, increments the term, votes for
      itself, and requests votes
          -> a node grants at most ONE vote per term
          -> a majority of votes makes it leader
          -> RANDOMISED timeouts make split votes rare

  REPLICATION
      clients send commands to the leader
      the leader appends to its log and sends AppendEntries
      when a MAJORITY have stored the entry, it is COMMITTED
      committed entries are applied to the state machine

  THE CRITICAL RULE -- ELECTION RESTRICTION
      a node votes for a candidate only if the candidate's log
      is AT LEAST AS UP TO DATE as its own.
      So any node that can win an election already holds every
      committed entry -- because a committed entry is on a
      majority, and any two majorities intersect.
""",
   "caption": "<b>Quorum intersection is the whole safety argument.</b> "
              "Everything else is mechanism.",
   "note": "If they take one thing: two majorities must share a member."},

  {"t": "callout", "title": "Quorum intersection is why any of this works",
   "kind": "The one-line argument",
   "body": ["<b>Any two majorities of the same set must share at least one "
            "member.</b> Three out of five and three out of five overlap in "
            "at least one node.",
            "<b>So a committed entry — stored on a majority — is held "
            "by at least one member of any future election's majority.</b>",
            "<b>Combined with the election restriction, a new leader "
            "therefore cannot be missing a committed entry.</b>",
            "<b>That is the entire safety proof in three sentences</b>, and "
            "it is the same argument underneath Paxos, quorum reads "
            "(Module 04), and every majority-based protocol. <b>Learn it "
            "once.</b>"]},

  {"t": "table", "kicker": "Safety", "title": "Raft's safety properties",
   "header": ["Property", "Statement"],
   "widths": [3.4, 8.7],
   "rows": [
     ["<b>Election safety</b>", "<b>At most one leader per term</b>"],
     ["<b>Leader append-only</b>", "A leader never overwrites its own entries"],
     ["<b>Log matching</b>", "<b>Same index and term ⇒ identical logs up to there</b>"],
     ["<b>Leader completeness</b>", "<b>A committed entry is in every future leader's log</b>"],
     ["State machine safety", "<b>No two nodes apply different commands at one index</b>"],
   ],
   "footnote": "<b>Leader completeness is the one the election "
               "restriction exists to establish</b>, and the others "
               "support it.",
   "note": "Worth noting these are what a test suite should assert."},

  {"t": "section", "label": "Part 3", "title": "What goes wrong",
   "blurb": "The failure modes to design against."},

  {"t": "callout", "title": "Split brain, and fencing",
   "kind": "The hazard that causes real outages",
   "body": ["<b>A partitioned leader may not know it has lost "
            "leadership</b> and may keep serving reads and accepting "
            "writes.",
            "<b>Majority writes stop automatically</b> — it cannot reach "
            "a quorum — but <b>local reads and any external side effects "
            "do not</b>.",
            "<b>So a lease, a GC pause, or a VM pause</b> (Module 03 §1) "
            "<b>can leave a stale leader acting with authority it lost "
            "minutes ago.</b>",
            "<b>Fencing tokens are the fix:</b> every operation carries a "
            "monotonically increasing token, and the resource rejects "
            "anything older than the highest it has seen. <b>The resource "
            "enforces it, not the client.</b>"]},

  {"t": "callout", "title": "Membership change is where implementations break",
   "kind": "The underestimated part",
   "body": ["<b>Changing the cluster from three nodes to five cannot be "
            "done atomically</b>, so for a moment different nodes disagree "
            "about who the members are.",
            "<b>If the old and new majorities do not intersect, two "
            "leaders can be elected simultaneously</b> — the safety "
            "argument's premise has been removed.",
            "<b>Raft's joint consensus</b> uses a transitional "
            "configuration requiring majorities of <i>both</i> old and new "
            "sets.",
            "<b>Single-server changes</b> — add or remove one at a time "
            "— are simpler and are what most implementations do. "
            "<b>Membership change is the most commonly broken part of real "
            "Raft implementations</b>, and it is where to focus testing."]},

  {"t": "section", "label": "Part 4", "title": "Using it",
   "blurb": "What consensus is for, and what it is not for."},

  {"t": "bullets", "kicker": "Uses", "title": "What consensus actually gets used for",
   "items": [
     "<b>Leader election</b> for some other system — the most common "
     "use by far.",
     "",
     "<b>Configuration and metadata</b>, where the data is small and "
     "correctness matters absolutely.",
     "",
     "<b>Distributed locks and leases</b> — with fencing tokens, per "
     "Part 3.",
     "",
     "<b>Replicated logs</b>, which are then the input to everything "
     "else.",
     "",
     "<b>Not for bulk data.</b> Every write costs a round trip to a "
     "majority, so throughput is bounded by the slowest quorum member.",
   ],
   "footnote": "<b>Use etcd, ZooKeeper, or Consul</b> rather than writing "
               "your own — and implement Raft once anyway, to "
               "understand what they promise."},

  {"t": "callout", "title": "Why consensus is wrong for a game",
   "kind": "The connection to Modules 09–11",
   "body": ["<b>Consensus costs at least one round trip to a majority</b> "
            "before anything is decided.",
            "<b>At 60 Hz the budget is 16.7 ms, and a round trip is "
            "50 to 150.</b> The arithmetic does not work.",
            "<b>So games do not reach agreement before acting.</b> The "
            "client predicts immediately and is corrected later "
            "(Module 10), and the server decides unilaterally.",
            "<b>That is a weaker guarantee bought for a hard deadline</b> "
            "— and it is the right trade, because an authoritative answer "
            "that arrives after the frame is worth nothing."]},
 ],
 "takeaways": [
   "Replicating a service reduces to agreeing on an ordered log, provided "
   "the operations are deterministic — which is easy to lose.",
   "Raft elects at most one leader per term using randomised timeouts, and "
   "commits an entry once a majority has stored it.",
   "The election restriction plus quorum intersection is the entire safety "
   "argument: any two majorities share a member.",
   "A partitioned leader cannot commit writes but can still serve stale "
   "reads and cause side effects — fencing tokens enforced at the "
   "resource are the fix.",
   "Membership change is the most commonly broken part of real Raft "
   "implementations, because the old and new majorities may not intersect.",
   "Consensus costs a round trip to a majority, which is why it is wrong "
   "for bulk data and wrong for a 16.7 ms frame budget.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Replicated state machines"),
  ("callout", "Agree on the log, not on the state",
   ["<b>If every replica starts from the same initial state and applies the "
    "same deterministic operations in the same order, they necessarily "
    "arrive at the same state.</b> The states are then equal without ever "
    "having been compared.",
    "<b>So replicating an arbitrary service reduces to agreeing on an "
    "ordered log of operations</b> — one problem, solved once, rather "
    "than a bespoke replication scheme per service. This reduction is why "
    "consensus is a foundational building block rather than a curiosity.",
    "<b>Determinism is required, and it is easy to lose accidentally.</b> "
    "Iterating a hash map in an unspecified order, reading the wall clock, "
    "drawing a random number, depending on pointer values, or "
    "floating-point summation order (CSCE 735 Module 13 &sect;2) will all "
    "silently desynchronise replicas — and the divergence may not "
    "surface for hours.",
    "<b>This is also exactly how lockstep netcode works</b> (Module 09 "
    "&sect;3): every client runs the identical simulation on the identical "
    "inputs and therefore computes the identical world, with only the "
    "inputs transmitted. <b>The same idea in two very different "
    "settings</b>, with the same determinism hazard and the same "
    "consequence when it fails."]),

  ("h1", "2 &nbsp; Raft"),
  ("code", """THREE ROLES: follower, candidate, leader.  One leader per TERM;
a term is a logical clock -- an integer that only increases.

ELECTION
    a follower hearing nothing for its RANDOMISED timeout
    becomes a candidate, increments the term, votes for itself,
    and requests votes
      -> each node grants at most ONE vote per term
      -> a majority of votes makes it leader
      -> randomised timeouts make split votes rare

REPLICATION
    clients send commands to the leader
    leader appends to its log, sends AppendEntries
    once a MAJORITY have stored it, the entry is COMMITTED
    committed entries are applied to the state machine

ELECTION RESTRICTION -- the critical rule
    a node votes for a candidate only if the candidate's log is
    AT LEAST AS UP TO DATE as its own."""),
  ("callout", "Quorum intersection is why any of this works",
   ["<b>Any two majorities of the same set must share at least one "
    "member.</b> Three out of five and three out of five cannot be "
    "disjoint; there are only five.",
    "<b>So a committed entry — which by definition is stored on a "
    "majority — is held by at least one member of any future "
    "election's voting majority.</b>",
    "<b>Combined with the election restriction, a new leader therefore "
    "cannot be missing a committed entry.</b> The member holding it would "
    "refuse to vote for a candidate whose log was behind, so no such "
    "candidate can assemble a majority.",
    "<b>That is the entire safety proof, in three sentences.</b> It is the "
    "same argument underneath Paxos, underneath quorum reads and writes "
    "(Module 04 &sect;1), and underneath every majority-based protocol in "
    "the subject. <b>Learn it once and it explains all of them</b> — "
    "and conversely, whenever a protocol uses majorities, look for where "
    "the intersection argument is being made."]),
  ("table", ["Property", "Statement"],
   [["<b>Election safety</b>", "<b>At most one leader is elected in any "
     "given term.</b> Follows from one-vote-per-term plus majority."],
    ["<b>Leader append-only</b>",
     "A leader never overwrites or deletes entries in its own log; it only "
     "appends."],
    ["<b>Log matching</b>",
     "<b>If two logs contain an entry with the same index and term, the "
     "logs are identical in all preceding entries.</b> Maintained by the "
     "consistency check in AppendEntries."],
    ["<b>Leader completeness</b>",
     "<b>If an entry is committed in a term, it is present in the logs of "
     "all leaders of higher terms.</b> <b>This is the one the election "
     "restriction exists to establish</b>, via quorum intersection."],
    ["<b>State machine safety</b>",
     "<b>If a node applies an entry at a given index, no other node ever "
     "applies a different entry at that index.</b> The property that "
     "actually matters to the application, and it follows from the "
     "others."]],
   [0.26, 0.74]),

  ("break",),
  ("h1", "3 &nbsp; What goes wrong"),
  ("callout", "Split brain, and fencing tokens",
   ["<b>A leader that becomes partitioned may not immediately know it has "
    "lost leadership.</b> It stops hearing from followers, but the absence "
    "of messages is exactly Module 01's ambiguity — it cannot "
    "distinguish 'everyone else is gone' from 'I am cut off'.",
    "<b>Majority writes stop automatically</b>, since it cannot reach a "
    "quorum to commit anything. <b>But local reads continue, and any "
    "external side effect continues</b> — writing to shared storage, "
    "sending an email, charging a card, moving a robot.",
    "<b>And a process pause makes it worse.</b> A long GC pause "
    "(CSCE 605 Module 12) or a VM migration (Module 03 &sect;1) can leave a "
    "node that believes it holds a lease <b>resuming minutes after the "
    "lease expired and acting with authority it lost long ago.</b> This has "
    "caused real data corruption in real systems.",
    "<b>Fencing tokens are the fix.</b> Every operation carries a "
    "monotonically increasing token obtained with the lease, and <b>the "
    "resource itself rejects any operation bearing a token lower than the "
    "highest it has already seen</b>. <b>The enforcement must be at the "
    "resource, not in the client</b> — a client that is paused cannot "
    "check anything, and a client that is confused cannot be trusted to "
    "check correctly."]),
  ("callout", "Membership change is where implementations break",
   ["<b>Changing the cluster from three nodes to five cannot be done "
    "atomically across all of them</b>, so there is necessarily an interval "
    "during which different nodes disagree about who the members are.",
    "<b>If the old majority and the new majority do not intersect, two "
    "leaders can be elected simultaneously</b> — one by a majority of "
    "the old configuration and one by a majority of the new. <b>The "
    "premise of the entire safety argument has been removed</b>, and both "
    "leaders believe themselves legitimate.",
    "<b>Raft's joint consensus</b> introduces a transitional configuration "
    "in which a decision requires separate majorities of <i>both</i> the "
    "old and the new sets, which restores intersection throughout the "
    "change at the cost of real complexity.",
    "<b>Single-server changes</b> — adding or removing exactly one "
    "node at a time — guarantee intersection automatically and are "
    "much simpler, which is what most implementations do. <b>Membership "
    "change is the most commonly broken part of real Raft "
    "implementations</b>, it is under-tested because it is rare in normal "
    "operation, and it is therefore exactly where a fault injector should "
    "be pointed."]),

  ("h1", "4 &nbsp; Using consensus"),
  ("ul", ["<b>Leader election for some other system.</b> By a wide margin "
          "the most common use: a consensus cluster decides which node of a "
          "separate, larger system is in charge.",
          "<b>Configuration and metadata.</b> Small data where correctness "
          "matters absolutely and throughput does not — which service "
          "is where, what the schema version is, which shard belongs to "
          "whom.",
          "<b>Distributed locks and leases</b>, with fencing tokens "
          "(&sect;3). <b>A distributed lock without a fencing token is not "
          "safe</b>, regardless of how good the consensus underneath it is.",
          "<b>Replicated logs</b>, which then serve as the input to "
          "everything else — the log-as-source-of-truth pattern that "
          "Kafka and event sourcing are built on.",
          "<b>Not for bulk data.</b> Every write costs a round trip to a "
          "majority, so throughput is bounded by the slowest member of the "
          "fastest majority, and the data is stored on every node. "
          "<b>Consensus coordinates systems; it does not store their "
          "data.</b>",
          "<b>And use etcd, ZooKeeper, or Consul rather than writing your "
          "own</b> — while implementing Raft once anyway, because you "
          "cannot reason about what those systems promise without knowing "
          "how they promise it."]),
  ("callout", "Why consensus is wrong for a game",
   ["<b>Consensus costs at least one round trip to a majority before "
    "anything is decided.</b> That is intrinsic — it is what the "
    "quorum intersection argument requires.",
    "<b>At 60 Hz the frame budget is 16.7 ms, and a round trip to a "
    "geographically distributed majority is 50 to 150 ms.</b> The "
    "arithmetic simply does not work, and no implementation quality fixes "
    "it.",
    "<b>So games do not reach agreement before acting.</b> The client "
    "predicts the outcome immediately and is corrected afterwards "
    "(Module 10), and the server decides unilaterally rather than seeking "
    "consensus with anyone.",
    "<b>That is a strictly weaker guarantee, bought in exchange for "
    "meeting a hard deadline</b> — and it is the right trade, because "
    "<b>an authoritative answer that arrives after the frame has been drawn "
    "is worth nothing at all</b>. This is the same shape of argument as "
    "CSCE 650's on latency and CSCE 605's on GC pauses: <b>for an "
    "interactive system, a worse answer on time beats a better answer "
    "late.</b>"]),
 ],
 "resources": [
   ("Ongaro & Ousterhout &mdash; In Search of an Understandable Consensus "
    "Algorithm (free)",
    "https://raft.github.io/raft.pdf",
    "<b>The Raft paper.</b> Deliberately written to be implementable, and "
    "the interactive visualisation on the same site is excellent."),
   ("MIT 6.5840 &mdash; the Raft labs (free)",
    "https://pdos.csail.mit.edu/6.824/",
    "<b>The best way to learn this is to implement it</b>, and these labs "
    "have a test suite that finds the bugs you will have."),
   ("Lamport &mdash; Paxos Made Simple (free)",
    "https://lamport.azurewebsites.net/pubs/paxos-simple.pdf",
    "The other algorithm, from its author. Worth reading after Raft for "
    "the contrast in exposition."),
   ("Kleppmann &mdash; How to do distributed locking (free)",
    "https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html",
    "<b>The fencing token argument of &sect;3</b>, with the process-pause "
    "scenario worked through."),
 ],
 "exercises": [
   "Implement Raft leader election with randomised timeouts.",
   "<b>Kill leaders repeatedly</b> and measure election latency as a "
   "distribution.",
   "Implement log replication and the commit rule.",
   "<b>Implement the election restriction</b>, then remove it and "
   "construct a history where a committed entry is lost.",
   "Add persistence and verify a restarted node does not violate safety.",
   "<b>Build a fault injector</b>: drop, delay, reorder, partition, crash, "
   "restart.",
   "Run a linearizability checker over thousands of randomised histories "
   "with faults injected.",
   "<b>Produce a split-brain scenario</b> with a paused leader, and then "
   "defeat it with fencing tokens.",
   "Implement single-server membership change and test it under fault "
   "injection.",
   "<b>Measure write throughput against cluster size</b> from 3 to 9 nodes "
   "and explain the curve.",
 ],
 "selfcheck": [
   "What does the replicated state machine approach reduce consensus to, "
   "and what does it require?",
   "Name four ways determinism is accidentally lost.",
   "Describe Raft election and the role of randomised timeouts.",
   "State the election restriction and the quorum intersection argument.",
   "Name Raft's five safety properties.",
   "What is split brain, and why do fencing tokens have to be enforced at "
   "the resource?",
   "Why is membership change dangerous, and what are the two approaches?",
   "Name five uses of consensus and one non-use.",
   "Why is consensus wrong for a 60 Hz game?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Failure Detection and Membership",
 "subtitle": "Deciding who is alive, when you cannot know.",
 "question": "How do you tell a dead node from a slow one?",
 "outcomes": [
     "Explain why perfect failure detection is impossible.",
     "Compare heartbeat and phi accrual detectors.",
     "Explain gossip and SWIM and their scaling properties.",
     "Explain why timeouts must be tuned against tail latency.",
     "Design membership that tolerates false positives.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The impossibility",
   "blurb": "You cannot tell, and you must decide anyway."},

  {"t": "callout", "title": "You cannot distinguish dead from slow",
   "kind": "Module 01, restated as a design constraint",
   "body": ["<b>A node that has not responded might be crashed, "
            "overloaded, paused, or unreachable.</b> No observation "
            "separates these (Module 01 §1).",
            "<b>So a failure detector is necessarily a guess</b>, and it "
            "will be wrong in both directions.",
            "<b>A false positive declares a live node dead</b> — which "
            "triggers a needless failover, and the 'dead' node is still "
            "running and may still act.",
            "<b>A false negative keeps a dead node in the cluster</b> "
            "— requests to it hang, and recovery is delayed. <b>You tune "
            "the trade; you do not escape it.</b>"]},

  {"t": "callout", "title": "A timeout is a bet about the tail",
   "kind": "How to choose one",
   "body": ["<b>Too short and you declare healthy nodes dead</b> whenever "
            "latency spikes — which it does, routinely.",
            "<b>Too long and real failures go undetected</b>, so requests "
            "pile up against a corpse.",
            "<b>So set it from the measured latency distribution</b>, not "
            "from a round number. The p99.9, with margin, is the usual "
            "starting point.",
            "<b>And remember GC pauses</b> (CSCE 605 M12): a 200 ms "
            "heartbeat timeout on a service with 500 ms pauses declares "
            "failures that are not failures. <b>The two numbers must be "
            "chosen together.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Detectors",
   "blurb": "Better than a fixed threshold."},

  {"t": "callout", "title": "Phi accrual: a suspicion level, not a boolean",
   "kind": "The better detector",
   "body": ["<b>Record the distribution of heartbeat inter-arrival times "
            "and fit it.</b> Then compute how surprising the current "
            "silence is.",
            "<b>Output φ = −log₁₀(probability of this "
            "delay or longer)</b> — a continuous suspicion level rather "
            "than alive or dead.",
            "<b>So different consumers can use different thresholds</b> "
            "— a cheap action at φ = 1, an expensive failover at "
            "φ = 8.",
            "<b>And it adapts automatically.</b> A link that is normally "
            "slow raises the bar; one that is normally fast lowers it. "
            "<b>Cassandra and Akka use this, and it is strictly better than "
            "a fixed timeout.</b>"]},

  {"t": "table", "kicker": "Detectors", "title": "The options",
   "header": ["Approach", "How", "Scaling"],
   "widths": [2.8, 4.3, 5.0],
   "rows": [
     ["<b>Central heartbeat</b>", "All report to one monitor", "<b>O(n); the monitor is a SPOF</b>"],
     ["<b>All-to-all</b>", "Everyone pings everyone", "<b>O(n&#178;). Dies past ~100 nodes</b>"],
     ["<b>Gossip</b>", "<b>Random peers exchange membership</b>", "<b>O(log n) rounds to spread</b>"],
     ["<b>SWIM</b>", "<b>Random probe + indirect probe via k peers</b>", "<b>O(1) per node per round</b>"],
     ["Ring / neighbour", "Each watches its successors", "O(1); slow to detect regions"],
     ["<b>Lease-based</b>", "<b>Hold a lease or lose authority</b>", "<b>Self-expiring. Pairs with fencing</b>"],
   ],
   "footnote": "<b>SWIM's indirect probe is the key idea:</b> before "
               "declaring a node dead, ask k others to try — which "
               "distinguishes 'unreachable from me' from 'dead'.",
   "note": "The indirect probe directly attacks the false-positive "
           "problem."},

  {"t": "section", "label": "Part 3", "title": "Gossip",
   "blurb": "Spreading information without coordination."},

  {"t": "code", "kicker": "Gossip", "title": "The protocol, and why it works",
   "lang": "text", "code": """
  Every T milliseconds, each node:
      picks a RANDOM peer
      exchanges its membership table with that peer
      merges: for each node, keep the entry with the higher
              version / incarnation number

  PROPERTIES:
    * information reaches all n nodes in O(log n) rounds
    * each node sends O(1) messages per round -- constant,
      regardless of cluster size
    * no coordinator, no single point of failure
    * robust to message loss: the next round retries implicitly
    * eventually consistent membership, by construction

  THE COST:
    * eventual, not immediate -- there is a propagation delay
    * O(n) state at every node (the full membership table)
    * conflicting information must be ordered, which needs
      version or incarnation numbers (Module 03)

  A node declared dead can REFUTE it by broadcasting a higher
  incarnation number. This is how SWIM handles false positives
  without a central arbiter.
""",
   "caption": "<b>The refutation mechanism is what makes false positives "
              "survivable</b> — a wrongly-accused node can simply say "
              "so.",
   "note": "Refutation is the detail that makes gossip membership "
           "practical."},

  {"t": "section", "label": "Part 4", "title": "Designing for false positives",
   "blurb": "Because they will happen."},

  {"t": "bullets", "kicker": "Design", "title": "How to tolerate being wrong",
   "items": [
     "<b>Make failover idempotent and reversible.</b> A node declared "
     "dead that returns must rejoin cleanly.",
     "",
     "<b>Fence every side effect</b> (Module 06 §3) — so a "
     "wrongly-evicted node cannot corrupt anything when it resumes.",
     "",
     "<b>Use suspicion, not a binary</b> — act proportionally to "
     "confidence.",
     "",
     "<b>Require a quorum to agree a node is dead</b>, rather than "
     "trusting one observer.",
     "",
     "<b>And rate-limit failover.</b> <b>A detector that flaps causes more "
     "damage than the failures it detects</b> — repeated failover is an "
     "outage.",
   ],
   "footnote": "<b>Flapping is the real danger.</b> Most failure-detection "
               "incidents are the detector overreacting, not the detector "
               "missing something."},

  {"t": "callout", "title": "In a game, disconnection is a product decision",
   "kind": "The netcode connection",
   "body": ["<b>A client that stops sending might have crashed, lost "
            "connection, rage-quit, or be exploiting the ambiguity to avoid "
            "a loss.</b>",
            "<b>The server cannot tell</b> — and unlike an internal "
            "cluster, it has no quorum of peers to consult.",
            "<b>So the policy is a design question:</b> freeze the "
            "character, let an AI take over, or remove it — and how long "
            "to wait before each.",
            "<b>Every choice is exploitable.</b> Freezing lets players "
            "escape damage by pulling the cable; immediate removal punishes "
            "genuine connection loss. <b>There is no correct answer, only a "
            "stated one.</b>"]},
 ],
 "takeaways": [
   "No observation distinguishes a dead node from a slow one, so a failure "
   "detector is a tunable guess that is wrong in both directions.",
   "A timeout is a bet about the latency tail, and it must be chosen "
   "against the measured distribution and the GC pause time together.",
   "Phi accrual outputs a continuous suspicion level instead of a boolean, "
   "adapts to the link, and lets different consumers use different "
   "thresholds.",
   "SWIM's indirect probe asks k other nodes to try before declaring death, "
   "which separates 'unreachable from me' from 'dead'.",
   "Gossip spreads in O(log n) rounds with O(1) messages per node, and "
   "incarnation numbers let a wrongly-accused node refute.",
   "Flapping detectors cause more damage than the failures they detect, so "
   "rate-limit failover and make it reversible.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The impossibility"),
  ("callout", "You cannot distinguish dead from slow",
   ["<b>A node that has not responded might be crashed, overloaded, paused "
    "by its garbage collector or hypervisor, or perfectly healthy but "
    "unreachable from you.</b> <b>No observation separates these cases</b> "
    "— it is Module 01 &sect;1's ambiguity, now as a design "
    "constraint rather than a curiosity.",
    "<b>So a failure detector is necessarily a guess</b>, and it will be "
    "wrong in both directions. The design question is not how to be right "
    "but how to be wrong safely.",
    "<b>A false positive declares a live node dead.</b> This triggers an "
    "unnecessary failover — and, worse, <b>the 'dead' node is still "
    "running and may still be acting</b>, which is the split-brain hazard "
    "of Module 06 &sect;3.",
    "<b>A false negative keeps a dead node in the cluster.</b> Requests "
    "routed to it hang until their own timeouts expire, and recovery is "
    "delayed by exactly that much. <b>You tune the trade between these; "
    "you do not escape it.</b>"]),
  ("callout", "A timeout is a bet about the latency tail",
   ["<b>Too short, and you declare healthy nodes dead</b> every time "
    "latency spikes — which it does routinely, from GC, from a "
    "scheduler decision, from a noisy neighbour, from a transient network "
    "event.",
    "<b>Too long, and real failures go undetected</b>, so requests pile up "
    "against a node that is not coming back and the system's recovery time "
    "is dominated by the detection delay.",
    "<b>So derive it from the measured latency distribution rather than "
    "picking a round number.</b> The p99.9 with a margin is a reasonable "
    "starting point, and the right value changes when the workload does "
    "— which means it should be re-derived, not set once.",
    "<b>And remember process pauses.</b> <b>A 200 ms heartbeat timeout on "
    "a service with 500 ms garbage collection pauses declares failures that "
    "are not failures</b> (CSCE 605 Module 12), repeatedly and under load, "
    "which is when you can least afford it. <b>The timeout and the "
    "collector's pause target must be chosen together</b>, and this "
    "coupling is routinely missed because the two are configured by "
    "different people."]),

  ("h1", "2 &nbsp; Detectors"),
  ("callout", "Phi accrual: a suspicion level rather than a boolean",
   ["<b>Record the distribution of heartbeat inter-arrival times and fit a "
    "model to it</b> — typically normal or exponential. Then, given "
    "the time since the last heartbeat, compute how surprising that silence "
    "is under the fitted model.",
    "<b>The output is &phi; = &minus;log<sub>10</sub>(probability of a "
    "delay at least this long)</b>. A &phi; of 1 means roughly a 10% "
    "chance this is normal; a &phi; of 8 means one in a hundred million. "
    "<b>It is a continuous suspicion level, not a binary verdict.</b>",
    "<b>So different consumers can apply different thresholds to the same "
    "signal.</b> Stop routing new requests at &phi; = 1 (cheap, easily "
    "reversed); trigger an expensive failover at &phi; = 8. <b>The action "
    "is proportional to the confidence</b>, which a boolean detector cannot "
    "express.",
    "<b>And it adapts automatically.</b> A link that is normally slow and "
    "variable produces a wide distribution, so the bar for suspicion rises; "
    "a consistently fast link lowers it. <b>Cassandra and Akka use "
    "this</b>, and it is strictly better than a fixed timeout for "
    "essentially no extra cost."]),
  ("table", ["Approach", "How it works", "Scaling"],
   [["<b>Central heartbeat</b>", "Every node reports to one monitor.",
     "<b>O(n) messages, and the monitor is a single point of failure</b> "
     "that must itself be made highly available — which is Module 06."],
    ["<b>All-to-all</b>", "Everyone pings everyone.",
     "<b>O(n&#178;) messages per round.</b> Works fine to tens of nodes and "
     "collapses somewhere around a hundred."],
    ["<b>Gossip</b>",
     "<b>Each node periodically exchanges membership with a random "
     "peer</b>, merging by version number.",
     "<b>O(log n) rounds to reach everyone, with O(1) messages per node per "
     "round</b> — see &sect;3."],
    ["<b>SWIM</b>",
     "<b>Probe one random node per round; if it does not answer, ask k "
     "other nodes to probe it on your behalf.</b>",
     "<b>O(1) per node per round</b>, with detection time independent of "
     "cluster size. <b>The indirect probe is the key idea</b> — it "
     "distinguishes 'unreachable from me' from 'dead', which directly "
     "attacks the false-positive problem of &sect;1."],
    ["<b>Ring / neighbour watching</b>",
     "Each node monitors its successors in a ring.",
     "O(1) per node, and slow to detect the failure of a contiguous region "
     "of the ring."],
    ["<b>Lease-based</b>",
     "<b>A node holds a time-limited lease and loses authority when it "
     "expires</b>, whether or not anyone noticed.",
     "<b>Self-expiring, which is its great virtue</b> — no detection "
     "is required for authority to lapse. <b>Pairs with fencing tokens</b> "
     "(Module 06 &sect;3)."]],
   [0.17, 0.39, 0.44]),

  ("break",),
  ("h1", "3 &nbsp; Gossip"),
  ("code", """Every T milliseconds, each node:
    pick a RANDOM peer
    exchange membership tables
    merge: for each node keep the entry with the higher
           version / incarnation number

PROPERTIES
  * reaches all n nodes in O(log n) rounds
  * O(1) messages per node per round, regardless of n
  * no coordinator and no single point of failure
  * robust to loss -- the next round retries implicitly

COST
  * eventual, not immediate: there is a propagation delay
  * O(n) state at every node (the full membership table)
  * conflicting entries need version numbers to order

REFUTATION: a node wrongly declared dead broadcasts a HIGHER
incarnation number for itself, which beats the death rumour on
merge. This is how SWIM survives false positives with no
central arbiter."""),
  ("p", "<b>The refutation mechanism is what makes false positives "
        "survivable.</b> Without it, a single mistaken suspicion propagates "
        "to the whole cluster and cannot be withdrawn; with it, <b>the "
        "accused node simply says otherwise and its statement wins</b>, "
        "because it holds a higher incarnation number for itself than "
        "anyone else can produce. It is a small and elegant mechanism that "
        "turns an unrecoverable error into a transient one."),

  ("h1", "4 &nbsp; Designing for false positives"),
  ("ul", ["<b>Make failover idempotent and reversible.</b> A node declared "
          "dead that subsequently returns must be able to rejoin cleanly "
          "without manual intervention — which is a design property, "
          "not an operational procedure.",
          "<b>Fence every side effect</b> (Module 06 &sect;3), so that a "
          "wrongly-evicted node resuming after a pause cannot corrupt "
          "anything. <b>This is the single most important item on the "
          "list</b>, because it converts a correctness failure into a "
          "rejected operation.",
          "<b>Use suspicion rather than a binary verdict</b> (&sect;2) and "
          "act proportionally to confidence.",
          "<b>Require a quorum of observers to agree a node is dead</b>, "
          "rather than letting one observer's view trigger action — "
          "which is SWIM's indirect probe generalised.",
          "<b>And rate-limit failover.</b> <b>A detector that flaps causes "
          "far more damage than the failures it detects</b>: repeated "
          "leader elections, repeated rebalancing, and repeated cache "
          "invalidation together constitute an outage. <b>Most "
          "failure-detection incidents are the detector overreacting, not "
          "the detector missing something</b>, and that asymmetry should "
          "shape the tuning."]),
  ("callout", "In a game, disconnection is a product decision",
   ["<b>A client that stops sending might have crashed, lost its "
    "connection, closed the game in frustration, or be deliberately "
    "exploiting the ambiguity to avoid a loss</b> — pulling the "
    "network cable to escape a fight is an old and effective cheat.",
    "<b>The server cannot tell</b>, and unlike an internal cluster it has "
    "no quorum of mutually-trusting peers to consult. There is exactly one "
    "observer and it has exactly one noisy signal.",
    "<b>So the policy is a design question rather than a technical "
    "one:</b> freeze the character in place, hand it to an AI, mark it "
    "invulnerable, or remove it immediately — and how many seconds to "
    "wait before doing so.",
    "<b>Every choice is exploitable.</b> Freezing lets players escape "
    "damage by disconnecting; immediate removal punishes players with "
    "genuinely poor connections; AI takeover produces a character behaving "
    "unlike its owner. <b>There is no correct answer, only a stated "
    "one</b> — which is worth recognising as a general pattern: "
    "<b>when the ambiguity is irreducible, the decision moves from "
    "engineering to policy</b>, and the right output of the engineering is "
    "a clear statement of the options and their costs."]),
 ],
 "resources": [
   ("Das, Gupta & Motivala &mdash; SWIM: Scalable Weakly-consistent "
    "Infection-style Process Group Membership (free)",
    "https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf",
    "<b>The &sect;2 and &sect;3 protocol</b>, including the indirect probe "
    "and the refutation mechanism."),
   ("Hayashibara et al. &mdash; The &phi; Accrual Failure Detector "
    "(free)",
    "https://www.computer.org/csdl/proceedings-article/srds/2004/22390066/12OmNvT2phv",
    "The &sect;2 detector, from the paper that introduced it."),
   ("HashiCorp &mdash; Serf and the Lifeguard extensions (free)",
    "https://www.serf.io/docs/internals/gossip.html",
    "<b>SWIM in production</b>, with the modifications needed to make it "
    "behave under real-world latency variance."),
   ("Chandra & Toueg &mdash; Unreliable Failure Detectors for Reliable "
    "Distributed Systems (free)",
    "https://dl.acm.org/doi/10.1145/226643.226647",
    "The theory of &sect;1 — what properties a detector must have for "
    "consensus to be solvable despite FLP (Module 05)."),
 ],
 "exercises": [
   "Implement heartbeat failure detection with a fixed timeout.",
   "<b>Measure your service's heartbeat inter-arrival distribution</b> and "
   "choose a timeout from the p99.9 rather than a round number.",
   "<b>Induce a 500 ms GC pause</b> and show your detector declares a false "
   "failure.",
   "Implement a phi accrual detector and plot &phi; over time through a "
   "real pause.",
   "<b>Use two different &phi; thresholds</b> for two different actions "
   "and show the behaviour differs appropriately.",
   "Implement gossip membership with version numbers.",
   "<b>Measure propagation time against cluster size</b> from 5 to 100 "
   "nodes and confirm the O(log n) behaviour.",
   "Implement SWIM's indirect probe and <b>demonstrate it preventing a "
   "false positive</b> caused by a one-way network problem.",
   "Implement incarnation-number refutation and show a wrongly-accused "
   "node recovering.",
   "<b>Make your detector flap</b> by setting the timeout too low under "
   "load, and measure the damage the resulting failovers cause.",
 ],
 "selfcheck": [
   "Why can you not distinguish a dead node from a slow one?",
   "What are the two kinds of detector error and what does each cost?",
   "How should a timeout be chosen, and what else must it be chosen "
   "against?",
   "What does phi accrual output, and give two advantages over a "
   "threshold.",
   "Compare six detection approaches on scaling.",
   "What is SWIM's indirect probe for?",
   "State gossip's properties and costs.",
   "What is refutation and why does it matter?",
   "Give five ways to tolerate false positives, and say which matters "
   "most.",
 ],
},

]
