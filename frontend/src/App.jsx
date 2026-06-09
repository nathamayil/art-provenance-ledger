import { useState } from "react";
import ImageUploader from "./components/ImageUploader";
import GraphExplorer from "./components/GraphExplorer";
import ArtistCard from "./components/ArtistCard";
import "./App.css";

export default function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="app">
      <header className="app-header">
        <h1>Art Provenance Ledger</h1>
        <p>Trace the stylistic DNA of any AI-generated image</p>
      </header>

      <ImageUploader onResult={setResult} />

      {result && (
        <>
          <section className="section">
            <h2>Top Artist Influences</h2>
            <div className="cards-row">
              {result.influence_summary.artists.map((a) => (
                <ArtistCard key={a.name} name={a.name} weight={a.weight} />
              ))}
            </div>
          </section>

          <section className="section">
            <h2>Art Movements</h2>
            {result.influence_summary.movements.map((m) => (
              <div key={m.name} className="movement-row">
                <span className="movement-name">{m.name}</span>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{ width: `${m.weight * 100}%` }}
                  />
                </div>
                <span className="movement-pct">
                  {Math.round(m.weight * 100)}%
                </span>
              </div>
            ))}
          </section>

          <section className="section">
            <h2>Influence Graph</h2>
            <GraphExplorer imageId={result.image_id} />
          </section>
        </>
      )}
    </div>
  );
}