# -*- coding: utf-8 -*-
"""CSCE 611 Operating Systems — original course content."""

COURSE = {
    "code": "CSCE 611",
    "title": "Operating Systems",
    "tagline": "Abstraction, arbitration, and isolation — built by "
               "writing a kernel rather than reading about one",
    "term": "Semester 2 (with CSCE 645 and CSCE 606)",
    "prereqs": "CSCE 614 Computer Architecture; C proficiency; comfort with "
               "pointers and manual memory",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A working kernel: context switching, a scheduler, "
                   "virtual memory, system calls, and a file system, running "
                   "on emulated hardware",
    "description": [
        "An operating system does two things. It <b>abstracts</b> hardware "
        "into something programmable — a disk becomes a file, a timer "
        "becomes a scheduler, physical memory becomes an address space. And "
        "it <b>arbitrates</b> between programs that would otherwise interfere "
        "— deciding who runs, who gets memory, who may read what.",
        "Both jobs are exercises in building a convincing illusion on "
        "uncooperative hardware. A process believes it has the whole machine; "
        "it has a few milliseconds at a time. It believes it has a contiguous "
        "address space; it has scattered physical pages. It believes a write "
        "landed on disk; it is in a buffer. Every one of those illusions "
        "leaks, and knowing where is most of what systems programming is.",
        "This course is built around implementation. Reading about context "
        "switching is not the same as writing the assembly that saves a "
        "register set and returns into a different stack. The xv6 teaching "
        "kernel — a small, complete, readable Unix — is the "
        "vehicle, and by the end you will have modified every major "
        "subsystem in it.",
        "CSCE 614 explained the machine. This course explains the software "
        "that makes the machine usable by more than one program at a time, "
        "and the two are deliberately adjacent: scheduling decisions are "
        "cache decisions, and page tables are the hardware you already met.",
    ],
    "outcomes": [
        "Explain the kernel/user boundary and how control crosses it.",
        "Implement context switching and explain exactly what must be saved.",
        "Compare scheduling policies and reason about the latency/throughput "
        "trade.",
        "Implement locks and condition variables, and explain why each "
        "primitive exists.",
        "Explain deadlock's four conditions and apply the standard responses.",
        "Implement a page-table-based virtual memory system with demand "
        "paging.",
        "Implement a file system with crash consistency, and explain why "
        "journaling works.",
        "Explain the isolation mechanisms behind containers and virtual "
        "machines.",
    ],
    "materials": [
        ("MIT 6.1810 / 6.S081 Operating System Engineering — xv6 (free, "
         "with labs)",
         "https://pdos.csail.mit.edu/6.1810/",
         "Primary source. A complete small Unix kernel with a book, lecture "
         "notes, and graded labs. The single best free OS course in "
         "existence."),
        ("MIT 6.S081 2020 archive — lecture video and labs",
         "https://pdos.csail.mit.edu/6.S081/2020/schedule.html",
         "The version with full recorded lectures. Use alongside the current "
         "course page."),
        ("OSTEP — Operating Systems: Three Easy Pieces (free book)",
         "https://pages.cs.wisc.edu/~remzi/OSTEP/",
         "The best written OS textbook, free from the authors. Organised as "
         "virtualisation, concurrency, persistence — which is this "
         "course's structure."),
        ("xv6: a simple, Unix-like teaching operating system (free book)",
         "https://pdos.csail.mit.edu/6.1810/2023/xv6/book-riscv-rev3.pdf",
         "The commentary on the xv6 source. Read it with the code open "
         "beside it."),
        ("Berkeley CS162 (free lectures)",
         "https://cs162.org/",
         "A third voice, with more emphasis on distributed systems and "
         "security."),
        ("Linux kernel documentation",
         "https://docs.kernel.org/",
         "What a production kernel actually does, for when you want to know "
         "how the real thing differs."),
    ],
    "tooling": [
        "<b>xv6-riscv</b> and the RISC-V toolchain. RISC-V because the "
        "privileged architecture is clean and documented in a readable "
        "specification, unlike x86.",
        "<b>QEMU</b> for emulation. You will not brick anything, and you can "
        "attach a debugger to a kernel mid-boot.",
        "<b>GDB</b> attached to QEMU. Being able to break inside an interrupt "
        "handler is the difference between understanding and guessing.",
        "<b>A Linux or WSL environment.</b> The toolchain assumes it.",
        "<b>A portfolio repository</b> with your kernel at each lab stage, "
        "and written notes on what broke.",
    ],
    "projects": [
        {"title": "Scheduler and system calls", "after": 5,
         "brief": "Add new system calls and replace xv6's scheduler. The "
                  "deliverable is a measurable change in behaviour, not just "
                  "code that compiles.",
         "reqs": [
             "At least three new system calls, including one that returns "
             "information about the calling process.",
             "A replacement for xv6's round-robin scheduler: implement "
             "multi-level feedback queues with aging.",
             "Priority inheritance on at least one lock, demonstrating that "
             "it fixes priority inversion.",
             "Instrumentation recording per-process run time, wait time, and "
             "context switch count.",
             "A workload mix of CPU-bound and I/O-bound processes used to "
             "compare schedulers.",
         ],
         "done": [
             "A table comparing round-robin and MLFQ on the same workload: "
             "average turnaround, average response time, and fairness.",
             "A demonstration of priority inversion occurring, and then not "
             "occurring after inheritance is added.",
             "A written explanation of one scheduling decision your "
             "implementation makes that surprised you.",
         ]},
        {"title": "Virtual memory and a file system", "after": 12,
         "brief": "Implement demand paging with swapping, then make the file "
                  "system survive crashes. Both must be demonstrated under "
                  "adversarial conditions, not just happy paths.",
         "reqs": [
             "Lazy allocation: <code>sbrk</code> returns immediately; pages "
             "are allocated on first fault.",
             "Copy-on-write <code>fork</code>, with page reference counting.",
             "Demand paging from a backing store, with a page replacement "
             "policy of your choice, implemented and justified.",
             "mmap and munmap for file-backed mappings.",
             "A journaling layer for the file system, with recovery on boot.",
             "A crash injection harness that kills the kernel at a random "
             "point during a write.",
         ],
         "done": [
             "COW fork demonstrated: fork a process with a 100 MB heap and "
             "show that physical memory use does not double until writes "
             "occur.",
             "A plot of fault count against working-set size for your "
             "replacement policy, compared against a second policy.",
             "One hundred crash-injection runs with the file system verified "
             "consistent after every one. Report the number of runs that "
             "required recovery.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What an Operating System Is For",
 "subtitle": "Abstraction, arbitration, and the illusions in between.",
 "question": "What problem does a kernel actually solve?",
 "outcomes": [
     "State the two jobs of an operating system and give examples of each.",
     "Explain the kernel/user boundary and what enforces it.",
     "Trace a system call from the user instruction to the kernel and back.",
     "Explain why hardware support is required for isolation.",
     "Describe the illusions an OS maintains and where each leaks.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two jobs",
   "blurb": "Everything a kernel does is one of these."},

  {"t": "two", "kicker": "The job", "title": "Abstraction and arbitration",
   "lh": "Abstraction — make hardware usable",
   "l": ["A disk becomes a <b>file</b>.",
         "Physical memory becomes an <b>address space</b>.",
         "A CPU becomes a <b>process</b>.",
         "A network card becomes a <b>socket</b>.",
         ("Each hides a device behind an interface you can program "
          "against.", 1)],
   "rh": "Arbitration — share it safely",
   "r": ["Who runs next? (scheduling)",
         "Who gets this memory? (allocation)",
         "Who may read this file? (protection)",
         "What happens when two programs want the same thing?",
         ("Each prevents one program from ruining another.", 1)],
   "note": "Every module in this course slots into one column or the other. "
           "Worth saying so now."},

  {"t": "callout", "title": "Both jobs are the same job",
   "kind": "Framing",
   "body": ["Abstraction without arbitration is a library. Arbitration "
            "without abstraction is a traffic cop with nothing to direct.",
            "The kernel's real work is maintaining a set of <b>illusions</b>: "
            "each program believes it has the whole machine, a contiguous "
            "address space, and exclusive access to its files.",
            "Those illusions are what makes programs writable. Without them "
            "every application would have to cooperate explicitly with every "
            "other, which is how computers worked before 1965 and why they "
            "were unusable.",
            "Every illusion leaks somewhere. The rest of this course is "
            "largely about where."]},

  {"t": "table", "kicker": "Illusions", "title": "What a process believes, and the truth",
   "header": ["The illusion", "The reality", "Where it leaks"],
   "widths": [3.4, 4.4, 4.3],
   "rows": [
     ["I have the whole CPU", "A few ms at a time", "Timing jitter; cache cold after a switch"],
     ["I have contiguous memory", "Scattered physical pages", "TLB misses (CSCE 614 Mod 07); page faults"],
     ["My memory is private", "Shared hardware", "Spectre; cache side channels"],
     ["My write reached disk", "It is in a buffer", "<b>Data loss on power failure</b>"],
     ["Files are byte arrays", "Blocks on a device", "Alignment; fsync cost"],
   ],
   "note": "The fsync row is the one that costs companies money. It gets its "
           "own module (09)."},

  {"t": "section", "label": "Part 2", "title": "The boundary",
   "blurb": "Two modes, enforced by hardware, crossed deliberately."},

  {"t": "bullets", "kicker": "Privilege", "title": "Why isolation needs hardware",
   "items": [
     "A kernel cannot protect itself using software alone — any check it "
     "writes, a program could skip.",
     "",
     "So the <b>CPU</b> provides at least two modes:",
     ("<b>User mode:</b> ordinary instructions only. No device access, no "
      "page table changes.", 1),
     ("<b>Supervisor/kernel mode:</b> everything.", 1),
     "",
     "Privileged instructions attempted in user mode <b>trap</b> — "
     "control transfers to the kernel.",
     "",
     "The one-way door: user code can enter the kernel only at addresses the "
     "<i>kernel</i> chose.",
   ],
   "note": "The 'kernel chooses the entry point' property is the whole "
           "security argument and is worth stating explicitly."},

  {"t": "code", "kicker": "System call", "title": "Crossing the boundary, step by step",
   "lang": "c", "code": """
// User code
write(fd, buf, n);

// 1. libc places the syscall number in a register, args in others
//    a7 = SYS_write;  a0 = fd;  a1 = buf;  a2 = n
// 2. executes ECALL  (RISC-V) / SYSCALL (x86-64) / SVC (ARM)
//
// -- HARDWARE: switch to supervisor mode, jump to the trap vector
//    the kernel installed at boot. User code never chose this address.
//
// 3. Kernel saves the user register set into the trapframe
// 4. Looks up the syscall number in a table -> sys_write()
// 5. VALIDATES the arguments:
//      is fd open?  is [buf, buf+n) inside this process's address space?
// 6. Does the work
// 7. Restores registers, places the return value, executes SRET
//
// -- HARDWARE: back to user mode, resume after the ECALL
""",
   "caption": "Step 5 is the security boundary. A pointer from user space is "
              "<b>untrusted input</b> and must be checked every time.",
   "note": "Students consistently underrate step 5. Most kernel CVEs are a "
           "missing check there."},

  {"t": "callout", "title": "Never trust a user pointer",
   "kind": "The rule that matters",
   "body": ["A system call argument is attacker-controlled data. A pointer "
            "that happens to be valid in user space may point at kernel "
            "memory, at another process, or at nothing.",
            "The kernel must validate every pointer and every length against "
            "the calling process's address space <i>before</i> dereferencing "
            "— and must not be fooled by overflow in "
            "<code>buf + n</code>.",
            "It must also copy the data rather than using it in place, "
            "because another thread in the same process could change it "
            "between the check and the use. That is a "
            "<b>time-of-check/time-of-use</b> bug, and it is a standard "
            "exploitation technique.",
            "A large fraction of kernel vulnerabilities are a missing or "
            "defeated check here."]},

  {"t": "section", "label": "Part 3", "title": "Entering the kernel",
   "blurb": "Three ways in, one way back."},

  {"t": "table", "kicker": "Traps", "title": "Three reasons control enters the kernel",
   "header": ["Cause", "Source", "Example", "Synchronous?"],
   "widths": [2.6, 2.8, 3.6, 3.1],
   "rows": [
     ["System call", "Deliberate, by the program", "read, write, fork", "Yes"],
     ["Exception", "The program did something", "Page fault, divide by zero", "Yes"],
     ["Interrupt", "A device, externally", "Timer, disk, keyboard", "<b>No</b>"],
   ],
   "note": "The synchronous/asynchronous distinction matters: an interrupt "
           "can arrive anywhere, which is why kernels disable them in "
           "critical sections."},

  {"t": "bullets", "kicker": "Timer", "title": "Why the timer interrupt is the most important one",
   "items": [
     "Without it, a process that never makes a system call <b>never yields</b>.",
     ("One infinite loop would hang the machine. That was cooperative "
      "multitasking, and it is why Windows 3.1 froze.", 1),
     "",
     "The timer interrupt gives the kernel control back unconditionally.",
     "",
     "<b>Preemptive</b> multitasking is exactly this: the kernel can take the "
     "CPU away whether the process cooperates or not.",
     "",
     "Everything in Module 03 depends on it.",
   ],
   "footnote": "A scheduler without a timer is a suggestion."},

  {"t": "bullets", "kicker": "Structure", "title": "Where the kernel sits",
   "items": [
     "<b>Monolithic</b> — drivers and file systems run in kernel mode. "
     "Fast; a driver bug takes down the machine. (Linux, Windows, xv6.)",
     "",
     "<b>Microkernel</b> — only IPC, scheduling, and memory in the "
     "kernel; everything else is a user process. Robust; IPC cost. (seL4, "
     "QNX, Minix.)",
     "",
     "<b>Hybrid</b> — mostly monolithic with some services moved out. "
     "(macOS/XNU.)",
     "",
     "Module 13 returns to this. For now: xv6 is monolithic and small enough "
     "to read entirely.",
   ]},
 ],
 "takeaways": [
   "An OS abstracts hardware into programmable objects and arbitrates between "
   "programs that would otherwise interfere.",
   "The kernel maintains illusions — whole CPU, contiguous private "
   "memory, durable writes — and every one of them leaks somewhere.",
   "Isolation requires hardware support: user and supervisor modes, with "
   "privileged instructions trapping.",
   "User code can enter the kernel only at addresses the kernel chose. That "
   "one-way door is the entire security boundary.",
   "Every user pointer is untrusted input. Validate it, and copy rather than "
   "using it in place, or you have a TOCTOU bug.",
   "The timer interrupt is what makes preemption possible. Without it a "
   "single infinite loop hangs the machine.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The two jobs"),
  ("p", "Strip away the detail and an operating system does two things."),
  ("table", ["Job", "Means", "Examples"],
   [["<b>Abstraction</b>",
     "Turn awkward hardware into something a program can be written against.",
     "A spinning disk with sectors and seek times becomes a file you "
     "<code>read()</code>. Physical RAM becomes a private address space. One "
     "CPU becomes many processes. A network card becomes a socket."],
    ["<b>Arbitration</b>",
     "Decide who gets what, and prevent programs from interfering with each "
     "other.",
     "Scheduling the CPU. Allocating memory. Enforcing file permissions. "
     "Ensuring one process cannot read another's data or crash the "
     "machine."]],
   [0.17, 0.36, 0.47]),
  ("callout", "The two are inseparable",
   ["Abstraction without arbitration is a library — useful, and no "
    "protection. Arbitration without abstraction is a traffic policeman with "
    "nothing to direct.",
    "The kernel's actual work is maintaining a set of <b>illusions</b>: each "
    "program is given a convincing impression that it owns the machine. That "
    "illusion is what makes programs writable at all — the alternative "
    "is that every application must cooperate explicitly with every other, "
    "which is how computing worked before the mid-1960s and why it did not "
    "scale.",
    "Every illusion leaks. Knowing where each one leaks is a large part of "
    "what distinguishes a systems programmer."]),
  ("table", ["What a process believes", "What is actually true", "Where it leaks"],
   [["I have the CPU to myself.",
     "It gets a few milliseconds at a time, interleaved with others.",
     "Timing jitter; cold caches after a context switch (CSCE 614 Module 05); "
     "unpredictable latency."],
    ["My address space is contiguous and starts at a fixed address.",
     "Physical pages are scattered wherever they were free.",
     "TLB misses (CSCE 614 Module 07); page faults; NUMA placement."],
    ["My memory is private.",
     "Caches, branch predictors, and TLBs are shared hardware.",
     "Spectre and cache side channels (CSCE 614 Module 04)."],
    ["My <code>write()</code> reached the disk.",
     "It is in a kernel buffer and may not be written for seconds.",
     "<b>Data loss on power failure.</b> Module 09."],
    ["A file is a contiguous array of bytes.",
     "It is a set of blocks scattered across a device.",
     "Alignment effects; the cost of <code>fsync</code>; fragmentation."]],
   [0.28, 0.32, 0.40]),

  ("h1", "2 &nbsp; The kernel/user boundary"),
  ("p", "Isolation cannot be achieved in software alone. Any check the kernel "
        "writes in software is an instruction a malicious program could "
        "simply not execute. The guarantee must come from hardware."),
  ("h2", "2.1 &nbsp; Privilege modes"),
  ("p", "Every processor intended to run an operating system provides at "
        "least two privilege modes:"),
  ("ul", ["<b>User mode.</b> Ordinary computation only. Instructions that "
          "touch devices, modify page tables, disable interrupts, or change "
          "privilege level are forbidden and <b>trap</b> if attempted.",
          "<b>Supervisor (kernel) mode.</b> Everything is permitted."]),
  ("callout", "The one-way door",
   ["The crucial property is not merely that user code cannot execute "
    "privileged instructions. It is that user code cannot <i>choose where it "
    "enters the kernel</i>.",
    "At boot, the kernel installs a <b>trap vector</b> — a fixed address "
    "the hardware jumps to on any trap. A system call instruction transfers "
    "control to that address and nowhere else.",
    "So the kernel is entered only at code the kernel wrote, with the "
    "hardware having already switched privilege level. Without this, a "
    "program could jump into the middle of a kernel routine past its "
    "validation checks, and no amount of careful kernel programming would "
    "help."]),
  ("h2", "2.2 &nbsp; A system call, step by step"),
  ("code", """// User code
write(fd, buf, n);

// 1. libc loads the call number and arguments into registers:
//       a7 = SYS_write, a0 = fd, a1 = buf, a2 = n
// 2. executes ECALL (RISC-V) / SYSCALL (x86-64) / SVC (ARM)

//    HARDWARE: raise privilege to supervisor mode; jump to the
//    trap vector the kernel installed at boot.

// 3. Kernel saves the user register set into the process's trapframe.
// 4. Dispatches on the call number to sys_write().
// 5. VALIDATES: is fd a valid open file for this process?
//               does [buf, buf+n) lie entirely within this
//               process's address space?
// 6. Performs the operation.
// 7. Places the return value, restores registers, executes SRET.

//    HARDWARE: drop to user mode; resume at the instruction
//    after the ECALL."""),
  ("callout", "Step 5 is the security boundary",
   ["Every argument to a system call is <b>attacker-controlled data</b>. A "
    "pointer supplied by a user program might point into the kernel, into "
    "another process's memory, or at an unmapped address.",
    "The kernel must check every pointer and length against the calling "
    "process's own address space before dereferencing — and the check "
    "must not be defeated by integer overflow in <code>buf + n</code>.",
    "It must also <b>copy</b> the data into kernel memory rather than "
    "operating on it in place, because another thread in the same process "
    "could modify it between the validation and the use. That is a "
    "<b>time-of-check to time-of-use</b> race, and it is a standard "
    "exploitation technique rather than a theoretical concern.",
    "A substantial fraction of all kernel vulnerabilities are a missing, "
    "incomplete, or racily-defeated check at this step."]),

  ("break",),
  ("h1", "3 &nbsp; Three ways into the kernel"),
  ("table", ["Cause", "Origin", "Synchronous?", "Examples"],
   [["<b>System call</b>", "The program asks, deliberately.", "Yes",
     "<code>read</code>, <code>write</code>, <code>fork</code>, "
     "<code>exit</code>."],
    ["<b>Exception / fault</b>", "The program did something the hardware "
     "could not complete.", "Yes",
     "Page fault, divide by zero, illegal instruction, protection "
     "violation."],
    ["<b>Interrupt</b>", "A device, independently of what is running.",
     "<b>No</b>",
     "Timer tick, disk completion, keyboard, network packet arrival."]],
   [0.17, 0.33, 0.14, 0.36]),
  ("p", "The synchronous/asynchronous distinction has real consequences. A "
        "system call or fault happens at a known instruction in a known "
        "context. An interrupt can arrive <i>anywhere</i> — including in "
        "the middle of a kernel routine that is halfway through updating a "
        "data structure. This is why kernels disable interrupts around "
        "critical sections, and why interrupt handlers must be short and must "
        "not block."),
  ("p", "Note that a <b>page fault</b> is an exception, not an error. It is "
        "the normal mechanism by which demand paging, copy-on-write, and "
        "memory-mapped files work (Module 07). Most page faults are expected "
        "and are handled by allocating a page and resuming."),
  ("h2", "3.1 &nbsp; The timer interrupt"),
  ("callout", "The interrupt that makes everything else possible",
   ["Suppose a process enters an infinite loop that makes no system calls. If "
    "the kernel only regains control when a program asks for something, it "
    "never regains control. The machine hangs.",
    "That was <b>cooperative</b> multitasking, and it is exactly why early "
    "Windows and Mac systems could be frozen by a single misbehaving "
    "application.",
    "The <b>timer interrupt</b> fires on a hardware clock regardless of what "
    "the running program does. The kernel regains control unconditionally, "
    "every few milliseconds, and can choose to run something else.",
    "<b>Preemptive multitasking is precisely this capability.</b> Every "
    "scheduling policy in Module 03 presupposes it; without a timer, a "
    "scheduler is only a suggestion."]),

  ("h1", "4 &nbsp; Kernel structure"),
  ("table", ["Design", "What runs in kernel mode", "Trade-off", "Examples"],
   [["<b>Monolithic</b>", "Scheduling, memory, file systems, device drivers, "
     "network stack — all of it.",
     "Fast: a file system call is a function call. Fragile: a driver bug can "
     "corrupt anything.", "Linux, Windows NT, xv6, FreeBSD."],
    ["<b>Microkernel</b>", "Only IPC, scheduling, and basic memory "
     "management. Drivers and file systems are ordinary user processes.",
     "Robust: a driver crash kills one process. Costly: every service "
     "interaction is IPC rather than a call.",
     "seL4, QNX, Minix 3, L4."],
    ["<b>Hybrid</b>", "Mostly monolithic, with selected services moved out.",
     "A pragmatic middle.", "macOS (XNU), Windows in part."]],
   [0.15, 0.33, 0.30, 0.22]),
  ("p", "Module 13 returns to this argument with the evidence from the "
        "intervening twelve modules. For now it is enough to know that xv6 is "
        "monolithic, which is why the whole kernel is about nine thousand "
        "lines and can be read in a weekend — which is the point of "
        "using it."),
 ],
 "resources": [
   ("MIT 6.1810 — Lecture 1 (Introduction and Examples) and the xv6 "
    "book, Chapter 1",
    "https://pdos.csail.mit.edu/6.1810/",
    "Sets up the whole course. Do the setup lab in the same sitting."),
   ("OSTEP — Chapters 2 and 4 (Introduction, The Abstraction: The "
    "Process)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "The abstraction/arbitration framing, written unusually well."),
   ("xv6 book — Chapter 4 (Traps and system calls)",
    "https://pdos.csail.mit.edu/6.1810/2023/xv6/book-riscv-rev3.pdf",
    "The system call path through actual code. Read it with "
    "<code>trampoline.S</code> open beside it."),
   ("RISC-V Privileged Architecture specification",
    "https://riscv.org/technical/specifications/",
    "The hardware contract for privilege modes and traps. Short, clear, and "
    "far more readable than the x86 equivalent."),
 ],
 "exercises": [
   "Set up the xv6 toolchain and QEMU. Boot xv6, run <code>ls</code>, and "
   "attach GDB to the running kernel. Set a breakpoint in "
   "<code>syscall()</code> and observe a call arriving.",
   "Trace a single <code>write()</code> from user code to the kernel and "
   "back, using GDB. Record every mode transition and where the registers "
   "are saved.",
   "Add a system call <code>getpinfo()</code> returning the calling process's "
   "PID, state, and accumulated run time. This requires touching the syscall "
   "table, the user library, and the kernel.",
   "Write a user program that passes a deliberately invalid pointer to a "
   "system call. Confirm the kernel rejects it rather than crashing, and find "
   "the validation code that caught it.",
   "Remove the timer interrupt handler from xv6 and run a program with an "
   "infinite loop. Observe the hang, then restore it. This makes preemption "
   "concrete.",
   "Count the lines of code in xv6 by subsystem. Compare against the line "
   "count of the Linux kernel and consider what the difference consists of.",
 ],
 "selfcheck": [
   "State the two jobs of an operating system, with two examples of each.",
   "Name three illusions a kernel maintains and say where each leaks.",
   "Why can isolation not be implemented in software alone?",
   "What is a trap vector, and why does it matter that user code cannot "
   "choose the kernel entry address?",
   "Why must the kernel copy data from a user pointer rather than using it in "
   "place?",
   "Name the three ways control enters the kernel and say which is "
   "asynchronous.",
   "Why is the timer interrupt the precondition for preemptive "
   "multitasking?",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Processes, Threads, and Context Switching",
 "subtitle": "The illusion of having the machine to yourself.",
 "question": "What exactly must be saved to stop one program and start "
             "another?",
 "outcomes": [
     "Describe a process's state and where the kernel keeps it.",
     "Implement a context switch and explain each saved register.",
     "Distinguish processes from threads and state what each shares.",
     "Explain fork, exec, and why they are separate calls.",
     "Quantify context switch cost, including the indirect costs.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a process is",
   "blurb": "A program in execution, plus everything needed to resume it."},

  {"t": "table", "kicker": "Process state", "title": "What the kernel must remember",
   "header": ["Component", "Contains", "Where"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Registers", "PC, SP, general purpose, status", "Trapframe / context struct"],
     ["Address space", "Page table root", "PCB; installed on switch"],
     ["Open files", "File descriptor table", "PCB"],
     ["Kernel stack", "Per-process, for syscalls and traps", "Allocated at creation"],
     ["Scheduling state", "Priority, run time, state", "PCB"],
     ["Identity", "PID, parent, UID, working directory", "PCB"],
   ],
   "note": "The per-process kernel stack is the one students miss. Without "
           "it, a blocked syscall could not resume."},

  {"t": "bullets", "kicker": "States", "title": "The process state machine",
   "items": [
     "<b>RUNNING</b> — currently on a CPU.",
     "<b>RUNNABLE</b> — ready, waiting for a CPU.",
     "<b>SLEEPING</b> — waiting for an event (I/O, a lock, a child).",
     "<b>ZOMBIE</b> — exited, but the parent has not collected the exit "
     "status.",
     "",
     "The transition that matters: <b>RUNNING → SLEEPING</b> is "
     "voluntary (a blocking call); <b>RUNNING → RUNNABLE</b> is "
     "involuntary (preemption).",
     "",
     "Zombies exist so a parent can always read a child's exit status, "
     "whenever it gets around to it.",
   ],
   "note": "The zombie explanation ('the exit status must outlive the "
           "process') clears up a perennial confusion."},

  {"t": "section", "label": "Part 2", "title": "The switch",
   "blurb": "A function that returns into a different process."},

  {"t": "code", "kicker": "Context switch", "title": "The strangest function you will write",
   "lang": "asm", "code": """
# swtch(old_context*, new_context*)
# Save callee-saved registers into *old, load them from *new.
# Caller-saved registers are already on the stack by convention.

swtch:
    sd ra,  0(a0)        # save return address
    sd sp,  8(a0)        # save stack pointer
    sd s0, 16(a0)        # ... callee-saved registers s0-s11
    ...
    ld ra,  0(a1)        # load the NEW process's return address
    ld sp,  8(a1)        # load the NEW process's stack
    ld s0, 16(a1)
    ...
    ret                  # returns to where the NEW process left off

# You called it from process A. It returns in process B.
# The `ret` uses the ra that was just loaded from the new context.
""",
   "caption": "Only callee-saved registers need saving — the calling "
              "convention guarantees the rest were already spilled by "
              "whoever called swtch.",
   "note": "The 'called in A, returns in B' framing is what makes this click. "
           "It is genuinely strange the first time."},

  {"t": "callout", "title": "The scheduler runs on its own stack",
   "kind": "The design that avoids a paradox",
   "body": ["A process cannot switch directly to another process. It would "
            "have to run on its own stack while tearing that stack down.",
            "So xv6 switches <b>process → scheduler → process</b>. "
            "Each CPU has a dedicated scheduler context with its own stack.",
            "The process calls <code>swtch</code> into the scheduler; the "
            "scheduler picks the next runnable process and calls "
            "<code>swtch</code> into it.",
            "Two switches instead of one, and the scheduler always has a "
            "valid stack to run on. Every real kernel does something "
            "equivalent."]},

  {"t": "section", "label": "Part 3", "title": "Threads",
   "blurb": "The same mechanism, sharing more."},

  {"t": "two", "kicker": "Compare", "title": "Process and thread",
   "lh": "Processes",
   "l": ["Separate address spaces.",
         "Communication via IPC: pipes, sockets, shared memory.",
         "A crash kills one process only.",
         "Switch costs a page table change → TLB flush.",
         ("Isolation by default.", 1)],
   "rh": "Threads",
   "r": ["<b>Share</b> the address space, file descriptors, signal handlers.",
         "Communication by just writing to memory.",
         "A crash takes down the whole process.",
         "Switch keeps the page table → no TLB flush.",
         ("Cheap, and no isolation at all.", 1)],
   "note": "The TLB flush difference is the quantitative reason threads are "
           "cheaper, and it comes straight from CSCE 614 Module 07."},

  {"t": "bullets", "kicker": "Threads", "title": "Where threads are implemented",
   "items": [
     "<b>Kernel threads (1:1).</b> The kernel schedules each one. True "
     "parallelism; syscall cost per switch. (Linux, Windows.)",
     "",
     "<b>User threads (N:1).</b> A library multiplexes many onto one kernel "
     "thread. Very cheap switches; <b>one blocking call blocks all of "
     "them</b>, and no multicore parallelism.",
     "",
     "<b>Hybrid (M:N).</b> Attempted repeatedly; the complexity rarely paid "
     "off.",
     "",
     "<b>Modern answer:</b> green threads / coroutines over an async runtime "
     "— Go goroutines, Rust async, virtual threads. N:1 with "
     "non-blocking I/O underneath.",
   ],
   "note": "Goroutines being 'N:M done right because the runtime owns the "
           "I/O' is the honest summary."},

  {"t": "section", "label": "Part 4", "title": "fork and exec",
   "blurb": "An unusual design that turns out to be right."},

  {"t": "code", "kicker": "fork/exec", "title": "Two calls where one would seem to do",
   "lang": "c", "code": """
pid_t pid = fork();           // duplicate the calling process
if (pid == 0) {
    // child: a copy of the parent, with pid == 0 returned
    close(1); open("out.txt", O_WRONLY|O_CREAT);  // redirect stdout
    execv("/bin/ls", argv);   // REPLACE the program, keep the process
    // only reached if exec failed
} else {
    wait(&status);            // parent collects the child
}

// Why two calls? The gap between them is where the shell sets up
// redirection, pipes, signal handling, and resource limits --
// in the child, using ordinary code, with no special API.
""",
   "caption": "A combined spawn() would need a parameter for every possible "
              "adjustment. fork/exec lets you make them with ordinary code.",
   "note": "This is the clearest example in the course of an interface "
           "decision paying off in flexibility."},

  {"t": "callout", "title": "Copy-on-write makes fork cheap",
   "kind": "The implementation trick",
   "body": ["Copying a parent's entire address space would make "
            "<code>fork</code> absurdly expensive — and most of that "
            "copy is thrown away immediately by <code>exec</code>.",
            "So: do not copy. Map the same physical pages into both, mark "
            "them <b>read-only</b> in both page tables, and increment a "
            "reference count.",
            "On the first <i>write</i>, the hardware raises a page fault. The "
            "kernel copies that one page, makes the copy writable, and "
            "resumes.",
            "Only pages actually modified are ever copied. "
            "<code>fork</code> + <code>exec</code> copies almost nothing. "
            "This is Project 2's requirement and a direct use of CSCE 614 "
            "Module 07."]},

  {"t": "table", "kicker": "Cost", "title": "What a context switch actually costs",
   "header": ["Cost", "Magnitude", "Why"],
   "widths": [3.6, 3.2, 5.3],
   "rows": [
     ["Direct (save/restore)", "~1–2 μs", "Registers, scheduler logic"],
     ["TLB flush", "Significant", "Page table change; CSCE 614 Mod 07"],
     ["Cold cache", "<b>Often dominant</b>", "The new process's data is not in cache"],
     ["Branch predictor", "Moderate", "History is now wrong"],
   ],
   "footnote": "The indirect costs usually exceed the direct ones several "
               "times over.",
   "note": "This is why scheduling quanta are milliseconds, not "
           "microseconds — the switch must be amortised."},
 ],
 "takeaways": [
   "A process is a program plus everything needed to resume it: registers, "
   "address space, open files, kernel stack, and scheduling state.",
   "A context switch saves callee-saved registers and returns into a "
   "different process — called in A, returning in B.",
   "Switching goes process → scheduler → process, because the "
   "scheduler needs its own stack to run on.",
   "Threads share the address space, so switching avoids a TLB flush. That is "
   "the quantitative reason they are cheaper.",
   "fork and exec are separate so the gap between them can be used for "
   "redirection and setup with ordinary code.",
   "Copy-on-write makes fork cheap: share pages read-only and copy only on "
   "the first write.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a process consists of"),
  ("p", "A process is a program in execution together with everything the "
        "kernel needs in order to stop it and later resume it as though "
        "nothing had happened. That state lives in the <b>process control "
        "block</b>."),
  ("table", ["Component", "Contents", "Why it is needed"],
   [["<b>Register state</b>", "Program counter, stack pointer, general "
     "registers, status register.",
     "Execution resumes exactly where it stopped."],
    ["<b>Address space</b>", "The root of the page table.",
     "Installed on switch; defines what memory the process can see "
     "(CSCE 614 Module 07)."],
    ["<b>Open file table</b>", "File descriptors and their offsets.",
     "A read must continue where the last one stopped."],
    ["<b>Kernel stack</b>", "A separate stack used while in kernel mode.",
     "A system call that blocks must keep its kernel-side call frames. "
     "Without a per-process kernel stack, a blocked syscall could not be "
     "resumed."],
    ["<b>Scheduling state</b>", "State, priority, accumulated run time.",
     "Module 03."],
    ["<b>Identity</b>", "PID, parent PID, user ID, working directory.",
     "Permissions and process relationships."]],
   [0.19, 0.36, 0.45]),
  ("h2", "1.1 &nbsp; States"),
  ("table", ["State", "Meaning", "Leaves by"],
   [["<b>RUNNING</b>", "Executing on a CPU now.",
     "Blocking (&rarr; SLEEPING), being preempted (&rarr; RUNNABLE), or "
     "exiting (&rarr; ZOMBIE)."],
    ["<b>RUNNABLE</b>", "Ready to run; waiting only for a CPU.",
     "Being scheduled (&rarr; RUNNING)."],
    ["<b>SLEEPING</b>", "Waiting for an event: I/O completion, a lock, a "
     "child's exit.", "The event occurring (&rarr; RUNNABLE)."],
    ["<b>ZOMBIE</b>", "Has exited; the exit status has not yet been "
     "collected.", "The parent calling <code>wait()</code>."]],
   [0.17, 0.38, 0.45]),
  ("callout", "Why zombies exist",
   ["When a process exits, its exit status must remain available until the "
    "parent asks for it — the parent may not be running at that moment, "
    "and may not ask for some time.",
    "So the process's memory, files, and address space are released "
    "immediately, and a small record survives holding the exit status. That "
    "record is the zombie.",
    "A zombie is therefore not a leak or a malfunction; it is a deliberate "
    "data structure. An <i>accumulation</i> of zombies is a bug — a "
    "parent that never calls <code>wait()</code>. If the parent dies first, "
    "the child is reparented to init, which reaps it."]),

  ("h1", "2 &nbsp; The context switch"),
  ("code", """# swtch(struct context *old, struct context *new)
swtch:
    sd ra,  0(a0)        # save return address into *old
    sd sp,  8(a0)        # save stack pointer
    sd s0, 16(a0)        # save callee-saved registers s0-s11
    ...                  #   (caller-saved ones are already spilled
    ...                  #    by the calling convention)

    ld ra,  0(a1)        # load the NEW context's return address
    ld sp,  8(a1)        # load the NEW context's stack pointer
    ld s0, 16(a1)
    ...
    ret                  # return using the newly loaded ra"""),
  ("callout", "Called in one process, returns in another",
   ["<code>swtch</code> is entered on process A's stack and leaves on process "
    "B's. The <code>ret</code> at the end uses the return address just loaded "
    "from B's saved context, so control resumes wherever B last called "
    "<code>swtch</code>.",
    "From B's point of view, its own call to <code>swtch</code> — made "
    "possibly milliseconds ago — has simply returned.",
    "Only <b>callee-saved</b> registers are stored. The calling convention "
    "guarantees that caller-saved registers were already spilled to the stack "
    "by whoever called <code>swtch</code>, and that stack is saved along with "
    "the stack pointer. This is a genuine economy, not a shortcut."]),
  ("h2", "2.1 &nbsp; Why there are two switches, not one"),
  ("callout", "The scheduler needs its own stack",
   ["A process cannot switch directly to another process: it would have to "
    "execute the switching code on its own kernel stack while that stack is "
    "being abandoned.",
    "xv6 therefore switches <b>process &rarr; scheduler &rarr; process</b>. "
    "Each CPU has a dedicated scheduler context with its own stack. The "
    "outgoing process calls <code>swtch</code> into the scheduler; the "
    "scheduler loop selects the next runnable process and calls "
    "<code>swtch</code> into it.",
    "Two switches rather than one, and at every moment the code that is "
    "running has a valid stack that nobody is about to reuse. Every real "
    "kernel does something equivalent, whatever it calls it."]),

  ("break",),
  ("h1", "3 &nbsp; Threads"),
  ("table", ["", "Processes", "Threads"],
   [["Address space", "Separate.", "<b>Shared.</b>"],
    ["File descriptors", "Separate.", "<b>Shared.</b>"],
    ["Communication", "IPC: pipes, sockets, shared memory segments.",
     "Write to a variable."],
    ["Fault isolation", "A crash affects one process.",
     "A crash takes down every thread in the process."],
    ["Switch cost", "Page table change &rarr; <b>TLB flush</b>.",
     "No page table change &rarr; no flush."],
    ["Default posture", "Isolated.", "No isolation whatsoever."]],
   [0.17, 0.42, 0.41]),
  ("p", "The switch-cost row is the quantitative heart of the comparison. "
        "Changing address space invalidates TLB entries (CSCE 614 Module 07), "
        "so the new process begins with no cached translations and pays page "
        "walks until the TLB refills. Modern hardware mitigates this with "
        "address-space identifiers that tag TLB entries, avoiding a full "
        "flush — but the cache is still cold either way."),
  ("h2", "3.1 &nbsp; Where threads live"),
  ("table", ["Model", "How", "Consequence"],
   [["<b>1:1 (kernel threads)</b>", "Each user thread is a kernel-scheduled "
     "entity.",
     "True multicore parallelism. Each switch is a kernel operation. Linux "
     "and Windows use this."],
    ["<b>N:1 (user threads)</b>", "A library multiplexes many threads onto "
     "one kernel thread.",
     "Switches are a function call — very cheap. <b>One blocking system "
     "call blocks every thread</b>, and no multicore parallelism is "
     "possible."],
    ["<b>M:N</b>", "Many user threads over several kernel threads.",
     "Attempted repeatedly (Solaris, early Rust) and generally abandoned: the "
     "scheduler interactions are complex and the benefit modest."],
    ["<b>Async runtimes</b>", "N:1 or M:N, with the runtime owning all I/O "
     "and making it non-blocking.",
     "The modern answer. Go goroutines, Rust async, Java virtual threads. "
     "Cheap switches <i>and</i> no blocking problem, because the runtime "
     "controls the blocking points."]],
   [0.22, 0.36, 0.42]),

  ("h1", "4 &nbsp; fork and exec"),
  ("p", "Unix creates processes with two calls where most systems have one. "
        "<code>fork()</code> duplicates the calling process; "
        "<code>exec()</code> replaces the program running in the current "
        "process, keeping the process itself."),
  ("code", """pid_t pid = fork();
if (pid == 0) {
    // Child. The gap between fork and exec is the useful part:
    close(1);
    open("out.txt", O_WRONLY | O_CREAT, 0666);   // becomes fd 1
    setrlimit(...);                              // resource limits
    signal(SIGINT, SIG_DFL);                     // reset handlers
    execv("/bin/ls", argv);                      // replace the program
    _exit(1);                                    // exec failed
} else {
    wait(&status);
}"""),
  ("callout", "Why two calls is the better design",
   ["A single <code>spawn(program, args, ...)</code> call would need a "
    "parameter for every adjustment anyone might want: redirect this "
    "descriptor, set that limit, change the working directory, adjust the "
    "signal mask, join this namespace. The parameter list grows without "
    "bound, and anything the designers did not anticipate is impossible.",
    "With <code>fork</code>/<code>exec</code>, the child performs those "
    "adjustments with <b>ordinary code</b>, using the same system calls "
    "available everywhere else. A shell implements pipes, redirection, and "
    "job control entirely in this gap, with no special API.",
    "The cost is that <code>fork</code> is expensive to implement well, and "
    "that it interacts badly with threads — only the calling thread "
    "survives in the child, so locks held by other threads are left held "
    "forever. This is why <code>posix_spawn</code> and "
    "<code>vfork</code> exist, and why fork-in-a-threaded-program is "
    "treacherous."]),
  ("h2", "4.1 &nbsp; Copy-on-write"),
  ("callout", "The optimisation that makes fork viable",
   ["Duplicating the parent's entire address space would make "
    "<code>fork</code> cost time proportional to the parent's memory "
    "footprint — and in the common <code>fork</code>-then-"
    "<code>exec</code> pattern, essentially all of that work is discarded "
    "microseconds later.",
    "So the kernel does not copy. It maps the same physical pages into both "
    "address spaces, marks them <b>read-only in both</b>, and increments a "
    "per-page reference count.",
    "The first time either process writes, the hardware raises a page fault. "
    "The kernel allocates one new page, copies the contents, makes the copy "
    "writable in the faulting process, decrements the reference count, and "
    "resumes the instruction.",
    "Only pages actually written are ever copied. <code>fork</code> becomes "
    "proportional to the page table size rather than the memory size, and "
    "<code>fork</code>+<code>exec</code> copies almost nothing. This is "
    "required in Project 2 and is a direct application of the page-fault "
    "machinery from CSCE 614 Module 07."]),

  ("h1", "5 &nbsp; What a switch really costs"),
  ("table", ["Cost", "Typical magnitude", "Cause"],
   [["<b>Direct</b>", "1&ndash;2 &mu;s",
     "Saving and restoring registers, scheduler bookkeeping, the trap in and "
     "out."],
    ["<b>TLB</b>", "Hundreds of cycles, spread over the next millisecond",
     "Address space change invalidates translations; subsequent accesses pay "
     "page walks (CSCE 614 Module 07)."],
    ["<b>Cache</b>", "<b>Frequently the largest term</b>",
     "The incoming process's working set is not in L1 or L2. Every access "
     "misses until the cache refills, at ~250 cycles for a main-memory miss "
     "(CSCE 614 Module 05)."],
    ["<b>Branch predictor</b>", "Moderate",
     "Accumulated history now refers to different code (CSCE 614 Module "
     "04)."]],
   [0.17, 0.32, 0.51]),
  ("p", "The indirect costs typically exceed the direct cost by several "
        "times, and they are invisible in any measurement that only times the "
        "switch itself. This is the practical reason scheduling quanta are "
        "measured in milliseconds rather than microseconds: the switch must "
        "be amortised over enough useful work to be worth paying for. "
        "Module 03 builds on this directly."),
 ],
 "resources": [
   ("MIT 6.1810 — lectures and lab on scheduling / <code>swtch</code>",
    "https://pdos.csail.mit.edu/6.1810/",
    "The context switch traced through real code, with the two-switch design "
    "explained."),
   ("xv6 book — Chapter 7 (Scheduling)",
    "https://pdos.csail.mit.edu/6.1810/2023/xv6/book-riscv-rev3.pdf",
    "<code>swtch</code>, the scheduler loop, and the per-CPU scheduler "
    "context."),
   ("OSTEP — Chapters 4&ndash;6 (Processes, the Process API, Limited "
    "Direct Execution)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "The clearest written treatment of fork/exec and of why the API is shaped "
    "as it is."),
   ("Baumann, Appavoo, Krieger, Roscoe — A fork() in the road (free)",
    "https://www.microsoft.com/en-us/research/publication/a-fork-in-the-road/",
    "A serious argument that fork was a mistake. Read it after you have "
    "understood why it was a good idea — the disagreement is "
    "instructive."),
 ],
 "exercises": [
   "Read xv6's <code>swtch.S</code> and <code>scheduler()</code>. Set a GDB "
   "breakpoint in <code>swtch</code> and single-step across a switch, "
   "watching the stack pointer change process.",
   "Instrument xv6 to count context switches per process. Run a CPU-bound and "
   "an I/O-bound program together and compare their counts.",
   "Measure context switch cost on your own machine: ping-pong a byte through "
   "a pipe between two processes, and then between two threads. Explain the "
   "difference.",
   "Repeat the measurement with the two processes pinned to the same core and "
   "then to different cores. Explain both results in terms of cache "
   "behaviour.",
   "Write a program that forks a child with a 100 MB heap and measures "
   "resident memory before and after. Then have the child write to every "
   "page and measure again. Explain the numbers using copy-on-write.",
   "Implement a simple user-level thread library: a context structure, a "
   "switch routine, and a round-robin scheduler. Demonstrate that one "
   "blocking <code>read()</code> stalls all of your threads.",
   "Create a zombie process deliberately and observe it with <code>ps</code>. "
   "Then kill the parent and watch init reap it.",
 ],
 "selfcheck": [
   "List six things the kernel must store per process, and say why the "
   "per-process kernel stack is necessary.",
   "Why does a zombie exist, and when does an accumulation of them indicate a "
   "bug?",
   "Why does <code>swtch</code> save only callee-saved registers?",
   "Why does xv6 switch via the scheduler rather than directly from process "
   "to process?",
   "Give the quantitative reason a thread switch is cheaper than a process "
   "switch.",
   "Why are fork and exec separate calls? Give a concrete thing the gap "
   "between them is used for.",
   "Explain copy-on-write fork and say which earlier module's mechanism it "
   "depends on.",
   "Which cost of a context switch is usually largest, and why is it "
   "invisible to naive measurement?",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c611_b2", "c611_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
