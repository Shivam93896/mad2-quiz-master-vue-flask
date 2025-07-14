<template>
  <div class="container mt-5">
    <!-- Title -->
    <h2 class="text-center mb-4 text-primary fw-bold">📊 User Quiz Results</h2>

    <!-- Results Table in a Card -->
    <div class="card shadow-sm border-0">
      <div class="card-body p-4">
        <div class="table-responsive">
          <table class="table table-hover table-bordered align-middle text-center">
            <thead class="table-primary">
              <tr>
                <th>Subject</th>
                <th>Chapter</th>
                <th>Quiz</th>
                <th>Score</th>
                <th>Max Score</th>
                <th>Percentage</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="score in scores" :key="score.id">
                <td>{{ score.subject_name }}</td>
                <td>{{ score.chapter_name }}</td>
                <td>{{ score.quiz_name }}</td>
                <td>{{ score.score }}</td>
                <td>{{ score.total_possible_score }}</td>
                <td><span class="badge bg-success">{{ score.percentage }}%</span></td>
                <td>{{ formatDate(score.date) }}</td>
              </tr>
              <tr v-if="scores.length === 0">
                <td colspan="7">No results available</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Buttons -->
    <div class="text-center mt-4 d-flex justify-content-center gap-3">
      <button class="btn btn-success px-4" @click="exportScores">
        <i class="bi bi-download me-1"></i> Export as CSV
      </button>
      <button class="btn btn-outline-primary px-4" @click="goBack">
        <i class="bi bi-arrow-left me-1"></i> Back
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      scores: [],
    };
  },
  methods: {
    fetchScores() {
      fetch('http://127.0.0.1:5000/user_result', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'authorization': 'Bearer ' + localStorage.getItem('user_token'),
        },
      })
        .then(response => response.json())
        .then(data => {
          this.scores = data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    exportScores() {
      fetch('http://127.0.0.1:5000/export_details', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'authorization': 'Bearer ' + localStorage.getItem('user_token'),
        },
      })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
        })
        .catch(error => {
          console.error(error);
        });
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
      });
    },
    goBack() {
      this.$router.back(); // If using Vue Router
      // or use: window.history.back();
    },
  },
  mounted() {
    this.fetchScores();
  },
};
</script>
