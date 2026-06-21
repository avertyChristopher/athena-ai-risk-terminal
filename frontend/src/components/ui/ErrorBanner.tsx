type ErrorBannerProps = {
  title: string;
  message: string;
  retryLabel?: string;
  onRetry?: () => void;
};

export function ErrorBanner({
  title,
  message,
  retryLabel,
  onRetry,
}: ErrorBannerProps) {
  return (
    <div className="empty-state" role="alert">
      <strong>{title}</strong>
      <p>{message}</p>
      {onRetry && retryLabel ? (
        <button className="button button--secondary" type="button" onClick={onRetry}>
          {retryLabel}
        </button>
      ) : null}
    </div>
  );
}
