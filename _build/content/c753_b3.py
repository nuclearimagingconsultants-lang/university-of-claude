# -*- coding: utf-8 -*-
"""CSCE 753 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Learned Representations",
 "subtitle": "What a network learns about images, and what to reuse.",
 "question": "Why does a model trained on one task help on another?",
 "outcomes": [
     "Explain what convolutional features represent at each depth.",
     "Explain transfer learning and choose a transfer strategy.",
     "Explain receptive field and why it constrains architecture.",
     "Explain the role of resolution in vision models.",
     "State what learned features cannot do.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What the layers learn",
   "blurb": "A hierarchy that was designed and turns out to be learned."},

  {"t": "table", "kicker": "Hierarchy", "title": "What is found at each depth",
   "header": ["Depth", "What the filters respond to", "Comment"],
   "widths": [2.3, 4.5, 5.2],
   "rows": [
     ["<b>Layer 1</b>", "<b>Oriented edges and colour blobs</b>", "<b>Gabor-like. Essentially always, in every model</b>"],
     ["<b>Layer 2–3</b>", "Corners, junctions, textures", "<b>Recognisably the features of Module 03</b>"],
     ["<b>Mid depth</b>", "<b>Parts — wheels, eyes, text-like patterns</b>", "<b>The most transferable layers</b>"],
     ["<b>Late</b>", "<b>Object-like and category-specific</b>", "Tied to the training task"],
     ["<b>Final</b>", "The classes themselves", "<b>Discard on transfer</b>"],
   ],
   "footnote": "<b>Layer 1 learning Gabor filters is the clearest "
               "evidence that the hierarchy is a property of natural "
               "images</b>, not of the architecture — it happens "
               "regardless of task.",
   "note": "That the first layer is always the same is genuinely "
           "striking and worth dwelling on."},

  {"t": "callout", "title": "Learned early layers rediscovered hand-designed ones",
   "kind": "The result that should surprise you",
   "body": ["<b>The first convolutional layer learns oriented edge and "
            "colour-opponent filters</b> — which is what Gabor "
            "filters are, and what SIFT's gradient histograms were built "
            "from.",
            "<b>Nobody put them there.</b> They fall out of gradient "
            "descent on natural images under essentially any "
            "objective.",
            "<b>So the hand-designed features of Module 03 were not "
            "arbitrary</b> — decades of design converged on roughly "
            "the right primitives, which is why learned descriptors beat "
            "SIFT only modestly (M03 §4).",
            "<b>What learning added was the middle.</b> <b>Parts and "
            "configurations were never successfully hand-designed</b>, "
            "and that is where the gains are."]},

  {"t": "section", "label": "Part 2", "title": "Transfer",
   "blurb": "Reusing a representation, and choosing how much."},

  {"t": "code", "kicker": "Transfer", "title": "The decision, by data volume",
   "lang": "text", "code": """
  < 1000 labelled images
      FREEZE the backbone, train a linear head only.
      Anything more overfits. A linear probe on good
      features is a strong baseline and is frequently
      enough.

  1k - 10k images
      Fine-tune the LAST FEW BLOCKS, freeze the rest.
      Use a learning rate 10x lower than from scratch --
      the features are already good and large steps
      destroy them.

  10k - 100k images
      Fine-tune EVERYTHING, with a layer-wise decaying
      learning rate: lowest at layer 1, highest at the
      head. Early layers need almost no change (Part 1).

  > 100k images
      Fine-tuning still beats training from scratch, but
      the margin narrows. Pretraining is buying you
      optimisation speed more than final accuracy here.

  ALWAYS: compare against the FROZEN linear probe. If
  fine-tuning does not beat it, you are overfitting and
  reporting it as progress -- CSCE 633 Module 03's lesson,
  in the exact form it takes in vision.
""",
   "caption": "<b>The linear probe is the baseline that keeps transfer "
              "honest</b>, and it is one line of code.",
   "note": "The linear-probe-as-baseline habit is the most useful thing "
           "in this module."},

  {"t": "section", "label": "Part 3", "title": "Receptive field",
   "blurb": "What a unit can possibly see."},

  {"t": "callout", "title": "A unit cannot respond to anything outside its receptive field",
   "kind": "The architectural constraint",
   "body": ["<b>The receptive field is the region of the input that can "
            "influence a given unit</b>, and it grows with depth, stride, "
            "and dilation.",
            "<b>If your object spans 200 pixels and the receptive field "
            "is 80, no single unit can see the whole object</b> — "
            "and no amount of training fixes that.",
            "<b>So compute it.</b> It is a short recurrence over the "
            "layers, and <b>a mismatch between object scale and "
            "receptive field is a common, invisible architectural "
            "error.</b>",
            "<b>The <i>effective</i> receptive field is smaller than the "
            "theoretical one</b> — contributions fall off roughly as "
            "a Gaussian from the centre — so build in margin rather "
            "than matching exactly."]},

  {"t": "bullets", "kicker": "Resolution", "title": "Why resolution matters more in vision than elsewhere",
   "items": [
     "<b>Small objects occupy few pixels</b>, and after four "
     "downsamplings a 32-pixel object is 2 pixels. <b>It is gone.</b>",
     "",
     "<b>So detection at multiple scales needs features at multiple "
     "resolutions</b> — which is what feature pyramid networks "
     "exist for, and it is Module 03's scale pyramid again.",
     "",
     "<b>Compute scales quadratically with resolution</b>, so "
     "resolution is the most expensive single choice.",
     "",
     "<b>And training and test resolution must match</b>, or the "
     "apparent object scale shifts and accuracy drops for no visible "
     "reason.",
     "",
     "<b>Which is a distribution shift</b> (Module 12) <b>that you "
     "introduced yourself in the data pipeline.</b>",
   ],
   "footnote": "<b>The train/test resolution mismatch is a real and "
               "frequent bug</b>, and it presents as a mysterious "
               "accuracy gap rather than as an error."},

  {"t": "section", "label": "Part 4", "title": "Limits",
   "blurb": "What this representation does not give you."},

  {"t": "callout", "title": "What learned features cannot do",
   "kind": "Stated plainly",
   "body": ["<b>They do not give metric geometry.</b> A network can "
            "estimate relative depth well and absolute scale not at all "
            "— <b>Module 01's theorem binds learned methods exactly "
            "as hard as geometric ones.</b>",
            "<b>They do not generalise outside their training "
            "distribution</b>, and the degradation is not graceful or "
            "predictable (Module 12).",
            "<b>They do not provide uncertainty</b> without explicit "
            "effort — softmax confidence is not calibrated "
            "(CSCE 633 M12 §3).",
            "<b>And they are not interpretable in the way the "
            "hierarchy picture suggests.</b> <b>The clean 'edges, parts, "
            "objects' story is a partial truth</b>, assembled from "
            "visualisations that select for interpretability, and it "
            "should be held loosely."]},
 ],
 "takeaways": [
   "Convolutional layers learn edges, then textures, then parts, then "
   "object-like features — and the first layer is Gabor-like in every "
   "model regardless of task.",
   "That convergence shows the hand-designed features of Module 03 were "
   "close to right, and that learning's contribution was the middle of the "
   "hierarchy.",
   "Transfer strategy follows from labelled data volume, and the frozen "
   "linear probe is the baseline that keeps it honest.",
   "A unit cannot respond to anything outside its receptive field, so "
   "object scale and receptive field must be matched deliberately.",
   "Resolution is the most expensive architectural choice and the "
   "train/test resolution mismatch is a self-inflicted distribution shift.",
   "Learned features do not give metric scale, do not degrade gracefully "
   "off-distribution, and are less interpretable than the hierarchy picture "
   "suggests.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What the layers learn"),
  ("table", ["Depth", "What the filters respond to", "Comment"],
   [["<b>Layer 1</b>", "<b>Oriented edges and colour-opponent blobs.</b>",
     "<b>Gabor-like, essentially always, in every architecture and "
     "under almost any training objective.</b> See the callout."],
    ["<b>Layers 2–3</b>", "Corners, junctions, simple textures.",
     "<b>Recognisably the features of Module 03</b> — the Harris "
     "corner response has a clear analogue here."],
    ["<b>Mid depth</b>",
     "<b>Object parts — wheels, eyes, text-like patterns, "
     "characteristic textures.</b>",
     "<b>The most transferable layers</b>, and the part that was never "
     "successfully hand-designed."],
    ["<b>Late layers</b>",
     "<b>Object-like and increasingly category-specific.</b>",
     "Tied to the training task, so less transferable the further the "
     "target task is from the source."],
    ["<b>Final layer</b>", "The training classes themselves.",
     "<b>Discard on transfer</b>; it encodes the source label set and "
     "nothing more."]],
   [0.14, 0.42, 0.44]),
  ("callout", "Learned early layers rediscovered hand-designed ones",
   ["<b>The first convolutional layer reliably learns oriented edge "
    "detectors and colour-opponent filters</b> — which is what Gabor "
    "filters are, and what SIFT's gradient-orientation histograms were "
    "built out of.",
    "<b>Nobody put them there.</b> They emerge from gradient descent on "
    "natural images under classification, under self-supervision "
    "(Module 10), and under reconstruction objectives alike. <b>The "
    "hierarchy is a property of natural image statistics, not of the "
    "architecture or the task.</b>",
    "<b>So the hand-designed features of Module 03 were not "
    "arbitrary.</b> Decades of design converged on approximately the "
    "right primitives, <b>which is exactly why learned descriptors beat "
    "SIFT only modestly</b> (Module 03 &sect;4) — a result that is "
    "puzzling until this module and obvious after it.",
    "<b>What learning added was the middle of the hierarchy.</b> <b>Parts "
    "and their configurations were never successfully hand-designed</b> "
    "— the attempts (deformable part models, constellation models) "
    "were ingenious and did not scale — <b>and that is where the "
    "gains in recognition came from</b>. Knowing which part of the stack "
    "learning actually contributed is more useful than the general claim "
    "that it works."]),

  ("h1", "2 &nbsp; Transfer"),
  ("code", """UNDER 1000 LABELLED IMAGES
    FREEZE the backbone and train a linear head only.
    Anything more overfits. A linear probe on good
    features is a strong baseline and frequently enough.

1k - 10k IMAGES
    Fine-tune the LAST FEW BLOCKS, freeze the rest. Use a
    learning rate about 10x lower than you would train
    from scratch -- the features are already good and
    large steps destroy them before the head can adapt.

10k - 100k IMAGES
    Fine-tune EVERYTHING with a layer-wise decaying
    learning rate: lowest at layer 1, highest at the head.
    Early layers need almost no change (section 1).

OVER 100k IMAGES
    Fine-tuning still beats training from scratch, but the
    margin narrows. Here pretraining is mostly buying
    optimisation speed rather than final accuracy.

