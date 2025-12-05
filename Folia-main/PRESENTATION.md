# FOLIA
## Scrabble Leave Value Study Tool

**Benjamin Kramer & Zachary Ansell**

---

# SLIDE 1: What Folia Does

## The Problem
- Scrabble players need to evaluate "leaves" (tiles remaining after a play)
- 900,000+ possible leave combinations each with strategic value
- Can't memorize all values → need to develop **intuition**

## Our Solution: Folia
**A desktop study tool combining interactive quizzes with instant lookup**

### What Distinguishes Folia:
- **Active Learning**: Quiz-based training vs. passive reference
- **Immediate Feedback**: Shows your guess vs. actual value + difference
- **Flexible Difficulty**: Customizable filters (length, vowels, value ranges)
- **Zero Dependencies**: Pure Python + Tkinter (built-in)

---

# SLIDE 2: Architecture

```
        ┌─────────────────────────────┐
        │   folia_gui_simple.py       │  ← Tkinter UI
        │   (Presentation Layer)       │
        └──────────┬──────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
   ┌────▼────┐          ┌────▼─────┐
   │ Quiz.py │          │LeaveSet.py│  ← Business Logic
   │QuizItem │          │           │
   └─────────┘          └─────┬─────┘
                              │
                    ┌─────────▼──────────┐
                    │ nwl-leave-values   │  ← Data Layer
                    │      .csv          │    (900K entries)
                    └────────────────────┘
```

## Component Responsibilities
- **LeaveSet**: CSV parsing, normalization, filtering, lookup
- **Quiz/QuizItem**: State management, scoring, timing, statistics
- **GUI**: Menu navigation, quiz display, results, user input

---

# SLIDE 3: Lessons Learned (Part 1)

## 1. Performance Optimization Matters
- **Problem**: 900K CSV load took 5-6 seconds
- **Solution**: Optimized parsing + pre-filtering
- **Result**: Reduced to 2-3 seconds
- **Lesson**: Profile first, optimize bottlenecks

## 2. GUI Responsiveness is Critical
- **Problem**: Tkinter froze during data loading
- **Solution**: Separate data operations from UI thread
- **Lesson**: Never block the UI thread

## 3. Input Validation is Essential
- **Problem**: Users could submit multiple answers
- **Solution**: State management + button disabling (partially implemented)
- **Lesson**: Edge cases will find you - test user workflows early

---

# SLIDE 4: Lessons Learned (Part 2)

## 4. Testing Saves Time
- **Benefit**: Caught edge cases in leave normalization (e.g., blank tile sorting)
- **Impact**: Confidence in refactoring, faster debugging
- **Lesson**: Invest in test infrastructure for data-heavy apps

## 5. Simplicity > Feature Creep
- **Temptation**: Difficulty levels, timed modes, dark mode, leaderboards
- **Decision**: Focus on core functionality (quiz + lookup)
- **Result**: Clean codebase, faster MVP delivery
- **Lesson**: Ship a polished core experience first

## 6. Choose Appropriate Complexity
- **Trade-off**: CSV vs. SQLite database
- **Decision**: CSV is "good enough" for 900K entries
- **Lesson**: Don't over-engineer - match solution to scale

---

# SLIDE 5: Demo & Next Steps

## Demo Flow
1. Launch app & load 900K leave values
2. **Quiz Mode**: Guess leave values, see feedback
3. **Lookup Mode**: Quick reference for any leave
4. **Results**: Performance statistics

## Future Enhancements
- Export quiz results to CSV
- Difficulty presets (beginner/intermediate/advanced)
- Keyboard shortcuts
- Timed challenge mode

## Questions?

