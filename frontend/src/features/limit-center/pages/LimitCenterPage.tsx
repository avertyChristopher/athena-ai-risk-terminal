import { FormEvent, useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { AthenaAICommentaryCard } from "../../../components/ai/AthenaAICommentaryCard";
import { PageHeader } from "../../../components/layout/PageHeader";
import { EmptyState } from "../../../components/ui/EmptyState";
import { ErrorBanner } from "../../../components/ui/ErrorBanner";
import { LoadingState } from "../../../components/ui/LoadingState";
import { StatusBadge } from "../../../components/ui/StatusBadge";
import { PortfolioSelector } from "../../../components/workflow/PortfolioSelector";
import { usePortfolioContext } from "../../../context/PortfolioContext";
import { useTranslation } from "../../../hooks/useTranslation";
import { limitCenterApi } from "../../../services/limitCenterApi";
import type {
  BreachStatus,
  ComparisonOperator,
  LimitBreach,
  LimitCategory,
  LimitEvaluationRequest,
  LimitEvaluationResponse,
  LimitRule,
  LimitRuleCreate,
  LimitRuleUpdate,
  LimitSeverity,
  LimitSourceModule,
  OverallLimitStatus,
  ReviewAction,
  SourceModuleCard,
} from "../../../types/limit-center";

type LimitTab =
  | "overview"
  | "rules"
  | "breaches"
  | "workflow"
  | "sources"
  | "severity"
  | "methodology"
  | "commentary";

const tabs: LimitTab[] = [
  "overview",
  "rules",
  "breaches",
  "workflow",
  "sources",
  "severity",
  "methodology",
  "commentary",
];

const sourceModules: LimitSourceModule[] = [
  "portfolio_builder",
  "risk_monitor",
  "volatility_lab",
  "options_pricing_lab",
  "rates_lab",
  "stress_testing",
  "trade_simulator",
];

const categories: LimitCategory[] = [
  "portfolio",
  "risk",
  "stress",
  "fixed_income",
  "options",
  "trade",
];

const operators: ComparisonOperator[] = [
  "greater_than",
  "greater_than_or_equal",
  "less_than",
  "less_than_or_equal",
  "equal",
  "not_equal",
];

const severities: LimitSeverity[] = ["low", "medium", "high", "critical"];
const breachStatuses: BreachStatus[] = [
  "open",
  "under_review",
  "approved_exception",
  "rejected",
  "resolved",
];

const defaultRuleForm: LimitRuleCreate = {
  rule_id: "",
  name: "",
  category: "portfolio",
  metric_key: "single_position_weight",
  limit_value: 0.25,
  comparison_operator: "greater_than",
  severity_if_breached: "medium",
  enabled: true,
  description: "User-defined risk governance limit.",
  source_modules: ["portfolio_builder"],
  methodology: "User-defined rule evaluated against structured module payloads.",
};

export function LimitCenterPage() {
  const { t, i18n } = useTranslation();
  const queryClient = useQueryClient();
  const { selectedPortfolioId, selectedPortfolioName } = usePortfolioContext();
  const [activeTab, setActiveTab] = useState<LimitTab>("overview");
  const [sourceModule, setSourceModule] = useState<LimitSourceModule>("risk_monitor");
  const [selectedBreachId, setSelectedBreachId] = useState("");
  const [severityFilter, setSeverityFilter] = useState<LimitSeverity | "all">("all");
  const [statusFilter, setStatusFilter] = useState<BreachStatus | "all">("all");
  const [sourceFilter, setSourceFilter] = useState<LimitSourceModule | "all">("all");
  const [reviewNote, setReviewNote] = useState("");
  const [ruleForm, setRuleForm] = useState<LimitRuleCreate>(defaultRuleForm);
  const [editingRuleId, setEditingRuleId] = useState<string | null>(null);
  const [latestEvaluation, setLatestEvaluation] =
    useState<LimitEvaluationResponse | null>(null);
  const language = i18n.resolvedLanguage?.startsWith("fr") ? "fr" : "en";
  const portfolioId = selectedPortfolioId || "pf_001";

  const statusQuery = useQuery({
    queryKey: ["limit-center-status"],
    queryFn: limitCenterApi.status,
  });
  const rulesQuery = useQuery({
    queryKey: ["limit-center-rules"],
    queryFn: limitCenterApi.rules,
  });
  const breachesQuery = useQuery({
    queryKey: ["limit-center-breaches"],
    queryFn: limitCenterApi.breaches,
  });
  const sourceModulesQuery = useQuery({
    queryKey: ["limit-center-source-modules"],
    queryFn: limitCenterApi.sourceModules,
  });
  const demoQuery = useQuery({
    queryKey: ["limit-center-demo"],
    queryFn: limitCenterApi.demo,
  });

  const evaluation = latestEvaluation ?? demoQuery.data ?? null;
  const breachList = breachesQuery.data?.breaches ?? evaluation?.breaches ?? [];
  const filteredBreaches = useMemo(
    () =>
      breachList.filter((breach) => {
        const severityMatches =
          severityFilter === "all" || breach.severity === severityFilter;
        const statusMatches = statusFilter === "all" || breach.status === statusFilter;
        const sourceMatches =
          sourceFilter === "all" || breach.source_module === sourceFilter;
        return severityMatches && statusMatches && sourceMatches;
      }),
    [breachList, severityFilter, sourceFilter, statusFilter],
  );
  const selectedBreach =
    breachList.find((breach) => breach.breach_id === selectedBreachId) ??
    filteredBreaches[0] ??
    null;

  const evaluateMutation = useMutation({
    mutationFn: (payload: LimitEvaluationRequest) => limitCenterApi.evaluate(payload),
    onSuccess: (data) => {
      setLatestEvaluation(data);
      void queryClient.invalidateQueries({ queryKey: ["limit-center-breaches"] });
      if (data.breaches[0]) setSelectedBreachId(data.breaches[0].breach_id);
    },
  });
  const createRuleMutation = useMutation({
    mutationFn: (payload: LimitRuleCreate) => limitCenterApi.createRule(payload),
    onSuccess: () => {
      setRuleForm(defaultRuleForm);
      setEditingRuleId(null);
      void queryClient.invalidateQueries({ queryKey: ["limit-center-rules"] });
    },
  });
  const updateRuleMutation = useMutation({
    mutationFn: ({ ruleId, payload }: { ruleId: string; payload: LimitRuleUpdate }) =>
      limitCenterApi.updateRule(ruleId, payload),
    onSuccess: () => {
      setRuleForm(defaultRuleForm);
      setEditingRuleId(null);
      void queryClient.invalidateQueries({ queryKey: ["limit-center-rules"] });
    },
  });
  const deleteRuleMutation = useMutation({
    mutationFn: (ruleId: string) => limitCenterApi.deleteRule(ruleId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["limit-center-rules"] });
    },
  });
  const reviewMutation = useMutation({
    mutationFn: ({ breachId, action }: { breachId: string; action: ReviewAction }) =>
      limitCenterApi.reviewBreach(breachId, {
        action,
        reviewer: "athena.risk.manager",
        note: reviewNote || null,
      }),
    onSuccess: (data) => {
      setReviewNote("");
      setSelectedBreachId(data.breach.breach_id);
      void queryClient.invalidateQueries({ queryKey: ["limit-center-breaches"] });
    },
  });

  function handleEvaluate() {
    evaluateMutation.mutate({
      portfolio_id: portfolioId,
      source_module: sourceModule,
      payload: demoPayloadForSource(sourceModule, portfolioId),
      language,
    });
  }

  function handleRuleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const payload = {
      ...ruleForm,
      rule_id: ruleForm.rule_id || undefined,
    };
    if (editingRuleId) {
      const { rule_id: _ruleId, ...updatePayload } = payload;
      updateRuleMutation.mutate({
        ruleId: editingRuleId,
        payload: updatePayload,
      });
    } else {
      createRuleMutation.mutate(payload);
    }
  }

  function editRule(rule: LimitRule) {
    setEditingRuleId(rule.rule_id);
    setRuleForm({
      rule_id: rule.rule_id,
      name: rule.name,
      category: rule.category,
      metric_key: rule.metric_key,
      limit_value: rule.limit_value,
      comparison_operator: rule.comparison_operator,
      severity_if_breached: rule.severity_if_breached,
      enabled: rule.enabled,
      description: rule.description,
      source_modules: rule.source_modules,
      methodology: rule.methodology,
    });
    setActiveTab("rules");
  }

  const rules = rulesQuery.data?.rules ?? [];
  const activeRules = rulesQuery.data?.active_rules ?? statusQuery.data?.active_rules ?? 0;
  const openBreaches = breachesQuery.data?.open_breaches ?? evaluation?.summary.open_breach_count ?? 0;
  const criticalBreaches =
    breachesQuery.data?.critical_breaches ?? evaluation?.summary.critical_breach_count ?? 0;
  const approvedExceptions = breachesQuery.data?.approved_exceptions ?? 0;
  const resolvedBreaches = breachesQuery.data?.resolved_breaches ?? 0;
  const highestSeverity = highestSeverityFromBreaches(breachList) ?? evaluation?.highest_severity ?? null;

  return (
    <div className="page limit-center-page">
      <PageHeader
        title={t("limitCenter.title")}
        subtitle={t("limitCenter.subtitle")}
      />

      <div className="limit-center-command-panel">
        <PortfolioSelector compact showDetails={false} />
        <section className="card limit-center-control-card">
          <div className="section-heading">
            <div>
              <span className="equity-kicker">{t("limitCenter.controls.title")}</span>
              <h2>{t("limitCenter.controls.evaluateTitle")}</h2>
            </div>
            <StatusBadge
              label={statusQuery.data?.status ?? t("common.loading")}
              variant={statusQuery.data?.status === "ready" ? "success" : "warning"}
            />
          </div>
          <label className="form-field">
            <span>{t("limitCenter.sourceModule")}</span>
            <select
              value={sourceModule}
              onChange={(event) => setSourceModule(event.target.value as LimitSourceModule)}
            >
              {sourceModules.map((source) => (
                <option key={source} value={source}>
                  {moduleLabel(source, t)}
                </option>
              ))}
            </select>
          </label>
          <div className="workflow-actions">
            <button
              className="button button--primary"
              type="button"
              onClick={handleEvaluate}
            >
              {evaluateMutation.isPending
                ? t("common.loading")
                : t("limitCenter.evaluateLimits")}
            </button>
            <button
              className="button button--ghost"
              type="button"
              onClick={() => void breachesQuery.refetch()}
            >
              {t("limitCenter.refreshBreaches")}
            </button>
          </div>
        </section>
      </div>

      {evaluateMutation.isError ? (
        <ErrorBanner
          title={t("limitCenter.errors.evaluateTitle")}
          message={t("limitCenter.errors.evaluateMessage")}
        />
      ) : null}

      <section className="risk-monitor-kpi-grid">
        <KpiCard title={t("limitCenter.totalRules")} value={rules.length} />
        <KpiCard title={t("limitCenter.activeRules")} value={activeRules} tone="positive" />
        <KpiCard title={t("limitCenter.openBreaches")} value={openBreaches} tone={openBreaches ? "warning" : "positive"} />
        <KpiCard title={t("limitCenter.criticalBreaches")} value={criticalBreaches} tone={criticalBreaches ? "negative" : "positive"} />
        <KpiCard title={t("limitCenter.highestSeverity")} value={highestSeverity ? severityLabel(highestSeverity, t) : t("limitCenter.none")} tone={highestSeverityTone(highestSeverity)} />
        <KpiCard title={t("limitCenter.modulesConnected")} value={sourceModulesQuery.data?.length ?? sourceModules.length} />
        <KpiCard title={t("limitCenter.approvedExceptions")} value={approvedExceptions} />
        <KpiCard title={t("limitCenter.resolvedBreaches")} value={resolvedBreaches} tone="positive" />
      </section>

      <nav className="risk-monitor-tabs limit-center-tabs" aria-label={t("limitCenter.tabsLabel")}>
        {tabs.map((tab) => (
          <button
            key={tab}
            className={`risk-monitor-tab ${activeTab === tab ? "risk-monitor-tab--active" : ""}`}
            type="button"
            onClick={() => setActiveTab(tab)}
          >
            <span>{t(`limitCenter.tabs.${tab}`)}</span>
            <small>{t(`limitCenter.tabs.${tab}Short`)}</small>
          </button>
        ))}
      </nav>

      <div className="risk-monitor-panel">
        {activeTab === "overview" ? (
          <OverviewTab
            evaluation={evaluation}
            portfolioName={selectedPortfolioName || "Athena Demo Portfolio"}
            t={t}
          />
        ) : null}
        {activeTab === "rules" ? (
          <RulesTab
            editingRuleId={editingRuleId}
            form={ruleForm}
            isSaving={createRuleMutation.isPending || updateRuleMutation.isPending}
            rules={rules}
            setEditingRuleId={setEditingRuleId}
            setForm={setRuleForm}
            onDelete={(ruleId) => deleteRuleMutation.mutate(ruleId)}
            onEdit={editRule}
            onSubmit={handleRuleSubmit}
            onToggle={(rule) =>
              updateRuleMutation.mutate({
                ruleId: rule.rule_id,
                payload: { enabled: !rule.enabled },
              })
            }
            t={t}
          />
        ) : null}
        {activeTab === "breaches" ? (
          <BreachRegisterTab
            breaches={filteredBreaches}
            selectedBreachId={selectedBreach?.breach_id ?? ""}
            severityFilter={severityFilter}
            sourceFilter={sourceFilter}
            statusFilter={statusFilter}
            setSelectedBreachId={setSelectedBreachId}
            setSeverityFilter={setSeverityFilter}
            setSourceFilter={setSourceFilter}
            setStatusFilter={setStatusFilter}
            t={t}
          />
        ) : null}
        {activeTab === "workflow" ? (
          <ReviewWorkflowTab
            breach={selectedBreach}
            note={reviewNote}
            isReviewing={reviewMutation.isPending}
            setNote={setReviewNote}
            onReview={(action) => {
              if (selectedBreach) {
                reviewMutation.mutate({ breachId: selectedBreach.breach_id, action });
              }
            }}
            t={t}
          />
        ) : null}
        {activeTab === "sources" ? (
          <SourceModulesTab modules={sourceModulesQuery.data ?? []} t={t} />
        ) : null}
        {activeTab === "severity" ? <SeverityGovernanceTab t={t} /> : null}
        {activeTab === "methodology" ? (
          <MethodologyTab evaluation={evaluation} t={t} />
        ) : null}
        {activeTab === "commentary" ? (
          <AthenaAICommentaryCard commentary={evaluation?.athena_ai_commentary} />
        ) : null}
      </div>
    </div>
  );
}

