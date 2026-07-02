# ТЗ на независимое review: TASK-004-FBT-ATLAS-V1 bundle

## Идентификатор

Ожидаемый review report: `REV-TASK-004-FBT-ATLAS-V1-001`.

Проверяемый bundle:

- `TASK-004-FBT-ATLAS-V1-SPEC`
- `TASK-004-FBT-ATLAS-V1-ENGINE`
- `TASK-004-FBT-ATLAS-V1-AGGREGATE`

Эпистемический статус: `E` — проектное расширение, не reproduction исходной
теоремы.

## Роль reviewer

Вы независимый verifier. Не предполагайте, что реализация верна. Проверяйте source
boundary, спецификацию, код, тесты, raw artifacts, derived reports и manifests как
аудитор. Не исправляйте код в рамках review.

## Главный вопрос review

Корректно ли v1 bundle реализует ограниченный pipeline:

```text
draft config -> exact raw-cell engine -> manifest-backed raw-cell JSON
             -> aggregate/report layer reading that raw JSON
             -> manifest-backed derived JSON/Markdown summary
```

и не превращает ли этот pipeline в:

- full finite atlas run;
- реализацию Theorem 4;
- source-level theorem result;
- биологический, метафизический, ML/RL, UI или figure claim.

## Обязательные файлы для чтения

Прочитайте минимум:

- `AGENTS.md`
- `01_research_strategy.md`
- `02_stage_tasks_roles.md`
- `docs/decisions/RDR-0004-stage4-fbt-blockers.md`
- `tasks/TASK-004_fbt_atlas_v1_spec.md`
- `tasks/TASK-004_fbt_atlas_v1_engine.md`
- `tasks/TASK-004_fbt_atlas_v1_aggregate.md`
- `specs/fbt/atlas_v1_design.md`
- `experiments/configs/fbt_atlas_v1_draft.json`
- `src/fts_lab/fbt/atlas_v1.py`
- `src/fts_lab/fbt/atlas_v1_aggregate.py`
- `tests/exact/test_fbt_atlas_v1_spec.py`
- `tests/exact/test_fbt_atlas_v1_engine.py`
- `tests/exact/test_fbt_atlas_v1_aggregate.py`
- `tests/integration/test_cli_and_smoke.py`
- `sources/source_map.md`
- `sources/claim_matrix.csv`
- `assumptions/register.md`

## Что проверить по существу

1. Source/spec boundary:
   - v1 корректно помечен как `E`, а не `R`;
   - `SRC-FBT-2021`, `CLM-FBT-ATLAS-001`, `ASM-FBT-0001..0004` связаны
     последовательно;
   - `CLM-FBT-THM-001` не повышен до implemented/reviewed theorem.

2. Draft config:
   - primary comparison остается `truth_map` vs `fitness_only_expected`;
   - extension baselines не входят в primary results;
   - arithmetic exact rational;
   - stochastic simulation, ML/RL, UI, notebooks, figures отключены;
   - denominator semantics сохраняют blocked/tie-sensitive cells.

3. Raw-cell engine:
   - engine читает `experiments/configs/fbt_atlas_v1_draft.json`;
   - axis count независимо пересчитывается как `2 * 2 * 3 * 4 * 3 * 1 = 144`;
   - cell IDs детерминированы и включают grid/version/axis/policy identity;
   - raw artifact содержит status per cell и не содержит aggregate summary;
   - zero-marginal observations не сглаживаются epsilon;
   - MAP ties не скрываются lexical/random tie-break.

4. Aggregate/report layer:
   - команда принимает raw-cell artifact через `--raw-cells`;
   - aggregate JSON/Markdown считаются из `cells[*].status`;
   - aggregate module не импортирует raw-cell enumeration helpers и не пересчитывает
     hidden cells из config;
   - derived JSON не встраивает полную raw `cells` table;
   - status counts и `grid_frequency` можно независимо восстановить из raw JSON;
   - denominator basis — все raw cells, включая blocked/tie-sensitive.

5. Manifest discipline:
   - raw manifest имеет config как input и raw JSON как output;
   - aggregate manifest имеет raw JSON как input и derived JSON/Markdown как outputs;
   - checksums валидируются;
   - git state, dependency lock checksum, command, task IDs, claim IDs, source IDs,
     assumption IDs присутствуют.

6. Claim boundary:
   - README, CHANGELOG, source_map, claim_matrix не обещают full atlas, theorem
     implementation, biological/metaphysical result, ML/RL result, dashboard or figure;
   - allowed public claim ограничен pending-review v1 design/engine/raw/aggregate
     bundle.

## Команды для запуска

Используйте доступный Python/uv entrypoint. На Windows обычно подходит:

```powershell
py -m uv run fts doctor --release-check
py -m uv run pytest
py -m uv run ruff check .
py -m uv run ruff format --check .
py -m uv run mypy src
py -m uv run fts fbt atlas-v1-raw-cells
py -m uv run fts fbt atlas-v1-aggregate --raw-cells <path-to-fbt_atlas_v1_raw_cells.json>
py -m uv run fts validate-manifest <raw-manifest-path>
py -m uv run fts validate-manifest <aggregate-manifest-path>
```

Если `py -m uv` недоступен, используйте локальный `.venv`/`uv run` эквивалент и
зафиксируйте это в отчете.

## Минимальные независимые проверки данных

После raw run:

- подтвердить `raw_cell_count = 144`;
- пересчитать количество rows в `cells`;
- пересчитать status counts без импорта `src/fts_lab/fbt/atlas_v1.py`;
- проверить, что `blocked_zero_marginal = 45`;
- проверить, что `blocked_zero_marginal` frequency в aggregate равен `45/144 = 5/16`;
- проверить, что сумма всех exact `grid_frequency` равна `1`;
- проверить, что aggregate JSON и Markdown отражают те же status counts.

## Severity rubric

- `fatal`: результат невалиден как artifact pipeline; checksum/manifest нарушен;
  aggregate пересчитывает скрытые cells; есть theorem/full-atlas/биологический overclaim.
- `major`: существенная traceability ошибка; denominator policy нарушен; raw и
  aggregate расходятся; тесты пропускают важный edge case.
- `minor`: wording, документация, небольшая неполнота объяснения, не меняющая
  artifact validity и claim boundary.

## Требуемый формат verdict

В конце отчета укажите:

```text
verdict: accepted | accepted_with_minor_findings | changes_requested | rejected
fatal_findings: none | ...
major_findings: none | ...
minor_findings: none | ...
review_status_token: REV-TASK-004-FBT-ATLAS-V1-001_no_fatal_or_major
```

Если есть хотя бы один unresolved `fatal` или `major`, bundle нельзя считать
reviewed и нельзя повышать public claim status.
