# IEEE Discussion Section

The baseline NLP-SVM approach is strong when training and testing distributions are similar, but it can over-rely on token-level artifacts. SQL injection attacks often preserve or perturb text in ways that make lexical classification brittle: comments split keywords, URL encoding hides operators, and time-based or union-based payloads may be embedded in otherwise legitimate queries.

Aura addresses these limitations by combining lexical evidence with structural evidence. Template matching estimates whether a query resembles an expected application query. Structural delta analysis then measures whether logical flow has expanded beyond the legitimate form. For example, a normal query such as `SELECT * FROM users WHERE id = ?` has one predicate over `id`, whereas `SELECT * FROM users WHERE id = 1 OR 1=1 --` introduces a new control operator, tautology, and comment truncation. This makes the attack visible even when individual tokens are obfuscated.

Explainability is also central. Each prediction returns the decision, confidence, threat level, most influential features, and reason. This supports analyst review, production debugging, and reviewer inspection.

The expected trade-off is that template intelligence requires maintaining representative legitimate templates. This is practical in many production systems because ORM-generated and parameterized SQL tends to be stable. For highly dynamic analytic SQL, templates should be learned from query logs and organized by service, endpoint, tenant, or query family.