ALWAYS: compare against the FROZEN LINEAR PROBE. If
fine-tuning does not beat it, you are overfitting and
reporting it as progress. That is CSCE 633 Module 03's
lesson in the exact form it takes in vision, and the probe
costs one line of code."""),

  ("h1", "3 &nbsp; Receptive field and resolution"),
  ("callout", "A unit cannot respond to anything outside its receptive field",
   ["<b>The receptive field is the region of the input image that can "
    "influence a given unit's activation</b>, and it grows with depth, "
    "with stride, and with dilation — computable by a short "
    "recurrence over the layers.",
    "<b>If the object you need to recognise spans 200 pixels and the "
    "receptive field at your decision layer is 80 pixels, no single unit "
    "can see the whole object</b>, and <b>no amount of training or data "
    "fixes it</b>. The information is not available to that unit.",
    "<b>So compute it rather than assuming it.</b> <b>A mismatch "
    "between object scale and receptive field is a common and completely "
    "invisible architectural error</b> — the model trains, the loss "
    "decreases, and the ceiling is structural.",
    "<b>And the <i>effective</i> receptive field is considerably smaller "
    "than the theoretical one</b>: contributions fall off roughly as a "
    "Gaussian from the centre, because there are far more paths through "
    "the network to the centre than to the periphery. <b>So build in "
    "margin rather than matching the theoretical figure exactly</b>, and "
    "prefer architectures with explicit global context (pooling, "
    "attention) when the task needs it."]),
  ("ul", ["<b>Small objects occupy few pixels</b>, and after four "
          "stride-2 downsamplings a 32-pixel object occupies 2 pixels in "
          "the feature map. <b>It is effectively gone</b>, and the "
          "detector's small-object performance reflects exactly that.",
          "<b>So detection across scales needs features at multiple "
          "resolutions</b> — which is what feature pyramid networks "
          "exist for, and <b>it is Module 03's scale pyramid "
          "again</b>, arrived at independently and for the same reason.",
          "<b>Compute scales quadratically with input resolution</b>, so "
          "<b>resolution is the single most expensive architectural "
          "choice</b> and deserves to be chosen from the smallest object "
          "that must be detected rather than by convention.",
          "<b>And the training and test resolution must match.</b> If "
          "you train on 224-pixel crops of 256-pixel images and test on "
          "full 512-pixel images, <b>the apparent object scale shifts and "
          "accuracy drops for no visible reason</b> — which is "
          "<b>a distribution shift</b> (Module 12) <b>that you "
          "introduced yourself, in the data pipeline, with no model "
          "defect at all</b>. It is a frequent bug and it presents as a "
          "mysterious accuracy gap rather than as an error."]),

  ("break",),
  ("h1", "4 &nbsp; What learned features cannot do"),
  ("callout", "Stated plainly",
   ["<b>They do not give metric geometry.</b> A network can estimate "
    "relative depth within a scene quite well and absolute scale not at "
    "all — because <b>Module 01's scale theorem binds learned "
    "methods exactly as hard as geometric ones</b>. A monocular depth "
    "network that appears to output metric depth has learned the typical "
    "size of objects in its training distribution, which is a prior and "
    "fails on an unusual room.",
    "<b>They do not generalise outside their training distribution</b>, "
    "and <b>the degradation is neither graceful nor predictable</b> "
    "— performance can fall sharply on a shift that looks minor to a "
    "person. This is Module 12's entire subject.",
    "<b>They do not provide usable uncertainty without explicit "
    "effort.</b> <b>Softmax confidence is not calibrated</b> (CSCE 633 "
    "Module 12 &sect;3), and a confidently wrong detection is "
    "indistinguishable from a confidently right one at the interface.",
    "<b>And they are less interpretable than &sect;1's clean hierarchy "
    "suggests.</b> <b>The 'edges, then parts, then objects' story is a "
    "partial truth assembled from visualisations that select for "
    "interpretability</b> — the units that produce legible "
    "visualisations are a minority, many units are polysemantic, and the "
    "story is a useful organising picture rather than a description of "
    "the whole network. <b>Hold it loosely, and do not use it to justify "
    "a claim about why a particular prediction was made.</b>"]),
 ],
 "resources": [
   ("Michigan EECS 498 — CNN architectures and transfer lectures "
    "(free)",
    "https://web.archive.org/web/20260824025044/https://web.eecs.umich.edu/~justincj/teaching/eecs498/",
    "<b>The reference for this module.</b> The transfer-learning lecture "
    "covers &sect;2 directly."),
   ("Zeiler & Fergus — Visualizing and Understanding Convolutional "
    "Networks (free)",
    "https://arxiv.org/abs/1311.2901",
    "<b>Where &sect;1's hierarchy picture comes from</b>, and worth "
    "reading alongside &sect;4's caveat about it."),
   ("Araujo, Norris & Sim — Computing Receptive Fields of "
    "Convolutional Neural Networks (free, Distill)",
    "https://distill.pub/2019/computing-receptive-fields/",
    "<b>The &sect;3 recurrence, worked out</b>, with interactive "
    "calculators."),
   ("Touvron et al. — Fixing the train-test resolution discrepancy "
    "(free)",
    "https://arxiv.org/abs/1906.06423",
    "<b>The &sect;3 bug, measured and fixed</b> — a good example of "
    "a data-pipeline problem mistaken for a model problem."),
 ],
 "exercises": [
   "<b>Visualise the first-layer filters</b> of three pretrained models "
   "and compare them.",
   "<b>Compare them against Gabor filters</b> you generate yourself.",
   "<b>Train a linear probe</b> on frozen features for a small task and "
   "record the accuracy.",
   "<b>Fine-tune the whole network on the same data</b> and compare. "
   "Report which wins and at what dataset size the crossover occurs.",
   "<b>Compute the receptive field</b> of each layer of a network you use, "
   "by hand.",
   "<b>Verify it empirically</b> by occluding input regions and measuring "
   "which units change.",
   "<b>Train at 224 and test at 384</b> and report the accuracy change.",
   "<b>Correct for it</b> and report the recovered accuracy.",
   "<b>Take a monocular depth model</b> and test it on a scene with "
   "unusually sized objects. Report the scale error.",
   "<b>Find three units in a mid-layer</b> and try to characterise what "
   "each responds to. Report how many were interpretable.",
 ],
 "selfcheck": [
   "What is learned at each depth, and which layers transfer best?",
   "Why is it striking that layer 1 learns Gabor filters?",
   "What did learning add that hand design never achieved?",
   "Give the transfer strategy for each data regime.",
   "Why is the linear probe the essential baseline?",
   "What is a receptive field, and why must it be computed?",
   "Why is resolution the most expensive choice?",
   "Explain the train/test resolution bug.",
   "Name four things learned features cannot do.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Detection and Segmentation",
 "subtitle": "Where, not just what — and how to measure it.",
 "question": "How do you find and delineate objects, and how do you know "
             "whether you did?",
 "outcomes": [
     "Explain the detection problem and the standard architectures.",
     "Explain non-maximum suppression and its parameters.",
     "Compute and interpret mean average precision correctly.",
     "Distinguish semantic, instance, and panoptic segmentation.",
     "Choose a metric that matches the actual use.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Detection",
   "blurb": "An output of variable length, which is the whole "
            "difficulty."},

  {"t": "callout", "title": "Detection is hard because the output has no fixed size",
   "kind": "The structural problem",
   "body": ["<b>Classification outputs one label.</b> Detection outputs "
            "a variable number of boxes with labels — and a network "
            "produces fixed-size tensors.",
            "<b>So every architecture is a way of handling that "
            "mismatch.</b> Anchors predict offsets from a fixed grid of "
            "candidate boxes; centre-based methods predict from each "
            "location; query-based methods use a fixed set of learned "
            "queries.",
            "<b>All three produce too many predictions and prune "
            "them</b> — which is what non-maximum suppression does, "
            "and the one exception is instructive.",
            "<b>DETR removed the pruning</b> by training with a "
            "bipartite matching loss (CSCE 669 M11's assignment problem), "
            "so each query commits to at most one object. <b>The "
            "architecture change was really a <i>loss</i> change.</b>"]},

  {"t": "table", "kicker": "Families", "title": "The detection architectures",
   "header": ["Family", "How", "Trade"],
   "widths": [2.5, 4.4, 5.1],
   "rows": [
     ["<b>Two-stage</b>", "<b>Propose regions, then classify each</b>", "<b>Accurate, slower. Faster R-CNN</b>"],
     ["<b>One-stage anchored</b>", "<b>Dense predictions over anchor boxes</b>", "<b>Fast; anchor tuning is fiddly. RetinaNet, YOLO</b>"],
     ["<b>Anchor-free</b>", "Predict box from each centre location", "<b>Simpler; fewer hyperparameters. FCOS</b>"],
     ["<b>Query-based</b>", "<b>Learned queries + matching loss</b>", "<b>No NMS; slow to train. DETR</b>"],
   ],
   "footnote": "<b>Class imbalance is the one-stage difficulty:</b> "
               "almost every anchor is background, and focal loss exists "
               "specifically to stop the easy negatives dominating the "
               "gradient.",
   "note": "Focal loss is best understood as a fix for a specific "
           "structural problem, not a general trick."},

  {"t": "section", "label": "Part 2", "title": "Non-maximum suppression",
   "blurb": "The step that quietly decides your metrics."},

  {"t": "code", "kicker": "NMS", "title": "The algorithm, and the two failures",
   "lang": "text", "code": """
  sort detections by confidence, descending
  for each detection, highest first:
      keep it
      discard every lower-confidence detection of the same
          class whose IoU with it exceeds a threshold

  THE IoU THRESHOLD IS A REAL DESIGN CHOICE:
      too low  -> genuinely overlapping objects are merged
                  (a crowd becomes one person)
      too high -> duplicate boxes survive and precision
                  falls

  TWO FAILURE MODES, both common:
      CROWDS. Overlapping instances of the same class are
          exactly what NMS cannot distinguish from
          duplicates. Pedestrian detection lives here.
      ELONGATED / ROTATED objects. Axis-aligned IoU is a
          poor similarity for a diagonal object, so boxes
          that do not overlap in reality have high IoU.

  SOFT-NMS decays confidence instead of discarding, which
  helps crowds. Query-based models (Part 1) remove the step
  entirely -- which is the cleaner fix.
""",
   "caption": "<b>NMS runs after the model and before the metric</b>, so "
              "its threshold changes your reported numbers without "
              "changing the model at all.",
   "note": "Students rarely realise NMS is a tunable that moves mAP."},

  {"t": "section", "label": "Part 3", "title": "Measuring it",
   "blurb": "mAP, and the four ways it is misread."},

  {"t": "callout", "title": "Mean average precision, precisely",
   "kind": "What the number means",
   "body": ["<b>A detection is correct if its IoU with an unmatched "
            "ground-truth box of the same class exceeds a threshold</b> "
            "— and each ground truth matches at most one "
            "detection.",
            "<b>Sort by confidence, sweep the threshold, trace a "
            "precision–recall curve, take the area.</b> That is "
            "average precision, per class. <b>Mean over classes is "
            "mAP.</b>",
            "<b>COCO's primary metric averages over IoU thresholds from "
            "0.50 to 0.95</b>, so it rewards localisation accuracy, while "
            "<b>mAP@0.5 is far more forgiving</b> — the two numbers "
            "are not comparable.",
            "<b>And mAP is an average over classes, so a rare class "
            "counts as much as a common one.</b> A model that fails "
            "entirely on one of twenty classes loses 5 points, however "
            "rare that class is."]},

  {"t": "bullets", "kicker": "Misreadings", "title": "How detection metrics mislead",
   "items": [
     "<b>Comparing mAP@0.5 against mAP@[0.5:0.95].</b> <b>The first "
     "is roughly twice the second.</b> Papers report both; readers "
     "confuse them.",
     "",
     "<b>Ignoring the size breakdown.</b> <b>Small-object AP is "
     "frequently a third of large-object AP</b>, and if your use is "
     "small objects, the headline number is irrelevant.",
     "",
     "<b>Ignoring the confidence threshold.</b> <b>mAP integrates over "
     "all thresholds; a deployed system picks one.</b> Report precision "
     "and recall at the threshold you will actually use.",
     "",
     "<b>Averaging over classes you do not care about</b> — or "
     "being dragged down by one you do not.",
     "",
     "<b>And mAP says nothing about temporal stability</b>, which is "
     "what a user of a video system actually perceives.",
   ],
   "footnote": "<b>Report precision and recall at your operating "
               "threshold alongside mAP</b> — that pair is what "
               "determines whether the system is usable."},

  {"t": "section", "label": "Part 4", "title": "Segmentation",
   "blurb": "Three different problems with similar names."},

  {"t": "table", "kicker": "Segmentation", "title": "The three tasks and their metrics",
   "header": ["Task", "Output", "Metric"],
   "widths": [2.6, 4.3, 5.1],
   "rows": [
     ["<b>Semantic</b>", "<b>A class per pixel; instances not separated</b>", "<b>mean IoU over classes</b>"],
     ["<b>Instance</b>", "<b>A mask per object</b>", "<b>mask AP — mAP with mask IoU</b>"],
     ["<b>Panoptic</b>", "<b>Every pixel assigned to a class AND an instance</b>", "<b>Panoptic quality = recognition × segmentation</b>"],
     ["Boundary-sensitive", "Any of the above", "<b>Boundary IoU — mean IoU hides edge error</b>"],
   ],
   "footnote": "<b>Mean IoU is dominated by large regions</b>, so a model "
               "can score well while getting every boundary wrong "
               "— which is precisely what matters for matting and "
               "compositing (CSCE 748).",
   "note": "The boundary point connects directly to the compositing "
           "course."},

  {"t": "callout", "title": "Choose the metric from the use, not from the leaderboard",
   "kind": "The recurring discipline",
   "body": ["<b>Counting objects?</b> Count accuracy, not mAP. They "
            "diverge: a model can have excellent mAP and systematically "
            "miscount.",
            "<b>Compositing or matting?</b> Boundary accuracy and alpha "
            "error, not region IoU.",
            "<b>Triggering an action?</b> Precision and recall at your "
            "threshold, with the cost of each error type stated.",
            "<b>Video?</b> <b>Temporal consistency, which no standard "
            "detection metric measures at all</b> — and flicker is "
            "the complaint users actually make. <b>CSCE 633 Module 01 "
            "§3's point, in the form it takes here.</b>"]},
 ],
 "takeaways": [
   "Detection is hard because the output length is variable, and every "
   "architecture is a strategy for reconciling that with fixed-size "
   "tensors.",
   "DETR's contribution was really a loss change — bipartite matching "
   "makes each query commit to one object, removing the need for "
   "suppression.",
   "NMS runs after the model and before the metric, so its threshold moves "
   "your reported numbers without changing the model.",
   "NMS fundamentally cannot distinguish overlapping instances from "
   "duplicates, which is why crowded scenes are hard.",
   "mAP@0.5 is roughly twice mAP@[0.5:0.95], and the two are routinely "
   "confused when comparing results.",
   "Mean IoU is dominated by large regions, so a model can score well "
   "while getting every boundary wrong.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Detection"),
  ("callout", "Detection is hard because the output has no fixed size",
   ["<b>Classification outputs one label per image. Detection outputs a "
    "variable number of boxes with labels</b> — and a neural network "
    "produces fixed-size tensors. <b>That mismatch is the structural "
    "difficulty of the task</b>, and recognising it makes the "
    "architectural zoo comprehensible.",
    "<b>Every architecture is a way of handling the mismatch.</b> "
    "Anchor-based methods predict offsets and a class from a fixed dense "
    "grid of candidate boxes; centre-based methods predict a box from "
    "each spatial location; query-based methods use a fixed set of learned "
    "query vectors. <b>In all cases the network's output is "
    "fixed-size</b> and the variability is handled afterwards.",
    "<b>All three produce far too many predictions and then prune "
    "them</b> — which is what non-maximum suppression does "
    "(&sect;2) — and the one exception is instructive.",
    "<b>DETR removed the pruning step</b> by training with a bipartite "
    "matching loss: each prediction is matched to at most one ground-truth "
    "object by a Hungarian assignment (<b>CSCE 669 Module 11's "
    "matching problem, inside a loss function</b>), so duplicates are "
    "penalised during training rather than removed after it. <b>The "
    "architectural novelty was really a <i>loss</i> novelty</b>, which is "
    "worth noticing because it is a recurring pattern: the hard part of a "
    "structured-output problem is usually the loss, not the network."]),
  ("table", ["Family", "How it works", "Trade"],
   [["<b>Two-stage</b>",
     "<b>Propose candidate regions, then classify and refine each "
     "one.</b>",
     "<b>Most accurate, slower.</b> Faster R-CNN and its descendants."],
    ["<b>One-stage anchored</b>",
     "<b>Dense class and box-offset predictions over a fixed set of "
     "anchor boxes at every location.</b>",
     "<b>Fast; the anchor shapes and scales are fiddly "
     "hyperparameters.</b> RetinaNet, the YOLO family."],
    ["<b>Anchor-free</b>",
     "Predict a box directly from each centre location, with no anchor "
     "priors.",
     "<b>Simpler and with fewer hyperparameters</b>, at comparable "
     "accuracy. FCOS, CenterNet."],
    ["<b>Query-based</b>",
     "<b>A fixed set of learned queries attends to image features; "
     "trained with a matching loss.</b>",
     "<b>No non-maximum suppression at all</b>, and notably slow to "
     "converge in training. DETR and successors."]],
   [0.19, 0.39, 0.42]),
  ("p", "<b>Class imbalance is the specific difficulty of one-stage "
        "detectors.</b> Almost every one of tens of thousands of anchors "
        "is background, so the summed loss over easy negatives swamps the "
        "gradient from the handful of positives. <b>Focal loss exists "
        "precisely to fix that</b> — it down-weights "
        "confidently-classified examples so the easy negatives contribute "
        "little — and it is best understood as a targeted fix for a "
        "structural problem rather than a general-purpose improvement to "
        "cross-entropy."),

  ("h1", "2 &nbsp; Non-maximum suppression"),
  ("code", """sort detections by confidence, descending
for each detection, highest confidence first:
    keep it
    discard every lower-confidence detection OF THE SAME
        CLASS whose IoU with it exceeds a threshold

THE IoU THRESHOLD IS A REAL DESIGN CHOICE:
    too low  -> genuinely overlapping objects are merged,
                and a crowd becomes one person
    too high -> duplicate boxes survive and precision
                falls

TWO FAILURE MODES, both common in practice:

  CROWDS. Overlapping instances of the same class are
      exactly what NMS cannot distinguish from duplicate
      detections of one instance -- the information needed
      is not in the boxes. Pedestrian and cell detection
      live in this regime permanently.

  ELONGATED OR ROTATED objects. Axis-aligned IoU is a poor
      similarity measure for a diagonal object, so two
      boxes around genuinely separate objects can have
      high IoU and one gets suppressed.