function OverviewTab({
  evaluation,
  portfolioName,
  t,
}: {
  evaluation: LimitEvaluationResponse | null;
  portfolioName: string;
  t: Translator;
}) {
  if (!evaluation) {
    return <LoadingState label={t("common.loading")} />;
  }
  const topBreaches = evaluation.breaches.slice(0, 5);
  return (
    <div className="risk-monitor-stack">
      <AthenaAICommentaryCard commentary={evaluation.athena_ai_commentary} />
      <section className="card risk-monitor-section-card">
        <div className="risk-monitor-section-card__header">
          <div>
            <h2>{t("limitCenter.overview.title")}</h2>
            <p>{t("limitCenter.overview.description")}</p>
          </div>
          <StatusBadge
            label={overallStatusLabel(evaluation.overall_status, t)}
            variant={overallStatusVariant(evaluation.overall_status)}
          />
        </div>
        <div className="risk-monitor-overview-grid">
          <div className="risk-monitor-driver-list">
            <h3>{t("limitCenter.selectedPortfolio")}</h3>
            <p>{portfolioName}</p>
            <p>{evaluation.portfolio_id}</p>
          </div>
          <div className="risk-monitor-driver-list">
            <h3>{t("limitCenter.overview.summary")}</h3>
            <p>
              {evaluation.summary.breach_count} {t("limitCenter.breachesLower")} /{" "}
              {evaluation.summary.evaluated_rule_count} {t("limitCenter.rulesLower")}
            </p>
            <p>
              {t("limitCenter.highestSeverity")}:{" "}
              {evaluation.highest_severity
                ? severityLabel(evaluation.highest_severity, t)
                : t("limitCenter.none")}
            </p>
          </div>
        </div>
        {topBreaches.length ? (
          <div className="limit-center-breach-strip">
            {topBreaches.map((breach) => (
              <article key={breach.breach_id}>
                <StatusBadge
                  label={severityLabel(breach.severity, t)}
                  variant={severityVariant(breach.severity)}
                />
                <strong>{breach.rule_name}</strong>
                <span>{moduleLabel(breach.source_module, t)}</span>
              </article>
            ))}
          </div>
        ) : (
          <EmptyState
            title={t("limitCenter.noBreachesTitle")}
            message={t("limitCenter.noBreachesMessage")}
          />
        )}
      </section>
    </div>
  );
}

