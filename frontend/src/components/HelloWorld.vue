<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-primary text-white text-center py-5">
      <div class="container">
        <h1 class="display-4 fw-bold">Welcome to QuizMaster</h1>
        <p class="lead">Test your knowledge. Compete. Learn more every day!</p>
        <router-link to="/login" class="btn btn-light btn-lg mt-3" >Login</router-link>
        <router-link to="/signup" class="btn btn-outline-light btn-lg mt-3 ms-2">Sign Up</router-link>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-5">
      <div class="container">
        <div class="row text-center">
          <div class="col-md-4 mb-4">
            <i class="bi bi-journal-check display-4 text-primary"></i>
            <h5 class="mt-3">Multiple Categories</h5>
            <p>Choose from various topics to challenge your mind.</p>
          </div>
          <div class="col-md-4 mb-4">
            <i class="bi bi-clock-history display-4 text-success"></i>
            <h5 class="mt-3">Timed Quizzes</h5>
            <p>Improve your speed and accuracy with timed sessions.</p>
          </div>
          <div class="col-md-4 mb-4">
            <i class="bi bi-bar-chart-fill display-4 text-danger"></i>
            <h5 class="mt-3">Score Reports</h5>
            <p>Track your progress and improve with detailed reports.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-3">
      <p class="mb-0">© 2025 QuizMaster. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "LandingPage",
  
};
</script>

<style scoped>
/* Optional: Additional styles */
</style>
