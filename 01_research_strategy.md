# Fitness, Truth & Structure Lab
## Основная стратегия AI-first исследования

**Статус:** рабочая стратегия v0.1  
**Область:** вычислительное исследование `Fitness Beats Truth` (FBT) и `Fact, Fiction, and Fitness` (FFF)  
**Модель работы:** человек задаёт намерение и принимает исследовательские решения; ChatGPT/исследовательский ИИ формализует вопросы и интерпретирует данные; Codex реализует, тестирует и документирует код; независимый AI-review проверяет реализацию и выводы.

---

## 1. Миссия программы

Основной вопрос программы:

> **Когда оптимизация полезности/fitness уничтожает информацию о структуре мира, а когда truth-like представления дают преимущество за счёт устойчивости, переноса и адаптации к изменению среды?**

Программа не создаётся для подтверждения заранее выбранной метафизики. Она создаётся для:

1. точного воспроизведения доступной математики FBT и FFF;
2. превращения теорем и аргументов в проверяемые вычислительные объекты;
3. поиска границ применимости утверждений Хоффмана и соавторов;
4. построения открытого инструментария для исследований reward optimization, representation learning, robustness и generalization;
5. постепенной публикации положительных, отрицательных и нулевых результатов.

### Что программа может установить

- воспроизводятся ли опубликованные численные примеры и комбинаторные формулы;
- при каких конечных параметрах fitness-only strategy превосходит truth strategy;
- при каких условиях преимущество исчезает или меняет знак;
- какие структуры мира сохраняются или разрушаются payoff-функциями и learned representations;
- влияет ли структурная веридичность на перенос в новые среды;
- какие выводы зависят от конкретной меры, prior, payoff family, perceptual cost или evolutionary dynamics.

### Что программа не может установить сама по себе

- что объективной реальности не существует;
- что пространство-время обязательно является интерфейсом;
- что сознание фундаментально;
- что сети conscious agents являются правильной онтологией;
- что результаты toy-моделей автоматически описывают человеческое восприятие.

---

## 2. Научная линия исследования

Две исходные работы играют разные роли.

### FBT: конкуренция стратегий

`Fitness Beats Truth in the Evolution of Perception` формализует сравнение стратегии, оценивающей состояние мира, и стратегии, непосредственно максимизирующей ожидаемый fitness payoff. Работа использует Bayesian decision theory и evolutionary game theory и содержит численный пример, пригодный для точной вычислительной проверки.

### FFF: сохранение структуры

`Fact, Fiction, and Fitness` рассматривает payoff-функции как отображения и спрашивает, являются ли они гомоморфизмами структур мира. Авторы исследуют:

- полные порядки;
- группы перестановок;
- циклические группы;
- измеримые пространства.

Их аргумент основан на подсчёте всех допустимых payoff-функций и тех из них, которые сохраняют соответствующую структуру.

### Объединяющий шаг

FBT измеряет **успех стратегии**.  
FFF измеряет **структурную верность отображения**.

Объединённая программа измеряет одновременно:

\[
\text{fitness/reward},\quad
\text{truth accuracy},\quad
\text{structure preservation},\quad
\text{robustness},\quad
\text{transfer}.
\]

Именно эта интеграция превращает проект из репликации двух статей в самостоятельную AI/ML-исследовательскую программу.

---

## 3. Эпистемический контракт

Каждый результат должен иметь один из четырёх статусов.

| Статус | Смысл |
|---|---|
| **R — Reproduction** | Реализация буквально следует опубликованному определению, формуле или численному примеру. |
| **C — Computational reconstruction** | В статье недостаточно деталей; недостающие решения явно записаны в `assumptions/`. |
| **E — Extension** | Новая модель или эксперимент, не заявленные авторами. |
| **A — Analogy** | Перенос идеи в ML/AI; не является проверкой исходной биологической или философской гипотезы. |

Нельзя смешивать эти статусы в одном графике или выводе без явной маркировки.

### Обязательные правила

1. **Воспроизведение предшествует расширению.**
2. **Точный расчёт предшествует stochastic simulation.**
3. **Простые конечные модели предшествуют ML.**
4. **Отсутствующий параметр нельзя молча угадывать.**
5. **Результат не обязан поддерживать Хоффмана.**
6. **Несовпадение с публикацией является результатом, а не поводом скрыть эксперимент.**
7. **Каждый публичный тезис должен указывать, какие assumptions ему необходимы.**
8. **Код, написанный ИИ, не считается проверенным только потому, что он запускается.**

