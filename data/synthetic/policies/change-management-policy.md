# Change Management Policy

## 1. Document Control

| Field | Detail |
|---|---|
| **Policy Title** | Change Management Policy |
| **Version** | 1.3 |
| **Effective Date** | 1 February 2025 |
| **Next Review Date** | 31 January 2026 |
| **Document Owner** | Tom Hargreaves, Chief Technology Officer |
| **Approving Body** | Board Risk Committee |

---

## 2. Purpose

This policy establishes Crest Bank's framework for managing changes to its technology systems, infrastructure, and customer-facing products in a controlled, auditable, and risk-proportionate manner. Given that all customer interaction occurs exclusively through the Crest Bank mobile application and API layer, uncontrolled change poses a direct and immediate risk to service availability, customer outcomes, and regulatory compliance. This policy ensures that every change is assessed, tested, approved, and reviewed in a manner consistent with Crest Bank's obligations as a dual-regulated digital bank.

---

## 3. Scope

This policy applies to:

- **Teams:** Technology Engineering, Platform Operations, Product, Compliance, Risk, Customer Operations, and any third-party suppliers or contractors making changes to Crest Bank systems under a managed service or development agreement.
- **Systems:** All production systems, including the mobile application (iOS and Android), public-facing APIs, core banking platform, data pipelines, cloud infrastructure (including all AWS environments), identity and authentication services, and internal tooling that interfaces with customer data or regulated processes.
- **Products:** Personal current accounts, instant-access savings, fixed-term savings, personal loans, and SME business current accounts.
- **Customer Segments:** All retail and SME customers.
- **Exclusions:** Changes confined entirely to non-production environments with no pathway to production within the same change window are out of scope, but must still be logged in the change management system.

---

## 4. Regulatory Context

| Regulatory Source | Relevance to This Policy |
|---|---|
| **SYSC 8.1** | Requires Crest Bank to ensure that outsourced functions and third-party technology arrangements are subject to adequate oversight and control, including change processes. |
| **SYSC 13.7** | Sets out requirements for managing operational risk in IT systems, including the need for documented change and release management processes. |
| **PRIN 2 (Principle 2)** | Requires Crest Bank to conduct its business with due skill, care and diligence; uncontrolled change that degrades service or creates customer harm is a direct breach of this principle. |
| **PRIN 6 (Principle 6)** | Requires Crest Bank to pay due regard to the interests of its customers and treat them fairly; changes that introduce product defects or restrict access to funds without adequate controls risk breaching this principle. |
| **BCOBS 5.1** | Requires Crest Bank to provide banking services that meet the reasonable expectations of retail banking customers, including reliable access to accounts and funds. |
| **COBS 2.1.1R** | Requires Crest Bank to act honestly, fairly and professionally in the best interests of its customers; this extends to ensuring that changes to customer-facing systems do not introduce misleading information or degraded functionality. |
| **PRA Supervisory Statement SS2/21** | Sets out PRA expectations for operational resilience, including the requirement that important business services remain within impact tolerances during and after system changes. |

---

## 5. Policy Statement

5.1 Crest Bank will classify every proposed change according to a defined risk taxonomy before any work is approved for production deployment.

5.2 Every change with a regulatory, customer-data, or product-behaviour impact will undergo a formal regulatory impact analysis before approval, conducted jointly by the Technology and Compliance functions.

5.3 No change will be deployed to production without passing all mandatory testing gates appropriate to its risk classification.

5.4 Every change will have a documented and tested rollback procedure approved prior to deployment; deployment will not proceed where a viable rollback cannot be demonstrated.

5.5 Changes to customer-facing features, pricing logic, interest calculations, or credit decisioning algorithms will require sign-off from the relevant product owner and the Chief Compliance Officer before deployment.

5.6 Crest Bank will maintain a complete, auditable record of all changes, including the rationale, approvals, test evidence, deployment outcome, and post-implementation review, for a minimum of six years.

5.7 Emergency changes, while subject to an expedited process, remain subject to risk assessment, approval, and retrospective review; no change is exempt from governance.

5.8 Crest Bank will treat a failed or partially deployed change as an operational incident and invoke the Incident Management Policy immediately upon detection.

---

## 6. Roles and Responsibilities