SOFT-NMS decays confidence rather than discarding, which
helps crowds measurably. Query-based models (section 1)
remove the step entirely, which is the cleaner fix."""),
  ("p", "<b>NMS runs after the model and before the metric</b>, so <b>its "
        "threshold changes your reported numbers without changing the "
        "model at all</b> — which means a comparison between two "
        "systems with different suppression settings is not a comparison "
        "of models. <b>State it when reporting</b>, and tune it on "
        "validation data like any other hyperparameter rather than "
        "leaving it at a framework default."),

  ("break",),
  ("h1", "3 &nbsp; Measuring detection"),
  ("callout", "Mean average precision, precisely",
   ["<b>A detection counts as correct if its intersection-over-union with "
    "an as-yet-unmatched ground-truth box of the same class exceeds a "
    "threshold</b>, and <b>each ground truth may be matched by at most "
    "one detection</b> — so a second overlapping detection of the "
    "same object is a false positive, which is what makes &sect;2's "
    "suppression necessary.",
    "<b>Sort all detections by confidence, sweep the confidence "
    "threshold downward, trace the resulting precision–recall curve, "
    "and take its area.</b> That is average precision for one class; the "
    "<b>mean over classes is mAP</b>.",
    "<b>COCO's primary metric averages AP over IoU thresholds from 0.50 "
    "to 0.95 in steps of 0.05</b>, so it rewards precise localisation "
    "and not merely detection. <b>mAP@0.5 is far more forgiving, and the "
    "two numbers are not comparable</b> — typically differing by "
    "nearly a factor of two on the same model.",
    "<b>And mAP is an unweighted average over classes, so a rare class "
    "counts exactly as much as a ubiquitous one.</b> A model that fails "
    "completely on one class out of twenty loses 5 mAP points whether "
    "that class appears in every image or in three of them — which "
    "is sometimes what you want and frequently not, and either way should "
    "be a deliberate choice."]),
  ("ul", ["<b>Comparing mAP@0.5 against mAP@[0.5:0.95].</b> <b>The first "
          "is roughly twice the second on the same model.</b> Papers "
          "report both, readers conflate them, and apparent "
          "state-of-the-art jumps sometimes consist of nothing else.",
          "<b>Ignoring the object-size breakdown.</b> <b>Small-object AP "
          "is frequently a third of large-object AP</b> (Module 08 "
          "&sect;3's resolution argument), <b>so if your application is "
          "small objects, the headline number tells you almost "
          "nothing.</b> COCO reports the breakdown; read it.",
          "<b>Ignoring the operating threshold.</b> <b>mAP integrates "
          "over every confidence threshold, and a deployed system picks "
          "exactly one.</b> <b>Report precision and recall at the "
          "threshold you will actually use</b> — that pair, not mAP, "
          "determines whether the system is usable.",
          "<b>Averaging over classes you do not care about</b>, or being "
          "dragged down by a class that is irrelevant to the "
          "application — both of which are fixed by reporting "
          "per-class AP.",
          "<b>And mAP says nothing whatsoever about temporal "
          "stability.</b> <b>A detector that flickers between frames can "
          "have excellent mAP and be unusable in video</b>, because "
          "flicker is what a user perceives and no per-frame metric "
          "measures it."]),

  ("h1", "4 &nbsp; Segmentation"),
  ("table", ["Task", "Output", "Standard metric"],
   [["<b>Semantic segmentation</b>",
     "<b>A class label per pixel. Separate instances of the same class "
     "are not distinguished.</b>",
     "<b>Mean IoU over classes</b> — and see the caveat below."],
    ["<b>Instance segmentation</b>",
     "<b>A mask per detected object, with a class.</b>",
     "<b>Mask AP</b> — &sect;3's mAP with mask IoU replacing box "
     "IoU."],
    ["<b>Panoptic segmentation</b>",
     "<b>Every pixel assigned both a class and, for countable classes, "
     "an instance.</b> The unification of the two above.",
     "<b>Panoptic quality</b> — a recognition term times a "
     "segmentation term, which keeps both failure types visible."],
    ["<b>Boundary-sensitive evaluation</b>", "Any of the above.",
     "<b>Boundary IoU, computed in a band around the contour</b>, "
     "because mean IoU hides boundary error almost completely."]],
   [0.21, 0.40, 0.39]),
  ("p", "<b>Mean IoU is dominated by large regions</b>, since it is "
        "computed over all pixels and most pixels are interior. <b>So a "
        "model can score very well on mean IoU while getting essentially "
        "every boundary wrong</b> — and <b>boundaries are precisely "
        "what matters for matting, compositing, and any downstream use "
        "that cuts along the mask</b> (CSCE 748 Module 05's "
        "requirement). <b>Report boundary IoU when the boundary is the "
        "product.</b>"),
  ("callout", "Choose the metric from the use, not from the leaderboard",
   ["<b>Counting objects?</b> <b>Report count accuracy, not mAP.</b> "
    "They diverge sharply: a detector with excellent mAP can "
    "systematically miscount, because mAP integrates over thresholds and "
    "counting happens at one.",
    "<b>Compositing or matting?</b> <b>Boundary accuracy and alpha "
    "error</b>, not region IoU — for the reason just given.",
    "<b>Triggering an action — an alert, a brake, a "
    "notification?</b> <b>Precision and recall at your chosen threshold, "
    "with the cost of each error type stated</b>, because the two error "
    "types almost never cost the same and a single metric cannot express "
    "that.",
    "<b>Video?</b> <b>Temporal consistency, which no standard detection "
    "metric measures at all.</b> <b>Flicker is the complaint users "
    "actually make</b> about video detection systems, and it is invisible "
    "to every number in this module. <b>This is CSCE 633 Module 01 "
    "&sect;3's point — the metric is a proxy and the proxy has "
    "chosen what you will optimise</b> — in the specific form it "
    "takes in perception."]),
 ],
 "resources": [
   ("Michigan EECS 498 — detection and segmentation lectures (free)",
    "https://web.archive.org/web/20260824025044/https://web.eecs.umich.edu/~justincj/teaching/eecs498/",
    "<b>The reference for &sect;1 and &sect;4</b>, with the architecture "
    "families laid out clearly."),
   ("Lin et al. — Focal Loss for Dense Object Detection (free)",
    "https://arxiv.org/abs/1708.02002",
    "<b>The &sect;1 imbalance problem and its fix</b>, with the analysis "
    "that motivates it."),
   ("Carion et al. — End-to-End Object Detection with Transformers "
    "(DETR) (free)",
    "https://arxiv.org/abs/2005.12872",
    "<b>The matching loss of &sect;1</b> — read it for the loss, "
    "which is the contribution."),
   ("COCO detection evaluation documentation (free)",
    "https://cocodataset.org/#detection-eval",
    "<b>Exactly what the metrics of &sect;3 compute</b>, including the "
    "size breakdown that is so often ignored."),
 ],
 "exercises": [
   "<b>Implement mAP from scratch</b> and verify it against the COCO "
   "evaluation tool on the same predictions.",
   "<b>Report mAP@0.5 and mAP@[0.5:0.95]</b> for one model and compute "
   "the ratio.",
   "<b>Break your results down by object size</b> and report the three "
   "numbers.",
   "<b>Sweep the NMS IoU threshold</b> and plot mAP against it. Report "
   "the best value and the spread.",
   "<b>Construct a crowded test case</b> and show NMS merging distinct "
   "objects.",
   "<b>Try soft-NMS on it</b> and report the improvement.",
   "<b>Pick one confidence threshold</b> and report precision and recall "
   "there. Compare against the mAP.",
   "<b>Count objects with your detector</b> and compare count accuracy "
   "against mAP across thresholds.",
   "<b>Compute mean IoU and boundary IoU</b> for a segmentation model and "
   "report both.",
   "<b>Run a detector on video</b> and measure flicker — the "
   "fraction of frames where a stationary object's detection "
   "disappears.",
 ],
 "selfcheck": [
   "Why is detection structurally harder than classification?",
   "Name four architecture families and the trade each makes.",
   "What was DETR's actual contribution?",
   "Why does focal loss exist?",
   "Describe NMS and its two intrinsic failure modes.",
   "Why does the NMS threshold change your reported metrics?",
   "Define mAP precisely, including the matching rule.",
   "Give five ways detection metrics mislead.",
   "Distinguish the three segmentation tasks and their metrics.",
   "Why does mean IoU hide boundary error?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Transformers and Self-Supervision",
 "subtitle": "Learning without labels, and attention over patches.",
 "question": "What changed when vision adopted the transformer?",
 "outcomes": [
     "Explain the vision transformer and how it differs from a CNN.",
     "Explain what inductive bias buys and costs.",
     "Explain the main self-supervised objectives.",
     "Explain contrastive language-image pretraining and what it "
     "enables.",
     "State what self-supervised features are and are not good for.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Vision transformers",
   "blurb": "An image as a sequence of patches."},

  {"t": "callout", "title": "A vision transformer is CSCE 636's transformer with patches as tokens",
   "kind": "The architecture, in one slide",
   "body": ["<b>Cut the image into 16×16 patches, flatten "
            "each, project to a vector, add a positional "
            "embedding.</b> That is a sequence.",
            "<b>Then run a standard transformer encoder</b> "
            "(CSCE 636 M06) <b>and classify from a prepended class "
            "token.</b> There is nothing vision-specific in the body.",
            "<b>Self-attention is global from layer one</b> — "
            "every patch attends to every other — so there is no "
            "receptive-field growth to manage (Module 08 §3).",
            "<b>And cost is quadratic in the patch count</b>, which "
            "makes high resolution expensive and is why windowed "
            "variants like Swin exist."]},

  {"t": "table", "kicker": "Comparison", "title": "Convolution against attention",
   "header": ["", "CNN", "ViT"],
   "widths": [2.5, 4.4, 5.1],
   "rows": [
     ["<b>Inductive bias</b>", "<b>Locality, translation equivariance, hierarchy</b>", "<b>Almost none — only the patch grid</b>"],
     ["<b>Small data</b>", "<b>Much better — the bias is correct and free</b>", "<b>Much worse — must learn the bias</b>"],
     ["<b>Large data</b>", "Plateaus earlier", "<b>Keeps improving; eventually wins</b>"],
     ["<b>Receptive field</b>", "Grows with depth; must be designed", "<b>Global immediately</b>"],
     ["<b>Cost in resolution</b>", "<b>Linear in pixels</b>", "<b>Quadratic in patches</b>"],
   ],
   "footnote": "<b>So the crossover is a data-volume question</b>, and "
               "below roughly ten million images a CNN or a hybrid is "
               "usually the right choice.",
   "note": "The honest answer is 'it depends on your data volume', and "
           "saying so is more useful than picking a winner."},

  {"t": "callout", "title": "Inductive bias is a prior, with the same trade as every prior",
   "kind": "The general lesson",
   "body": ["<b>Convolution hard-codes that nearby pixels are related "
            "and that features should be translation-equivariant.</b> "
            "Both are true of natural images.",
            "<b>So a CNN starts with free, correct knowledge</b> and "
            "needs less data — exactly Module 01 §3's fourth "
            "strategy, built into the architecture rather than learned.",
            "<b>And a correct prior becomes a ceiling once data is "
            "abundant</b>, because the model cannot represent the "
            "exceptions. Translation equivariance is wrong for an image "
            "with a consistent horizon.",
            "<b>Which is the bias–variance trade of CSCE 633 "
            "M03, in architectural form</b> — and it is why the "
            "CNN-versus-transformer question has a data-dependent answer "
            "rather than a winner."]},

  {"t": "section", "label": "Part 2", "title": "Self-supervision",
   "blurb": "Labels are expensive; images are not."},

  {"t": "code", "kicker": "Objectives", "title": "The three families that worked",
   "lang": "text", "code": """
  CONTRASTIVE  (SimCLR, MoCo)
      two augmentations of one image should embed close;
      different images should embed far apart.
      NEEDS many negatives -- a large batch or a queue.
      Risk: learns the augmentation invariances you chose,
      which is a feature when they match your task and a
      limitation when they do not.

  SELF-DISTILLATION  (BYOL, DINO)
      a student network predicts a teacher's output on a
      different view; the teacher is an exponential moving
      average of the student.
      NO NEGATIVES NEEDED, which was surprising, and the
      reason it does not collapse is still debated.
      DINO's attention maps segment objects without ever
      being told objects exist.

  MASKED PREDICTION  (MAE, BEiT)
      mask 75% of the patches and reconstruct them.
      Directly CSCE 638's masked language modelling.
      Scales well, trains cheaply (the encoder only sees
      25% of patches), and yields features that fine-tune
      excellently and linear-probe poorly.

  THAT LAST ASYMMETRY MATTERS: masked models learn
  representations that need adaptation, contrastive models
  learn ones that are immediately linearly separable.
  Which you want depends on your labelled data budget.
