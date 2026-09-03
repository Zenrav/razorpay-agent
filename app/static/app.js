const messages = document.getElementById("messages");
const auditList = document.getElementById("audit");
const composer = document.getElementById("composer");
const input = document.getElementById("input");
const send = document.getElementById("send");

function addMessage(text, role, orderId) {
  const el = document.createElement("div");
  el.className = `msg ${role}`;
  el.textContent = text;
  if (orderId) {
    const order = document.createElement("span");
    order.className = "order";
    order.textContent = `order id: ${orderId}`;
    el.appendChild(order);
  }
  messages.appendChild(el);
  messages.scrollTop = messages.scrollHeight;
  return el;
}

async function refreshAudit() {
  const entries = await fetch("/audit").then((response) => response.json());
  auditList.innerHTML = "";
  if (!entries.length) {
    auditList.innerHTML = '<li class="empty">No decisions yet.</li>';
    return;
  }
  for (const entry of entries.slice().reverse()) {
    const item = document.createElement("li");
    item.dataset.action = entry.action;
    const amount = entry.amount ? ` <span class="amount">INR ${entry.amount}</span>` : "";
    item.innerHTML = `<span class="action">${entry.action}</span>${amount}<br /><span class="reason"></span>`;
    item.querySelector(".reason").textContent = entry.reason;
    auditList.appendChild(item);
  }
}

async function sendMessage(text) {
  addMessage(text, "user");
  const pending = addMessage("thinking…", "agent typing");
  send.disabled = true;
  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await response.json();
    pending.remove();
    addMessage(data.reply, "agent", data.order_id);
  } catch (error) {
    pending.remove();
    addMessage(`Could not reach the agent: ${error.message}`, "error");
  } finally {
    send.disabled = false;
    input.focus();
    refreshAudit();
  }
}

composer.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  sendMessage(text);
});

document.getElementById("suggestions").addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (button) sendMessage(button.dataset.msg);
});

refreshAudit();
