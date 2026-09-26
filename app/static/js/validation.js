/* Client-side validation layer (runs in addition to HTML5 and server-side checks). */
document.querySelectorAll("form[data-validate]").forEach(function (form) {
  form.addEventListener("submit", function (event) {
    var messages = [];

    form.querySelectorAll("[required]").forEach(function (field) {
      if (!field.value.trim()) {
        messages.push("The field '" + (field.name || "input") + "' is required.");
      }
    });

    var email = form.querySelector("input[type=email]");
    if (email && email.value && !/^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$/.test(email.value)) {
      messages.push("Please enter a valid email address.");
    }

    var password = form.querySelector("input[type=password]");
    if (password && password.value && password.value.length < 6) {
      messages.push("Password must be at least 6 characters long.");
    }

    if (messages.length) {
      event.preventDefault();
      alert(messages.join("\n"));
    }
  });
});
