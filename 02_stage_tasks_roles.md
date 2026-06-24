# Fitness, Truth & Structure Lab
## Поэтапные задачи участников, ожидаемые результаты и критерии приёмки

**Документ:** операционный протокол для человека, исследовательского ИИ и Codex  
**Связанная стратегия:** `01_research_strategy.md`

---

# 1. Роли

| Код | Участник | Основная ответственность |
|---|---|---|
| **H** | Human Principal Investigator | Намерение, scope, assumptions, допустимые выводы, решение о публикации |
| **R** | Research AI / ChatGPT | Источники, формализация, план эксперимента, объяснение математики, интерпретация |
| **C** | Codex Implementer | Код, tests, CI, experiments, documentation, release artifacts |
| **V** | Independent AI/Codex Verifier | Независимая проверка формул, кода, assumptions, counterexamples и claims |
| **O** | Automated Oracles / CI | Exact checks, brute force, property tests, regression tests, reproducibility |

Один и тот же продукт может выполнять роли R, C и V, но **не в одной непрерывной сессии**. Reviewer должен начинать с нового контекста и получать только source, specification, code и claimed result.

---

# 2. Что остаётся обязанностью человека

Человек не пишет код, но не превращается в пассивного наблюдателя.

## Человек обязан

- сформулировать, зачем задаётся вопрос;
- выбрать между альтернативными формализациями;
- утвердить assumptions;
- решить, какое утверждение допустимо публиковать;
- отличить интересный результат от желательного результата;
- запросить объяснение до уровня, который он способен пересказать;
- остановить scope creep;
- принять или отклонить release.

## Человек не обязан

- вручную реализовывать алгоритмы;
- вручную считать большие таблицы;
- самостоятельно искать все ошибки в коде;
- знать заранее теорию групп, Bayesian decision theory или RL;
- соглашаться с интерпретацией ИИ без объяснения.

## Минимальный человеческий контроль перед публикацией

Человек должен суметь ответить:

1. Какой именно вопрос проверялся?
2. Какие предположения были заданы?
3. Что измерялось?
4. Какой результат получен?
5. Какой альтернативный результат был возможен?
6. Что из результата не следует?
7. Где лежат код, данные и manifest?

---

# 3. Универсальный контракт задачи для Codex

Ни одна задача не передаётся Codex как «реализуй статью» или «докажи Хоффмана».

Каждый task brief содержит:

```text
TASK ID:
EPISTEMIC STATUS: R / C / E / A
RESEARCH QUESTION:
PRIMARY SOURCE:
FORMAL DEFINITIONS:
INPUT DOMAIN:
EXPECTED OUTPUT:
KNOWN SMALL CASES:
INVARIANTS:
ASSUMPTIONS:
TESTS REQUIRED BEFORE MERGE:
ARTIFACTS TO SAVE:
CLAIMS ALLOWED:
CLAIMS FORBIDDEN:
OUT OF SCOPE:
```

## Универсальные требования к Codex

- математическое ядро не зависит от UI;
- notebooks не являются единственным местом реализации;
- exact arithmetic используется там, где возможен точный ответ;
- каждый новый алгоритм получает tests;
- каждый эксперимент получает manifest;
- random seed не скрывается внутри функции;
- result files не перезаписываются молча;
- код не меняет scientific definitions без decision record;
- каждое допущение получает идентификатор `ASM-...`;
- каждый результат получает идентификатор `EXP-...`;
- каждый публичный claim связан с `CLM-...`.

---

# 4. Универсальный AI-review

Reviewer получает следующий prompt:

```text
Вы независимый проверяющий вычислительного исследования.
Не предполагайте, что реализация или заявленный вывод верны.

1. Независимо перепишите определения.
2. Выведите малые случаи без использования проверяемого кода.
3. Найдите edge cases и counterexamples.
4. Проверьте, соответствует ли алгоритм specification.
5. Проверьте, не встроен ли желаемый результат в assumptions.
6. Проверьте соответствие выводов фактическому domain эксперимента.
7. Разделите fatal errors, major concerns, minor concerns.
8. Не исправляйте код до завершения отчёта.
```

Merge запрещён при unresolved `fatal` или `major` findings.

---

# 5. Этап 0 — исследовательская инфраструктура

## Цель

Создать репозиторий и правила, позволяющие доверять не ИИ, а проверкам.

## H — задачи человека