function RulesTab({
  editingRuleId,
  form,
  isSaving,
  rules,
  setEditingRuleId,
  setForm,
  onDelete,
  onEdit,
  onSubmit,
  onToggle,
  t,
}: {
  editingRuleId: string | null;
  form: LimitRuleCreate;
  isSaving: boolean;
  rules: LimitRule[];
  setEditingRuleId: (ruleId: string | null) => void;
  setForm: (form: LimitRuleCreate) => void;
  onDelete: (ruleId: string) => void;
  onEdit: (rule: LimitRule) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  onToggle: (rule: LimitRule) => void;
  t: Translator;
}) {
  return (
    <div className="risk-monitor-stack">
      <section className="card risk-monitor-section-card">
        <div className="risk-monitor-section-card__header">
          <div>
            <h2>{t("limitCenter.rulesLibrary")}</h2>
            <p>{t("limitCenter.rules.description")}</p>
          </div>
          <StatusBadge
            label={editingRuleId ? t("limitCenter.rules.editing") : t("limitCenter.rules.create")}
            variant="info"
          />
        </div>
        <form className="limit-center-rule-form" onSubmit={onSubmit}>
          <label className="form-field">
            <span>{t("limitCenter.ruleId")}</span>
            <input
              disabled={Boolean(editingRuleId)}
              value={form.rule_id ?? ""}
              onChange={(event) => setForm({ ...form, rule_id: event.target.value })}
            />
          </label>
          <label className="form-field">
            <span>{t("limitCenter.ruleName")}</span>
            <input
              required
              value={form.name}
              onChange={(event) => setForm({ ...form, name: event.target.value })}
            />
          </label>
          <label className="form-field">
            <span>{t("limitCenter.category")}</span>
            <select
              value={form.category}
              onChange={(event) =>
                setForm({ ...form, category: event.target.value as LimitCategory })
              }
            >
              {categories.map((category) => (
                <option key={category} value={category}>
                  {categoryLabel(category, t)}
                </option>
              ))}
            </select>
          </label>
          <label className="form-field">
            <span>{t("limitCenter.metric")}</span>
            <input
              required
              value={form.metric_key}
              onChange={(event) => setForm({ ...form, metric_key: event.target.value })}
            />
          </label>
          <label className="form-field">
            <span>{t("limitCenter.operator")}</span>
            <select
              value={form.comparison_operator}
              onChange={(event) =>
                setForm({
                  ...form,
                  comparison_operator: event.target.value as ComparisonOperator,
                })
              }
            >
              {operators.map((operator) => (
                <option key={operator} value={operator}>
                  {operatorLabel(operator, t)}
                </option>
              ))}
            </select>
          </label>
          <label className="form-field">
            <span>{t("limitCenter.limitValue")}</span>
            <input
              required
              type="number"
              step="0.01"
              value={Number(form.limit_value)}
              onChange={(event) =>
                setForm({ ...form, limit_value: Number(event.target.value) })
              }
            />
          </label>
          <label className="form-field">
            <span>{t("limitCenter.severity")}</span>
            <select
              value={form.severity_if_breached}
              onChange={(event) =>
                setForm({
                  ...form,
                  severity_if_breached: event.target.value as LimitSeverity,
                })
              }
            >
              {severities.map((severity) => (
                <option key={severity} value={severity}>
                  {severityLabel(severity, t)}
                </option>
              ))}
            </select>
          </label>
          <label className="form-field">
            <span>{t("limitCenter.sourceModule")}</span>
            <select
              value={form.source_modules[0] ?? "portfolio_builder"}
              onChange={(event) =>
                setForm({
                  ...form,
                  source_modules: [event.target.value as LimitSourceModule],
                })
              }
            >
              {sourceModules.map((source) => (
                <option key={source} value={source}>
                  {moduleLabel(source, t)}
                </option>
              ))}
            </select>
          </label>
          <label className="form-field limit-center-wide-field">
            <span>{t("limitCenter.description")}</span>
            <input
              value={form.description}
              onChange={(event) => setForm({ ...form, description: event.target.value })}
            />
          </label>
          <div className="workflow-actions limit-center-wide-field">
            <button className="button button--primary" type="submit">
              {isSaving ? t("common.loading") : t("limitCenter.rules.save")}
            </button>
            <button
              className="button button--ghost"
              type="button"
              onClick={() => {
                setEditingRuleId(null);
                setForm(defaultRuleForm);
              }}
            >
              {t("limitCenter.rules.reset")}
            </button>
          </div>
        </form>
      </section>
      <RulesTable
        rules={rules}
        onDelete={onDelete}
        onEdit={onEdit}
        onToggle={onToggle}
        t={t}
      />
    </div>
  );
}