---

## 4. Модель участников

### Человек — Principal Investigator / источник намерения

Человек не обязан писать код или вручную доказывать теоремы. Его незаменимые функции:

- выбирать исследовательский вопрос;
- определять, какие assumptions допустимы;
- фиксировать приоритет между строгостью, широтой и скоростью;
- утверждать допустимую формулировку выводов;
- решать, публиковать ли результат;
- не позволять ИИ подменять вопрос более удобной задачей.

### Исследовательский ИИ — Research Lead

Задачи:

- разбирать первичные статьи;
- переводить определения в формальные спецификации;
- составлять карту утверждений и зависимостей;
- проектировать эксперименты и falsification tests;
- объяснять математику человеку;
- интерпретировать результаты с учётом ограничений;
- готовить черновики исследовательских заметок.

### Codex — Implementer

Задачи:

- создавать и изменять репозиторий;
- реализовывать математическое ядро;
- писать exact, unit, property-based и integration tests;
- создавать CLI, конфигурации, анализ и визуализации;
- запускать воспроизводимые эксперименты;
- формировать документацию и release artifacts.

### Независимый AI/Codex reviewer — Verifier

Это отдельная сессия или агент с новым контекстом. Он должен:

- независимо вывести ожидаемые малые случаи;
- искать counterexamples;
- проверять соответствие кода спецификации;
- атаковать assumptions и статистический дизайн;
- пытаться опровергнуть вывод до публикации.

Разработчик и reviewer не должны быть одной и той же непрерывной сессией.

### Автоматические проверяющие механизмы

- exact rational arithmetic;
- brute-force oracle для малых пространств;
- symbolic algebra там, где она уместна;
- property-based tests;
- CI;
- статические проверки типов;
- проверка воспроизводимости из чистого окружения.

---

## 5. Рабочий цикл одного исследовательского утверждения

Каждая задача проходит одинаковый конвейер.

1. **Claim Card**  
   Какое конкретное утверждение проверяется? Где оно находится в источнике? Какой результат его поддерживает или опровергает?

2. **Formal Specification**  
   Определения, обозначения, входы, выходы, domains, assumptions и edge cases.

3. **Acceptance Tests Before Implementation**  
   Минимальные случаи, известные формулы, точные дроби, инварианты и ожидаемые ошибки.

4. **Implementation**  
   Codex пишет математическое ядро отдельно от UI и notebooks.

5. **Independent Review**  
   Второй агент получает статью, спецификацию и код, но не получает оправдания решений первого агента.

6. **Experiment Lock**  
   До основного запуска фиксируются конфигурация, метрики, seeds, критерии исключения и допустимые выводы.

7. **Execution**  
   Результаты сохраняются как неизменяемые artifacts вместе с commit hash и environment metadata.

8. **Interpretation**  
   Сначала автоматически формируется factual report. Интерпретация добавляется отдельно.

9. **Publication Gate**  
   Публикуются код, данные, assumptions, failures и ограничения — не только удачные графики.

---

## 6. Предлагаемая структура репозитория

```text
fitness-truth-structure-lab/
├── AGENTS.md
├── README.md
├── CITATION.cff
├── LICENSE
├── pyproject.toml
├── uv.lock
├── sources/
│   ├── bibliography.bib
│   ├── source_map.md
│   └── claim_matrix.csv
├── specs/
│   ├── notation.md
│   ├── epistemic_status.md
│   ├── fff/
│   ├── fbt/
│   └── integrated/
├── assumptions/
│   ├── register.md
│   └── decisions/
├── src/fts_lab/
│   ├── common/
│   ├── fff/
│   ├── fbt/
│   ├── evolution/
│   ├── structure_metrics/
│   └── ml/
├── tests/
│   ├── exact/
│   ├── properties/
│   ├── regression/
│   └── integration/
├── experiments/
│   ├── configs/
│   ├── manifests/
│   └── schemas/
├── results/
│   ├── raw/
│   ├── derived/
│   └── reports/
├── notebooks/
├── web/
├── docs/
│   ├── research_notes/
│   ├── tutorials/
│   └── figures/
└── publications/
    ├── notes/
    ├── preprints/
    └── slides/
```

