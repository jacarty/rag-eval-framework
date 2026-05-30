# Business Continuity Policy

---

## 1. Document Control

| Field | Detail |
|---|---|
| **Policy Title** | Business Continuity Policy |
| **Version** | 2.1 |
| **Effective Date** | 1 February 2025 |
| **Next Review Date** | 31 January 2026 |
| **Document Owner** | Tom Hargreaves, Chief Technology Officer |
| **Approving Body** | Board Risk Committee |

---

## 2. Purpose

This policy establishes Crest Bank's framework for maintaining operational resilience and ensuring continuity of critical business services in the event of a disruption, whether caused by technology failure, cyber incident, third-party outage, or other adverse event. It sets out the obligations of all relevant staff and governance bodies in preparing for, responding to, and recovering from business disruptions. This policy supports Crest Bank's compliance with FCA and PRA operational resilience requirements and its commitment to delivering uninterrupted service to its 850,000 retail and 12,000 SME customers.

---

## 3. Scope

This policy applies to:

- **All Crest Bank employees**, contractors, and third-party service providers operating on behalf of Crest Bank
- **All business functions**, including Technology, Customer Operations, Finance, Compliance, Risk, and People
- **All products and services**, including personal current accounts, savings products (instant-access and fixed-term), personal loans, and SME business current accounts
- **All systems and infrastructure** supporting the delivery of digital banking services, including core banking platforms, mobile and web applications, payment processing systems, cloud infrastructure, and data storage environments
- **Third-party and outsourced arrangements** where a provider delivers a function material to Crest Bank's operations

---

## 4. Regulatory Context

| Regulatory Source | Relevance to This Policy |
|---|---|
| **SS1/21 — Operational Resilience (PRA/FCA joint policy)** | Requires firms to identify important business services, set impact tolerances, and demonstrate the ability to remain within those tolerances through severe but plausible disruption scenarios |
| **SYSC 4.1** | Requires firms to have robust governance arrangements, including adequate internal control mechanisms and business continuity policies |
| **SYSC 6.1** | Requires firms to establish, implement, and maintain adequate policies and procedures to ensure compliance with regulatory obligations, including resilience of operations |
| **SYSC 13.1** | Addresses operational risk management, requiring firms to implement appropriate systems and controls to manage risks arising from inadequate internal processes, people, systems, or external events |
| **PRIN 2 (Principle 2)** | Requires Crest Bank to conduct its business with due skill, care, and diligence, which encompasses maintaining continuity of service to customers |
| **PRIN 6 (Principle 6)** | Requires Crest Bank to pay due regard to the interests of its customers and treat them fairly, including during periods of operational disruption |
| **PS21/3 — Building Operational Resilience** | FCA policy statement setting out final rules and expectations for operational resilience implementation, including the March 2025 deadline for remaining within impact tolerances |

---

## 5. Policy Statement

Crest Bank is committed to maintaining the continuity of its important business services and protecting its customers, staff, and counterparties from the adverse effects of operational disruption. The following principles govern Crest Bank's approach to business continuity:

1. **Crest Bank will identify and document all important business services** and the people, processes, technology, facilities, and third-party dependencies that support them, maintaining this mapping as a living record reviewed at least annually.

2. **Crest Bank will set and maintain impact tolerances** for each important business service, expressed as the maximum tolerable duration and level of disruption, and will take all reasonable steps to ensure it can remain within those tolerances during a severe but plausible disruption scenario.

3. **Crest Bank will conduct a Business Impact Analysis (BIA)** at least annually, and following any material change to business services or infrastructure, to assess the potential consequences of disruption and inform recovery prioritisation.

4. **Crest Bank will maintain documented Business Continuity Plans (BCPs) and Disaster Recovery Plans (DRPs)** for all critical systems and business functions, with clearly defined Recovery Time Objectives (RTOs) and Recovery Point Objectives (RPOs).

5. **Crest Bank will test its continuity and recovery arrangements** at a frequency and depth proportionate to the criticality of the service, and will act on lessons identified through testing to continuously improve its resilience posture.

6. **Crest Bank will maintain a crisis communication framework** that ensures timely, accurate, and transparent communication with customers, regulators, and other stakeholders during a disruption.

7. **Crest Bank will manage third-party and outsourcing risks** as an integral part of its business continuity framework, requiring material third-party providers to demonstrate continuity arrangements consistent with Crest Bank's own standards.