- выбрать рабочее название и публичность репозитория;
- утвердить миссию и non-goals;
- выбрать лицензию;
- утвердить статусы R/C/E/A;
- решить, публиковать ли prompts и AI-review logs;
- утвердить правило: отрицательные результаты не удаляются.

## R — задачи исследовательского ИИ

- составить `source_map.md`;
- создать `claim_matrix.csv`;
- создать glossary;
- выделить определения FBT и FFF;
- подготовить шаблоны:
  - Claim Card;
  - Assumption Record;
  - Research Decision Record;
  - Experiment Manifest;
  - Publication Checklist;
- сформировать первую smoke specification.

## C — задачи Codex

- создать структуру репозитория;
- создать `pyproject.toml` и lockfile;
- настроить tests, linting, typing и CI;
- создать `AGENTS.md`;
- создать CLI с командой `fts doctor`;
- реализовать manifest schema;
- добавить smoke experiment;
- добавить GitHub issue/PR templates;
- создать команды:
  - install;
  - test;
  - reproduce-smoke;
  - build-docs.

## V — задачи verifier

- проверить, что репозиторий собирается из чистого окружения;
- проверить отсутствие hidden manual steps;
- проверить, что `AGENTS.md` запрещает смешение R/C/E/A;
- проверить manifest schema на полноту.

## Ожидаемые результаты

- зелёный CI;
- reproducible smoke run;
- documented workflow;
- ни одного содержательного вывода о FBT/FFF.

## Не ожидается

- подтверждение теорем;
- симуляция эволюции;
- ML;
- красивый публичный dashboard.

## Acceptance criteria

- новая чистая среда воспроизводит smoke artifact;
- artifact содержит commit hash, dependency lock hash и parameters;
- есть шаблон независимого review;
- все scientific files UTF-8 и машиночитаемы.

## Публикация

P0: методологическая заметка и открытые templates.

## Task brief для Codex

```text
Создай AI-first research repository fitness-truth-structure-lab.
На этом этапе не реализуй FBT или FFF.

Обязательны:
- src layout;
- pytest;
- property-based testing dependency;
- static typing;
- CI;
- immutable experiment manifests;
- AGENTS.md с epistemic statuses R/C/E/A;
- source, assumption, claim и decision registries;
- one-command smoke reproduction;
- documentation describing allowed and forbidden scientific claims.

Не добавляй UI и ML dependencies.
```

---

# 6. Этап 1 — FFF: полные порядки и циклические группы

## Цель

Реализовать первые два exact theorem companions.

## H — задачи человека

- утвердить, что first release ограничен двумя структурами;
- выбрать уровень объяснения demo: простой, математический или оба;
- решить, включать ли только definitions статьи или сразу alternative admissibility в extension tab;
- утвердить формулировку публичного результата.

## R — задачи исследовательского ИИ

- выписать определения:
  - payoff function;
  - admissible function;
  - order-preserving;
  - order-reversing;
  - cyclic group homomorphism;
- вывести small cases вручную;
- составить таблицу edge cases:
  - \(n=1\);
  - \(m=1\);
  - \(n<m\);
  - \(m<n\);
  - constant functions;
  - functions not attaining maximum payoff;
- определить allowed claims;
- спроектировать finite-size figures.

## C — задачи Codex

Создать:

```text
src/fts_lab/fff/
├── functions.py
├── admissibility.py
├── total_orders.py
├── cyclic_groups.py
├── formulas.py
└── reports.py
```

Реализовать:

- enumeration всех функций для малых \(n,m\);
- lazy iterator, не создающий весь список в памяти;
- admissibility filter;
- order preservation/reversal checker;
- cyclic homomorphism checker;
- exact formulas;
- CLI;
- CSV/Parquet export;
- plots;
- thin interactive demo.

## O — обязательные tests

- brute force count = formula для объявленной сетки малых \(n,m\);
- cyclic homomorphism count = \(\gcd(n,m)\);
- identity map сохраняет структуру;
- известные non-homomorphisms отвергаются;
- label relabeling не меняет counts;
- invalid inputs дают явную ошибку.

## V — задачи verifier

- независимо перечислить функции для нескольких малых случаев;
- проверить определение admissibility;
- попытаться найти double counting между order-preserving и order-reversing;
- проверить edge cases;
- проверить, что asymptotic plots не скрывают finite-size behavior.

## Ожидаемые результаты

Допустимы:

- полное совпадение с формулами;
- исправленная интерпретация определения;
- finite-size особенности;
- documented discrepancy.

## Не ожидается

- доказательство выводов о человеческом восприятии;
- проверка permutation groups;
- проверка measurable spaces;
- evolutionary simulation.

## Acceptance criteria

- exact counts совпадают с независимым oracle;
- demo не использует отдельную скрытую реализацию;
- пользователь может скачать исходную таблицу;
- все графики имеют \(n,m\), measure и admissibility definition.

## Публикация

P1: research note + open demo.

## Task brief для Codex

```text
Реализуй этап FFF-Core для total orders и cyclic groups.

Сначала создай tests из specs/fff/.
Brute-force enumeration является oracle для малых случаев.
Closed-form formulas должны быть отдельными функциями.
Не оптимизируй до прохождения exact tests.
Не добавляй permutation groups или measurable spaces.
Сохраняй каждый sweep через experiment manifest.
```

---

# 7. Этап 2 — FBT: точный численный пример

## Цель

Воспроизвести Bayesian calculations из приложения статьи.

## H — задачи человека

- утвердить, что это reproduction, а не общая проверка FBT theorem;
- выбрать формат объяснения calculation trace;
- запросить простое объяснение различия MAP и expected-fitness decision.

## R — задачи исследовательского ИИ

- перенести таблицу статьи в machine-readable specification;
- выписать priors, likelihoods и payoff values;
- независимо рассчитать marginals и posteriors;
- зафиксировать tie policy;
- сформировать allowed/forbidden claims.

## C — задачи Codex

Реализовать:

- immutable data model для finite Bayesian decision problem;
- `Fraction`/exact rational backend;
- posterior calculation;
- MAP truth estimator;
- expected-fitness calculation;
- human-readable derivation report;
- CLI `fts fbt reproduce-numerical-example`;
- regression fixture.

## O — обязательные контрольные значения

Должны быть получены exact arithmetic:

- \(P(x_1)=13/28\);
- \(P(x_2)=15/28\);
- posterior для \(x_1\): \(1/13, 9/13, 3/13\);
- posterior для \(x_2\): \(1/5, 1/5, 3/5\);
- expected fitness: \(5\) и \(33/5\).

## V — задачи verifier

- рассчитать значения независимо;
- проверить ориентацию matrices;
- проверить нормировку;
- проверить tie handling;
- проверить zero-probability observation;
- сравнить exact и float paths.

## Ожидаемые результаты

- точное совпадение;
- либо прозрачный discrepancy report с локализованной причиной.

## Не ожидается

- популяционная динамика;
- генетический алгоритм;
- доказательство FBT theorem;
- вывод о реальном восприятии.

## Acceptance criteria

- ни одно целевое число не hard-coded в implementation;
- derivation report строится из тех же объектов, что tests;
- изменение input table меняет результат;
- regression fixture связан с source citation.

## Публикация

P2: executable reproduction note.

## Task brief для Codex

```text
Реализуй exact reproduction численного примера FBT.
Используй rational arithmetic end to end.
Не реализуй evolution и не вводи perceptual cost.
Целевые числа могут находиться только в tests, но не в production code.
Создай calculation trace, пригодный для чтения человеком.
```

---

# 8. Этап 3 — полный FFF Computational Companion

## Цель

Добавить permutation groups и measurable spaces.

## H — задачи человека

- утвердить допустимый предел exhaustive enumeration;
- решить, является ли approximate homomorphism частью текущего release или backlog;
- утвердить, какие математические детали должны отображаться пользователю.

## R — задачи исследовательского ИИ

### Для permutation groups

- формализовать \(S_n\);
- уточнить тип morphism из статьи;
- вывести counts для минимальных \(n\);
- описать изоморфные дубликаты и canonicalization.

### Для measurable spaces

- связать конечные алгебры событий с partitions;
- определить order \(k\);
- перечислить trivial/discrete special cases;
- вывести small examples measurable/non-measurable functions;
- проверить theorem bound.

## C — задачи Codex

Реализовать:

- finite permutation representation;
- group operation, identity, inverse и closure validation;
- homomorphism checker;
- symmetry-aware enumeration;
- set partition generator;
- finite event algebra constructor;
- inverse-image measurability checker;
- small-space exhaustive oracle;
- theorem formula/bound functions;
- benchmark limits;
- full documentation and demo tabs.

## O — обязательные tests