`AGENTS.md` должен задавать Codex правила проекта: не менять формулы без ссылки на decision record, не смешивать reproduction и extension, не добавлять случайные зависимости, всегда запускать exact tests перед stochastic tests.

---

# 7. Последовательность исследования

## Этап 0. Исследовательская инфраструктура и контракт воспроизводимости

**Цель:** создать систему, в которой AI-generated code можно проверять, а не просто запускать.

### Работы

- собрать первичные источники и таблицу проверяемых утверждений;
- утвердить терминологию;
- создать `assumptions/register.md`;
- определить статусы R/C/E/A;
- создать repository scaffold;
- настроить lockfile, CI, tests, linting, type checking;
- реализовать единый формат experiment manifest;
- создать шаблоны research issue, decision record и release checklist.

### Выход

- пустой, но полностью работоспособный исследовательский репозиторий;
- один smoke experiment;
- одна демонстрационная Claim Card, прошедшая весь процесс.

### Точка публикации P0

**Открытая заметка:** «Как проверять математические утверждения с помощью AI-generated research code».

Публикуются:

- методология;
- шаблоны;
- `AGENTS.md`;
- reproducibility contract;
- ограничения AI-first исследования.

Это самостоятельный полезный результат даже до появления научных данных.

### Условие перехода

Новый пользователь или новый Codex-agent может клонировать репозиторий, выполнить одну команду и получить зелёный CI и идентичный smoke result.

---

## Этап 1. FFF-Core: полные порядки и циклические группы

**Цель:** получить первое строгое вычислительное ядро с точным oracle.

### Исследовательские вопросы

1. Совпадает ли brute-force enumeration с формулами статьи на малых \(n,m\)?
2. Как быстро доля structure-preserving payoff functions уменьшается в конечных пространствах?
3. Насколько результат зависит от определения admissibility?
4. Что видно на конечных размерах до асимптотического режима?

### Реализация

- генератор всех функций \(f:W\to V\) для малых пространств;
- фильтр admissible payoff functions;
- проверка сохранения/обращения полного порядка;
- проверка homomorphism для \(\mathbb{Z}_n\to\mathbb{Z}_m\);
- exact counts и closed-form formulas;
- property-based tests;
- finite-size heatmaps;
- интерактивная демонстрация.

### Возможные результаты

- полное совпадение с формулами;
- обнаружение ошибки в собственной интерпретации;
- неоднозначность в admissibility;
- корректная асимптотика, но неожиданный finite-size режим;
- несовпадение, требующее публичного discrepancy report.

### Точка публикации P1

**Research note + open demo:**  
`When Does Fitness Preserve Order and Cycles? A Computational Companion`

Пакет публикации:

- GitHub release;
- архивированный набор таблиц;
- короткая статья с exact checks;
- браузерная демонстрация;
- объяснение без метафизических выводов.

### Условие перехода

- brute force и формулы совпадают на всех заявленных малых случаях;
- reviewer независимо подтверждает определения;
- каждый график строится из сохранённого manifest.

---

## Этап 2. FBT-Core: точное воспроизведение численного примера

**Цель:** проверить базовый Bayesian/decision-theoretic расчёт до любой эволюционной симуляции.

### Реализация

- точные priors;
- likelihood/perceptual kernel;
- Bayes posterior;
- MAP truth estimate;
- expected-fitness strategy;
- exact rational arithmetic;
- автоматическое формирование calculation trace;
- сравнение результата с приложением статьи.

### Контрольные значения

Реализация должна независимо получить опубликованные промежуточные дроби, posterior distributions и expected fitness values. Любое расхождение блокирует дальнейшую работу до выяснения причин.

### Дополнительные проверки

- перестановка labels не должна менять содержательный результат;
- нормировка вероятностей;
- обработка ties;
- zero-probability observations;
- сравнение float и exact arithmetic.

### Точка публикации P2

**Короткая воспроизводимая заметка:**  
`Reproducing the Fitness-Beats-Truth Numerical Example`

Даже если результат полностью совпадает, заметка полезна как открытый executable companion к статье.

### Условие перехода

- все exact tests зелёные;
- calculation trace можно прочитать без кода;
- definitions truth strategy и fitness strategy явно зафиксированы.

---

## Этап 3. Полный FFF Computational Companion

**Цель:** реализовать все четыре семейства структур из FFF.

### Новые модули

#### Группы перестановок

