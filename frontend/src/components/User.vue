<template>
  <div>
    <!-- Navbar -->

    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm py-3">
    <div class="container-fluid d-flex justify-content-between align-items-center">

      <!-- Left: App Logo / Name -->
      <a class="navbar-brand fw-bold fs-4 text-white" href="#">User Dashboard</a>

      <!-- Center: Welcome User -->
      <div class="text-white d-none d-md-block">
        <span class="fw-semibold fs-5">Welcome, {{ user.fullname }}</span>
      </div>

      <!-- Right: Action Buttons -->
      <div class="d-flex gap-2">
        <a href="/user_result" class="btn btn-outline-light fw-semibold">
          <i class="bi bi-bar-chart-line-fill me-1"></i> Result
        </a>

        <a href="/" class="btn btn-light fw-semibold text-primary">
          <i class="bi bi-box-arrow-right me-1"></i> Logout
        </a>
      </div>

    </div>
  </nav>

    <!-- Main content -->
    <div class="container py-4">
      <!-- Search box -->
      <div class="row mb-4">
        <div class="col-md-6 mx-auto">
          <input
            type="text"
            class="form-control form-control-lg shadow-sm"
            placeholder="🔍 Search quizzes by title, subject or chapter..."
            v-model="searchQuery"
          />
        </div>
      </div>

      <!-- Quizzes -->
      <div class="row">
        <div
          class="col-lg-4 col-md-6 mb-4"
          v-for="quiz in filteredQuizzes"
          :key="quiz.id"
        >
          <div class="card border-0 shadow h-100">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title text-primary fw-bold">{{ quiz.name }}</h5>
              <p class="card-text">{{ quiz.description }}</p>
              <ul class="list-unstyled small text-muted">
                <li><strong>Subject:</strong> {{ quiz.subject }}</li>
                <li><strong>Chapter:</strong> {{ quiz.chapter }}</li>
              </ul>
              <span
                class="badge"
                :class="quiz.single_attempt ? 'bg-danger' : 'bg-success'"
              >
                {{ quiz.single_attempt ? 'Single Attempt Only' : 'Multiple Attempts Allowed' }}
              </span>

              <div class="mt-auto pt-3">
                <router-link
                  :to="`/start_quiz/${quiz.id}`"
                  class="btn btn-primary w-100"
                >
                  🚀 Start Quiz
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- If no quiz matches the search -->
        <div v-if="filteredQuizzes.length === 0" class="text-center text-muted mt-5">
          <h5>No quizzes found matching your search.</h5>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      searchQuery: '',
      quizzes: [],
      user: {
        fullname: ''
      },
    };
  },
  computed: {
    filteredQuizzes() {
      return this.quizzes.filter((quiz) =>
        quiz.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    fetchQuizzes() {
      fetch('https://mad2-quiz-master-vue-flask-7.onrender.com//get_quiz', {
        headers: {
            "content-type": "application/json",
          'Authorization': `Bearer ${localStorage.getItem('user_token')}`
        }
      })
        .then(response => response.json())
        .then(data => {
          this.quizzes = data;
        })
        .catch(error => {
          console.error('Error fetching quizzes:', error);
        });
    },

    fetchUserDetails() {
       fetch('https://mad2-quiz-master-vue-flask-7.onrender.com//username', {
        headers: {
            'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('user_token')}`
        }
      })
        .then(response => response.json())
        .then(data => {
          this.user = data;
        })
        .catch(error => {
          console.error('Error fetching user details:', error);
        });
    },
    startQuiz(quizId) {
      this.$router.push(`/quiz/${quizId}`);
    }
  },
  mounted() {
    this.fetchQuizzes();
    this.fetchUserDetails();
  }
};
</script>

<style scoped>
.card-title {
  font-size: 1.2rem;
  font-weight: bold;
}
</style>
