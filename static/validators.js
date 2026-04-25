document.addEventListener('DOMContentLoaded', function () {
    let djangoInput = document.getElementById('id_username');
    let UserError = document.getElementById('UserError');
    let emailInput = document.getElementById('id_email');
    let EmailError = document.getElementById('EmailError');
    let passwordInput1 = document.getElementById('id_password1');
    let PasswordError1 = document.getElementById('PasswordError1')
    let passwordInput2 = document.getElementById('id_password2');
    let PasswordError2 = document.getElementById('PasswordError2')
    let BirthdayInput = document.getElementById('id_birthday')
    let BirthdayError = document.getElementById('BirthdayInputError')

    if(emailInput !== null) {
        emailInput.addEventListener('blur', function () {
            if (!validateEmail(this.value)) {
                EmailError.textContent = 'Email is not valid. E.g. example@exmp.com';
                this.classList.add('invalid');
            } else {
                this.classList.remove('invalid');
                EmailError.textContent = '';
            }
        });
    }

    if(passwordInput1 !== null) {
        passwordInput1.addEventListener('blur', function () {
            if (!validatePassword(this.value)) {
                this.classList.add('invalid');
                PasswordError1.textContent = 'Password does not stick to below requirements';
            } else {
                this.classList.remove('invalid');
                PasswordError1.textContent = '';
            }
        });
    }

    if(passwordInput2 !== null) {
        passwordInput2.addEventListener('blur', function () {
            if (!validatePassword(this.value)) {
                this.classList.add('invalid');
                PasswordError2.textContent = 'Password does not stick to above requirements';
            } else {
                this.classList.remove('invalid');
                PasswordError2.textContent = '';
            }
        });
    }

    if(djangoInput !== null) {
        djangoInput.addEventListener('blur', function () {
            if (!validateUserName(this.value)) {
                this.classList.add('invalid');
                UserError.textContent = 'Username does not stick to below requirements'
            } else {
                this.classList.remove('invalid');
                UserError.textContent = ''
            }
        });
    }

    if(BirthdayInput !== null) {
        BirthdayInput.addEventListener('blur', function () {
            if (!validateDate(this.value)) {
                this.classList.add('invalid');
                BirthdayError.textContent = 'Username does not stick to below requirements'
            } else {
                this.classList.remove('invalid');
                BirthdayError.textContent = ''
            }
        });
    }
});

function validateEmail(email) {
    let re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    // Example: Minimum eight characters, at least one letter and one number
    let re= /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&(*)]{8,}$/;
    return re.test(password);
}

function validateUserName(text) {
    // Example: No validation logic, can be replaced with actual validation
    let re = /^[A-Za-z\d@_.+-]{1,150}$/;
    return re.test(text);
}

function validateDate(dateString) {
    // Regular expression to check the date format (YYYY-MM-DD)
    const regex = /^\d{4}-\d{2}-\d{2}$/;

    // Check if date matches the required format
    if (!regex.test(dateString)) {
        return false;
    }

    // Try to create a date object
    const date= new Date(dateString);

    // Check if the date is valid
    if (!date.getTime() && date.getTime() !== 0) {
        return false;
    }

    // Extract year, month, and day from the date string
    const [year, month, day] = dateString.split('-').map(Number);

    // Check if the year, month, and day correspond to the date object
    // Note: Month in JavaScript Date is 0-indexed (0-11)
    if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) {
        return false;
    }
    return true;
}