- конечные symmetric groups;
- group operation и identity/inverse checks;
- homomorphism/equivariance tests;
- exact enumeration только для вычислимо малых размеров;
- formulas и symmetry reduction для больших случаев.

#### Измеримые пространства

- конечные partitions;
- алгебры событий, порождённые partitions;
- inverse-image measurability;
- enumeration малых measurable spaces;
- проверка bounds/formulas из статьи;
- выявление trivial/discrete edge cases.

### Исследовательские расширения

Пока только как отдельная ветка E:

- partial orders;
- approximate homomorphisms;
- weighted/non-uniform measures на payoff functions;
- distance to nearest homomorphism.

### Точка публикации P3

**Полный открытый computational companion к FFF:**

- четыре интерактивных раздела;
- exact tables;
- automated theorem checks;
- tutorial;
- технический отчёт;
- архивированный release.

При качественной документации это уже самостоятельный сильный проект по mathematical research engineering.

### Условие перехода

- все четыре theorem modules имеют независимые малые oracles;
- ограничения полного перебора измерены, а не скрыты;
- exact reproduction отделена от новых мер и approximate metrics.

---

## Этап 4. FBT Finite Atlas: полный перебор конечных моделей

**Цель:** перейти от одного примера к карте конечных пространств решений.

### Пространство исследования

- конечные world states \(W\);
- perceptual states \(X\);
- actions \(A\);
- priors \(\mu(w)\);
- stochastic perceptual kernels \(p(x\mid w)\);
- payoff matrices \(F(w,a)\);
- несколько чётко разделённых truth strategies;
- fitness-only strategy.

### Стратегии truth

Нельзя использовать только одно неявное определение. Минимум:

1. MAP estimate;
2. posterior sampling;
3. posterior mean — только при наличии метрики;
4. full-posterior decision baseline.

Каждый вариант сравнивается отдельно.

### Основные метрики

- expected payoff;
- probability of strict dominance;
- ties;
- truth/reconstruction accuracy;
- mutual information;
- regret;
- sensitivity к prior и noise;
- доля результатов, зависящих от tie-breaking.

### Ограничение

«Полный перебор» относится только к заранее объявленной дискретной сетке рациональных priors, kernels и payoffs. Нельзя выдавать finite atlas за перебор всех непрерывных моделей.

### Точка публикации P4

**Dataset + explorer + methods note:**  
`A Finite Atlas of Fitness-Only and Truth-Seeking Decision Strategies`

Публикация ценна независимо от того, преобладает ли fitness-only strategy.

### Условие перехода

- пространство перебора описано полностью;
- любой atlas cell воспроизводится по manifest;
- reviewer находит те же результаты независимым скриптом для случайной выборки клеток;
- выводы ограничены исследованной сеткой.

---

## Этап 5. Эволюционная динамика

**Цель:** проверить, как статическое преимущество превращается — или не превращается — в динамику популяций.

### Минимальный набор моделей

1. replicator dynamics для аналитического baseline;
2. finite-population Moran process;
3. mutation;
4. контролируемая стоимость perception/information.

Wright–Fisher, crossover и сложные геномы добавляются только после стабильного минимального ядра.

### Ключевые вопросы

- означает ли более высокий expected payoff фиксацию в конечной популяции;
- как population size влияет на drift;
- когда mutation поддерживает coexistence;
- что происходит при frequency-dependent payoffs;
- насколько результат чувствителен к perceptual cost;
- можно ли получить преимущество interface strategy без вручную назначенного «налога на истину».

### Нестационарные среды

Вводятся как отдельный preregistered блок:

- изменение prior;
- изменение payoff;
- изменение observation channel;
- появление новых world states;
- переключение целей.

### Точка публикации P5

**Open benchmark + technical report:**  
`From Expected Fitness to Evolutionary Fixation`

Полезные результаты:

- подтверждение;
- coexistence;
- reversal;
- сильная зависимость от population size;
- отсутствие эффекта после устранения встроенного perceptual cost.

### Условие перехода

- аналитический baseline совпадает с симуляцией в предельных случаях;
- результаты устойчивы к seeds;
- cost model проходит ablation;
- нет скрытого неравенства computational budget между агентами.

---

## Этап 6. Интеграция FBT и FFF: Fitness–Structure Atlas

**Цель:** измерить не только успех стратегии, но и то, какую структуру она сохраняет.

### Структурные метрики