""",
   "caption": "<b>The probe-versus-fine-tune asymmetry is the practical "
              "difference between the families</b>, and it decides which "
              "to use.",
   "note": "This asymmetry is the genuinely actionable finding and is "
           "rarely stated clearly."},

  {"t": "section", "label": "Part 3", "title": "Language supervision",
   "blurb": "The caption as a label that already exists."},

  {"t": "callout", "title": "CLIP: train image and text encoders to agree",
   "kind": "Why this was a step change",
   "body": ["<b>Train an image encoder and a text encoder so that a "
            "photograph and its caption embed close together</b>, "
            "contrastively, over hundreds of millions of pairs.",
            "<b>Captions are supervision that already exists</b> — "
            "no annotation campaign, and the label space is open rather "
            "than a fixed list of classes.",
            "<b>Which gives zero-shot classification:</b> embed the "
            "candidate class names as text, embed the image, pick the "
            "nearest. <b>No training on the target classes at all.</b>",
            "<b>And it gives a shared space for retrieval and for "
            "conditioning generators</b> — which is why text-to-image "
            "models depend on it. <b>The limitation is that it inherits "
            "the biases of web captions</b>, faithfully."]},

  {"t": "section", "label": "Part 4", "title": "What they are good for",
   "blurb": "An honest account."},

  {"t": "bullets", "kicker": "Uses", "title": "Where self-supervised features earn their keep",
   "items": [
     "<b>Little labelled data, plenty of unlabelled.</b> The core case, "
     "and the gains are large.",
     "",
     "<b>Retrieval and nearest-neighbour search.</b> <b>A good "
     "embedding is directly useful without any head</b> "
     "(CSCE 670's subject).",
     "",
     "<b>Dense correspondence.</b> <b>DINO features match across "
     "instances and viewpoints</b> surprisingly well — which is "
     "Module 03's problem, solved sideways.",
     "",
     "<b>And initialisation for anything</b>, including the geometric "
     "pipelines of Modules 03–07.",
     "",
     "<b>Not: metric geometry, uncertainty, or anything requiring "
     "guarantees.</b> <b>Module 08 §4's limits are "
     "unchanged.</b>",
   ],
   "footnote": "<b>DINO features as a dense descriptor is the result most "
               "worth knowing</b> — it connects this module directly "
               "back to the geometric half of the course."},

  {"t": "callout", "title": "What scale did and did not deliver",
   "kind": "Closing honestly",
   "body": ["<b>Scale delivered representation quality.</b> Features "
            "from a large self-supervised model beat supervised features "
            "on most transfer tasks, which was not true in 2018.",
            "<b>It delivered open-vocabulary recognition</b> through "
            "language supervision, which no amount of fixed-class "
            "training achieves.",
            "<b>It did not deliver robustness.</b> <b>Large models are "
            "more robust than small ones and still fail under "
            "distribution shift</b> (Module 12), and they fail "
            "confidently.",
            "<b>And it did not deliver geometry.</b> <b>CLIP cannot "
            "count reliably, struggles with spatial relations, and has no "
            "metric scale</b> — the geometric half of this course is "
            "not obsolete, which is the honest summary."]},
 ],
 "takeaways": [
   "A vision transformer is CSCE 636's transformer with image patches as "
   "tokens, and the body contains nothing vision-specific.",
   "Convolution's inductive bias is a prior: free correct knowledge at "
   "small data, a ceiling at large data — the bias-variance trade in "
   "architectural form.",
   "Contrastive methods need negatives, self-distillation surprisingly does "
   "not, and masked prediction is CSCE 638's objective applied to "
   "patches.",
   "Masked models fine-tune excellently and linear-probe poorly; "
   "contrastive models are immediately linearly separable — which "
   "decides the choice.",
   "CLIP uses captions as supervision that already exists, giving "
   "open-vocabulary zero-shot classification and a shared embedding "
   "space.",
   "Scale delivered representation quality and open vocabulary; it did not "
   "deliver robustness or geometry.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Vision transformers"),
  ("callout", "A vision transformer is CSCE 636's transformer with patches "
              "as tokens",
   ["<b>Cut the image into non-overlapping 16&times;16 patches, flatten "
    "each into a vector, project it linearly, and add a positional "
    "embedding.</b> The image is now a sequence of a few hundred tokens.",
    "<b>Then run a completely standard transformer encoder</b> "
    "(CSCE 636 Module 06) <b>and classify from a prepended class "
    "token.</b> <b>There is nothing vision-specific in the body of the "
    "architecture at all</b> — which was the point of the paper and "
    "is why the result was striking.",
    "<b>Self-attention is global from the first layer</b>: every patch "
    "attends to every other patch. <b>So there is no receptive field to "
    "grow or to design</b> (Module 08 &sect;3), and the architectural "
    "failure mode of a too-small receptive field simply does not exist.",
    "<b>And the cost is quadratic in the number of patches</b>, since "
    "attention compares every pair. <b>High resolution is therefore "
    "expensive in a way it is not for a convolutional network</b>, which "
    "is why windowed and hierarchical variants (Swin and its relatives) "
    "exist — they reintroduce locality for computational reasons, "
    "arriving back at something structurally close to a CNN."]),
  ("table", ["", "Convolutional network", "Vision transformer"],
   [["<b>Inductive bias</b>",
     "<b>Locality, translation equivariance, and a spatial "
     "hierarchy</b> — all built in.",
     "<b>Almost none beyond the patch grid itself.</b>"],
    ["<b>Small data</b>",
     "<b>Substantially better — the built-in bias is correct for "
     "natural images and costs no data to acquire.</b>",
     "<b>Substantially worse — it must learn from data what the CNN "
     "was given.</b>"],
    ["<b>Large data</b>", "Plateaus earlier.",
     "<b>Keeps improving, and eventually wins</b> — the crossover "
     "is empirical and depends on the task."],
    ["<b>Receptive field</b>",
     "Grows with depth; must be computed and designed for.",
     "<b>Global from layer one.</b>"],
    ["<b>Cost in resolution</b>", "<b>Linear in pixel count.</b>",
     "<b>Quadratic in patch count.</b>"]],
   [0.18, 0.41, 0.41]),
  ("callout", "Inductive bias is a prior, with the same trade as every prior",
   ["<b>Convolution hard-codes two facts: nearby pixels are more related "
    "than distant ones, and a feature detector useful at one location is "
    "useful at another.</b> Both are true of natural images, and both "
    "were established by Module 08 &sect;1's observation that learned "
    "layer-1 filters converge on the same primitives regardless.",
    "<b>So a convolutional network begins with free, correct "
    "knowledge</b> and needs correspondingly less data — <b>which "
    "is exactly Module 01 &sect;3's fourth strategy, built into the "
    "architecture rather than learned from examples.</b>",
    "<b>And a correct prior becomes a ceiling once data is "
    "abundant</b>, because the architecture cannot represent the "
    "exceptions to it. <b>Translation equivariance is simply wrong for "
    "an image with a consistent horizon</b>, where 'sky' at the top and "
    "'sky' at the bottom mean different things, and a CNN cannot easily "
    "learn that distinction.",
    "<b>Which is the bias–variance trade of CSCE 633 Module 03 in "
    "architectural form.</b> <b>It is why the CNN-versus-transformer "
    "question has a data-dependent answer rather than a winner</b>, and "
    "why the honest recommendation below roughly ten million images is a "
    "CNN or a hybrid — a claim about your dataset, not about the "
    "architectures."]),

  ("h1", "2 &nbsp; Self-supervision"),
  ("code", """CONTRASTIVE  (SimCLR, MoCo)
    two augmentations of one image should embed close
    together; different images should embed far apart.
    NEEDS MANY NEGATIVES -- a large batch, or a queue of
    past embeddings.
    Risk: it learns exactly the invariances your
    augmentations encode, which is a feature when they
    match your task and a hard limitation when they do
    not. Colour-jitter augmentation teaches the model to
    ignore colour, which is wrong for bird species.

SELF-DISTILLATION  (BYOL, DINO)
    a student network predicts a teacher's output on a
    different view of the same image; the teacher is an
    exponential moving average of the student.
    NO NEGATIVES NEEDED, which was genuinely surprising,
    and the reason it does not collapse to a constant is
    still debated.
    DINO's attention maps segment objects without ever
    being told that objects exist.

MASKED PREDICTION  (MAE, BEiT)
    mask 75% of the patches and reconstruct them.
    Directly CSCE 638's masked language modelling, applied
    to patches. Trains cheaply, because the encoder only
    sees the visible 25%.

THE ASYMMETRY THAT MATTERS: masked models fine-tune
excellently and LINEAR-PROBE POORLY; contrastive models
produce features that are immediately linearly separable.
Which you want depends entirely on your labelled budget."""),
  ("p", "<b>That asymmetry is the practically actionable finding and it is "
        "rarely stated clearly.</b> <b>If you have very little labelled "
        "data and will train only a linear head</b> (Module 08 "
        "&sect;2), <b>a contrastive or self-distilled model is the right "
        "choice.</b> <b>If you have enough to fine-tune, a masked model "
        "will usually end higher.</b> <b>Choosing by benchmark headline "
        "rather than by which protocol you will actually use is a common "
        "and expensive error.</b>"),

  ("break",),
  ("h1", "3 &nbsp; Language supervision"),
  ("callout", "CLIP: train image and text encoders to agree",
   ["<b>Train an image encoder and a text encoder jointly so that a "
    "photograph and its caption embed close together, and mismatched "
    "pairs embed far apart</b> — contrastive learning across two "
    "modalities, over hundreds of millions of image-text pairs scraped "
    "from the web.",
    "<b>Captions are supervision that already exists.</b> No annotation "
    "campaign, no fixed label taxonomy, and <b>the label space is open "
    "rather than a closed list of classes</b> — which is the "
    "structural advance, not the architecture.",
    "<b>Which gives zero-shot classification directly:</b> embed the "
    "candidate class names as text ('a photograph of a &hellip;'), embed "
    "the image, and take the nearest. <b>No training on the target "
    "classes at all</b>, and it works well enough to be a serious "
    "baseline on tasks nobody collected data for.",
    "<b>And it gives a shared embedding space usable for retrieval and "
    "for conditioning generative models</b>, which is why text-to-image "
    "systems are built on top of it. <b>The limitation is that it "
    "inherits the biases of web captions faithfully</b> — the "
    "associations in the training text become associations in the "
    "embedding space, which is Module 12 &sect;4's subject and is not "
    "fixable by scaling."]),

  ("h1", "4 &nbsp; What they are good for"),
  ("ul", ["<b>Little labelled data and plenty of unlabelled data.</b> "
          "The core case, and the gains over supervised pretraining are "
          "large and reliable.",
          "<b>Retrieval and nearest-neighbour search.</b> <b>A good "
          "embedding is directly useful with no head and no "
          "fine-tuning</b> — which is CSCE 670's subject, and is "
          "where self-supervised features are least caveated.",
          "<b>Dense correspondence.</b> <b>DINO features match across "
          "object instances and across wide viewpoint changes "
          "surprisingly well</b>, giving semantic correspondence between "
          "different objects of the same category — which is "
          "<b>Module 03's problem solved sideways</b>, and the result in "
          "this module most worth knowing, because it connects the learned "
          "half of the course back to the geometric half.",
          "<b>And initialisation for essentially anything</b>, including "
          "components of the geometric pipelines of Modules 03 through "
          "07.",
          "<b>Not for: metric geometry, calibrated uncertainty, or "
          "anything requiring a guarantee.</b> <b>Module 08 &sect;4's "
          "limits are entirely unchanged by scale or by "
          "self-supervision</b>, and it is worth saying so explicitly "
          "because the breadth of these models invites the assumption "
          "otherwise."]),
  ("callout", "What scale did and did not deliver",
   ["<b>Scale delivered representation quality.</b> Features from a large "
    "self-supervised model now beat supervised ImageNet features on most "
    "transfer tasks — which was not true in 2018 and was not widely "
    "expected.",
    "<b>It delivered open-vocabulary recognition</b> through language "
    "supervision (&sect;3), which no amount of fixed-class training "
    "achieves, because the limitation there was the taxonomy rather than "
    "the data volume.",
    "<b>It did not deliver robustness.</b> <b>Large models are more "
    "robust than small ones and still fail under distribution shift</b> "
    "(Module 12), <b>and they fail confidently</b> — the "
    "calibration problem of Module 08 &sect;4 is not improved by scale "
    "and in some respects is worsened by it.",
    "<b>And it did not deliver geometry.</b> <b>CLIP cannot count "
    "reliably, struggles with spatial relations ('the cup left of the "
    "book'), and has no metric scale whatsoever</b> — because "
    "Module 01's theorem is a theorem. <b>The geometric half of this "
    "course is not obsolete, and that is the honest summary of where the "
    "two halves stand relative to each other.</b>"]),
 ],
 "resources": [
   ("Dosovitskiy et al. — An Image is Worth 16x16 Words (ViT) "
    "(free)",
    "https://arxiv.org/abs/2010.11929",
    "<b>The &sect;1 architecture</b>, including the data-volume crossover "
    "measurements of the comparison table."),
   ("Caron et al. — Emerging Properties in Self-Supervised Vision "
    "Transformers (DINO) (free)",
    "https://arxiv.org/abs/2104.14294",
    "<b>The &sect;2 self-distillation method</b>, and the attention maps "
    "that segment objects unsupervised."),
   ("He et al. — Masked Autoencoders Are Scalable Vision Learners "
    "(free)",
    "https://arxiv.org/abs/2111.06377",
    "<b>The &sect;2 masked objective</b>, with the probe-versus-fine-tune "
    "asymmetry reported honestly."),
   ("Radford et al. — Learning Transferable Visual Models from "
    "Natural Language Supervision (CLIP) (free)",
    "https://arxiv.org/abs/2103.00020",
    "<b>The &sect;3 result</b>, and the limitations section is unusually "
    "candid and worth reading."),
 ],
 "exercises": [
   "<b>Implement patch embedding and a small ViT</b> and train it on a "
   "small dataset.",
   "<b>Train a comparable CNN on the same data</b> and report which wins "
   "at 1k, 10k, and 50k training images.",
   "<b>Visualise ViT attention maps</b> at several layers and describe "
   "what they attend to.",
   "<b>Implement SimCLR's contrastive loss</b> and train on unlabelled "
   "images.",
   "<b>Vary the augmentations</b> and report how the learned invariances "
   "change on a downstream task that needs colour.",
   "<b>Linear-probe a masked model and a contrastive model</b> on the same "
   "task and report the gap.",
   "<b>Fine-tune both</b> and report whether the ordering reverses.",
   "<b>Run CLIP zero-shot</b> on a classification task of your own and "
   "compare against a trained baseline.",
   "<b>Test CLIP on counting and spatial relations</b> and report the "
   "failures.",
   "<b>Use DINO features for dense correspondence</b> between two "
   "different objects of the same category, and compare against SIFT.",
 ],
 "selfcheck": [
   "Describe a vision transformer and say what is vision-specific in "
   "it.",
   "Compare CNN and ViT on five axes.",
   "Why is inductive bias both an advantage and a ceiling?",
   "Describe the three self-supervised families and what each needs.",
   "State the probe-versus-fine-tune asymmetry and its consequence.",
   "What was CLIP's structural advance, and what does it enable?",
   "Give four good uses of self-supervised features and three bad ones.",
   "What did scale deliver, and what did it not?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Neural Scene Representations",
 "subtitle": "Inverse rendering, finally.",
 "question": "What if you reconstructed a scene by optimising a renderer "
             "against photographs?",
 "outcomes": [
     "Explain a radiance field and how it is rendered.",
     "Explain why the rendering must be differentiable.",
     "Explain 3D Gaussian splatting and why it is faster.",
     "Compare these against classical multi-view stereo honestly.",
     "State what these representations are and are not suitable for.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The idea",
   "blurb": "Stop searching for correspondence; optimise a scene "
            "instead."},

  {"t": "callout", "title": "Invert rendering by differentiating it",
   "kind": "The whole module in one callout",
   "body": ["<b>Classical reconstruction searches for "
            "correspondences</b>, then triangulates "
            "(Modules 04–06). <b>Correspondence is the hard, "
            "brittle part.</b>",
            "<b>Neural reconstruction skips it.</b> Parameterise the "
            "scene, <i>render</i> it from each known camera pose, and "
            "<b>minimise the difference between the rendered and the "
            "captured image.</b>",
            "<b>If the renderer is differentiable, gradient descent "
            "solves it</b> — which is CSCE 647's forward model used "
            "as a loss function and CSCE 669's optimiser used on it.",
            "<b>The requirement is that rendering be differentiable, "
            "which rasterisation is not</b> — a pixel's visible "
            "triangle changes discontinuously. <b>Resolving that is the "
            "technical core</b> (Part 2)."]},

  {"t": "eq", "kicker": "Radiance field", "title": "The representation and its rendering",
   "eqs": [
     ("F(x, y, z, θ, φ) → (r, g, b, σ)",
      "A function from position and view direction to colour and "
      "density. Stored as a small MLP, or a grid, or a hash table."),
     ("C(ray) = ∫ T(t) · σ(t) · c(t) dt",
      "Volume rendering: integrate colour weighted by density and by "
      "transmittance T along the ray."),
     ("T(t) = exp( −∫ σ(s) ds )",
      "Transmittance — the probability light reaches t unoccluded. "
      "This is CSCE 647's participating-media integral."),
   ],
   "caption": "<b>Volume rendering is chosen precisely because it is "
              "differentiable</b> — density is continuous, so there "
              "is no visibility discontinuity to differentiate "
              "through.",
   "note": "That the representation was chosen for differentiability, not "
           "realism, is the key design insight."},

  {"t": "section", "label": "Part 2", "title": "Why volumes",
   "blurb": "The differentiability problem, and its solution."},

  {"t": "callout", "title": "Surfaces are not differentiable; volumes are",
   "kind": "The design constraint that chose the representation",
   "body": ["<b>Move a triangle slightly and a pixel's visible surface "
            "may switch discontinuously.</b> The gradient of the image "
            "with respect to geometry does not exist there.",
            "<b>A density field has no such discontinuity.</b> Every "
            "point along the ray contributes continuously, weighted by "
            "transmittance, so the integral is smooth in the "
            "parameters.",
            "<b>So the volumetric representation was chosen for "
            "optimisability, not for physical accuracy.</b> <b>Real "
            "scenes are mostly surfaces</b>, and representing them as fog "
            "is a deliberate concession.",
            "<b>Which is why extracting a clean mesh from a radiance "
            "field is hard</b>, and why signed-distance variants exist "
            "— <b>they reintroduce surfaces while keeping a smooth "
            "gradient path.</b>"]},

  {"t": "code", "kicker": "Training", "title": "What makes it work in practice",
   "lang": "text", "code": """
  POSITIONAL ENCODING is not optional. An MLP on raw (x,y,z)
  produces a blurry field -- it cannot represent high
  frequencies. Encode each coordinate as sin/cos at many
  frequencies first. CSCE 647's sampling theory: the
  network's capacity to represent detail is set by the
  input's frequency content.

  HIERARCHICAL SAMPLING. Most of a ray is empty. Sample
  coarsely, build a density-weighted distribution, then
  sample finely where density is. 2-3x speedup for free.

  CAMERA POSES MUST BE ACCURATE. NeRF assumes them known,
  and they come from COLMAP (Module 05). A pose error of
  one degree produces visible blur that looks like
  under-training, which sends people to the wrong fix.

  WHAT GOES WRONG
    too few views     -> floaters: density in empty space
                         that happens to fit the images
    all views one side-> the unseen side is invented
    moving objects    -> smeared, as in Module 05
    changing exposure -> baked into the radiance field
    reflections       -> modelled as geometry BEHIND the
                         mirror, which is self-consistent
                         and wrong
