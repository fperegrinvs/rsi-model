import "./artifact-viewer.css";

import { enhanceArtifactViewer } from "./artifact-viewer.ts";

document.documentElement.classList.add("rsi-enhanced");
enhanceArtifactViewer();
window.dispatchEvent(new CustomEvent("rsi:ready"));