- group axioms на generated groups;
- known homomorphisms и non-homomorphisms;
- counts для малых \(S_n\);
- every generated event algebra closed under complement и union;
- measurable functions проходят inverse-image criterion;
- trivial/discrete edge cases;
- formula/bound versus enumeration.

## V — задачи verifier

- независимо реализовать малый checker в отдельном файле/языке;
- искать путаницу между group homomorphism и equivariant map;
- проверить, не считается ли одна partition несколько раз;
- проверить theorem domain;
- проверить claims об asymptotic behavior.

## Ожидаемые результаты

- открытая вычислительная реализация четырёх theorem families;
- измеренные границы exhaustive methods;
- возможность обнаружить неоднозначность interpretation.

## Не ожидается

- общая category-theoretic theorem;
- проверка всех возможных структур;
- доказательство психологической неверидичности;
- approximate metrics как часть reproduction.

## Acceptance criteria

- четыре модуля имеют единый интерфейс;
- малые cases проверяются минимум двумя методами;
- UI сообщает, где exact count, где formula, где bound;
- performance limits документированы.

## Публикация

P3: full computational companion + technical report.

## Task brief для Codex

```text
Расширь FFF-Core до permutation groups и finite measurable spaces.
Сначала реализуй валидаторы математических объектов.
Exhaustive enumeration допускается только ниже измеренного порога.
Для больших случаев используй только формулы или bounds из specification.
Не называй bound exact count.
Раздели reproduction и approximate extensions.
```

---

# 9. Этап 4 — FBT Finite Atlas

## Цель

Систематически сравнить стратегии на конечной дискретной сетке моделей.

## H — задачи человека

- утвердить размеры первой сетки;
- выбрать, какие truth strategies являются обязательными;
- утвердить ограничения вычислительного бюджета;
- до запуска утвердить primary metrics;
- принять experiment lock.

## R — задачи исследовательского ИИ

- определить model schema \(W,X,A,\mu,p,F\);
- разделить truth strategy variants;
- определить fitness-only strategy;
- определить dominance, tie и regret;
- спроектировать rational parameter grid;
- оценить размер перебора;
- создать preregistered analysis plan;
- определить, какие результаты могут опровергнуть ожидание.

## C — задачи Codex

Реализовать:

- generic finite decision-problem engine;
- strategy registry;
- exact evaluator;
- rational-grid generator;
- duplicate/canonical model detection;
- parallel sweep;
- resumable execution;
- immutable atlas dataset;
- data validation;
- interactive slice explorer;
- report generator.

## O — обязательные tests

- single-example regression из этапа 2;
- strategies совпадают в специальных случаях;
- relabeling invariance;
- deterministic-kernel cases;
- monotonic-payoff cases;
- tie cases;
- independent random sample recomputation;
- manifest determinism.

## V — задачи verifier

- проверить, не определена ли truth strategy заведомо неудачно;
- проверить fairness action access;
- проверить влияние tie-breaking;
- проверить weighting atlas cells;
- проверить, не выдаётся ли grid count за probability без меры;
- найти counterexamples.

## Ожидаемые результаты

Любой из вариантов:

- fitness-only часто доминирует;
- результат зависит от truth definition;
- доминирование ограничено конкретными payoff families;
- много ties;
- существуют крупные области reverse dominance;
- выбранная мера определяет общую картину.

## Не ожидается

- общий вывод для непрерывных пространств;
- эволюционная фиксация;
- биологическая достоверность;
- подтверждение метафизики.

## Acceptance criteria

- model space полностью описан;
- atlas cells имеют уникальные IDs;
- primary analysis зафиксирован до просмотра полной карты;
- любой cell пересчитывается одной командой;
- альтернативные меры показываются отдельно.

## Публикация

P4: versioned dataset + explorer + methods note.

## Task brief для Codex

```text
Создай exact finite atlas FBT decision problems.
Не используй случайную генерацию как замену объявленной exhaustive grid.
Каждый model, strategy и result должен иметь stable ID.
Раздели raw evaluation и aggregate statistics.
Не интерпретируй число grid cells как probability без явной measure.
```

---

# 10. Этап 5 — эволюционная динамика

## Цель

Проверить переход от expected payoff к population outcomes.

## H — задачи человека

- выбрать две обязательные dynamics: replicator и Moran;
- утвердить mutation и cost assumptions;
- утвердить nonstationary scenarios;
- подтвердить, что «fitness» в модели не тождественен автоматически реальной биологической приспособленности.

