const messageInput = document.getElementById("message");
const buttonSend = document.getElementById("button-addon2");
const chatbox = document.getElementById("chatbox");
const localUrl = "http://localhost:5000/api/v1/bot";
let botname = "Chat bot";

function fetchInitData() {
  const http = new XMLHttpRequest();

  http.onload = function () {
    if (http.status == 200) {
      data = JSON.parse(http.responseText);
      botname = data?.bot_name;
      greet = data?.response;
      createBotChatUI(greet);
    } else {
      createBotChatUI("Something went wrong, Unable to fetch data..");
    }
  };

  http.open("GET", localUrl);
  http.send();
}

fetchInitData();

function sendMessage(message, method, url) {
  const header = createHeaderBot();
  chatbox.appendChild(header);

  const p = document.createElement("p");
  p.classList.add("small", "p-2", "ms-3", "mb-3", "rounded-3");
  p.setAttribute("style", "background-color: #f5f6f7");
  p.textContent = "Loading...";

  const chatBody = createBotChatBody(p);
  chatbox.appendChild(chatBody);

  const http = new XMLHttpRequest();
  http.open(method, url);
  http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

  http.onload = function () {
    if (http.status == 200) {
      const data = JSON.parse(http.responseText);
      p.textContent = data?.response;
    } else {
      p.textContent = "Unable to fetch reply..";
    }
  };

  http.send(
    JSON.stringify({
      message: message,
    })
  );
}

function createHeaderUser(name) {
  const p = document.createElement("p");
  p.classList.add("small", "mb-1", "ms-auto");
  p.textContent = name;

  const div = document.createElement("div");
  div.classList.add("d-flex", "justify-content-between");
  div.appendChild(p);

  return div;
}

function createHeaderBot() {
  const p = document.createElement("p");
  p.classList.add("small", "mb-1");
  p.textContent = botname;

  const div = document.createElement("div");
  div.classList.add("d-flex", "justify-content-between");
  div.appendChild(p);

  return div;
}

function createBotChatBody(p) {
  const div = document.createElement("div");
  div.appendChild(p);

  const img = document.createElement("img");
  img.setAttribute(
    "src",
    "https://img.freepik.com/free-icon/robot_318-843663.jpg?w=2000"
  );
  img.setAttribute("alt", "avatar 1");
  img.setAttribute("style", "width: 45px; height: 100%");

  const container = document.createElement("div");
  container.classList.add("d-flex", "flex-row", "justify-content-start");

  container.appendChild(img);
  container.appendChild(div);

  return container;
}

function createUserChatBody(message) {
  const p = document.createElement("p");
  p.classList.add(
    "small",
    "p-2",
    "me-3",
    "text-white",
    "rounded-3",
    "bg-warning"
  );
  p.textContent = message;

  const div = document.createElement("div");
  div.appendChild(p);

  const img = document.createElement("img");
  img.setAttribute(
    "src",
    "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp"
  );
  img.setAttribute("alt", "avatar 1");
  img.setAttribute("style", "width: 45px; height: 100%");

  const container = document.createElement("div");
  container.classList.add(
    "d-flex",
    "flex-row",
    "justify-content-end",
    "mb-4",
    "pt-1"
  );

  container.appendChild(div);
  container.appendChild(img);

  return container;
}

function createUserChatUI(message) {
  const header = createHeaderUser("John Doe");
  chatbox.appendChild(header);

  const chatBody = createUserChatBody(message);
  chatbox.appendChild(chatBody);

  scrollToBottomChatbox();
}

function scrollToBottomChatbox() {
  chatbox.scrollTo(0, chatbox.scrollHeight);
}

function createBotChatUI(message) {
  const header = createHeaderBot();
  chatbox.appendChild(header);

  const p = document.createElement("p");
  p.classList.add("small", "p-2", "ms-3", "mb-3", "rounded-3");
  p.setAttribute("style", "background-color: #f5f6f7");
  p.textContent = message;

  const chatBody = createBotChatBody(p);
  chatbox.appendChild(chatBody);

  scrollToBottomChatbox();
}

buttonSend.addEventListener("click", function (event) {
  event.preventDefault();
  const message = messageInput.value;
  createUserChatUI(message);
  sendMessage(message, "POST", localUrl);
  messageInput.value = "";
  scrollToBottomChatbox();
});
