async function sendMessage() {

    let input =
        document.getElementById("message");

    let message = input.value;

    if(message.trim() === "") return;

    let chatBox =
        document.getElementById("chat-box");

    // =========================
    // USER MESSAGE
    // =========================

    chatBox.innerHTML += `

        <div class="user-message">
            ${message}
        </div>

    `;

    input.value = "";

    // =========================
    // TYPING MESSAGE
    // =========================

    chatBox.innerHTML += `

        <div class="bot-message typing">
            Designing superconducting architecture...
        </div>

    `;

    chatBox.scrollTop =
        chatBox.scrollHeight;

    // =========================
    // API CALL
    // =========================

    const response = await fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })

    });

    const data = await response.json();

    // =========================
    // REMOVE TYPING
    // =========================

    document.querySelector(".typing").remove();

    // =========================
    // CONDITIONAL IMAGE
    // =========================

    let imageHTML = "";

    if(data.image && data.image !== "") {

        imageHTML = `

            <img
                src="${data.image}?t=${new Date().getTime()}"
                class="generated-image"
            >

        `;
    }

    // =========================
    // BOT RESPONSE
    // =========================

    chatBox.innerHTML += `

        <div class="bot-message">

            ${data.reply.replace(/\n/g, "<br>")}

            ${imageHTML}

        </div>

    `;

    // =========================
    // AUTO SCROLL
    // =========================

    chatBox.scrollTop =
        chatBox.scrollHeight;
}