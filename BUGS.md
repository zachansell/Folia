# Bug Tracker

## Active Issues

| ID | Priority | Status | Component | Description | Reported |
|----|----------|--------|-----------|-------------|----------|
| 001 | High | Open | folia_gui_simple | Submit button doesn't disable after clicking, allows duplicate submissions | 2025-11-09 |
| 002 | Medium | Open | scrabble_leave_trainer | Stats display doesn't update after completing quiz | 2025-11-08 |
| 003 | Low | Open | LeaveSet | No validation for malformed CSV entries | 2025-11-10 |
| 004 | Medium | Open | Quiz | Time tracking resets between questions instead of accumulating | 2025-11-11 |

## Resolved Issues

| ID | Priority | Status | Component | Description | Resolved |
|----|----------|--------|-----------|-------------|----------|
| - | - | - | - | - | - |

## Enhancement Requests

| ID | Priority | Status | Feature | Description | Requested |
|----|----------|--------|---------|-------------|-----------|
| E001 | Medium | Planned | Quiz | Add difficulty levels (beginner/intermediate/advanced) | 2025-11-10 |
| E002 | Low | Planned | UI | Add keyboard shortcuts (Enter to submit, Esc to cancel) | 2025-11-10 |
| E003 | High | Planned | Stats | Export quiz results to CSV | 2025-11-08 |
| E004 | Medium | Backlog | Quiz | Add timed mode with countdown | 2025-11-11 |
| E005 | Low | Backlog | UI | Dark mode toggle | 2024-11-13 |

## Known Limitations

- CSV file must be in same directory as LeaveSet.py
- No undo functionality during quiz
- Session stats stored in plaintext JSON (no encryption)
- Large CSV files (900K+ entries) take ~2-3 seconds to load on startup
- No multi-user support

## Bug Report Template

```
**Bug ID:** [Auto-assigned]
**Priority:** [Low/Medium/High/Critical]
**Component:** [LeaveSet/Quiz/QuizItem/UI/Other]
**Status:** [Open/In Progress/Resolved/Closed]

**Description:**
[Clear description of the issue]

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Environment:**
- OS: 
- Python Version: 
- Folia Version: 

**Additional Notes:**
[Any other relevant information]
```

## Priority Definitions

- **Critical**: App crashes or data loss
- **High**: Major functionality broken
- **Medium**: Feature works but has issues
- **Low**: Minor cosmetic or edge case issues

## Status Definitions

- **Open**: Reported but not started
- **In Progress**: Currently being worked on
- **Resolved**: Fixed and ready for testing
- **Closed**: Verified fixed and deployed
- **Backlog**: Acknowledged but not scheduled
- **Planned**: Scheduled for upcoming release

