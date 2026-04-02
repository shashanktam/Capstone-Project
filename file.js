function validateForm() {
  let email = document.getElementById("email").value;
  let password = document.getElementById("password").value;
  let confirmPassword = document.getElementById("confirmPassword").value;
  let inputs = document.querySelectorAll("input");

  let valid = true;

  inputs.forEach((input) => {
    if (input.value.trim() === "") {
      input.style.border = "2px solid red";
      valid = false;
    } else {
      input.style.border = "1px solid #ccc";
    }
  });

  if (!email.endsWith("@iitp.ac.in")) {
    alert("Email must be IIT Patna email (@iitp.ac.in)");
    valid = false;
  }

  if (password !== confirmPassword) {
    alert("Passwords do not match");
    valid = false;
  }

  if (valid) {
    alert("Form Submitted Successfully!");
  }
}

document.getElementById("password").addEventListener("input", function () {
  let password = this.value;
  let strengthBar = document.getElementById("strengthBar");

  let strength = 0;

  if (password.length > 6) strength++;
  if (/[A-Z]/.test(password)) strength++;
  if (/[0-9]/.test(password)) strength++;
  if (/[@$!%*?&]/.test(password)) strength++;

  if (strength <= 1) {
    strengthBar.style.background = "red";
    strengthBar.style.width = "33%";
  } else if (strength == 2 || strength == 3) {
    strengthBar.style.background = "yellow";
    strengthBar.style.width = "66%";
  } else {
    strengthBar.style.background = "green";
    strengthBar.style.width = "100%";
  }
});

document
  .getElementById("confirmPassword")
  .addEventListener("input", function () {
    let password = document.getElementById("password").value;
    let confirmPassword = this.value;

    if (password !== confirmPassword) {
      this.style.border = "2px solid red";
    } else {
      this.style.border = "2px solid green";
    }
  });