- order violation rate;
- cyclic homomorphism defect;
- equivariance error;
- partition/measurability preservation;
- distance to nearest homomorphism;
- compression ratio;
- mutual information \(I(W;Z)\);
- task-relevant information \(I(F;Z)\).

### Центральные вопросы

1. Всегда ли более высокий fitness связан с меньшей структурной верностью?
2. Существуют ли структуры, сохраняемые даже fitness-only representations?
3. Какие структуры предсказывают transfer?
4. Может ли representation быть невалидным по одному критерию и структурно верным по другому?
5. Предсказывает ли approximate homomorphism robustness лучше, чем reconstruction accuracy?

### Основной новый вклад

Это первая точка, где проект перестаёт быть только computational companion и становится самостоятельным исследованием:

\[
\text{reward optimization}
\longleftrightarrow
\text{structure preservation}
\longleftrightarrow
\text{robustness}.
\]

### Точка публикации P6

**Preprint + interactive atlas:**  
`Fitness, Truth, and Structure: When Useful Representations Preserve the World`

Публикация должна включать и counterexamples к собственной основной тенденции.

### Условие перехода

- structural metrics проверены на искусственных отображениях с известными свойствами;
- метрики не подбирались после просмотра конечного результата;
- указано, какие структуры заданы исследователем, а не «обнаружены в реальности».

---

## Этап 7. ML/AI-расширение

**Цель:** проверить те же вопросы на обучаемых representations.

### Минимальный эксперимент

Одна контролируемая POMDP-среда и три агента с одинаковым parameter/compute budget:

1. **reward-only:** оптимизирует reward;
2. **reconstruction-only:** восстанавливает world state;
3. **hybrid:** оптимизирует reward и reconstruction с коэффициентом \(\alpha\).

Базовая схема:

\[
w_t \rightarrow o_t \rightarrow z_t
\rightarrow a_t \rightarrow r_t.
\]

### Обязательные сравнения

- in-distribution reward;
- reconstruction accuracy;
- structural metrics из этапа 6;
- OOD reward;
- transfer после изменения payoff;
- adaptation speed;
- calibration;
- representation complexity.

### Следующие ветки только после минимального эксперимента

- information bottleneck;
- model-based versus model-free RL;
- continual learning;
- meta-learning;
- coevolution;
- causal representation learning;
- adversarial environment shift.

LLM-агенты не являются первым экспериментом: они добавляют слишком много скрытых priors и плохо контролируемого поведения.

### Точка публикации P7

**AI/ML research report + live demo:**  
`Do Truth-Like Representations Transfer Better? Fitness Optimization under Distribution Shift`

Это наиболее сильный портфолио-артефакт для AI/ML:

- environment;
- training pipeline;
- reproducible experiments;
- representation analysis;
- OOD evaluation;
- interactive visualization.

### Условие завершения

- одинаковый compute budget;
- заранее зафиксированные objectives;
- несколько seeds и confidence intervals;
- ablations;
- не скрываются неудачные runs;
- выводы не переносятся на биологическое восприятие без отдельного аргумента.

---

## Этап 8. Синтез и открытая исследовательская платформа

**Цель:** собрать программу в понятный открытый продукт.

### Финальные артефакты

- единый Python package;
- CLI;
- интерактивный atlas;
- документация от интуитивного до математического уровня;
- воспроизводимые notebooks;
- versioned datasets;
- experiment manifests;
- technical report;
- открытая презентация;
- портфолио-кейс;
- архивированный release с DOI;
- список подтверждённых, опровергнутых и открытых вопросов.

### Точка публикации P8

**Living research atlas:** сайт, на котором любой пользователь может:

- выбрать \(n,m\) и структуру;
- проверить exact counts;
- собрать FBT-модель;
- сравнить стратегии;
- запустить малую популяцию;
- увидеть structural metrics;
- воспроизвести опубликованный график.

---

# 8. Карта постепенных публикаций