""",
   "caption": "<b>Every one of these failures is the ill-posedness of "
              "Module 01</b> — the optimiser found a scene "
              "consistent with the images that is not the real scene.",
   "note": "The mirror failure is the most illuminating one; it is "
           "geometrically reasonable and physically wrong."},

  {"t": "section", "label": "Part 3", "title": "Gaussian splatting",
   "blurb": "The same idea, a different primitive, two orders of "
            "magnitude faster."},

  {"t": "table", "kicker": "Comparison", "title": "Radiance fields against Gaussian splatting",
   "header": ["", "NeRF", "3D Gaussian splatting"],
   "widths": [2.4, 4.4, 5.2],
   "rows": [
     ["<b>Scene as</b>", "<b>An implicit function (MLP or grid)</b>", "<b>An explicit set of 3D Gaussians</b>"],
     ["<b>Rendering</b>", "<b>Ray marching — many network queries per pixel</b>", "<b>Rasterise and alpha-blend, sorted by depth</b>"],
     ["<b>Render speed</b>", "Seconds per frame originally", "<b>Real time — hundreds of fps</b>"],
     ["<b>Train time</b>", "Hours", "<b>Minutes</b>"],
     ["<b>Editing</b>", "<b>Hard — weights are not local</b>", "<b>Easy — move or delete primitives</b>"],
     ["<b>Memory</b>", "Small (a network)", "<b>Large — millions of primitives</b>"],
   ],
   "footnote": "<b>Splatting won on speed and editability by going back "
               "to an explicit representation</b>, which is a useful "
               "reminder that implicit is not automatically better.",
   "note": "The explicit-vs-implicit reversal is a good lesson about "
           "research fashion."},

  {"t": "callout", "title": "Why splatting is fast, exactly",
   "kind": "The mechanism",
   "body": ["<b>A 3D Gaussian projects to a 2D Gaussian</b>, which can "
            "be rasterised — so the whole scene renders with the "
            "graphics pipeline of CSCE 641 rather than by marching "
            "rays.",
            "<b>No network query per sample.</b> NeRF evaluates an MLP "
            "hundreds of times per pixel; splatting blends a few dozen "
            "primitives.",
            "<b>And alpha blending sorted by depth is differentiable</b> "
            "— which recovers the Part 2 property with an explicit "
            "primitive, because a Gaussian has no hard boundary.",
            "<b>The density control is the clever part:</b> <b>split "
            "Gaussians where the gradient is large and prune "
            "transparent ones</b>, so the representation adapts its "
            "resolution to the scene during optimisation."]},

  {"t": "section", "label": "Part 4", "title": "Honest comparison",
   "blurb": "Against classical methods, and what each is for."},

  {"t": "bullets", "kicker": "Comparison", "title": "Neural reconstruction against multi-view stereo",
   "items": [
     "<b>Novel-view image quality: neural wins decisively.</b> It "
     "optimises exactly that objective, so this is not surprising.",
     "",
     "<b>Mesh quality for downstream geometry: classical MVS still "
     "competitive</b>, and often better. <b>Radiance fields are not "
     "surfaces</b> (Part 2).",
     "",
     "<b>Robustness to few or badly distributed views: classical "
     "wins</b> — it degrades to sparse rather than to confident "
     "fabrication.",
     "",
     "<b>Metric accuracy: both depend on the same COLMAP poses</b>, so "
     "neither escapes Module 01's scale theorem.",
     "",
     "<b>And for a game engine: splatting is the one you can "
     "render</b>, which is why the track cares.",
   ],
   "footnote": "<b>Choose by what the output is for:</b> an image, a "
               "mesh, or a measurement. <b>They are different "
               "deliverables and the methods rank differently on each.</b>"},

  {"t": "callout", "title": "Why this module is the centre of the track",
   "kind": "The connection made explicit",
   "body": ["<b>CSCE 641 gave the rasterisation pipeline. CSCE 647 gave "
            "the rendering integral and the sampling theory. CSCE 645 "
            "gave the surface representations. CSCE 669 gave the "
            "optimiser.</b>",
            "<b>This module is all four at once</b>, pointed backwards: "
            "a renderer, differentiated, optimised against photographs, "
            "producing a scene.",
            "<b>Which is why Graphics and Vision are one track and not "
            "two.</b> <b>The forward model is the thing you invert</b>, "
            "and you cannot invert what you do not understand.",
            "<b>And it is the clearest case in the program of a subject "
            "that could only have been built by people who knew both "
            "halves.</b>"]},
 ],
 "takeaways": [
   "Neural reconstruction skips correspondence entirely: parameterise the "
   "scene, render it, and minimise the image difference.",
   "The volumetric representation was chosen because it is differentiable, "
   "not because it is physically accurate — real scenes are mostly "
   "surfaces.",
   "Positional encoding is not optional: without it the MLP cannot "
   "represent high frequencies, which is CSCE 647's sampling theory.",
   "Every characteristic failure — floaters, invented back sides, "
   "mirrors as geometry — is Module 01's ill-posedness, with the "
   "optimiser finding a consistent wrong scene.",
   "Gaussian splatting is faster because a projected Gaussian rasterises, "
   "so the graphics pipeline replaces ray marching.",
   "Neural wins on novel-view image quality, classical multi-view stereo "
   "remains competitive on mesh quality, and neither escapes the scale "
   "theorem.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Inverting rendering by differentiating it"),
  ("callout", "Invert rendering by differentiating it",
   ["<b>Classical reconstruction searches for correspondences and then "
    "triangulates</b> (Modules 04 through 06). <b>Correspondence is the "
    "hard and brittle part</b> — Module 06 &sect;4's entire failure "
    "list is correspondence failure.",
    "<b>Neural reconstruction skips it.</b> Parameterise the scene "
    "somehow, <i>render</i> that parameterisation from each known camera "
    "pose, and <b>minimise the difference between the rendered image and "
    "the captured photograph.</b> No correspondence is ever computed or "
    "needed.",
    "<b>If the renderer is differentiable, gradient descent solves "
    "it</b> — <b>which is CSCE 647's forward model used as a loss "
    "function, with CSCE 669 Module 05's first-order methods as the "
    "optimiser.</b> Both of those courses were prerequisites for exactly "
    "this.",
    "<b>The requirement is that rendering be differentiable with respect "
    "to the scene parameters, and rasterisation is not</b>: move a "
    "triangle slightly and a pixel's visible surface can switch "
    "discontinuously, so the derivative does not exist. <b>Resolving that "
    "is the technical core of the module</b> (&sect;2), and it is what "
    "determined the representation."]),
  ("eq", "F(x, y, z, &theta;, &phi;) &rarr; (r, g, b, &sigma;)"),
  ("eq", "C(ray) = &int; T(t) &middot; &sigma;(t) &middot; c(t) dt, "
         "&nbsp;&nbsp; T(t) = exp( &minus;&int; &sigma;(s) ds )"),
  ("p", "<b>A radiance field is a function from position and viewing "
        "direction to colour and density</b>, stored as a small "
        "multilayer perceptron, a voxel grid, or a multiresolution hash "
        "table. <b>Rendering is volume rendering:</b> integrate emitted "
        "colour along the ray, weighted by local density and by the "
        "transmittance T — the probability that light reaches that "
        "point unoccluded. <b>This is precisely CSCE 647's "
        "participating-media integral</b>, which is why that course's "
        "treatment of volumetric transport was worth the effort it took."),

  ("h1", "2 &nbsp; Why a volume"),
  ("callout", "Surfaces are not differentiable; volumes are",
   ["<b>Move a triangle slightly and a pixel's visible surface may switch "
    "discontinuously from one triangle to another.</b> The derivative of "
    "the image with respect to the geometry does not exist at that "
    "configuration, and gradient descent cannot cross it.",
    "<b>A density field has no such discontinuity.</b> Every point along "
    "the ray contributes continuously, weighted by transmittance, so <b>the "
    "rendered colour is a smooth function of the scene parameters "
    "everywhere</b> — which is exactly what the optimiser requires.",
    "<b>So the volumetric representation was chosen for optimisability "
    "rather than for physical accuracy.</b> <b>Real scenes are "
    "overwhelmingly surfaces</b>, and representing a wooden table as a "
    "cloud of dense fog is a deliberate concession to the optimiser "
    "— one worth understanding, because it explains the method's "
    "characteristic artefacts.",
    "<b>Which is why extracting a clean mesh from a radiance field is "
    "difficult</b> — there is no surface in the representation, only "
    "a density level set that may be thick, noisy, or ambiguous — "
    "and why signed-distance-function variants (VolSDF, NeuS) exist: "
    "<b>they reintroduce an explicit surface while keeping a smooth "
    "gradient path to it</b>, which is CSCE 645 Module 04's implicit "
    "surfaces used for a new purpose."]),
  ("code", """POSITIONAL ENCODING IS NOT OPTIONAL. An MLP applied to raw
(x,y,z) produces a blurry field -- it cannot represent high
spatial frequencies. Encode each coordinate as sin/cos at
many frequencies first, then feed that.

    This is CSCE 647's sampling theory: the network's
    capacity to represent detail is bounded by the
    frequency content of its input, and raw coordinates
    have none.

HIERARCHICAL SAMPLING. Most of a ray is empty space.
Sample coarsely, build a density-weighted distribution
along the ray, then sample finely where the density
actually is. A 2-3x speedup for no accuracy cost, and it
is importance sampling (CSCE 647 Module 03).

CAMERA POSES MUST BE ACCURATE. NeRF assumes them known,
and in practice they come from COLMAP (Module 05). A pose
error of one degree produces visible blur that looks
exactly like under-training -- which sends people to the
wrong fix and wastes days.