| Role | Responsibilities Under This Policy |
|---|---|
| **Tom Hargreaves, CTO** | Policy owner; chairs the Change Approval Board (CAB); accountable for the integrity of the change management framework; approves High and Critical risk changes. |
| **David Okonkwo, CRO** | Reviews and approves the risk classification of High and Critical changes; escalates systemic change risk to the Executive Risk Committee. |
| **Rachel Whitfield, CCO** | Conducts or delegates regulatory impact analysis for all Standard and above changes; provides mandatory sign-off for changes affecting regulated product behaviour. |
| **Fatima Al-Rashid, DPO** | Reviews all changes with personal data implications under the Data Protection Impact Assessment process; provides sign-off where data flows are materially altered. |
| **James Patel, MLRO** | Reviews changes affecting transaction monitoring, sanctions screening, or customer due diligence systems; provides sign-off before deployment of such changes. |
| **Priya Sharma, Head of Customer Operations** | Reviews changes with anticipated customer-facing impact; ensures Customer Operations is briefed and ready before deployment; raises customer outcome concerns to the CCO. |
| **Engineering Leads** | Responsible for completing change request documentation, test evidence, and rollback plans; accountable for technical accuracy of submissions to the CAB. |
| **Third-Party Suppliers** | Must comply with this policy and Crest Bank's Supplier Change Management Schedule when making changes to systems within scope; subject to audit rights. |

---

## 7. Procedures

### 7.1 Change Classification

7.1.1 All proposed changes must be logged in Crest Bank's change management system (currently ServiceNow) before any development work targeting production begins.

7.1.2 The submitting Engineering Lead will assign an initial risk classification using the following taxonomy:

| Classification | Criteria |
|---|---|
| **Standard** | Low-risk, pre-approved change type with a well-understood and tested process (e.g. routine dependency version updates within a defined safe range). |
| **Normal** | Any change not meeting Standard criteria; requires full CAB review. |
| **High** | Changes affecting core banking logic, credit decisioning, interest calculations, authentication, API contracts, or any system processing customer funds. |
| **Critical** | Changes required to remediate a live incident, address an imminent regulatory deadline, or prevent material customer harm; subject to expedited process under 7.6. |

7.1.3 The CRO may escalate the classification of any change upward at any point in the process.

### 7.2 Regulatory Impact Analysis

7.2.1 For all Normal, High, and Critical changes, the submitting team will complete the Regulatory Impact Assessment (RIA) template, identifying whether the change affects: regulated product terms or disclosures; customer data processing or consent; transaction monitoring or financial crime controls; access to funds or account functionality; or any system subject to a live regulatory commitment or remediation plan.

7.2.2 The CCO will review the completed RIA within three business days for Normal changes and within four hours for Critical changes. In accordance with COBS 2.1.1R and PRIN 6, the CCO will reject any change where the regulatory impact has not been adequately assessed or mitigated.

7.2.3 Where the RIA identifies a material change to personal data processing, the DPO will conduct a Data Protection Impact Assessment in accordance with Crest Bank's Data Protection Policy before approval proceeds.

7.2.4 Where the RIA identifies an impact on financial crime controls, the MLRO will review and provide written sign-off before the change proceeds to testing.

### 7.3 Testing Gates

7.3.1 All changes must pass the testing gates applicable to their classification before submission to the CAB for deployment approval:

| Gate | Standard | Normal | High | Critical |
|---|---|---|---|---|
| Unit and integration tests (automated) | ✓ | ✓ | ✓ | ✓ |
| Regression test suite (automated) | — | ✓ | ✓ | ✓ |
| Performance and load testing | — | — | ✓ | ✓ (abbreviated) |
| Security and penetration testing | — | — | ✓ | Where feasible |
| User acceptance testing (UAT) | — | ✓ | ✓ | — |
| Compliance functional review | — | ✓ | ✓ | ✓ |

7.3.2 Test evidence must be attached to the change record in ServiceNow. The CAB will not approve a change where mandatory test gates have not been passed and evidenced.

7.3.3 Where a High change affects the mobile application or public API, Engineering Leads must include API contract validation results and, where applicable, evidence of backward compatibility or a versioning strategy.

### 7.4 Change Approval Gates

7.4.1 The Change Approval Board (CAB) meets weekly and is chaired by the CTO. Membership includes representatives from Engineering, Platform Operations, Product, Compliance, and Risk.

7.4.2 Approval authority is as follows:

- **Standard changes:** Pre-approved; Engineering Lead confirms compliance with the Standard change checklist.
- **Normal changes:** CAB approval required.
- **High changes:** CAB approval plus written sign-off from the CTO and CCO.
- **Critical changes:** Expedited approval under 7.6; retrospective CAB review within five business days.

7.4.3 The CAB will confirm a deployment window for each approved change. Deployments to production must occur within the approved window; any deviation requires re-approval.

### 7.5 Rollback Procedures

7.5.1 Every Normal, High, and Critical change must include a documented rollback plan as a mandatory component of the change record. The rollback plan must specify: the trigger conditions under which rollback will be initiated; the precise steps to revert the production environment; the individual responsible for executing the rollback; and the estimated time to restore the previous state.

7.5.2 For High changes, the rollback plan must be tested in a staging environment that mirrors production, and test evidence must be attached to the change record.

