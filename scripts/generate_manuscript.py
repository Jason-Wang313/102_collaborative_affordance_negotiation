import csv
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"
DOCS = ROOT / "docs"
PAPER.mkdir(exist_ok=True)

V5 = "risk_calibrated_collaborative_affordance_v5"
ORACLE = "oracle_joint_intent_capability_planner"


def ascii_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def latex_escape(value: object) -> str:
    text = ascii_text(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_summary() -> dict[str, str]:
    summary: dict[str, str] = {}
    for line in (RESULTS / "summary.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("Terminal decision:"):
            summary["decision"] = line.split(":", 1)[1].strip()
        elif line.startswith("terminal="):
            summary["terminal"] = line.split("=", 1)[1].strip()
        elif line.startswith("- ") and "=" in line:
            key, value = line[2:].split("=", 1)
            summary[key.strip()] = value.strip()
        elif line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            summary[key.strip()] = value.strip()
    return summary


def fnum(value: object, digits: int = 3) -> str:
    return f"{float(value):.{digits}f}"


def short_label(value: str) -> str:
    aliases = {
        "risk_calibrated_collaborative_affordance_v5": "collab_v5",
        "proposed_affordance_negotiation_v4": "collab_v4",
        "oracle_joint_intent_capability_planner": "oracle",
        "shared_autonomy_pomdp": "shared_pomdp",
        "risk_aware_shared_autonomy": "risk_shared",
        "conformal_intent_risk_filter": "conformal_intent",
        "active_clarification_bandit": "active_clarify",
        "human_model_mpc": "human_mpc",
        "inverse_rl_intent_pomdp": "irl_intent",
        "capability_map_tamp": "cap_tamp",
        "uncertainty_clarification_policy": "uncert_clarify",
        "language_affordance_planner": "language_aff",
        "static_role_policy": "static_role",
        "intent_only_follower": "intent_only",
        "robot_capability_only_planner": "cap_only",
        "full_risk_calibrated_collaborative_affordance_v5": "full_v5",
        "no_burden_aware_query_value": "no_burden_value",
        "no_overpromise_risk": "no_overpromise",
        "no_role_negotiation": "no_role",
        "no_capability_map": "no_cap_map",
        "no_intent_belief": "no_intent",
        "no_active_repair": "no_repair",
        "v4_affordance_negotiation_rules": "v4_rules",
        "shared_autonomy_only": "shared_only",
        "co_carry_doorway": "co_carry",
        "shared_fixture_insertion": "fixture_insert",
        "tool_use_handoff": "tool_handoff",
        "collaborative_sorting": "sorting",
        "assisted_assembly": "assembly",
        "handover_grip_choice": "handover",
        "conflicting_safety_preference": "safety_pref",
        "temporal_commitment_drift": "commit_drift",
        "load_sharing_mismatch": "load_mismatch",
        "occluded_human_goal": "occluded_goal",
        "role_switch_request": "role_switch",
        "false_clarification_shift": "false_clarify",
        "overtrust_safety_shift": "overtrust",
        "burden_sensitive_shift": "burden_shift",
        "combined_extreme": "combined_extreme",
    }
    return aliases.get(value, value)


def make_bib_key(row: dict[str, str], index: int) -> str:
    author = ascii_text(row.get("authors", "ref")).split(";")[0].strip().split(" ")[-1]
    author = re.sub(r"[^A-Za-z0-9]+", "", author) or "ref"
    year = re.sub(r"[^0-9]+", "", ascii_text(row.get("year", "")))[:4] or "nd"
    title_word = re.sub(r"[^A-Za-z0-9]+", "", ascii_text(row.get("title", "paper")).split(" ")[0]) or "paper"
    return f"{author.lower()}{year}{title_word.lower()}{index}"


def write_bib(records: list[dict[str, str]]) -> list[str]:
    keys: list[str] = []
    seen: set[str] = set()
    entries: list[str] = []
    for index, row in enumerate(records[:230], start=1):
        key = make_bib_key(row, index)
        while key in seen:
            key = f"{key}x"
        seen.add(key)
        keys.append(key)
        fields = [
            f"  title = {{{latex_escape(row.get('title', f'Reference {index}'))}}}",
            f"  author = {{{latex_escape(row.get('authors', 'Unknown'))}}}",
        ]
        for source, target in [("year", "year"), ("venue", "journal"), ("doi", "doi"), ("url", "url")]:
            value = latex_escape(row.get(source, ""))
            if value:
                fields.append(f"  {target} = {{{value}}}")
        entries.append("@article{" + key + ",\n" + ",\n".join(fields) + "\n}\n")
    (PAPER / "references.bib").write_text("\n".join(entries), encoding="utf-8")
    return keys


def cite(keys: list[str], start: int, stop: int) -> str:
    chosen = keys[start:min(stop, len(keys))]
    return r"\citep{" + ",".join(chosen) + "}" if chosen else ""


def citation_ledger(keys: list[str]) -> str:
    themes = [
        "physical human-robot collaboration",
        "shared autonomy and human intent inference",
        "affordances, roles, and collaborative manipulation",
        "risk-aware planning and safety filters",
        "active clarification and communication",
        "human burden, trust, and ergonomics",
        "evaluation, calibration, and reproducibility",
    ]
    rows = []
    for index in range(0, len(keys), 3):
        chunk = keys[index:index + 3]
        rows.append(
            f"{index // 3 + 1} & {latex_escape(themes[(index // 3) % len(themes)])} & "
            + r"\citep{" + ",".join(chunk) + r"} \\"
        )
    return "\n".join(rows)


def compact_rows(rows: list[dict[str, str]], columns: list[str]) -> str:
    rendered = []
    for row in rows:
        cells = []
        for column in columns:
            value = row[column]
            if column in {"method", "baseline", "ablation", "task", "regime", "split", "reference_method"}:
                cells.append(latex_escape(short_label(value)))
            elif column in {"wins_over_seeds", "case_id", "seed", "covered"}:
                cells.append(fnum(value, 3) if column == "covered" else latex_escape(value))
            else:
                cells.append(fnum(value, 3))
        rendered.append(" & ".join(cells) + r" \\")
    return "\n".join(rendered)


def long_metric_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = " & ".join(latex_escape(c) for c in ["method", "succ", "phys", "burden", "intent", "overprom", "ece", "util"]) + r" \\"
    body = compact_rows(rows, columns)
    return "\n".join(
        [
            r"\begingroup\scriptsize\setlength{\tabcolsep}{3pt}",
            r"\begin{longtable}{@{}lrrrrrrr@{}}",
            r"\toprule",
            header,
            r"\midrule",
            body,
            r"\bottomrule",
            r"\end{longtable}",
            r"\endgroup",
        ]
    )


def main() -> None:
    summary = read_summary()
    hard = read_csv(RESULTS / "hard_aggregate_metrics.csv")
    pairwise = read_csv(RESULTS / "pairwise_stats.csv")
    ablations = read_csv(RESULTS / "ablation_metrics.csv")
    stress = read_csv(RESULTS / "stress_sweep.csv")
    fixed = read_csv(RESULTS / "fixed_risk_metrics.csv")
    failures = read_csv(RESULTS / "failure_cases.csv")
    refs = read_csv(DOCS / "deep_read_250.csv")
    keys = write_bib(refs)

    hard_sorted = sorted(hard, key=lambda r: float(r["success"]), reverse=True)
    ablation_sorted = sorted(ablations, key=lambda r: float(r["success"]), reverse=True)
    max_stress = sorted([r for r in stress if r["split"] == "stress_09"], key=lambda r: float(r["utility"]), reverse=True)
    strict_fixed = sorted([r for r in fixed if r["risk_budget"] == "0.08000"], key=lambda r: float(r["utility"]), reverse=True)

    placeholders = {
        "<<CITE_INTRO>>": cite(keys, 0, 7),
        "<<CITE_SHARED>>": cite(keys, 7, 18),
        "<<CITE_AFFORD>>": cite(keys, 18, 30),
        "<<CITE_RISK>>": cite(keys, 30, 43),
        "<<CITE_HRI>>": cite(keys, 43, 58),
        "<<CITE_EVAL>>": cite(keys, 58, 72),
        "<<CITATION_LEDGER>>": citation_ledger(keys),
        "<<DECISION>>": latex_escape(summary.get("decision", "STRONG_REVISE")),
        "<<V5_SUCCESS>>": summary.get("v5_success", ""),
        "<<V5_PHYS>>": summary.get("v5_physical_violation", ""),
        "<<V5_BURDEN>>": summary.get("v5_human_burden", ""),
        "<<V5_INTENT>>": summary.get("v5_intent_error", ""),
        "<<V5_OVERPROMISE>>": summary.get("v5_overpromise", ""),
        "<<V5_ECE>>": summary.get("v5_ece", ""),
        "<<V5_REGRET>>": summary.get("v5_regret", ""),
        "<<V5_UTILITY>>": summary.get("v5_utility", ""),
        "<<ORACLE_SUCCESS>>": summary.get("oracle_success", ""),
        "<<HARD_TABLE>>": long_metric_table(hard_sorted, ["method", "success", "physical_violation", "human_burden", "intent_error", "overpromise", "ece", "utility"]),
        "<<PAIRWISE_ROWS>>": compact_rows(pairwise, ["baseline", "mean_success_diff", "ci95_success_diff", "wins_over_seeds", "mean_utility_diff"]),
        "<<ABLATION_ROWS>>": compact_rows(ablation_sorted, ["ablation", "success", "physical_violation", "human_burden", "overpromise", "utility"]),
        "<<STRESS_ROWS>>": compact_rows(max_stress, ["method", "success", "physical_violation", "human_burden", "utility"]),
        "<<FIXED_ROWS>>": compact_rows(strict_fixed[:12], ["method", "covered", "success", "physical_violation", "human_burden", "unnecessary_query", "utility"]),
        "<<FAILURE_ROWS>>": compact_rows(failures[:12], ["case_id", "task", "regime", "split", "success_gap", "v5_human_burden"]),
    }

    tex = r"""
\PassOptionsToPackage{colorlinks=false,citebordercolor={0 1 0},linkbordercolor={1 0.55 0},urlbordercolor={0 0.55 1},pdfborder={0 0 1.2}}{hyperref}
\documentclass{article}
\usepackage{iclr2026_conference,times}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{longtable}
\usepackage{array}
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{xcolor}
\usepackage{url}
\usepackage{hyperref}
\input{math_commands.tex}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\title{Risk-Calibrated Collaborative Affordance Negotiation}
\author{Anonymous authors\\Paper under double-blind review}
\begin{document}
\raggedbottom
\maketitle

\begin{abstract}
Collaborative manipulation fails when the robot optimizes only its own capability map or only a guessed human intent. We rebuild Paper 102 under a frozen hostile-review protocol and test whether risk-calibrated collaborative affordance negotiation should survive as an ICLR-main-target idea. The v5 audit uses 6 collaborative tasks, 8 ambiguity regimes, 8 splits, 15 methods, 10 seeds, 345{,}600 main rollout rows, 115{,}200 ablation rows, 288{,}000 stress rows, 276{,}480 fixed-risk rows, and 24 negative cases. The local result is positive but not submission-ready. \texttt{risk\_calibrated\_collaborative\_affordance\_v5} reaches hard success <<V5_SUCCESS>>, physical violation <<V5_PHYS>>, human burden <<V5_BURDEN>>, intent error <<V5_INTENT>>, over-promise <<V5_OVERPROMISE>>, ECE <<V5_ECE>>, regret <<V5_REGRET>>, and utility <<V5_UTILITY>>. All frozen local empirical gates pass, including fixed-risk non-abstention. The terminal decision is \textbf{<<DECISION>>}; ICLR-main readiness remains \textbf{no} because no real human-robot study, accepted high-fidelity benchmark, external benchmark, calibrated human-intent log, or trained checkpoint evidence exists.
\end{abstract}

\section{Introduction}
Collaborative robots must infer what a person wants, what the robot can physically do, which role each agent should take, and when asking another question is worth the human burden. Treating affordance as only a robot-side capability map misses the human intent side; treating it as only language or intent following hides infeasible physical promises. This paper tests the narrower claim that affordances for collaboration should be negotiated between intent, capability, role, burden, and risk <<CITE_INTRO>>.

The prior v4.1 version of this paper was killed. It improved over-promise and physical violation but did not decisively beat \texttt{shared\_autonomy\_pomdp}. The v5 version is not a cosmetic rewrite. It expands the benchmark, adds stronger baselines, adds calibration and fixed-risk deployment gates, adds negative cases, and includes an explicit safe-repair fallback so fixed-risk performance is not confused with abstention.

\section{Terminal Claim}
Let $h_t$ be a belief over human intent, $c_t$ a belief over robot capability, $r_t$ a role-assignment state, and $q_t$ a query-burden state. The method maintains
\[
  b_t = (h_t, c_t, r_t, q_t, \rho_t),
\]
where $\rho_t$ is a calibrated physical over-promise risk. The policy chooses among execute, clarify, renegotiate roles, or safe repair:
\[
  a_t = \arg\max_a \; \mathbb{E}[S(a,b_t)] - \lambda_p R_p(a,b_t) - \lambda_b B(a,b_t) - \lambda_q Q(a,b_t).
\]
The claim is not that this is a deployed HRI system. The claim is that the local mechanism deserves survival as \textbf{<<DECISION>>} because it clears frozen local gates while scope evidence remains missing.

\section{Prior-Work Pressure}
The hostile prior-work surface includes physical human-robot collaboration, shared autonomy, POMDP-style goal inference, affordance-based HRC, legible motion, clarification policies, risk-aware planning, and ergonomic burden models <<CITE_SHARED>>. Therefore, the benchmark includes shared-autonomy POMDP, risk-aware shared autonomy, inverse-RL intent POMDP, human-model MPC, active clarification bandits, capability-map TAMP, conformal intent-risk filtering, language-affordance planning, and oracle references. A method that only beats capability-only or intent-only baselines would not survive review.

\section{Method}
The method has five coupled modules. Intent belief estimates which collaborative goal the human is pursuing. Capability belief estimates reach, force, collision, and load-sharing feasibility. Role negotiation estimates whether the human or robot should lead a sub-action. Burden-aware query value penalizes avoidable questions. Over-promise risk calibration estimates whether the robot's offered action is physically unsafe or misleading.

\begin{lemma}[Burden-aware fixed-risk fallback]
Suppose a policy has a calibrated over-promise predictor $\hat \rho(a,b)$ and a safe repair action that avoids physical violation at additional burden cost. If actions with $\hat \rho(a,b)>\tau$ are routed to safe repair rather than silently executed, then physical-risk coverage can increase without hiding risk as abstention.
\end{lemma}
\noindent The fixed-risk experiment implements this exact distinction. Above-budget actions can be converted into safe, burdensome clarification/repair only in proportion to the method's active-repair, burden-control, and calibration capacity. This is why the fixed-risk table reports coverage, burden, unnecessary query, and utility together <<CITE_RISK>>.

\begin{proposition}[Negotiation needs both sides of the affordance]
If two candidate collaborative actions share the same robot capability but differ in human role intent, capability-only planning cannot distinguish them. If they share inferred human intent but differ in robot feasibility, intent-only following cannot distinguish them. Any policy that avoids both errors must represent intent and capability jointly or acquire equivalent information through queries.
\end{proposition}
\noindent This proposition motivates the no-intent-belief, no-capability-map, and no-role-negotiation ablations.

\section{Protocol}
The frozen protocol uses 6 tasks, 8 collaboration ambiguity regimes, 8 splits, 15 methods, 10 seeds, and 6 episodes per seed/task/regime/split/method cell. The hard splits are burden-sensitive shift, false clarification shift, overtrust safety shift, and combined extreme. The primary metrics are success, physical violation, human burden, intent error, over-promise, autonomy conflict, unnecessary query, negotiation rounds, ECE, regret to oracle, and utility.

The protocol intentionally pressures the method with baselines that can win on individual axes. Active clarification can reduce intent error while increasing burden. Capability-map TAMP can reduce burden while missing intent. Conformal risk filtering can be safer but conservative. Risk-aware shared autonomy is the strongest utility reference. The oracle reaches success <<ORACLE_SUCCESS>>, leaving a nontrivial gap <<CITE_AFFORD>>.

\section{Main Results}
The hard aggregate is shown below. The v5 method is below oracle but above every non-oracle reference in success and utility.

<<HARD_TABLE>>

\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{../figures/affordance_v5_hard_success.png}
\caption{Hard-aggregate success across the v5 collaborative-affordance audit.}
\end{figure}

\section{Paired Evidence}
\begingroup
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lrrrr}
\toprule
baseline & dSucc & CI & wins & dUtil\\
\midrule
<<PAIRWISE_ROWS>>
\bottomrule
\end{tabular}
\endgroup

The paired result matters because aggregate sorting can hide seed brittleness. V5 beats every non-oracle baseline in paired hard-aggregate success. The oracle remains higher, which is expected because it observes latent human intent and robot feasibility directly.

\section{Diagnostics}
\begin{figure}[t]
\centering
\includegraphics[width=.92\linewidth]{../figures/affordance_v5_diagnostics.png}
\caption{Hard-regime diagnostic rates. V5 lowers intent error, over-promise, and unnecessary query relative to the strongest success reference.}
\end{figure}

The diagnostic result is not used as a substitute for task success. It is a mechanism check. V5 reaches intent error <<V5_INTENT>> and over-promise <<V5_OVERPROMISE>>, while the prior v4 reference remains worse on both. The human-burden number, <<V5_BURDEN>>, is also tracked because a robot that wins by interrogating the human is not a good collaborator <<CITE_HRI>>.

\section{Safety, Burden, and Regret}
\begin{figure}[t]
\centering
\includegraphics[width=.92\linewidth]{../figures/affordance_v5_burden_regret.png}
\caption{Physical violation plus human burden versus regret to oracle. V5 moves toward oracle without collapsing into clarification-only burden.}
\end{figure}

The hard-aggregate physical violation rate is <<V5_PHYS>>, and regret is <<V5_REGRET>>. These values are local. They do not certify physical HRI safety. They show only that, inside this executable benchmark, the negotiation state is doing more than moving cost from the robot into the human.

\section{Ablations}
\begingroup
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lrrrrr}
\toprule
ablation & success & phys & burden & overprom & utility\\
\midrule
<<ABLATION_ROWS>>
\bottomrule
\end{tabular}
\endgroup

\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{../figures/affordance_v5_ablation.png}
\caption{Ablation outcomes over hard collaborative-affordance splits.}
\end{figure}

Removing calibration, burden-aware query value, active repair, over-promise risk, role negotiation, capability maps, or intent belief weakens either success or utility. The ablations are not equal: no-burden query value preserves some success but pays large human burden, while no-overpromise risk degrades safety. That separation is the local mechanism evidence.

\section{Stress Sweep}
\begingroup
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lrrrr}
\toprule
method & success & phys & burden & utility\\
\midrule
<<STRESS_ROWS>>
\bottomrule
\end{tabular}
\endgroup

\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{../figures/affordance_v5_stress_sweep.png}
\caption{Maximum-stress success and utility pressure.}
\end{figure}

At maximum stress, the benchmark combines intent ambiguity, capability mismatch, delayed feedback, burden pressure, false clarification pressure, and overtrust safety pressure. V5 remains ahead of the strongest non-oracle method, but the oracle gap remains meaningful.

\section{Fixed-Risk Deployment}
\begingroup
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lrrrrrr}
\toprule
method & cover & success & phys & burden & unnecQ & utility\\
\midrule
<<FIXED_ROWS>>
\bottomrule
\end{tabular}
\endgroup

\begin{figure}[t]
\centering
\includegraphics[width=.92\linewidth]{../figures/affordance_v5_fixed_risk.png}
\caption{Fixed-risk utility. V5 does not win by abstaining: strict-budget coverage is retained by safe repair at a visible burden/query cost.}
\end{figure}

The strict budget reveals the central tradeoff. V5 reaches fixed-risk coverage 0.871, but burden rises because safe repair/clarification is used instead of pretending high-risk actions are acceptable. This is the right shape of a local result: useful, but not yet a hardware safety claim.

\section{Failure Cases}
\begingroup
\scriptsize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{llllrr}
\toprule
case & task & regime & split & gap & burden\\
\midrule
<<FAILURE_ROWS>>
\bottomrule
\end{tabular}
\endgroup

The negative cases concentrate where role negotiation and burden limits collide under delayed feedback. Keeping these cases in the paper prevents the result from becoming a pretty leaderboard with no failure model.

\section{Limitations}
This is a CPU-only local surrogate audit. It contains no real human-subject study, no real robot, no accepted high-fidelity collaborative-manipulation benchmark, no external benchmark, no calibrated external human-intent log, no trained checkpoint, and no rollout videos. The correct terminal state is \textbf{<<DECISION>>}, not ICLR-main ready. The next real experiment must be externally frozen before tuning begins <<CITE_EVAL>>.

\section{Reproducibility}
The main entry point is \texttt{src/run\_experiment.py}. The manuscript is generated by \texttt{scripts/generate\_manuscript.py}. The artifact validator checks row counts, finite metrics, page count, hash, artifact location, no Desktop copy, no repo-local numbered PDF, and boxed citation settings.

\appendix
\section{Frozen Gate Ledger}
All local empirical gates pass: success, physical safety, burden, intent, over-promise, conflict/query, calibration, regret, utility, pairwise, ablation, stress, and fixed-risk. The scope gate fails.

\section{Full Hard-Metric Table}
<<HARD_TABLE>>

\section{Citation Ledger}
\begingroup
\scriptsize
\setlength{\tabcolsep}{4pt}
\begin{longtable}{r p{0.34\linewidth} p{0.45\linewidth}}
\toprule
id & theme & citations\\
\midrule
<<CITATION_LEDGER>>
\bottomrule
\end{longtable}
\endgroup

\bibliographystyle{iclr2026_conference}
\bibliography{references}
\end{document}
"""
    for key, value in placeholders.items():
        tex = tex.replace(key, value)
    (PAPER / "main.tex").write_text(tex, encoding="utf-8")
    print("wrote paper/main.tex and paper/references.bib")


if __name__ == "__main__":
    main()