WHAT GOES WRONG
  too few views      -> FLOATERS: density in empty space
                        that happens to fit every input
                        image from the angles you captured
  all views one side -> the unseen side is INVENTED, with
                        no indication that it was
  moving objects     -> smeared, exactly as in Module 05
  changing exposure  -> baked into the radiance field as
                        if it were scene appearance
  mirrors            -> modelled as GEOMETRY BEHIND the
                        mirror, which is self-consistent
                        with every input view and
                        completely wrong"""),
  ("p", "<b>Every one of those failures is Module 01's ill-posedness, "
        "arriving in a new costume.</b> <b>The optimiser found a scene "
        "consistent with the photographs that is not the real scene</b> "
        "— which is permitted, because the inversion is "
        "under-determined and nothing in the objective prefers the true "
        "explanation. <b>The mirror case is the most illuminating:</b> "
        "<b>a room behind the glass explains every input view "
        "correctly</b>, it is geometrically reasonable, and it is "
        "physically wrong — and no amount of additional views from "
        "the same side of the mirror resolves it. <b>Resolving it needs a "
        "prior about materials</b>, which is Module 01 &sect;3's fourth "
        "strategy and is what reflection-aware variants supply."),

  ("break",),
  ("h1", "3 &nbsp; Gaussian splatting"),
  ("table", ["", "NeRF (radiance field)", "3D Gaussian splatting"],
   [["<b>Scene stored as</b>",
     "<b>An implicit function — an MLP, grid, or hash table.</b>",
     "<b>An explicit set of 3D Gaussians, each with position, "
     "covariance, opacity, and view-dependent colour.</b>"],
    ["<b>Rendering</b>",
     "<b>Ray marching, with many network queries per pixel.</b>",
     "<b>Project each Gaussian to 2D, rasterise, and alpha-blend sorted "
     "by depth.</b>"],
    ["<b>Render speed</b>", "Seconds per frame in the original method.",
     "<b>Real time — hundreds of frames per second.</b>"],
    ["<b>Training time</b>", "Hours.", "<b>Minutes.</b>"],
    ["<b>Editability</b>",
     "<b>Hard — the network weights are not spatially local, so "
     "editing one region affects others.</b>",
     "<b>Easy — move, delete, or recolour individual "
     "primitives.</b>"],
    ["<b>Memory</b>", "Small — a network of a few megabytes.",
     "<b>Large — millions of primitives, hundreds of "
     "megabytes.</b>"]],
   [0.17, 0.39, 0.44]),
  ("p", "<b>Splatting won on speed and editability by going back to an "
        "explicit representation</b>, after several years in which "
        "implicit neural representations were assumed to be the "
        "direction. <b>That is a useful reminder that implicit is not "
        "automatically better</b> — the implicit formulation was "
        "solving a differentiability problem, and once that problem could "
        "be solved explicitly, the explicit form's advantages "
        "reasserted themselves."),
  ("callout", "Why splatting is fast, exactly",
   ["<b>A 3D Gaussian projects to a 2D Gaussian under perspective "
    "projection</b> (to a good approximation), <b>and a 2D Gaussian can "
    "be rasterised</b> — so the entire scene renders through the "
    "graphics pipeline of CSCE 641 rather than by marching rays through "
    "a field.",
    "<b>There is no network query per sample.</b> NeRF evaluates an MLP "
    "hundreds of times per pixel; splatting alpha-blends a few dozen "
    "primitives per pixel, with no neural network in the rendering loop "
    "at all.",
    "<b>And alpha blending sorted by depth is differentiable</b>, which "
    "recovers &sect;2's essential property with an explicit primitive "
    "— <b>because a Gaussian has no hard boundary</b>, so its "
    "contribution to a pixel varies smoothly as it moves. The "
    "discontinuity that defeated triangles is absent.",
    "<b>The adaptive density control is the genuinely clever part.</b> "
    "<b>Split Gaussians where the positional gradient is large (the "
    "representation is under-resolved there) and prune ones that become "
    "transparent</b>, so <b>the representation adapts its own resolution "
    "to the scene during optimisation</b> — which is what replaces "
    "NeRF's hierarchical sampling and is why no resolution needs to be "
    "chosen in advance."]),

  ("h1", "4 &nbsp; An honest comparison"),
  ("ul", ["<b>Novel-view image quality: neural methods win "
          "decisively.</b> <b>They optimise exactly that objective</b>, "
          "so the result is unsurprising rather than mysterious — "
          "and it is worth stating that way, because it sets the correct "
          "expectation for the other rows.",
          "<b>Mesh quality for downstream geometric use: classical "
          "multi-view stereo remains competitive and is frequently "
          "better.</b> <b>A radiance field is not a surface</b> "
          "(&sect;2), and a mesh extracted from one inherits the "
          "density field's ambiguity at every thin or transparent "
          "structure.",
          "<b>Robustness to few views or badly distributed views: "
          "classical wins.</b> <b>Multi-view stereo degrades to a sparse "
          "or incomplete reconstruction, which is honest; neural methods "
          "degrade to confident fabrication</b> (&sect;2's floaters and "
          "invented back sides), which is not. <b>That difference in "
          "failure mode matters more than the average-case quality "
          "gap</b> for any system that must know when it does not "
          "know.",
          "<b>Metric accuracy: both depend on the same COLMAP poses</b>, "
          "so <b>neither escapes Module 01's scale theorem</b> — and "
          "a neural reconstruction is no more metric than the structure "
          "from motion that initialised it.",
          "<b>And for a game engine: splatting is the one you can "
          "actually render</b> at interactive rates on a consumer GPU, "
          "which is why this track cares and why it moved into production "
          "tools within two years of publication.",
          "<b>So choose by what the output is for:</b> <b>an image, a "
          "mesh, or a measurement.</b> <b>They are different "
          "deliverables, and the methods rank differently on each</b> "
          "— which is the same discipline as Module 09 &sect;4's "
          "metric choice, applied to reconstruction."]),
  ("callout", "Why this module is the centre of the track",
   ["<b>CSCE 641 gave the rasterisation pipeline. CSCE 647 gave the "
    "rendering integral, the volumetric transport, and the sampling "
    "theory. CSCE 645 gave the surface representations. CSCE 669 gave "
    "the optimiser and the convergence theory.</b>",
    "<b>This module is all four at once, pointed backwards:</b> a "
    "renderer, differentiated, optimised against photographs, producing a "
    "scene. <b>Nothing in it would be approachable without those four, "
    "and with them it is almost straightforward.</b>",
    "<b>Which is why Graphics and Vision are one track and not two.</b> "
    "<b>The forward model is the thing you invert, and you cannot invert "
    "what you do not understand</b> — which was Module 01's opening "
    "claim, and this module is the evidence for it.",
    "<b>And it is the clearest case in this program of a subject that "
    "could only have been built by people who knew both halves.</b> The "
    "method is not a vision advance that happens to use rendering, nor a "
    "graphics advance that happens to use photographs; <b>it is the "
    "composition, and it was unavailable to anyone holding only one "
    "side.</b>"]),
 ],
 "resources": [
   ("Mildenhall et al. — NeRF: Representing Scenes as Neural "
    "Radiance Fields (free)",
    "https://www.matthewtancik.com/nerf",
    "<b>The &sect;1 and &sect;2 method.</b> Readable, with a reference "
    "implementation and the positional-encoding ablation that makes "
    "&sect;2's point."),
   ("Kerbl et al. — 3D Gaussian Splatting for Real-Time Radiance "
    "Field Rendering (free)",
    "https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/",
    "<b>The &sect;3 method</b>, with the adaptive density control "
    "described properly."),
   ("Müller et al. — Instant Neural Graphics Primitives "
    "(free)",
    "https://nvlabs.github.io/instant-ngp/",
    "<b>The multiresolution hash encoding</b> that made radiance fields "
    "train in seconds — and a good example of a data-structure "
    "contribution beating an architectural one."),
   ("Tewari et al. — Advances in Neural Rendering (free survey)",
    "https://arxiv.org/abs/2111.05849",
    "<b>The field laid out systematically</b>, including the "
    "surface-versus-volume question of &sect;2."),
 ],
 "exercises": [
   "<b>Implement volume rendering</b> along a ray for a hand-built "
   "density field, and verify the transmittance integral.",
   "<b>Train a small NeRF on your own captured scene</b>, using COLMAP "
   "poses.",
   "<b>Train it without positional encoding</b> and compare. Report the "
   "frequency content of each result.",
   "<b>Perturb the camera poses by one degree</b> and report the "
   "degradation.",
   "<b>Capture a scene from one side only</b> and render the unseen side. "
   "Report what was invented.",
   "<b>Capture a scene containing a mirror</b> and inspect the recovered "
   "geometry behind it.",
   "<b>Train Gaussian splatting on the same scene</b> and compare "
   "training time, render speed, and quality.",
   "<b>Run COLMAP's dense multi-view stereo on the same images</b> and "
   "compare the meshes.",
   "<b>Compare all three on a deliberately sparse capture</b> of ten "
   "images, and describe how each fails.",
   "<b>Import a splat into a renderer</b> and report the achieved frame "
   "rate on your GPU.",
 ],
 "selfcheck": [
   "How does neural reconstruction avoid the correspondence problem?",
   "Write the volume rendering integral and say what transmittance is.",
   "Why is a volume used rather than a surface?",
   "Why is positional encoding necessary, and what theory explains it?",
   "Name five NeRF failure modes and relate each to Module 01.",
   "Why is the mirror failure particularly instructive?",
   "Why is Gaussian splatting fast, in three specific respects?",
   "What is adaptive density control and what does it replace?",
   "Compare neural and classical reconstruction on five axes.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Evaluation and Failure",
 "subtitle": "What a vision system can be trusted to do.",
 "question": "Your model scores 94%. On what, and where will it break?",
 "outcomes": [
     "Explain distribution shift and its kinds.",
     "Design an evaluation that measures robustness.",
     "Explain shortcut learning and detect it.",
     "Explain adversarial examples and their practical relevance.",
     "State a scoped trust claim for a vision system.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Shift",
   "blurb": "The test set is not the world."},

  {"t": "table", "kicker": "Shift", "title": "The kinds of distribution shift",
   "header": ["Kind", "What changes", "Example"],
   "widths": [2.6, 4.2, 5.2],
   "rows": [
     ["<b>Covariate</b>", "<b>The inputs; the labelling rule is unchanged</b>", "<b>New camera, new lighting, new location</b>"],
     ["<b>Label</b>", "The class frequencies", "<b>A rare condition becomes common</b>"],
     ["<b>Concept</b>", "<b>The relationship itself</b>", "What counts as 'damaged' is redefined"],
     ["<b>Subpopulation</b>", "<b>A group under-represented in training</b>", "<b>Skin tones, accents, vehicle types</b>"],
     ["<b>Adversarial</b>", "Inputs chosen to fail", "Deliberate attack"],
   ],
   "footnote": "<b>Covariate shift is the one vision systems meet "
               "constantly</b> — every new deployment site is one "
               "— and subpopulation shift is the one that causes "
               "harm.",
   "note": "Naming the kinds lets students diagnose rather than just "
           "worry."},

  {"t": "callout", "title": "The benchmark gap is measured, not hypothetical",
   "kind": "What the literature establishes",
   "body": ["<b>Models evaluated on a freshly collected test set drawn "
            "the same way as the original drop several points</b> "
            "— on ImageNet, measurably, in a careful replication.",
            "<b>Under corruptions — blur, noise, weather, "
            "compression — accuracy falls far more</b>, and the fall "
            "is not predicted by clean accuracy.",
            "<b>And rankings change.</b> <b>The best model on the clean "
            "benchmark is frequently not the best under shift</b>, so "
            "selecting on clean accuracy selects the wrong model.",
            "<b>Which means your test set measures your test set.</b> "
            "<b>It is a lower bound on difficulty and not an estimate of "
            "deployed performance</b> — and the gap is a research "
            "finding, not a cautious guess."]},

  {"t": "section", "label": "Part 2", "title": "Shortcuts",
   "blurb": "The model learned something real that you did not want."},

  {"t": "code", "kicker": "Shortcuts", "title": "The documented cases, and how to find yours",
   "lang": "text", "code": """
  WHAT HAPPENED, IN REAL SYSTEMS:
    a pneumonia classifier that read the HOSPITAL's
        scanner signature, because prevalence differed
        between hospitals
    a skin-lesion classifier that used the RULER placed
        beside malignant lesions for scale
    a cow detector that used GRASS, and failed on cows
        on a beach
    a "COVID from chest X-ray" model that used patient
        POSITIONING, which differed between wards

  EVERY ONE WORKED ON THE TEST SET. The shortcut was
  genuinely predictive there, because the test set came
  from the same collection process.

  HOW TO FIND YOURS
    occlude parts of the input; if accuracy survives
        without the object, the object was not being used
    evaluate per SOURCE -- per hospital, camera, site --
        and look for a model that is excellent within each
        and poor across
    look at saliency, with suspicion (they are unreliable,
        but a map pointing at the corner is a signal)
    test on data you collected YOURSELF, differently
    and show the FAILURE GALLERY to a domain expert
""",
   "caption": "<b>A shortcut is not a bug in the model; it is a "
              "correlation in your data that you did not intend to "
              "teach</b> — which is why the fix is in the data.",
   "note": "The per-source evaluation is the most reliable detector and "
           "is cheap."},

  {"t": "section", "label": "Part 3", "title": "Adversarial examples",
   "blurb": "What they prove, and what they do not."},

  {"t": "callout", "title": "Adversarial examples, in proportion",
   "kind": "Neither dismissed nor overstated",
   "body": ["<b>An imperceptible, carefully computed perturbation "
            "flips a confident prediction.</b> This is a real and "
            "reproducible property of essentially every vision model.",
            "<b>What it establishes:</b> the decision boundary is far "
            "closer to typical inputs than the model's confidence "
            "suggests. <b>That is a statement about calibration and "
            "geometry</b>, and it is important.",
            "<b>What it does not establish:</b> that the model is "
            "useless. <b>Most deployment failures are ordinary "
            "distribution shift, not attacks</b> — and that is where "
            "effort belongs for most systems.",
            "<b>When it does matter:</b> an adversary benefits and can "
            "control the input. <b>Physical attacks exist</b> — "
            "printed patterns that defeat detectors — <b>so assess "
            "by threat model, not by whether the phenomenon is "
            "real.</b>"]},

  {"t": "section", "label": "Part 4", "title": "The claim",
   "blurb": "What you can honestly say."},

  {"t": "bullets", "kicker": "Evaluation", "title": "What a real evaluation contains",
   "items": [
     "<b>A test set collected separately</b> from training — "
     "different day, place, or device. <b>Not a random split.</b>",
     "",
     "<b>Per-subgroup results</b> for every subgroup you can identify. "
     "<b>Aggregate accuracy conceals the failures that matter.</b>",
     "",
     "<b>Performance under corruption:</b> blur, noise, compression, "
     "low light, weather. <b>Cheap to generate and highly "
     "informative.</b>",
     "",
     "<b>A failure gallery</b>, grouped by hypothesised cause, with at "
     "least twenty cases.",
     "",
     "<b>Calibration</b> — a reliability diagram "
     "(CSCE 633 M12 §3) — <b>and latency on the real "
     "hardware.</b>",
   ],
   "footnote": "<b>Report the worst subgroup and the corrupted number as "
               "prominently as the headline</b>, because those are the "
               "numbers that describe deployment."},

  {"t": "callout", "title": "The honest claim is scoped",
   "kind": "The deliverable of this course",
   "body": ["<b>Not: 'our detector achieves 94% accuracy'.</b> That "
            "sentence has no scope and is therefore not checkable.",
            "<b>But: '94% on held-out data from the same three sites; "
            "81% at a fourth site; 62% under heavy rain; worst subgroup "
            "71%; miscalibrated above 0.9 confidence; 28 ms on the target "
            "device.'</b>",
            "<b>That is longer, less impressive, and actually "
            "usable</b> — it tells someone whether to deploy it and "
            "under what conditions.",
            "<b>And it is the same discipline as every course in this "
            "program:</b> <b>state what you measured, state what you "
            "assumed, and never claim more than you established.</b>"]},
 ],
 "takeaways": [
   "Distribution shift has five kinds; covariate shift is what vision "
   "systems meet constantly and subpopulation shift is what causes harm.",
   "The benchmark gap is measured: models drop on freshly collected test "
   "sets and drop far more under corruption, and rankings change.",
   "So selecting a model on clean benchmark accuracy can select the wrong "
   "model for deployment.",
   "A shortcut is a real correlation in your data that you did not intend "
   "to teach, and per-source evaluation is the cheapest reliable "
   "detector.",
   "Adversarial examples establish that the decision boundary is closer "
   "than confidence suggests; most deployment failures are ordinary "
   "shift.",
   "The honest claim is scoped to conditions, and it is longer, less "
   "impressive, and actually usable.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Distribution shift"),
  ("table", ["Kind", "What changes", "Example in vision"],
   [["<b>Covariate shift</b>",
     "<b>The input distribution; the labelling rule is unchanged.</b>",
     "<b>A new camera, new lighting, a new installation site, a "
     "different season.</b> <b>Every new deployment is one of these.</b>"],
    ["<b>Label shift</b>", "The class frequencies.",
     "<b>A condition that was rare in the training hospital is common in "
     "the deployment one</b>, so the calibrated thresholds are wrong."],
    ["<b>Concept shift</b>",
     "<b>The relationship between input and label itself.</b>",
     "What counts as 'damaged' or 'defective' is redefined by the people "
     "using the system."],
    ["<b>Subpopulation shift</b>",
     "<b>A group that was under-represented in training becomes a larger "
     "share of the input.</b>",
     "<b>Skin tones, body types, vehicle types, regional signage.</b> "
     "<b>This is the kind that causes harm</b>, and aggregate accuracy "
     "conceals it by construction."],
    ["<b>Adversarial shift</b>", "Inputs deliberately chosen to fail.",
     "A targeted attack — see &sect;3 for the proportionate "
     "response."]],
   [0.18, 0.34, 0.48]),
  ("callout", "The benchmark gap is measured, not hypothetical",
   ["<b>When researchers carefully collected a new ImageNet test set "
    "following the original protocol as closely as they could, every model "
    "dropped by a substantial and consistent margin.</b> Not because the "
    "new set was harder in any identifiable way, but because the original "
    "had been selected against by a decade of model development.",
    "<b>Under corruptions — blur, Gaussian noise, simulated "
    "weather, JPEG compression — accuracy falls far more</b>, and "
    "<b>the size of the fall is not predicted by clean accuracy</b>, "
    "which means it has to be measured separately.",
    "<b>And rankings change.</b> <b>The best model on the clean "
    "benchmark is frequently not the best under shift</b> — so "
    "<b>selecting a model on clean accuracy can select the wrong model "
    "for deployment</b>, which is a stronger and more actionable claim "
    "than 'accuracy drops'.",
    "<b>Which means your test set measures your test set.</b> <b>It is a "
    "lower bound on the difficulty of the real problem and not an "
    "estimate of deployed performance</b> — and this is a research "
    "finding with numbers attached, not a cautious hedge. <b>It is "
    "CSCE 633 Module 12's distribution-shift section, with the vision "
    "literature's specific measurements behind it.</b>"]),

  ("h1", "2 &nbsp; Shortcut learning"),
  ("code", """WHAT HAPPENED, IN REAL DEPLOYED AND PUBLISHED SYSTEMS:

  a pneumonia classifier that read the HOSPITAL's scanner
      signature from image metadata burned into the pixels,
      because prevalence differed between hospitals

  a skin-lesion classifier that used the RULER that
      clinicians place beside lesions they already suspect
      are malignant

  a cow detector that relied on GRASS, and failed on
      photographs of cows on a beach

  a "COVID from chest X-ray" model that used patient
      POSITIONING, which differed between the wards where
      positive and negative cases were imaged

