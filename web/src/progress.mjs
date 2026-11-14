export function saveSession(progress, setId, rating, date = new Date().toISOString()) {
  return { ...progress, sessions: [...progress.sessions, { setId, rating, date }] };
}
export function toggleReview(progress, id) {
  return { ...progress, review: progress.review.includes(id) ? progress.review.filter(x => x !== id) : [...progress.review, id] };
}
