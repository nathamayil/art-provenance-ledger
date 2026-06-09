export default function ArtistCard({ name, weight }) {
  return (
    <div className="artist-card">
      <div className="name">{name}</div>
      <div className="pct">{Math.round(weight * 100)}%</div>
    </div>
  );
}