EVERY ONE OF THESE WORKED ON THE TEST SET. The shortcut was
genuinely predictive there, because the test set came from
the same collection process as the training set.

HOW TO FIND YOURS
  occlude parts of the input; if accuracy survives with
      the object removed, the object was not being used
  evaluate PER SOURCE -- per hospital, camera, site,
      photographer -- and look for a model that is
      excellent within each source and poor across them
  look at saliency maps, with suspicion: they are
      unreliable, but a map pointing at a corner watermark
      is a signal worth following
  test on data YOU collected, differently, yourself
  and show the failure gallery to a domain expert"""),
  ("p", "<b>A shortcut is not a bug in the model.</b> <b>It is a real "
        "correlation in your data that you did not intend to teach</b>, "
        "and the model found it because it was easier to use than the "
        "feature you had in mind — which is exactly what an "
        "optimiser should do. <b>So the fix is in the data and the "
        "evaluation, not in the architecture</b>, and <b>per-source "
        "evaluation is the cheapest reliable detector</b>: it costs a "
        "<code>groupby</code> and it catches most of the documented cases "
        "above."),

  ("break",),
  ("h1", "3 &nbsp; Adversarial examples"),
  ("callout", "Adversarial examples, in proportion",
   ["<b>An imperceptible, carefully computed perturbation of an image "
    "flips a confident prediction to a different confident "
    "prediction.</b> This is a real, reproducible property of essentially "
    "every vision model, including large and modern ones, and it has "
    "resisted a decade of defences.",
    "<b>What it establishes:</b> <b>the decision boundary lies far "
    "closer to typical inputs than the model's confidence suggests.</b> "
    "<b>That is a statement about calibration and about the geometry of "
    "the learned function</b>, and it is genuinely important — it "
    "means confidence cannot be read as distance from the boundary.",
    "<b>What it does not establish:</b> that the model is useless, or "
    "that robustness to attack is the main robustness problem. <b>The "
    "overwhelming majority of deployment failures are ordinary "
    "distribution shift and shortcut learning, not attacks</b> — and "
    "for most systems that is where the effort belongs.",
    "<b>When it does matter:</b> when an adversary benefits from a "
    "misprediction and can influence the input. <b>Physical attacks "
    "exist</b> — printed patterns that defeat detectors, stickers "
    "that alter sign classification — <b>so the assessment should "
    "be by threat model rather than by whether the phenomenon is "
    "real.</b> <b>It is real; whether it is your problem is a separate "
    "question, and conflating the two leads both to complacency and to "
    "misdirected effort.</b>"]),

  ("h1", "4 &nbsp; What a real evaluation contains"),
  ("ul", ["<b>A test set collected separately from the training data</b> "
          "— a different day, a different place, a different device, "
          "a different operator. <b>Not a random split of one "
          "collection</b>, which measures only interpolation within that "
          "collection.",
          "<b>Per-subgroup results for every subgroup you can "
          "identify.</b> <b>Aggregate accuracy conceals exactly the "
          "failures that matter</b> — a model at 94% overall can be "
          "at 61% on a subgroup that is 5% of the data, and the aggregate "
          "will not move.",
          "<b>Performance under corruption:</b> blur, Gaussian and shot "
          "noise, JPEG compression, low light, simulated rain and fog, "
          "and the resolution changes of Module 08 &sect;3. <b>These "
          "are cheap to generate synthetically and highly informative</b>, "
          "and standard corruption benchmarks exist.",
          "<b>A failure gallery of at least twenty cases, grouped by "
          "hypothesised cause</b> — which is the single most useful "
          "artefact for anyone deciding whether to rely on the system, "
          "and the one most often omitted.",
          "<b>Calibration</b> — a reliability diagram (CSCE 633 "
          "Module 12 &sect;3), because &sect;3 established that "
          "confidence is not distance from the boundary — <b>and "
          "latency measured on the hardware it will actually run on</b>, "
          "not on a development GPU."]),
  ("callout", "The honest claim is scoped",
   ["<b>Not: 'our detector achieves 94% accuracy'.</b> That sentence has "
    "no scope attached, so <b>it is not checkable and tells a reader "
    "nothing about whether to use the system.</b>",
    "<b>But: '94% on held-out data from the same three sites; 81% at a "
    "fourth site not used in training; 62% under heavy rain; worst "
    "identified subgroup 71%; systematically overconfident above 0.9; "
    "28 ms per frame on the target device.'</b>",
    "<b>That is longer, less impressive, and actually usable.</b> <b>It "
    "tells someone whether to deploy the system and under what "
    "conditions</b>, which is the only purpose an evaluation has.",
    "<b>And it is the same discipline as every course in this "
    "program</b>, in the form it takes when the input is the physical "
    "world: <b>state what you measured, state what you assumed, and never "
    "claim more than you established.</b> <b>In this course the "
    "assumption that needs stating is almost always about the capture "
    "conditions</b> — the camera, the lighting, the site — "
    "because that is what the model silently learned alongside the "
    "task."]),
 ],
 "resources": [
   ("Recht et al. — Do ImageNet Classifiers Generalize to ImageNet? "
    "(free)",
    "https://arxiv.org/abs/1902.10811",
    "<b>The &sect;1 replication.</b> The measured gap, with the "
    "collection protocol described in enough detail to assess."),
   ("Hendrycks & Dietterich — Benchmarking Neural Network "
    "Robustness to Common Corruptions (free)",
    "https://arxiv.org/abs/1903.12261",
    "<b>The corruption benchmark of &sect;4</b>, and the finding that "
    "clean accuracy does not predict corrupted accuracy."),
   ("Geirhos et al. — Shortcut Learning in Deep Neural Networks "
    "(free)",
    "https://arxiv.org/abs/2004.07780",
    "<b>The &sect;2 reference</b>, with the documented cases and the "
    "detection strategies."),
   ("Madry et al. — Towards Deep Learning Models Resistant to "
    "Adversarial Attacks (free)",
    "https://arxiv.org/abs/1706.06083",
    "<b>The &sect;3 phenomenon treated rigorously</b>, with the threat "
    "model stated explicitly — which is the part worth imitating."),
 ],
 "exercises": [
   "<b>Collect a second test set yourself</b>, differently, and report "
   "the gap against your original.",
   "<b>Apply ten standard corruptions</b> and plot accuracy against "
   "severity.",
   "<b>Rank three models on clean data and on corrupted data</b> and "
   "report whether the ranking changes.",
   "<b>Evaluate per source</b> — per camera, site, or session — "
   "and look for the within/across gap.",
   "<b>Occlude the object of interest</b> and report how much accuracy "
   "survives.",
   "<b>Deliberately introduce a shortcut</b> into a training set and "
   "confirm the model takes it.",
   "<b>Then detect it</b> with each of the methods in &sect;2 and report "
   "which worked.",
   "<b>Generate adversarial examples</b> for your model and measure the "
   "perturbation size needed.",
   "<b>Plot a reliability diagram</b> and report where the model is "
   "overconfident.",
   "<b>Write the scoped claim</b> for your own project in the form of "
   "&sect;4's callout.",
 ],
 "selfcheck": [
   "Name five kinds of distribution shift and an example of each.",
   "Which kind do vision systems meet constantly, and which causes "
   "harm?",
   "What does the ImageNet replication establish?",
   "Why can clean benchmark accuracy select the wrong model?",
   "Give four documented shortcuts and say why each passed its test "
   "set.",
   "Give five ways to detect a shortcut, and the cheapest reliable one.",
   "What do adversarial examples establish, and what do they not?",
   "Name five components of a real evaluation.",
   "Write a scoped trust claim.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Vision in Systems",
 "subtitle": "Running continuously, on real hardware, over time.",
 "question": "What changes when the system has to run, not just score?",
 "outcomes": [
     "Reason about the latency budget of a perception system.",
     "Choose where computation happens.",
     "Explain what degrades over time and how to detect it.",
     "Design a perception system that knows when it is "
     "unreliable.",
     "State the course's closing position.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Latency",
   "blurb": "The deadline is part of the specification."},

  {"t": "callout", "title": "A late answer is a wrong answer",
   "kind": "The constraint that reorders everything",
   "body": ["<b>For a system acting on the world, perception has a "
            "deadline.</b> A 200 ms detection on a moving platform "
            "describes where things were, not where they are.",
            "<b>So the correct metric is accuracy <i>at the "
            "deadline</i></b>, and a faster, less accurate model is "
            "frequently the better one. <b>Streaming perception metrics "
            "exist to measure exactly this.</b>",
            "<b>And the budget is end to end:</b> capture, transfer, "
            "preprocess, inference, postprocess, act. <b>Inference is "
            "often not the largest term</b>, and optimising it first is a "
            "common mistake.",
            "<b>Measure the whole pipeline before optimising any of "
            "it</b> — CSCE 735's profiling discipline and CSCE 678's "
            "tail-latency lesson, both applying directly."]},

  {"t": "table", "kicker": "Budget", "title": "Where the milliseconds go",
   "header": ["Stage", "Typical cost", "What helps"],
   "widths": [2.6, 3.8, 5.6],
   "rows": [
     ["<b>Capture + exposure</b>", "<b>8–33 ms</b>", "<b>Higher frame rate; shorter exposure</b>"],
     ["<b>Transfer to GPU</b>", "<b>1–10 ms</b>", "<b>Pinned memory; avoid round trips</b>"],
     ["<b>Preprocess</b>", "<b>1–20 ms</b>", "<b>Do it on the GPU. Often the hidden cost</b>"],
     ["<b>Inference</b>", "5–100 ms", "Quantisation, pruning, a smaller model"],
     ["<b>Postprocess (NMS)</b>", "<b>1–30 ms</b>", "<b>Batched GPU NMS; cap the candidates</b>"],
     ["<b>Tail latency</b>", "<b>2–5× the median</b>", "<b>Budget for p99, not the mean (CSCE 678)</b>"],
   ],
   "footnote": "<b>Preprocessing and NMS on the CPU are the two costs "
               "people forget</b>, and together they can exceed "
               "inference.",
   "note": "The p99 point is the one that causes production incidents."},

  {"t": "section", "label": "Part 2", "title": "Where to compute",
   "blurb": "Device, edge, or cloud."},

  {"t": "bullets", "kicker": "Placement", "title": "Choosing where inference runs",
   "items": [
     "<b>On device:</b> lowest latency, no network dependency, no "
     "image leaves the user's hardware. <b>Constrained by memory and "
     "power.</b>",
     "",
     "<b>On a local edge machine:</b> more compute, a few milliseconds "
     "of network, images stay on the premises.",
     "",
     "<b>In the cloud:</b> unlimited compute, 50–500 ms of "
     "round trip, and <b>every frame is transmitted and may be "
     "retained.</b>",
     "",
     "<b>Hybrid is usual:</b> a small on-device model handles the "
     "common case and triggers a larger one only when uncertain.",
     "",
     "<b>And camera data is personal data.</b> <b>Where it goes is a "
     "design decision with consequences beyond latency</b>, and on-device "
     "inference is a privacy property, not only a performance one.",
   ],
   "footnote": "<b>The hybrid cascade is the standard architecture</b> "
               "and it needs a usable uncertainty estimate to route on "
               "— which Module 12 §3 says you do not get for "
               "free."},

  {"t": "section", "label": "Part 3", "title": "Degradation",
   "blurb": "Systems that worked, and then did not."},

  {"t": "code", "kicker": "Degradation", "title": "What decays, and how to notice",
   "lang": "text", "code": """
  WHAT DECAYS
    CALIBRATION   thermal drift, mechanical shock, lens
                  cleaning, remounting   (Module 02 Part 4)
    THE SCENE     new signage, repainted walls, a moved
                  camera, seasonal foliage, a new product
    THE LENS      dust, scratches, a smeared cover
    THE CAMERA    sensor ageing, a changed auto-exposure
                  firmware update
    THE LABELS    what the operators consider a positive
                  drifts -- concept shift (Module 12)

  HOW TO NOTICE WITHOUT GROUND TRUTH
    track the INPUT distribution: mean brightness, contrast,
        sharpness, feature-count per frame. A shift here
        precedes an accuracy drop and needs no labels.
    track the OUTPUT distribution: detection rate per hour,
        confidence histogram, class mix. A change without a
        known cause is the alarm.
    track REPROJECTION ERROR continuously if you do
        geometry -- it is a free, direct calibration monitor
    reserve a FIXED set of reference inputs and re-score
        them weekly
    and SAMPLE for human review on a schedule, not only
        when something looks wrong

  A SYSTEM WITH NO MONITORING IS NOT DEPLOYED. IT IS
  ABANDONED IN PRODUCTION.
