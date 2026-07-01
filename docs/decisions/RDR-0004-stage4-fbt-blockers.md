# RDR-0004: Stage 4 FBT blocker policies

## Статус

APPROVED

Решение утверждено Human Principal Investigator 2026-07-01 после review
decision brief и явного согласия с рекомендациями.

## Цель

Закрыть четыре блокера Stage 4 до реализации atlas engine:

- `ASM-FBT-0001`: что делать при MAP tie;
- `ASM-FBT-0002`: что делать при zero-probability observation;
- `ASM-FBT-0003`: какая finite grid / measure semantics допустима;
- `ASM-FBT-0004`: какие truth strategies входят в primary comparison.

## Область решения

Связанные ID:

- `TASK-004-FBT-ATLAS-SPEC`;
- `SRC-FBT-2021`;
- `CLM-FBT-THM-001`;
- `CLM-FBT-ATLAS-001`;
- `ASM-FBT-0001`, `ASM-FBT-0002`, `ASM-FBT-0003`, `ASM-FBT-0004`.

Это решение нужно для будущей Stage 4 реализации. Оно не запускает atlas, не
создает результаты и не меняет статус claims на reviewed.

## Ключевой принцип

Stage 4 должен разделять:

- source-aligned comparison: `MAP Truth` vs `Fitness-only expected fitness`;
- project extension: `finite rational grid atlas`;
- theorem probability из `SRC-FBT-2021`;
- project grid frequencies из нашей конечной enumeration.

Если эти уровни смешать, результат будет выглядеть сильнее, чем фактически
разрешают источник и текущая реализация.

## ASM-FBT-0001: MAP tie handling

Проблема: источник использует MAP estimate для Truth strategy, но в конечной
сетке MAP может быть не единственным. Молчаливый tie-break может изменить
победителя сравнения.

Варианты:

1. **Lexicographic tie-break.** Просто и детерминированно, но результат зависит от
   именования world states.
2. **Random tie-break.** Похоже на поведенческую модель, но добавляет stochastic
   assumption и seed-dependence.
3. **Return full MAP set.** Не выбирает произвольного победителя; позволяет
   увидеть, где итог устойчив, а где зависит от tie policy.
4. **Block every tied cell.** Максимально осторожно, но может выбросить много
   информативных cases.

Рекомендуемое решение:

Использовать полный MAP set как primary exact behavior.

- Если все MAP maximizers дают один и тот же Truth decision / Truth fitness
  comparison, cell можно классифицировать как `determined`.
- Если разные MAP maximizers дают разные comparison outcomes, cell получает
  статус `map_tie_policy_sensitive`.
- Lexicographic и random tie-break не использовать в primary results; их можно
  добавить позже только как отдельно помеченную sensitivity analysis.

Последствия:

- Не появляется скрытый произвольный tie-break.
- Atlas сможет считать не только "blocked", но и "policy-sensitive" cases.
- Output schema станет немного сложнее: нужна запись MAP set и tie status.

Что это решение не означает:

- Это не утверждает, что источник ошибается.
- Это не говорит, что ties надо игнорировать.
- Это не превращает random tie-break в source strategy.
- Это не разрешает публиковать tied/policy-sensitive cases как строгую победу
  Fitness-only.

## ASM-FBT-0002: zero-probability observation

Проблема: если `P(x) = 0`, posterior `p(w | x)` не определен. Нормализация через
ноль создала бы искусственную информацию.

Варианты:

1. **Exception / blocked status.** Научно чисто, но дает blocked cells.
2. **Exclude by domain contract.** Не допускает такие offered observations в
   valid cell, но может скрыть, сколько таких cases было в сырой сетке.
3. **Smoothing epsilon.** Делает posterior определенным, но меняет модель и
   вводит новый параметр.
4. **Return undefined object and let caller decide.** Гибко, но опасно для
   агрегатов.

Рекомендуемое решение:

Не использовать smoothing. Observation-level result должен быть
`zero_marginal_undefined`, когда `P(x) = 0`.

- Если comparison требует такой observation, cell получает
  `blocked_zero_marginal`.
- Grid report должен отдельно показывать count таких observations/cells.
- Domain-prefiltered summaries допустимы только как secondary view и должны
  явно указывать denominator.

Последствия:

- Exact path остается source-faithful.
- Нет произвольного epsilon.
- Aggregates обязаны различать total grid cells, valid comparable cells и blocked
  cells.

Что это решение не означает:

- Это не значит, что zero-probability cases можно удалить из raw accounting.
- Это не запрещает будущую extension-модель со smoothing, но она должна быть
  отдельным E-claim и отдельной assumption.
- Это не делает posterior определенным там, где Bayes formula undefined.

## ASM-FBT-0003: finite grid / measure semantics

Проблема: theorem probability из `SRC-FBT-2021` не равна доле cells в нашей
finite rational grid. Выбор сетки может менять headline aggregate patterns.

Варианты:

1. **No aggregate frequency, only tables.** Самый осторожный путь, но плохо
   отвечает на atlas-вопросы.