8. **Crest Bank will embed a culture of operational resilience** across all business functions, ensuring that continuity planning is treated as a standing operational responsibility rather than a periodic compliance exercise.

---

## 6. Roles and Responsibilities

| Role | Responsibilities Under This Policy |
|---|---|
| **Tom Hargreaves, CTO** | Policy owner; overall accountability for technology disaster recovery; approves RTOs and RPOs; chairs the Technology Crisis Response Team |
| **David Okonkwo, CRO** | Oversees the operational risk framework within which BCP sits; escalates material resilience risks to the Board Risk Committee |
| **Rachel Whitfield, CCO** | Ensures BCP arrangements satisfy regulatory obligations; leads regulatory notification in the event of a material disruption |
| **Priya Sharma, Head of Customer Operations** | Owns customer-facing continuity procedures; leads crisis communication to customers; maintains the Customer Operations BCP |
| **Sarah Chen, CEO** | Chairs the Executive Crisis Management Team during a declared major incident; has authority to invoke the firm-wide BCP |
| **Michael Byrne, Chair, Board Risk Committee** | Receives quarterly resilience reporting; approves this policy and any material amendments; escalation point for incidents that may require regulatory notification |
| **All Heads of Department** | Maintain function-level BCPs; ensure staff complete mandatory BCP training; participate in scheduled BCP tests |
| **Third-Party Providers (material)** | Provide evidence of their own BCP and DR arrangements; notify Crest Bank promptly of any disruption affecting services delivered to Crest Bank |

---

## 7. Procedures

### 7.1 Business Impact Analysis

7.1.1 The CRO, working with the CTO and Heads of Department, will commission a full Business Impact Analysis (BIA) annually, with results documented and presented to the Executive Risk Committee no later than 31 October each year.

7.1.2 The BIA will assess each important business service against the following dimensions: financial impact, customer harm, regulatory breach risk, and reputational damage, scored across disruption durations of one hour, four hours, 24 hours, 72 hours, and one week.

7.1.3 BIA outputs will directly inform the setting or revision of impact tolerances, RTOs, and RPOs for each service. Any proposed change to an impact tolerance must be approved by the Board Risk Committee before taking effect.

7.1.4 An ad-hoc BIA will be triggered by any material change to Crest Bank's technology infrastructure, product set, or third-party arrangements, as determined by the CRO.

### 7.2 Recovery Time Objectives and Recovery Point Objectives

7.2.1 The CTO will maintain a register of RTOs and RPOs for all critical systems, reviewed and reaffirmed annually as part of the BIA cycle. The current minimum standards are:

| Service Category | RTO | RPO |
|---|---|---|
| Core banking platform | 4 hours | 1 hour |
| Payment processing (Faster Payments, BACS) | 2 hours | 30 minutes |
| Mobile and web banking applications | 4 hours | 1 hour |
| Customer authentication and identity services | 2 hours | 30 minutes |
| Internal communications and staff systems | 8 hours | 4 hours |
| Regulatory reporting systems | 24 hours | 4 hours |

7.2.2 Where a system's actual recovery capability does not meet its RTO or RPO, the CTO will raise a remediation plan to the Executive Risk Committee within 30 days of the gap being identified, with a target remediation date.

### 7.3 Disaster Recovery for Digital Banking Services

7.3.1 In accordance with SYSC 13.1, Crest Bank will maintain a geographically separate secondary environment capable of hosting all critical digital banking services. The CTO is responsible for ensuring this environment is kept current and tested in accordance with section 7.5.

7.3.2 Failover procedures for each critical system will be documented in the relevant DRP, held in Crest Bank's policy management system and accessible to authorised personnel offline in the event of a primary system failure.

7.3.3 Cloud infrastructure arrangements will be configured to support automated failover where technically feasible. The CTO will review the feasibility of automated failover for any system currently relying on manual failover procedures as part of each annual BIA cycle.

7.3.4 Data backup procedures will ensure that backups are performed at a frequency consistent with each system's RPO, stored in an encrypted format, and tested for restorability at least quarterly.

### 7.4 Crisis Communication

7.4.1 The Head of Customer Operations, Priya Sharma, is responsible for maintaining the Customer Crisis Communication Plan, which sets out pre-approved messaging templates, communication channels (in-app notifications, email, website status page, social media), and escalation triggers for customer-facing communications.

7.4.2 In the event of a disruption affecting customer access to any product or service, Crest Bank will publish an initial customer notification within 30 minutes of a major incident being declared, and provide updates at intervals of no greater than two hours until service is restored.

