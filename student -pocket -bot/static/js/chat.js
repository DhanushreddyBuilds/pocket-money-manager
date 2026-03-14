const chatBox = document.getElementById("chat");
const typing = document.getElementById("typing");

function nowTime() {
    const d = new Date();
    return d.getHours() + ":" + d.getMinutes().toString().padStart(2,"0");
}

function addMsg(text, cls) {
    const div = document.createElement("div");
    div.className = "message " + cls;

    div.innerHTML = text + `<span class="message-time">${nowTime()}</span>`;
    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTyping(show) {
    typing.style.display = show ? "block" : "none";
    chatBox.scrollTop = chatBox.scrollHeight;
}

function send() {

    const input = document.getElementById("msg");
    const text = input.value.trim();
    if (!text) return;

    addMsg(text, "user");
    input.value = "";

    showTyping(true);

    fetch("/chat", {
        method: "POST",
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({msg:text})
    })
    .then(r => r.json())
    .then(d => {
        setTimeout(() => {
            showTyping(false);
            addMsg(d.reply.replace(/\n/g,"<br>"), "bot");
        }, 600);
    });
}
