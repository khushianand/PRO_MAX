"""Theme management for modern cybersecurity dashboard UI."""

from __future__ import annotations

THEMES = {
    "Dark": {
        "bg": "#1e1e2e",
        "panel": "#27293d",
        "primary": "#00c896",
        "secondary": "#3b82f6",
        "text": "#f5f5f5",
        "muted": "#9ca3af",
        "border": "#3a3d4d",
    },
    "Light": {
        "bg": "#ffffff",
        "panel": "#ffffff",
        "center": "#2563eb",
        "primary": "#2563eb",
        "secondary": "#2563eb",
        "text": "#1f2937",
        "muted": "#64748b",
        "border": "#dbeafe",
    },
    "Cybersecurity Neon": {
        "bg": "#0f172a",
        "panel": "#111827",
        "primary": "#22d3ee",
        "secondary": "#a78bfa",
        "text": "#e5e7eb",
        "muted": "#94a3b8",
        "border": "#1f2937",
    },
}


def palette(name: str) -> dict:
    return THEMES.get(name, THEMES["Dark"])