function RulesTable({
  rules,
  onDelete,
  onEdit,
  onToggle,
  t,
}: {
  rules: LimitRule[];
  onDelete: (ruleId: string) => void;
  onEdit: (rule: LimitRule) => void;
  onToggle: (rule: LimitRule) => void;
  t: Translator;
}) {
  return (
    <section className="card risk-monitor-section-card">
      <div className="risk-monitor-section-card__header">
        <div>
          <h2>{t("limitCenter.rules.tableTitle")}</h2>
          <p>{t("limitCenter.rules.tableDescription")}</p>
        </div>
      </div>
      <div className="table-scroll">
        <table className="data-table risk-monitor-table limit-center-table">
          <thead>
            <tr>
              <th>{t("limitCenter.ruleName")}</th>
              <th>{t("limitCenter.category")}</th>
              <th>{t("limitCenter.metric")}</th>
              <th>{t("limitCenter.operator")}</th>
              <th>{t("limitCenter.limitValue")}</th>
              <th>{t("limitCenter.severity")}</th>
              <th>{t("limitCenter.enabled")}</th>
              <th>{t("limitCenter.sourceModule")}</th>
              <th>{t("limitCenter.actions")}</th>
            </tr>
          </thead>
          <tbody>
            {rules.map((rule) => (
              <tr key={rule.rule_id}>
                <td>{rule.name}</td>
                <td>{categoryLabel(rule.category, t)}</td>
                <td>{rule.metric_key}</td>
                <td>{operatorLabel(rule.comparison_operator, t)}</td>
                <td>{formatValue(rule.limit_value)}</td>
                <td>
                  <StatusBadge
                    label={severityLabel(rule.severity_if_breached, t)}
                    variant={severityVariant(rule.severity_if_breached)}
                  />
                </td>
                <td>{rule.enabled ? t("limitCenter.ruleEnabled") : t("limitCenter.ruleDisabled")}</td>
                <td>{rule.source_modules.map((source) => moduleLabel(source, t)).join(", ")}</td>
                <td>
                  <div className="limit-center-table-actions">
                    <button className="button button--compact" type="button" onClick={() => onEdit(rule)}>
                      {t("limitCenter.edit")}
                    </button>
                    <button className="button button--compact" type="button" onClick={() => onToggle(rule)}>
                      {rule.enabled ? t("limitCenter.disable") : t("limitCenter.enable")}
                    </button>
                    <button className="button button--compact button--danger" type="button" onClick={() => onDelete(rule.rule_id)}>
                      {t("limitCenter.delete")}
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function BreachRegisterTab({
  breaches,
  selectedBreachId,
  severityFilter,
  sourceFilter,
  statusFilter,
  setSelectedBreachId,
  setSeverityFilter,
  setSourceFilter,
  setStatusFilter,
  t,
}: {
  breaches: LimitBreach[];
  selectedBreachId: string;
  severityFilter: LimitSeverity | "all";
  sourceFilter: LimitSourceModule | "all";
  statusFilter: BreachStatus | "all";
  setSelectedBreachId: (breachId: string) => void;
  setSeverityFilter: (severity: LimitSeverity | "all") => void;
  setSourceFilter: (source: LimitSourceModule | "all") => void;
  setStatusFilter: (status: BreachStatus | "all") => void;
  t: Translator;
}) {
  return (
    <section className="card risk-monitor-section-card">
      <div className="risk-monitor-section-card__header">
        <div>
          <h2>{t("limitCenter.breachRegister")}</h2>
          <p>{t("limitCenter.breaches.description")}</p>
        </div>
      </div>
      <div className="limit-center-filter-grid">
        <FilterSelect
          label={t("limitCenter.severity")}
          value={severityFilter}
          options={["all", ...severities]}
          formatter={(value) => value === "all" ? t("limitCenter.all") : severityLabel(value as LimitSeverity, t)}
          onChange={(value) => setSeverityFilter(value as LimitSeverity | "all")}
        />
        <FilterSelect
          label={t("limitCenter.status")}
          value={statusFilter}
          options={["all", ...breachStatuses]}
          formatter={(value) => value === "all" ? t("limitCenter.all") : breachStatusLabel(value as BreachStatus, t)}
          onChange={(value) => setStatusFilter(value as BreachStatus | "all")}
        />
        <FilterSelect
          label={t("limitCenter.sourceModule")}
          value={sourceFilter}
          options={["all", ...sourceModules]}
          formatter={(value) => value === "all" ? t("limitCenter.all") : moduleLabel(value as LimitSourceModule, t)}
          onChange={(value) => setSourceFilter(value as LimitSourceModule | "all")}
        />
      </div>
      {breaches.length ? (
        <div className="table-scroll">
          <table className="data-table risk-monitor-table limit-center-table">
            <thead>
              <tr>
                <th>{t("limitCenter.breachId")}</th>
                <th>{t("limitCenter.ruleName")}</th>
                <th>{t("limitCenter.sourceModule")}</th>
                <th>{t("limitCenter.currentValue")}</th>
                <th>{t("limitCenter.limitValue")}</th>
                <th>{t("limitCenter.severity")}</th>
                <th>{t("limitCenter.status")}</th>
                <th>{t("limitCenter.createdAt")}</th>
              </tr>
            </thead>
            <tbody>
              {breaches.map((breach) => (
                <tr
                  className={breach.breach_id === selectedBreachId ? "limit-center-selected-row" : ""}
                  key={breach.breach_id}
                  onClick={() => setSelectedBreachId(breach.breach_id)}
                >
                  <td>{breach.breach_id}</td>
                  <td>{breach.rule_name}</td>
                  <td>{moduleLabel(breach.source_module, t)}</td>
                  <td>{formatValue(breach.current_value)}</td>
                  <td>{formatValue(breach.limit_value)}</td>
                  <td>
                    <StatusBadge label={severityLabel(breach.severity, t)} variant={severityVariant(breach.severity)} />
                  </td>
                  <td>
                    <StatusBadge label={breachStatusLabel(breach.status, t)} variant={breachStatusVariant(breach.status)} />
                  </td>
                  <td>{formatDate(breach.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <EmptyState title={t("limitCenter.noBreachesTitle")} message={t("limitCenter.noBreachesMessage")} />
      )}
    </section>
  );
}

function ReviewWorkflowTab({
  breach,
  note,
  isReviewing,
  setNote,
  onReview,
  t,
}: {
  breach: LimitBreach | null;
  note: string;
  isReviewing: boolean;
  setNote: (note: string) => void;
  onReview: (action: ReviewAction) => void;
  t: Translator;
}) {
  if (!breach) {
    return <EmptyState title={t("limitCenter.workflow.emptyTitle")} message={t("limitCenter.workflow.emptyMessage")} />;
  }
  const actions: ReviewAction[] = [
    "mark_under_review",
    "approve_exception",
    "reject",
    "resolve",
    "reopen",
  ];
  return (
    <section className="card risk-monitor-section-card">
      <div className="risk-monitor-section-card__header">
        <div>
          <h2>{t("limitCenter.reviewWorkflow")}</h2>
          <p>{breach.explanation}</p>
        </div>
        <StatusBadge label={breachStatusLabel(breach.status, t)} variant={breachStatusVariant(breach.status)} />
      </div>
      <div className="risk-monitor-overview-grid">
        <div className="risk-monitor-driver-list">
          <h3>{t("limitCenter.suggestedAction")}</h3>
          <p>{breach.suggested_action}</p>
          <p>{t("limitCenter.currentValue")}: {formatValue(breach.current_value)}</p>
          <p>{t("limitCenter.limitValue")}: {formatValue(breach.limit_value)}</p>
        </div>
        <div className="risk-monitor-driver-list">
          <h3>{t("limitCenter.reviewNote")}</h3>
          <label className="form-field">
            <span>{t("limitCenter.reviewNote")}</span>
            <input value={note} onChange={(event) => setNote(event.target.value)} />
          </label>
          <div className="workflow-actions">
            {actions.map((action) => (
              <button
                className="button button--compact"
                disabled={isReviewing}
                key={action}
                type="button"
                onClick={() => onReview(action)}
              >
                {reviewActionLabel(action, t)}
              </button>
            ))}
          </div>
        </div>
      </div>
      <div className="limit-center-review-history">
        {breach.review_history.length ? breach.review_history.map((event) => (
          <article key={`${event.timestamp}-${event.action}`}>
            <strong>{reviewActionLabel(event.action, t)}</strong>
            <span>{event.reviewer} - {formatDate(event.timestamp)}</span>
            <p>{event.note ?? event.decision}</p>
          </article>
        )) : <p className="risk-monitor-table-note">{t("limitCenter.workflow.noHistory")}</p>}
      </div>
    </section>
  );
}

function SourceModulesTab({
  modules,
  t,
}: {
  modules: SourceModuleCard[];
  t: Translator;
}) {
  return (
    <section className="card risk-monitor-section-card">
      <div className="risk-monitor-section-card__header">
        <div>
          <h2>{t("limitCenter.sourceModules")}</h2>
          <p>{t("limitCenter.sources.description")}</p>
        </div>
      </div>
      <div className="limit-center-source-grid">
        {modules.map((module) => (
          <article className="risk-monitor-driver-list" key={module.module}>
            <div className="section-heading">
              <h3>{module.display_name}</h3>
              <StatusBadge
                label={module.connected ? t("limitCenter.connected") : t("common.unavailable")}
                variant={module.connected ? "success" : "warning"}
              />
            </div>
            <p>{t("limitCenter.payloadAvailable")}: {module.payload_available ? t("common.yes") : t("common.no")}</p>
            <ul>
              {module.metrics_provided.map((metric) => (
                <li key={metric}>{metric}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
}

function SeverityGovernanceTab({ t }: { t: Translator }) {
  const rows: Array<[LimitSeverity, string]> = [
    ["low", t("limitCenter.governance.low")],
    ["medium", t("limitCenter.governance.medium")],
    ["high", t("limitCenter.governance.high")],
    ["critical", t("limitCenter.governance.critical")],
  ];
  return (
    <section className="card risk-monitor-section-card">
      <div className="risk-monitor-section-card__header">
        <div>
          <h2>{t("limitCenter.severityGovernance")}</h2>
          <p>{t("limitCenter.governance.description")}</p>
        </div>
      </div>
      <div className="risk-monitor-commentary-grid">
        {rows.map(([severity, description]) => (
          <article className="risk-monitor-driver-list" key={severity}>
            <StatusBadge label={severityLabel(severity, t)} variant={severityVariant(severity)} />
            <p>{description}</p>
          </article>
        ))}
      </div>
      <div className="risk-monitor-driver-list">
        <h3>{t("limitCenter.governance.cfaTitle")}</h3>
        <p>{t("limitCenter.governance.cfaNote")}</p>
      </div>
    </section>
  );
}

function MethodologyTab({
  evaluation,
  t,
}: {
  evaluation: LimitEvaluationResponse | null;
  t: Translator;
}) {
  return (
    <section className="card risk-monitor-section-card">
      <div className="risk-monitor-section-card__header">
        <div>
          <h2>{t("limitCenter.methodology.title")}</h2>
          <p>{t("limitCenter.methodology.description")}</p>
        </div>
        <StatusBadge label={t("athenaIntelligence.fallbackMode")} variant="warning" />
      </div>
      <div className="risk-monitor-commentary-grid">
        {[
          "demoPersistence",
          "ruleset",
          "payload",
          "fallback",
          "missingData",
          "notAdvice",
        ].map((key) => (
          <article className="risk-monitor-driver-list" key={key}>
            <h3>{t(`limitCenter.methodology.${key}Title`)}</h3>
            <p>{t(`limitCenter.methodology.${key}`)}</p>
          </article>
        ))}
      </div>
      {evaluation?.warnings.length ? (
        <div className="model-warning-list">
          {evaluation.warnings.slice(0, 8).map((warning) => (
            <p key={warning}>{warning}</p>
          ))}
        </div>
      ) : null}
    </section>
  );
}

function KpiCard({
  title,
  value,
  tone = "neutral",
}: {
  title: string;
  value: string | number;
  tone?: "neutral" | "positive" | "warning" | "negative";
}) {
  return (
    <article className={`risk-monitor-metric-card risk-monitor-metric-card--${tone}`}>
      <span>{title}</span>
      <strong>{value}</strong>
    </article>
  );
}

function FilterSelect({
  label,
  value,
  options,
  formatter,
  onChange,
}: {
  label: string;
  value: string;
  options: string[];
  formatter: (value: string) => string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="form-field">
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => (
          <option key={option} value={option}>
            {formatter(option)}
          </option>
        ))}
      </select>
    </label>
  );
}

function demoPayloadForSource(source: LimitSourceModule, portfolioId: string): Record<string, unknown> {
  if (source === "portfolio_builder") {
    return {
      portfolio_id: portfolioId,
      concentration: {
        largest_position: { name: "NVDA", weight: 0.31 },
        top_3_weight: 0.72,
        sector_exposures: [{ name: "Technology", weight: 0.64 }],
        cash_weight: 0.03,
      },
    };
  }
  if (source === "volatility_lab") {
    return {
      portfolio_id: portfolioId,
      volatility_summary: { annualized_volatility: 0.26 },
      var_models: { historical_var: 0.035, historical_cvar: 0.052 },
      benchmark_risk: { beta: 1.6 },
    };
  }
  if (source === "options_pricing_lab") {
    return {
      portfolio_id: portfolioId,
      risk_payload: { delta_adjusted_exposure: 125000, vega: 6100 },
      max_loss: { type: "unlimited", value: null },
    };
  }
  if (source === "rates_lab") {
    return {
      portfolio_id: portfolioId,
      modified_duration: 8.2,
      dv01: 65,
      estimated_rate_shock_loss: -8500,
      fixed_income_market_value: 100000,
    };
  }
  if (source === "stress_testing") {
    return {
      portfolio_id: portfolioId,
      percent_loss: 0.22,
      severity: { severity: "critical" },
    };
  }
  if (source === "trade_simulator") {
    return {
      portfolio_id: portfolioId,
      portfolio_value: 100000,
      trade_ticket: {
        gross_trade_value: 25000,
        estimated_cash_after_trade_weight: 0.02,
      },
      constraints_warnings: [
        { name: "Post-trade sector exposure", actual: 0.57 },
      ],
    };
  }
  return {
    portfolio_id: portfolioId,
    global_risk_score: 82,
    risk_metrics: [
      { name: "Portfolio volatility", value: 0.24 },
      { name: "VaR 95%", value: 0.038 },
      { name: "CVaR 95%", value: 0.055 },
    ],
  };
}

function highestSeverityFromBreaches(breaches: LimitBreach[]) {
  const rank: Record<LimitSeverity, number> = { low: 1, medium: 2, high: 3, critical: 4 };
  return breaches.reduce<LimitSeverity | null>(
    (highest, breach) =>
      !highest || rank[breach.severity] > rank[highest] ? breach.severity : highest,
    null,
  );
}

function highestSeverityTone(severity: LimitSeverity | null) {
  if (severity === "critical" || severity === "high") return "negative";
  if (severity === "medium") return "warning";
  return "positive";
}

function formatValue(value: number | boolean) {
  if (typeof value === "boolean") return value ? "Yes" : "No";
  if (Math.abs(value) <= 2) return `${(value * 100).toFixed(2)}%`;
  return value.toLocaleString(undefined, { maximumFractionDigits: 2 });
}

function formatDate(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}

function severityVariant(severity: LimitSeverity) {
  if (severity === "critical" || severity === "high") return "danger";
  if (severity === "medium") return "warning";
  return "info";
}

function breachStatusVariant(status: BreachStatus) {
  if (status === "approved_exception" || status === "resolved") return "success";
  if (status === "under_review") return "warning";
  if (status === "rejected") return "danger";
  return "info";
}

function overallStatusVariant(status: OverallLimitStatus) {
  if (status === "critical_breach" || status === "severe_breach") return "danger";
  if (status === "breached" || status === "watchlist") return "warning";
  return "success";
}

function moduleLabel(source: LimitSourceModule, t: Translator) {
  return t(`limitCenter.modules.${source}`);
}

function categoryLabel(category: LimitCategory, t: Translator) {
  return t(`limitCenter.categories.${category}`);
}

function severityLabel(severity: LimitSeverity, t: Translator) {
  return t(`limitCenter.severities.${severity}`);
}

function breachStatusLabel(status: BreachStatus, t: Translator) {
  return t(`limitCenter.statuses.${status}`);
}

function overallStatusLabel(status: OverallLimitStatus, t: Translator) {
  return t(`limitCenter.overallStatuses.${status}`);
}

function operatorLabel(operator: ComparisonOperator, t: Translator) {
  return t(`limitCenter.operators.${operator}`);
}

function reviewActionLabel(action: ReviewAction, t: Translator) {
  return t(`limitCenter.reviewActions.${action}`);
}

type Translator = (key: string) => string;
