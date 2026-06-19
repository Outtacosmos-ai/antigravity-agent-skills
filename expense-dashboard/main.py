from fastapi import FastAPI, responses
from pydantic import BaseModel

app = FastAPI(title="Kaggle 5-Day AI Agents Dashboard")

# Mocking the VertexAiSessionService state locally for the course assignment
PENDING_SESSIONS = [
    {
        "session_id": "session-b12c9801",
        "interrupt_id": "int-9921a",
        "employee": "Mohamed ESSRHIR",
        "item": "AWS Cloud Cert",
        "amount": 150.00,
        "compliance_review": "PASSED: Production-grade event architecture validation."
    },
    {
        "session_id": "session-a84f3210",
        "interrupt_id": "int-4412b",
        "employee": "Bob",
        "item": "Ergonomic Desk",
        "amount": 230.50,
        "compliance_review": "WARNING: Item exceeds standard equipment thresholds. Requires human evaluation."
    }
]

class ActionPayload(BaseModel):
    approved: bool

@app.get("/api/pending")
def get_pending():
    return PENDING_SESSIONS

@app.post("/api/action/{session_id}")
def take_action(session_id: str, payload: ActionPayload):
    global PENDING_SESSIONS
    PENDING_SESSIONS = [s for s in PENDING_SESSIONS if s["session_id"] != session_id]
    return {"status": "SUCCESS", "message": f"Resumed execution context for {session_id} on Agent Runtime."}

@app.get("/", response_class=responses.HTMLResponse)
def server_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kaggle 5-Day AI Agents Course - Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                font-family: 'Inter', sans-serif;
                background: radial-gradient(circle at 50% 50%, #0f111a 0%, #050608 100%);
                color: #f3f4f6;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
                padding: 4rem 2rem;
            }
            .header-container {
                width: 100%;
                max-width: 800px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 2rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                padding-bottom: 1.5rem;
            }
            h1 { font-weight: 600; margin: 0; font-size: 1.5rem; letter-spacing: -0.03em; color: #fff; }
            .subtitle { color: #38bdf8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
            .badge {
                background: rgba(16, 185, 129, 0.1);
                color: #34d399;
                padding: 0.35rem 0.75rem;
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 600;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            .dashboard-container {
                width: 100%;
                max-width: 800px;
                display: grid;
                gap: 1.25rem;
            }
            .card {
                background: rgba(255, 255, 255, 0.02);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.07);
                border-radius: 12px;
                padding: 1.5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: border-color 0.2s, background 0.2s;
            }
            .card:hover {
                border-color: rgba(56, 189, 248, 0.3);
                background: rgba(255, 255, 255, 0.03);
            }
            .info-section h3 { margin: 0 0 0.35rem 0; font-size: 1.15rem; color: #fff; }
            .info-section p { margin: 0; color: #9ca3af; font-size: 0.875rem; }
            .compliance { font-size: 0.8rem; color: #6b7280; margin-top: 0.5rem; padding-left: 0.5rem; border-left: 2px solid rgba(255,255,255,0.1); }
            .right-section { text-align: right; }
            .amount { font-size: 1.35rem; font-weight: 600; color: #38bdf8; margin-bottom: 0.75rem; }
            .actions { display: flex; gap: 0.5rem; }
            button {
                padding: 0.45rem 1rem;
                border-radius: 6px;
                font-weight: 600;
                cursor: pointer;
                font-size: 0.8rem;
                transition: background 0.2s;
                border: none;
            }
            .btn-approve { background-color: #059669; color: #fff; }
            .btn-approve:hover { background-color: #10b981; }
            .btn-reject { background-color: #dc2626; color: #fff; }
            .btn-reject:hover { background-color: #ef4444; }
            .empty-state {
                text-align: center;
                padding: 5rem 2rem;
                background: rgba(255, 255, 255, 0.01);
                border-radius: 12px;
                border: 1px dashed rgba(255, 255, 255, 0.08);
            }
            .sparkle { font-size: 2rem; margin-bottom: 0.75rem; color: #38bdf8; }
        </style>
    </head>
    <body>
        <div class="header-container">
            <div>
                <div class="subtitle">5-Day AI Agents: Intensive Vibe Coding Course With Google</div>
                <h1>Expense Management Dashboard</h1>
            </div>
            <div class="badge">? Live Sync</div>
        </div>

        <div id="dashboard" class="dashboard-container"></div>

        <script>
            async function fetchPending() {
                const res = await fetch('/api/pending');
                const data = await res.json();
                const container = document.getElementById('dashboard');
                container.innerHTML = '';

                if (data.length === 0) {
                    container.innerHTML = `
                        <div class="empty-state">
                            <div class="sparkle">?</div>
                            <h3>All caught up!</h3>
                            <p style="color: #6b7280; margin: 0; font-size: 0.9rem;">No expenses are currently pending manager approval.</p>
                        </div>`;
                    return;
                }

                data.forEach(session => {
                    const card = document.createElement('div');
                    card.className = 'card';
                    card.innerHTML = `
                        <div class="info-section">
                            <h3>${session.employee}</h3>
                            <p>Item: ${session.item}</p>
                            <div class="compliance">${session.compliance_review}</div>
                        </div>
                        <div class="right-section">
                            <div class="amount">$${session.amount.toFixed(2)}</div>
                            <div class="actions">
                                <button class="btn-reject" onclick="handleAction('${session.session_id}', false)">Reject</button>
                                <button class="btn-approve" onclick="handleAction('${session.session_id}', true)">Approve</button>
                            </div>
                        </div>
                    `;
                    container.appendChild(card);
                });
            }

            async function handleAction(sessionId, isApproved) {
                await fetch(`/api/action/${sessionId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ approved: isApproved })
                });
                fetchPending();
            }

            fetchPending();
        </script>
    </body>
    </html>
    """
