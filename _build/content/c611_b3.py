# -*- coding: utf-8 -*-
"""CSCE 611 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "File Systems",
 "subtitle": "Turning a block device into names, directories, and bytes.",
 "question": "How do you store a growing file on fixed-size blocks?",
 "outcomes": [
     "Explain inodes and the separation of names from files.",
     "Compare block allocation strategies and their costs.",
     "Explain how directories and path resolution work.",
     "Explain hard links, symlinks, and why unlink is named as it is.",
     "Explain the buffer cache and why fsync exists.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The layers",
   "blurb": "From a flat array of blocks to a named hierarchy."},

  {"t": "table", "kicker": "Layers", "title": "What each layer provides",
   "header": ["Layer", "Turns", "Into"],
   "widths": [2.8, 4.4, 4.9],
   "rows": [
     ["Disk", "—", "An array of fixed-size blocks"],
     ["Buffer cache", "Blocks", "Cached blocks; write buffering"],
     ["Inode layer", "Blocks", "A growable byte array with metadata"],
     ["Directory layer", "Inodes", "Names mapped to inode numbers"],
     ["Path layer", "Names", "<code>/usr/bin/ls</code>"],
     ["File descriptor", "Inodes", "Open files with offsets"],
   ],
   "note": "Each layer is a small abstraction over the one below. xv6's file "
           "system is organised exactly this way and is readable in an hour."},

  {"t": "callout", "title": "An inode is the file. A name is not.",
   "kind": "The central separation",
   "body": ["A file's identity, metadata, and block pointers live in an "
            "<b>inode</b>, identified by number.",
            "A <b>directory</b> is just a file whose contents are (name, "
            "inode number) pairs.",
            "So a name is a <i>reference</i> to a file, not the file itself. "
            "One file can have many names — that is a hard link — "
            "and deleting a name does not delete the file.",
            "This separation explains hard links, why <code>unlink</code> is "
            "called unlink rather than delete, and why a running program "
            "survives having its executable removed."]},

  {"t": "section", "label": "Part 2", "title": "Block allocation",
   "blurb": "A file grows. Where do its blocks go?"},

  {"t": "table", "kicker": "Strategies", "title": "Three ways to find a file's blocks",
   "header": ["Scheme", "How", "Problem"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["Contiguous", "Start block + length", "<b>External fragmentation</b>; cannot grow"],
     ["Linked", "Each block points to the next", "Random access is O(n); one bad pointer loses the tail"],
     ["Indexed (inode)", "A table of block numbers", "<b>What everyone uses</b>"],
     ["Extents", "(start, length) runs", "Compact for large contiguous files"],
   ],
   "note": "FAT is linked-list allocation with the list pulled out into one "
           "table — which is why it must be kept in memory."},

  {"t": "code", "kicker": "Inode", "title": "Direct and indirect blocks",
   "lang": "text", "code": """
inode:
   metadata: type, size, link count, permissions, timestamps
   addrs[0..11]   -> 12 DIRECT block pointers
   addrs[12]      -> SINGLY indirect: a block full of pointers
   (ext2 adds doubly and triply indirect)

With 1 KB blocks and 4-byte pointers (256 pointers per block):

   direct         12 blocks        =  12 KB
   single ind.   256 blocks        = 256 KB
   double ind.   256*256           =  64 MB
   triple ind.   256*256*256       =  16 GB

Small files: all data reachable in ONE inode read.
Large files: more indirection, but still O(1) random access.
""",
   "caption": "The design optimises for the common case — most files are "
              "small — while still supporting very large ones.",
   "note": "The size table makes the design rationale obvious and is worth "
           "working through."},

  {"t": "section", "label": "Part 3", "title": "Names",
   "blurb": "Directories, links, and path resolution."},

  {"t": "code", "kicker": "Path resolution", "title": "Walking /usr/bin/ls",
   "lang": "text", "code": """
1. Start at the root inode (a known, fixed inode number).
2. Read the root directory. Search for "usr" -> inode 42.
3. Read inode 42. Confirm it is a directory. Read it.
4. Search for "bin" -> inode 87.
5. Read inode 87. Read it. Search for "ls" -> inode 1203.
6. Return inode 1203.

Every component costs at least one inode read and one data read.
Deep paths are expensive -- which is why kernels cache the
results in a DENTRY CACHE.
""",
   "caption": "Path resolution is a loop, and permission is checked at every "
              "component — you need execute permission on each directory "
              "along the way.",
   "note": "The per-component permission check is why 'x' on a directory "
           "means 'traverse', which confuses everyone once."},

  {"t": "two", "kicker": "Links", "title": "Hard and symbolic",
   "lh": "Hard link",
   "l": ["Another <b>name</b> for the same inode.",
         "Indistinguishable from the original — there is no original.",
         "Increments the inode's link count.",
         "Cannot cross file systems; cannot link directories.",
         ("The file vanishes when the count hits 0 <i>and</i> nothing has it "
          "open.", 1)],
   "rh": "Symbolic link",
   "r": ["A small file containing a <b>path</b>.",
         "Resolved at access time, every time.",
         "Can point anywhere — or nowhere.",
         "Crosses file systems; can point at directories.",
         ("Dangles if the target is removed.", 1)],
   "note": "The 'no original' point for hard links is the one that clarifies "
           "everything else about them."},

  {"t": "callout", "title": "Why it is called unlink",
   "kind": "The name is the explanation",
   "body": ["<code>unlink(path)</code> removes a <i>name</i>. It decrements "
            "the inode's link count.",
            "The file's blocks are freed only when the link count reaches "
            "zero <b>and</b> no process still has it open.",
            "Hence the classic Unix behaviour: delete a file that a running "
            "program has open, and the program keeps reading it happily. The "
            "space is reclaimed when the last descriptor closes.",
            "And the classic puzzle: a disk shows 100% full, "
            "<code>du</code> accounts for far less, and the space returns "
            "when you restart the process holding a deleted log file."]},

  {"t": "section", "label": "Part 4", "title": "The buffer cache",
   "blurb": "Why writes are fast and why that is dangerous."},

  {"t": "bullets", "kicker": "Buffer cache", "title": "What caching buys and costs",
   "items": [
     "Disk blocks are cached in memory. Reads hit; writes land in the cache "
     "and return.",
     "",
     "<b>Buys:</b> reads avoid the disk entirely; repeated writes to the same "
     "block collapse into one; writes can be reordered and batched for the "
     "device.",
     "",
     "<b>Costs:</b> <code>write()</code> returning means the data is in "
     "<b>memory</b>, not on disk.",
     ("A power failure loses it. Silently.", 1),
     "",
     "<code>fsync(fd)</code> forces it out and does not return until the "
     "device says so.",
   ],
   "note": "The write/fsync distinction is the single most consequential "
           "thing in this module."},

  {"t": "callout", "title": "write() does not mean written",
   "kind": "The expensive misunderstanding",
   "body": ["A successful <code>write()</code> guarantees the data is in the "
            "kernel's page cache. Nothing more.",
            "It may remain there for tens of seconds. A power loss, a kernel "
            "panic, or a yanked cable loses it, with no error reported to "
            "anyone.",
            "<code>fsync()</code> is the only guarantee — and it is "
            "slow, because it must actually reach durable media.",
            "<b>And it is not enough on its own:</b> creating a file requires "
            "fsyncing the <i>directory</i> too, or the file may exist with no "
            "name after a crash. Module 09 develops this."]},

  {"t": "table", "kicker": "Practice", "title": "Durability costs what it costs",
   "header": ["Operation", "Latency", "Guarantee"],
   "widths": [3.6, 3.4, 5.1],
   "rows": [
     ["write() to page cache", "~1 μs", "<b>None</b> — memory only"],
     ["fsync() to SSD", "~100 μs – 1 ms", "On durable media"],
     ["fsync() to spinning disk", "~5–10 ms", "On durable media"],
     ["fsync() with write cache lied to", "Fast", "<b>None</b> — the device lied"],
   ],
   "footnote": "Some consumer drives report completion before data is "
               "durable. This is a real and documented problem.",
   "note": "The last row explains a lot of 'impossible' corruption reports."},
 ],
 "takeaways": [
   "An inode is the file; a name is a reference to it. That separation "
   "explains links, unlink, and open-but-deleted files.",
   "A directory is a file containing (name, inode) pairs. Path resolution is "
   "a loop with a permission check per component.",
   "Indexed allocation with direct and indirect blocks optimises for small "
   "files while supporting very large ones.",
   "A hard link is another name for the same inode — there is no "
   "original. A symlink is a path, resolved on every access.",
   "<code>write()</code> means 'in memory'. Only <code>fsync()</code> means "
   "'on disk', and it is three orders of magnitude slower.",
   "Creating a file durably requires fsyncing the directory as well as the "
   "file.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The layered structure"),
  ("p", "A disk presents a flat array of numbered fixed-size blocks. A file "
        "system builds, in layers, the illusion of named growable byte "
        "arrays arranged in a hierarchy."),
  ("table", ["Layer", "Input", "Output"],
   [["Block device", "—", "An array of 512- or 4096-byte blocks."],
    ["Buffer cache", "Blocks", "Cached blocks; write buffering and "
     "reordering."],
    ["Inode layer", "Blocks", "A growable byte array with metadata."],
    ["Directory layer", "Inodes", "A mapping from names to inode numbers."],
    ["Path layer", "Directories", "Hierarchical path resolution."],
    ["Descriptor layer", "Inodes", "Open files with per-descriptor offsets, "
     "shared across fork and dup."]],
   [0.22, 0.23, 0.55]),
  ("callout", "The inode is the file; the name is not",
   ["A file's metadata and block pointers live in an <b>inode</b>, identified "
    "by a number. A <b>directory</b> is simply a file whose contents are "
    "(name, inode number) pairs.",
    "So a filename is a <i>reference</i> to a file rather than the file "
    "itself. One file may have several names, and removing a name does not "
    "necessarily remove the file.",
    "Once this separation is clear, three otherwise confusing behaviours "
    "become obvious: hard links, the fact that the deletion call is named "
    "<code>unlink</code>, and a running program continuing to work after its "
    "executable is deleted."]),

  ("h1", "2 &nbsp; Finding a file's blocks"),
  ("table", ["Scheme", "Representation", "Problem"],
   [["<b>Contiguous</b>", "Start block and length.",
     "Reading is maximally efficient. The file cannot grow without moving, "
     "and the free space fragments externally — exactly the Module 06 "
     "problem."],
    ["<b>Linked</b>", "Each block stores the number of the next.",
     "Growth is free; random access is O(n), and losing one pointer loses the "
     "entire remainder of the file."],
    ["<b>File allocation table</b>", "The links extracted into one array.",
     "FAT. Random access improves if the table is in memory, which means the "
     "whole table must be, and it scales poorly."],
    ["<b>Indexed (inode)</b>", "A table of block numbers per file.",
     "<b>What essentially everything uses.</b> O(1) random access and free "
     "growth."],
    ["<b>Extents</b>", "(start, length) runs instead of individual blocks.",
     "Far more compact for large, contiguously allocated files. Used by ext4, "
     "XFS, NTFS, APFS."]],
   [0.18, 0.28, 0.54]),
  ("h2", "2.1 &nbsp; Direct and indirect blocks"),
  ("code", """inode:
    type, size, link count, permissions, timestamps
    addrs[0..11]    -> 12 direct block pointers
    addrs[12]       -> singly indirect (a block of pointers)
    [ext2 also: doubly indirect, triply indirect]

With 1 KB blocks and 4-byte pointers (256 pointers per block):

    direct            12 blocks  =   12 KB
    singly indirect  256 blocks  =  256 KB
    doubly indirect  256 x 256   =   64 MB
    triply indirect  256^3       =   16 GB"""),
  ("p", "The design is a deliberate optimisation for the observed "
        "distribution of file sizes. Most files are small, and for those "
        "every data block is reachable directly from the inode — one "
        "inode read and then the data. Large files pay additional "
        "indirection, but random access remains O(1) with a bounded small "
        "constant."),
  ("p", "Modern file systems prefer <b>extents</b>, which record runs of "
        "contiguous blocks rather than individual numbers. A 1 GB "
        "contiguously allocated file needs one extent rather than a quarter "
        "of a million pointers, which also makes the metadata itself "
        "cache-friendly."),

  ("h1", "3 &nbsp; Names and directories"),
  ("code", """Resolving /usr/bin/ls:

1. Begin at the root inode (a fixed, known inode number).
2. Read the root directory's data; search for "usr"  -> inode 42.
3. Read inode 42; verify it is a directory; read its data.
4. Search for "bin"                                  -> inode 87.
5. Read inode 87; read its data; search for "ls"     -> inode 1203.
6. Return inode 1203."""),
  ("p", "Every path component costs at least one inode read and one data "
        "block read, and a permission check. Deep paths are therefore "
        "genuinely expensive, which is why kernels maintain a <b>dentry "
        "cache</b> mapping recently resolved (directory, name) pairs straight "
        "to inodes."),
  ("p", "Note that the permission checked at each component is <b>execute</b> "
        "on the directory, which for a directory means 'may traverse'. This "
        "is why a directory can be traversable but not listable "
        "(<code>--x</code>): you can open a file inside it if you know the "
        "name, and you cannot enumerate the contents."),
  ("h2", "3.1 &nbsp; Hard links and symbolic links"),
  ("table", ["", "Hard link", "Symbolic link"],
   [["What it is", "An additional directory entry pointing at the same "
     "inode.", "A small file whose contents are a path string."],
    ["Resolution", "None needed — it <i>is</i> the inode number.",
     "The path is resolved on every access."],
    ["Original vs copy", "<b>There is no original.</b> All names are equal.",
     "There is a clear target, which may not exist."],
    ["Link count", "Incremented in the inode.", "Not affected."],
    ["Restrictions", "Cannot cross file systems (inode numbers are per-"
     "filesystem); cannot link directories (would permit cycles).",
     "No restrictions. May point anywhere, including nowhere."],
    ["If the target goes", "Nothing happens — the file survives while "
     "any name remains.", "The link dangles."]],
   [0.16, 0.42, 0.42]),
  ("callout", "Why the system call is called unlink",
   ["<code>unlink(path)</code> removes a <i>name</i> and decrements the "
    "inode's link count. It does not necessarily delete anything.",
    "The file's blocks are released only when the link count reaches zero "
    "<b>and</b> no process holds it open. The kernel tracks both.",
    "This produces two familiar behaviours. First, deleting a file that a "
    "running program has open is harmless — the program continues "
    "reading it, and the space is reclaimed when the last descriptor closes. "
    "Programs exploit this deliberately for temporary files: create, unlink "
    "immediately, and the file is guaranteed to vanish when the process "
    "exits however it exits.",
    "Second, the classic operations puzzle: <code>df</code> reports the disk "
    "full, <code>du</code> accounts for far less, and the space reappears "
    "when a process is restarted — because it was holding a deleted log "
    "file open."]),

  ("break",),
  ("h1", "4 &nbsp; The buffer cache"),
  ("p", "Disk blocks are cached in memory. Reads check the cache first; "
        "writes modify the cached copy and return immediately, with the "
        "actual device write deferred."),
  ("table", ["Benefit", "Mechanism"],
   [["Reads avoid the device entirely.", "Cache hits on recently used "
     "blocks — locality applies here exactly as in CSCE 614 Module 05."],
    ["Repeated writes collapse.", "Ten writes to the same block within a "
     "second become one device write."],
    ["Writes are batched and reordered.", "The kernel can issue them in an "
     "order that suits the device — historically elevator ordering for "
     "seek time, now mostly queue depth management for SSDs."],
    ["Read-ahead.", "Sequential access is detected and subsequent blocks are "
     "fetched before they are requested."]],
   [0.30, 0.70]),
  ("callout", "<code>write()</code> does not mean written",
   ["A successful <code>write()</code> guarantees that the data is in the "
    "kernel's page cache. It guarantees nothing about durable storage.",
    "The data may sit there for tens of seconds. A power failure, kernel "
    "panic, or disconnected cable loses it, and <i>no error is reported to "
    "anybody</i> — the write already returned success.",
    "<code>fsync(fd)</code> forces the file's data to durable media and does "
    "not return until the device reports completion. It is the only "
    "guarantee available, and it is roughly a thousand times slower than a "
    "cached write.",
    "<b>And it is not sufficient by itself.</b> Creating a file involves "
    "writing the file's data <i>and</i> adding its name to a directory. "
    "<code>fsync</code> on the file does not flush the directory, so after a "
    "crash the file's blocks can exist with no name referring to them. "
    "Durably creating a file means fsyncing the file and then the containing "
    "directory. Module 09 develops why this ordering matters."]),
  ("table", ["Operation", "Typical latency", "What is guaranteed"],
   [["<code>write()</code> into the page cache", "~1 &mu;s",
     "<b>Nothing durable.</b> The data is in volatile memory."],
    ["<code>fsync()</code> to an SSD", "100 &mu;s &ndash; 1 ms",
     "Data has reached the device's durable storage."],
    ["<code>fsync()</code> to a rotating disk", "5&ndash;10 ms",
     "As above, after a seek and a rotation."],
    ["<code>fsync()</code> to a device with a lying write cache", "Fast",
     "<b>Nothing.</b> Some consumer drives acknowledge before data is "
     "durable. This is documented, real, and the cause of a great deal of "
     "'impossible' corruption."]],
   [0.30, 0.22, 0.48]),
  ("p", "The three-orders-of-magnitude gap between a cached write and a "
        "durable one is why databases and file systems work so hard to "
        "minimise synchronous writes, and why the next module exists."),
 ],
 "resources": [
   ("OSTEP — Chapters 39&ndash;41 (Files and Directories, File System "
    "Implementation, FFS)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "Inodes, directories, and allocation, with the Fast File System's "
    "locality arguments."),
   ("xv6 book — Chapter 8 (File system)",
    "https://pdos.csail.mit.edu/6.1810/2023/xv6/book-riscv-rev3.pdf",
    "A complete, readable file system in about a thousand lines, organised "
    "in exactly the layers of &sect;1."),
   ("MIT 6.1810 — file system lectures and lab",
    "https://pdos.csail.mit.edu/6.1810/",
    "Including the lab that adds large files and symbolic links."),
   ("Linux Documentation — ext4 and VFS",
    "https://docs.kernel.org/filesystems/",
    "How extents, delayed allocation, and the virtual file system layer work "
    "in production."),
 ],
 "exercises": [
   "Read xv6's <code>fs.c</code> and map each function to a layer in "
   "&sect;1's table.",
   "Add doubly indirect blocks to xv6's inode and verify you can create a "
   "file larger than the previous maximum.",
   "Implement symbolic links in xv6, including loop detection for a symlink "
   "chain that points to itself.",
   "Create a hard link to a file, modify through one name, and read through "
   "the other. Then remove one name and confirm the data survives. Report the "
   "link count at each step.",
   "Open a file, unlink it while keeping the descriptor, write to it, and "
   "read it back. Check <code>df</code> and <code>du</code> while the "
   "descriptor is open, then close it and check again.",
   "Measure the cost of durability: time ten thousand <code>write()</code> "
   "calls, then ten thousand <code>write()</code> + <code>fsync()</code> "
   "pairs. Report the ratio.",
   "Write a program that creates a file and fsyncs only the file. Crash the "
   "machine (or use a VM snapshot) and determine whether the file exists "
   "afterwards. Then fsync the directory too and repeat.",
   "Instrument path resolution in xv6 to count block reads for "
   "<code>/a/b/c/d/e</code>. Explain the number.",
 ],
 "selfcheck": [
   "What is an inode, and in what sense is a filename not the file?",
   "Compare contiguous, linked, and indexed allocation, giving the specific "
   "failure of each of the first two.",
   "Why does an inode have both direct and indirect block pointers?",
   "Describe path resolution and say which permission is checked at each "
   "component.",
   "Distinguish hard and symbolic links, and explain why hard links cannot "
   "cross file systems.",
   "Why is the call named <code>unlink</code>, and what two conditions must "
   "hold before blocks are freed?",
   "What exactly does a successful <code>write()</code> guarantee, and what "
   "must you do for durability?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Crash Consistency",
 "subtitle": "Surviving a power failure in the middle of an update.",
 "question": "How do you make a multi-block update atomic on a device with "
             "no transactions?",
 "outcomes": [
     "Explain why a crash mid-update corrupts a file system.",
     "Explain fsck and why it is inadequate.",
     "Explain write-ahead logging and why ordering is everything.",
     "Compare journaling modes and their guarantees.",
     "Explain copy-on-write file systems as an alternative.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "One logical operation, several physical writes."},

  {"t": "code", "kicker": "The problem", "title": "Appending a block requires three writes",
   "lang": "text", "code": """
To append one block to a file, the kernel must:

    1. mark the block as used in the free bitmap
    2. add the block's number to the inode
    3. write the data into the block