""",
   "caption": "<b>Monitoring the input distribution needs no labels and "
              "catches most degradation early</b>, which makes it the "
              "highest-value thing to build.",
   "note": "The label-free monitoring point is what makes this "
           "actionable."},

  {"t": "section", "label": "Part 4", "title": "Knowing when not to answer",
   "blurb": "The property that makes a perception system usable."},

  {"t": "callout", "title": "Build the refusal in",
   "kind": "The design principle",
   "body": ["<b>A system that answers everything confidently is less "
            "useful than one that abstains when uncertain</b>, because "
            "the downstream consumer can handle 'unknown' and cannot "
            "handle 'wrong'.",
            "<b>Geometry gives you honest signals:</b> inlier counts, "
            "reprojection error, conditioning, left–right "
            "consistency, track closure error. <b>Use them.</b>",
            "<b>Learned components do not, by default</b> "
            "(Module 12 §3) — so add an explicit "
            "out-of-distribution check, or calibrate and threshold.",
            "<b>And make the abstention <i>visible</i></b>. <b>A depth "
            "map with a validity mask</b> (Module 06 §4) <b>is "
            "the model: the measurement, plus where it is not a "
            "measurement.</b>"]},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can calibrate a camera, match features robustly, "
            "recover pose, reconstruct a scene, and diagnose why a "
            "reconstruction failed from its symptom.</b>",
            "<b>You can train and honestly evaluate a learned "
            "component</b>, and say what it can be trusted to do and "
            "under what conditions.",
            "<b>And you understand Module 11 both ways round</b> "
            "— which is the thing this track exists to produce. "
            "<b>The forward model is what you invert, and the inverse is "
            "ill-posed, and both facts are load-bearing.</b>",
            "<b>The closing rule is the program's, unchanged:</b> "
            "<b>state what you measured, state what you assumed, and "
            "never claim more than you established.</b> <b>Here it means "
            "stating the capture conditions</b>, because that is what the "
            "system quietly learned along with the task."]},
 ],
 "takeaways": [
   "A late answer is a wrong answer, so the right metric is accuracy at "
   "the deadline and a faster, less accurate model is often better.",
   "The latency budget is end to end, and preprocessing and NMS on the CPU "
   "are the two costs people forget.",
   "Budget for p99 rather than the median, which is CSCE 678's tail "
   "latency lesson applied to perception.",
   "Camera data is personal data, so where inference runs is a privacy "
   "decision as much as a performance one.",
   "Monitoring the input distribution needs no labels and catches most "
   "degradation early — the highest-value thing to build.",
   "A system that abstains when uncertain is more useful than one that "
   "answers everything, because consumers handle 'unknown' and not "
   "'wrong'.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Latency"),
  ("callout", "A late answer is a wrong answer",
   ["<b>For any system that acts on the world, perception carries a "
    "deadline.</b> A detection that takes 200 milliseconds on a moving "
    "platform describes where objects <i>were</i>, not where they are "
    "— and at 10 m/s that is two metres of error that no accuracy "
    "improvement addresses.",
    "<b>So the correct metric is accuracy <i>at the deadline</i></b>, "
    "and <b>a faster, less accurate model is frequently the better "
    "choice</b>. <b>Streaming perception metrics exist to measure exactly "
    "this</b> — they evaluate the most recent available output "
    "against the current world state, which penalises latency and "
    "inaccuracy on the same scale.",
    "<b>And the budget is end to end:</b> capture and exposure, transfer "
    "to the accelerator, preprocessing, inference, postprocessing, and "
    "the action itself. <b>Inference is often not the largest term</b>, "
    "and <b>optimising it first is a common and expensive mistake</b> "
    "— quantising a model to save 10 ms while 25 ms goes to CPU-side "
    "image resizing.",
    "<b>So measure the whole pipeline before optimising any part of "
    "it.</b> <b>CSCE 735 Module 02's profiling discipline and "
    "CSCE 678 Module 06's tail-latency lesson both apply directly "
    "here</b>, and the second is the one that causes production incidents: "
    "a pipeline sized for the median fails at the 99th percentile, which "
    "on a 30 Hz camera happens eighteen times a minute."]),
  ("table", ["Stage", "Typical cost", "What helps"],
   [["<b>Capture and exposure</b>", "<b>8–33 ms</b>",
     "<b>A higher frame rate, a shorter exposure</b> — and note "
     "that exposure time is a latency term, which people forget."],
    ["<b>Transfer to the accelerator</b>", "<b>1–10 ms</b>",
     "<b>Pinned memory, and avoiding GPU-to-CPU-to-GPU round "
     "trips</b>, which are the usual hidden cost here."],
    ["<b>Preprocessing</b>", "<b>1–20 ms</b>",
     "<b>Do resizing and normalisation on the GPU.</b> <b>Frequently "
     "the single largest forgotten cost</b>, because it looks like "
     "bookkeeping rather than computation."],
    ["<b>Inference</b>", "5–100 ms",
     "Quantisation, pruning, distillation, or simply a smaller model "
     "(CSCE 636 Module 09)."],
    ["<b>Postprocessing (NMS)</b>", "<b>1–30 ms</b>",
     "<b>Batched GPU non-maximum suppression, and capping the candidate "
     "count before it</b> — an unbounded candidate list makes this "
     "term unbounded too."],
    ["<b>Tail latency</b>", "<b>2–5&times; the median</b>",
     "<b>Budget for p99, not the mean</b> — CSCE 678 Module 06. "
     "Garbage collection, thermal throttling, and contention all land "
     "here."]],
   [0.18, 0.21, 0.61]),

  ("h1", "2 &nbsp; Where computation happens"),
  ("ul", ["<b>On device.</b> <b>Lowest latency, no network dependency, "
          "and no image ever leaves the user's hardware.</b> Constrained "
          "by memory, by power, and by thermal budget — and the "
          "thermal constraint is real: sustained inference throttles, so "
          "a benchmark measured cold overstates sustained performance.",
          "<b>On a local edge machine.</b> More compute, a few "
          "milliseconds of local network, and images stay on the "
          "premises — which is frequently the deciding factor in "
          "regulated settings rather than the performance.",
          "<b>In the cloud.</b> Effectively unlimited compute, "
          "50–500 ms of round trip including the unpredictable "
          "parts, <b>and every frame is transmitted and may be "
          "retained</b>.",
          "<b>Hybrid is the usual answer:</b> a small on-device model "
          "handles the common case and escalates to a larger one only "
          "when it is uncertain. <b>The cascade needs a usable "
          "uncertainty estimate to route on</b> — and Module 12 "
          "&sect;3 established that you do not get one for free, so the "
          "calibration work is a prerequisite for the architecture rather "
          "than a refinement of it.",
          "<b>And camera data is personal data.</b> <b>Where it goes is "
          "a design decision with consequences well beyond latency</b> "
          "— retention, access, subject rights, and the "
          "irreversibility of a leak. <b>On-device inference is a privacy "
          "property, not only a performance one</b>, and it is worth "
          "choosing deliberately rather than arriving at by default."]),

  ("break",),
  ("h1", "3 &nbsp; Degradation over time"),
  ("code", """WHAT DECAYS

  CALIBRATION   thermal drift, mechanical shock, lens
                cleaning, remounting  (Module 02 section 4)
  THE SCENE     new signage, repainted walls, a camera
                nudged by 2 degrees, seasonal foliage,
                a new product line
  THE LENS      dust, scratches, a smeared protective cover
  THE CAMERA    sensor ageing, and an auto-exposure
                firmware update that changed the response
  THE LABELS    what the operators consider a positive
                drifts over months -- concept shift
                (Module 12 section 1)

HOW TO NOTICE WITHOUT GROUND TRUTH

  track the INPUT distribution: mean brightness, contrast,
      sharpness, detected feature count per frame. A shift
      here PRECEDES an accuracy drop and NEEDS NO LABELS.
  track the OUTPUT distribution: detections per hour, the
      confidence histogram, the class mix. A change with no
      known external cause is the alarm.
  track REPROJECTION ERROR continuously if you do geometry
      -- it is a free and direct calibration monitor.
  reserve a FIXED set of reference inputs and re-score them
      on a schedule, so you have a controlled comparison.
  and SAMPLE outputs for human review on a schedule, not
      only when something already looks wrong.

A SYSTEM WITH NO MONITORING IS NOT DEPLOYED.
IT IS ABANDONED IN PRODUCTION."""),
  ("p", "<b>Monitoring the input distribution needs no labels and catches "
        "most degradation early</b>, which makes it the highest-value "
        "thing to build and the first thing to build. <b>It is also the "
        "one piece of this that transfers unchanged to every other "
        "learned system</b> — CSCE 633 Module 13 made the same "
        "argument, and in vision it is easier, because the input "
        "statistics of an image are cheap to compute and genuinely "
        "informative."),

  ("h1", "4 &nbsp; Knowing when not to answer"),
  ("callout", "Build the refusal in",
   ["<b>A system that answers everything confidently is less useful than "
    "one that abstains when uncertain</b>, because <b>the downstream "
    "consumer can handle 'unknown' and cannot handle 'wrong'</b> — "
    "an unknown triggers a fallback, a human, or a retry, while a "
    "confident error propagates.",
    "<b>Geometry gives you honest signals, for free.</b> RANSAC inlier "
    "counts (Module 03 &sect;3), reprojection error (Module 05 "
    "&sect;2), estimate conditioning (Module 01 &sect;2), "
    "left–right stereo consistency (Module 06 &sect;4), track "
    "closure error (Module 07 &sect;4). <b>Every one of these is "
    "already computed and usually discarded.</b> <b>Use them.</b>",
    "<b>Learned components do not provide this by default</b> "
    "(Module 12 &sect;3), so it must be added: an explicit "
    "out-of-distribution detector, a calibrated confidence with a "
    "threshold chosen from the cost of each error type, or an ensemble "
    "disagreement measure.",
    "<b>And make the abstention visible in the output type.</b> <b>A "
    "depth map with a validity mask</b> (Module 06 &sect;4) <b>is the "
    "model for this: the measurement, together with where it is not a "
    "measurement.</b> <b>An interface that cannot express 'I do not "
    "know' forces every component downstream to guess on its behalf</b>, "
    "and that is where the hardest failures in perception systems come "
    "from."]),
  ("callout", "Where this course leaves you",
   ["<b>You can calibrate a camera and verify the calibration "
    "independently; detect, describe, and match features robustly; "
    "recover relative pose and triangulate; run and diagnose a structure "
    "from motion pipeline; compute dense depth and know where it is "
    "fabricated; and estimate motion while knowing what the estimate "
    "assumes.</b> <b>And you can diagnose a failed reconstruction from "
    "its symptom</b>, which is the skill that distinguishes someone who "
    "has used these tools from someone who has read about them.",
    "<b>You can train and honestly evaluate a learned component</b>, "
    "choose a transfer strategy from your data volume, pick a metric from "
    "the use rather than the leaderboard, detect a shortcut, and <b>state "
    "what the system can be trusted to do and under what "
    "conditions</b>.",
    "<b>And you understand Module 11 in both directions</b> — which "
    "is the thing this track exists to produce. <b>The forward model is "
    "what you invert; the inversion is ill-posed; and both facts are "
    "load-bearing in every method in this course.</b> Module 01 claimed "
    "that and Module 11 demonstrated it.",
    "<b>The closing rule is the program's, unchanged across nineteen "
    "courses:</b> <b>state what you measured, state what you assumed, "
    "and never claim more than you established.</b> <b>In computer "
    "vision it means stating the capture conditions</b> — the "
    "camera, the lighting, the sites, the season — <b>because that "
    "is what the system quietly learned alongside the task you intended "
    "to teach it.</b>"]),
 ],
 "resources": [
   ("Li, Wang & Ramanan — Towards Streaming Perception (free)",
    "https://arxiv.org/abs/2005.10420",
    "<b>The &sect;1 metric.</b> Evaluates perception against the world's "
    "current state rather than the frame's, which is the right "
    "formulation."),
   ("NVIDIA TensorRT and ONNX Runtime documentation (free)",
    "https://docs.nvidia.com/deeplearning/tensorrt/",
    "<b>The practical tools for &sect;1's inference row</b>, including "
    "quantisation and the profiling output that shows where the time "
    "goes."),
   ("Sculley et al. — Hidden Technical Debt in Machine Learning "
    "Systems (free)",
    "https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html",
    "<b>The &sect;3 argument</b>, and the clearest short statement of why "
    "monitoring is not optional."),
   ("Szeliski &mdash; Computer Vision, chapter 14 and the conclusions "
    "(free PDF)",
    "https://szeliski.org/Book/",
    "<b>A survey of applications and open problems</b>, and a reasonable "
    "place to choose what to study next."),
 ],
 "exercises": [
   "<b>Profile your own perception pipeline end to end</b> and report "
   "each stage's cost.",
   "<b>Report the p50, p95, and p99 latency</b> and the ratio between "
   "them.",
   "<b>Move preprocessing to the GPU</b> and report the change.",
   "<b>Measure sustained throughput over twenty minutes</b> and report "
   "the thermal throttling.",
   "<b>Implement a two-stage cascade</b> with a small model routing to a "
   "large one, and report the accuracy-latency trade.",
   "<b>Log input-distribution statistics</b> for your system over a week "
   "and plot them.",
   "<b>Deliberately smear the lens</b> and confirm the statistics move "
   "before accuracy does.",
   "<b>Track reprojection error continuously</b> and plot it against "
   "camera temperature.",
   "<b>Add an abstention path</b> to your system using a geometric "
   "signal, and report how often it fires.",
   "<b>Project 2 is now due.</b> Submit the trained component, the "
   "separately-collected test results, the per-subgroup and corrupted "
   "numbers, the failure gallery, the latency measurement, and the scoped "
   "claim.",
 ],
 "selfcheck": [
   "Why is a late answer a wrong answer, and what metric follows?",
   "Name the six stages of a latency budget and the two most often "
   "forgotten.",
   "Why budget for p99 rather than the median?",
   "Compare device, edge, and cloud placement on three axes.",
   "Why is on-device inference a privacy property?",
   "Name five things that degrade, and five ways to detect degradation "
   "without labels.",
   "Why is input-distribution monitoring the highest-value monitor?",
   "Why is abstention more useful than confident answering?",
   "Name five geometric signals you already compute and could abstain "
   "on.",
 ],
},

]
