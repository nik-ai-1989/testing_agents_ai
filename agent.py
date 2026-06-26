"""
BA Requirements → User Stories Agent

Usage:
    python agent.py <requirements_file>
    python agent.py example_requirements.md
"""

import anthropic
import sys
from datetime import datetime
from pathlib import Path


SYSTEM_PROMPT = """You are an expert Business Analyst and Agile practitioner. \
Your job is to transform raw business requirements into clear, actionable user stories \
that a development team can implement.

For each user story, output exactly this Markdown structure:

---

## [US-XXX]: [Short Title]

**User Story:**
As a [user role], I want [goal] so that [benefit].

**Acceptance Criteria:**
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]
- [ ] [Edge case or negative scenario]

**Priority:** High | Medium | Low
**Story Points:** 1 | 2 | 3 | 5 | 8 | 13
**Labels:** [comma-separated labels, e.g. frontend, auth, api]

---

Rules:
- Number stories sequentially: US-001, US-002, etc.
- Write from the end user's perspective
- Each story must be independently deployable (INVEST principle)
- Acceptance criteria must be specific and testable by QA
- Use Fibonacci for story points (complexity, not time)
- Add "Depends on: US-XXX" at the end when a story has a hard dependency
- Split large features into multiple focused stories
- Cover happy paths, edge cases, and error states"""


def read_requirements(path: str) -> str:
    p = Path(path)
    if not p.exists():
        sys.exit(f"Error: file not found: {path}")
    return p.read_text(encoding="utf-8")


def generate_user_stories(requirements: str, client: anthropic.Anthropic) -> str:
    collected: list[str] = []

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=8192,
        thinking={"type": "adaptive"},
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    "Analyze these requirements and generate all necessary user stories. "
                    "Cover every functional requirement. Number them sequentially.\n\n"
                    "---\n\n"
                    f"{requirements}\n\n"
                    "---"
                ),
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            collected.append(text)

    print()
    return "".join(collected)


def save_stories(stories: str, source_file: str) -> Path:
    out_dir = Path("user_stories")
    out_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    source_stem = Path(source_file).stem
    out_file = out_dir / f"{source_stem}_{timestamp}.md"

    header = (
        f"# User Stories\n\n"
        f"**Source:** `{source_file}`  \n"
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    )
    out_file.write_text(header + stories, encoding="utf-8")
    return out_file


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python agent.py <requirements_file>")
        print("       python agent.py example_requirements.md")
        sys.exit(1)

    requirements_file = sys.argv[1]

    print(f"Reading requirements: {requirements_file}\n")
    requirements = read_requirements(requirements_file)

    client = anthropic.Anthropic()

    print("Generating user stories...\n")
    print("─" * 60)
    stories = generate_user_stories(requirements, client)
    print("─" * 60)

    out_file = save_stories(stories, requirements_file)

    print(f"\n✓ Saved: {out_file}")
    print("\nTo commit and push:")
    print(f"  git add {out_file}")
    print(f"  git commit -m 'feat: add user stories from {Path(requirements_file).name}'")
    print("  git push")


if __name__ == "__main__":
    main()