7.5.3 If a deployment is not confirmed as stable within the post-deployment observation window defined in the change record (minimum 30 minutes for Normal; minimum two hours for High), the responsible Engineering Lead will initiate rollback and raise an incident in accordance with the Incident Management Policy.

7.5.4 Given that all customer access to Crest Bank services is via the mobile application and API, any degradation in API response times exceeding defined SLA thresholds, or any error rate above 0.5% on critical customer journeys (account access, payments, savings withdrawals), will automatically trigger a rollback review by the on-call Platform Operations engineer.

### 7.6 Emergency and Critical Changes

7.6.1 Where a change is required urgently to remediate a live incident or meet an imminent regulatory obligation, the CTO may invoke the Critical change process.

7.6.2 Critical changes require verbal approval from the CTO and CRO (or their nominated deputies) before deployment, with written confirmation logged in ServiceNow within one hour of deployment.

7.6.3 The CCO must be notified of all Critical changes at the point of deployment. Where the change affects a regulated system, the CCO will assess whether regulatory notification is required in accordance with SYSC 13.7.

7.6.4 A full retrospective review of every Critical change, including root cause analysis and assessment of whether the emergency process was appropriately invoked, must be completed and submitted to the Executive Risk Committee within ten business days.

### 7.7 Post-Implementation Review

7.7.1 All High and Critical changes require a formal Post-Implementation Review (PIR) completed within ten business days of deployment.

7.7.2 The PIR must assess: whether the change achieved its intended outcome; whether any unintended customer, system, or compliance impacts occurred; whether the rollback plan was adequate; and whether any process improvements are required.

7.7.3 PIR outcomes for High and Critical changes will be reported to the Executive Risk Committee monthly as part of the Technology Risk Report.

7.7.4 Where a PIR identifies a customer harm or a potential regulatory breach, the CCO will assess whether a Significant Harm Report or regulatory notification is required and will escalate to the Board Risk Committee if material.

---

## 8. Monitoring, Reporting and Escalation

8.1 The Platform Operations team will monitor all production deployments in real time using automated observability tooling (application performance monitoring, error rate dashboards, and synthetic transaction testing against critical API endpoints).

8.2 The CTO will produce a monthly Change Management Report for the Executive Risk Committee covering: total changes by classification; deployment success and failure rates; rollback events; Critical changes invoked; overdue PIRs; and any open change-related incidents.

8.3 The CCO will include a summary of regulatory-impact changes and any compliance concerns arising from the change process in the monthly Compliance Oversight Committee report.

8.4 The Board Risk Committee will receive a quarterly summary of change management performance, including trend analysis of High and Critical changes, as part of the Technology and Operational Risk section of the Board Risk Report.

8.5 **Escalation path:** Engineering Lead → CTO → CRO → Executive Risk Committee → Board Risk Committee. Where a change event constitutes or may constitute a regulatory breach, the CCO will escalate directly to the Board Risk Committee and assess notification obligations to the FCA and/or PRA.

---

## 9. Training

9.1 All staff with a role in the change management process (Engineering, Platform Operations, Product, Compliance, Risk) must complete Crest Bank's Change Management Awareness training upon joining and annually thereafter.

9.2 Engineering Leads and CAB members must complete an advanced Change Management and Operational Risk module annually, covering risk classification, regulatory impact assessment, and rollback procedures.

9.3 Training completion is tracked via Crest Bank's Learning Management System (LMS). The CCO will review completion rates quarterly; any team with completion below 90% will be escalated to the relevant Head of Function.

9.4 Ad-hoc training will be triggered following any Critical change event, significant rollback, or material PIR finding, targeted at the teams involved.

---

## 10. Review Cycle

10.1 This policy will be reviewed annually by the CTO in conjunction with the CCO, with the revised version submitted to the Board Risk Committee for approval.

10.2 An ad-hoc review will be triggered by any of the following: a material change to Crest Bank's technology architecture or cloud provider; a Critical change event resulting in customer harm or regulatory breach; new or amended FCA/PRA rules or guidance materially affecting operational resilience or change management obligations; a recommendation from an internal audit, external audit, or regulatory review; or a significant increase in change volume or complexity arising from product expansion.

10.3 Minor amendments (typographical corrections, updated role titles, non-substantive process clarifications) may be approved by the CTO without full Board Risk Committee review, provided the CCO confirms the amendment is non-substantive. All amendments must be versioned and logged.

---

## 11. Related Documents

- Incident Management Policy
- Operational Resilience Policy
- Technology Risk Policy
- Third-Party and Outsourcing Management Policy
- Data Protection Policy
- Business Continuity and Disaster Recovery Policy
- Information Security Policy
- Product Governance Policy
- Financial Crime Controls Policy
