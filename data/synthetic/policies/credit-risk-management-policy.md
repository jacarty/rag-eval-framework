# Credit Risk Management Policy

---

## 1. Document Control

| Field | Detail |
|---|---|
| **Policy Title** | Credit Risk Management Policy |
| **Version** | 2.1 |
| **Effective Date** | 1 February 2025 |
| **Next Review Date** | 31 January 2026 |
| **Document Owner** | David Okonkwo, Chief Risk Officer |
| **Approving Body** | Board Risk Committee |

---

## 2. Purpose

This policy establishes Crest Bank's framework for identifying, measuring, managing, and mitigating credit risk across its lending portfolio. It sets minimum standards for creditworthiness assessment, affordability evaluation, credit scoring, arrears management, forbearance, and loan loss provisioning to ensure that Crest Bank lends responsibly and maintains financial resilience. The policy supports compliance with applicable FCA and PRA regulatory requirements and reflects Crest Bank's commitment to fair customer outcomes.

---

## 3. Scope

This policy applies to:

- **Products:** Personal loans, personal current accounts with overdraft facilities, and SME business current accounts with overdraft facilities.
- **Customer segments:** All retail (personal) borrowers and SME borrowers.
- **Teams:** Credit Risk, Customer Operations, Collections and Recoveries, Finance (Provisioning), Compliance, and any third-party credit decisioning or collections partners acting on Crest Bank's behalf.
- **Systems:** The automated credit decisioning engine, credit bureau integration layer, arrears management platform, and core banking system.

This policy does not cover treasury or counterparty credit risk, which is governed separately under the Treasury Risk Policy.

---

## 4. Regulatory Context