## R — задачи исследовательского ИИ

- вывести analytical replicator baselines;
- определить fixation probability metrics;
- определить population-size sweep;
- спроектировать cost ablations;
- спроектировать environment shifts;
- preregister seeds, repeats и confidence intervals;
- описать возможные reversal и coexistence regimes.

## C — задачи Codex

Реализовать:

- replicator dynamics;
- Moran process;
- mutation;
- strategy invasion experiments;
- parameter sweeps;
- reproducible seed schedule;
- uncertainty estimates;
- cost models как plugins;
- environment shift protocol;
- population trajectory viewer;
- batch reports.

## O — обязательные tests

- neutral selection;
- constant fitness;
- known fixation formulas;
- large-population convergence к replicator baseline;
- zero-mutation limits;
- symmetric strategies;
- no-cost and equal-cost ablations.

## V — задачи verifier

- проверить update order;
- проверить population normalization;
- проверить selection bias;
- проверить, не наследуется ли hidden state некорректно;
- проверить statistical power;
- повторить часть runs другим simulator implementation.

## Ожидаемые результаты

- fixation;
- extinction;
- coexistence;
- drift-dominated regime;
- reversal после environment shift;
- исчезновение эффекта после cost ablation.

Все варианты приемлемы.

## Не ожидается

- реалистичная модель всей эволюции;
- доказательство универсального extinction truth;
- оправдание произвольной стоимости информации;
- ML.

## Acceptance criteria

- exact payoff engine остаётся oracle;
- аналитические special cases воспроизводятся;
- confidence intervals и seeds опубликованы;
- sensitivity analysis входит в release;
- cost assumptions маркированы C или E.

## Публикация

P5: evolutionary benchmark report.

## Task brief для Codex

```text
Добавь replicator dynamics и finite Moran process поверх неизменённого FBT core.
Не дублируй вычисление payoff в simulator.
Начни с neutral и analytically solvable tests.
Cost of perception должен быть отключаемым plugin с отдельными ablations.
Сохраняй все trajectories и summary statistics.
```

---

# 11. Этап 6 — Fitness–Structure Atlas

## Цель

Связать успешность агента со структурой его representation.

## H — задачи человека

- выбрать primary structural metrics;
- утвердить, какие структуры считаются заданными задачей;
- запретить post-hoc выбор одной «красивой» метрики;
- утвердить primary hypotheses до запуска.

## R — задачи исследовательского ИИ

Формализовать:

- order violation rate;
- cyclic defect;
- equivariance error;
- measurability/partition preservation;
- distance to nearest exact homomorphism;
- information metrics;
- robustness и transfer metrics.

Создать synthetic maps:

- exact homomorphism;
- near-homomorphism;
- random map;
- constant map;
- adversarially distorted map.

## C — задачи Codex

Реализовать:

- общий `RepresentationMap` protocol;
- structural metric library;
- synthetic ground-truth generator;
- integration с FBT atlas;
- multi-objective analysis;
- Pareto frontier;
- counterexample search;
- interactive linked views;
- exportable report tables.

## O — обязательные tests

- exact maps имеют zero defect;
- controlled perturbations монотонно увеличивают defect там, где ожидается;
- invariance к relabeling;
- metrics различают collapse и true compression;
- nearest-homomorphism routine проверяется brute force на малых cases.

## V — задачи verifier

- искать metric gaming;
- проверять dependence на encoding labels;
- проверять correlation versus causation;
- искать агента с высоким reward и высокой structural fidelity;
- искать агента с низким reward и низкой fidelity;
- проверять counterexamples к основной narrative.

## Ожидаемые результаты

- trade-off;
- отсутствие общего trade-off;
- structure-specific pattern;
- approximate structure предсказывает transfer;
- reconstruction accuracy лучше или хуже structural metrics;
- несколько несовместимых regimes.

## Не ожидается

- единая универсальная мера «истинности»;
- доказательство causal effect без intervention;
- утверждение, что выбранная структура фундаментальна.

## Acceptance criteria

- metrics проходят synthetic ground truth;
- primary hypotheses preregistered;
- counterexamples публикуются;
- post-hoc findings помечены exploratory;
- atlas связывает reward и structure на уровне individual models.

## Публикация

P6: основной preprint и interactive atlas.

## Task brief для Codex

