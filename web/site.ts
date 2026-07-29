import "./site.css";

import { enhanceArtifactViewer } from "./artifact-viewer.ts";

function enhanceEquationExplanations(): void {
  const explanations = [
    ...document.querySelectorAll<HTMLDetailsElement>("details[data-equation-explanation]"),
  ];
  if (explanations.length === 0) return;
  const controls = new Map<string, HTMLButtonElement>();
  for (const button of document.querySelectorAll<HTMLButtonElement>("[data-equation-explain]")) {
    const fragment = button.dataset.equationExplain;
    if (fragment) controls.set(fragment, button);
  }

  function setOpen(details: HTMLDetailsElement, open: boolean): void {
    details.open = open;
    controls.get(details.id)?.setAttribute("aria-expanded", String(open));
  }

  function closeOthers(active: HTMLDetailsElement): void {
    for (const details of explanations) {
      if (details !== active) setOpen(details, false);
    }
  }

  function openFromFragment(): boolean {
    const fragment = decodeURIComponent(location.hash.slice(1));
    const details = explanations.find(({ id }) => id === fragment);
    if (details === undefined) {
      for (const candidate of explanations) setOpen(candidate, false);
      return false;
    }
    closeOthers(details);
    setOpen(details, true);
    return true;
  }

  for (const details of explanations) {
    const button = controls.get(details.id);
    if (button === undefined) continue;
    button.addEventListener("click", () => {
      if (details.open) {
        setOpen(details, false);
        if (location.hash === `#${details.id}`) {
          if (history.state?.equationExplanation === details.id) {
            history.back();
          } else {
            history.replaceState(null, "", `${location.pathname}${location.search}`);
          }
        }
        button.focus();
        return;
      }
      closeOthers(details);
      setOpen(details, true);
      history.pushState({ equationExplanation: details.id }, "", `#${details.id}`);
    });
  }

  window.addEventListener("popstate", openFromFragment);
  window.addEventListener("hashchange", openFromFragment);
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    const open = explanations.find((details) => details.open);
    if (open === undefined) return;
    event.preventDefault();
    const button = controls.get(open.id);
    setOpen(open, false);
    if (location.hash === `#${open.id}`) {
      if (history.state?.equationExplanation === open.id) {
        history.back();
      } else {
        history.replaceState(null, "", `${location.pathname}${location.search}`);
      }
    }
    button?.focus();
  });
  openFromFragment();
}

function enhanceEquationScrollCues(): void {
  const wrappers = [...document.querySelectorAll<HTMLElement>(".equation-math-scroll")];
  if (wrappers.length === 0) return;
  const update = (): void => {
    for (const wrapper of wrappers) {
      wrapper.parentElement?.classList.toggle(
        "has-scrollable-math",
        wrapper.scrollWidth > wrapper.clientWidth + 1,
      );
    }
  };
  void document.fonts.ready.then(update);
  window.addEventListener("resize", update);
  update();
}

function enhanceFootnoteEscape(): void {
  document.addEventListener(
    "keydown",
    (event) => {
      if (event.key !== "Escape") return;
      let closed = false;
      for (const reference of document.querySelectorAll<
        HTMLAnchorElement & { _tippy?: { hide(): void; state?: { isVisible: boolean } } }
      >('a[role="doc-noteref"]')) {
        if (reference._tippy?.state?.isVisible === true) {
          reference._tippy.hide();
          closed = true;
        }
      }
      if (closed) event.preventDefault();
    },
    true,
  );
}

document.documentElement.classList.add("rsi-enhanced");
enhanceArtifactViewer();
enhanceEquationExplanations();
enhanceEquationScrollCues();
enhanceFootnoteEscape();
window.dispatchEvent(new CustomEvent("rsi:ready"));
