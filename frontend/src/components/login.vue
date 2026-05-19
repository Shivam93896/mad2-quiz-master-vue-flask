<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="card shadow p-4" style="width: 100%; max-width: 400px;">
      <div class="text-center mb-4">
        <h2 class="text-primary">Login</h2>
        <p class="text-muted">Please enter your credentials</p>
      </div>
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            type="text"
            class="form-control"
            id="username"
            v-model="username"
            required
            placeholder="Enter your username"
          />
        </div>
        <div class="mb-4">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="password"
            required
            placeholder="Enter your password"
          />
        </div>
        <div class="d-grid">
          <button type="submit" class="btn btn-primary">Login</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      const response = await fetch('https://mad2-quiz-master-vue-flask-7.onrender.com//login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        if (data.username === 'admin') {
          localStorage.setItem('admin_username', data.username);
          localStorage.setItem('admin_id', data.user_id);
          localStorage.setItem('admin_token', data.access_token);
          this.$router.push('/admin');
        } else {
          localStorage.setItem('user_username', data.username);
          localStorage.setItem('user_id', data.user_id);
          localStorage.setItem('user_token', data.access_token);
          this.$router.push('/user');
        }
      } else {
        alert('Login failed: ' + data.message);
      }
    },
  },
};
</script>

<style scoped>
/* Optional: Add a smooth shadow effect on hover for the card */
.card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}
</style>