```text
Создай library structural diagnostics и интегрируй её с FBT atlas.
Каждая metric должна иметь formal spec и synthetic tests.
Не используй reconstruction accuracy как синоним structure preservation.
Реализуй counterexample search до построения narrative report.
Раздели confirmatory и exploratory analyses.
```

---

# 12. Этап 7 — ML/AI-эксперимент

## Цель

Сравнить learned representations, обученные на reward, reconstruction и hybrid objective.

## H — задачи человека

- выбрать одну контролируемую среду;
- утвердить одинаковый compute budget;
- утвердить OOD shifts;
- утвердить primary evaluation;
- запретить замену неудачного environment после просмотра результата без новой preregistration.

## R — задачи исследовательского ИИ

- описать POMDP;
- определить observations, latent world state, actions и reward;
- определить три objectives;
- определить architecture budget;
- определить training protocol;
- определить ID/OOD splits;
- определить adaptation protocol;
- сформировать hypothesis matrix.

## C — задачи Codex

Реализовать:

- deterministic environment API;
- oracle state access только для evaluation/reconstruction target;
- shared encoder/policy architecture;
- reward-only objective;
- reconstruction-only objective;
- hybrid objective;
- training/evaluation pipeline;
- checkpointing;
- seeded runs;
- OOD suite;
- representation extraction;
- structural metrics;
- dashboard/replay.

## O — обязательные tests

- environment determinism;
- reward calculation;
- no oracle leakage;
- equal parameter counts;
- equal training-step budgets;
- checkpoint reproducibility;
- random-policy baseline;
- oracle-policy ceiling;
- shuffled-label controls;
- objective-ablation tests.

## V — задачи verifier

- искать leakage true state в reward-only agent;
- проверить fairness hyperparameter tuning;
- проверить cherry-picking seeds;
- проверить OOD definition;
- проверить whether hybrid gets larger effective capacity;
- повторить training subset;
- проверить uncertainty и effect sizes.

## Ожидаемые результаты

Любой из следующих:

- reward-only лучше ID, хуже OOD;
- reconstruction помогает transfer;
- hybrid доминирует;
- truth-like objective не помогает;
- structural metrics не предсказывают transfer;
- эффект зависит от shift type.

## Не ожидается

- вывод о сознании;
- вывод о человеческом зрении;
- универсальное превосходство world models;
- доказательство ITP.

## Acceptance criteria

- одинаковые budgets;
- no leakage;
- несколько seeds;
- uncertainty estimates;
- полный log failed runs;
- primary и exploratory results разделены;
- one-command reproduction хотя бы уменьшенного benchmark.

## Публикация

P7: ML research report + live demo + portfolio case.

## Task brief для Codex

```text
Реализуй один контролируемый POMDP benchmark.
Сравни reward-only, reconstruction-only и hybrid agents при одинаковых
parameter counts, training steps и observation access.

True world state доступен только environment и evaluation code.
Добавь oracle и random baselines, ID/OOD evaluation, structural metrics,
seeded repeats и failed-run registry.
Не добавляй LLM agents.
```

---

# 13. Этап 8 — синтез и открытая платформа

## Цель

Сделать результаты доступными для проверки и обучения.

## H — задачи человека

- выбрать окончательное framing;
- утвердить список claims;
- выбрать порядок подачи материала;
- утвердить releases и archival deposit;
- записать личное объяснение: зачем этот проект существует и чему он научил.

## R — задачи исследовательского ИИ

- создать cross-stage synthesis;
- разделить confirmed, contradicted, assumption-sensitive и open claims;
- подготовить manuscript, slides и tutorials;
- сформировать FAQ;
- подготовить limitations и future work;
- проверить, что популярное объяснение не сильнее technical report.

## C — задачи Codex

- объединить CLI;
- стабилизировать public API;
- собрать website;
- связать figures с manifests;
- создать downloadable datasets;
- создать reproducibility capsule;
- проверить clean-room installation;
- сформировать release notes;
- обновить `CITATION.cff`.

## V — задачи verifier

- audit всех headline claims;
- random figure reproduction;
- dead-link and artifact audit;
- проверить license/provenance;
- проверить, что dashboard не скрывает negative results.

## Ожидаемые результаты

- living atlas;
- technical report;
- open presentation;
- portfolio narrative;
- архивированный release.

## Не ожидается

- «финальное доказательство»;
- закрытие философского вопроса;
- отсутствие открытых проблем.