| Regulatory Source | Relevance to This Policy |
|---|---|
| **CONC 5.2** (Creditworthiness assessment) | Requires firms to conduct a reasonable creditworthiness assessment before entering into a regulated credit agreement, taking into account the potential for the commitment to adversely impact the customer's financial situation. |
| **CONC 5.3** (Conduct of business: creditworthiness) | Sets out the information firms must obtain and verify when assessing creditworthiness, including income, expenditure, and credit history. |
| **CONC 6.7** (Arrears, default and recovery) | Requires firms to treat customers in arrears fairly, to consider forbearance options, and to signpost free debt advice. |
| **CONC 7** (Arrears and default) | Sets out detailed conduct requirements for communicating with customers in financial difficulty and for the application of charges and interest during arrears. |
| **SYSC 6.1** (Compliance function) | Requires Crest Bank to establish and maintain effective policies and procedures to manage material risks, including credit risk. |
| **SYSC 7.1** (Risk management) | Requires the firm to have robust strategies, processes, and mechanisms to identify, measure, manage, and monitor credit risk on an ongoing basis. |
| **PRIN 6** (Customers' interests) | Requires Crest Bank to pay due regard to the interests of its customers and treat them fairly throughout the credit lifecycle. |
| **PRIN 12** (Consumer Duty — FCA PS22/9) | Requires Crest Bank to act to deliver good outcomes for retail customers, including ensuring credit products are appropriate and affordable. |
| **PRA Rulebook: CRR Firms — Credit Risk** | Sets out capital requirements and internal ratings-based standards applicable to Crest Bank's credit exposures. |
| **IFRS 9** (as implemented via PRA supervisory statements) | Governs expected credit loss (ECL) provisioning methodology, including staging criteria and forward-looking adjustments. |

---

## 5. Policy Statement

5.1 Crest Bank will only extend credit where a reasonable and documented assessment concludes that the customer is likely to be able to meet repayments in a sustainable manner, without undue financial hardship.

5.2 Creditworthiness assessments will be based on verified information about the customer's income, committed expenditure, existing credit obligations, and credit history, drawing on data from at least one FCA-registered credit reference agency (CRA).

5.3 Crest Bank's credit scoring models will be subject to documented governance, regular validation, and bias testing to ensure they produce fair, accurate, and consistent outcomes across all customer groups.

5.4 Crest Bank will not apply credit limits, loan amounts, or pricing that it has reasonable grounds to believe will cause the customer financial harm, and will decline applications where affordability cannot be demonstrated.

5.5 Customers who fall into arrears will be treated with forbearance and due consideration. Crest Bank will proactively identify customers in financial difficulty and offer appropriate support, including referral to free debt advice services, before escalating to formal collections or recovery action.

5.6 Forbearance arrangements will be offered in good faith and tailored to the individual customer's circumstances. Crest Bank will not apply charges or fees that make a customer's position materially worse during an agreed forbearance period.

5.7 Loan loss provisions will be calculated in accordance with IFRS 9 expected credit loss principles, with staging and forward-looking adjustments reviewed at least quarterly by the Finance function in conjunction with the Credit Risk team.

5.8 Credit risk appetite limits, concentration thresholds, and portfolio-level triggers will be set by the Board Risk Committee and monitored monthly by the Executive Risk Committee.

---

## 6. Roles and Responsibilities

| Role | Responsibilities Under This Policy |
|---|---|
| **David Okonkwo, CRO** | Overall ownership of the credit risk framework; approval of credit risk appetite metrics; escalation to Board Risk Committee; oversight of model governance. |
| **Rachel Whitfield, CCO** | Ensuring CONC and Consumer Duty compliance in credit processes; reviewing customer-facing communications in arrears and collections; reporting to Compliance Oversight Committee. |
| **James Patel, MLRO** | Identifying and reporting any credit applications or arrears patterns that give rise to suspicion of fraud or financial crime. |
| **Priya Sharma, Head of Customer Operations** | Operational delivery of creditworthiness assessments, arrears management, and forbearance processes; ensuring Collections team adherence to CONC 6.7 and CONC 7. |
| **Head of Credit Risk (reporting to CRO)** | Day-to-day management of credit scoring models, policy rules, and portfolio monitoring; production of monthly credit risk MI. |
| **Finance (Provisioning team)** | Calculation and reporting of IFRS 9 expected credit loss provisions; liaison with external auditors; quarterly staging review. |
| **Tom Hargreaves, CTO** | Ensuring the integrity, availability, and auditability of credit decisioning systems and arrears management platforms. |
| **Michael Byrne, Chair, Board Risk Committee** | Approving credit risk appetite; receiving quarterly credit risk reports; challenging the adequacy of provisioning and arrears management. |

---

## 7. Procedures

### 7.1 Creditworthiness and Affordability Assessment

7.1.1 Before approving any personal loan or overdraft facility, Crest Bank's credit decisioning engine will perform an automated creditworthiness assessment in accordance with CONC 5.2. This assessment will incorporate:

- A hard or soft credit search (as appropriate to the product stage) from at least one FCA-registered CRA, capturing credit history, existing commitments, and any adverse markers;
- Verified or declared income data, cross-referenced against open banking transaction data where the customer has consented;
- Committed expenditure, derived from transaction analysis or declared outgoings, including rent or mortgage payments, existing loan repayments, and essential household costs;
- A residual income calculation to confirm that the proposed repayment is affordable after essential expenditure.

7.1.2 In accordance with CONC 5.3, Crest Bank will not rely solely on declared income for loans above £5,000. For such applications, income must be verified via open banking data, payslip upload, or HMRC-linked confirmation.

7.1.3 The affordability model will apply a stress test of at least 2 percentage points above the offered rate to assess resilience to interest rate changes for variable-rate products.

7.1.4 Applications that fail the affordability threshold will be declined automatically. The customer will receive a clear decline notification, including the primary reason for decline and signposting to free debt advice where appropriate, consistent with PRIN 12 Consumer Duty obligations.

### 7.2 Credit Scoring Methodology and Model Governance

7.2.1 Crest Bank operates a scorecard-based credit decisioning model, supplemented by policy rules and manual referral triggers. The model assigns each applicant a risk score used to determine accept/decline decisions, credit limits, and risk-based pricing.

7.2.2 The credit scoring model is subject to formal model governance under Crest Bank's Model Risk Policy. This includes:

- An initial validation report before deployment, signed off by an independent model validator;
- Annual full model validation, assessing discriminatory power (Gini coefficient), stability (Population Stability Index), and calibration;
- Quarterly performance monitoring reports reviewed by the Head of Credit Risk;
- Bias and fairness testing at least annually, covering protected characteristics under the Equality Act 2010.

7.2.3 Any material change to the scoring model or policy rules requires approval from the Executive Risk Committee before deployment.

7.2.4 Model performance metrics and validation outcomes will be reported to the Board Risk Committee at least annually.

### 7.3 Arrears Management

7.3.1 An account is classified as in arrears when a scheduled payment is missed in full or in part. Crest Bank's arrears management platform will flag accounts automatically on the first missed payment.

7.3.2 The Collections team, operating under the oversight of Priya Sharma, will contact customers in arrears in accordance with the following minimum contact schedule:

- **Day 1–7 (early arrears):** Automated notification via app push notification and email, prompting self-cure or contact with Crest Bank.
- **Day 8–30:** Outbound contact attempt by a trained Collections agent, with a focus on understanding the customer's circumstances and offering appropriate support.
- **Day 31+:** Formal arrears notice issued, setting out the outstanding amount, any charges applied, and the customer's right to seek free debt advice.

7.3.3 In accordance with CONC 7, Crest Bank will not contact customers in arrears at unreasonable times, will not apply pressure tactics, and will ensure all communications are clear, fair, and not misleading.

7.3.4 Customers who indicate financial difficulty at any stage will be immediately referred to the Financial Difficulty pathway (see 7.4 below).

### 7.4 Forbearance

7.4.1 In accordance with CONC 6.7, Crest Bank will consider forbearance for any customer who demonstrates or indicates that they are experiencing financial difficulty. Forbearance options include, but are not limited to:

- Temporary payment deferral (up to three months);
- Reduced payment arrangement;
- Interest freeze or reduction;
- Term extension to reduce monthly repayment;
- Partial or full debt write-off in exceptional circumstances.

7.4.2 The Collections agent will conduct a financial assessment with the customer to identify the most appropriate forbearance option. Arrangements will be documented in the arrears management platform and confirmed to the customer in writing within two business days.

7.4.3 During an agreed forbearance period, Crest Bank will not apply default charges or fees that worsen the customer's position, consistent with CONC 6.7 and PRIN 6.

7.4.4 All customers in financial difficulty will be signposted to free, independent debt advice services (including StepChange, National Debtline, and Citizens Advice) at the point of first contact and in all written communications.

7.4.5 Forbearance arrangements will be reviewed at the end of each agreed period. Where a customer remains in difficulty, the Collections team will reassess and offer a revised arrangement rather than defaulting immediately to formal recovery action.

### 7.5 Provisioning

7.5.1 Crest Bank calculates loan loss provisions in accordance with IFRS 9 expected credit loss (ECL) methodology. Exposures are staged as follows:

- **Stage 1:** Performing — 12-month ECL applied.
- **Stage 2:** Significant increase in credit risk (SICR) since origination — lifetime ECL applied.
- **Stage 3:** Credit-impaired (including accounts 90+ days past due or subject to forbearance indicating unlikeliness to pay) — lifetime ECL applied on an individual or collective basis.

7.5.2 SICR triggers include: 30+ days past due, significant deterioration in credit score, entry into forbearance, or macroeconomic indicators identified as relevant by the Finance and Credit Risk teams.

7.5.3 The Provisioning team will produce an ECL calculation quarterly, incorporating forward-looking macroeconomic scenarios (base, upside, and downside) probability-weighted in accordance with PRA supervisory guidance.

7.5.4 Provisioning outputs will be reviewed by the CRO and CFO before submission to the Board Risk Committee and inclusion in financial statements.

---

## 8. Monitoring, Reporting and Escalation

8.1 The Head of Credit Risk will produce a **monthly Credit Risk MI pack** for the Executive Risk Committee, covering: new lending volumes and approval rates, portfolio arrears rates (by product and vintage), forbearance stock and flows, and model performance indicators.

8.2 The Provisioning team will present a **quarterly ECL report** to the Board Risk Committee, including staging movements, macroeconomic scenario assumptions, and any management overlays applied.

8.3 The Compliance Oversight Committee will receive a **quarterly CONC compliance report** from Rachel Whitfield, covering: complaints related to credit decisioning or collections, outcomes testing results, and any regulatory correspondence.

8.4 **Escalation triggers** requiring immediate notification to the CRO and, where material, to the Board Risk Committee include:

- Portfolio arrears rate exceeding the risk appetite threshold set by the Board;
- A model validation failure or material model error identified in production;
- A regulatory finding or FCA supervisory contact relating to creditworthiness or collections conduct;
- A single forbearance cohort exceeding 5% of the active loan book by value.

---

## 9. Training

9.1 All staff in Credit Risk, Collections, and Customer Operations must complete Crest Bank's **Credit Risk and Responsible Lending** training module upon joining and annually thereafter.

9.2 Collections agents must additionally complete a **CONC Arrears and Forbearance** training module, covering regulatory obligations under CONC 6.7 and CONC 7, before handling live customer accounts.

9.3 Training completion is tracked via Crest Bank's learning management system (LMS). Completion rates are reported to the Compliance Oversight Committee quarterly. Any team member not completing mandatory training within the required window will be escalated to their line manager and the CCO.

9.4 Material changes to this policy will trigger a targeted refresher communication to all in-scope staff within 20 business days of the effective date.

---

## 10. Review Cycle

10.1 This policy will be reviewed annually by the CRO, with approval by the Board Risk Committee, no later than 31 January each year.

10.2 An ad-hoc review will be triggered by any of the following:

- A material change to FCA or PRA rules affecting consumer credit, creditworthiness assessment, or provisioning;
- A significant change to Crest Bank's credit product range or target market;
- A material model change or validation failure;
- A regulatory finding or enforcement action relating to credit risk management;
- A significant deterioration in portfolio quality beyond risk appetite thresholds.

10.3 Interim amendments of a minor or clarificatory nature may be approved by the CRO, with ratification at the next Board Risk Committee meeting.

---

## 11. Related Documents

- Responsible Lending Policy
- Model Risk Policy
- Collections and Recoveries Procedure
- Financial Difficulty and Vulnerability Policy
- Treasury Risk Policy
- Consumer Duty Implementation Policy
- Anti-Fraud Policy
- Capital Adequacy and ICAAP Policy
- Data Quality and Integrity Policy

---

*This is a synthetic policy document created for evaluation purposes. Crest Bank Ltd is a fictional entity.*