7.4.3 The CCO, Rachel Whitfield, is responsible for regulatory notification. In accordance with SYSC 6.1, Crest Bank will notify the FCA and PRA of any operational incident that meets the threshold for regulatory reporting as soon as practicable, and no later than the timeframe specified in applicable regulatory guidance. The CCO will maintain a log of all regulatory notifications made under this procedure.

7.4.4 Internal crisis communications will be coordinated by the CEO through the Executive Crisis Management Team, using the designated out-of-band communication channel maintained by the CTO for use when primary systems are unavailable.

### 7.5 BCP and DRP Testing

7.5.1 Crest Bank will conduct the following minimum programme of BCP and DRP testing each calendar year:

| Test Type | Frequency | Led By |
|---|---|---|
| Tabletop exercise (scenario walkthrough) | Twice yearly | CRO |
| Component-level DR test (individual systems) | Quarterly | CTO |
| Full failover test (end-to-end DR simulation) | Annually | CTO and CRO jointly |
| Third-party resilience review | Annually | CRO |

7.5.2 Each test will produce a written report, including a summary of findings, any gaps identified, and a remediation action log with owners and target dates. Test reports will be presented to the Executive Risk Committee within 30 days of the test being completed.

7.5.3 Where a test reveals that Crest Bank cannot meet an impact tolerance, the CTO and CRO will jointly present a remediation plan to the Board Risk Committee at its next scheduled meeting.

---

## 8. Monitoring, Reporting and Escalation

8.1 The CTO will maintain a live operational resilience dashboard, reviewed weekly by the Technology leadership team, tracking system availability, backup success rates, and open remediation actions.

8.2 The CRO will present a quarterly Operational Resilience Report to the Board Risk Committee, covering: BCP and DRP test outcomes, open remediation actions, any incidents that triggered BCP invocation, and changes to the important business services mapping or impact tolerances.

8.3 The Executive Risk Committee will receive a monthly update on the status of BCP and DR remediation actions and any emerging resilience risks.

8.4 **Escalation path for live incidents:**

- **Level 1 (Minor disruption — service degraded but within impact tolerance):** CTO notified; Technology Crisis Response Team convened; Head of Customer Operations informed.
- **Level 2 (Significant disruption — risk of breaching impact tolerance within four hours):** CEO and CRO notified; Executive Crisis Management Team convened; CCO assesses regulatory notification obligation.
- **Level 3 (Major incident — impact tolerance breached or breach imminent):** Board Risk Committee Chair notified; FCA/PRA notification initiated by CCO; customer communications activated.

---

## 9. Training

9.1 All staff must complete Crest Bank's mandatory Business Continuity Awareness training module upon joining and annually thereafter. Completion is tracked through Crest Bank's learning management system, with non-completion reported to the relevant Head of Department and to the CCO.

9.2 Staff with named roles in any BCP or DRP (including all Heads of Department and members of the Executive Crisis Management Team) must complete an enhanced BCP role-holder training module annually, and must participate in at least one tabletop exercise per year.

9.3 The CTO will ensure that Technology staff responsible for executing DR procedures receive hands-on technical DR training at least twice per year, aligned with the quarterly component-level DR test programme.

9.4 Training completion rates will be reported to the Compliance Oversight Committee quarterly.

---

## 10. Review Cycle

10.1 This policy will be reviewed annually by the document owner (CTO) in conjunction with the CRO and CCO, with any proposed amendments submitted to the Board Risk Committee for approval.

10.2 An ad-hoc review will be triggered by any of the following:

- A material operational incident that resulted in BCP invocation
- A significant change to Crest Bank's technology infrastructure or product set
- A material change to FCA or PRA operational resilience requirements
- A BCP or DRP test that identifies a gap against an impact tolerance
- A recommendation from internal audit or an external review

10.3 Minor amendments (for example, updates to named role-holders or contact details) may be approved by the CTO and CCO jointly, without requiring full Board Risk Committee approval, provided the substantive content of the policy is unchanged. All amendments, however minor, will be recorded in the document version history.

---

## 11. Related Documents

- Operational Resilience Policy
- IT Security and Cyber Resilience Policy
- Incident Management Policy
- Third-Party and Outsourcing Risk Policy
- Data Management and Backup Policy
- Crisis Communications Framework
- Customer Vulnerability Policy
- Risk Appetite Statement

---

*This is a synthetic document produced for evaluation and testing purposes. It does not represent the policy of any real financial institution.*
