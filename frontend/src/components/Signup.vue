<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="card shadow p-4 w-100" style="max-width: 500px;">
      <h2 class="text-center text-primary mb-4">Sign Up</h2>
      <form @submit.prevent="signup">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            type="text"
            class="form-control"
            id="username"
            v-model="username"
            placeholder="Enter a unique username"
            required
          />
        </div>

        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            class="form-control"
            id="email"
            v-model="email"
            placeholder="you@example.com"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="password"
            placeholder="Create a strong password"
            required
          />
        </div>

        <div class="mb-3">
          <label for="dob" class="form-label">Date of Birth</label>
          <input
            type="date"
            class="form-control"
            id="dob"
            v-model="dob"
            required
          />
        </div>

        <div class="mb-3">
          <label for="fullname" class="form-label">Full Name</label>
          <input
            type="text"
            class="form-control"
            id="fullname"
            v-model="fullname"
            placeholder="Enter your full name"
            required
          />
        </div>

        <div class="mb-4">
          <label for="qualification" class="form-label">Qualification</label>
          <input
            type="text"
            class="form-control"
            id="qualification"
            v-model="qualification"
            placeholder="e.g. B.Sc, B.Tech, etc."
            required
          />
        </div>

        <div class="d-grid">
          <button type="submit" class="btn btn-primary btn-block">Sign Up</button>
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
      email: '',
      password: '',
      dob: '',
      fullname: '',
      qualification: '',
    };
  },
  methods: {
    async signup() {
      const response = await fetch('https://mad2-quiz-master-vue-flask-7.onrender.com//signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: this.username,
          email: this.email,
          password: this.password,
          dob: this.dob,
          fullname: this.fullname,
          qualification: this.qualification,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        alert('Signup successful! Please login.');
        this.$router.push('/login');
      } else {
        alert('Signup failed: ' + data.message);
      }
    },
  },
};
</script>

<style scoped>
.card:hover {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}
</style>
