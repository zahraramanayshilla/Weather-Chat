function addMessage(text, sender) {
    const box = document.getElementById("chatBox");
    const div = document.createElement("div");

    div.className =
        sender === "user"
            ? "bg-blue-500 text-white p-2 rounded self-end max-w-xs ml-auto"
            : "bg-gray-200 p-2 rounded self-start max-w-xs";

    div.innerHTML = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("message");
    const msg = input.value.trim();

    if (!msg) return;

    addMessage(msg, "user");
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: msg }),
    })
        .then((res) => res.json())
        .then((data) => addMessage(data.reply, "bot"))
        .catch(() =>
            addMessage("⚠️ Server tidak merespons.", "bot")
        );
}

// Kirim pesan saat tekan Enter
document.addEventListener("DOMContentLoaded", () => {
    document
        .getElementById("message")
        .addEventListener("keypress", function (e) {
            if (e.key === "Enter") sendMessage();
        });
});
