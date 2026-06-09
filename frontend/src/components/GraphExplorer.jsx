import { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import axios from "axios";

const API = import.meta.env.VITE_API_BASE_URL;

const NODE_COLORS = {
  query:    "#FF6B6B",
  artist:   "#4ECDC4",
  movement: "#45B7D1"
};

export default function GraphExplorer({ imageId }) {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  useEffect(() => {
    if (!imageId) return;
    axios
      .get(`${API}/api/graph/${imageId}`)
      .then(({ data }) => setGraphData(data))
      .catch(console.error);
  }, [imageId]);

  return (
    <div className="graph-container">
      <ForceGraph2D
        graphData={graphData}
        nodeLabel="id"
        nodeColor={(node) => NODE_COLORS[node.type] || "#999"}
        nodeRelSize={8}
        linkWidth={(link) => (link.value || 0.5) * 4}
        linkColor={() => "#ffffff18"}
        backgroundColor="#13131f"
        width={860}
        height={420}
      />
    </div>
  );
}