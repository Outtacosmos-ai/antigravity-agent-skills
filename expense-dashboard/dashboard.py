import time
import uuid

# In-memory "Session Service" database simulating state preservation
SESSION_DB = {
    "pending": [],
    "approved": [],
    "rejected": []
}

def process_pubsub_event(employee: str, amount: float, item: str):
    """Simulates event execution on the Agent Runtime."""
    print(f"\n[Pub/Sub Event Inested] Processing submission from {employee}...")
    time.sleep(0.5)
    
    event_id = str(uuid.uuid4())[:8]
    payload = {"id": event_id, "employee": employee, "amount": amount, "item": item}
    
    # Core Spec-Driven Logic Boundary
    if amount < 100:
        print(f"? [Auto-Approved] Expense {event_id} (${amount}) is under the $100 threshold.")
        SESSION_DB["approved"].append(payload)
    else:
        print(f"??  [HITL Interception] Expense {event_id} (${amount}) requires review!")
        print(f"?? Session {event_id} has been paused and persisted to the Session Service.")
        SESSION_DB["pending"].append(payload)

def show_manager_dashboard():
    """Simulates the Cloud Run Dashboard UI & Manager Resolution."""
    print("\n" + "="*50)
    print("        MANAGER DASHBOARD (CLOUD RUN UI)")
    print("="*50)
    
    if not SESSION_DB["pending"]:
        print("?? No pending expenses require human resolution.")
        return False
        
    print(f"?? Pending Reviews ({len(SESSION_DB['pending'])}):")
    for idx, item in enumerate(SESSION_DB["pending"], 1):
        print(f"  [{idx}] ID: {item['id']} | {item['employee']} | {item['item']} | ${item['amount']}")
    
    print("-" * 50)
    try:
        choice = input("Select an index to review (or press enter to skip): ").strip()
        if not choice: return True
        
        idx = int(choice) - 1
        if 0 <= idx < len(SESSION_DB["pending"]):
            item = SESSION_DB["pending"].pop(idx)
            action = input(f"Action for {item['id']} - [A]pprove or [R]eject? ").strip().upper()
            
            if action == 'A':
                print(f"?? Resuming execution context: Session {item['id']} APPROVED.")
                SESSION_DB["approved"].append(item)
            else:
                print(f"?? Terminating execution context: Session {item['id']} REJECTED.")
                SESSION_DB["rejected"].append(item)
        else:
            print("Invalid index selection.")
    except ValueError:
        print("Please enter a numeric choice.")
    return True

if __name__ == "__main__":
    # 1. Simulate asynchronous ingest payloads matching our Gherkin scenarios
    process_pubsub_event("Alice", 50.00, "Team Lunch")       # Scenario 1 (Auto-approve)
    process_pubsub_event("Mohamed", 150.00, "AWS Cloud Cert") # Scenario 2 (Pause/HITL)
    process_pubsub_event("Bob", 230.50, "Ergonomic Desk")    # Additional test case
    
    # 2. Run the human dashboard interface loop
    looping = True
    while looping:
        looping = show_manager_dashboard()
        
    print("\n?? Workflow execution trace complete. Zero resources provisioned, zero cost incurred!")