| Точка | Тип | Минимальное содержимое | Независимая ценность |
|---|---|---|---|
| **P0** | Методологическая заметка | AI-first research protocol, templates, CI | Воспроизводимость AI-generated science |
| **P1** | Research note + demo | Orders и cyclic groups | Точный математический визуализатор |
| **P2** | Reproduction note | FBT numerical appendix | Исполняемое дополнение к статье |
| **P3** | Computational companion | Все четыре FFF structures | Полная открытая реализация |
| **P4** | Dataset + explorer | Finite FBT atlas | Новая карта конечных моделей |
| **P5** | Benchmark report | Evolutionary dynamics | Проверка перехода payoff → fixation |
| **P6** | Preprint | Fitness–Structure Atlas | Основной самостоятельный вклад |
| **P7** | ML report + demo | Learned representations и OOD | Главный AI/ML-портфолио результат |
| **P8** | Living platform | Объединённый инструмент | Долгосрочный открытый ресурс |

Каждая публикация должна ссылаться на конкретный release tag, dataset version и experiment manifest.

---

## 9. Правила, предотвращающие разрастание проекта

1. На каждом этапе существует **один обязательный core question**.
2. Новая идея попадает в `backlog/extensions.md`, а не в текущий sprint.
3. ML не начинается до прохождения exact gates.
4. UI не переписывается, пока математическое API нестабильно.
5. В один release входит не более одного нового семейства assumptions.
6. Незавершённый модуль не маскируется общим названием «поддержка теоремы».
7. Ни один график не считается результатом без machine-readable data.
8. Если два независимых агента не согласны с формализацией, статус задачи — `BLOCKED: AMBIGUOUS`, а не «выбрать более удобную версию».

---

## 10. Stop/repair criteria

Работа по ветке останавливается и возвращается к спецификации, если:

- brute-force oracle и formula расходятся;
- exact arithmetic и floating-point implementation дают разные решения вне объявленной tolerance;
- результат меняется от произвольного tie-breaking;
- reviewer находит counterexample к заявленному инварианту;
- experiment config нельзя восстановить;
- преимущество агента исчезает после выравнивания compute/parameter budget;
- основной вывод зависит только от вручную назначенной стоимости truth;
- график нельзя построить из сохранённых raw artifacts;
- интерпретация шире, чем domain проверенной модели.

---

## 11. Стандарт воспроизводимости

Для каждого release обязательны:

- зафиксированные зависимости;
- одна команда установки;
- одна команда запуска tests;
- одна команда воспроизведения figures;
- фиксированные и записанные seeds;
- CPU reference implementation;
- GPU implementation только как оптимизация;
- exact small-case oracle;
- raw и derived data отдельно;
- commit hash в каждом result manifest;
- machine-readable assumptions;
- CI из чистого окружения;
- лицензия на код и данные;
- `CITATION.cff`;
- changelog научных, а не только программных изменений.

---

## 12. Definition of Done для всей программы

Проект считается зрелым, когда:

1. опубликованные FBT numerical calculations воспроизводятся exact arithmetic;
2. четыре FFF theorem families имеют вычислительные companions;
3. finite FBT atlas открыт и версионирован;
4. минимум две evolutionary dynamics реализации согласуются в контрольных режимах;
5. structural metrics проверены на synthetic ground truth;
6. проведён минимум один контролируемый ML/OOD эксперимент;
7. опубликованы как поддерживающие, так и ограничивающие результаты;
8. любой ключевой график воспроизводится из release;
9. каждое крупное утверждение имеет статус R/C/E/A;
10. человек может объяснить вывод простыми словами, не полагаясь на авторитет ИИ.

---

## 13. Основные источники

### Научные работы

- Prakash, Stephens, Hoffman, Singh & Fields. [Fitness Beats Truth in the Evolution of Perception](https://doi.org/10.1007/s10441-020-09400-0).
- Prakash, Fields, Hoffman, Prentner & Singh. [Fact, Fiction, and Fitness](https://doi.org/10.3390/e22050514).
- Hoffman, Singh & Prakash. [The Interface Theory of Perception](https://doi.org/10.3758/s13423-015-0890-8).
- Hoffman & Prakash. [Objects of Consciousness](https://doi.org/10.3389/fpsyg.2014.00577).

### Организация работы с Codex

- OpenAI. [Codex](https://openai.com/codex/).
- OpenAI Developers. [Codex documentation](https://developers.openai.com/codex/).
- OpenAI Developers. [Worktrees](https://developers.openai.com/codex/app/worktrees).
- OpenAI Developers. [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md).
- OpenAI Developers. [Codex best practices](https://developers.openai.com/codex/learn/best-practices).
- OpenAI Developers. [Subagents](https://developers.openai.com/codex/concepts/subagents).
- OpenAI Developers. [Code review](https://developers.openai.com/codex/app/review).
