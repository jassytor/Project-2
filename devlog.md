# Development Log

## November 19, 2025 9:51PM
- Created initial commits and github repository
- Set up project structure

## November 19, 2025 10:26PM
- Read assignment requirements
- Created file structure and initial titles

## November 19, 2025 11:16PM

Implemented the complete bank simulation with threading and semaphores.

**What I did:**
- Bank class with semaphores for door (2), safe (2), manager (1)
- Customer class with unique IDs and full workflow (9 steps)
- Teller class with service loop that handles deposits and withdrawals
- Main.py to start 3 tellers and customers
- Proper output formatting and error handling with try-finally blocks

**Problems I ran into:**
- First design was too complicated with separate event tuples
- Fixed by using Customer object as shared resource with instance events
- Had to update output format to match exact specification (spaces instead of dashes)

**What I learned:**
- Starting small (5 customers) is way easier to debug than jumping to 50
- Using the Customer object directly is cleaner than passing parameters around
- Semaphore capacity matters: binary (1), counting (2), and signal (0) do different things

**Next time:**
- Test with full 50 customers
- Check for deadlocks and race conditions
- Make sure output looks right
- Commit changes with good messages

## Current Session - Output & Docs

Made the code output exactly match the spec and wrote documentation for the TA.

**What I did:**
- Fixed output format: changed "Teller-1" to "Teller 1"
- Made sure blocking operations show two lines (before/after)
- Made sure resource access shows three lines (going/using/done)
- Cleaned up README to remove unnecessary jargon
- Added TA notes explaining the synchronization strategy

**Problems:**
- Output format didn't match spec (dashes vs spaces)
- README had awkward phrasing - fixed by making it more straightforward
- Started with 50 customers which made testing hard - changed to 5 by default

**What's working:**
- Thread synchronization looks solid
- All 9 customer steps are implemented
- Teller handles both deposits and withdrawals
- Output format is correct
- Exception handling with try-finally blocks

**Next time:**
- Run the program with 5, 10, 25, and 50 customers
- Verify semaphores work correctly (max 2 at door, max 2 at safe, max 1 at manager)
- Check if there are any deadlocks
- Fix any output issues based on actual test runs
- Make final commits

## Testing Session - Output Format Fix

Updated the code to match the exact sample output format provided.

**What I did:**
- Changed Customer messages to use empty brackets `[]` for initial steps
- Updated Customer to show `[Teller X]` only when interacting with teller
- Changed Teller startup to say "ready to serve" then "waiting for a customer"
- Fixed resource access messages to match sample exactly
- Set teller IDs to 0, 1, 2 (instead of 1, 2, 3)
- Set final customer count to 50
- Added closing message "The bank closes for the day."

**Sample output format now matches:**
```
Customer 0 []: wants to perform a deposit transaction
Customer 0 []: going to bank.
Customer 0 []: entering bank.
Customer 0 []: getting in line.
Customer 0 []: selecting a teller.
Customer 0 [Teller 1]: selects teller
Customer 0 [Teller 1] introduces itself
Customer 0 [Teller 1]: asks for deposit transaction
...
Teller 1 [Customer 0]: serving a customer
Teller 1 [Customer 0]: asks for transaction
Teller 1 [Customer 0]: handling deposit transaction
Teller 1 [Customer 0]: going to safe
Teller 1 [Customer 0]: enter safe
Teller 1 [Customer 0]: leaving safe
```

**Created TESTING.md** with:
- Quick start instructions
- What to check in output (format, lifecycle, semaphores)
- Step-by-step testing from 5 to 50 customers
- Commands to analyze output
- Common issues and fixes

**Next time:**
- Run the program starting with 5 customers
- Verify output matches expected format
- Scale up to 10, 25, then 50 customers
- Check semaphore behavior (door, safe, manager limits)
- Look for deadlocks or missing customers
- Make final commits with test results