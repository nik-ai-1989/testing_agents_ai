# BA User Story Agent

Transforms Business Analyst requirements documents (markdown/text) into structured agile user stories using the Claude API.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
```

## Usage

```bash
python agent.py <requirements_file>
python agent.py example_requirements.md
```

Output is written to `user_stories/<source>_<timestamp>.md`. The script prints git commands to commit and push when done.

## File Structure

- `agent.py` — main agent script
- `example_requirements.md` — sample requirements document to test with
- `requirements.txt` — Python dependencies
- `user_stories/` — generated output (created automatically)

## User Story Format

Each generated story follows the standard agile structure:

```
## US-001: Short Title

As a [role], I want [goal] so that [benefit].

Acceptance Criteria, Priority, Story Points, Labels
```

## Notes

- Uses `claude-opus-4-8` with adaptive thinking and prompt caching on the system prompt
- Streams output to the terminal as it generates
- Git commit/push is a manual step after review