## Acceptance criteria

- каждый headline claim связан с data и manifest;
- пользователь может воспроизвести representative subset;
- negative/null results доступны;
- release frozen и citable;
- ограничения видны до, а не после выводов.

## Публикация

P8: unified open platform.

## Task brief для Codex

```text
Собери stable public release без изменения scientific results.
Каждая figure должна указывать source manifest.
Добавь clean-room reproduction workflow, downloadable data,
API documentation, tutorials, release notes и citation metadata.
Не удаляй negative/null artifacts ради упрощения интерфейса.
```

---

# 14. Матрица ответственности

| Действие | H | R | C | V | O |
|---|---:|---:|---:|---:|---:|
| Выбор вопроса | **A/R** | C | I | C | I |
| Формализация | A | **R** | C | C | I |
| Assumptions | **A** | R | C | C | I |
| Tests specification | C | **A/R** | R | C | I |
| Код | I | C | **A/R** | C | I |
| CI/oracles | I | C | R | C | **R** |
| Основной experiment lock | **A** | R | C | C | I |
| Независимый review | I | I | I | **A/R** | C |
| Интерпретация | **A** | **R** | C | C | I |
| Публикация | **A/R** | R | C | C | I |

`A` — accountable, `R` — responsible, `C` — consulted, `I` — informed.

---

# 15. Использование Codex worktrees

Рекомендуемая схема для каждой значимой задачи:

```text
main
├── worktree/spec-tests       # тесты и fixtures
├── worktree/implementation   # основная реализация
├── worktree/independent-check# отдельный oracle/reviewer
└── worktree/docs-demo        # документация и UI после стабилизации API
```

Правила:

- implementation не меняет tests без отдельного review;
- independent-check не импортирует production implementation;
- docs-demo не создаёт вторую математическую реализацию;
- merge order: specs/tests → implementation → independent review → docs/demo.

Codex поддерживает параллельные независимые задачи через Git worktrees; project-specific instructions следует хранить в `AGENTS.md`.

---

# 16. Шаблон человеческого Research Decision Record

```markdown
# RDR-XXXX: Название решения

## Намерение
Почему это важно исследовать?

## Варианты
1. ...
2. ...
3. ...

## Объяснение ИИ простыми словами
...

## Риски каждого варианта
...

## Решение человека
...

## Что это решение не означает
...

## Когда пересмотреть
...
```

Человек может принять решение после объяснения, не владея всей техникой доказательства.

---

# 17. Запрещённые короткие пути

- Просить одного агента одновременно придумать формулу, реализовать её и подтвердить её правильность.
- Использовать stochastic simulation там, где доступен exact enumeration.
- Подгонять payoff после просмотра результата.
- Давать truth-agent дополнительную стоимость, не показывая no-cost ablation.
- Считать отсутствие тестовых ошибок доказательством математики.
- Публиковать только лучший seed.
- Называть correlation между structure и transfer причинностью.
- Переносить toy-model conclusion на человеческое восприятие.
- Смешивать reproduction и extension в одном aggregated result.
- Делать UI источником данных вместо отображения versioned artifacts.

---

# 18. Минимальный пакет каждого release

```text
release/
├── README.md
├── CLAIMS.md
├── LIMITATIONS.md
├── ASSUMPTIONS.md
├── REVIEW_REPORT.md
├── environment/
├── manifests/
├── raw_data/
├── derived_data/
├── figures/
├── reproduction_commands.md
└── checksums.txt
```

Release не считается научным release без `CLAIMS.md`, `LIMITATIONS.md` и `REVIEW_REPORT.md`.

---

# 19. Что считать успехом

Успехом является не подтверждение Хоффмана, а одно или несколько из следующего:

- точное воспроизведение результата;
- обнаружение скрытой зависимости от assumption;
- counterexample;
- finite-size correction;
- граница, где результат меняет знак;
- новая structural metric;
- отрицательный ML result;
- открытый reusable tool;
- понятное объяснение сложной математики;
- публичный discrepancy, который другие могут проверить.

---

# 20. Ссылки по организации Codex

- [Codex overview](https://developers.openai.com/codex/)
- [Worktrees](https://developers.openai.com/codex/app/worktrees)
- [AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [Best practices](https://developers.openai.com/codex/learn/best-practices)
- [Subagents](https://developers.openai.com/codex/concepts/subagents)
- [Review](https://developers.openai.com/codex/app/review)
