// Alternar formulários
function toggleForm(formId) {
    document.querySelectorAll('.form').forEach(form => form.classList.remove('active'));
    document.getElementById(`form-${formId}`).classList.add('active');
}

// Login
function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    auth.signInWithEmailAndPassword(email, password)
        .then(() => {
            Swal.fire('Sucesso!', 'Login realizado com sucesso!', 'success');
        })
        .catch(error => {
            Swal.fire('Erro!', error.message, 'error');
        });
}

// Cadastro
function register() {
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    auth.createUserWithEmailAndPassword(email, password)
        .then(() => {
            Swal.fire('Sucesso!', 'Conta criada com sucesso!', 'success');
            toggleForm('login');
        })
        .catch(error => {
            Swal.fire('Erro!', error.message, 'error');
        });
}

// Redefinir senha
function resetPassword() {
    const email = document.getElementById('reset-email').value;

    auth.sendPasswordResetEmail(email)
        .then(() => {
            Swal.fire('Sucesso!', 'E-mail de redefinição de senha enviado!', 'success');
            toggleForm('login');
        })
        .catch(error => {
            Swal.fire('Erro!', error.message, 'error');
        });
                      }
