# Token map — prototype to production

*Every token and component the prototype defines, and what it becomes in the real build. Written
2026-09-25. The prototype's names (`--gf-*`, `.gf-*`) are the production names: nothing is renamed,
so a developer can lift `tokens.css` as the design-token file.*

## Tokens

| Prototype token | Production | Note |
|---|---|---|
| `--gf-ground`, `--gf-surface`, `--gf-sunk` | `color.background.{page,surface,sunk}` | light and dark values as in `05-design.md` |
| `--gf-ink`, `--gf-text`, `--gf-muted` | `color.text.{strong,body,muted}` | contrast pairs gated |
| `--gf-line`, `--gf-line-strong` | `color.border.{subtle,strong}` | |
| `--gf-blue`, `--gf-blue-soft`, `--gf-on-blue` | `color.brand.{base,soft,on}` | Form Blue |
| `--gf-orange`, `--gf-orange-soft`, `--gf-orange-ink`, `--gf-on-orange` | `color.accent.{base,soft,text,on}` | Energy Orange |
| `--gf-draw`, `--gf-on-draw` | `color.result.draw.{base,on}` | W uses brand, L uses accent |
| `--gf-band`, `--gf-on-band`, `--gf-band-muted` | `color.band.{base,text,muted}` | the same in both themes |
| `--gf-focus` | `color.focus` | 3 px outline |
| `--gf-font` | `font.family.base` (Archivo, self-hosted) | ADR-05 |
| `--gf-condensed` (72%), 85%, `--gf-wide` (100%) | `font.width.{display,headline,ui}` | the `wdth` axis |
| `--gf-radius`, `--gf-radius-sm`, `--gf-radius-pill` | `radius.{md,sm,pill}` | |
| `--gf-space` (8 px), `--gf-max` (1240 px), `--gf-tap` (44 px), `--gf-header` (60 px) | `space.base`, `layout.max`, `size.tap-min`, `size.header` | |
| `--gf-shadow` | `shadow.card` | |

## Components

| Prototype class | Production component | Data |
|---|---|---|
| `.gf-header`, `.gf-nav`, `.gf-tabbar`, `.gf-sheet` | Header, Nav, TabBar, MoreSheet | nav config |
| `.gf-strip`, `.gf-chip-match` | ScoreStrip (a live island in M3) | latest round / live feed |
| `.gf-table` + `[data-views]` + `.gf-sort` | LeagueTable (views, sort, compact mode) | table rows |
| `.gf-form` | FormGuide | last five results |
| `.gf-stat`, `.gf-stats-row` | StatTile | aggregate |
| `.gf-story-card`, `.gf-lead-story`, `.gf-list-item`, `.gf-cover` | StoryCard, LeadStory, StoryListItem, DataCover | article + cover spec |
| `.gf-snap` | LeagueSnapshot | top rows |
| `.gf-figure`, `.gf-bars`, `.gf-stack`, `.gf-cols`, `.gf-line`, `.gf-data` | ChartFigure with Bar, StackedBar, Column, Line and DataTable variants | chart spec |
| `.gf-results` | ResultsList | matches |
| `.gf-bracket`, `.gf-tie`, `.gf-groups` | Bracket, Tie, GroupTables | knock-out tree, groups |
| `.gf-matchhead`, `.gf-timeline`, `.gf-lineups` | MatchHeader, EventTimeline (a `role="log"` live island in M3), Lineups | match |
| `.gf-label` (+ `--explainer`, `--automated`, `--data`) | ContentLabel | article kind |
| `.gf-inert` | UnavailablePanel (disappears when the data exists) | — |
| `.gf-band`, `.gf-signup` | Band, NewsletterSignup | — |
| `.gf-topicbar` | TopicBar | topics config |
| `.gf-cardmeta`, `.gf-topiclink` | ArticleMeta (topic · kind) | article |
| `.gf-latest` | LatestList | recent articles |
| `.gf-topic-grid`, `.gf-topic-tile` | TopicGrid, TopicTile | topic + article count |
| `.gf-promise` | SourcingPromise | the house rules |
| `.gf-toc-box`, `.gf-seg-block` | ArticleContents, ArticleSegment | segments |
| `.gf-sources`, `.gf-source-list[data-sources]` | SourceLists (used / investigated) | sources |
| `.gf-later` | LaterPhaseNotice | — |
| `.proto-banner` | removed at M1 | — |
