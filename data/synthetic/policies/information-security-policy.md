# Information Security Policy

---

## 1. Document Control

| Field | Detail |
|---|---|
| **Policy Title** | Information Security Policy |
| **Version** | 2.1 |
| **Effective Date** | 1 February 2025 |
| **Next Review Date** | 31 January 2026 |
| **Document Owner** | Tom Hargreaves, Chief Technology Officer |
| **Approving Body** | Board Risk Committee |

---

## 2. Purpose

This policy establishes Crest Bank's framework for protecting the confidentiality, integrity, and availability of its information assets, technology systems, and customer data. It sets out the minimum security standards that all staff, contractors, and third parties must observe when accessing or processing Crest Bank's information. The policy ensures that Crest Bank's information security arrangements remain proportionate to the risks inherent in operating a digital-only banking platform serving approximately 862,000 customers.

---

## 3. Scope

This policy applies to:

- **Personnel:** All Crest Bank employees (permanent and fixed-term), contractors, consultants, and third-party suppliers who access Crest Bank systems or data.
- **Systems:** All production, development, and test environments, including cloud-hosted infrastructure, internal applications, customer-facing platforms, APIs, and end-user devices (corporate-issued and personal devices used under Crest Bank's BYOD provisions).
- **Data:** All information assets owned or processed by Crest Bank, including personal data relating to retail and SME customers, financial transaction data, and internal business data.
- **Products:** Personal current accounts, instant-access and fixed-term savings accounts, personal loans, and SME business current accounts.

This policy does not supersede Crest Bank's Data Protection Policy, which governs obligations under UK GDPR; however, the two policies must be read together.

---

## 4. Regulatory Context

| Regulatory Source | Relevance to This Policy |
|---|---|
| **SYSC 6.1** (Compliance, internal audit and financial crime) | Requires Crest Bank to establish, implement, and maintain adequate policies and procedures to manage operational risk, including information security risk. |
| **SYSC 13** (Operational risk: systems and controls for insurers — applied by analogy under SYSC 1 Annex 1) | Sets out requirements for managing operational risk arising from systems failures, inadequate processes, and external events, including cyber threats. |
| **SYSC 8** (Outsourcing) | Requires that outsourcing arrangements, including cloud service providers, do not impair Crest Bank's ability to manage operational and security risk or meet its regulatory obligations. |
| **PRIN 2** (Skill, care and diligence) | Requires Crest Bank to conduct its business with due skill, care, and diligence, which extends to protecting customer assets and data from security threats. |
| **PRIN 11** (Relations with regulators) | Requires Crest Bank to deal with the FCA and PRA in an open and cooperative way, including prompt notification of material security incidents. |
| **COBS 2.1.1R** (Acting honestly, fairly and professionally) | Underpins the obligation to maintain systems that protect customers' interests, including the security of their accounts and personal data. |
| **PRA Supervisory Statement SS2/21** (Outsourcing and third-party risk management) | Sets PRA expectations for managing technology and security risk in third-party and cloud arrangements. |
| **FCA PS21/3 / SYSC 15A** (Operational resilience) | Requires Crest Bank to identify important business services, set impact tolerances, and ensure information security controls support the ability to remain within those tolerances. |

---

## 5. Policy Statement

Crest Bank is committed to maintaining a robust information security posture that protects its customers, staff, and business operations. The following principles govern Crest Bank's approach:

1. **Risk-based security:** Crest Bank will identify, assess, and treat information security risks in proportion to their likelihood and potential impact, prioritising controls that protect customer data and critical banking services.
2. **Least privilege access:** Access to Crest Bank systems and data will be granted on the basis of least privilege — users will receive only the permissions necessary to perform their defined role, and no more.
3. **Defence in depth:** Crest Bank will deploy layered security controls across its technology estate, so that no single control failure results in a material breach of confidentiality, integrity, or availability.
4. **Data classification:** All information assets will be classified according to Crest Bank's data classification scheme, and handled in accordance with the controls applicable to that classification level.
5. **Encryption by default:** Crest Bank will encrypt sensitive data at rest and in transit using industry-standard algorithms, ensuring that customer and business data cannot be read by unauthorised parties.
6. **Prompt incident response:** Crest Bank will detect, contain, and recover from information security incidents in a timely manner, and will notify the FCA, PRA, and affected customers where required.
7. **Continuous assurance:** Crest Bank will test the effectiveness of its security controls through regular penetration testing, vulnerability assessments, and independent audit, and will remediate identified weaknesses within defined timeframes.
8. **Security culture:** Crest Bank will ensure that all personnel understand their security responsibilities through mandatory training and ongoing awareness activity.

---

## 6. Roles and Responsibilities

| Role | Responsibilities Under This Policy |
|---|---|
| **Tom Hargreaves, CTO** | Policy owner; accountable for the design and maintenance of Crest Bank's technical security controls; approves encryption standards and security architecture decisions; chairs the Information Security Working Group. |
| **Rachel Whitfield, CCO** | Ensures this policy remains aligned with FCA/PRA regulatory requirements; oversees compliance monitoring; escalates material security compliance failures to the Board Risk Committee. |
| **David Okonkwo, CRO** | Owns the information security risk appetite; ensures security risks are reflected in the Enterprise Risk Register; chairs the Executive Risk Committee review of security risk. |
| **Fatima Al-Rashid, DPO** | Ensures information security controls are consistent with UK GDPR obligations; leads the data breach notification process to the ICO where personal data is involved. |
| **James Patel, MLRO** | Assesses whether security incidents have financial crime implications; ensures security controls support AML transaction monitoring system integrity. |
| **Priya Sharma, Head of Customer Operations** | Ensures customer-facing operational teams comply with access control and data handling procedures; manages security awareness for operational staff. |
| **All Staff** | Comply with this policy and all related procedures; complete mandatory security training; report suspected security incidents to the Information Security team without delay. |
| **Third-Party Suppliers** | Comply with Crest Bank's Supplier Security Requirements (Schedule A of the standard supplier contract); notify Crest Bank of any security incident affecting Crest Bank data within 24 hours of discovery. |

---

## 7. Procedures

### 7.1 Data Classification

7.1.1 All information assets must be assigned one of the following classification levels at the point of creation or receipt:

| Classification | Description | Examples |
|---|---|---|
| **Restricted** | Highest sensitivity; unauthorised disclosure would cause serious harm | Customer financial data, authentication credentials, cryptographic keys |
| **Confidential** | Sensitive business or personal data; disclosure would cause material harm | Internal financial reports, staff personal data, regulatory correspondence |
| **Internal** | Non-public information with limited sensitivity | Internal policies, project documentation, meeting minutes |
| **Public** | Information approved for external publication | Marketing materials, published product terms |

7.1.2 The information asset owner (typically the relevant Head of Department) is responsible for assigning and maintaining the correct classification. The CTO will publish and maintain a Data Classification Standard that provides worked examples for common asset types.

7.1.3 Restricted and Confidential data must not be stored on unmanaged personal devices or transmitted via personal email accounts.

### 7.2 Access Controls

7.2.1 In accordance with SYSC 6.1, Crest Bank will operate a formal access management process. All access to production systems must be requested via the IT Service Management platform, approved by the relevant system owner, and provisioned by the Information Security team.

7.2.2 Access rights will be reviewed in full every six months for all production systems. Privileged access (administrator-level accounts) will be reviewed quarterly. The Information Security team will produce a report of each review for the CTO.

7.2.3 Access rights for any individual whose employment or engagement with Crest Bank ends must be revoked on the date of departure, or earlier if directed by HR or the CCO. The People team will notify the Information Security team no later than the working day before a leaver's last day.

7.2.4 Multi-factor authentication (MFA) is mandatory for all access to Crest Bank production systems, remote access connections, and any system processing Restricted or Confidential data.

7.2.5 Shared or generic accounts are prohibited on production systems. All access must be attributable to a named individual.

### 7.3 Encryption Standards

7.3.1 Crest Bank will encrypt all Restricted and Confidential data at rest using AES-256 or an equivalent algorithm approved by the Information Security team.

7.3.2 All data in transit across public or untrusted networks must be encrypted using TLS 1.2 or higher. TLS 1.0 and 1.1 are prohibited. The CTO will maintain an approved cipher suite list, reviewed annually.

7.3.3 Cryptographic keys must be managed in accordance with Crest Bank's Key Management Standard. Keys must be rotated at least annually and immediately upon suspected compromise. Keys must not be stored in application source code or version control repositories.

7.3.4 The use of end-to-end encryption for customer communications will be assessed on a product-by-product basis by the Product Governance Committee, with a recommendation from the CTO.

### 7.4 Security Incident Response

7.4.1 Any member of staff who suspects or identifies a security incident must report it to the Information Security team immediately via the designated security incident reporting channel (available on the Crest Bank intranet). Staff must not attempt to investigate or remediate incidents independently.

7.4.2 The Information Security team will triage all reported incidents within two hours of receipt and assign a severity rating (P1–P4) in accordance with the Incident Classification Matrix (Appendix A).

7.4.3 P1 (Critical) and P2 (High) incidents will trigger immediate escalation to the CTO, CRO, and CCO. The CTO will convene an incident response team within four hours of a P1 classification.

7.4.4 In accordance with SYSC 15A and PRIN 11, the CCO will assess whether a P1 or P2 incident requires notification to the FCA and/or PRA. Where notification is required, the CCO will submit an initial notification within the timeframe specified by the relevant regulator and no later than 72 hours after the incident is identified.

7.4.5 Where a security incident involves a personal data breach, Fatima Al-Rashid (DPO) will lead the assessment of ICO notification obligations under UK GDPR Article 33, in parallel with the regulatory notification process described in 7.4.4.

7.4.6 A post-incident review will be completed for all P1 and P2 incidents within ten working days of resolution. The CTO will present findings and remediation actions to the Executive Risk Committee at its next scheduled meeting.

### 7.5 Penetration Testing and Vulnerability Management

7.5.1 Crest Bank will commission an independent penetration test of its external-facing infrastructure and applications at least annually, conducted by a CREST-accredited provider. The scope will be agreed by the CTO and CRO and will include customer-facing platforms and APIs.

7.5.2 Internal penetration tests and red team exercises will be conducted at least every 18 months, or following any material change to Crest Bank's technology architecture.

7.5.3 All systems will be subject to automated vulnerability scanning at least monthly. Critical and High vulnerabilities (as rated by CVSS) must be remediated within the following timeframes:

| CVSS Severity | Remediation Deadline |
|---|---|
| Critical (9.0–10.0) | 72 hours |
| High (7.0–8.9) | 14 calendar days |
| Medium (4.0–6.9) | 60 calendar days |
| Low (0.1–3.9) | Next scheduled release cycle |

7.5.4 Where remediation within the above timeframes is not feasible, the Information Security team will document a risk acceptance or compensating control, approved by the CTO and recorded on the risk register. The CRO must be notified of any Critical vulnerability that cannot be remediated within 72 hours.

7.5.5 Penetration test reports and remediation status will be presented to the Board Risk Committee annually.

---

## 8. Monitoring, Reporting and Escalation

8.1 The Information Security team will operate a Security Information and Event Management (SIEM) system providing continuous monitoring of Crest Bank's production environment. Alerts will be triaged in accordance with the Incident Classification Matrix.

8.2 The CTO will produce a monthly Information Security Dashboard for the Executive Risk Committee, covering: open vulnerabilities by severity, incident volumes and resolution times, access review completion rates, and MFA adoption rates.

8.3 The CCO will include a summary of material security risks and incidents in the quarterly compliance report presented to the Board Risk Committee.

8.4 The escalation path for information security matters is: **Information Security Team → CTO → Executive Risk Committee → Board Risk Committee**. Where a matter has regulatory implications, the CCO is notified in parallel at the CTO escalation stage.

8.5 Any security incident assessed as potentially material to Crest Bank's operational resilience will be escalated to the Board Risk Committee outside of the normal meeting cycle, at the discretion of the CTO or CRO.

---

## 9. Training

9.1 All Crest Bank staff must complete mandatory information security awareness training upon joining Crest Bank (within the first five working days) and annually thereafter.

9.2 Staff in roles with elevated security responsibilities — including the Information Security team, software engineers, and system administrators — must complete role-specific technical security training annually. The CTO will define the required curriculum for these roles.

9.3 Phishing simulation exercises will be conducted at least quarterly across the full staff population. Results will be reported to the Executive Risk Committee. Staff who fail two consecutive simulations will be required to complete targeted remedial training within ten working days.

9.4 Training completion is tracked via Crest Bank's Learning Management System (LMS). The Head of Customer Operations and relevant Heads of Department are responsible for ensuring their teams achieve 100% completion of mandatory training within the required timeframes. Completion rates will be reported to the Compliance Oversight Committee monthly.

---

## 10. Review Cycle

10.1 This policy will be reviewed annually by the CTO, with input from the CCO and CRO, and submitted to the Board Risk Committee for approval.

10.2 An ad-hoc review will be triggered by any of the following:

- A P1 security incident affecting Crest Bank's production environment or customer data.
- A material change to Crest Bank's technology architecture or product set.
- New or amended FCA/PRA rules or guidance that affect information security obligations.
- A recommendation from internal audit or an external penetration test that identifies a gap in this policy's coverage.
- A significant change in the threat landscape, as assessed by the CTO and CRO.

10.3 Any amendments to this policy must be approved by the Board Risk Committee before taking effect. Minor typographical or formatting corrections may be approved by the CTO and noted at the next Board Risk Committee meeting.

---

## 11. Related Documents

| Document | Relationship |
|---|---|
| Data Protection Policy | Governs UK GDPR obligations; must be read alongside this policy for all matters involving personal data. |
| Operational Resilience Policy | Sets impact tolerances for important business services; information security controls must support resilience within those tolerances. |
| Third-Party and Outsourcing Risk Policy | Governs security requirements for suppliers and cloud service providers under SYSC 8. |
| Business Continuity and Disaster Recovery Plan | Defines recovery procedures for technology failures and security incidents affecting service availability. |
| Acceptable Use Policy | Sets out rules for staff use of Crest Bank systems, devices, and networks. |
| Change Management Policy | Governs security review requirements for changes to production systems. |
| AML and Financial Crime Policy | Addresses the intersection of security controls and financial crime prevention, including transaction monitoring system integrity. |

---

*This is a synthetic document created for evaluation purposes. Crest Bank Ltd is a fictional entity. FCA Firm Reference Number 924173 is illustrative only.*
