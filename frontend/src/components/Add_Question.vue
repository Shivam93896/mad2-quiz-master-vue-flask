<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" >Admin Panel</a>
      </div>
    </nav>

    <!-- Main Container -->
    <div class="container py-5">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="text-primary fw-bold">Add Question</h2>
        <button class="btn btn-outline-secondary" @click="$router.go(-1)">⬅ Back</button>
      </div>

      <form @submit.prevent="addQuestion" class="bg-light p-4 rounded shadow-sm">
        <div class="row">
          <div class="col-md-12 mb-3">
            <label for="question" class="form-label fw-semibold">Question</label>
            <input type="text" class="form-control" id="question" v-model="newQuestion.question_tag" placeholder="Enter question" required>
          </div>

          <div class="col-md-12 mb-3">
            <label for="state" class="form-label fw-semibold">Question State</label>
            <input type="text" class="form-control" id="state" v-model="newQuestion.question_state" placeholder="Enter question state" required>
          </div>

          <div class="col-md-6 mb-3">
            <label for="option1" class="form-label">Option A</label>
            <input type="text" class="form-control" id="option1" v-model="newQuestion.option1" placeholder="Enter option A" required>
          </div>

          <div class="col-md-6 mb-3">
            <label for="option2" class="form-label">Option B</label>
            <input type="text" class="form-control" id="option2" v-model="newQuestion.option2" placeholder="Enter option B" required>
          </div>

          <div class="col-md-6 mb-3">
            <label for="option3" class="form-label">Option C</label>
            <input type="text" class="form-control" id="option3" v-model="newQuestion.option3" placeholder="Enter option C" required>
          </div>

          <div class="col-md-6 mb-3">
            <label for="option4" class="form-label">Option D</label>
            <input type="text" class="form-control" id="option4" v-model="newQuestion.option4" placeholder="Enter option D" required>
          </div>

          <div class="col-md-12 mb-4">
            <label for="answer" class="form-label fw-semibold">Correct Answer</label>
            <select class="form-select" id="answer" v-model="newQuestion.correct_option" required>
              <option value="" disabled selected>Select correct answer</option>
              <option value="option1">Option A</option>
              <option value="option2">Option B</option>
              <option value="option3">Option C</option>
              <option value="option4">Option D</option>
            </select>
          </div>
        </div>

        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
          <button type="submit" class="btn btn-success me-md-2">Add Question</button>
          <button type="reset" class="btn btn-secondary" @click="resetForm">Reset</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newQuestion: {
        question_tag: '',
        question_state: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: ''
      }
    };
  },
  methods: {
    addQuestion() {
      fetch(`mad2-quiz-master-vue-flask-7.onrender.com/add_question/${this.$route.params.quiz_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.newQuestion)
      })
        .then(response => response.json())
        .then(data => {
          if (data.message) {
            alert(data.message);
            this.resetForm();
            this.$router.push('/manage_quiz');
          }
        })
        .catch(error => {
          console.error('Error adding question:', error);
        });
    },
    resetForm() {
      this.newQuestion = {
        question_tag: '',
        question_state: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: ''
      };
    }
  }
};
</script>

<style scoped>
form label {
  font-weight: 500;
}
</style>
