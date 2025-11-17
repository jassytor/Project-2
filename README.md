# Bank Simulation with Threading

## Overview

This program simulates a bank with 3 tellers serving 50 customers using multi-threading and semaphore-based synchronization.

## Files and Roles

- **bank.py** - Defines the `Bank` class with all shared resources and synchronization primitives (door, safe, manager semaphores and customer queue)
- **teller.py** - Implements the `Teller` thread class that continuously waits for customers and processes their transactions
- **customer.py** - Implements the `Customer` thread class with unique ID generation and full transaction workflow
- **main.py** - Entry point that creates the bank, starts 3 teller threads, and generates 50 customer threads

## Shared Resources

### Semaphores
- **door** (Capacity: 2) - Controls maximum 2 customers entering the bank simultaneously
- **safe** (Capacity: 2) - Controls maximum 2 tellers accessing the safe simultaneously
- **manager** (Capacity: 1) - Ensures only one teller can request withdrawal approval at a time
- **customer_arrives** (Capacity: 0) - Signals when a customer is waiting in the queue

### Queues
- **customer_queue** - Holds `Customer` objects waiting to be served by tellers

## Thread Behavior

### Customer Thread
Each customer performs the following sequence:

1. **Decide transaction** - Randomly chooses between Deposit or Withdrawal
2. **Wait** - Sleeps for 0-100ms before entering bank
3. **Enter bank** - Acquires door semaphore (max 2 concurrent)
4. **Get in line** - Enqueues itself in the customer queue
5. **Select teller** - Waits for teller to signal availability
6. **Provide transaction** - Tells teller the transaction type
7. **Wait for completion** - Waits for teller to complete transaction
8. **Leave bank** - Releases door semaphore and exits

### Teller Thread
Each teller performs the following sequence repeatedly:

1. **Ready to serve** - Prints status and waits for customers
2. **Signal customer** - When customer arrives, signals customer to approach
3. **Ask for transaction** - Requests transaction type from customer
4. **Manager approval** (if Withdrawal) - Acquires manager semaphore (5-30ms interaction)
5. **Access safe** - Acquires safe semaphore (max 2 tellers)
6. **Perform transaction** - Simulates transaction with 10-50ms delay
7. **Notify customer** - Signals transaction completion to customer

## Synchronization Primitives

### Semaphores
- **Binary semaphore** (capacity 1) - Provides mutual exclusion for the manager resource
- **Counting semaphore** (capacity 2) - Controls resource limits for door and safe
- **Signal semaphore** (capacity 0) - Synchronizes arrival events

### Events
- Each `Customer` object has individual threading events for coordinating with its assigned teller:
  - `teller_ready` - Customer waits for teller to be available
  - `ask_transaction` - Customer waits for teller to ask for transaction type
  - `transaction_ready` - Teller waits for customer to provide transaction type
  - `transaction_done` - Customer waits for teller to complete transaction

## Running the Program

### Prerequisites
- Python 3.x
- No external dependencies (uses standard library `threading` and `queue`)

### Compilation
No compilation needed. This is a Python program.

### Execution
From the command line in the project directory, run:
```bash
python main.py
```

or

```bash
python3 main.py
```

### Testing with Different Thread Counts
The program is currently set to run with 50 customers. To test with fewer threads, edit `main.py` and change the `num_customers` variable:

```python
num_customers = 5   # Change 50 to 5, 10, 25, etc. for testing
```

Then run the program normally.

## Output Format

Each thread action is logged in the format:
```
THREAD_TYPE ID [THREAD_TYPE ID]: MESSAGE
```

Examples:
- `Customer 1: decides to perform Deposit`
- `Teller 1 [Customer 5]: is ready`
- `Teller 1 [Customer 5]: goes to manager`
- `Teller 1 [Customer 5]: talks to manager`
- `Teller 1 [Customer 5]: finishes with manager`

Blocking operations produce two lines (before and after the wait):
- `Customer 1: waits before entering bank` (before sleep)
- `Customer 1: finished waiting` (after sleep)

Resource access (manager, safe) produces three lines (going to, using, leaving):
- `Teller 1 [Customer 5]: goes to manager` (before acquiring semaphore)
- `Teller 1 [Customer 5]: talks to manager` (after acquiring, during sleep)
- `Teller 1 [Customer 5]: finishes with manager` (after releasing semaphore)

## Key Design Decisions

1. **Customer as shared object** - Each Customer is enqueued and passed to its assigned Teller, reducing complexity in parameter passing
2. **Instance events** - Each Customer has its own threading events for cleaner synchronization
3. **Semaphore management** - Uses `acquire()` and explicit `release()` with try-finally blocks to ensure proper cleanup
4. **Queue-based dispatch** - Uses Python's thread-safe `Queue` to distribute customers to tellers

## Thread Safety

All shared resources are protected by appropriate synchronization primitives:
- Door, Safe, and Manager use semaphores for mutual exclusion
- Customer queue is thread-safe by design (Python's `Queue` class)
- Individual customer synchronization uses thread-safe `Event` objects
- Customer ID generation uses a lock-protected counter

## Scaling

The program is designed to work with varying thread counts for testing:
- **5 customers** - Quick test to verify basic functionality
- **10 customers** - Ensures proper queue handling
- **25 customers** - Tests resource contention
- **50 customers** - Full simulation as specified

Simply change the `num_customers` variable in `main.py` to test different scales.

## Notes for TA

The program implements a complete bank simulation with proper synchronization:

**Synchronization Primitives Used:**
- Door semaphore (capacity 2) - Limits concurrent customers in bank
- Safe semaphore (capacity 2) - Limits concurrent tellers accessing safe
- Manager semaphore (capacity 1) - Ensures single teller handles withdrawals
- customer_arrives semaphore (capacity 0) - Signals tellers when customers arrive
- Threading Events - For per-customer coordination with assigned teller

**Key Implementation Details:**
- Each Customer generates a unique ID from a lock-protected counter
- Tellers continuously wait for customers in a queue
- All semaphores use acquire() and release() with try-finally blocks for exception safety
- Door is released in a finally block to ensure customers always exit properly
- Manager and Safe semaphores use explicit acquire/release for fine-grained control
- Customer queue holds Customer objects that tellers operate on directly

**Testing:**
- Start with smaller customer counts (5, 10, 25) by editing main.py
- Change `num_customers` variable to test different load scenarios
- Program terminates after all customers are served and queue is empty