A crash between any two of these leaves the file system
INCONSISTENT:

  crash after 1      -> block marked used, referenced by nobody
                        (a leak -- wasteful, not dangerous)

  crash after 2      -> inode points at a block the bitmap says
                        is FREE. It will be handed to another file.
                        (two files sharing a block -- CORRUPTION)

  crash after 1,2    -> inode points at a block containing
                        whatever was there before
                        (garbage in the file, or ANOTHER FILE'S DATA)
""",
   "caption": "The disk provides atomicity for a single sector and nothing "
              "more. Multi-block updates have no atomicity at all.",
   "note": "The 'another file's data' case is the one that makes this a "
           "security problem, not just a reliability one."},

  {"t": "callout", "title": "The device gives you one guarantee",
   "kind": "What you have to work with",
   "body": ["A single sector write is atomic: it either happens completely or "
            "not at all. That is essentially the only guarantee.",
            "Writes may be <b>reordered</b> by the device's queue. Issuing A "
            "then B does not mean A lands first.",
            "Write caches may acknowledge before the data is durable.",
            "So building a multi-block atomic update means constructing "
            "atomicity from a single-sector primitive plus explicit ordering "
            "barriers. That is what journaling does."]},

  {"t": "section", "label": "Part 2", "title": "fsck, and why it is not enough",
   "blurb": "Repair after the fact."},

  {"t": "bullets", "kicker": "fsck", "title": "Scan everything and fix what you can",
   "items": [
     "Walk the entire file system. Rebuild the free bitmap from the inodes. "
     "Fix link counts. Reconnect orphans to <code>lost+found</code>.",
     "",
     "<b>Problem 1: it is slow.</b> Time proportional to the size of the file "
     "system, not to the work in progress. Hours for a large volume.",
     "",
     "<b>Problem 2: it restores <i>consistency</i>, not <i>correctness</i>.</b>",
     ("It can tell that an inode points at a block the bitmap calls free. It "
      "cannot tell which was right.", 1),
     ("Your data may be gone; the file system is merely self-consistent "
      "again.", 1),
   ],
   "note": "The consistency-vs-correctness distinction is the key insight and "
           "motivates everything after it."},

  {"t": "section", "label": "Part 3", "title": "Journaling",
   "blurb": "Write what you intend to do, then do it."},

  {"t": "code", "kicker": "Write-ahead logging", "title": "The protocol",
   "lang": "text", "code": """
To perform a multi-block update atomically:

  1. Write all the new block contents to the LOG.
  2. BARRIER -- wait for those writes to be durable.
  3. Write a COMMIT record to the log.
  4. BARRIER.
  5. Write the blocks to their real locations ("checkpointing").
  6. Mark the log entry free.

RECOVERY after a crash: scan the log.
  - transaction has a commit record -> REPLAY it (idempotent)
  - no commit record                -> DISCARD it

The commit record is a SINGLE SECTOR, so it is atomic. That one
atomic write is what makes the whole multi-block update atomic.
""",
   "caption": "Everything rests on the commit record being one sector. Before "
              "it lands the transaction never happened; after, it definitely "
              "did.",
   "note": "This is the central idea and it recurs in databases, in "
           "distributed consensus, and in version control."},

  {"t": "callout", "title": "The barriers are the whole thing",
   "kind": "Why ordering matters more than the log",
   "body": ["If the commit record reaches disk <i>before</i> the data it "
            "commits, a crash in between leaves a log entry that claims to "
            "describe data that is not there. Recovery replays garbage.",
            "Devices reorder writes freely. Issuing them in the right order "
            "is not enough — you must <b>wait</b>.",
            "Hence step 2: the data must be durable before the commit record "
            "is even issued. This is why journaling is slow, and why the cost "
            "is unavoidable.",
            "File systems that skipped the barrier for performance lost data, "
            "repeatedly and publicly, through the 2000s. The ordering is not "
            "optional."]},

  {"t": "table", "kicker": "Modes", "title": "Journaling modes, and what each promises",
   "header": ["Mode", "Journals", "Guarantee", "Cost"],
   "widths": [2.4, 3.0, 3.6, 3.1],
   "rows": [
     ["Data", "Metadata and data", "<b>Full</b> — no garbage, no loss", "Everything written twice"],
     ["Ordered", "Metadata; data written first", "Metadata consistent; no stale data exposed", "Default in ext4"],
     ["Writeback", "Metadata only", "Metadata consistent; <b>may expose stale data</b>", "Fastest"],
   ],
   "footnote": "Ordered mode is the default because writeback's exposure of "
               "old data is a security problem.",
   "note": "The writeback data-exposure issue is concrete: a newly created "
           "file can contain another user's deleted content."},

  {"t": "section", "label": "Part 4", "title": "The alternative",
   "blurb": "Never overwrite anything."},

  {"t": "bullets", "kicker": "Copy-on-write", "title": "Shadow paging",
   "items": [
     "<b>Never modify a block in place.</b> Write a new copy elsewhere.",
     "",
     "That means the parent pointing at it must also be rewritten — and "
     "so on, up to the root.",
     "",
     "Finally, one atomic write switches the <b>root pointer</b> to the new "
     "tree.",
     "",
     "Before: the old tree. After: the new one. There is no in-between state "
     "to be caught in.",
     "",
     "<b>Free:</b> snapshots. Keep the old root and you have a consistent "
     "point-in-time view.",
   ],
   "note": "Snapshots falling out for free is the selling point and explains "
           "why ZFS and btrfs are built this way."},

  {"t": "table", "kicker": "Compare", "title": "Journaling and copy-on-write",
   "header": ["", "Journaling", "Copy-on-write"],
   "widths": [2.6, 4.8, 4.7],
   "rows": [
     ["Writes data", "Twice (data mode) or once", "Once, to a new location"],
     ["Layout", "Preserved", "<b>Fragments</b> over time"],
     ["Snapshots", "Bolted on", "<b>Intrinsic</b>"],
     ["Recovery", "Replay the log", "Nothing to do — the root is valid"],
     ["Examples", "ext4, XFS, NTFS", "ZFS, btrfs, APFS, WAFL"],
   ],
   "note": "CoW fragmentation is real and is why ZFS performance degrades on "
           "nearly-full pools."},

  {"t": "callout", "title": "This idea is everywhere",
   "kind": "Beyond file systems",
   "body": ["<b>Databases</b> use write-ahead logging for exactly this "
            "reason, and the recovery protocol is the same.",
            "<b>Distributed consensus</b> — Raft, Paxos — is a "
            "replicated log with a commit point.",
            "<b>Git</b> is copy-on-write: objects are immutable and a commit "
            "is an atomic pointer update.",
            "<b>Copy-on-write fork</b> (Module 02) is the same idea applied "
            "to memory.",
            "Write the intent, make it durable, then make it visible with one "
            "atomic step. It is one of the genuinely general ideas in "
            "systems."]},
 ],
 "takeaways": [
   "One logical file operation is several physical writes, and a crash "
   "between them corrupts the file system — sometimes exposing another "
   "file's data.",
   "The device gives you one atomic sector write and reorders everything "
   "else. Atomicity must be constructed from that.",
   "fsck restores <i>consistency</i>, not correctness, and takes time "
   "proportional to the volume rather than the work in flight.",
   "Write-ahead logging: log the intent, barrier, commit record, barrier, "
   "then checkpoint. Replay committed transactions on recovery.",
   "The barriers are the mechanism. Without them the commit record can "
   "overtake the data it commits, and recovery replays garbage.",
   "Copy-on-write never overwrites: build a new tree and flip the root "
   "atomically. Snapshots come free; fragmentation is the cost.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why a crash corrupts"),
  ("p", "A single logical operation — appending a block to a file "
        "— requires several physical writes that must all happen or "
        "none."),
  ("code", """Appending one block requires:
    1. mark the block allocated in the free bitmap
    2. record the block number in the inode
    3. write the data into the block itself"""),
  ("table", ["Crash after", "State", "Severity"],
   [["step 1 only", "A block is marked used and referenced by nothing.",
     "A <b>leak</b>. Space is wasted until fsck reclaims it. Annoying, not "
     "dangerous."],
    ["step 2 only", "The inode references a block that the bitmap says is "
     "free. That block will eventually be allocated to another file.",
     "<b>Corruption.</b> Two files sharing one block; writes through one "
     "appear in the other."],
    ["steps 1 and 2", "The inode references an allocated block containing "
     "whatever was there previously.",
     "<b>Security failure.</b> The file now contains the previous contents of "
     "that block — possibly another user's deleted data."]],
   [0.17, 0.41, 0.42]),
  ("callout", "The only primitive you have",
   ["A single sector write is atomic: it completes entirely or not at all. "
    "The device guarantees that much and very little else.",
    "<b>Writes are reordered.</b> Issuing A then B does not mean A reaches "
    "durable storage first; the device's queue may reorder freely for "
    "performance.",
    "<b>Write caches may lie.</b> Some devices acknowledge a write before it "
    "is durable.",
    "So the engineering problem is to build a multi-block atomic update out "
    "of one atomic sector write plus explicit ordering barriers. Everything "
    "in this module is a way of doing that."]),

  ("h1", "2 &nbsp; fsck and its limits"),
  ("p", "The historical approach was to repair afterwards. On boot, "
        "<code>fsck</code> walks the entire file system, rebuilds the free "
        "bitmap from what the inodes actually reference, corrects link "
        "counts, and attaches unreferenced inodes to "
        "<code>lost+found</code>."),
  ("ul", ["<b>It is slow.</b> The time is proportional to the size of the "
          "file system, not to the amount of work that was in progress when "
          "the crash occurred. A large volume takes hours, during which the "
          "system is unavailable — which became untenable as disks grew.",
          "<b>It restores consistency, not correctness.</b> This is the "
          "deeper problem."]),
  ("callout", "Consistency is not correctness",
   ["<code>fsck</code> can detect that an inode references a block the bitmap "
    "marks free. It cannot determine which of the two is right, because that "
    "information was never written down.",
    "It will choose one — typically trusting the inode and marking the "
    "block used — and produce a file system that is internally "
    "consistent. Whether it contains your data is a separate question it "
    "cannot answer.",
    "A file system that passes fsck is one where the metadata agrees with "
    "itself. That is a much weaker property than 'your data is intact', and "
    "conflating the two has caused a great deal of misplaced confidence."]),

  ("h1", "3 &nbsp; Write-ahead logging"),
  ("p", "The insight is to record <i>what you are about to do</i> somewhere "
        "safe before doing it, so that after a crash you can either complete "
        "or abandon the operation, but never be caught halfway."),
  ("code", """1. Write all new block contents to the LOG.
2. BARRIER -- wait until those writes are durable.
3. Write a single-sector COMMIT record.
4. BARRIER.
5. Write the blocks to their real locations (checkpoint).
6. Mark the log entry free.

RECOVERY: scan the log.
    committed transactions  -> replay (idempotent)
    uncommitted             -> discard"""),
  ("callout", "One atomic sector makes a multi-block update atomic",
   ["The commit record is a single sector, so writing it is atomic: it is "
    "either there or it is not.",
    "Before the commit record lands, recovery discards the transaction and "
    "the file system is exactly as it was. After it lands, recovery replays "
    "the transaction and the file system is exactly as if the operation had "
    "completed. There is no third state.",
    "Replay must be <b>idempotent</b> — a crash during recovery must be "
    "survivable — which it is, because replay simply writes known block "
    "contents to known locations."]),
  ("callout", "The barriers are the mechanism, not an optimisation detail",
   ["Suppose the commit record reached durable storage before the logged data "
    "it describes. A crash in between leaves a committed transaction whose "
    "data is absent, and recovery faithfully replays garbage into the file "
    "system — worse than having done nothing.",
    "Because devices reorder, issuing the writes in order is insufficient. "
    "The file system must <b>wait</b> for the data to be durable before even "
    "issuing the commit. That is step 2, and it is where journaling's cost "
    "lies.",
    "Through the 2000s, several file systems and drive firmwares omitted or "
    "weakened these barriers for benchmark performance, and lost user data as "
    "a direct result. The ordering requirement is not negotiable, and "
    "'faster' implementations that drop it are simply incorrect."]),
  ("h2", "3.1 &nbsp; Modes"),
  ("table", ["Mode", "What is journaled", "Guarantee", "Cost"],
   [["<b>Data</b>", "Metadata and file data.",
     "Full: after recovery, metadata is consistent and data is either the old "
     "version or the new one.",
     "All data written twice. Roughly halves write throughput."],
    ["<b>Ordered</b>", "Metadata only, but data blocks are forced to disk "
     "<i>before</i> the metadata that references them is committed.",
     "Metadata consistent, and a file never references a block containing "
     "stale contents.",
     "Moderate. The default in ext4 for good reason."],
    ["<b>Writeback</b>", "Metadata only, with no ordering constraint on data.",
     "Metadata consistent. A file may reference blocks whose contents were "
     "never written — <b>exposing whatever was there before</b>.",
     "Fastest, and a security hazard."]],
   [0.14, 0.32, 0.34, 0.20]),
  ("p", "Writeback mode's failure is concrete: after a crash, a newly "
        "extended file can contain the previous contents of its blocks "
        "— potentially another user's deleted data. That is why ordered "
        "mode is the default despite being slower."),

  ("break",),
  ("h1", "4 &nbsp; Copy-on-write file systems"),
  ("p", "A different answer: never overwrite a live block at all."),
  ("ol", ["To modify a block, write a <b>new copy</b> at a free location.",
          "The parent block that pointed at it must now be updated — so "
          "write a new copy of the parent too.",
          "This propagates up the tree to the root.",
          "Finally, one atomic single-sector write switches the <b>root "
          "pointer</b> to the new tree."]),
  ("callout", "There is no intermediate state",
   ["Before the root pointer is updated, the entire old tree is intact and "
    "valid. After, the entire new tree is intact and valid. A crash at any "
    "moment leaves one or the other.",
    "Recovery is therefore trivial: there is nothing to do. The root pointer "
    "either references the old tree or the new one, and both are consistent.",
    "<b>Snapshots come free.</b> Retain an old root pointer and you have a "
    "complete, consistent, read-only view of the file system as it was at "
    "that instant, sharing all unmodified blocks with the present. This is "
    "why ZFS, btrfs, and APFS make snapshots nearly costless while ext4 has "
    "to construct them with separate machinery."]),
  ("table", ["", "Journaling", "Copy-on-write"],
   [["Data written", "Twice in data mode; once in ordered mode.",
     "Once, to a new location."],
    ["Layout over time", "Preserved — blocks stay where they were.",
     "<b>Fragments.</b> Repeated small updates scatter a file, and "
     "performance degrades as the pool fills."],
    ["Snapshots", "Require separate machinery (LVM, device mapper).",
     "<b>Intrinsic</b> and nearly free."],
    ["Recovery", "Scan and replay the log.",
     "Nothing to do; the root pointer is always valid."],
    ["Checksums", "Usually metadata only.",
     "Typically end-to-end on data as well, detecting silent corruption."],
    ["Examples", "ext4, XFS, NTFS, JFS.", "ZFS, btrfs, APFS, NetApp WAFL."]],
   [0.16, 0.42, 0.42]),

  ("h1", "5 &nbsp; The idea generalises"),
  ("callout", "Log-then-commit is one of the few genuinely general ideas",
   ["<b>Databases</b> use write-ahead logging for transaction durability, "
    "with the same protocol and the same recovery procedure. The ARIES "
    "algorithm is this module, elaborated.",
    "<b>Distributed consensus</b> — Raft and Paxos — is a "
    "replicated log with an agreed commit point. 'Committed' means the same "
    "thing: the point after which the operation definitely happened.",
    "<b>Git</b> is a copy-on-write store. Objects are immutable, and a commit "
    "is an atomic update of a reference to point at a new tree — "
    "structurally identical to &sect;4.",
    "<b>Copy-on-write <code>fork</code></b> (Module 02) is the same idea "
    "applied to memory pages.",
    "The pattern is: <i>write the intent somewhere durable, then make it "
    "visible with a single atomic step</i>. Recognising it is worth more than "
    "any one of the instances."]),
 ],
 "resources": [
   ("OSTEP — Chapter 42 (Crash Consistency: FSCK and Journaling)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "The clearest written treatment, including the three-write example and "
    "the journaling modes."),
   ("xv6 book — Chapter 8, logging section",
    "https://pdos.csail.mit.edu/6.1810/2023/xv6/book-riscv-rev3.pdf",
    "A complete, working journaling layer in a few hundred lines. Read it "
    "before implementing your own."),
   ("Rosenblum & Ousterhout — The Design and Implementation of a "
    "Log-Structured File System (free)",
    "https://people.eecs.berkeley.edu/~brewer/cs262/LFS.pdf",
    "The log-structured approach, which treats the whole disk as a log. "
    "Influential well beyond file systems."),
   ("Bonwick & Moore — ZFS: The Last Word in File Systems (free slides)",
    "https://www.cs.hmc.edu/~rhodes/courses/cs134/fa20/readings/zfs_last.pdf",
    "Copy-on-write, end-to-end checksums, and snapshots from the designers."),
 ],
 "exercises": [
   "Read xv6's <code>log.c</code>. Identify the commit point and the two "
   "barriers, and explain what each protects against.",
   "Build a crash-injection harness: run a file system operation in QEMU and "
   "kill the emulator at a randomly chosen point. Verify consistency "
   "afterwards.",
   "Disable xv6's logging and run your crash injector a hundred times. "
   "Classify the resulting corruptions against the three cases in &sect;1.",
   "Restore logging and repeat. Report how many runs required recovery and "
   "how many left the file system inconsistent.",
   "Deliberately reorder the commit record before the data writes and "
   "demonstrate that recovery now replays garbage.",
   "Measure the cost of journaling: time a workload with logging enabled and "
   "disabled, and report the overhead.",
   "Implement a trivial copy-on-write store: a tree of immutable blocks with "
   "an atomic root pointer. Demonstrate that a crash mid-update leaves either "
   "the old or the new tree, and implement snapshots by keeping old roots.",
 ],
 "selfcheck": [
   "Give the three physical writes needed to append a block and the "
   "consequence of crashing after each.",
   "What is the only atomicity guarantee a disk provides, and what else does "
   "it <i>not</i> guarantee?",
   "Why is fsck inadequate, in two distinct respects?",
   "State the write-ahead logging protocol, including both barriers.",
   "Why must the commit record be a single sector?",
   "Give the three journaling modes with the guarantee and cost of each, and "
   "explain writeback's security problem.",
   "How does copy-on-write avoid needing recovery at all, and what does it "
   "cost?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "I/O and Device Drivers",
 "subtitle": "Talking to hardware that is slow, asynchronous, and hostile.",
 "question": "How does a kernel manage devices a million times slower than "
             "itself?",
 "outcomes": [
     "Explain memory-mapped I/O and port I/O.",
     "Compare polling and interrupts and say when each is right.",
     "Explain DMA and why it matters.",
     "Explain the top-half/bottom-half split in interrupt handling.",
     "Explain the block layer and I/O scheduling.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Talking to a device",
   "blurb": "Registers that are not memory."},

  {"t": "two", "kicker": "Two mechanisms", "title": "How the CPU reaches a device",
   "lh": "Memory-mapped I/O",
   "l": ["Device registers appear at physical addresses.",
         "Read and write them with ordinary loads and stores.",
         "<b>Must be marked uncacheable</b> — or the cache will serve "
         "stale values and swallow writes.",
         ("Also needs <code>volatile</code> and barriers.", 1),
         "What everything modern uses."],
   "rh": "Port I/O",
   "r": ["A separate address space with dedicated instructions.",
         "<code>in</code> and <code>out</code> on x86.",
         "No cache interaction by construction.",
         ("Legacy; x86 only.", 1),
         "Still used for a few ancient devices."],
   "note": "The uncacheable requirement is a real bug source: a driver that "
           "works and then fails after a cache config change."},

  {"t": "callout", "title": "Device registers are not memory",
   "kind": "The trap",
   "body": ["Reading a status register can have <b>side effects</b> — it "
            "may clear an interrupt, or pop a value from a FIFO.",
            "Writing the same value twice is not the same as writing it once.",
            "So the compiler must not cache the value in a register, must not "
            "reorder accesses, and must not eliminate 'redundant' reads. That "
            "is what <code>volatile</code> is actually for — "
            "<i>this</i>, not thread synchronisation (CSCE 614 Module 12).",
            "And the processor must not reorder either, which needs explicit "
            "memory barriers."]},

  {"t": "section", "label": "Part 2", "title": "Knowing when the device is ready",
   "blurb": "Ask repeatedly, or be told."},

  {"t": "table", "kicker": "Notification", "title": "Polling and interrupts",
   "header": ["", "Polling", "Interrupts"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Mechanism", "Read a status register in a loop", "The device raises a signal"],
     ["CPU cost while waiting", "<b>100%</b>", "Zero"],
     ["Latency", "<b>Very low</b>", "Interrupt entry overhead"],
     ["Good for", "Fast devices; very high rates", "Slow or infrequent devices"],
     ["Example", "NVMe at high queue depth; NIC under load", "Keyboard, disk completion"],
   ],
   "note": "The modern twist: for very fast devices, polling wins again. "
           "NAPI and NVMe poll mode exist for exactly this."},

  {"t": "callout", "title": "At high rates, interrupts become the problem",
   "kind": "Interrupt livelock",
   "body": ["A network card at ten million packets per second generates ten "
            "million interrupts per second. Each costs context save, handler "
            "entry, and a cache disturbance.",
            "The system spends all its time entering and leaving interrupt "
            "handlers and never runs the code that would <i>process</i> the "
            "packets. Throughput collapses while the CPU is fully busy "
            "— this is <b>interrupt livelock</b>.",
            "<b>Fix:</b> on the first interrupt, <i>disable</i> interrupts "
            "for that device and switch to polling. Re-enable when the queue "
            "drains.",
            "Linux's NAPI does exactly this. Interrupts for low rates, "
            "polling for high — adaptively."]},

  {"t": "section", "label": "Part 3", "title": "DMA",
   "blurb": "Letting the device move the data."},

  {"t": "bullets", "kicker": "DMA", "title": "Why programmed I/O does not scale",
   "items": [
     "<b>Programmed I/O:</b> the CPU copies every byte between the device and "
     "memory.",
     ("A 1 GB/s device would consume a core entirely, doing nothing but "
      "copying.", 1),
     "",
     "<b>DMA:</b> give the device a buffer address and a length. It writes "
     "memory directly and interrupts when finished.",
     "",
     "The CPU is free during the transfer. This is why high-throughput I/O is "
     "possible at all.",
     "",
     "<b>Cost:</b> the device now writes memory behind the CPU's back.",
   ],
   "note": "The coherence consequence on the next slide is the part driver "
           "authors must get right."},

  {"t": "callout", "title": "DMA and cache coherence",
   "kind": "Where drivers go wrong",
   "body": ["The device writes physical memory directly. The CPU's cache does "
            "not know.",
            "<b>Before a device read:</b> flush the buffer from cache, or the "
            "device may read stale data that is still dirty in cache.",
            "<b>After a device write:</b> invalidate the buffer, or the CPU "
            "may read a stale cached copy instead of the new data.",
            "Many systems have <i>coherent</i> DMA where hardware handles "
            "this. Many embedded systems do not, and the resulting bugs are "
            "intermittent and look like corruption.",
            "An <b>IOMMU</b> adds address translation for devices, which also "
            "makes DMA safe to expose to a virtual machine."]},

  {"t": "section", "label": "Part 4", "title": "Interrupt handlers",
   "blurb": "Do the minimum now, the rest later."},

  {"t": "code", "kicker": "Top and bottom half", "title": "Splitting the work",
   "lang": "c", "code": """
// TOP HALF -- runs with interrupts disabled. Must be FAST.
void disk_intr(void) {
    ack_device();                // tell the device we heard it
    struct buf *b = dequeue_completed();
    b->flags |= B_VALID;
    schedule_bottom_half(b);     // defer everything else
}

// BOTTOM HALF -- runs later, interrupts enabled, may sleep.
void disk_bh(struct buf *b) {
    wakeup(b);                   // wake the waiting process
    update_statistics();
    maybe_issue_next_request();
}

// Why: a long top half blocks ALL interrupts, including the timer.
// Miss enough timer ticks and the clock drifts and scheduling stops.
""",
   "caption": "The top half acknowledges and records; everything else is "
              "deferred. Linux calls the deferred part softirqs, tasklets, or "
              "workqueues.",
   "note": "The 'missed timer ticks' consequence makes the rule concrete "
           "rather than arbitrary."},

  {"t": "bullets", "kicker": "Block layer", "title": "Scheduling I/O",
   "items": [
     "Requests are queued, merged, and reordered before reaching the device.",
     "",
     "<b>Merging:</b> adjacent requests become one — a large win.",
     "",
     "<b>Reordering:</b> on spinning disks, elevator ordering minimised seek "
     "time.",
     ("On SSDs there is no seek, so this matters far less — and the "
      "schedulers changed accordingly.", 1),
     "",
     "<b>Modern NVMe:</b> many deep queues, one per core. "
     "<code>none</code> is often the best scheduler, because the device "
     "schedules better than the kernel can.",
   ],
   "footnote": "A case where the right answer reversed when the hardware "
               "changed."},
 ],
 "takeaways": [
   "Device registers are not memory: reads have side effects, so accesses "
   "need <code>volatile</code>, barriers, and uncacheable mappings.",
   "Polling burns CPU and has low latency; interrupts are free while waiting "
   "and cost entry overhead. Fast devices have swung the answer back to "
   "polling.",
   "At very high event rates, interrupts cause livelock. NAPI switches to "
   "polling adaptively.",
   "DMA lets the device move data directly, which is why high-throughput I/O "
   "is possible — and it creates cache coherence obligations.",
   "Split handlers: the top half acknowledges and records with interrupts "
   "off; everything else is deferred to a bottom half that may sleep.",
   "I/O scheduling mattered enormously for seek time and matters far less for "
   "SSDs. The right answer changed when the hardware did.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Reaching a device"),
  ("table", ["", "Memory-mapped I/O", "Port I/O"],
   [["Mechanism", "Device registers are assigned physical addresses; the CPU "
     "reads and writes them with ordinary load and store instructions.",
     "A separate address space accessed with dedicated instructions "
     "(<code>in</code>/<code>out</code> on x86)."],
    ["Requirement", "The mapping must be marked <b>uncacheable</b>.",
     "No cache interaction by construction."],
    ["Status", "Universal on modern architectures.",
     "Legacy, x86-only, retained for a few old devices."]],
   [0.15, 0.47, 0.38]),
  ("callout", "Device registers violate every assumption about memory",
   ["<b>Reads have side effects.</b> Reading a status register may clear a "
    "pending interrupt or pop an entry from a hardware FIFO. Reading twice is "
    "not the same as reading once.",
    "<b>Values change without being written.</b> A status register changes "
    "because the device changed it.",
    "<b>Writes are not idempotent.</b> Writing a command register twice "
    "issues the command twice.",
    "So the compiler must not cache the value in a register, must not "
    "reorder accesses, and must not eliminate reads it believes are "
    "redundant. <b>This is what <code>volatile</code> is for</b> — "
    "memory-mapped hardware, not thread synchronisation, which it does not "
    "provide (CSCE 614 Module 12).",
    "And <code>volatile</code> constrains only the compiler. The processor "
    "may still reorder, so explicit memory barriers are required as well, and "
    "the mapping must be uncacheable or the cache will return stale values "
    "and absorb writes."]),

  ("h1", "2 &nbsp; Knowing when the device is ready"),
  ("table", ["", "Polling", "Interrupts"],
   [["How", "Read a status register in a loop until it indicates ready.",
     "The device asserts a signal; the CPU traps to a handler."],
    ["CPU cost while waiting", "<b>A full core.</b>", "None."],
    ["Latency", "<b>Minimal</b> — noticed almost immediately.",
     "Interrupt entry, context save, handler dispatch — microseconds."],
    ["Best for", "Devices that respond in less time than an interrupt costs; "
     "very high event rates.",
     "Slow devices and infrequent events."],
    ["Examples", "NVMe at high queue depth; a NIC under heavy load.",
     "Keyboard, mouse, spinning disk completion."]],
   [0.20, 0.40, 0.40]),
  ("p", "The historical direction was from polling to interrupts, as devices "
        "became slower relative to processors. Fast storage and high-speed "
        "networking have partly reversed it: when a device responds in less "
        "time than an interrupt costs to deliver, polling is simply cheaper."),
  ("callout", "Interrupt livelock",
   ["A network interface receiving ten million packets per second will "
    "generate ten million interrupts per second if each packet raises one. "
    "Every interrupt costs a context save, a handler entry, and cache and "
    "branch-predictor disturbance (CSCE 614 Modules 04 and 05).",
    "The system spends all of its time entering and leaving interrupt "
    "handlers and never reaches the code that would actually process "
    "packets. Throughput collapses toward zero while CPU utilisation sits at "
    "100% — a livelock in the sense of Module 05.",
    "The standard fix is to switch modes adaptively: on the first interrupt, "
    "<b>disable</b> that device's interrupts and poll the queue; when the "
    "queue drains, re-enable them and go back to sleep.",
    "Linux's <b>NAPI</b> is exactly this, and it gives interrupt-driven "
    "efficiency at low rates with polled efficiency at high rates, without "
    "the administrator choosing."]),

  ("h1", "3 &nbsp; DMA"),
  ("p", "With <b>programmed I/O</b>, the CPU moves every byte between the "
        "device and memory. For a device capable of 1 GB/s this consumes an "
        "entire core doing nothing but copying — which is why it does "
        "not scale."),
  ("p", "<b>Direct memory access</b> instead hands the device a physical "
        "buffer address and a length. The device transfers data to or from "
        "memory itself and raises an interrupt on completion. The CPU is free "
        "throughout."),
  ("callout", "DMA creates a cache coherence obligation",
   ["The device writes physical memory directly, bypassing the CPU's caches. "
    "Those caches do not know.",
    "<b>Before a device-read transfer</b> (CPU &rarr; device), the buffer "
    "must be flushed from cache, or the device may read stale data from "
    "memory while the current data sits dirty in cache.",
    "<b>After a device-write transfer</b> (device &rarr; CPU), the buffer "
    "must be invalidated, or the CPU may read a stale cached copy instead of "
    "the freshly transferred data.",
    "Many systems provide <i>coherent</i> DMA, where hardware snoops and "
    "handles this automatically. Many embedded systems do not, and omitting "
    "the flush or invalidate produces intermittent corruption that depends on "
    "cache state — among the least pleasant bugs in systems programming.",
    "An <b>IOMMU</b> adds address translation and protection for device "
    "accesses, which contains a buggy or malicious device and is what makes "
    "it safe to assign a device directly to a virtual machine."]),

  ("break",),
  ("h1", "4 &nbsp; Interrupt handlers"),
  ("p", "An interrupt handler runs with interrupts disabled, preempting "
        "whatever was executing. While it runs, <i>no other interrupt can be "
        "serviced</i> — including the timer."),
  ("callout", "Why a long handler is dangerous",
   ["Blocking all interrupts delays every other device, raising latency and "
    "potentially overflowing hardware buffers.",
    "Worse, it delays the <b>timer</b> interrupt. Miss enough timer ticks and "
    "the system clock drifts and scheduling decisions are deferred, which "
    "affects everything.",
    "An interrupt handler also <b>cannot sleep</b>: there is no process "
    "context to block, and blocking with interrupts disabled would deadlock "
    "the machine."]),
  ("code", """// TOP HALF -- interrupts disabled. Minimal work only.
void disk_intr(void) {
    ack_device();                   // acknowledge, so it stops asserting
    struct buf *b = dequeue_completed();
    b->flags |= B_VALID;
    schedule_bottom_half(b);        // defer the rest
}

// BOTTOM HALF -- runs later, interrupts enabled, may sleep.
void disk_bh(struct buf *b) {
    wakeup(b);
    update_statistics();
    maybe_issue_next_request();
}"""),
  ("p", "The top half does only what must happen immediately: acknowledge the "
        "device so it stops asserting the interrupt, capture any state that "
        "would otherwise be lost, and schedule the remainder. Everything else "
        "runs in a <b>bottom half</b> with interrupts enabled."),
  ("p", "Linux provides several deferral mechanisms with different "
        "properties: <i>softirqs</i> (fixed set, high performance), "
        "<i>tasklets</i> (dynamically created, serialised per tasklet), and "
        "<i>workqueues</i> (run in process context and therefore may sleep). "
        "The choice depends on whether the deferred work needs to block."),

  ("h1", "5 &nbsp; The block layer"),
  ("p", "Requests do not go straight to the device. The kernel queues them, "
        "and before dispatch it can merge and reorder."),
  ("ul", ["<b>Merging</b> combines adjacent requests into one larger "
          "transfer. This is a substantial win on every device type, because "
          "per-request overhead is significant and large transfers amortise "
          "it.",
          "<b>Reordering</b> was historically the larger win. On a spinning "
          "disk, seek time dominates, and servicing requests in "
          "block-address order — the <i>elevator</i> algorithm, sweeping "
          "the head across the platter — could improve throughput "
          "several-fold.",
          "<b>On an SSD there is no seek.</b> Access time is essentially "
          "independent of address, so elevator ordering buys almost nothing "
          "and the complexity is wasted."]),
  ("callout", "A case where the right answer reversed",
   ["Decades of I/O scheduler research optimised for seek time. When storage "
    "stopped having a seek, most of that work became irrelevant — and "
    "some of it became actively harmful, because the scheduler introduced "
    "latency to perform reordering that no longer helped.",
    "Modern NVMe devices expose many deep queues, typically one per CPU core, "
    "and perform their own internal scheduling with far better knowledge of "
    "the flash layout than the kernel has. For these, Linux's "
    "<code>none</code> scheduler — do nothing, submit immediately "
    "— is frequently the best choice.",
    "It is a useful reminder that systems knowledge has a half-life, and that "
    "an optimisation is a claim about hardware that may stop being true."]),
 ],
 "resources": [
   ("OSTEP — Chapters 36&ndash;37 (I/O Devices, Hard Disk Drives)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "Polling, interrupts, DMA, and disk scheduling with the seek-time "
    "analysis."),
   ("xv6 book — Chapter 5 (Interrupts and device drivers)",
    "https://pdos.csail.mit.edu/6.1810/2023/xv6/book-riscv-rev3.pdf",
    "A complete disk and console driver, short enough to read entirely."),
   ("Linux Device Drivers, 3rd edition (free)",
    "https://lwn.net/Kernel/LDD3/",
    "Dated in specifics and still the best free explanation of the "
    "concepts — memory-mapped I/O, DMA, deferred work."),
   ("Mogul & Ramakrishnan — Eliminating Receive Livelock (free)",
    "https://dl.acm.org/doi/10.1145/263326.263335",
    "The paper behind NAPI. Clear, and the problem it describes recurs "
    "wherever event rates grow."),
 ],
 "exercises": [
   "Read xv6's console and disk drivers. Identify the memory-mapped register "
   "accesses and the interrupt handler, and classify the work as top-half or "
   "bottom-half.",
   "Remove <code>volatile</code> from a device register access and inspect "
   "the generated assembly at <code>-O2</code>. Confirm the compiler hoists "
   "the read out of the polling loop.",
   "Implement polling and interrupt-driven versions of a device driver in "
   "xv6. Measure CPU utilisation and latency for each at low and high event "
   "rates.",
   "Simulate interrupt livelock: generate events faster than the handler can "
   "retire them and observe throughput collapsing while the CPU saturates. "
   "Then implement NAPI-style adaptive polling and measure again.",
   "Split an interrupt handler into top and bottom halves. Measure the "
   "maximum interrupt-disabled duration before and after.",
   "Measure the effect of request merging: issue a thousand sequential 4 KB "
   "reads and then one 4 MB read, and compare total time.",
   "Compare I/O schedulers on a spinning disk and an SSD, if you have access "
   "to both, with a random-access workload. Explain the difference.",
 ],
 "selfcheck": [
   "Why must memory-mapped device registers be uncacheable, and why is "
   "<code>volatile</code> necessary but insufficient?",
   "Give the trade-off between polling and interrupts, and explain why fast "
   "devices have swung it back toward polling.",
   "What is interrupt livelock, and how does NAPI address it?",
   "What does DMA buy, and what obligation does it create for the driver?",
   "Why must an interrupt handler be short, and why can it not sleep?",
   "What goes in the top half and what in the bottom half?",
   "Why did I/O scheduling matter so much for spinning disks and so little "
   "for NVMe?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Protection and Isolation",
 "subtitle": "Containers, virtual machines, and what each actually isolates.",
 "question": "What mechanisms separate one workload from another, and how "
             "strong is each?",
 "outcomes": [
     "Explain users, groups, and the limits of discretionary access control.",
     "Explain capabilities and the principle of least privilege.",
     "Explain namespaces and cgroups, and what a container really is.",
     "Compare container and VM isolation honestly.",
     "Explain the kernel attack surface and why it matters.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Classical Unix protection",
   "blurb": "Users, groups, and a model from 1970."},

  {"t": "bullets", "kicker": "DAC", "title": "Discretionary access control",
   "items": [
     "Every process has a user ID; every file has an owner, a group, and nine "
     "permission bits.",
     "",
     "The owner decides who may access — hence <b>discretionary</b>.",
     "",
     "<b>Simple, and it has aged badly:</b>",
     ("<b>root bypasses everything.</b> A single all-powerful account.", 1),
     ("Permissions are per-file, so expressing 'this program may read these "
      "three files' is awkward.", 1),
     ("A compromised process inherits all its user's privileges — "
      "<b>ambient authority</b>.", 1),
   ],
   "note": "Ambient authority is the deep problem and the one capabilities "
           "are designed to fix."},

  {"t": "callout", "title": "setuid: the necessary hack",
   "kind": "Where the model strains",
   "body": ["Some operations need privilege that ordinary users must be able "
            "to invoke — <code>passwd</code> must write "
            "<code>/etc/shadow</code>.",
            "The <b>setuid</b> bit makes a program run with the file owner's "
            "privileges rather than the caller's. <code>passwd</code> is "
            "setuid root.",
            "So every setuid-root binary is a potential privilege escalation: "
            "find a bug in it and you have root. Historically this has been "
            "one of the richest sources of local exploits.",
            "The principled fix is <b>capabilities</b>: grant the one "
            "specific power needed instead of all of them."]},

  {"t": "section", "label": "Part 2", "title": "Least privilege",
   "blurb": "Give each component only what it needs."},

  {"t": "table", "kicker": "Mechanisms", "title": "Narrowing privilege",
   "header": ["Mechanism", "Does", "Example"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Capabilities", "Split root into ~40 distinct powers", "CAP_NET_BIND_SERVICE only"],
     ["seccomp", "Restrict which syscalls a process may make", "A sandbox allowing 20 of 400"],
     ["chroot / pivot_root", "Change the visible filesystem root", "Weak alone; a building block"],
     ["MAC (SELinux)", "Policy-enforced, not owner-discretionary", "Even root is constrained"],
     ["Privilege dropping", "Start privileged, then give it up", "Bind port 80, then setuid"],
   ],
   "note": "seccomp is the one most worth knowing: shrinking the syscall "
           "surface is the most effective single hardening step."},

  {"t": "callout", "title": "Why reducing the syscall surface matters most",
   "kind": "The practical insight",
   "body": ["A container's isolation is enforced by the <b>kernel</b>. The "
            "kernel's attack surface is its system call interface — "
            "roughly 400 calls, some of them old, complex, and rarely "
            "audited.",
            "A kernel bug reachable from a system call is a container escape: "
            "the attacker is no longer confined.",
            "A typical application needs perhaps 40 system calls. Blocking "
            "the other 360 with seccomp removes most of the reachable attack "
            "surface for a few lines of configuration.",
            "This is why serious container runtimes ship seccomp profiles by "
            "default, and why 'what syscalls does this need' is a useful "
            "security question."]},

  {"t": "section", "label": "Part 3", "title": "Containers",
   "blurb": "Not a thing — a combination of kernel features."},

  {"t": "bullets", "kicker": "Namespaces", "title": "What a container is made of",
   "items": [
     "<b>There is no 'container' object in the kernel.</b> A container is a "
     "process with several kernel features applied.",
     "",
     "<b>Namespaces</b> — give a process a private view of a global "
     "resource:",
     ("PID (own process tree), mount (own filesystem view), network (own "
      "interfaces), user (own UID mapping), UTS, IPC.", 1),
     "",
     "<b>cgroups</b> — limit and account for resources: CPU, memory, "
     "I/O, PIDs.",
     "",
     "<b>seccomp + capabilities</b> — restrict what it may ask the "
     "kernel to do.",
   ],
   "note": "Students are often surprised there is no container abstraction. "
           "It clarifies a great deal."},

  {"t": "two", "kicker": "Compare", "title": "Containers and virtual machines",
   "lh": "Container",
   "l": ["Shares the host <b>kernel</b>.",
         "Isolation enforced by kernel features.",
         "Start in milliseconds; near-zero overhead.",
         "<b>Attack surface: the whole syscall interface.</b>",
         ("One kernel bug and the isolation is gone.", 1)],
   "rh": "Virtual machine",
   "r": ["Runs its <b>own kernel</b>.",
         "Isolation enforced by the hypervisor and hardware.",
         "Start in seconds; real memory overhead.",
         "<b>Attack surface: the hypervisor interface.</b>",
         ("Much smaller, and hardware-assisted.", 1)],
   "note": "Being honest that containers are a weaker boundary is more useful "
           "than the marketing framing."},

  {"t": "callout", "title": "Containers are a weaker boundary than VMs",
   "kind": "Honest assessment",
   "body": ["This is not a criticism — it is a trade, and usually the "
            "right one.",
            "Containers isolate <i>workloads you already trust</i> from each "
            "other: your own services, built by your own team. The efficiency "
            "gain is enormous and the risk is acceptable.",
            "VMs isolate <i>mutually distrusting</i> parties: different "
            "customers on shared hardware. The hypervisor interface is a far "
            "smaller and more carefully audited boundary.",
            "<b>Middle ground:</b> lightweight VMs with a minimal guest "
            "— Firecracker, Kata — giving VM-grade isolation with "
            "container-like startup. This is what serverless platforms run."]},

  {"t": "section", "label": "Part 4", "title": "Virtualisation",
   "blurb": "Running a kernel inside a kernel."},

  {"t": "bullets", "kicker": "Hypervisors", "title": "How a VM works",
   "items": [
     "The guest kernel believes it is in supervisor mode. It is not.",
     "",
     "<b>Hardware support</b> (Intel VT-x, AMD-V, ARM EL2) adds a privilege "
     "level <i>below</i> the kernel.",
     ("Privileged guest operations trap to the hypervisor, which emulates "
      "them.", 1),
     "",
     "<b>Nested paging</b> (EPT/NPT) translates guest-physical to "
     "host-physical in hardware — no shadow page tables.",
     "",
     "<b>Paravirtualisation</b> (virtio) — the guest knows it is "
     "virtualised and uses efficient interfaces instead of emulated hardware.",
   ],
   "note": "Nested paging is the development that made virtualisation cheap "
           "enough to be ubiquitous."},

  {"t": "table", "kicker": "Spectrum", "title": "The isolation spectrum",
   "header": ["Mechanism", "Isolates by", "Strength"],
   "widths": [3.2, 4.4, 4.5],
   "rows": [
     ["Process", "Page tables", "Weak — shared kernel, full syscall access"],
     ["Container", "Namespaces + cgroups + seccomp", "Moderate"],
     ["Lightweight VM", "Hypervisor, minimal guest", "<b>Strong</b>, fast start"],
     ["Full VM", "Hypervisor + own kernel", "<b>Strong</b>"],
     ["Separate machine", "Physics", "Strongest; side channels remain"],
   ],
   "footnote": "Even separate machines share a network. There is no absolute "
               "isolation.",
   "note": "Ending on 'side channels remain' connects back to CSCE 614 Module "
           "04 and is honest."},
 ],
 "takeaways": [
   "Unix DAC gives every process its user's full authority — ambient "
   "authority — so a compromised process inherits everything.",
   "setuid is a necessary hack that makes every setuid-root binary a "
   "potential privilege escalation.",
   "Capabilities and seccomp narrow privilege. Reducing the syscall surface "
   "is the single most effective hardening step.",
   "A container is not a kernel object: it is namespaces plus cgroups plus "
   "seccomp plus capabilities, applied to an ordinary process.",
   "Containers share the host kernel, so the attack surface is the whole "
   "syscall interface. VMs have a much smaller boundary.",
   "Hardware virtualisation adds a privilege level below the kernel; nested "
   "paging is what made it cheap enough to be universal.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Classical Unix protection"),
  ("p", "Every process carries a user ID and group IDs; every file carries an "
        "owner, a group, and nine permission bits. Access is decided by "
        "comparing them. This is <b>discretionary access control</b>: the "
        "owner of a resource decides who may use it."),
  ("p", "It is admirably simple and it has aged poorly in three specific "
        "ways."),
  ("ul", ["<b>root bypasses everything.</b> A single account with unlimited "
          "authority means any compromise of a root process is a total "
          "compromise.",
          "<b>Granularity is wrong.</b> Permissions attach to files, so "
          "expressing 'this program may read these three files and open "
          "outbound connections to this host' requires contortions.",
          "<b>Ambient authority.</b> A process automatically holds <i>all</i> "
          "of its user's privileges, whether it needs them or not. A text "
          "editor can delete your entire home directory because you can. A "
          "bug in any program is a bug with your full authority behind it."]),
  ("callout", "setuid, and why it is a persistent weakness",
   ["Some operations genuinely require privilege but must be available to "
    "ordinary users: <code>passwd</code> must modify "
    "<code>/etc/shadow</code>, <code>ping</code> historically needed raw "
    "sockets.",
    "The <b>setuid</b> bit causes a program to run with the privileges of the "
    "file's owner rather than the invoking user. <code>passwd</code> is "
    "setuid root.",
    "The consequence is that every setuid-root binary on the system is a "
    "potential privilege escalation: find an exploitable bug in any of them "
    "and you obtain root. This has historically been one of the most "
    "productive categories of local vulnerability.",
    "The principled response is <b>least privilege</b>: grant the specific "
    "power required rather than all powers. That is what capabilities "
    "provide, and why <code>ping</code> now uses "
    "<code>CAP_NET_RAW</code> instead of being setuid."]),

  ("h1", "2 &nbsp; Narrowing privilege"),
  ("table", ["Mechanism", "What it does", "Example"],
   [["<b>Capabilities</b>", "Divide root's authority into roughly forty "
     "distinct powers that can be granted individually.",
     "A web server receives <code>CAP_NET_BIND_SERVICE</code> to bind port 80 "
     "and nothing else — it cannot read arbitrary files or load kernel "
     "modules."],
    ["<b>seccomp</b>", "Restrict which system calls a process may issue, with "
     "a BPF filter.",
     "A sandboxed renderer permits around twenty calls and blocks the rest. "
     "Chrome and OpenSSH use this heavily."],
    ["<b>chroot / pivot_root</b>", "Change the process's apparent filesystem "
     "root.",
     "Weak alone — a privileged process can escape — but a useful "
     "building block when combined with the others."],
    ["<b>Mandatory access control</b> (SELinux, AppArmor)",
     "Policy set by the administrator and enforced regardless of the file "
     "owner's wishes.",
     "Even root is constrained by policy. Changes the model from "
     "discretionary to mandatory."],
    ["<b>Privilege dropping</b>", "Start with the privilege needed for "
     "initialisation, then permanently relinquish it.",
     "Bind to port 80 as root, then <code>setuid</code> to an unprivileged "
     "account before handling any request."]],
   [0.21, 0.37, 0.42]),
  ("callout", "The syscall surface is the thing to shrink",
   ["A container's isolation is enforced <i>by the kernel</i>. The kernel's "
    "attack surface is therefore its system call interface — around 400 "
    "calls, several of them decades old, complex, and rarely exercised.",
    "A kernel bug reachable through any of them is a container escape: the "
    "attacker ceases to be confined.",
    "A typical application needs perhaps forty system calls. A seccomp "
    "profile blocking the other 360 eliminates most of the reachable attack "
    "surface for the cost of a configuration file.",
    "This is why serious container runtimes apply a default seccomp profile, "
    "and why 'which system calls does this workload actually need' is a "
    "productive security question rather than a pedantic one."]),

  ("break",),
  ("h1", "3 &nbsp; What a container actually is"),
  ("callout", "There is no container object in the kernel",
   ["A container is not a kernel abstraction. It is an ordinary process with "
    "several independent kernel features applied to it, assembled by a "
    "runtime such as runc into something that behaves like an isolated "
    "machine.",
    "Understanding this clarifies both the capabilities and the limits: "
    "whatever the features isolate is isolated, and whatever they do not, is "
    "not."]),
  ("table", ["Feature", "Provides", "Namespace types"],
   [["<b>Namespaces</b>", "A private view of an otherwise global resource.",
     "<b>PID</b> (its own process tree, where it is PID 1); <b>mount</b> (its "
     "own filesystem view); <b>network</b> (its own interfaces and routing "
     "table); <b>user</b> (UID mapping, so container root is an unprivileged "
     "host user); <b>UTS</b> (hostname); <b>IPC</b>; <b>cgroup</b>; "
     "<b>time</b>."],
    ["<b>cgroups</b>", "Resource limits and accounting.",
     "CPU shares and quotas, memory limits, block I/O bandwidth, process "
     "count. This is what stops one container starving the others."],
    ["<b>seccomp</b>", "System call restriction.",
     "Shrinks the kernel attack surface, as above."],
    ["<b>Capabilities</b>", "Privilege restriction.",
     "A container's 'root' holds a reduced capability set."]],
   [0.17, 0.26, 0.57]),
  ("h2", "3.1 &nbsp; Containers against virtual machines"),
  ("table", ["", "Container", "Virtual machine"],
   [["Kernel", "<b>Shares the host's.</b>", "Runs its own."],
    ["Isolation enforced by", "Kernel features: namespaces, cgroups, seccomp.",
     "Hypervisor plus hardware virtualisation support."],
    ["Start-up", "Milliseconds.", "Seconds."],
    ["Overhead", "Essentially none.", "A full kernel's worth of memory, plus "
     "some trap overhead."],
    ["<b>Attack surface</b>", "<b>The entire system call interface</b> "
     "— large, old, complex.",
     "<b>The hypervisor interface</b> — far smaller and more heavily "
     "audited."],
    ["Guest OS", "Must match the host kernel.", "Any."]],
   [0.19, 0.41, 0.40]),
  ("callout", "Containers are a weaker boundary, and usually the right choice",
   ["Stating this plainly is more useful than the marketing framing. A "
    "container escape requires one exploitable kernel bug reachable from a "
    "permitted system call, and such bugs are found regularly.",
    "<b>Containers isolate workloads you already trust</b> from one another "
    "— your own services, built by your own team, from your own code. "
    "The density and startup advantages are enormous and the residual risk is "
    "acceptable.",
    "<b>VMs isolate mutually distrusting parties</b> — different "
    "customers sharing hardware. The smaller, hardware-assisted boundary is "
    "worth the overhead.",
    "The middle ground is <b>lightweight VMs</b>: a minimal guest kernel and "
    "a stripped hypervisor, giving VM-grade isolation with container-like "
    "startup times. AWS Firecracker and Kata Containers are the examples, and "
    "this is what serverless platforms actually run — precisely because "
    "they execute untrusted customer code."]),

  ("h1", "4 &nbsp; Virtualisation mechanics"),
  ("p", "A guest kernel is written on the assumption that it runs in "
        "supervisor mode with full control of the hardware. It does not."),
  ("table", ["Mechanism", "How it works"],
   [["<b>Hardware virtualisation</b> (Intel VT-x, AMD-V, ARM EL2)",
     "Adds a privilege level <i>beneath</i> the kernel's. The guest runs in a "
     "mode that looks like supervisor mode; privileged operations trap to the "
     "hypervisor, which emulates them and resumes the guest. Before this "
     "existed, the same effect required binary translation or "
     "paravirtualisation."],
    ["<b>Nested paging</b> (EPT, NPT, Stage-2)",
     "Two levels of translation in hardware: guest-virtual to guest-physical "
     "(by the guest's page tables) and guest-physical to host-physical (by "
     "the hypervisor's). Before this, hypervisors maintained <i>shadow page "
     "tables</i> and trapped every guest page table modification — "
     "ruinously expensive. Nested paging is the single development that made "
     "virtualisation cheap enough to be ubiquitous."],
    ["<b>Paravirtualisation</b> (virtio)",
     "The guest knows it is virtualised and uses efficient ring-buffer "
     "interfaces for disk and network rather than driving emulated hardware "
     "registers that would trap on every access."],
    ["<b>Device passthrough</b> (with an IOMMU)",
     "Assign a physical device directly to a guest. The IOMMU translates and "
     "confines the device's DMA (Module 10), making this safe."]],
   [0.30, 0.70]),

  ("h1", "5 &nbsp; The isolation spectrum"),
  ("table", ["Mechanism", "Boundary enforced by", "Strength"],
   [["Process", "Page tables.",
     "Weak. Shares the kernel; full system call access; shares all "
     "microarchitectural state."],
    ["Container", "Namespaces, cgroups, seccomp, capabilities.",
     "Moderate. Good against accident and against unprivileged attackers; one "
     "kernel bug from failure."],
    ["Lightweight VM", "Hypervisor with a minimal guest.",
     "<b>Strong</b>, with fast startup. The current best answer for untrusted "
     "code at density."],
    ["Full VM", "Hypervisor plus a complete guest kernel.",
     "<b>Strong.</b> The standard for multi-tenant infrastructure."],
    ["Separate hardware", "Physics.",
     "Strongest available, and still not absolute."]],
   [0.20, 0.33, 0.47]),
  ("callout", "There is no perfect isolation",
   ["Even separate machines share a network, a power supply, and a physical "
    "environment.",
    "Within a machine, <b>side channels</b> cross every boundary described "
    "here. Cache timing, branch predictor state, and speculative execution "
    "leak information between processes, between containers, and between "
    "virtual machines — Spectre and its relatives (CSCE 614 Module 04) "
    "were effective across all of them.",
    "Mitigations exist and cost real performance. The honest summary is that "
    "isolation is a matter of degree and of cost, not a binary property, and "
    "that choosing a mechanism means choosing an acceptable residual risk "
    "rather than eliminating risk."]),
 ],
 "resources": [
   ("OSTEP — security chapters",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "Access control and the authentication model."),
   ("Linux kernel documentation — namespaces, cgroups v2, seccomp",
    "https://docs.kernel.org/admin-guide/",
    "The primary reference for what a container is actually built from."),
   ("Agache et al. — Firecracker: Lightweight Virtualization for "
    "Serverless Applications (free)",
    "https://www.usenix.org/conference/nsdi20/presentation/agache",
    "Why serverless platforms use micro-VMs rather than containers, argued "
    "with data."),
   ("Saltzer & Schroeder — The Protection of Information in Computer "
    "Systems (1975, free)",
    "https://www.cs.virginia.edu/~evans/cs551/saltzer/",
    "The paper that stated least privilege and the other design principles. "
    "Still the clearest statement of them."),
 ],
 "exercises": [
   "Write a program that drops privileges correctly: bind a privileged port "
   "as root, then permanently relinquish root. Verify with "
   "<code>/proc/self/status</code> that the capability set is empty.",
   "Write a seccomp filter permitting only the system calls your program "
   "needs. Determine the set empirically with <code>strace</code>, then "
   "verify that a blocked call terminates the process.",
   "Build a minimal container by hand: <code>clone()</code> with new PID, "
   "mount, and network namespaces, then <code>pivot_root</code>. Confirm the "
   "child sees itself as PID 1.",
   "Add a cgroup memory limit to your hand-built container and demonstrate "
   "that exceeding it triggers the OOM killer inside the container only.",
   "Compare startup time and memory footprint for the same trivial workload "
   "as a process, a container, and a VM.",
   "Enumerate the setuid-root binaries on a Linux system. Pick one and "
   "identify which capability it would need if rewritten to use capabilities "
   "instead.",
   "Read a default Docker seccomp profile and count how many of the roughly "
   "400 system calls it permits.",
 ],
 "selfcheck": [
   "What is ambient authority, and why is it a problem?",
   "Why is every setuid-root binary a potential privilege escalation, and "
   "what is the principled alternative?",
   "Why is reducing the system call surface the most effective single "
   "hardening measure for a container?",
   "What is a container made of? Name four kernel features and what each "
   "provides.",
   "Why is a container a weaker isolation boundary than a VM, and when is "
   "that acceptable?",
   "What does nested paging replace, and why did it matter so much?",
   "Why is there no such thing as perfect isolation?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Distributed Aspects: RPC and Network File Systems",
 "subtitle": "Where the operating system's abstractions stop working.",
 "question": "What breaks when a system call crosses a network?",
 "outcomes": [
     "Explain RPC and why it cannot be transparent.",
     "State the fallacies of distributed computing and their consequences.",
     "Explain at-most-once, at-least-once, and exactly-once semantics.",
     "Explain NFS's stateless design and what it buys and costs.",
     "Explain caching and consistency trade-offs in distributed file "
     "systems.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "RPC",
   "blurb": "Make a remote call look like a local one. It does not work."},

  {"t": "bullets", "kicker": "RPC", "title": "The appealing idea",
   "items": [
     "A client stub marshals the arguments, sends them, and blocks.",
     "The server unmarshals, calls the real function, and returns the result.",
     "",
     "The programmer writes what looks like an ordinary function call.",
     "",
     "<b>The appeal:</b> distribution becomes invisible.",
     "",
     "<b>The problem:</b> distribution is not invisible, and pretending "
     "otherwise produces systems that fail in ways nobody designed for.",
   ]},

  {"t": "table", "kicker": "Differences", "title": "Why a remote call is not a local call",
   "header": ["Local call", "Remote call"],
   "widths": [6.0, 6.1],
   "rows": [
     ["Nanoseconds", "Microseconds to seconds — 10⁶× more"],
     ["Cannot fail independently", "<b>Can fail without the caller failing</b>"],
     ["Pointers work", "Pointers are meaningless"],
     ["Shared memory", "Everything must be serialised"],
     ["Caller and callee die together", "Either may die alone"],
     ["Failure means a crash", "<b>Failure may mean 'no answer yet'</b>"],
   ],
   "note": "The last row is the one that breaks everything: you cannot "
           "distinguish slow from dead."},

  {"t": "callout", "title": "The fundamental problem: you cannot tell slow from dead",
   "kind": "The core difficulty",
   "body": ["A request goes out. No reply arrives. What happened?",
            "The request was lost. Or it arrived and the server is slow. Or "
            "it executed and the <i>reply</i> was lost. Or the server "
            "crashed before executing. Or after.",
            "<b>These are indistinguishable from the client.</b> No timeout "
            "value resolves them, because any timeout may be too short for a "
            "slow server.",
            "Everything difficult about distributed systems descends from "
            "this. It is why consensus is hard, why exactly-once delivery is "
            "impossible, and why retries need idempotence."]},

  {"t": "section", "label": "Part 2", "title": "Delivery semantics",
   "blurb": "Three options, and one of them is a lie."},

  {"t": "table", "kicker": "Semantics", "title": "What a retry can promise",
   "header": ["Semantics", "Means", "Requires"],
   "widths": [2.8, 4.4, 4.9],
   "rows": [
     ["At-most-once", "Never executed twice; may not execute", "Do not retry"],
     ["At-least-once", "Executed, possibly many times", "<b>Idempotent</b> operations"],
     ["Exactly-once", "Executed precisely once", "<b>Impossible</b> at the transport layer"],
   ],
   "footnote": "'Exactly-once' systems achieve it by making retries "
               "idempotent, not by delivering once.",
   "note": "Being clear that exactly-once is a lie at the transport layer "
           "saves a lot of confusion about Kafka and friends."},

  {"t": "callout", "title": "Exactly-once does not exist. Idempotence does.",
   "kind": "What people mean",
   "body": ["You cannot guarantee a message is delivered and processed "
            "exactly once over an unreliable network. This is a theorem, not "
            "an engineering gap.",
            "What systems advertising 'exactly-once' actually do: retry "
            "freely (at-least-once) and make the <i>effect</i> idempotent, "
            "usually with a deduplication key.",
            "<code>transfer(account, +$100)</code> is not idempotent. "
            "<code>set_balance(account, $500)</code> is. "
            "<code>apply(txn_id, +$100)</code> with duplicate detection is.",
            "<b>Design the operation to be safely repeatable</b> and the "
            "delivery problem stops mattering."]},

  {"t": "bullets", "kicker": "Fallacies", "title": "The eight fallacies of distributed computing",
   "items": [
     "The network is reliable. — It is not.",
     "Latency is zero. — It is not, and it is variable.",
     "Bandwidth is infinite. — It is not.",
     "The network is secure. — It is not.",
     "Topology does not change. — It does.",
     "There is one administrator. — There is not.",
     "Transport cost is zero. — Serialisation is expensive.",
     "The network is homogeneous. — It is not.",
     "",
     "Every one of these is an assumption a local call may safely make.",
   ],
   "footnote": "Deutsch and Gosling, 1994. Still entirely accurate.",
   "note": "Worth stating that the fallacies are exactly the assumptions RPC "
           "transparency invites you to make."},

  {"t": "section", "label": "Part 3", "title": "Network file systems",
   "blurb": "The same problem, applied to files."},

  {"t": "bullets", "kicker": "NFS", "title": "Stateless by design",
   "items": [
     "The NFS server keeps <b>no per-client state</b>. Every request is "
     "self-contained.",
     ("No 'open file' on the server — each read carries a file handle "
      "and an offset.", 1),
     "",
     "<b>Why:</b> crash recovery becomes trivial. A rebooted server just "
     "starts answering again; clients retry and notice nothing.",
     "",
     "<b>Cost:</b> no server-side locking or open semantics.",
     ("Deleting an open file does not work as it does locally (Module 08).", 1),
     ("Every operation must be <b>idempotent</b>, because clients retry.", 1),
   ],
   "note": "NFS is a clean example of a design choice driven entirely by the "
           "failure model."},

  {"t": "callout", "title": "Caching forces a consistency choice",
   "kind": "The unavoidable trade",
   "body": ["Without client caching, every read is a network round trip "
            "— unusably slow.",
            "With caching, a client may read stale data after another client "
            "writes.",
            "<b>NFS chose</b> close-to-open consistency: changes are visible "
            "to a client that opens the file after the writer closed it. "
            "Weaker than local semantics, and strong enough for most use.",
            "<b>AFS chose</b> callbacks: the server notifies clients when "
            "their cached copy becomes invalid. Stronger, and the server must "
            "now keep state — which is exactly what NFS avoided.",
            "There is no option that is both fast and locally-consistent. "
            "This is CAP in miniature."]},

  {"t": "table", "kicker": "Compare", "title": "Two designs, two trades",
   "header": ["", "NFS", "AFS"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Server state", "<b>None</b>", "Tracks client caches"],
     ["Consistency", "Close-to-open", "Callbacks — stronger"],
     ["Crash recovery", "<b>Trivial</b>", "Must rebuild callback state"],
     ["Scalability", "Good", "<b>Better</b> — fewer round trips"],
     ["Caching unit", "Blocks", "Whole files"],
   ],
   "note": "AFS's whole-file caching was designed for a campus WAN and the "
           "trade shows it."},

  {"t": "bullets", "kicker": "Where this goes", "title": "The lessons that generalise",
   "items": [
     "<b>Make operations idempotent.</b> Then retries are safe and delivery "
     "semantics stop mattering.",
     "",
     "<b>Do not hide the network.</b> An interface that pretends remote calls "
     "are local invites every fallacy.",
     "",
     "<b>Decide your consistency model explicitly</b> and write it down. "
     "Every distributed system has one, stated or not.",
     "",
     "<b>Design for partial failure</b> — it is the normal case, not an "
     "exception.",
     "",
     "CSCE 662 and 678 develop all of this properly.",
   ]},
 ],
 "takeaways": [
   "RPC makes a remote call look local, and the differences — latency, "
   "independent failure, no shared memory — cannot be hidden.",
   "You cannot distinguish a slow server from a dead one. Every hard problem "
   "in distributed systems descends from this.",
   "At-most-once means do not retry; at-least-once requires idempotence; "
   "exactly-once is impossible at the transport layer.",
   "Systems claiming exactly-once achieve it by making effects idempotent "
   "with deduplication keys, not by delivering once.",
   "NFS is stateless so that crash recovery is trivial, and pays for it with "
   "weaker semantics and mandatory idempotence.",
   "Caching forces a consistency choice. NFS chose close-to-open; AFS chose "
   "callbacks and had to keep state.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Remote procedure call"),
  ("p", "RPC's premise is that a call to a remote service should look like an "
        "ordinary function call. A client <b>stub</b> marshals the arguments "
        "into a message, sends it, and blocks; a server stub unmarshals, "
        "invokes the real function, and returns the result the same way."),
  ("p", "The appeal is obvious: distribution becomes an implementation "
        "detail. The difficulty is that distribution is not an implementation "
        "detail, and an abstraction that pretends otherwise leads programmers "
        "to write code that cannot handle the failures that will occur."),
  ("table", ["Local call", "Remote call"],
   [["Takes nanoseconds.",
     "Takes microseconds to seconds — six orders of magnitude more, and "
     "highly variable."],
    ["Cannot fail without the caller also failing.",
     "<b>Can fail independently.</b> The callee may die while the caller "
     "continues."],
    ["Pointers are valid.",
     "Pointers are meaningless; everything must be serialised and copied."],
    ["Shares memory with the callee.", "Shares nothing."],
    ["Failure means the whole process crashed.",
     "<b>Failure may mean 'no answer yet'</b> — an outcome with no local "
     "analogue."]],
   [0.42, 0.58]),
  ("callout", "You cannot distinguish slow from dead",
   ["A request is sent. No reply arrives within the timeout. What happened?",
    "The request may have been lost in transit. It may have arrived and the "
    "server is merely slow. It may have executed successfully and the "
    "<i>reply</i> was lost. The server may have crashed before executing it, "
    "or after.",
    "<b>From the client these are indistinguishable.</b> No choice of timeout "
    "resolves the ambiguity, because any timeout is potentially too short for "
    "a server that is heavily loaded rather than dead.",
    "Essentially every difficulty in distributed systems descends from this "
    "single fact: it is why consensus algorithms are subtle, why exactly-once "
    "delivery is impossible, why failure detectors are necessarily imperfect, "
    "and why retries must be safe to repeat."]),

  ("h1", "2 &nbsp; Delivery semantics"),
  ("table", ["Semantics", "Guarantee", "How to obtain it"],
   [["<b>At-most-once</b>", "The operation never executes more than once. It "
     "may not execute at all.",
     "Do not retry. Suitable when a duplicate is worse than a loss."],
    ["<b>At-least-once</b>", "The operation executes, possibly several times.",
     "Retry until acknowledged. Requires the operation to be "
     "<b>idempotent</b>, or duplicates cause damage."],
    ["<b>Exactly-once</b>", "The operation executes precisely once.",
     "<b>Not achievable</b> at the transport layer over an unreliable "
     "network."]],
   [0.18, 0.37, 0.45]),
  ("callout", "What 'exactly-once' systems actually do",
   ["Exactly-once delivery is impossible, and this is a theorem rather than a "
    "gap in current engineering: the sender cannot know whether a lost "
    "acknowledgement means the operation happened.",
    "Systems that advertise exactly-once semantics achieve it differently: "
    "they retry freely, giving at-least-once delivery, and make the "
    "<b>effect</b> idempotent — typically by attaching a unique "
    "identifier to each operation and having the receiver discard duplicates.",
    "The design lesson is concrete. <code>transfer(account, +$100)</code> is "
    "not idempotent, and a retry doubles the transfer. "
    "<code>set_balance(account, $500)</code> is idempotent. "
    "<code>apply(txn_id=abc123, +$100)</code> with server-side duplicate "
    "detection is idempotent and preserves the semantics you wanted.",
    "<b>Make the operation safely repeatable and the delivery problem stops "
    "mattering.</b> This single technique resolves a large fraction of "
    "distributed systems difficulty."]),
  ("h2", "2.1 &nbsp; The fallacies of distributed computing"),
  ("p", "Peter Deutsch and James Gosling's list of assumptions that newcomers "
        "to distributed systems make, all of which are false and all of which "
        "a local function call may safely make:"),
  ("ol", ["The network is reliable.",
          "Latency is zero.",
          "Bandwidth is infinite.",
          "The network is secure.",
          "Topology does not change.",
          "There is one administrator.",
          "Transport cost is zero.",
          "The network is homogeneous."]),
  ("p", "The list is thirty years old and has not aged. Note the relationship "
        "to &sect;1: these are precisely the assumptions that RPC's "
        "transparency invites, which is the strongest argument against making "
        "remote calls look local."),

  ("break",),
  ("h1", "3 &nbsp; Network file systems"),
  ("h2", "3.1 &nbsp; NFS and statelessness"),
  ("p", "NFS's defining decision is that the server keeps <b>no per-client "
        "state</b>. There is no server-side notion of an open file; each "
        "request carries a file handle and an explicit offset and is "
        "completely self-contained."),
  ("callout", "The failure model drove the design",
   ["With no per-client state, server crash recovery is trivial: the server "
    "reboots and begins answering requests again. Clients, which were "
    "retrying anyway, simply succeed on a later attempt and may not notice "
    "the outage at all.",
    "A stateful server would have to reconstruct every client's open files, "
    "offsets, and locks after a crash — and would have to distinguish a "
    "client that had crashed from one that was merely slow, which &sect;1 "
    "says it cannot.",
    "<b>The price is paid in semantics.</b> Every operation must be "
    "idempotent, because clients retry. There is no server-side locking in "
    "the base protocol. And the Unix behaviour of deleting an open file "
    "(Module 08) cannot work, because the server does not know the file is "
    "open — NFS clients fake it by renaming the file to a hidden name, "
    "which is why stray <code>.nfs*</code> files appear."]),
  ("h2", "3.2 &nbsp; Caching and consistency"),
  ("callout", "Caching forces a choice you cannot avoid",
   ["Without client-side caching, every read is a network round trip. The "
    "result is correct and unusably slow.",
    "With caching, a client can read data that another client has already "
    "changed. Correctness has been traded for speed, and the only question is "
    "how much.",
    "<b>NFS chose close-to-open consistency:</b> a client that opens a file "
    "after another client closed it sees that client's writes. Within an open "
    "session, no guarantee. This is substantially weaker than local file "
    "semantics and sufficient for the dominant use case of one writer at a "
    "time.",
    "<b>AFS chose callbacks:</b> the server records which clients hold cached "
    "copies and notifies them when a copy becomes invalid. The consistency is "
    "much stronger — and the server is now stateful, which is precisely "
    "what NFS avoided, so crash recovery requires rebuilding the callback "
    "table.",
    "There is no design that is simultaneously fast, strongly consistent, and "
    "simple to recover. This is the CAP trade-off appearing in a small and "
    "concrete setting."]),
  ("table", ["", "NFS", "AFS"],
   [["Server state", "<b>None.</b>",
     "Tracks which clients cache which files."],
    ["Consistency", "Close-to-open.", "Callbacks — near-local."],
    ["Crash recovery", "<b>Trivial</b> — just restart.",
     "Must rebuild callback state; clients must revalidate."],
    ["Caching granularity", "Blocks.",
     "Whole files, cached to local disk — designed for a campus-scale "
     "network with high latency."],
    ["Scalability", "Good.",
     "<b>Better</b> — whole-file caching means far fewer round trips."]],
   [0.19, 0.38, 0.43]),

  ("h1", "4 &nbsp; What generalises"),
  ("ol", ["<b>Make operations idempotent.</b> Then retrying is always safe, "
          "and the impossibility of exactly-once delivery stops being a "
          "problem. This is the single most valuable technique in the module.",
          "<b>Do not hide the network.</b> An abstraction that makes remote "
          "calls indistinguishable from local ones encourages every fallacy "
          "in &sect;2.1. Make latency and failure visible in the interface "
          "— which is why modern RPC frameworks expose deadlines, "
          "retries, and explicit error types.",
          "<b>Choose a consistency model deliberately and document it.</b> "
          "Every distributed system has one whether or not anyone wrote it "
          "down, and an undocumented one is discovered by users.",
          "<b>Treat partial failure as normal.</b> In a distributed system, "
          "some component is always down. Code that handles this only as an "
          "exceptional path will spend most of its life on that path."]),
  ("p", "CSCE 662 and CSCE 678 develop all of this properly — consensus, "
        "replication, consistency models, and the impossibility results that "
        "bound what is achievable. This module's purpose is to show where the "
        "operating system's abstractions stop working, and why."),
 ],
 "resources": [
   ("OSTEP — Chapters 48&ndash;50 (Distributed Systems, NFS, AFS)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "RPC, NFS's statelessness, and the AFS comparison, written clearly."),
   ("MIT 6.5840 Distributed Systems (free lectures and labs)",
    "https://pdos.csail.mit.edu/6.824/",
    "The natural follow-on. Build Raft and a fault-tolerant key-value store."),
   ("Waldo et al. — A Note on Distributed Computing (free)",
    "https://scholar.harvard.edu/files/waldo/files/waldo-94.pdf",
    "The classic argument that local and remote objects cannot be unified. "
    "Short, and it settled the question."),
   ("Deutsch & Gosling — The Eight Fallacies of Distributed Computing",
    "https://nighthacks.com/jag/res/Fallacies.html",
    "The original list, with commentary."),
 ],
 "exercises": [
   "Implement a simple RPC mechanism over TCP: marshal arguments, send, "
   "block, unmarshal the reply. Then add a timeout and decide what to do when "
   "it expires.",
   "Demonstrate the slow-versus-dead problem: make the server sleep longer "
   "than the client's timeout and observe the client retrying an operation "
   "that is still executing.",
   "Implement at-least-once semantics with retries. Use a non-idempotent "
   "operation and demonstrate the duplicate effect.",
   "Add a deduplication key and server-side duplicate detection. Demonstrate "
   "that retries are now harmless.",
   "Set up an NFS mount between two machines or VMs. Write from one and read "
   "from the other, and determine experimentally when changes become "
   "visible.",
   "Delete a file on an NFS mount while a process on another client has it "
   "open. Observe the <code>.nfs*</code> file and explain it.",
   "Measure the cost of close-to-open consistency: time a workload that "
   "opens, reads, and closes repeatedly against one that holds the file "
   "open.",
 ],
 "selfcheck": [
   "Give four ways a remote call differs from a local one.",
   "Why can a client not distinguish a slow server from a dead one, and what "
   "follows from that?",
   "Define at-most-once, at-least-once, and exactly-once, and say which is "
   "impossible.",
   "How do systems that advertise exactly-once semantics actually work?",
   "Why is the NFS server stateless, and what three things does that cost?",
   "What consistency model does NFS provide, and how does AFS differ?",
   "Name four of the eight fallacies and say why RPC transparency invites "
   "them.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Kernel Design",
 "subtitle": "Monolithic, micro, and what the argument was really about.",
 "question": "Where should the boundary between kernel and user code be?",
 "outcomes": [
     "Compare monolithic and microkernel designs on concrete criteria.",
     "Explain why IPC cost decided the historical argument.",
     "Explain formal verification and what seL4 achieves.",
     "Explain modern hybrids: modules, eBPF, unikernels.",
     "Judge kernel design choices against workload requirements.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The question",
   "blurb": "Which code must be trusted?"},

  {"t": "two", "kicker": "Two answers", "title": "Monolithic and micro",
   "lh": "Monolithic",
   "l": ["Drivers, file systems, network stack — all in kernel mode.",
         "A service call is a <b>function call</b>.",
         "Fast.",
         "<b>A driver bug can corrupt anything.</b>",
         ("Trusted computing base: millions of lines.", 1)],
   "rh": "Microkernel",
   "r": ["Only IPC, scheduling, and address spaces in the kernel.",
         "A service call is <b>IPC to another process</b>.",
         "Slower — how much slower is the whole argument.",
         "A driver crash kills one process.",
         ("Trusted computing base: ~10,000 lines.", 1)]},

  {"t": "callout", "title": "The argument was about IPC cost",
   "kind": "Why monolithic won",
   "body": ["A microkernel replaces function calls with IPC. If IPC is "
            "expensive, every file read pays for it.",
            "First-generation microkernels (Mach) had IPC costs of thousands "
            "of cycles, and the performance penalty was severe enough to "
            "settle the argument in practice.",
            "<b>Liedtke's L4 showed this was an implementation failure, not "
            "an inherent one</b> — careful design brought IPC to a few "
            "hundred cycles, an order of magnitude better.",
            "By then Linux and Windows NT had won on other grounds. The "
            "microkernel argument was <i>right</i> and <i>late</i>, which is "
            "a common fate in systems."]},

  {"t": "section", "label": "Part 2", "title": "Where microkernels won",
   "blurb": "Not on the desktop."},

  {"t": "table", "kicker": "Deployed", "title": "Microkernels in production",
   "header": ["System", "Where", "Why it won there"],
   "widths": [2.6, 4.2, 5.3],
   "rows": [
     ["QNX", "Cars, medical, industrial", "Isolation and real-time guarantees"],
     ["seL4", "Defence, aviation", "<b>Formally verified</b>"],
     ["L4 family", "Billions of phone basebands", "Isolation from the application processor"],
     ["Fuchsia (Zircon)", "Google devices", "Driver isolation; updatable drivers"],
   ],
   "note": "The phone baseband case is the biggest deployment nobody knows "
           "about."},

  {"t": "callout", "title": "seL4: a kernel with a proof",
   "kind": "The strongest result",
   "body": ["seL4 is <b>formally verified</b>: a machine-checked proof that "
            "the C implementation satisfies its specification.",
            "The proof covers functional correctness, and extends to "
            "integrity and confidentiality enforcement.",
            "No buffer overflows, no null dereferences, no undefined "
            "behaviour — not 'none found', but <i>none exist</i>, proven.",
            "It is possible because the kernel is about 10,000 lines. The "
            "proof is roughly 200,000 lines of Isabelle. <b>That ratio is why "
            "nobody has verified Linux.</b>",
            "A small trusted computing base is not only easier to audit "
            "— it is the precondition for proving anything at all."]},

  {"t": "section", "label": "Part 3", "title": "What actually happened",
   "blurb": "Both sides got most of what they wanted."},

  {"t": "table", "kicker": "Convergence", "title": "Monolithic kernels adopted microkernel ideas",
   "header": ["Mechanism", "What it gives", "Microkernel idea"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Loadable modules", "Drivers loaded and unloaded at runtime", "Modularity"],
     ["FUSE", "File systems as user processes", "Services outside the kernel"],
     ["User-space drivers", "USB, GPU, network in user space", "Driver isolation"],
     ["eBPF", "Verified programs extending the kernel safely", "<b>Safe extension</b>"],
     ["Hypervisors", "A tiny trusted layer under the kernel", "A small TCB"],
   ],
   "note": "eBPF is the most interesting: it is a verifier, not a process "
           "boundary, achieving safety a different way."},

  {"t": "callout", "title": "eBPF: a third answer",
   "kind": "The modern development",
   "body": ["The microkernel question was 'should extensions run in a "
            "separate address space?' eBPF answers differently: <b>run them "
            "in the kernel, but prove they are safe first</b>.",
            "A verifier checks that the program terminates, accesses only "
            "permitted memory, and respects type constraints — before it "
            "is allowed to load.",
            "The result: kernel-speed extension with no process boundary and "
            "no trust required. Used for networking, tracing, security "
            "policy, and scheduling.",
            "It is neither monolithic nor microkernel. It is a static "
            "guarantee replacing a runtime boundary, which is a genuinely "
            "new answer to a forty-year-old question."]},

  {"t": "bullets", "kicker": "Unikernels", "title": "The other direction entirely",
   "items": [
     "<b>Unikernel:</b> compile the application and the OS into a single "
     "binary with one address space.",
     "",
     "No kernel/user boundary at all. No system calls — just function "
     "calls.",
     "",
     "<b>Rationale:</b> in a VM running one application, the kernel's "
     "protection and multiplexing are redundant. The hypervisor already "
     "isolates.",
     "",
     "Tiny, fast to boot, minimal attack surface — and difficult to "
     "debug, with no process model.",
   ],
   "footnote": "A reminder that 'what is the kernel for' has a different "
               "answer when it serves exactly one program."},

  {"t": "table", "kicker": "Judgement", "title": "Choosing a design",
   "header": ["Requirement", "Design"],
   "widths": [5.6, 6.5],
   "rows": [
     ["General-purpose, broad hardware support", "Monolithic with modules"],
     ["Safety certification or formal proof", "<b>Microkernel</b> — seL4"],
     ["Hard real-time with isolation", "Microkernel — QNX"],
     ["Multi-tenant cloud", "Hypervisor + lightweight VMs"],
     ["One application per VM", "Unikernel, or a thin library OS"],
   ],
   "note": "The honest conclusion: the right design depends entirely on what "
           "must be trusted and what must be guaranteed."},

  {"t": "bullets", "kicker": "End", "title": "Where this course leaves you",
   "items": [
     "You have written context switching, a scheduler, virtual memory, system "
     "calls, and a journaling file system.",
     "You know what every illusion costs and where each one leaks.",
     "You can read kernel source and know what you are looking at.",
     "",
     "<b>CSCE 614</b> was the hardware under all of this.",
     "<b>CSCE 662 / 678</b> take Module 12 seriously.",
     "<b>CSCE 713</b> takes Module 11 seriously.",
     "<b>CSCE 735</b> takes concurrency to many cores.",
   ]},
 ],
 "takeaways": [
   "Monolithic kernels make a service call a function call; microkernels make "
   "it IPC. The whole argument was about what IPC costs.",
   "First-generation microkernel IPC was slow enough to settle the argument; "
   "L4 showed that was an implementation failure, not an inherent one.",
   "Microkernels won where isolation and certification matter: cars, medical "
   "devices, aviation, and billions of phone basebands.",
   "seL4 is formally verified — and that is only possible because it is "
   "10,000 lines. A small TCB is the precondition for proof.",
   "Monolithic kernels adopted most microkernel ideas anyway: modules, FUSE, "
   "user-space drivers, hypervisors.",
   "eBPF is a third answer: run extensions in the kernel, but verify safety "
   "statically rather than enforcing it with a process boundary.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The question"),
  ("p", "Every operating system must decide which code runs with full "
        "privilege. That code is the <b>trusted computing base</b>: a bug "
        "anywhere in it can compromise everything."),
  ("table", ["", "Monolithic", "Microkernel"],
   [["In kernel mode", "Scheduling, memory, file systems, device drivers, "
     "network stack, and more.",
     "Only IPC, scheduling, and address space management."],
    ["Everything else", "—",
     "Ordinary user processes: drivers, file systems, network stack."],
    ["A service request is", "A function call.",
     "An IPC message to another process."],
    ["Performance", "Fast.",
     "Depends entirely on IPC cost — see &sect;2."],
    ["A driver bug", "Can corrupt any kernel data structure, including "
     "another subsystem's.",
     "Kills one user process; the system continues."],
    ["Trusted computing base", "Millions of lines.", "~10,000 lines."],
    ["Examples", "Linux, Windows NT, FreeBSD, xv6.",
     "seL4, QNX, Minix 3, L4 family."]],
   [0.17, 0.42, 0.41]),

  ("h1", "2 &nbsp; Why monolithic kernels won the desktop"),
  ("callout", "The argument was decided by IPC cost",
   ["In a microkernel, every file read becomes at least one IPC round trip to "
    "the file system process, which may itself IPC to the driver process. A "
    "function call becomes several context switches.",
    "First-generation microkernels — Mach above all — had IPC costs "
    "in the thousands of cycles. The resulting performance penalty was large "
    "enough to decide the matter in practice, and it is why the "
    "Tanenbaum&ndash;Torvalds debate of 1992 was settled by the market rather "
    "than by argument.",
    "<b>Jochen Liedtke demonstrated this was an implementation failure, not "
    "a structural one.</b> By designing L4 around IPC from the beginning "
    "— minimal message formats, careful register use, no unnecessary "
    "copying — he reduced the cost by roughly an order of magnitude, to "
    "a few hundred cycles.",
    "By that point Linux and Windows NT had established themselves on other "
    "grounds entirely: hardware support, developer familiarity, and momentum. "
    "The microkernel case was correct and arrived too late, which is a "
    "recurring pattern in systems research."]),

  ("h1", "3 &nbsp; Where microkernels did win"),
  ("table", ["System", "Deployment", "Why it won there"],
   [["<b>QNX</b>", "Automotive infotainment and control, medical devices, "
     "industrial automation.",
     "Fault isolation and hard real-time guarantees. A failing component must "
     "not take the system down, and certification requires being able to "
     "argue that it cannot."],
    ["<b>seL4</b>", "Defence, avionics, high-assurance systems.",
     "<b>Formal verification.</b> See below."],
    ["<b>L4 family</b>", "Billions of mobile phone basebands.",
     "The baseband processor runs proprietary firmware that must be isolated "
     "from the application processor. This is quietly the largest microkernel "
     "deployment in existence."],
    ["<b>Zircon (Fuchsia)</b>", "Google devices.",
     "Driver isolation and independently updatable drivers — a direct "
     "response to Android's difficulty in shipping kernel updates across "
     "vendors."]],
   [0.17, 0.36, 0.47]),
  ("callout", "seL4 and what verification actually means",
   ["seL4 carries a machine-checked proof that its C implementation satisfies "
    "its formal specification, together with proofs of integrity and "
    "confidentiality enforcement.",
    "This is categorically stronger than extensive testing. There are no "
    "buffer overflows, no null pointer dereferences, no undefined behaviour "
    "— not 'none have been found', but <i>none exist</i>, demonstrated "
    "mathematically.",
    "It is achievable because the kernel is roughly 10,000 lines. The proof "
    "is around 200,000 lines of Isabelle/HOL and took person-decades. "
    "<b>That ratio is precisely why nobody has verified Linux</b>, and it "
    "will not change.",
    "The lesson generalises: a small trusted computing base is not merely "
    "easier to audit, it is the precondition for proving anything about the "
    "system at all. Architecture determines what assurance is even "
    "possible."]),

  ("break",),
  ("h1", "4 &nbsp; What actually happened: convergence"),
  ("p", "The interesting outcome is that monolithic kernels adopted most of "
        "the microkernel programme without adopting the architecture."),
  ("table", ["Mechanism", "What it provides", "The microkernel idea it adopts"],
   [["<b>Loadable modules</b>", "Drivers and file systems loaded and unloaded "
     "at runtime rather than compiled in.",
     "Modularity — though still in kernel mode, so without the isolation."],
    ["<b>FUSE</b>", "File systems implemented as ordinary user processes.",
     "Services outside the kernel. sshfs, s3fs, and many others rely on this."],
    ["<b>User-space drivers</b>", "USB, GPU, and high-performance networking "
     "drivers substantially in user space.",
     "Driver isolation. DPDK and SPDK bypass the kernel entirely for "
     "performance, which is the microkernel argument made for speed rather "
     "than safety."],
    ["<b>eBPF</b>", "Sandboxed, verified programs that extend kernel "
     "behaviour.", "<b>Safe extension</b> — see below."],
    ["<b>Hypervisors</b>", "A small, carefully audited layer beneath the "
     "kernel.",
     "A minimal trusted computing base. Arguably the microkernel idea "
     "succeeding under a different name."]],
   [0.20, 0.38, 0.42]),
  ("callout", "eBPF is a genuinely different answer",
   ["The microkernel question was: <i>should extensions run in a separate "
    "address space?</i> eBPF answers a different question: <i>can we run them "
    "in the kernel but prove in advance that they are safe?</i>",
    "Before an eBPF program is loaded, a verifier establishes that it "
    "terminates (no unbounded loops), that every memory access is within "
    "permitted bounds, that types are respected, and that it cannot crash the "
    "kernel. Only then is it accepted.",
    "The outcome is kernel-speed extension with no process boundary, no IPC, "
    "and no trust placed in the program's author. It is used for packet "
    "filtering and routing, tracing and observability, security policy "
    "enforcement, and increasingly for scheduling.",
    "This is neither monolithic nor microkernel: it replaces a <i>runtime</i> "
    "isolation boundary with a <i>static</i> guarantee. After forty years of "
    "the same argument, that is a genuinely new position."]),
  ("h2", "4.1 &nbsp; Unikernels: the opposite direction"),
  ("p", "A <b>unikernel</b> compiles the application together with just the "
        "operating system functionality it needs into a single binary running "
        "in one address space, usually directly on a hypervisor."),
  ("p", "There is no kernel/user boundary and no system call mechanism "
        "— a 'system call' is a function call. The reasoning is that in "
        "a virtual machine dedicated to one application, the kernel's "
        "protection and multiplexing are redundant: the hypervisor already "
        "provides isolation, and there is no second program to be protected "
        "from."),
  ("p", "The result boots in milliseconds, occupies a few megabytes, and "
        "presents a minimal attack surface. The costs are real: debugging is "
        "difficult, there is no process model, and the tooling is immature. "
        "It is a useful reminder that 'what is a kernel for' has a different "
        "answer when it serves exactly one program."),

  ("h1", "5 &nbsp; Judging a design"),
  ("table", ["Requirement", "Appropriate design", "Reason"],
   [["General-purpose computing, broad hardware support.",
     "Monolithic with loadable modules.",
     "Performance and the enormous driver ecosystem. Linux and Windows."],
    ["Safety certification or formal assurance.", "Microkernel — seL4.",
     "A small TCB is the precondition for proof."],
    ["Hard real-time with fault isolation.", "Microkernel — QNX.",
     "Bounded latency and the ability to argue that a component failure is "
     "contained."],
    ["Multi-tenant cloud running untrusted code.",
     "Hypervisor with lightweight VMs.",
     "A small, hardware-assisted isolation boundary (Module 11)."],
    ["One application per virtual machine.", "Unikernel or library OS.",
     "The protection the kernel provides is redundant."]],
   [0.28, 0.26, 0.46]),
  ("callout", "Where this course leaves you",
   ["You have written a context switch in assembly, replaced a scheduler, "
    "implemented demand paging and copy-on-write, added system calls, and "
    "made a file system survive crashes. Those are the things an operating "
    "system is.",
    "More usefully, you know what the illusions cost and where each one "
    "leaks: that a write is not durable until fsync, that a context switch "
    "costs more in cold cache than in registers, that a container is a "
    "process with flags, and that no timeout distinguishes slow from dead.",
    "<b>CSCE 614</b> was the hardware beneath all of it. <b>CSCE 662</b> and "
    "<b>678</b> take Module 12 seriously and build real distributed systems. "
    "<b>CSCE 713</b> takes Module 11 seriously. <b>CSCE 735</b> takes the "
    "concurrency of Modules 04 and 05 to many cores.",
    "And you can now read kernel source and know what you are looking at, "
    "which is the thing that actually transfers."]),
 ],
 "resources": [
   ("Klein et al. — seL4: Formal Verification of an OS Kernel (free)",
    "https://sel4.systems/About/seL4-whitepaper.pdf",
    "What was proved, how, and what it cost. The most significant result in "
    "kernel design in decades."),
   ("Liedtke — On micro-kernel construction (free)",
    "https://dl.acm.org/doi/10.1145/224056.224075",
    "The paper that showed microkernel IPC could be fast, and why the first "
    "generation was not."),
   ("The Tanenbaum&ndash;Torvalds debate (1992, archived)",
    "https://www.oreilly.com/openbook/opensources/book/appa.html",
    "The original argument, in full. Worth reading for how both sides were "
    "partly right."),
   ("Brendan Gregg — eBPF resources",
    "https://www.brendangregg.com/ebpf.html",
    "What eBPF can actually do, from someone who uses it daily."),
   ("Madhavapeddy et al. — Unikernels: Library Operating Systems for "
    "the Cloud (free)",
    "https://anil.recoil.org/papers/2013-asplos-mirage.pdf",
    "The case for collapsing the boundary entirely."),
 ],
 "exercises": [
   "Measure xv6's system call overhead: time a null system call and compare "
   "against a null function call. Compute the ratio.",
   "Implement a trivial FUSE file system in user space. Measure its "
   "throughput against the equivalent kernel file system and attribute the "
   "difference.",
   "Write and load an eBPF program that counts system calls by number. Note "
   "what the verifier rejects before it accepts your program.",
   "Count the lines of code in xv6 by subsystem, then in seL4, then in the "
   "Linux kernel. Plot trusted computing base size against the three designs "
   "and consider what is being traded.",
   "Read the Tanenbaum&ndash;Torvalds debate and write a one-page assessment "
   "of which predictions held, now that you have built a kernel.",
   "Take one subsystem you implemented in this course and sketch how it would "
   "be structured in a microkernel. Identify every place a function call "
   "becomes IPC and estimate the cost.",
   "<b>Project 2 is now due.</b> Complete the virtual memory and crash-"
   "consistent file system work described in the syllabus, including the "
   "hundred-run crash injection results.",
 ],
 "selfcheck": [
   "What runs in kernel mode in each design, and what does a service request "
   "cost in each?",
   "Why did monolithic kernels win, and in what sense was the microkernel "
   "argument correct?",
   "Name three places microkernels are deployed in production and why each "
   "chose one.",
   "What does seL4's verification establish, and why is it only possible for "
   "a small kernel?",
   "Name four microkernel ideas that monolithic kernels adopted.",
   "How does eBPF differ from both designs, and what does it replace a "
   "runtime boundary with?",
   "When would a unikernel be the right choice, and what is given up?",
 ],
},

]
