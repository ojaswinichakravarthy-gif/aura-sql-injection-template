# IEEE Methodology Section

The proposed framework extends the NLP-based machine learning architecture reported by Triloka et al. In the baseline system, SQL queries are converted into a text corpus, transformed by NLP feature engineering, and classified by a supervised learning algorithm. That study evaluates Naive Bayes, Logistic Regression, Gradient Boosting, K-Nearest Neighbor, and Support Vector Machine, with SVM selected as the best-performing classifier.

The proposed Aura framework preserves the baseline SVM experiment as a reproducible reference and introduces five additional research components.

First, a query normalization engine canonicalizes raw queries using iterative URL decoding, Unicode normalization, case folding, SQL comment removal, whitespace normalization, tokenization, hexadecimal literal decoding, and common obfuscation cleanup. This reduces the attacker's ability to evade detection by superficial encoding changes.

Second, a semantic feature extractor computes lexical and NLP-inspired statistics, including SQL keyword frequency, operator frequency, special character density, entropy, token diversity, query length, suspicious token indicators, and attack signature indicators.

Third, an Aura template database models legitimate query structures. Each template stores a canonical pattern, query-tree abstraction, and token sequence. Template intelligence is motivated by the observation that legitimate application queries usually follow stable parameterized forms, whereas SQL injection modifies structure, intent, or logical flow.

Fourth, structural delta analysis compares the normalized query against the closest legitimate template. It computes template mismatch, structural delta, control keyword expansion, predicate complexity, tautology detection, and stacked-query detection.

Fifth, a learning layer fuses semantic and structural features. The experimental design trains a baseline SVM, Random Forest, XGBoost, LightGBM, soft-voting ensemble, weighted-voting ensemble, and stacking ensemble. The best configuration is selected on validation F1 score and then frozen before cross-dataset testing.

The evaluation protocol uses Dataset A for primary training, Dataset B for external validation, Dataset C for independent public-style testing, Dataset D for synthetic obfuscated attacks, and Dataset E for legitimate production-style queries. The strict generalization experiment trains only on Dataset A and tests on B-E without retuning.