2. **Fixed uniform finite grid.** Воспроизводимо и понятно, но grid-dependent.
3. **Several grid families with robustness report.** Лучше для sensitivity, но
   дороже и сложнее.
4. **Weighted grid / prior over models.** Может быть осмысленно позже, но требует
   отдельного научного обоснования.

Рекомендуемое решение:

Утвердить finite atlas semantics, а не claim о theorem probability:

- каждый atlas run должен указывать один frozen `grid_version`;
- внутри этого `grid_version` aggregate labels должны говорить
  `grid_frequency`, а не `probability`, если текст явно не уточняет
  "probability under this finite project grid";
- primary Stage 4 report может использовать fixed uniform count over enumerated
  cells;
- blocked/tie-sensitive cells должны оставаться в denominator accounting и
  показываться отдельно;
- точные численные grid parameters должны быть зафиксированы в config до
  первого run и не должны меняться после просмотра результатов.

Рекомендуемый первый implementation path:

- начать с одного small exact rational `grid_version`;
- показывать stratified counts по `|W|`, `|X|`, perceptual-map/kernel family,
  strategy family, tie policy и zero-marginal policy;
- отложить weighted grids и robustness grid families до момента, когда базовый
  exact atlas будет manifest-backed и reviewed.

Последствия:

- Мы сможем запускать atlas, не выдавая его за reproduction of Theorem 4
  probability.
- Читатели смогут точно воспроизвести, какая конечная universe была посчитана.
- Первый atlas будет project extension (`E`), а не доказательством source theorem.

Что это решение не означает:

- Это не утверждает, что finite grid samples biological reality.
- Это не доказывает source theorem.
- Это не позволяет переносить grid frequency за пределы frozen grid version.
- Это не разрешает менять grid after seeing results без exploratory labeling.

## ASM-FBT-0004: truth strategies in primary comparison

Проблема: source Truth strategy является MAP point estimate. Posterior sampling,
posterior mean и full-posterior decision могут быть полезными baselines, но это
не та же source Truth strategy.

Варианты:

1. **Source MAP Truth only in primary comparison.** Максимальная traceability к
   source, но меньше baseline diversity.
2. **Source MAP Truth primary; extension baselines separate.** Сохраняет source
   comparison и позволяет честно изучать альтернативы.
3. **Full-posterior decision as primary "strong truth" baseline.** Может быть
   интереснее как adversarial baseline, но это уже не source Truth.
4. **Aggregate all truth-like strategies together.** Удобно для таблиц, но
   смешивает R/E statuses и ломает claim boundary.

Рекомендуемое решение:

Primary Stage 4 comparison:

```text
truth_map
vs
fitness_only_expected
```

Разрешенные secondary extension baselines, если они показываются отдельно:

- `truth_posterior_sampling`;
- `truth_full_posterior_decision`;
- `truth_posterior_mean` только после утверждения metric/vector semantics on
  `W`;
- другие regret/decision variants только под новыми assumption IDs.

Последствия:

- `CLM-FBT-THM-001` остается привязанным к boundary source theorem.
- `CLM-FBT-ATLAS-001` может включать extension baselines, но только с отдельными
  labels и без overclaim про source strategy.
- Public tables не должны смешивать source MAP и extension baselines в один
  безымянный aggregate "Truth".

Что это решение не означает:

- Это не говорит, что MAP является best possible truth-like strategy.
- Это не запрещает stronger baselines later.
- Это не делает posterior sampling или full-posterior decision частью source
  theorem.
- Это не разрешает claim "Fitness beats every truth-like strategy".

## Решение человека

Human PI утверждает recommended combined decision as written:

| Assumption | Decision |
|---|---|
| `ASM-FBT-0001` | represent MAP ties as full MAP sets; classify tie-sensitive cells separately |
| `ASM-FBT-0002` | no smoothing; zero-marginal observations are undefined and block dependent comparisons |
| `ASM-FBT-0003` | use frozen finite grid versions and report `grid_frequency`, never source theorem probability |
| `ASM-FBT-0004` | primary comparison is `truth_map` vs `fitness_only_expected`; extension baselines are separate |

## После утверждения

Документационный follow-up после утверждения:

- update `assumptions/register.md` statuses for `ASM-FBT-0001..0004`;
- update `specs/fbt/theorem4_domain.md` and
  `specs/fbt/finite_atlas_design.md` with the approved policy IDs.

Следующий implementation PR должен:

- создать первый exact oracle / fixture task для Stage 4;
- держать все atlas outputs manifest-backed и labeled as extension, если только
  явно не реализован source reproduction target;
- отложить independent review до готовности Stage 4 spec+oracle+implementation
  bundle, если Human PI не запросит более раннее review.

## Когда пересматривать

Пересмотреть этот RDR, если:

- source re-reading покажет другой source tie policy;
- первый finite grid даст слишком много blocked/tie-sensitive cells для
  содержательного отчета;
- Stage 4 добавит action sets, metrics on `W`, weighted grids или evolutionary
  dynamics;
- будущий public release захочет поднять любой atlas result выше
  project-defined extension status.
