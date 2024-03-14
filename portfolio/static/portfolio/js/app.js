const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("slidein");
    } else {
      entry.target.classList.remove("slidein");
    }
  });
});

const hiddenElement = document.querySelectorAll(".slidein-card");
hiddenElement.forEach((element) => {
  observer.observe(element);
});

var toggler = document.getElementById("dark-side-toggle");
toggler.onclick = () => {
  document.body.classList.toggle("light-side");
  let togglerIcon = document.getElementById("toggler-icon");
  if (togglerIcon.classList.contains("bi-sun-fill")) {
    togglerIcon.classList.replace("bi-sun-fill", "bi-moon-fill");
  } else {
    togglerIcon.classList.replace("bi-moon-fill", "bi-sun-fill");
  }
};

function submitForm() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const message = document.getElementById("message").value;
  const re =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

  if (!name || !email || !message) {
    alert("Please fill in all fields.");
    return;
  }

  if (!re.test(String(email).toLowerCase())) {
    alert("Please provide a valid email address.");
    return;
  }

  alert("Thank you for contacting me.");

  fetch(contactUrl, {
    method: "POST",
    body: JSON.stringify({ name, email, message }),
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error("Error:", error);
    });
}
